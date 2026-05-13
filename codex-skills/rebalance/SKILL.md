---
name: rebalance
description: Use when beads tasks are too large, too small, poorly ordered, blocked incorrectly, or need restructuring to keep a merge tree reviewable.
---

# Rebalance

Use this skill to repair task trees before implementation cost compounds.

## Triggers

- Estimated task size exceeds 500 changed lines.
- Estimated task size exceeds 1000 changed lines, which must be split.
- Several tiny tasks under 50 lines each add coordination overhead without useful isolation.
- A task mixes unrelated files, layers, or behaviors.
- Dependencies force unsafe ordering.

## Process

1. Inspect the bead tree with `bd show <id> --json`, `bd ready`, and dependency listings.
2. Identify natural split or merge boundaries.
3. Preserve the original design doc linkage with `--design`.
4. Create child tasks or replacement tasks with clear acceptance criteria.
5. Update dependencies so each task starts only after required upstream changes exist.
6. Close or supersede obsolete beads with a reason.

## Commands

```bash
bd create "Subtask title" -t task -p 1 --design="<design-path>" -d "<scope>" --json
bd dep add <parent-id> <child-id>
bd dep add <dependent-id> <blocker-id>
bd update <parent-id> -t epic
bd close <old-id> --reason "Superseded by <new-id>"
```

## Output

Report before/after task shape, dependency changes, ready work, and any obsolete bead IDs.
