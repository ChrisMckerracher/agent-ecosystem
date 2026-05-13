# Docs

`docs/` is the current docs system of record for repo standards and reference material.

Use it to understand how to work in this repo now.

## Read Order
1. `AGENTS.md`
2. `docs/README.md`
3. `docs/repo-map.md`
4. the active design doc in `docs/plans/architect/`
5. task-relevant standards in `docs/standards/`
6. task-relevant spelunks in `docs/spelunk/`

## What Lives Where
- `docs/repo-map.md`: current repo layout and navigation help
- `docs/standards/engineering.md`: architecture and engineering rules
- `docs/standards/testing.md`: testing expectations
- `docs/standards/documentation.md`: docs, design-doc, and conventions rules
- `docs/standards/workflow.md`: beads, worktrees, agent workflow, and execution policy
- `docs/plans/architect/`: active design docs
- `docs/plans/product/briefs/`: product briefs feeding into design
- `docs/runbooks/`: operator runbooks for live behavior and local verification
- `docs/spelunk/`: audits, spelunks, and implementation follow-ups
- `docs/questions/`: unresolved questions parking lot
- `docs/archive/`: archived reference material, treated as read-only history

## Cleanup Policy
1. Remove tracked placeholder packages and stale tracked files rather than keeping them just in case.
2. Keep editor junk, caches, and local temp artifacts ignored rather than tracked.
3. Put archived reference material under `docs/archive/`, not in current reference docs.
4. Keep current live standards directly under `docs/standards/`.
