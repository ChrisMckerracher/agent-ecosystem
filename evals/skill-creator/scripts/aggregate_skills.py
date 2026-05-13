#!/usr/bin/env python3
"""Run trigger-rate eval across all agent-ecosystem skills and aggregate results.

For each skill that has both a SKILL.md (with frontmatter) and an eval-set JSON,
shells out to run_eval.py, parses the per-query results, and computes:

  - positive_trigger_rate: triggers / runs across should_trigger=true queries
  - false_positive_rate:   triggers / runs across should_trigger=false queries
  - pass:                  positive >= POS_THRESHOLD AND fp <= FP_THRESHOLD

Writes the aggregate to evals/results/skill-trigger-rates.json and prints a
human-readable summary table to stderr.

Usage:
  python -m evals.skill-creator.scripts.aggregate_skills \\
      --runs-per-query 3 \\
      --output evals/results/skill-trigger-rates.json
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

POS_THRESHOLD = 0.60
FP_THRESHOLD = 0.10


def find_repo_root() -> Path:
    """Walk up from this file looking for .claude-plugin/plugin.json."""
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / ".claude-plugin" / "plugin.json").is_file():
            return parent
    raise SystemExit("Could not locate repo root (no .claude-plugin/plugin.json found)")


def aggregate_results(results: list[dict]) -> dict:
    """Compute pos-trigger-rate and fp-rate from a list of per-query result dicts."""
    pos_runs = pos_triggers = 0
    neg_runs = neg_triggers = 0
    for r in results:
        if r["should_trigger"]:
            pos_runs += r["runs"]
            pos_triggers += r["triggers"]
        else:
            neg_runs += r["runs"]
            neg_triggers += r["triggers"]
    pos_rate = pos_triggers / pos_runs if pos_runs else 0.0
    fp_rate = neg_triggers / neg_runs if neg_runs else 0.0
    return {
        "positive_trigger_rate": pos_rate,
        "false_positive_rate": fp_rate,
        "positive_triggers": pos_triggers,
        "positive_runs": pos_runs,
        "negative_triggers": neg_triggers,
        "negative_runs": neg_runs,
    }


def run_one_skill(
    skill_name: str,
    skill_path: Path,
    eval_set: Path,
    runs_per_query: int,
    timeout: int,
    num_workers: int,
    model: str | None,
    repo_root: Path,
) -> dict:
    """Invoke run_eval.py as a subprocess and return parsed JSON."""
    script_dir = Path(__file__).resolve().parent
    cmd = [
        sys.executable, "-m", "scripts.run_eval_installed",
        "--eval-set", str(eval_set),
        "--skill-path", str(skill_path),
        "--runs-per-query", str(runs_per_query),
        "--timeout", str(timeout),
        "--num-workers", str(num_workers),
    ]
    if model:
        cmd.extend(["--model", model])

    print(f"  [running] {skill_name}", file=sys.stderr, flush=True)
    t0 = time.time()
    proc = subprocess.run(
        cmd,
        cwd=script_dir.parent,  # evals/skill-creator/ — so `-m scripts.run_eval` resolves
        capture_output=True,
        text=True,
    )
    elapsed = time.time() - t0

    if proc.returncode != 0:
        return {
            "skill": skill_name,
            "error": f"run_eval exited {proc.returncode}",
            "stderr": proc.stderr[-2000:],
            "elapsed_seconds": elapsed,
        }

    try:
        output = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        return {
            "skill": skill_name,
            "error": f"could not parse run_eval JSON output: {e}",
            "stdout_tail": proc.stdout[-2000:],
            "stderr_tail": proc.stderr[-2000:],
            "elapsed_seconds": elapsed,
        }

    agg = aggregate_results(output["results"])
    pos_ok = agg["positive_trigger_rate"] >= POS_THRESHOLD
    fp_ok = agg["false_positive_rate"] <= FP_THRESHOLD
    return {
        "skill": skill_name,
        "description": output["description"],
        "elapsed_seconds": elapsed,
        **agg,
        "pos_threshold": POS_THRESHOLD,
        "fp_threshold": FP_THRESHOLD,
        "pass_positive": pos_ok,
        "pass_false_positive": fp_ok,
        "pass": pos_ok and fp_ok,
        "per_query": output["results"],
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger eval across all skills")
    parser.add_argument("--runs-per-query", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--num-workers", type=int, default=10)
    parser.add_argument("--model", default=None, help="claude -p --model override")
    parser.add_argument("--output", default="evals/results/skill-trigger-rates.json")
    parser.add_argument("--skill", action="append", default=None,
                        help="Restrict to this skill (repeatable). Default: all eval sets.")
    args = parser.parse_args()

    repo_root = find_repo_root()
    eval_sets_dir = repo_root / "evals" / "eval-sets"
    skills_dir = repo_root / "skills"

    available = sorted(p.stem for p in eval_sets_dir.glob("*.json"))
    selected = args.skill or available

    print(f"Running trigger eval for {len(selected)} skill(s): {', '.join(selected)}",
          file=sys.stderr)
    print(f"  runs/query={args.runs_per_query}  timeout={args.timeout}s  "
          f"workers={args.num_workers}", file=sys.stderr)

    per_skill = []
    skipped = []
    for skill_name in selected:
        skill_path = skills_dir / skill_name
        eval_set = eval_sets_dir / f"{skill_name}.json"

        if not (skill_path / "SKILL.md").exists():
            skipped.append({"skill": skill_name, "reason": "no SKILL.md"})
            print(f"  [skip] {skill_name}: no SKILL.md", file=sys.stderr)
            continue
        if not eval_set.exists():
            skipped.append({"skill": skill_name, "reason": "no eval set"})
            print(f"  [skip] {skill_name}: no eval set", file=sys.stderr)
            continue

        # Pre-check: SKILL.md needs frontmatter for the description to be parsed.
        skill_md_head = (skill_path / "SKILL.md").read_text().splitlines()[:1]
        if not skill_md_head or skill_md_head[0].strip() != "---":
            skipped.append({"skill": skill_name, "reason": "SKILL.md missing frontmatter"})
            print(f"  [skip] {skill_name}: SKILL.md missing frontmatter (cannot trigger)",
                  file=sys.stderr)
            continue

        per_skill.append(run_one_skill(
            skill_name=skill_name,
            skill_path=skill_path,
            eval_set=eval_set,
            runs_per_query=args.runs_per_query,
            timeout=args.timeout,
            num_workers=args.num_workers,
            model=args.model,
            repo_root=repo_root,
        ))

    summary = {
        "pos_threshold": POS_THRESHOLD,
        "fp_threshold": FP_THRESHOLD,
        "runs_per_query": args.runs_per_query,
        "model": args.model,
        "evaluated": len(per_skill),
        "skipped": skipped,
        "results": per_skill,
    }
    summary["passed"] = sum(1 for r in per_skill if r.get("pass"))
    summary["failed"] = sum(1 for r in per_skill if not r.get("pass") and "error" not in r)
    summary["errored"] = sum(1 for r in per_skill if "error" in r)

    out_path = repo_root / args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2))

    print("", file=sys.stderr)
    print(f"{'SKILL':<20} {'POS':>8} {'FP':>8} {'TIME':>8}  STATUS", file=sys.stderr)
    print("-" * 64, file=sys.stderr)
    for r in per_skill:
        if "error" in r:
            print(f"{r['skill']:<20} {'-':>8} {'-':>8} {r['elapsed_seconds']:>7.1f}s  "
                  f"ERROR: {r['error']}", file=sys.stderr)
            continue
        status = "PASS" if r["pass"] else "FAIL"
        if not r["pass_positive"]:
            status += " (pos<60%)"
        if not r["pass_false_positive"]:
            status += " (fp>10%)"
        print(f"{r['skill']:<20} {r['positive_trigger_rate']:>7.0%} "
              f"{r['false_positive_rate']:>7.0%} {r['elapsed_seconds']:>7.1f}s  "
              f"{status}", file=sys.stderr)

    print("", file=sys.stderr)
    print(f"Summary: evaluated={summary['evaluated']}  "
          f"passed={summary['passed']}  failed={summary['failed']}  "
          f"errored={summary['errored']}  skipped={len(skipped)}", file=sys.stderr)
    print(f"Results written to: {out_path}", file=sys.stderr)

    # Exit non-zero if any failed (for CI gating)
    if summary["failed"] > 0 or summary["errored"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
