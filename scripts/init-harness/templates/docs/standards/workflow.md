# Workflow Standards

## Beads
1. Decompose implementation work into beads tied to the active design doc.
2. Every task bead must set `--design` to the canonical design doc path.
3. Use one agent per task bead.
4. Use one git worktree per task bead.
5. Create task worktrees from the current epic branch.
6. Only create worktrees for ready, unblocked tasks.
7. Execute ready task beads through their assigned agents; one agent owns one task worktree until that task is reviewed and merged.
8. When a task is done, review it, merge it into the epic, then branch newly unblocked work from the updated epic.

## Epic Execution
1. Do not ask the user for input while an epic is in progress unless there is a true hard blocker or destructive decision.
2. Let delegated agents finish before synthesizing or advancing the design.
3. Do not interrupt or redirect a quiet task agent unless there is concrete evidence of a real stall or failure; assume a normal task may take 20-30 minutes of silent work before first reviewable output.
4. Do not mark a task `in_progress` unless that task's agent is actively working it.
5. When tests fail, reason about the real cause before changing code or tests.
6. Start substantial work with a spec-first epic bootstrap:
   - write or tighten the design doc first,
   - create the epic bead tied to that design doc,
   - branch the epic worktree,
   - then decompose into task beads and task worktrees before implementation.
7. Default to that spec-first epic bootstrap unless the change is truly tiny and does not justify an epic.

## Change Reporting
1. Keep responses direct and concrete.
2. Include exact verification commands for runnable changes.
3. Keep the active design doc and supporting docs aligned with behavior changes.
