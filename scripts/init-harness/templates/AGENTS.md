# AGENTS.md

## Purpose
This is the repo entry point for humans and agents.

Read this file first, then use `docs/` as the current system of record for repo standards and reference material.

## Required Read Order
1. `AGENTS.md`
2. `docs/README.md`
3. `docs/repo-map.md`
4. the task's design doc under `docs/plans/architect/`
5. task-relevant standards in `docs/standards/`
6. task-relevant audits or spelunks under `docs/spelunk/`

## Non-Negotiable Operating Rules
1. Prefer clarity over cleverness.
2. Keep one clear owner per concern and keep orchestration easy to trace end to end.
3. Do not introduce abstraction layers just in case; generalize only when multiple real backers or implementations exist.
4. When one concrete backing system is chosen, design directly to its native semantics.
5. Keep canonical domain models at boundaries; avoid duplicate `*Request` / `*Response` wrappers unless the external shape truly differs.
6. If a package exposes `contracts/`, it must only re-export approved canonical boundary models.
7. Diagnose failing tests before changing code or tests; do not brute-force them into passing.
8. Update docs when contracts or behavior change.
9. When you change something runnable, include copy-paste repo commands to verify it locally.
10. When helper concerns are shared across multiple real package owners, prefer one shared library over copy-pasted per-package helpers.
11. For repeated seams, prefer decorators and shared helper functions when they preserve explicit ownership and traceability; do not hand-roll near-identical wrapper code in every package.
12. When a concern has both shared primitives and package-owned semantics, keep the shared primitives in the shared library and the package-owned semantics in a dedicated package-local subpackage.

## Beads Workflow Rules
1. Every implementation task must be a bead tied to the active design doc with the bead `--design` field set.
2. Use one agent per task bead.
3. Use one git worktree per task bead.
4. Create task worktrees from the current epic branch.
5. Only create worktrees for ready, unblocked tasks.
6. Execute an epic through task agents, not by freehand jumping between worktrees:
   one agent takes one ready task bead, works only in that task worktree, and carries it through implementation and verification before merge-up.
7. Do not start the next task bead until the current task bead has been reviewed and merged into the epic branch, unless another ready task was intentionally delegated to its own separate agent already.
8. When a task is done, review it, merge it into the epic branch, then branch newly unblocked tasks from that updated epic.
9. Do not ask the user for input while an epic is in progress unless there is a true hard blocker or destructive decision.
10. If you delegate relevant work to sub-agents, wait for them to finish before synthesizing or moving the design forward.
11. Do not interrupt or redirect a task agent just because it has been quiet for a few minutes; assume a normal task may take 20-30 minutes of silent work before first reviewable output.
12. Do not mark a task bead `in_progress` unless that task's agent is actually working it.
13. For any substantial new implementation effort, use a spec-first epic bootstrap:
    write or tighten the design doc first, create the epic bead against that doc, branch the epic worktree, then decompose into task beads and task worktrees before coding.
14. Treat that spec-first epic bootstrap as the default operating mode, not as special ceremony.

## Standards Index
- Engineering: `docs/standards/engineering.md`
- Testing: `docs/standards/testing.md`
- Documentation: `docs/standards/documentation.md`
- Workflow: `docs/standards/workflow.md`

## Repo Reference
- Current docs home: `docs/README.md`
- Repo map: `docs/repo-map.md`
- Active design docs: `docs/plans/architect/`
- Audits and spelunks: `docs/spelunk/`
- Archived docs: `docs/archive/` when present, treated as read-only history
