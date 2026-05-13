# Strip and Rename Repo to Agent Ecosystem — Design

**Feature spec:** No feature spec (technical/repo-restructure task)
**Product brief:** `docs/plans/product/briefs/strip-to-agent-ecosystem.md`
**External research:** Three research passes summarized inline:
1. Rename mechanics (Class 7, § Phase C)
2. **Path resolution** (Class 2 — confirmed `${CLAUDE_PLUGIN_ROOT}/plugin/scripts/...` references are LATENT BUGS, not just future regressions)
3. **Beads CLI currency** (Class 11 — `bd sync` removed, storage moved to Dolt SQL, several upstream features now duplicate our custom scripts)

## Critical Findings From Research (read first)

### Path resolution: dead code in agent prompts

Empirical inspection of `~/.claude/plugins/cache/agent-ecosystem-marketplace/agent-ecosystem/0.14.1/` shows **no `plugin/` subdirectory** in the cache layout. Plugin source `./plugin` causes the *contents* of `plugin/` to be copied to the cache root.

**Implication:** Every reference to `${CLAUDE_PLUGIN_ROOT}/plugin/scripts/...` in agent prompts and command markdown expands to a non-existent path at runtime. The hooks form `${CLAUDE_PLUGIN_ROOT}/hooks/...` is the only correct form.

**Conclusion:** Phase B's path rewrite is fixing a **latent bug**, not just a layout migration. Verification must include an empirical execution test (invoke `/decompose` on a fresh install), not a file-existence check.

### Beads: significantly outdated

Local install is `bd 0.58.0`, latest upstream is `1.0.4`. Several commands documented in `CLAUDE.md` and `AGENTS.md` no longer exist:

| Documented | Reality |
|-----------|---------|
| `bd sync` | **Removed.** Use `bd dolt push` (remote) and `bd vc commit` (local). |
| `.beads/issues.jsonl` storage | **Removed.** Storage is now Dolt SQL at `.beads/embeddeddolt/`. JSONL is export-only. |
| `bd merge` gitattributes driver | **Removed.** Dolt handles merging internally. |
| `bd update --status in_progress` | Still works, but `bd update --claim` is the blessed atomic claim. |
| `bd hooks install` | Still works, but `bd setup claude` is the preferred one-shot integration. |
| Custom worktree workflow via `decompose-init.sh`/`decompose-task.sh` | `bd worktree create/list/remove/info` is now upstream. Our scripts duplicate functionality. |

A larger question — should `decompose-init.sh`/`decompose-task.sh` be replaced by `bd worktree`? — is **explicitly out of scope** of this work. Filed as follow-up. This work only updates documented commands to current syntax.

### GitLab subsystem: explicit removal authorized

User authorized full removal of GitLab integration mid-session. Folded into Phase A (no separate phase). Footprint:
- 2 commands (`gitlab-pull-comments`, `gitlab-push-mr`)
- 3 skills (`gitlab-pull-comments/`, `gitlab-push-mr/`, `gitlab-stack/`)
- 1 script (`scripts/gitlab-stack.sh`)
- ~14 doc files (architect plans, product validations, research, spelunk refs, README sections)

## Goal

Convert `claude_stuff` from a personal monorepo into a dedicated **agent-ecosystem** plugin repo, then rename it on GitHub. The repo *is* the plugin. After this work:

- Repo root contains the plugin directly (no `plugin/` indirection)
- README is exclusively about the agent ecosystem (no claude-bus, no GitLab)
- `claude-bus`, GitLab, `rag/`, `configs/`, and stale Jan 2025 plans are gone
- All path references use the canonical `${CLAUDE_PLUGIN_ROOT}/...` form (no `plugin/` prefix)
- Beads commands in docs match current `bd` CLI surface
- GitHub repo renamed to `agent-ecosystem`
- Existing marketplace installs and consumers continue to work via redirects

## Non-Goals

- Git history rewrite (plain `git rm`)
- Extracting deleted content to other repos
- Migrating `.claude-plugin/marketplace.json` to a separate repo
- Refactoring agent/skill/command content beyond path-reference and beads-command updates
- **Replacing `decompose-init.sh`/`decompose-task.sh` with `bd worktree`** (separate refactor, follow-up issue)
- **Adopting new beads features** (`bd swarm`, `bd remember`, `bd mol`, etc.) — separate feature work

## What Breaks (and Fix Strategy)

This is the heart of the design. Below are *every* class of breakage identified, with a concrete fix.

### Breakage Class 1: Internal `plugin/...` path references inside the plugin

**Problem.** Promoting `plugin/` to root means every reference to `plugin/scripts/...`, `plugin/lib/...`, `plugin/hooks/...`, `plugin/skills/...` is wrong. Grep evidence (50 files):

| Reference type | Files affected | Example |
|---------------|----------------|---------|
| `${CLAUDE_PLUGIN_ROOT}/plugin/scripts/...` | `commands/architect.md`, `commands/decompose.md`, `agents/architecture.md`, `skills/architect/SKILL.md`, `skills/gitlab-stack/SKILL.md` | `${CLAUDE_PLUGIN_ROOT}/plugin/scripts/decompose-init.sh` → `${CLAUDE_PLUGIN_ROOT}/scripts/decompose-init.sh` |
| `plugin/lib/**` boundary docs | `agents/architecture.md`, `agents/product.md`, `commands/architect.md`, `commands/product.md`, `skills/spelunk/SKILL.md` | "NEVER read `plugin/lib/**`" → "NEVER read `lib/**`" |
| Markdown link refs | `agents/orchestrator.md` (3 places: `[plugin/skills/.../SKILL.md]`) | `[plugin/skills/architect/SKILL.md](../skills/architect/SKILL.md)` → `[skills/architect/SKILL.md](../skills/architect/SKILL.md)` (link target unchanged, label updated) |
| Doc references | 30+ design/spelunk/product docs | Mostly informational; mass-update with `sed -i 's|plugin/|/|g'` then manual review of the diff |
| Shell script literal | `skills/task-complete/SKILL.md`: `plugin/scripts/task-complete.sh` | `scripts/task-complete.sh` |
| TS import examples | `skills/spelunk/SKILL.md`: `import ... from 'plugin/lib/spelunk'` | `import ... from 'lib/spelunk'` (these are illustrative, not real imports) |

**Fix.** Mechanical `sed`-based rewrite + diff review:

```bash
# Inside the promoted layout (after physical move):
grep -rln "plugin/" --include="*.md" --include="*.json" --include="*.sh" \
  | xargs sed -i '' 's|\${CLAUDE_PLUGIN_ROOT}/plugin/|${CLAUDE_PLUGIN_ROOT}/|g'

grep -rln "plugin/lib/\*\*" --include="*.md" \
  | xargs sed -i '' 's|plugin/lib/\*\*|lib/\*\*|g'

grep -rln "plugin/scripts/" --include="*.md" \
  | xargs sed -i '' 's|plugin/scripts/|scripts/|g'

grep -rln "plugin/skills/" --include="*.md" \
  | xargs sed -i '' 's|plugin/skills/|skills/|g'
# ... etc per directory
```

Then `git diff` reviewed file-by-file. Some doc references are intentional (e.g. historical design docs describing old layout) — those should be left alone in `docs/plans/architect/*.md` for old plans, OR they go away with the Jan 2025 plans deletion.

**Verification gate.** Post-rewrite, `grep -rn "plugin/" --include="*.md" --include="*.json" --include="*.sh"` should return zero results outside of `docs/plans/` historical content (or one allow-list of intentional references documented in this design).

### Breakage Class 2: `${CLAUDE_PLUGIN_ROOT}` resolution — LATENT BUG

**Problem (confirmed by empirical research).** `${CLAUDE_PLUGIN_ROOT}` resolves to the cache install dir (`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`). With `source: "./plugin"`, the *contents* of `plugin/` are copied to the cache root — there is **no `plugin/` subdirectory in the cache**.

Empirical verification (cache inspection):
```
~/.claude/plugins/cache/agent-ecosystem-marketplace/agent-ecosystem/0.14.1/
├── .claude-plugin/
├── hooks/
├── agents/
├── commands/
├── scripts/
└── ... (no `plugin/` subdir)
```

This means:
- `${CLAUDE_PLUGIN_ROOT}/hooks/session-start.sh` ✅ resolves correctly
- `${CLAUDE_PLUGIN_ROOT}/plugin/scripts/decompose-init.sh` ❌ resolves to a non-existent path

The prefixed form has been **dead code all along**. It hasn't caused user-visible failures because the LLM reading the slash-command markdown likely figures out the right path from context, or the user's session has been hard-coding paths during invocation. Either way, after promoting `plugin/` to root, the correct canonical form is unambiguous.

**Fix.** Rewrite all `${CLAUDE_PLUGIN_ROOT}/plugin/<dir>/` → `${CLAUDE_PLUGIN_ROOT}/<dir>/`. After the sed pass in Class 1, this is automatic.

**Verification gate (UPGRADED).** Manual smoke test on a fresh local install must include **actual script execution**, not file-existence:

```bash
# Fresh install
/plugin marketplace remove agent-ecosystem-marketplace 2>/dev/null
/plugin marketplace add file:///path/to/agent-ecosystem
/plugin install agent-ecosystem

# Empirical execution test (not just `ls`):
/architect strip-test    # Triggers decompose-init.sh via ${CLAUDE_PLUGIN_ROOT}
# OR run directly:
~/.claude/plugins/cache/agent-ecosystem-marketplace/agent-ecosystem/<v>/scripts/decompose-init.sh --version
```

Pass criteria: script executes without "no such file or directory".

### Breakage Class 3: `marketplace.json` source path

**Problem.** Root `.claude-plugin/marketplace.json` has `"source": "./plugin"`. After promotion, `./plugin` no longer exists.

**Fix.** Update to `"source": "."`. Bump version (e.g. `0.15.0` — major restructure, breaking layout change).

### Breakage Class 4: Shared `lib/package.json` exposes claude-bus bin

**Problem.** `plugin/lib/package.json` declares `"bin": { "claude-bus": "./dist/claude-bus/cli.js" }`. After deleting `lib/claude-bus/`, this entry is dangling.

**Fix.** Remove the `"bin"` field entirely (no other binaries needed) when deleting the claude-bus subdirectory.

### Breakage Class 5: `.mcp.json` registers claude-bus MCP server

**Problem.** `.mcp.json` registers `claude-bus` as an MCP server. After removal, this is a dead pointer.

**Fix.** Delete `.mcp.json` (no other MCP servers configured) OR replace with an empty `{ "mcpServers": {} }` if a placeholder is needed.

### Breakage Class 6: README and quick-start commands

**Problem.** README markets agent-ecosystem and claude-bus as sibling products. The Quick Start command:
```
/plugin marketplace add https://github.com/ChrisMckerracher/claude_stuff
```
will continue to work via GitHub redirect after rename, but is stale.

**Fix.** Rewrite README:
- Title: "Agent Ecosystem" (drop "+ Claude-Bus")
- Drop the entire Claude-Bus section, the ASCII diagrams, the worker registration example
- Update Quick Start to `https://github.com/ChrisMckerracher/agent-ecosystem`
- Update homepage/repository fields in `.claude-plugin/plugin.json` to the new URL

### Breakage Class 7: GitHub-side breakage post-rename

Per product agent research:

| What breaks | Fix |
|------------|-----|
| Local `origin` remote URL | After rename: `git remote set-url origin https://github.com/ChrisMckerracher/agent-ecosystem` (do this on every clone you maintain) |
| GitHub Actions `uses:` refs in *other* repos | None known to reference this repo. If discovered later, update those repos. |
| GitHub Pages | None hosted. N/A. |
| Marketplace caches in user installs | Existing installs continue working from local cache. Future `/plugin update` calls hit the redirect and resolve to the new URL transparently. |
| Badges, docs links | Rewrite Quick Start in README; nothing else to update. |
| **Don't re-claim the old name** — would shadow the redirect | Add a note to a follow-up issue: never create a new `claude_stuff` repo under this account. |

### Breakage Class 8: `.gitignore` / `.gitattributes`

**Problem.** `.gitignore` references `plugin/dashboard/node_modules/` and `plugin/lib/dist/`.

**Fix.** Update to `dashboard/node_modules/` and `lib/dist/`. Also remove `__pycache__/`, `.mypy_cache/`, `*.egg-info/`, `.venv/` (Python ignores were for `rag/`, no longer needed).

`.gitattributes` is fine as-is (only references `.beads/issues.jsonl`).

### Breakage Class 9: Spelunk staleness cache

**Problem.** `docs/spelunk/_staleness.json` contains hash references to `plugin/lib/...` files.

**Fix.** Two options (decompose chooses):
1. **Delete** `docs/spelunk/_staleness.json` and let next spelunker run regenerate it. Simplest.
2. Mass-rewrite paths inside it with sed. More fragile; staleness check will likely re-trigger anyway.

Recommend option 1.

### Breakage Class 10: `test-ecosystem.sh`

**Partially safe.** The script tests installed-plugin paths under `~/.claude/plugins/local/agent-ecosystem/`, not repo paths. It does NOT invoke claude-bus tests. **However**, it DOES check for GitLab files (lines 63-64, 120-121). After GitLab strip (Class 12), those entries must be removed.

### Breakage Class 11: Stale beads commands across docs and skills

**Problem (confirmed by `bd --version` + upstream research).** Outdated beads usage in:

| File | Line(s) | Stale call | Replacement |
|------|---------|-----------|-------------|
| `CLAUDE.md` | 125 | `bd update <id> --status in_progress` | `bd update <id> --claim` |
| `CLAUDE.md` | 127, 155 | `bd sync` | `bd dolt push` (and `bd vc commit` where appropriate) |
| `AGENTS.md` | 3 | `bd onboard` (still works but) | `bd setup claude` (preferred for Claude Code integration) |
| `AGENTS.md` | 9 | `bd hooks install` | `bd setup claude` |
| `AGENTS.md` | 15, 26, 41 | `bd sync` | `bd dolt push` |
| `AGENTS.md` | 24 | `bd update <id> --status in_progress` | `bd update <id> --claim` |
| `plugin/agents/coding.md` | 93 | `bd update {task-id} --status in_progress` | `bd update {task-id} --claim` |
| `plugin/skills/code/SKILL.md` | 51 | `bd update {task-id} --status in_progress` | `bd update {task-id} --claim` |
| `.gitattributes` | 2-3 | `.beads/issues.jsonl merge=beads` | **Delete entire entry** — Dolt handles merging internally |
| `.gitignore` | (missing) | — | Add `.beads/embeddeddolt/` if not already ignored by `.beads/` |

**Fix.** Mechanical edits per table. No mass-sed since command syntax varies.

**Out of scope (filed as follow-ups, not changed here):**
- Replacing `decompose-init.sh`/`decompose-task.sh` with `bd worktree create` (would simplify ~200 lines of custom shell)
- Adopting `bd swarm` for the merge-tree fan-out pattern
- Adopting `bd remember` / `bd memories` / `bd recall` to replace any custom memory mechanisms
- Adopting `bd preflight` in the pre-push hook
- `bd q "Title"` as scripting alias

**Verification gate.** `grep -rn "bd sync\|bd merge\|issues\.jsonl\|--status in_progress\|bd hooks install\|bd onboard"` against tracked files (excluding `docs/plans/` historical content) should return zero results.

### Breakage Class 12: GitLab subsystem removal

**Problem.** User authorized full removal of the GitLab integration. Footprint:

| Path | Action |
|------|--------|
| `plugin/commands/gitlab-pull-comments.md` | Delete |
| `plugin/commands/gitlab-push-mr.md` | Delete |
| `plugin/skills/gitlab-pull-comments/` | Delete (entire dir) |
| `plugin/skills/gitlab-push-mr/` | Delete (entire dir) |
| `plugin/skills/gitlab-stack/` | Delete (entire dir) |
| `plugin/scripts/gitlab-stack.sh` | Delete |
| `scripts/test-ecosystem.sh` lines 63-64, 120-121 | Remove GitLab entries |
| `CLAUDE.md` lines 13, 200-203 | Remove "GitLab Integration" feature mention + "GitLab Operations" section |
| `README.md` line 20 | Remove "GitLab integration" bullet |
| `docs/agent-ecosystem/README.md` lines 20, 76-77, 337-352, 385-391, 406 | Remove GitLab Integration feature, command table rows, full GitLab section, troubleshooting row, glab dependency |
| `docs/plans/architect/gitlab-stack-design*.md` (3 files) | Delete (stale; subsystem gone) |
| `docs/plans/architect/decompose-scripts-design.md` (gitlab refs) | Sed-edit (script is referenced for context; subsystem removed) |
| `docs/plans/product/research/gitlab-stacked-mr-workflow.md` | Delete |
| `docs/plans/product/validations/gitlab-stack-design*.md` (3 files) | Delete |
| `docs/spelunk/_staleness.json` | Delete (regenerates without gitlab refs) |

**Verification gate.** `grep -rln "gitlab\|GitLab\|glab" --include="*.md" --include="*.sh" --include="*.json"` against tracked files (excluding `docs/plans/2025-01-09-*` and any other historical Jan-2025 plan being deleted in same phase) returns only the design doc itself (this file).

## Layout Diff

```
BEFORE                                  AFTER
─────────                               ─────────
claude_stuff/                           agent-ecosystem/   (renamed on GitHub)
├── .claude-plugin/                     ├── .claude-plugin/
│   └── marketplace.json                │   ├── marketplace.json   (source: ".")
├── .mcp.json              [DELETE]     │   └── plugin.json        (promoted)
├── configs/               [DELETE]     ├── agents/                (promoted)
├── rag/                   [DELETE]     ├── commands/              (promoted, gitlab-* deleted)
├── docs/                               ├── skills/                (promoted, gitlab-* deleted)
│   ├── claude-bus/        [DELETE]     ├── hooks/                 (promoted)
│   ├── plans/                          ├── lib/                   (promoted, claude-bus stripped)
│   │   ├── 2025-01-09-*    [DELETE]    │   ├── spelunk/
│   │   ├── architect/                  │   ├── verify-cycle/
│   │   │   ├── claude-bus-* [DELETE]   │   └── package.json       (no bin field)
│   │   │   └── gitlab-*    [DELETE]    ├── dashboard/             (promoted)
│   │   └── product/                    ├── scripts/               (merged: top-level + plugin/scripts/
│   │       ├── research/gitlab-* [DEL] │                            minus gitlab-stack.sh)
│   │       └── validations/gitlab-* [DEL] ├── templates/          (promoted)
│   └── (rest)                          ├── docs/                  (kept; refs rewritten;
├── plugin/                             │                            gitlab/claude-bus docs deleted)
│   ├── .claude-plugin/                 ├── tests/                 (kept)
│   ├── agents/  ─┐                     ├── README.md              (rewritten — agent-eco only,
│   ├── commands/ │  (gitlab-* DELETED) │                            no claude-bus, no GitLab)
│   ├── skills/   │  (gitlab-* DELETED) ├── CLAUDE.md              (paths + beads cmds updated)
│   ├── hooks/    │  PROMOTE            ├── AGENTS.md              (beads cmds updated)
│   ├── lib/      │  TO ROOT            ├── .gitignore             (updated)
│   │   └── claude-bus/    [DELETE]     └── .gitattributes         (bd merge driver removed)
│   ├── dashboard/│
│   ├── scripts/  │ (gitlab-stack.sh DELETED)
│   └── templates/┘
├── scripts/test-ecosystem.sh   (gitlab entries removed; rest unchanged)
├── tests/e2e/                  (kept at root)
└── README.md
```

`scripts/test-ecosystem.sh` collides with promoted `plugin/scripts/`. Resolution: merge into single root `scripts/` dir. After merge: `test-ecosystem.sh` + `decompose-init.sh` + `decompose-task.sh` + `task-complete.sh` (gitlab-stack.sh deleted in Phase A).

## Sequence (mandatory order)

Per product research: **strip first, rename second.** Reduces moving parts during the messy work. Beads modernization happens last so it doesn't complicate the structural changes.

```
Phase A — STRIP                       (one branch, one PR)
  Subset A.1 — claude-bus + extras
    A1.  Delete configs/
    A2.  Delete rag/
    A3.  Delete .mcp.json
    A4.  Delete docs/claude-bus/
    A5.  Delete plugin/lib/claude-bus/
    A6.  Edit plugin/lib/package.json: remove "bin" field
    A7.  Delete docs/plans/2025-01-09-*.md
    A8.  Delete docs/plans/architect/claude-bus-*.md and claude-code-bus.md

  Subset A.2 — GitLab subsystem (Class 12)
    A9.  Delete plugin/commands/gitlab-pull-comments.md
    A10. Delete plugin/commands/gitlab-push-mr.md
    A11. Delete plugin/skills/gitlab-pull-comments/, gitlab-push-mr/, gitlab-stack/
    A12. Delete plugin/scripts/gitlab-stack.sh
    A13. Delete docs/plans/architect/gitlab-stack-design*.md (3 files)
    A14. Delete docs/plans/product/research/gitlab-stacked-mr-workflow.md
    A15. Delete docs/plans/product/validations/gitlab-stack-design*.md (3 files)
    A16. Edit scripts/test-ecosystem.sh: remove gitlab entries (lines 63-64, 120-121)
    A17. Edit README.md, CLAUDE.md, docs/agent-ecosystem/README.md: drop gitlab sections

  Subset A.3 — README + ignores
    A18. Update README.md (drop claude-bus sections, drop gitlab bullet)
    A19. Update CLAUDE.md (drop GitLab Operations section, drop any stale claude-bus refs)
    A20. Update .gitignore (drop python ignores from rag/)
    A21. Delete docs/spelunk/_staleness.json (will regenerate next spelunk)

  A22. Verify: grep -rln "claude-bus\|GitLab\|gitlab\|glab" returns 0 outside this design doc
  A23. Verify: ./scripts/test-ecosystem.sh passes after local reinstall

Phase B — PROMOTE                     (new branch, new PR; depends on A)
  B1.  Move plugin/* → repo root (preserving git history via `git mv`)
  B2.  Merge plugin/scripts/ → scripts/ (collision resolution)
  B3.  Update .claude-plugin/marketplace.json: "source" → "."
  B4.  Bump plugin.json version → 0.15.0
  B5.  Mass sed rewrite: ${CLAUDE_PLUGIN_ROOT}/plugin/ → ${CLAUDE_PLUGIN_ROOT}/
       (per Class 2 — fixes a LATENT BUG, not just a layout migration)
  B6.  Mass sed rewrite: plugin/lib/** → lib/** (boundary refs)
  B7.  Mass sed rewrite: plugin/skills/, plugin/scripts/, plugin/agents/ → without prefix
  B8.  Update .gitignore: plugin/dashboard/node_modules/ → dashboard/node_modules/, etc.
  B9.  Verify: grep -rn "plugin/" returns only allow-listed historical refs in docs/plans/
  B10. Verify: ./scripts/test-ecosystem.sh passes after fresh local reinstall
  B11. Verify (UPGRADED per Class 2): execute scripts/decompose-init.sh from ${CLAUDE_PLUGIN_ROOT}
       on fresh install — must run, not just exist

Phase C — RENAME                      (no PR; GitHub op + small commit; depends on B)
  C1.  gh repo rename agent-ecosystem --repo ChrisMckerracher/claude_stuff
  C2.  git remote set-url origin https://github.com/ChrisMckerracher/agent-ecosystem.git
  C3.  Update plugin.json `repository` and `homepage` URLs
  C4.  Update README Quick Start install URL
  C5.  Commit + push the URL updates
  C6.  Verify: redirect works (curl -I https://github.com/ChrisMckerracher/claude_stuff returns 301)
  C7.  Note in a follow-up issue: never re-claim the old `claude_stuff` name

Phase D — MODERNIZE BEADS DOCS         (new branch, new PR; depends on B, parallel to C)
  D1.  Edit CLAUDE.md: bd sync → bd dolt push (lines 127, 155); --status in_progress → --claim (line 125)
  D2.  Edit AGENTS.md: bd sync → bd dolt push (lines 15, 26, 41); --status in_progress → --claim (line 24);
       bd hooks install → bd setup claude (line 9); update onboard mention (line 3)
  D3.  Edit agents/coding.md (post-promotion): line 93, --status in_progress → --claim
  D4.  Edit skills/code/SKILL.md (post-promotion): line 51, --status in_progress → --claim
  D5.  Edit .gitattributes: delete `.beads/issues.jsonl merge=beads` line (Dolt handles internally)
  D6.  Edit .gitignore: confirm `.beads/` covers `.beads/embeddeddolt/` (it does via prefix match)
  D7.  Verify: grep -rn "bd sync\|bd merge\|issues\.jsonl\|--status in_progress" tracked files returns 0
       (excluding docs/plans/ historical content)
  D8.  File follow-up issues for out-of-scope beads modernization:
       - "Replace decompose-init.sh/decompose-task.sh with bd worktree create"
       - "Adopt bd swarm for merge-tree fan-out"
       - "Adopt bd remember/memories for agent persistence"
       - "Adopt bd preflight in pre-push hook"
```

Phases A and B can be combined into one branch if desired, but the design treats them as separable to keep diffs reviewable. Phase C is a one-line GitHub op gated on B. Phase D can run in parallel with C (independent file scope).

## Verification Gates

| Gate | When | What passes |
|------|------|-------------|
| Strip-clean | End of Phase A | `grep -rln "claude-bus\|GitLab\|gitlab\|glab"` returns 0 outside this design; `test-ecosystem.sh` green; README has no claude-bus or GitLab mention |
| Promote-clean | End of Phase B | `grep plugin/` returns only allow-listed historical refs; `test-ecosystem.sh` green from fresh install; **scripts/decompose-init.sh actually executes** when called via `${CLAUDE_PLUGIN_ROOT}` (not just file-exists check, per Class 2) |
| Rename-clean | End of Phase C | Old URL redirects; new URL serves; local `git fetch` works against new origin; README install command points to new URL |
| Beads-current | End of Phase D | `grep -rn "bd sync\|bd merge\|issues\.jsonl\|--status in_progress"` against tracked non-historical files returns 0; `bd dolt push` works in session-completion workflow |

## Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| ~~`${CLAUDE_PLUGIN_ROOT}` resolution differs from assumption (Class 2)~~ **Resolved by research** | ~~High~~ Resolved | Empirical cache inspection confirmed canonical form. No-prefix is correct. Phase B gate B11 verifies execution end-to-end. |
| sed rewrites catch unintended matches (e.g. `plugin/something-not-a-path`) | Medium | Mandatory `git diff` review per file in Phase B; allow-list `docs/plans/` historical content for exemption (explicit, not implicit) |
| Old `docs/plans/architect/*.md` historical content is "rewritten" by sed and loses fidelity | Low | Allow-list `docs/plans/` for sed exemption; document the allow-list explicitly in Phase B task brief |
| Marketplace consumers break on next `/plugin update` because cached source path is stale | Medium | GitHub redirect handles git URL changes; cache will refresh on next install. Document in PR description. |
| Phase A removes claude-bus while users have it active in their MCP config | Low | None — `.mcp.json` is repo-local, not user-global. Users with personal `.mcp.json` are independent. |
| Beads CLI changes again before Phase D ships, making D-edits stale | Low | `bd 1.0.4` is a stable major; use replacements documented in Class 11 verbatim. Re-verify with `bd --version` and `bd --help` immediately before commit. |
| Phase D edits agent prompts that Phase B just rewrote | Low | Phase D depends on B explicitly. Files are edited at canonical post-promotion paths. |
| GitLab strip leaves dangling skill imports in the orchestrator agent prompt | Low | Audited: orchestrator references skills via `[plugin/skills/.../SKILL.md]` markdown links. After strip, verify orchestrator agent doesn't reference any deleted skill. |

## Open Questions Deferred to Decompose

1. **Single PR vs two PRs for Phase A + B?** Recommend two for diff reviewability, but may be combined if disagrees.
2. **Should `scripts/test-ecosystem.sh` be enhanced to also test `plugin/lib/spelunk` and `plugin/lib/verify-cycle` build/test?** Out of scope; file as follow-up.
3. **Marketplace.json being a separate repo eventually?** Out of scope; file as follow-up.

## Decompose Plan (preview for /decompose)

Four leaf tasks. C and D both depend on B; they are parallel-eligible (independent file scope). Approximate sizes:

| Task | Lines | Blockers |
|------|-------|----------|
| `strip-claude-bus-gitlab-and-extras` (Phase A) | ~350 (deletions + README/CLAUDE.md/test-script edits across claude-bus + GitLab) | none |
| `promote-plugin-to-root` (Phase B) | ~400 (path-ref rewrites across ~50 files via sed + diff review + execution smoke test) | strip-claude-bus-gitlab-and-extras |
| `rename-github-and-update-urls` (Phase C) | ~50 (5 file edits + GitHub op + curl verification) | promote-plugin-to-root |
| `modernize-beads-commands-in-docs` (Phase D) | ~80 (10 line-level edits across 5 files + .gitattributes + 4 follow-up issues) | promote-plugin-to-root |

Total: ~880 lines across 4 tasks. Phase A is approaching the 1000-line cap due to GitLab subset; if it grows, split into A.1 (claude-bus + extras) and A.2 (GitLab) as sibling tasks (no inter-dependency).
