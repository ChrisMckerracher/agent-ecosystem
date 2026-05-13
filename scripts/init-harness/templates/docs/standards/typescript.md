# TypeScript Standards

1. Use ES modules; prefer `.ts` over `.tsx` outside of JSX-bearing files.
2. Require explicit return types on exported functions.
3. Prefer interfaces over type aliases for object shapes.
4. Avoid `any`; reach for `unknown` plus a narrowing guard at the boundary.
5. Use Zod (or equivalent) at runtime boundaries; do not trust external input shapes.
6. Keep side effects at the edges; pure core, impure shell.
7. Tests live in `*.test.ts` colocated with the module under test.
8. Lint and typecheck pass before opening a PR.
