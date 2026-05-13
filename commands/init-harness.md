---
description: Scaffold the universal harness (AGENTS.md, CLAUDE.md, CODEX.md, docs/) into a repo using a strict atomic-refuse installer
allowed-tools: ["Bash", "Read", "AskUserQuestion"]
argument-hint: "[--root PATH] [--project-name NAME] [--language python|typescript|polyglot] [--dry-run] [--force]"
---

# /init-harness

Install the universal harness templates into a target repo via the strict
installer at `{AGENT_ECOSYSTEM_ROOT}/scripts/init-harness/install.sh`.

> **Plugin-root placeholder.** `${CLAUDE_PLUGIN_ROOT}` does not expand in slash
> command markdown (anthropics/claude-code#9354, still open). The plugin's
> SessionStart hook (`hooks/session-start.sh`) prints `AGENT_ECOSYSTEM_ROOT="..."`
> to context at the start of every session. When composing Bash calls below,
> substitute `{AGENT_ECOSYSTEM_ROOT}` with the value you saw in that hook line.
> When #9354 lands, swap `{AGENT_ECOSYSTEM_ROOT}` → `${CLAUDE_PLUGIN_ROOT}` and
> drop the hook injection.

## What this lays down

- `AGENTS.md` — single source of truth, numbered atomic operating rules, required read order
- `CLAUDE.md` — Claude-specific execution notes, defers to `AGENTS.md`
- `CODEX.md` — Codex-specific execution notes, defers to `AGENTS.md`
- `docs/README.md`, `docs/repo-map.md` — docs home and layout map
- `docs/standards/{engineering,workflow,testing,documentation}.md` — universal standards
- `docs/standards/{python,typescript}.md` — language standards per `--language`
- `docs/plans/architect/.gitkeep`, `docs/plans/product/briefs/.gitkeep`,
  `docs/spelunk/.gitkeep`, `docs/runbooks/.gitkeep`,
  `docs/questions/.gitkeep`, `docs/archive/.gitkeep` — directory homes

## Strictness contract

The installer **refuses to overwrite anything**. If any target path already
exists, it aborts with exit 2 and writes zero files. The user must either:

1. Remove the conflicting files manually, or
2. Pass `--force` to overwrite.

`--dry-run` previews the planned copies and exits 0 without writing.

## Behavior

1. If the user did not supply flags, ask:
   - target root (default: current working dir)
   - project name (default: directory basename)
   - language preset: `python`, `typescript`, or `polyglot` (default: `polyglot`)
   - whether to do a `--dry-run` first
2. Run the installer (substitute `{AGENT_ECOSYSTEM_ROOT}` with the value from
   the SessionStart hook):
   ```
   bash "{AGENT_ECOSYSTEM_ROOT}/scripts/init-harness/install.sh" \
       --root <root> --project-name <name> --language <lang> [--dry-run] [--force]
   ```
   Always double-quote the path — `~/.claude/plugins/...` paths may contain
   spaces.
3. Surface the installer's stdout verbatim, including the "Next steps" block.
4. If exit code 2 (conflicts), do NOT silently rerun with `--force`. Show the
   conflict list to the user and ask whether to force-overwrite or to bail.
5. If exit 0, remind the user of the spec-first epic bootstrap path:
   - Edit `AGENTS.md` to tighten any rules that don't fit.
   - Fill in `docs/repo-map.md`.
   - Write the first design doc into `docs/plans/architect/`.
   - Create the first epic bead: `bd create --design=docs/plans/architect/<doc>.md --type=epic ...`

## Examples

```
/init-harness                                           # interactive
/init-harness --root ./my-repo --language python        # non-interactive
/init-harness --root . --dry-run                        # preview only
/init-harness --root . --force                          # bypass conflicts
```
