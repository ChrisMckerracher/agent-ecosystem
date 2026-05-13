# Rename Agent and Modernize Skills — Validation Report

**Design reviewed:** `docs/plans/architect/rename-agent-and-modernize-skills.md`
**Date:** 2026-05-12
**Status:** APPROVED

## Checklist
- [x] Clear problem statement
- [x] Solution addresses problem directly
- [x] No unnecessary features (YAGNI)
- [x] User value is clear
- [x] Success criteria defined

## Findings

### 1. "Update bead setup in skills" — scope interpretation

The architect's call is sound. Phase D was empirically verified as thorough (zero stale v0.x commands in remaining skills). The only concrete beads work remaining was the internal contradiction in `skills/architect/SKILL.md`, which is correctly targeted. Deferring `bd worktree`, `bd swarm`, `bd remember`, and `bd preflight` adoption to the four existing follow-up beads (`bzy`, `hkm`, `qn8`, `hhv`) is the right call — those are behavioral adoptions, not cleanup, and pulling them in here would inflate scope with no user-facing benefit from this specific request. The optional `bd setup claude` mention in `skills/code/SKILL.md` is low-cost and worth including; the recommendation to include it is correct.

### 2. Domain-language preservation strategy

The 13-occurrence audit and the allow-list are sound. Every "architecture" instance flagged as domain language genuinely refers to the artifact or the concept ("architecture designs", "architecture issues", "before architecture") not the agent's identity. The three hard-rename sites (filename, `name:` frontmatter, self-description) are the only identity uses. The rule of thumb supplied ("if it can be replaced with 'design' without changing meaning, leave it") is a reliable editorial test. No reclassification needed.

### 3. Risk completeness

One gap worth noting: the design addresses cached-session discovery risk at reinstall time but does not mention the CLAUDE.md reference at `/Users/chrismck/claude_stuff/CLAUDE.md` line referencing "Architect Agent" in the authority hierarchy comment. That is prose documentation inside a project file — it should be checked and updated along with the rename. It is low severity (no routing impact) but is an incomplete rename if left. Recommend the coding agent include it in the grep pass.

Otherwise the risk table is complete. The `subagent_type` audit covering zero hits in shippable code is the key safety check and it was done correctly.

### 4. Decompose plan

Two parallel leaf tasks at ~110 lines total is lean and correct. Splitting them is the right recommendation — `cleanup-beads-patterns-in-skills` and `rename-architecture-agent-to-architect` are logically independent and reviewing them as separate diffs reduces noise for Code Review. Folding into one PR is acceptable for merge velocity but keeping separate tasks is cleaner.

## Concerns
- Minor: CLAUDE.md authority hierarchy prose may use "Architect Agent" — include in the grep pass for the rename task.

## Scope Creep Flags
- None. Follow-up beads for `bd worktree` etc. correctly kept separate.

## Recommendation
Approve. Proceed to decompose. Coding agent should add CLAUDE.md to the rename grep pass as one additional check site.
