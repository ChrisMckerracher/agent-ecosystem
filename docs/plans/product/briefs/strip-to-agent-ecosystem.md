# Brief: Strip Repo to Agent Ecosystem Only

**Author:** Product Agent
**Date:** 2026-05-12
**Status:** Draft — ready for `/architect`

## Problem

`claude_stuff` is a personal monorepo bundling four unrelated things:

1. **Agent Ecosystem** — the Claude Code plugin (the actual product)
2. **Claude-Bus** — a separate orchestration daemon (code at `plugin/lib/claude-bus/`, docs at `docs/claude-bus/`, MCP server in `.mcp.json`)
3. **RAG project** — self-contained Python RAG/PHI-scrubbing experiment at `rag/`
4. **Personal dotfiles** — vim/tmux/nnn configs at `configs/`

The README markets these as if they were related products of one repo. They aren't. This dilutes project identity, confuses installers (the marketplace name is `agent-ecosystem` but the repo is `claude_stuff`), and makes the codebase harder to reason about.

## Goal

Convert this repo into a **dedicated agent-ecosystem plugin repo** — nothing else. The repo *is* the plugin. One product, one purpose, one README.

## Success Criteria

- Repo root contains the plugin directly (no `plugin/` indirection)
- README is exclusively about the agent ecosystem
- `bd ready`, `./scripts/test-ecosystem.sh`, and `/plugin install agent-ecosystem` still work
- No references to claude-bus, rag, or configs anywhere in tracked files
- Marketplace install path updated to reflect new layout

## In Scope (delete)

| Path | What it is | Why removed |
|------|-----------|-------------|
| `configs/` | Personal vim/tmux/nnn dotfiles | Unrelated to plugin |
| `rag/` | Python RAG project (~500KB lockfile + source) | Standalone project, doesn't belong here |
| `docs/claude-bus/` | Claude-Bus architecture docs | Separate product |
| `plugin/lib/claude-bus/` | Claude-Bus daemon/server/client/CLI/tests | Separate product, zero refs from agents/commands/skills/hooks/dashboard (verified via grep) |
| `.mcp.json` claude-bus entry | MCP server registration | Orphaned after lib removal |
| `docs/plans/2025-01-09-agent-ecosystem-*.md` | Old design/implementation plans | Historical; superseded by current `docs/plans/architect/` |
| `docs/plans/architect/claude-bus-*.md` | Architect plans for claude-bus | Companion to claude-bus removal |
| `docs/plans/architect/claude-code-bus.md` | Architect plan for claude-bus | Companion to claude-bus removal |

## In Scope (restructure)

**Promote `plugin/` to repo root.** After deletion, move contents of `plugin/` up one level so:

- `plugin/.claude-plugin/plugin.json` → `.claude-plugin/plugin.json`
- `plugin/agents/` → `agents/`
- `plugin/commands/` → `commands/`
- `plugin/skills/` → `skills/`
- `plugin/hooks/` → `hooks/`
- `plugin/lib/` → `lib/` (minus claude-bus subdir)
- `plugin/dashboard/` → `dashboard/`
- `plugin/scripts/` → `plugin-scripts/` (or merge with top-level `scripts/`)
- `plugin/templates/` → `templates/`

**Existing root `.claude-plugin/marketplace.json`** must be updated: `"source": "./plugin"` → `"source": "."`.

## In Scope (rewrite)

- `README.md` — rewrite as agent-ecosystem-only. Drop the dual-product framing, drop Claude-Bus section, drop the ASCII diagrams for claude-bus.
- `CLAUDE.md` — already agent-ecosystem-focused; only path references change (e.g. `plugin/lib/spelunk/` → `lib/spelunk/`).
- `AGENTS.md` — review for path refs, update if needed.
- Any `plugin/...` path references inside `docs/plans/architect/`, `docs/plans/product/`, hook scripts, command markdown, agent system prompts. These will break silently if not updated.

## Out of Scope

- Git history rewrite — plain `git rm` only. History stays recoverable.
- Extracting `rag/` or `configs/` to their own repos — user explicitly chose plain delete.
- Renaming the GitHub repo from `claude_stuff` to `agent-ecosystem` — that's a follow-up.
- Migrating the marketplace itself to a separate repo.

## Risks

1. **Path references inside the plugin.** Agents and skills reference `plugin/lib/spelunk/` and `plugin/.claude-plugin/plugin.json` in docs and prompts. Promoting to root will break every one of these. Architect must enumerate them before changes start. Grep target: `plugin/[a-z]` in all `.md`, `.sh`, `.json`, `.ts`, `.js`.
2. **`plugin/lib/claude-bus/` has its own `package.json` and tests.** Need to confirm no shared dependencies with `plugin/lib/spelunk/` or `plugin/lib/verify-cycle/` before deletion. (Likely safe — they're sibling subdirs — but verify.)
3. **`scripts/test-ecosystem.sh` may invoke claude-bus tests.** Must be checked and possibly trimmed.
4. **Marketplace consumers** who already installed via the old path are unaffected (install copies files); future installs need the updated `source` field.
5. **`.gitattributes` / `.gitignore`** may have entries for `rag/` or `configs/` worth pruning.
6. **Repo description on GitHub** still says "claude_stuff" — out of scope here, flag as follow-up.

## Recommendation

**APPROVED scope.** Hand off to `/architect` next. The architect should produce a design that:

1. Enumerates every file/dir to delete
2. Enumerates every path reference that needs rewriting (with grep evidence)
3. Sequences the work safely: delete → audit refs → promote → fix refs → update README → verify
4. Defines the verify gate: `./scripts/test-ecosystem.sh` passes, `/plugin install` from local path succeeds

Then `/decompose` should split it into ≤3 leaf tasks (deletes, restructure, README/refs cleanup) given the bounded blast radius.

## Open Question for Architect

Should top-level `scripts/test-ecosystem.sh` move into the plugin (since the repo *is* the plugin), or stay at root as a developer convenience? Same question for `tests/e2e/`. Recommend: keep both at root since they test *the plugin from outside* — that's a developer concern, not a plugin distribution concern.
