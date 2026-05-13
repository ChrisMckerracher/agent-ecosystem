#!/usr/bin/env python3
"""Trigger-rate eval for ALREADY-INSTALLED plugin skills.

The upstream `run_eval.py` is designed for description-optimization: it copies
a candidate description into a synthetic command file at
`.claude/commands/<name>-skill-<uuid>.md`, runs `claude -p <query>`, and watches
the stream for a Skill/Read tool call against that synthetic name.

That doesn't work when the real skill is already installed under a namespaced
name like `agent-ecosystem:visualize` — Claude invokes the real one, the
synthetic decoy is ignored, and detection returns 0% across the board.

This module is a thin variant that:

  - Does NOT create a synthetic command file
  - Detects triggering by matching the REAL installed skill name(s) — both
    the bare name (`visualize`) and any namespaced form (`*:visualize`)
  - Otherwise reuses the same Popen + stream-event detection as run_eval.py
"""

import argparse
import json
import os
import select
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md


def _matches_skill(arg_value: str, skill_name: str) -> bool:
    """Return True if arg_value is the bare skill name or any namespaced form."""
    if not arg_value:
        return False
    if arg_value == skill_name:
        return True
    # Plugin-qualified: e.g. "agent-ecosystem:visualize"
    if ":" in arg_value and arg_value.split(":", 1)[1] == skill_name:
        return True
    return False


def run_single_query(
    query: str,
    skill_name: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
) -> bool:
    """Run a single query; return True if the named installed skill triggered.

    Triggers detected from stream events (content_block_start with type=tool_use
    name=Skill or Read, then accumulated input_json_delta matching the skill).

    Each query runs in a fresh tmpdir cwd so any files claude -p writes don't
    pollute the worktree. The installed plugins are user-scoped (loaded from
    ~/.claude/plugins/), so this doesn't break skill discovery.
    """
    cmd = [
        "claude",
        "-p", query,
        "--output-format", "stream-json",
        "--verbose",
        "--include-partial-messages",
    ]
    if model:
        cmd.extend(["--model", model])

    # Strip CLAUDECODE so nested claude -p subprocesses don't trip the
    # interactive-terminal guard. (Same workaround as upstream run_eval.py.)
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

    tmpdir = tempfile.mkdtemp(prefix="claude-eval-")
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,  # avoid the 3s "no stdin" warning
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        cwd=tmpdir,
        env=env,
    )

    start_time = time.time()
    buffer = ""
    pending_tool_name = None
    accumulated_json = ""

    try:
        while time.time() - start_time < timeout:
            if process.poll() is not None:
                remaining = process.stdout.read()
                if remaining:
                    buffer += remaining.decode("utf-8", errors="replace")
                break

            ready, _, _ = select.select([process.stdout], [], [], 1.0)
            if not ready:
                continue

            chunk = os.read(process.stdout.fileno(), 8192)
            if not chunk:
                break
            buffer += chunk.decode("utf-8", errors="replace")

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue

                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Early detection via streaming partial messages.
                if event.get("type") == "stream_event":
                    se = event.get("event", {})
                    se_type = se.get("type", "")

                    if se_type == "content_block_start":
                        cb = se.get("content_block", {})
                        if cb.get("type") == "tool_use" and cb.get("name") in ("Skill", "Read"):
                            pending_tool_name = cb.get("name")
                            accumulated_json = ""

                    elif se_type == "content_block_delta" and pending_tool_name:
                        delta = se.get("delta", {})
                        if delta.get("type") == "input_json_delta":
                            accumulated_json += delta.get("partial_json", "")
                            # Try to parse partial JSON heuristically — if the
                            # skill arg is closed (has matching closing quote),
                            # we can decide early.
                            if _check_partial(accumulated_json, skill_name):
                                return True

                    elif se_type in ("content_block_stop", "message_stop"):
                        if pending_tool_name and _check_partial(accumulated_json, skill_name):
                            return True
                        # Reset and keep looking — there might be a later tool call.
                        pending_tool_name = None
                        accumulated_json = ""

                # Fallback: parse the full assistant message.
                elif event.get("type") == "assistant":
                    message = event.get("message", {})
                    for content_item in message.get("content", []):
                        if content_item.get("type") != "tool_use":
                            continue
                        tool_name = content_item.get("name", "")
                        tool_input = content_item.get("input", {})
                        if tool_name == "Skill":
                            if _matches_skill(tool_input.get("skill", ""), skill_name):
                                return True
                        elif tool_name == "Read":
                            fp = tool_input.get("file_path", "")
                            # SKILL.md reads are also a trigger signal — check if
                            # the path ends in /<skill_name>/SKILL.md.
                            if fp.rstrip("/").endswith(f"/{skill_name}/SKILL.md"):
                                return True

                elif event.get("type") == "result":
                    return False
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        shutil.rmtree(tmpdir, ignore_errors=True)

    return False


def _check_partial(accumulated_json: str, skill_name: str) -> bool:
    """Best-effort check on partial JSON. Looks for the closed skill string."""
    # Match "skill": "...:<name>" or "skill": "<name>" with the closing quote present.
    # Bare name match
    if f'"{skill_name}"' in accumulated_json:
        return True
    # Namespaced match (e.g. agent-ecosystem:visualize)
    if f':{skill_name}"' in accumulated_json:
        return True
    # SKILL.md path match for Read
    if f'/{skill_name}/SKILL.md' in accumulated_json:
        return True
    return False


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
) -> dict:
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            query_triggers.setdefault(query, [])
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        did_pass = (trigger_rate >= trigger_threshold) if should_trigger else (trigger_rate < trigger_threshold)
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {"total": len(results), "passed": passed, "failed": len(results) - passed},
    }


def main():
    p = argparse.ArgumentParser(description="Trigger eval for an installed plugin skill")
    p.add_argument("--eval-set", required=True)
    p.add_argument("--skill-path", required=True)
    p.add_argument("--num-workers", type=int, default=10)
    p.add_argument("--timeout", type=int, default=30)
    p.add_argument("--runs-per-query", type=int, default=3)
    p.add_argument("--trigger-threshold", type=float, default=0.5)
    p.add_argument("--model", default=None)
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    skill_path = Path(args.skill_path)
    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md at {skill_path}", file=sys.stderr)
        sys.exit(1)

    name, description, _ = parse_skill_md(skill_path)
    eval_set = json.loads(Path(args.eval_set).read_text())

    # cwd of the spawned `claude -p` matters — it determines which
    # `.claude/commands/` and which plugins are loaded.
    project_root = skill_path.resolve().parent.parent

    if args.verbose:
        print(f"Evaluating installed skill: {name}", file=sys.stderr)
        print(f"Description: {description}", file=sys.stderr)
        print(f"Project root for claude -p: {project_root}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
    )

    if args.verbose:
        s = output["summary"]
        print(f"Results: {s['passed']}/{s['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            print(f"  [{status}] {r['triggers']}/{r['runs']} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
