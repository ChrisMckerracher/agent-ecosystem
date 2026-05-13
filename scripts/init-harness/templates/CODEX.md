# CODEX.md

## Scope
Codex-specific execution notes. Shared coding standards live in `AGENTS.md`.
@AGENTS.md

## Execution Priorities
1. Keep implementation aligned with `AGENTS.md`.
2. Favor clear, testable, maintainable code.
3. Avoid introducing hidden coupling or unclear ownership.

## Codex Implementation Checklist
Before coding:
1. confirm requirements and acceptance criteria.
2. confirm contract and schema impact.
3. confirm test strategy.

During coding:
1. follow typing, validation, and idempotency standards from `AGENTS.md`.
2. enforce idempotency on async consumers and handlers.
3. keep auth, tracing, metrics, and logging hooks integrated.
4. keep side effects explicit and observable.

After coding:
1. update tests (unit + scenario parity where relevant).
2. regenerate/update API and event contracts when changed.
3. update docs for behavior, contract, or convention changes.

## Documentation Hygiene
1. Keep unresolved questions in `docs/questions/`.
2. Keep standards and examples current.
3. Capture conventions that reduce future human-AI correction loops.
