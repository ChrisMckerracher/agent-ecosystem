---
name: code
description: Use when implementing beads tasks, making code changes, running tests, or understanding code relationships directly in a Codex coding session.
---

# Code

Use this skill for implementation work. Keep the critical path local, use subagents only for bounded parallel work when the user has allowed delegation, and preserve user changes.

## Start Work

1. Run `bd show <task-id> --json` or `bd ready` to confirm the task is open and unblocked.
2. Claim the task with `bd update <task-id> --claim`.
3. Read the linked design from `bd show <task-id> --json | jq -r '.design // empty'` when present.
4. Work in the task worktree when one exists: `.worktrees/<task-id>/`.
5. Verify the branch is correct with `git branch --show-current`.

If an unblocked task has no worktree, create it from the current epic branch using the `$decompose` worktree pattern. If the task is blocked, stop and report the blocker.

## Implementation Rules

- Inspect the codebase before editing. Use `rg` and targeted file reads.
- Use TDD when practical: write or update a failing test, implement, then make the test pass.
- Keep changes inside the task scope. If new work appears, create a follow-up bead and link it in notes.
- Do not revert unrelated local changes.
- Use `apply_patch` for manual edits.
- Run the smallest meaningful verification first, then broader checks before completion.

## Delegation

- Use delegation only when the current Codex runtime exposes an explicit delegation tool and the user has allowed subagents.
- If no delegation tool is available, do the work locally or ask the user for direction when the task cannot safely proceed.
- Delegate concrete, non-overlapping work such as "write tests for module X" or "review changed files for security risks".
- Tell worker agents they are not alone in the codebase and must not revert others' changes.
- Review delegated results before merging or committing.

## Completion

1. Run relevant tests, linters, builds, or project verification commands.
2. Commit task work from the task branch.
3. Use `$task-complete` to merge the task to its epic and rebase dependents when the project uses merge-tree worktrees.
4. Close or update the bead with precise status.
5. Push at session end when repository instructions require it.

## Handoff

Report changed behavior, verification run, unresolved risks, and any follow-up bead IDs. Keep the summary short unless the user asks for detail.
