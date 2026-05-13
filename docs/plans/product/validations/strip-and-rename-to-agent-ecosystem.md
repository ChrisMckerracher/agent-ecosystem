# Strip and Rename to Agent Ecosystem — Validation Report

**Design reviewed:** `docs/plans/architect/strip-and-rename-to-agent-ecosystem.md`
**Brief reviewed:** `docs/plans/product/briefs/strip-to-agent-ecosystem.md`
**Date:** 2026-05-12
**Status:** APPROVED

## Checklist

- [x] Clear problem statement
- [x] Solution addresses problem directly
- [x] No unnecessary features (YAGNI)
- [x] User value is clear
- [x] Success criteria defined

## Findings

### 1. Coverage — Phase A + B + C vs In-Scope Items

All deletions from the brief are accounted for: `configs/`, `rag/`, `docs/claude-bus/`,
`plugin/lib/claude-bus/`, `.mcp.json`, the Jan 2025 plans, and the claude-bus architect docs
(Phase A steps A1–A6).

All restructure items are covered: every `plugin/` subdirectory is promoted to root (Phase B,
Layout Diff table), `marketplace.json` `source` field is updated (B3), and the scripts collision
is resolved by merging into a single root `scripts/` (B2).

All rewrite items are covered: README (A7/C4), CLAUDE.md (A9), path refs across 50 files via
sed (B5–B7), `.gitignore` (A8/B8).

Brief open question on `scripts/test-ecosystem.sh` and `tests/e2e/` placement: design confirms
both stay at root (Layout Diff, Class 10). Correct call; brief already recommended this.

Nothing from the brief's in-scope list is missing.

### 2. Risk Completeness — All 6 Brief Risks Addressed

| Brief Risk | Design Response |
|-----------|----------------|
| 1. Path references inside the plugin | Class 1 + Class 2, with grep evidence and sed strategy + verification gate B10/B12 |
| 2. claude-bus shared deps with spelunk/verify-cycle | Class 4 — bin field removal; implicit in Class 1 grep showing zero cross-refs |
| 3. test-ecosystem.sh invokes claude-bus tests | Class 10 — confirmed safe, no edits needed |
| 4. Marketplace consumers on old path | Class 3 (source update) + Class 7 (redirect note) |
| 5. .gitattributes / .gitignore entries | Class 8 — explicit fix for both files |
| 6. GitHub repo description still says "claude_stuff" | Class 7 (Phase C) + C7 follow-up note |

All six covered. Risk 6 was listed as out-of-scope in the brief; the architect correctly folded
it into the authorized rename phase rather than deferring it.

### 3. Scope Discipline

Class 7 (rename mechanics) was authorized by the user mid-session. Its inclusion as Phase C is
correct. The design explicitly labels it as product-research-derived, not architect-introduced
scope.

No other additions detected. The breakage class taxonomy (Classes 1–10) is a decomposition of
risks already implied by the brief's in-scope list, not new scope.

### 4. User Experience — Marketplace Continuity

The design relies on GitHub's automatic redirect after `gh repo rename`. The verify gate at C6
(curl for 301) confirms the redirect is live before the task closes. Existing installs are
served from local cache and are unaffected. Future `/plugin update` calls will follow the
redirect transparently. The README Quick Start URL is updated to the new canonical URL (C4).
No marketplace user experience gap identified.

The one residual risk (Class 2: `${CLAUDE_PLUGIN_ROOT}` resolution assumption) has a mandatory
manual smoke test gate (B12) before Phase B merges. This is the correct mitigation for the
highest-severity risk.

### 5. Sequencing

Strip (Phase A) → Promote (Phase B) → Rename (Phase C). This matches the brief's recommended
order and the product-research rationale (strip first to reduce moving parts during the messy
structural work; rename last when the repo is clean). Phases A and B are separable PRs with
Phase B blocking on Phase A; Phase C is a GitHub operation gating on Phase B merge. Sequencing
is correct.

## Concerns

None blocking. One minor observation: the sed exemption for `docs/plans/` historical content
(Class 1 fix notes) relies on a manual allow-list decision at diff-review time. The design
acknowledges this but leaves the allow-list implicit. Decompose may want to make it explicit
(e.g., a comment in the task brief). This is implementation-level detail, not a design gap.

## Scope Creep Flags

None.

## Recommendation

APPROVED. Hand off to `/decompose`.
