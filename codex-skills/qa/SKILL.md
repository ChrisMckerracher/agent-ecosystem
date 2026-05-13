---
name: qa
description: Use when creating tests from specs, generating Playwright end-to-end tests, reviewing feature specs for testability, or analyzing test coverage and test strategy.
---

# QA

Use this skill to turn requirements into testable checks and to identify coverage gaps.

## Operating Rules

- QA may read docs, specs, configs, and test files directly.
- For non-test source analysis, prefer `$spelunk --for=qa` and generated contract docs.
- Keep generated tests aligned with existing test patterns.
- If implementation support is required, create or request a follow-up bead instead of expanding QA scope silently.

## Default Routing

- "generate tests", "write tests", "test for": create tests for the current task or spec.
- "generate-tests", "Playwright", "e2e from spec": generate Playwright tests from Gherkin.
- "coverage", "test patterns", "what tests exist": examine coverage via tests plus spelunk reports.

## Spec Review

Check that each scenario is:

- Observable from user or API behavior.
- Independent of implementation details.
- Clear about preconditions and expected outcomes.
- Covered for success, failure, permission, validation, and boundary cases.

Return approve/revise/block with concrete scenario edits.

## Generate Playwright Tests From Gherkin

1. Read the `.feature` file from `docs/specs/features/`.
2. Parse `Feature`, `Background`, `Scenario`, `Scenario Outline`, and examples.
3. Create `tests/e2e/<feature-name>.spec.ts`.
4. Map `Given` to arrange, `When` to act, and `Then` to assert.
5. Prefer selectors in this order: `data-testid`, accessible role/label, visible text.
6. Note missing test IDs or fixture needs as follow-up implementation work.

Template:

```typescript
import { test, expect } from '@playwright/test';

test.describe('<Feature Name>', () => {
  test.beforeEach(async ({ page }) => {
    // Background setup.
  });

  test('<Scenario Name>', async ({ page }) => {
    // Given
    // When
    // Then
  });
});
```

## Coverage Analysis

1. List existing test files with `rg --files -g '*.{test,spec}.*'`.
2. Read test files and relevant docs.
3. Use `$spelunk --for=qa --focus="<area>"` for source contracts when needed.
4. Compare contracts and behavior specs against existing assertions.
5. Report missing cases with priority and suggested test location.

## Boundaries

QA generates tests, test plans, and coverage findings. Application code, complex fixtures, page objects, and CI changes should be separate implementation tasks unless the user explicitly includes them in scope.
