---
name: architect
description: Use when starting new features, making architecture decisions, analyzing system structure, writing design docs, or decomposing approved designs into implementation tasks in a Codex workflow.
---

# Architect

Use this skill to turn product intent or technical goals into a concrete design that other Codex sessions can implement safely.

## Operating Rules

- Treat `AGENTS.md` and `docs/standards/` as the source of project rules.
- Prefer existing docs and generated spelunk reports before reading broad source areas.
- For large codebase analysis, generate or refresh focused spelunk docs rather than loading many source files into context.
- Use `bd` for task tracking. Do not create markdown TODO lists.
- Ask for human approval before decomposing a design if the design changes user-visible behavior, architecture boundaries, or migration strategy.

## Default Routing

- New feature, implementation plan, design decision: run the design workflow.
- Architecture analysis, module boundaries, "how is this structured": run examine workflow.
- Break down work, task tree, merge tree: run decompose workflow or hand off to `$decompose`.

## Design Workflow

1. Read `AGENTS.md`, relevant `docs/standards/*`, existing product briefs, feature specs, and related prior design docs.
2. If the request is user-facing and lacks a feature spec, recommend `$product` to write one first. Proceed only if the user asks to skip that step.
3. Gather only the code context needed for design. If the area is broad, use `$spelunk` with `--for=architect` and a narrow `--focus`.
4. Produce a design doc under `docs/plans/architect/<feature-name>.md`.
5. Include problem statement, goals, non-goals, affected modules, data/control flow, implementation plan, test strategy, risks, and open questions.
6. Stop at the approval point before creating tasks unless approval is already explicit.

## Examine Workflow

1. Parse the focus area from the user request.
2. Use `$spelunk` with `--for=architect --focus="<area>"` unless a fresh report already exists.
3. Read only the generated `docs/spelunk/interfaces/` and `docs/spelunk/boundaries/` reports relevant to the focus.
4. Summarize architecture, ownership boundaries, coupling points, extension seams, and likely risks.

## Decompose Workflow

1. Confirm the design doc is approved or explicitly authorized for decomposition.
2. Use `$decompose` to create an epic and task tree with dependencies.
3. Store the design doc path in each bead's `--design` field.
4. Keep tasks near 500 changed lines; split anything likely to exceed 1000 lines.

## Output

- Design docs go in `docs/plans/architect/`.
- Follow-up implementation work goes into beads, not markdown task lists.
- Handoff should name the design doc, key risks, created bead IDs, and the next ready task.
