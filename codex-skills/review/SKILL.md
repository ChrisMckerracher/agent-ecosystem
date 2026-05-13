---
name: review
description: Use when reviewing code changes, diffs, branches, or epics for correctness, maintainability, regressions, style, missing tests, and project-specific quality gates.
---

# Review

Use this skill with a code-review mindset. Findings come first, ordered by severity, with file and line references.

## Scope

- Review current working tree, a specified diff, a task branch, or an epic branch.
- For epic worktrees, compare the epic branch to its recorded active branch.
- Include project-specific verify cycles when configured.

## Workflow

1. Identify the review target and base.
2. Read `AGENTS.md`, relevant standards, and any linked design/spec.
3. Inspect the diff with `git diff` or `git diff <base>...<branch>`.
4. Look for behavioral bugs, regressions, missing tests, edge cases, security-sensitive changes, and maintainability issues.
5. Run relevant automated checks or explain why they were not run.
6. If security-sensitive code changed, run `$security` or request a security review.

## Epic Review

```bash
project_root=$(dirname "$(git rev-parse --git-common-dir)")
active_branch=$(bd --cwd "$project_root" show "$epic_id" --json \
  | jq -r '.labels[]' \
  | grep '^active-branch:' \
  | sed 's/^active-branch://')
cd "${project_root}/.worktrees/${epic_id}"
git diff "${active_branch}...epic/${epic_id}"
```

## Verify Cycles

Check project-specific cycles in `.codex/verify-cycles/` first. For migrated projects, also check `.claude/verify-cycles/` if that is where the repo's verify-cycle library reads from.

For each relevant cycle:

- Run `Run:` commands for automated cycles.
- Show manual checklist cycles as review requirements.
- When relevance is ambiguous, run or show the cycle.

## Response Format

Start with findings:

```text
Findings
- High: <file:line> <issue and impact>
- Medium: <file:line> <issue and impact>

Open Questions
- <question>

Verification
- <commands run or not run>
```

If there are no findings, say that explicitly and list residual risks or tests not run.
