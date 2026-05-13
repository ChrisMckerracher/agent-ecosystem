# Python Standards

## Conventions
1. Use modern stable Python and `uv`.
2. Use `uv run` for Python entrypoints in this repo.
3. Require type hints for public functions and module boundaries.
4. Use dataclasses or Pydantic models for structured data instead of loose dicts.
5. Favor explicit dependency injection over hidden globals.
6. Keep side effects at the edges, not in core domain logic.
7. Validate external input strictly and fail with clear errors.
8. Prefer async I/O for network and queue paths; avoid blocking inside async code.
9. Do not use `typing.Any`.
10. Do not use raw JSON blob patterns like `dict[str, Any]`; model concrete shapes instead.
11. Prefer module-level helpers or private methods over nested helper functions that mutate closed-over state.
12. Use domain-specific helper names rather than generic `_do` / `_handle` patterns.

## Package Layout
1. Prefer canonical Python package layout under `packages/<pkg>/src/<pkg>/...`.
2. Prefer shallow cohesive subpackages over large flat directories.
3. When one deployable owns both API/server and worker code for one cohesive domain, keep them under one package root with sibling subpackages such as `api/`, `worker/`, and `infrastructure/`.
4. Mirror an established package shape in the repo unless a concrete mismatch requires divergence.
