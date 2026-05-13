---
description: Complete a task — commit, merge to epic, rebase dependents, close the bead
allowed-tools: ["Bash"]
argument-hint: "<task-id>"
---

# Merge Up

Atomically complete a task: commit pending work, merge the task branch to its epic, rebase dependent task branches, and close the bead.

## Usage

```bash
/merge-up <task-id>
```

Example: `/merge-up claude_stuff-abc.1`

## What It Does

Runs `${CLAUDE_PLUGIN_ROOT}/scripts/merge-up.sh <task-id>`, which:

1. Validates the task exists and is open
2. Derives the epic root from the task ID (e.g., `claude_stuff-abc.1` → `claude_stuff-abc`)
3. Navigates to the epic's worktree at `.worktrees/{epic_root}/`
4. Commits any pending changes on the task branch
5. Merges the task branch to the epic branch (aborts on conflict)
6. Rebases all dependent task branches that have this task as a blocker
7. Closes the task bead

See `skills/merge-up/SKILL.md` for the full skill workflow, conflict handling, and recovery procedures.
