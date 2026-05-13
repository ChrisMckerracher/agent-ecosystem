---
description: Route new conventions/feedback into the right standards file (or create a new one); never dumps into CLAUDE.md
allowed-tools: ["Read", "Edit", "Write", "Glob", "AskUserQuestion"]
argument-hint: "[<feedback or convention to add>]"
---

# /update-harness

Add new conventions, patterns, or feedback to the **right** harness file. The
detailed standards playbook means feedback should land in the *most specific*
file rather than being dumped into `CLAUDE.md`.

## Precheck

1. If `docs/standards/` does not exist, the harness hasn't been scaffolded.
   Tell the user: "Run `/init-harness` first to scaffold the standards
   playbook." Offer to append to `CLAUDE.md` as a one-time fallback for this
   invocation. Do not silently fall back.

## Routing decision

For each piece of feedback, classify by axis and route to the matching file:

| Feedback axis | Target file |
|---|---|
| Architecture / boundaries / helper sharing / state resolution | `docs/standards/engineering.md` |
| Test discipline / regression coverage / fixtures | `docs/standards/testing.md` |
| Docs hygiene / verification commands / archive policy | `docs/standards/documentation.md` |
| Workflow / beads / worktrees / spec-first / agent patience | `docs/standards/workflow.md` |
| Python-specific | `docs/standards/python.md` |
| TypeScript-specific | `docs/standards/typescript.md` |
| Read order / standards index / meta-process | `AGENTS.md` |

**If no existing axis fits:** propose creating a new `docs/standards/<axis>.md`.
Common new axes: `security`, `observability`, `deployment`, `data`,
`api-design`, `performance`. Always ask the user to confirm the axis name and
filename before creating.

**If multiple axes plausible:** pick the most specific. Mention the
runner(s)-up in the approval diff so the user can redirect.

## Process

1. Read the relevant existing standards files to understand what's already there.
2. Classify the feedback per the routing table.
3. If routing to an existing file: identify the right section (or propose a
   new section). Append the new rule as the next integer in that section's
   numbered list — **never renumber existing rules** (citations like
   `engineering.md > Architecture §10` would break).
4. If routing to a NEW file: ask the user to confirm the axis and filename
   first, then create the file with a brief Purpose header and the first rule.
5. Show the diff. Apply only on explicit approval.
6. If a new standards file was created, also update `AGENTS.md`'s Standards
   Index to add the new entry.

## Format requirements

- 1-sentence numbered rule (matches existing format in `docs/standards/*.md`).
- Positive responsibility statement ("Do X" rather than "Don't do Y" unless
  preventing a specific boundary mistake).
- Concrete enough to cite in a PR review.
- No project-specific filenames or APIs unless the rule genuinely binds to
  them.

## Examples

### Route to existing file
Input: "We should always use structured logging via pino, not console.log."
Routing: `docs/standards/typescript.md` (TS-specific)
Append: `9. Use structured logging via the chosen library; do not use console.log in production code.`

### Create a new file
Input: "All API endpoints must require auth and rate-limit per user."
Routing: No existing axis fits → ask: "I'd propose creating
`docs/standards/api-design.md`. Confirm filename?"
After confirmation: create file with `Purpose` header + the rule as §1.
Also append `- API Design: \`docs/standards/api-design.md\`` to AGENTS.md's
Standards Index.

### Update AGENTS.md directly
Input: "Agents should run spelunk before implementing any task."
Routing: `AGENTS.md` (meta-process about agent flow, not a specific code
convention).

## Safety

- Always show diff before apply.
- Never renumber existing rules (breaks `<file> > <section> §N` citations).
- Never write to `docs/archive/**` (read-only history per documentation §4).
- If feedback contradicts an existing rule, do not silently overwrite. Raise
  the contradiction explicitly and ask which rule wins.
- Commit harness updates as their own commit so the diff is easy to review.
