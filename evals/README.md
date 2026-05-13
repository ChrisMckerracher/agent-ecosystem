# Evals

End-to-end evaluation harness for agent-ecosystem skills and commands.

Three planned tiers:

| Tier | What | Tool | Status |
|------|------|------|--------|
| 1 | Skill trigger-rate eval | Vendored Anthropic `skill-creator` pipeline | **Implemented** |
| 2 | Command output-quality eval | Promptfoo + `claude-agent-sdk` provider | Pending |
| 3 | End-to-end agent loop eval | `inspect_swe` SWE-bench-style harness | Pending (stretch) |

## Tier 1: Skill trigger-rate eval

Measures, for each skill: given a realistic user prompt, does Claude actually
read the skill? We test positive prompts (should trigger) and negative
near-miss prompts (should NOT trigger).

### Pass criteria

Per skill:

  - **positive_trigger_rate ≥ 60%** — across all `should_trigger=true` queries
  - **false_positive_rate ≤ 10%** — across all `should_trigger=false` queries

### Layout

```
evals/
├── eval-sets/              ← 13 JSON eval sets, one per skill (10 pos + 10 neg)
│   ├── architect.json
│   ├── code.json
│   └── ...
├── results/
│   └── skill-trigger-rates.json   ← aggregator output (generated)
├── skill-creator/
│   ├── LICENSE.txt         ← Apache 2.0
│   ├── NOTICE.md           ← attribution + upstream commit hash
│   └── scripts/
│       ├── run_eval.py     ← VENDORED (Anthropic)
│       ├── run_loop.py     ← VENDORED
│       ├── improve_description.py  ← VENDORED
│       ├── generate_report.py      ← VENDORED
│       ├── utils.py        ← VENDORED
│       └── aggregate_skills.py     ← LOCAL — fans out + aggregates
└── README.md  (this file)
```

### Running

Requires the `claude` CLI on PATH.

```bash
# Run all skills (~30-60 min wall-clock at 3 runs/query)
./scripts/eval-skills.sh

# Restrict to specific skills
./scripts/eval-skills.sh architect code

# Tune cost / runtime (fewer runs/query reduces statistical confidence)
RUNS_PER_QUERY=1 TIMEOUT=20 ./scripts/eval-skills.sh

# Lower concurrency to avoid Anthropic API rate limits — recommended for a
# full 13-skill run on a personal API key.
NUM_WORKERS=3 ./scripts/eval-skills.sh

# Override the model (defaults to whatever `claude` picks)
MODEL=claude-opus-4-7 ./scripts/eval-skills.sh
```

Output lands in `evals/results/skill-trigger-rates.json`. The script exits
non-zero if any skill misses the thresholds — suitable for CI gating.

#### Rate-limit caveat

The default `NUM_WORKERS=10` will spawn 10 concurrent `claude -p` processes,
each hitting the Anthropic API. On a personal API key, a full 13-skill run at
this concurrency **will trip rate limits partway through**, producing 0%/0%
"results" for the later skills that are actually subprocess aborts. Symptoms
to look for in the output table:

  - Elapsed time per skill drops to ~27-30s (vs the 80-170s expected per skill)
  - Trigger rates collapse to 0% across both positive and negative queries

If you see this, either:

  - Re-run with `NUM_WORKERS=2` or `NUM_WORKERS=3` (slower but reliable), or
  - Wait until the rate-limit window resets and re-run

The result file is annotated with a top-level `_run_status` field — if it
reads `"rate_limited"`, the numbers below are partial signal at best. See the
inaugural rate-limited run committed at `evals/results/skill-trigger-rates.json`
and the follow-up bead `claude_stuff-e6r` for context.

### Side-effect isolation

`claude -p` subprocesses can write files in their cwd in response to certain
queries (e.g., a "write me parseConfig" query may land an actual `src/config.ts`).
`run_eval_installed.py` runs each query in a `tempfile.mkdtemp(prefix="claude-eval-")`
sandbox that is removed in `finally`, so the worktree stays clean. Installed
plugins still load because they're user-scoped (`~/.claude/plugins/`).

### Excluded skills

  - **`spelunk`** — `skills/spelunk/SKILL.md` has no YAML frontmatter, so it
    cannot trigger as a skill at all. Filed as bug `claude_stuff-4yo`. Add a
    `spelunk.json` eval set after the frontmatter is added.

### Authoring eval sets

Each eval set is a JSON array of `{"query": "...", "should_trigger": bool}`.
Aim for **10 positive + 10 negative** queries per skill.

Guidance (from upstream `skill-creator/SKILL.md`):

  - **Substantive queries.** Skills are only consulted for tasks Claude can't
    handle on its own. Simple one-step queries ("read file X") will *not*
    trigger any skill regardless of description quality.
  - **Realistic phrasing.** Mix formal and casual; include cases where the
    user doesn't explicitly name the skill or feature.
  - **Near-miss negatives.** The negative cases that bite are the ones that
    share keywords but actually need a different tool. `"decompose this
    matrix"` is a stronger negative for `/decompose` than `"write a haiku"`.

### Iterating on a failing skill

If a skill fails the threshold, use the upstream `run_loop.py` to
auto-rewrite the description across 5 iterations with a 60/40 train/test
split:

```bash
cd evals/skill-creator
python3 -m scripts.run_loop \
  --eval-set ../eval-sets/<skill>.json \
  --skill-path ../../skills/<skill> \
  --model claude-opus-4-7 \
  --max-iterations 5 \
  --verbose
```

Output includes `best_description` selected by **test** score (not train), so
overfitting is mitigated. Take that description and update the skill's
SKILL.md frontmatter manually — the loop does not write back.

## Attribution

See `evals/skill-creator/NOTICE.md` for upstream commit hash and license terms
(Apache 2.0).
