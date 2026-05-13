---
name: verify
description: Use when creating or running project-specific verification cycles that augment code review with automated commands or manual checklists.
---

# Verify

Use this skill to define quality checks that run during review when relevant.

## Storage

For Codex-first projects, store cycles in:

```text
.codex/verify-cycles/<cycle-name>.md
```

For migrated projects whose tooling still reads Claude paths, also support:

```text
.claude/verify-cycles/<cycle-name>.md
```

Use the path that the repo's review tooling currently discovers.

## Cycle Format

```markdown
# <Name> Check

Run: <command to run>
When: <plain-English relevance condition>

<notes, thresholds, manual checklist, or failure handling>
```

Rules:

- `When:` is required.
- `Run:` makes the cycle automated.
- Omitting `Run:` makes the cycle manual.
- Everything else is context for review.

## Create A Cycle

1. Choose a short hyphen-case filename.
2. Create the verify-cycles directory if needed.
3. Write a specific `When:` condition.
4. Use a deterministic `Run:` command when possible.
5. Add clear block/pass criteria.

Example automated cycle:

```markdown
# TypeScript Compilation Check

Run: npx tsc --noEmit
When: TypeScript or JavaScript files change

Block review if compilation fails.
```

Example manual cycle:

```markdown
# Visual Regression Check

When: CSS or UI component changes

Check responsive layout, focus states, contrast, and obvious visual regressions.
```

## Review Behavior

During `$review`:

1. Discover cycle files.
2. Determine relevance from `When:` and changed files.
3. Run automated relevant cycles.
4. Display manual relevant cycles as required checks.
5. When unsure, run or display the cycle.
