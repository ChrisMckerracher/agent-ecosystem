# Attribution

The Python scripts in `scripts/` (except `aggregate_skills.py`) are vendored from
Anthropic's open-source `skill-creator` skill:

  - **Source:** https://github.com/anthropics/skills/tree/main/skills/skill-creator
  - **Upstream commit:** `f458cee31a7577a47ba0c9a101976fa599385174`
  - **License:** Apache License 2.0 (see `LICENSE.txt`)

Vendored files (unchanged from upstream):

  - `scripts/run_eval.py`         — measures trigger rate of a skill description
  - `scripts/run_loop.py`         — iterative description-rewrite optimizer (5 rounds)
  - `scripts/improve_description.py` — single-pass description rewriter
  - `scripts/generate_report.py`  — HTML report generator
  - `scripts/utils.py`            — SKILL.md frontmatter parser

Locally-authored:

  - `scripts/aggregate_skills.py` — fans `run_eval.py` out across all our
                                    skills and aggregates pos-rate / fp-rate

If you upgrade the vendored scripts, bump the commit hash above and re-test
`aggregate_skills.py` — it depends on the exact shape of `run_eval.py`'s JSON
output.

## Known upstream behavior

`run_eval.py` invokes `claude -p` per query and strips the `CLAUDECODE`
environment variable. This is the documented workaround for the "claude -p
returns 0% trigger rate from inside a Claude Code session" issue — the env-var
guard is for interactive terminal conflicts, not programmatic subprocess use.

`run_eval.py` works by writing a synthetic command file to
`.claude/commands/<skill-name>-skill-<uuid>.md` carrying the skill's
**description** (not the full SKILL.md body), then watching the stream for a
`Skill` or `Read` tool call against that unique name. This means the eval
measures whether **the description** triggers — it doesn't matter whether the
skill is "really" installed elsewhere.
