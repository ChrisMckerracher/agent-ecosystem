# Engineering Standards

## Core Principles
1. Prefer clarity over cleverness.
2. Keep modules small, composable, and single-purpose.
3. Avoid duplication, but do not over-abstract early.
4. Optimize for maintainability and debuggability.
5. Use mature, well-supported libraries before custom equivalents.

## Architecture Rules
1. Prefer the minimum number of runtime components that cleanly solve the current problem.
2. Keep one clear owner per concern.
3. Keep one source of truth for each policy decision.
4. Keep orchestration pipelines explicit and easy to trace end to end.
5. Use concrete types and functions in core domain paths unless multiple real implementations justify abstraction.
6. Remove pass-through components that add no behavior, except approved `contracts/` re-export surfaces.
7. Generalize only real shared semantic concepts.
8. When one backing system is chosen, design directly to its native semantics instead of adding backend-agnostic layers.
9. Keep state resolution in a dedicated module and cover it with focused unit tests.
10. Fail closed for derived state; do not default unknown combinations to success.
11. When helper concerns are shared across multiple real package owners, centralize them in a shared library instead of duplicating the same helpers per package.
12. Prefer decorators or shared helper functions for repeated boundaries when they keep ownership explicit and make cross-package behavior easier to audit.
13. When a concern has both shared primitives and package-owned semantics, keep the shared primitives in the shared library and the package-owned semantics in a dedicated package-local subpackage.

## Boundary Model Rules
1. Prefer canonical domain models as boundary models.
2. Avoid duplicate `*Request` / `*Response` wrappers unless the external API shape truly differs.
3. Name boundary models by domain semantics, not transport direction.
4. If a package exposes `contracts/`, it may only re-export approved canonical boundary models.
