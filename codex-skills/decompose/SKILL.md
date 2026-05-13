---
name: decompose
description: Use when breaking an approved feature, design, or large task into a beads merge tree with epics, dependencies, branches, and git worktrees.
---

# Decompose

Use this skill to convert an approved design into reviewable implementation units.

## Sizing Rules

- Target about 500 changed lines per task.
- Split any task likely to exceed 1000 lines.
- Prefer boundaries by module, layer, file ownership, migration phase, or independently testable behavior.
- Block integration tasks on the tasks that create the APIs or behavior they consume.

## Epic Creation

```bash
active_branch=$(git branch --show-current)
project_root=$(git rev-parse --show-toplevel)

epic_json=$(bd create "Epic: Feature Name" -t epic -p 0 \
  -d "Description" \
  --design="docs/plans/architect/feature.md" \
  --json)
epic_id=$(echo "$epic_json" | jq -r '.id')

git branch "epic/${epic_id}"
mkdir -p "${project_root}/.worktrees"
git worktree add "${project_root}/.worktrees/${epic_id}" "epic/${epic_id}"
bd update "$epic_id" --add-label "active-branch:${active_branch}"
```

After creating worktrees, check whether `.worktrees/` is ignored. If `.gitignore` needs an entry, announce the tracked-file edit and use `apply_patch` rather than appending from shell.

## Task Creation

Create every task as a bead and make it block the epic:

```bash
epic_design=$(bd show "$epic_id" --json | jq -r '.design // empty')
task_json=$(bd create "Task title" -t task -p 1 \
  -d "Clear implementation scope and acceptance criteria" \
  --design="$epic_design" \
  --json)
task_id=$(echo "$task_json" | jq -r '.id')
bd dep add "$epic_id" "$task_id"
```

For unblocked tasks, immediately create a branch and worktree from the epic branch:

```bash
cd "${project_root}/.worktrees/${epic_id}"
git checkout "epic/${epic_id}"
git checkout -b "task/${task_id}"
cd "$project_root"
git worktree add ".worktrees/${task_id}" "task/${task_id}"
```

For blocked tasks, add blocker dependencies and do not create a branch or worktree yet:

```bash
bd dep add "$task_id" "$blocker_id"
```

Blocked tasks must start from the updated epic branch after dependencies merge.

## Output

Report the tree in plain language:

```text
Feature: Auth System
- middleware: ready
- routes: blocked by middleware
- tests: blocked by middleware, routes

Epic worktree: .worktrees/<epic-id>/
Ready next: <task-id>
```
