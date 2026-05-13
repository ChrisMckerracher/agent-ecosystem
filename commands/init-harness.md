---
description: Scaffold the universal harness (AGENTS.md, CLAUDE.md, CODEX.md, docs/) into a repo using a strict atomic-refuse installer
allowed-tools: ["Bash", "Read", "AskUserQuestion"]
argument-hint: "[--root <PATH>] [--project-name <NAME>] [--language <python|typescript|polyglot>] [--dry-run] [--force]"
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

## Resolving the install script (defensive)

The placeholder above is the primary path, but it can fail in four ways:
hook didn't fire, `CLAUDE_PLUGIN_ROOT` was empty in the hook env,
`CLAUDE_PLUGIN_ROOT` was stale (resolved to `.../unknown/`), or the line was
dropped from context. When you (Claude) cannot locate the install script via
the placeholder, recover with this chain:

1. **Primary** — try the substituted placeholder:
   `bash "{AGENT_ECOSYSTEM_ROOT}/scripts/init-harness/install.sh" ...`

2. **Recovery 1** — if the path is empty, unset, or the file doesn't exist,
   try `${CLAUDE_PLUGIN_ROOT}` directly (it may work in some local-dev
   scenarios):
   ```
   bash "${CLAUDE_PLUGIN_ROOT}/scripts/init-harness/install.sh" ...
   ```

3. **Recovery 2** — if that also fails, discover the script by globbing the
   marketplace cache:
   ```bash
   INSTALL_SH="$(find ~/.claude/plugins -path '*/init-harness/install.sh' \
                                         -type f 2>/dev/null | head -1)"
   ```
   Validate it: `[ -x "$INSTALL_SH" ]`. If multiple matches exist (dev +
   marketplace), the first is taken — warn the user briefly.

4. **Final fallback** — if all three return nothing, do NOT guess a path or
   inline the install logic. Tell the user:
   > Cannot locate the init-harness install script. The plugin may not be
   > installed correctly. The script should live under
   > `~/.claude/plugins/.../agent-ecosystem*/scripts/init-harness/install.sh`.
   > Run `ls ~/.claude/plugins/` to see what's installed and re-invoke
   > with `--plugin-root <path>` once you've located it, or reinstall the
   > plugin.

   Then stop. Do not proceed.

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
2. Resolve the install script via the chain in **Resolving the install script
   (defensive)** above. The happy path is the placeholder; the recovery chain
   handles broken hooks / stale `CLAUDE_PLUGIN_ROOT` / dropped context. Then
   invoke:
   ```
   bash "$INSTALL_SH" --root <root> --project-name <name> --language <lang> [--dry-run] [--force]
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
