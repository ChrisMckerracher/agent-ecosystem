---
name: product
description: Use when writing product briefs, Gherkin feature specs, validating designs against user goals, or analyzing what user-facing problem a codebase solves.
---

# Product

Use this skill to keep work tied to user value and observable behavior.

## Operating Rules

- Prefer docs, specs, briefs, and spelunk flow reports over raw source inspection.
- Use web research only when current market, API, legal, pricing, or external product facts matter.
- For broad codebase understanding, use `$spelunk --for=product` and analyze generated flow docs.
- Write durable artifacts under `docs/plans/product/` or `docs/specs/features/`.

## Default Routing

- "spec", "gherkin", "BDD", "feature behavior": write a feature spec.
- "brief", "PRD", "requirements": write a product brief.
- "validate", "check design", "design review": validate a design.
- "what does this do", "user flows", "product gaps": examine via spelunk.

## Feature Spec Workflow

1. Identify users, goals, key workflows, and expected outcomes.
2. Draft Gherkin scenarios for happy paths, alternatives, errors, and edge cases.
3. Write the spec to `docs/specs/features/<feature-name>.feature`.
4. Run `$qa` in the current session to review the spec, or delegate only if the current Codex runtime exposes an explicit delegation tool and the user has allowed it.
5. Iterate until scenarios are clear, testable, and implementation-independent.

Use this shape:

```gherkin
Feature: <Feature Name>
  As a <persona>
  I want <capability>
  So that <benefit>

  Scenario: <Descriptive behavior>
    Given <precondition>
    When <action>
    Then <observable outcome>
```

## Brief Workflow

Write `docs/plans/product/briefs/<feature-name>.md` with:

- Problem and target users.
- Current workflow or pain.
- Goals and non-goals.
- Success metrics or acceptance signals.
- Constraints, risks, and open questions.

## Design Validation Workflow

1. Read the design doc and any relevant brief/spec.
2. Check whether the design satisfies stated user outcomes.
3. Identify missing behaviors, unclear edge cases, UX regressions, and scope creep.
4. Write `docs/plans/product/validations/<feature-name>.md` with approve/revise/block verdict.

## Examine Workflow

1. Use `$spelunk --for=product --focus="<area>"` for flow discovery.
2. Read the generated `docs/spelunk/flows/` reports.
3. Summarize user-facing workflows, gaps, risks, and likely product intent.
