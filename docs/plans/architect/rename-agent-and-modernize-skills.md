# Rename `architecture` Agent → `architect` and Modernize Beads Patterns in Skills

**Feature spec:** No feature spec (technical/refactor task)
**Product brief:** None — direct user request mid-session
**Related prior work:** Phase D (`docs/plans/architect/strip-and-rename-to-agent-ecosystem.md`) modernized beads commands in repo docs and 2 specific skills. This work extends that to ALL skills and adds a small naming-consistency rename.

## Goal

Two small, independent improvements:

1. **Naming consistency:** Rename the agent identity from `architecture` to `architect` so the agent name matches its slash command (`/architect`) and its skill (`skills/architect/SKILL.md`). Today the agent is the only thing using the long form.
2. **Beads pattern cleanup in skills:** Audit found *no v0.x stale commands* (Phase D's pass was thorough), but the architect skill has an internal contradiction about `bd create` usage. Fix the contradiction. Clarify the design-field linkage pattern.

## Non-Goals

- Adopting any new bd 1.0.4 features (`bd worktree`, `bd swarm`, `bd remember`, `bd preflight`) — those stay in their existing follow-up beads (`claude_stuff-bzy`, `-hkm`, `-qn8`, `-hhv`).
- Migrating bead-ID prefix from `claude_stuff-` to `agent-ecosystem-` (separate concern; existing beads keep their IDs).
- Renaming `docs/plans/architect/` directory (already short form — fine).
- Mass-rewriting "architecture" everywhere — domain-language uses must be preserved.

## Scope of "architecture" → "architect" Rename

Empirical grep found **13 occurrences** of `architecture` across `agents/`, `commands/`, `skills/`. They split into two distinct categories:

### MUST change (agent identity — 4 sites)

| Site | Current | After |
|------|---------|-------|
| `agents/architecture.md` filename | `architecture.md` | `architect.md` (use `git mv`) |
| `agents/architect.md` frontmatter | `name: architecture` | `name: architect` |
| `agents/architect.md` description line | `Drafts architecture designs, analyzes codebase structure, and decomposes features into task trees.` | `Designs systems, analyzes codebase structure, and decomposes features into task trees.` (drops the "architecture" tautology in self-description; preserves meaning) |
| `CLAUDE.md:54` authority hierarchy | `Architect Agent (drafts design first)` | `Architect Agent (drafts design first)` |

### MUST NOT change (domain language — ~10 sites)

These use "architecture" as a domain noun referring to *the concept of system design*, not the agent's identity. A naive sed would break the prose. Examples to leave alone:

| File:Line | Context | Why preserve |
|-----------|---------|--------------|
| `agents/code-review.md:13` | "Review architecture designs for engineering principle compliance..." | "architecture designs" = the artifact being reviewed |
| `agents/coding.md:111` | "If **architecture issues** → STOP" | "architecture issues" = the class of concern |
| `agents/orchestrator.md:55` | "Codebase architecture analysis" | Routing keyword for the concept |
| `agents/product.md:107` | "Feature specs define behavior before architecture" | Sequencing of activities |
| `agents/product.md:126` | "spec is ready for architecture" | Same as above |
| `agents/security.md:18` | "Read architecture docs for context" | "architecture docs" = the artifact type |
| `commands/product.md:72` | "Feature specs defining behavior before architecture" | Same |
| `skills/spelunk/SKILL.md:48` | "Shows system architecture" | Domain noun |
| `skills/product/SKILL.md:50` | "Feature specs define behavior before architecture" | Same |

**Rule of thumb during edit review:** If the word can be replaced by "design"/"system design" without changing meaning, it's domain language — leave it. If it's the agent's name or routing label, change it.

### MAY change (judgment call — flag during review)

- `agents/architect.md` line 13 (was "Architect Agent"): could become "Architect" or stay "Architect Agent" for clarity. Recommend: stay "Architect Agent" — agents historically have "Agent" suffix in prose.

## Scope of Beads Pattern Cleanup in Skills

### Audit results

`grep -nE "bd sync|bd merge|--status in_progress|bd hooks install|bd onboard|issues\.jsonl" skills/*/SKILL.md` returns **zero hits**. Phase D was complete.

### Remaining concrete fix

**`skills/architect/SKILL.md` contradiction**:
- Line 111: "use the `/decompose` scripts — **never raw `bd create`**"
- Lines 136-141: shows raw `bd create` calls for the design-field linkage pattern

Resolve by clarifying the rule: the prohibition applies to *epic/task creation* (which the scripts handle including worktree + branch setup). The `--design` field linkage is a separate, sanctioned use of `bd create`/`bd update`. Rewrite line 111 to:

> Use the `/decompose` scripts for epic and task creation — they wire up worktree + branch + dependencies. Direct `bd create`/`bd update` is sanctioned for the `--design` field linkage shown below.

### Other improvement (optional, low-priority)

- Mention `bd setup claude` once in `skills/code/SKILL.md` or `skills/architect/SKILL.md` as the canonical setup command, so a fresh user landing in a skill knows how to bootstrap. Currently bootstrap is implicit. Defer or include — minor.

**Recommend: include the `bd setup claude` mention in skills/code/SKILL.md** (the most-trafficked skill), as one short line in any pre-existing setup section.

## Layout Diff

```
BEFORE                              AFTER
─────                               ─────
agents/                             agents/
├── architect.md   (← already exists?)  ├── architect.md   (was architecture.md)
├── architecture.md                   │   - name: architect
└── ...                               └── ...

skills/architect/SKILL.md           skills/architect/SKILL.md
  - line 111 contradicts            │   - line 111 clarified
  - lines 136-141 raw bd create     │   - lines 136-141 unchanged (sanctioned)

skills/code/SKILL.md                skills/code/SKILL.md
                                    │   + brief bd setup claude mention (optional)
```

**Collision check (verified):** Only `agents/architecture.md` exists. The earlier ambiguity in audit output was that `architect` (no extension) appeared in `ls` — that's `skills/architect/` and `commands/architect.md`, neither of which collides with `agents/architect.md`. Clean `git mv agents/architecture.md agents/architect.md`.

**`subagent_type` audit (verified):** `grep -rn "agent-ecosystem:architecture"` against shippable files (`*.md`, `*.json`, `*.sh`, excluding `docs/plans/`) returns **zero hits**. No internal callers to update. The Task delegation patterns elsewhere already use `agent-ecosystem:coding`, `agent-ecosystem:product`, etc. — `architecture` was not used as a subagent_type anywhere in this repo.

## Verification Gates

| Gate | What passes |
|------|-------------|
| Naming clean | `ls agents/architect.md` exists; `ls agents/architecture.md` does not exist; `grep "name: architecture" agents/architect.md` returns 0 |
| Domain refs intact | `grep -rn "architecture" agents/ commands/ skills/` returns the ~10 domain-language hits enumerated above (no more, no less); none of them are agent-identity refs |
| Plugin still loads | `./scripts/test-ecosystem.sh` passes after local reinstall |
| Slash command works | `/architect` (or `/architect examine`) invocable post-change |
| Beads contradiction fixed | `grep -A2 "never raw" skills/architect/SKILL.md` shows the clarified rule, not the absolute prohibition |

## Risks

| Risk | Mitigation |
|------|------------|
| Sibling agent prompts have hidden architecture-as-identity refs we miss | Manual diff review of all `architecture` hits before commit; the enumeration above is the allow-list — anything outside it is a candidate for rename, anything inside stays |
| Existing `agents/architect.md` collides with the rename target | Decompose's first step is to inspect/resolve the collision empirically |
| `name: architecture` frontmatter is referenced by Claude Code agent-discovery — renaming may break discovery for any session resume that has cached the old name | Marketplace plugin reinstall clears the agent registry. Document this in PR description. Verified: zero `subagent_type: "agent-ecosystem:architecture"` refs in shippable code, so no internal callers break. Any external user with cached references gets a one-time "agent not found" until they restart the session. |

## Decompose Plan

Two leaf tasks, parallel-eligible (different file scopes):

| Task | Lines | Blockers |
|------|-------|----------|
| `cleanup-beads-patterns-in-skills` | ~30 (one paragraph rewrite + one optional setup line) | none |
| `rename-architecture-agent-to-architect` | ~80 (file rename + frontmatter + 1 self-description line + audit grep for `subagent_type:` refs + cross-check sibling agents) | none (resolve `architect.md` collision in step 1) |

Both can land in one PR if desired. Total ~110 lines.

## Open Question for Decompose

The two tasks could be merged into a single `tighten-architect-naming-and-skills-cleanup` task if you prefer a single review unit. The split exists for clean separation of concerns; the fold exists for review velocity. Recommend split — they're not actually related work, just bundled in the user's request.
