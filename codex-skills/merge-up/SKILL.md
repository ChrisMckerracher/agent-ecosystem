---
name: merge-up
description: Use when completed task branches need to merge upward into their epic branch, when epics need to merge back to the active branch, or when beads dependency state must be updated after merges.
---

# Merge Up

Use this skill to keep merge-tree branches, worktrees, and beads state aligned.

## Preconditions

- Child task work is committed.
- Relevant tests or review gates have passed.
- No unresolved merge is in progress.
- The target parent branch is known.

Check merge state first:

```bash
test ! -f "$(git rev-parse --git-dir)/MERGE_HEAD" || {
  echo "Unresolved merge in progress"
  exit 1
}
```

## Task To Epic

```bash
project_root=$(dirname "$(git rev-parse --git-common-dir)")
cd "${project_root}/.worktrees/${epic_id}"
git checkout "epic/${epic_id}"
git merge --no-ff "task/${task_id}" -m "Merge ${task_id}"
cd "$project_root"
git worktree remove ".worktrees/${task_id}"
git branch -d "task/${task_id}"
bd close "$task_id" --reason "Merged to epic branch"
```

After closing a task, check for newly unblocked work with `bd ready --json`. Create worktrees for newly unblocked tasks from the updated epic branch.

## Epic To Active Branch

```bash
project_root=$(dirname "$(git rev-parse --git-common-dir)")
active_branch=$(bd --cwd "$project_root" show "$epic_id" --json \
  | jq -r '.labels[]' \
  | grep '^active-branch:' \
  | sed 's/^active-branch://')

cd "$project_root"
git checkout "$active_branch"
git merge --no-ff "epic/${epic_id}" -m "Merge ${epic_id}"
git worktree remove ".worktrees/${epic_id}"
git branch -d "epic/${epic_id}"
bd close "$epic_id" --reason "Merged to ${active_branch}"
```

## Conflict Protocol

1. Stop the automated merge path on conflict.
2. Report conflicting files and the worktree where the conflict occurred.
3. Abort the merge unless you are actively resolving it now.
4. Record the conflict in bead notes.
5. Create a follow-up bead for conflict resolution if it cannot be resolved immediately.

```bash
git merge --abort
bd update "$task_id" --notes "CONFLICT: <files>"
bd create "Resolve merge conflict for ${task_id}" -t task -p 1
```
