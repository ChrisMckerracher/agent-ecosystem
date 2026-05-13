---
name: update-harness
description: Use when you receive feedback that should land in the harness — routes to the right standards file in docs/standards/ or creates a new one when no existing axis fits
---

# /update-harness

Route feedback into the right harness file. Do **not** dump into `CLAUDE.md`.

## Usage

- `/update-harness <feedback>` — Route and apply
- `/update-harness` — Interactive: gather feedback first

## Precheck

If `docs/standards/` is absent, hint that `/init-harness` should run first.
Offer `CLAUDE.md` append as a one-time fallback; do not silently fall back.

## Routing

| Feedback axis | Target |
|---|---|
| Architecture / boundaries / helper sharing | `docs/standards/engineering.md` |
| Testing / regressions | `docs/standards/testing.md` |
| Docs hygiene / verification commands | `docs/standards/documentation.md` |
| Workflow / beads / worktrees | `docs/standards/workflow.md` |
| Python-specific | `docs/standards/python.md` |
| TypeScript-specific | `docs/standards/typescript.md` |
| Read order / meta-process | `AGENTS.md` |
| **No axis fits** | Propose new `docs/standards/<axis>.md`, confirm with user |

When multiple axes apply, pick the most specific; mention the runner-up in
the approval diff.

## Process

1. Classify feedback by axis.
2. Read target file.
3. Append as next-integer rule (never renumber).
4. Show diff.
5. Apply on approval.
6. If a new file was created, add it to `AGENTS.md`'s Standards Index.

## Safety

- Always show diff before apply.
- Never renumber existing rules — citations like `engineering.md > Architecture §10` would break.
- Never write to `docs/archive/**`.
- If feedback contradicts an existing rule, raise the contradiction; do not silently overwrite.
