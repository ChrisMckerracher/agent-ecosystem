---
name: update-harness
description: Use when user feedback should become durable repository operating guidance by updating AGENTS.md or docs/standards instead of ad hoc memory or scattered notes.
---

# Update Harness

Use this skill to route new conventions into the right project guidance file.

## Rules

- Do not dump durable rules into `CLAUDE.md` or `CODEX.md` unless the rule is tool-specific.
- Prefer `AGENTS.md` as the index and `docs/standards/` as the detailed source of truth.
- Never renumber existing standards.
- Do not write to `docs/archive/**`.
- If feedback contradicts an existing rule, surface the contradiction instead of overwriting it.

## Precheck

If `docs/standards/` is absent, recommend running the harness initializer or create a minimal standards structure only with explicit authorization.

## Routing

| Feedback | Target |
|---|---|
| Architecture, boundaries, helper sharing | `docs/standards/engineering.md` |
| Testing, regressions, quality gates | `docs/standards/testing.md` |
| Docs hygiene, verification commands | `docs/standards/documentation.md` |
| Workflow, beads, worktrees, git | `docs/standards/workflow.md` |
| Python-specific rules | `docs/standards/python.md` |
| TypeScript-specific rules | `docs/standards/typescript.md` |
| Read order, standards index, meta-process | `AGENTS.md` |
| No existing axis fits | propose `docs/standards/<axis>.md` |

## Process

1. Classify the feedback by axis.
2. Read the target file.
3. Draft the smallest rule that preserves the user's intent.
4. Show the diff before applying if the user has not already authorized edits.
5. Append as the next numbered rule or update the relevant index entry.
6. If a new standards file is created, add it to `AGENTS.md`.
