# Strip and Rename to Agent Ecosystem — Validation Report (v2)

**Design reviewed:** `docs/plans/architect/strip-and-rename-to-agent-ecosystem.md`
**Brief reference:** `docs/plans/product/briefs/strip-to-agent-ecosystem.md`
**Date:** 2026-05-12
**Status:** APPROVED

## Checklist

- [x] Clear problem statement
- [x] Solution addresses problem directly
- [x] No unnecessary features (YAGNI)
- [x] User value is clear
- [x] Success criteria defined

## Coverage of All Three Additions

**Path resolution findings (Class 2 / B11).**
Fully reflected. The latent-bug framing is explicit in the Critical Findings section and carried through to the risk table (risk downgraded to "Resolved by research") and gate B11 (upgraded from file-exists to actual script execution). No gaps.

**Beads modernization (Class 11 / Phase D).**
Complete. Every stale call is enumerated by file and line: `bd sync`, `--status in_progress`, `bd hooks install`, `bd onboard`, and the `.gitattributes` merge-driver entry. Out-of-scope adoptions (`bd worktree`, `bd swarm`, `bd remember`, `bd preflight`, `bd q`) are explicitly listed as follow-up issues, not touched in Phase D. The `.beads/embeddeddolt/` ignore question is addressed (D6 confirms prefix coverage). No gaps.

**GitLab subsystem removal (Class 12 / Subset A.2).**
All 2 commands, 3 skill directories, 1 script, and ~14 doc files are individually enumerated in the Class 12 table and in the Phase A step list (A9–A17). The test-script entries (lines 63-64, 120-121), README bullets, and `docs/agent-ecosystem/README.md` sections are called out. Orchestrator dangling-ref risk is flagged and mitigated. One minor observation: `docs/plans/architect/decompose-scripts-design.md` is listed as a sed-edit target for GitLab refs, but has no corresponding A-step number — it is covered by the prose in the Class 12 table, which is sufficient for an architect design. Not a blocker.

## Sequencing Soundness

Phase D is gated on B (files edited at canonical post-promotion paths) and runs parallel to C. There are no file conflicts: Phase C touches `plugin.json`, `README.md` Quick Start URL, and the git remote — none of which Phase D touches (D edits `CLAUDE.md`, `AGENTS.md`, `agents/coding.md`, `skills/code/SKILL.md`, `.gitattributes`, `.gitignore`). Parallel execution is safe.

## Scope Discipline

`bd worktree`, `bd swarm`, `bd remember`, `bd preflight`, and `bd q` are explicitly placed in Non-Goals and Phase D's follow-up list. No beads feature adoption is included in Phase D's step list. The architect held the line correctly.

## Risk Completeness

Existing risks are well-reasoned. Two observations:

1. The orchestrator dangling-ref risk (GitLab skill links in agent prompt) is logged and the mitigation (audit orchestrator) is adequate.
2. The sed false-positive risk (catching unintended `plugin/` strings) is covered by the mandatory `git diff` review gate.
3. One gap: `docs/spelunk/_staleness.json` appears in both Class 12's deletion list and Class 9's fix list, but the Phase A step list (A21) covers it in Subset A.3 rather than A.2. This is a minor ordering ambiguity — it resolves correctly either way since both subsets are in Phase A. Not a blocker.

## Decompose Size

Phase A is estimated at ~350 lines with a documented contingency to split A.1 and A.2 as sibling tasks if the diff grows. This is appropriate. The total of ~880 lines across four tasks is within the 4 × 1000 cap, with each task individually bounded.

## No Regressions from v1

The core v1 approvals — strip-first sequencing, marketplace.json source update, path-ref sed strategy with diff review, two-PR approach, GitHub redirect reliance — are all preserved and unchanged in v2. The three additions layer on cleanly without disturbing the v1 structure.

## Recommendation

APPROVED. All three user-authorized additions are fully covered, sequencing is safe, scope discipline is maintained, and the design contains no regressions from v1. Proceed to `/decompose`.
