---
name: visualize
description: Use when showing the current beads task tree, progress, blocked work, ready tasks, or merge-tree state in a concise human-readable format.
---

# Visualize

Use this skill to make beads state easy to scan.

## Inputs

Use:

```bash
bd list --json
bd ready --json
bd blocked --json
bd show <id> --json
```

If a tree command is available in the installed beads version, use it; otherwise assemble the tree from dependency data.

## Output Shape

```text
Feature: <name>
Progress: 3/8 complete | 2 ready | 3 blocked

Tree
- [x] Task A - Login form
- [~] Task B - API endpoint
- [ ] Task C - Integration (blocked by Task B)

Ready
- <id>: <title>

Blocked
- <id>: waiting on <blockers>
```

## Legend

- `[x]`: closed.
- `[~]`: in progress.
- `[ ]`: open.
- `(blocked by X)`: has unmet dependencies.

## Rules

- Keep output human-readable; do not dump raw JSON unless requested.
- Highlight the next ready task.
- Include branch/worktree path when it matters for implementation.
- Mention stale or inconsistent bead state if dependencies and branches do not match.
