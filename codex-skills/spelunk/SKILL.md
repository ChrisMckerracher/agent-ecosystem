---
name: spelunk
description: Use for targeted codebase exploration that generates reusable docs about interfaces, flows, boundaries, contracts, or trust zones for other agents and future sessions.
---

# Spelunk

Use this skill to explore code once and preserve the result as durable documentation.

## Syntax

```bash
spelunk --for=<agent> --focus="<area>"
spelunk --lens=<lens1>,<lens2> --focus="<area>"
spelunk --check --lens=<lens> --focus="<area>"
spelunk --refresh --for=<agent> --focus="<area>"
```

Either `--for` or `--lens` is required, but not both.

## Default Lenses

| Agent | Lenses | Purpose |
|---|---|---|
| architect | interfaces, boundaries | structure and module ownership |
| product | flows | user-facing behavior and data flow |
| qa | contracts | inputs, outputs, validation, errors |
| security | trust-zones, contracts | auth, privilege, and validation boundaries |

## Lens Definitions

- `interfaces`: types, public APIs, class signatures, exported shapes.
- `flows`: entry points, handlers, call chains, data movement.
- `boundaries`: module exports, dependencies, ownership seams.
- `contracts`: validation schemas, errors, API request/response shapes.
- `trust-zones`: auth checks, privilege transitions, sanitization points.

## Output

Write reports to:

```text
docs/spelunk/
  _index.md
  _staleness.json
  interfaces/
  flows/
  boundaries/
  contracts/
  trust-zones/
```

Each report should include focus, lens, source files examined, tool strategy, findings, and staleness data.

## Tool Strategy

1. Prefer language-aware tooling available in the environment, such as LSP commands, TypeScript compiler APIs, or repo-provided spelunk utilities.
2. Fall back to structural search with `ast-grep` or `semgrep` when available.
3. Use `rg` as the lexical fallback.
4. Keep scope narrow with max files, max depth, and explicit paths.

## Staleness

Use file hashes or equivalent metadata to classify reports:

- `FRESH`: source files unchanged.
- `STALE`: tracked source changed.
- `MISSING`: report does not exist.
- `ORPHANED`: report exists but is not tracked.

Check before regenerating unless the user requested refresh.

## Best Practices

- Start with a specific focus area, not the whole repo.
- Produce reusable summaries instead of dumping raw search results.
- Include enough source references for a future agent to verify conclusions quickly.
- Keep report content factual and avoid implementation recommendations unless the lens calls for them.
