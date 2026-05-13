---
name: task-complete
description: Use when finishing a beads task by committing work, merging the task branch to its epic, rebasing dependent tasks, closing the bead, and preparing pushed session handoff.
---

# Task Complete

Use this skill for the final task lifecycle step in merge-tree workflows.

## Preconditions

- The task implementation is complete.
- Required tests, lint, build, review, and security checks have passed or their gaps are documented.
- The working tree contains only intended task changes.
- The task branch and epic branch are known.

## Preferred Script

If `scripts/task-complete.sh` exists, use it from the repo root. Prefer the script whenever dependent task branches may need rebasing:

```bash
scripts/task-complete.sh <task-id>
```

The script should:

1. Validate the bead exists and is open.
2. Derive the epic ID from the task ID.
3. Commit pending task work.
4. Merge task branch into the epic branch.
5. Rebase dependent task branches.
6. Close the bead.
7. Return JSON status.

## Manual Fallback

The fallback below is merge-only. Use it only when there are no dependent branches to rebase, or after explicitly deciding to defer dependent rebases to a follow-up bead.

```bash
project_root=$(git rev-parse --show-toplevel)
epic_id="${task_id%%.*}"

cd "${project_root}/.worktrees/${task_id}"
git status --short
# Inspect the diff and stage only intended task files.
git diff
git add <intended-files>
git commit -m "Complete ${task_id}: <description>"

cd "${project_root}/.worktrees/${epic_id}"
git checkout "epic/${epic_id}"
git merge --no-ff "task/${task_id}" -m "Merge ${task_id}"

cd "$project_root"
git worktree remove ".worktrees/${task_id}"
git branch -d "task/${task_id}"
bd close "$task_id" --reason "Merged to epic"
```

Before staging, stop if `git status --short` shows unexpected or unrelated changes. Do not use `git add -A` unless every changed file has been inspected and confirmed in-scope.

If dependent tasks exist, either run `scripts/task-complete.sh` or rebase each dependent task branch onto the updated epic branch before closing the session:

```bash
bd show "$task_id" --json
cd "${project_root}/.worktrees/${epic_id}"
git checkout "task/${dependent_id}"
git rebase "epic/${epic_id}"
```

## Conflict Handling

- If merge conflicts occur, stop and report the conflicted files.
- Do not close the bead until the merge succeeds.
- Record conflict details in bead notes.
- Create a follow-up bead if resolution is not part of the current scope.

## Session Close

Follow repo instructions for finalization. In this repo, work is not complete until changes are committed and `git push` succeeds.
