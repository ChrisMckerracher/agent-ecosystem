# Skill Best-Practices Research Report

**Scope:** Audit of the 14 SKILL.md files at `/Users/chrismck/claude_stuff/skills/` against current Anthropic guidance and community best practices, with concrete adoption recommendations.

**Date:** 2026-05-12
**Skills audited in depth:** `architect`, `code`, `qa`, `spelunk`, `product`, `security`, `review`, `verify`, `decompose`, `merge-up`, `rebalance`, `task-complete`, `update-claude`, `visualize`

---

## 1. Audit Summary of Our Current Skills

### Frontmatter

All 14 skills use the minimum frontmatter (`name` + `description`). None use `allowed-tools`, `license`, `disable-model-invocation`, or `metadata`.

**Description patterns we currently use:**

| Skill | Current Description |
|---|---|
| architect | "Use when starting new features, making design decisions, or analyzing codebase architecture" |
| code | "Use when implementing tasks, or understanding code relationships in a codebase" |
| qa | "Use when creating tests from specs, or analyzing test coverage in a codebase" |
| spelunk | (NO frontmatter at all — major bug) |
| product | "Use when validating designs match product goals, or understanding what problem a codebase solves" |
| security | "Use when auditing code for security vulnerabilities, or before any merge involving auth/crypto" |
| review | "Use when reviewing code changes for style guide compliance and quality standards" |
| verify | "Create and manage verify cycles for project-specific quality checks during code review" |
| decompose | "Use when breaking a feature or design into a merge tree of dependent tasks" |
| merge-up | "Use when leaf tasks are complete and you need to merge up to the parent level" |
| rebalance | "Use when tasks are too large (over 500 lines) or too small, to rebalance the merge tree" |
| task-complete | "Use when completing a task - commits work, merges to epic, rebases dependents, and closes the task bead" |
| update-claude | "Use when you receive feedback that should update project CLAUDE.md conventions" |
| visualize | "Use when you want to see the current task tree, progress, and what's ready to work on" |

**Observations:**
- Descriptions are written in **second person / imperative** ("Use when…"). The official guidance is now **third person** ("This skill should be used when…" or "Used when…").
- Descriptions are **short** (most ~70–120 chars) — well under the 250-char effective cap but they often lack concrete trigger keywords (file types, specific user phrases, error patterns).
- They describe **when** but rarely the **what** in a way that distinguishes from sibling skills.
- No skill includes "do NOT use" negative boundaries even though several have heavy overlap (`code` vs `task-complete` vs `merge-up`; `architect` vs `decompose`).

### Body Structure

**File sizes (approximate lines):**
- Long: `qa` (~246), `spelunk` (~255 — and *no frontmatter*), `architect` (~149), `merge-up` (~186), `task-complete` (~140)
- Medium: `code` (~124), `verify` (~152), `product` (~149), `decompose` (~135)
- Short: `review` (~62), `security` (~62), `rebalance` (~58), `visualize` (~46), `update-claude` (~52)

Most of our skills fall under the 500-line ceiling, which is good. `qa` and `spelunk` are the heaviest and have the most content that could be moved to `references/`.

**Voice in body:** Mixed — switches between "You are…", imperative ("Read the file"), and declarative ("Agent activates…"). Inconsistent.

**Examples sections:** Mostly absent. Only `code`, `verify`, and `visualize` have anything labeled "Examples." None use the canonical `<example>…</example>` XML-tag pattern recommended in Anthropic's prompting docs.

**Use of references/:** **Zero skills** use a `scripts/`, `references/`, or `assets/` subdirectory. All content is inline in SKILL.md. (`task-complete` references `scripts/task-complete.sh` outside the skill folder, which isn't the canonical layout.)

**Progressive disclosure:** Not really used. `spelunk` has the most content that *should* be split out (TypeScript code samples, lens descriptions, LSP workflow phases).

### Critical Bugs Found

1. **`skills/spelunk/SKILL.md` has NO YAML frontmatter.** It opens directly with `# Spelunk Mode`. This skill will not auto-trigger at all — Claude has no `description` field to match against. This is the most urgent fix.
2. **`update-claude`** body literally edits CLAUDE.md inline at line ~40; it's just a "Code Standards / Logging" block dropped into the SKILL.md without a fence, which makes the file read as if it's actively defining CLAUDE.md content. Confusing rendering.
3. **`visualize`** ends with a section "Beads Commands (invisible)" — that subhead phrasing is unusual and the bash isn't in a code fence.

---

## 2. External Best Practices (Research Findings)

### 2.1 Description Field — The Single Most Important Field

**Pattern:** Use a `What + When` formula, in **third person**, packed with concrete trigger strings.

**Why it works:** Claude scans descriptions (~100 tokens per skill) at session start to decide which skills to load on demand. The description is matched against the *current user request*, so it must include the strings users actually say. Anthropic's official guidance says Claude tends to **under-trigger** skills, so descriptions should be slightly "pushy."

**Canonical good example (from Anthropic skill-creator guidance):**
> "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."

**Limits:**
- API spec: max **1024 characters**
- Practical Claude Code `/skills` listing cap: **250 characters** (truncation point)
- Put highest-signal trigger words **in the first 250 characters**

**Gap in our skills:** Our descriptions average ~80 chars — we have ~170 chars of unused budget. We're also second-person ("Use when…"), and we have no concrete trigger strings. Compare:
- Ours: *"Use when starting new features, making design decisions, or analyzing codebase architecture"*
- Idiomatic: *"Architecture design and codebase analysis for new features. This skill should be used when the user mentions designing, planning, or starting a new feature; when they say 'how is X structured', 'analyze architecture', or 'plan implementation'; or before any non-trivial implementation work begins."*

### 2.2 Third-Person Voice

**Pattern:** Write descriptions in third person ("This skill is used when…", "Used when…", "Used for…").

**Why it works:** First person ("I can help…") and second person ("You can use this to…") clash with Claude's system prompt structure. The description is injected into Claude's system prompt; voice mismatch causes discovery problems.

**Gap:** All 14 of our descriptions use "Use when…" (second-person imperative).

### 2.3 Specificity — Strings, Not Concepts

**Pattern:** Include the *actual phrases* users say, the file extensions involved, the tools/frameworks named. Claude is doing string matching as much as semantic matching.

**Why it works:** A description like "helps with code review" never triggers reliably. "Code style review for TypeScript, Python, Go. Use when the user says 'review this', 'check my code', mentions PRs, diffs, or commits before merging" matches concrete user input.

**Gap:** Our `qa` description says "creating tests" but doesn't mention `Playwright`, `Gherkin`, `.feature`, `e2e`, `unit tests`, `coverage` — all terms users would actually use.

### 2.4 "When NOT to use" / Disambiguation

**Pattern:** When multiple skills have overlapping triggers, include negative boundaries: "Do NOT use for X — use Y instead."

**Why it works:** Anthropic explicitly notes that with 5+ skills, overlap causes the wrong skill to fire (e.g., Content Repurposer beats Email Drafter on "draft an email"). Negative boundaries help Claude disambiguate.

**Gap — major in our case:** We have heavy overlap among:
- `code` vs `task-complete` (both close tasks)
- `code` vs `merge-up` vs `task-complete` (all merge child branches)
- `architect` vs `decompose` (both break down features)
- `product` vs `architect` (both "plan features")
- `review` vs `verify` vs `security` (all run quality checks)

None of these skills disambiguate from each other in the description.

### 2.5 Progressive Disclosure via `references/`, `scripts/`, `assets/`

**Pattern:** Keep SKILL.md body under ~500 lines (target ~1,500–2,000 words). Move deep content (long examples, reference tables, scripts) to:
- `scripts/` — executable code for deterministic operations
- `references/` — deep-dive docs loaded only when needed
- `assets/` — templates, fixtures used in outputs

The SKILL.md body links to them: "For full Gherkin→Playwright mapping, see `references/playwright-mapping.md`."

**Why it works:** Once a skill loads, every line in its body costs tokens on every turn. Linked files are only read if the agent decides they're needed. This is the whole point of "progressive disclosure."

**Gap — large:** No skill uses this pattern.
- `spelunk` should have `references/lens-specs.md`, `references/lsp-workflow.md`
- `qa` should have `references/gherkin-to-playwright.md`, `references/selector-strategy.md`
- `merge-up` should have `references/conflict-resolution.md`
- `code` should have `scripts/` referenced from inside the skill rather than from the plugin root

### 2.6 Imperative Voice in Body Instructions

**Pattern:** Anthropic explicitly says: "Prefer using the imperative form in instructions." Imperative is concise, unambiguous, and matches recipe/documentation style.

**Why it works:** Imperative ("Read the spec. Extract scenarios. Write tests.") is denser and clearer than "You should read the spec, then you should extract scenarios, then you should write tests." It also avoids the second-person voice that conflicts with system-prompt framing.

**Gap:** Our skills mix voices — `architect` says "You are a DOCUMENTATION-LAYER agent" but then "Agent activates in appropriate mode". `qa` mixes "QA Agent CAN…" with "Read…", "Generate…". Inconsistent.

### 2.7 `<example>` XML-Tag Examples

**Pattern:** Wrap concrete worked examples in `<example>` tags (multiple in `<examples>`). Include 3–5 examples showing input → expected output.

**Why it works:** Anthropic's prompting docs explicitly recommend XML tags because Claude was trained to attend to them. Examples are "one of the most reliable ways to steer Claude's output." Few-shot examples dramatically improve consistency.

**Gap:** Zero skills use `<example>` tags. `code` has an "## Examples" section with bash snippets, which is OK but not idiomatic. `qa` has a "Generated Test Template" but no realistic worked example.

### 2.8 One Skill, One Job

**Pattern:** Avoid "mega-skills" that do many things. Composable single-purpose skills are easier to trigger correctly and easier to maintain.

**Why it works:** Mega-skills have lower accuracy because the description has to be vaguer to cover multiple jobs, which makes triggering ambiguous.

**Gap:** A few of our skills are bordering on mega-skill:
- `code` covers task implementation, worktree management, merge-up, and bead closure
- `qa` covers Gherkin parsing, Playwright generation, coverage analysis, *and* test-from-spec
- `product` covers spec writing, brief writing, design validation, *and* codebase examination

Several of these could be decomposed (e.g., `product/spec`, `product/brief`, `product/validate` as separate skills) — though we already use subcommands inside one skill, which is a reasonable middle ground.

### 2.9 Role Framing

**Pattern:** Open the body with one or two sentences naming the role: "You are a senior security auditor reviewing code for OWASP Top 10 vulnerabilities." Specific, not vague ("seasoned generalist").

**Why it works:** Concrete role framing primes Claude to adopt the right persona and reasoning style.

**Gap:** Several skills lack role framing (`decompose`, `merge-up`, `rebalance`, `visualize`, `update-claude`, `task-complete`, `verify`). They jump straight to mechanics. Only `architect`, `qa`, `product` open with persona/boundary framing — though those are more constraint-heavy than role-rich.

### 2.10 `allowed-tools` Frontmatter

**Pattern:** Use `allowed-tools` in frontmatter to declare the tool surface the skill needs.

```yaml
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
```

**Caveat:** GitHub issue [anthropics/claude-code#37683](https://github.com/anthropics/claude-code/issues/37683) reports `allowed-tools` is parsed but not enforced as a hard restriction in Claude Code currently. So this is more documentation/intent than enforcement — but it still helps with skill discovery and serves as readable contract.

**Gap:** No skill uses this field. We currently embed tool restrictions as `<ACTIVE_BOUNDARY>` XML blocks inside the body, which is verbose (~15-20 lines per skill) and not the canonical pattern.

### 2.11 Description Length Budget

**Pattern:** Aim for 130–250 effective characters for the listing-visible portion, with extended detail allowed up to 1024 chars total.

**Why it works:** Claude Code truncates at 250 chars in `/skills` listings. Skills with descriptions exceeding 650 chars in some installations are silently dropped (see [danielmiessler/Personal_AI_Infrastructure#1205](https://github.com/danielmiessler/Personal_AI_Infrastructure/issues/1205)).

**Gap:** Our descriptions are *too short*, not too long — we're not using the budget for concrete trigger keywords.

### 2.12 Drafting + Testing Discipline

**Pattern:** From skill-creator: write a draft, then look at it with fresh eyes; write 2–3 realistic test prompts (the kind a user would actually say); for each test prompt, read the SKILL.md and follow its instructions yourself to see if they work.

**Why it works:** Catches ambiguity and missing steps before the skill ships. Most "skill never triggers" bugs are description problems caught by writing 3 realistic test prompts.

**Gap:** No evidence we have written test prompts for any of our skills. The spelunk skill missing its frontmatter entirely is the kind of bug a single test-prompt run would catch.

---

## 3. Per-Skill Quick Findings

| Skill | Top issue(s) |
|---|---|
| **spelunk** | **CRITICAL: missing frontmatter entirely.** Will never auto-trigger. |
| **architect** | Heavy XML boundary blocks should move to a `references/boundary.md`; description lacks trigger keywords like "design doc", "ADR", "feature spec" |
| **code** | Description doesn't disambiguate from `task-complete`/`merge-up`; mega-skill scope |
| **qa** | Long body (~246 lines); Gherkin→Playwright table belongs in `references/`; description doesn't mention "Playwright", "Gherkin", ".feature" |
| **product** | Same boundary-XML bloat as architect; subcommands could be separate skills |
| **security** | Description is fine; body is short and clean — good template |
| **review** | Description lacks "PR", "diff", "before merge"; weak role framing |
| **verify** | Description verb-first ("Create and manage…") instead of "Use when…"; otherwise OK |
| **decompose** | Description lacks "epic", "worktree", "merge tree", "tasks" specifics; bash-heavy body could move to scripts |
| **merge-up** | Heavy bash content (~186 lines) should move to `scripts/` |
| **rebalance** | Tiny but useful; description could be much more concrete |
| **task-complete** | Overlaps with `code` and `merge-up` — needs disambiguation; script lives outside skill folder |
| **update-claude** | Body has unfenced code-as-content rendering bug at ~line 40 |
| **visualize** | "(invisible)" subhead is weird; bash unfenced |

---

## 4. Prioritized Recommendations (Top 8)

### P0 — Fix data-integrity bug now

**1. Add frontmatter to `skills/spelunk/SKILL.md`.**
It currently has none, so it cannot auto-trigger. Add:
```yaml
---
name: spelunk
description: Targeted codebase exploration with hash-cached documentation. Used when an agent needs structured info about code interfaces, flows, boundaries, contracts, or trust zones in a codebase. Triggers on requests like "explore X", "understand Y module", "map auth flow", "what interfaces exist in Z", or when called via /code spelunk.
---
```
**Effort:** 2 minutes. **Impact:** Restores triggering for one of our most-referenced skills.

### P1 — Rewrite all descriptions (biggest leverage)

**2. Rewrite all 14 descriptions in third-person `What + When` form, with concrete trigger strings, using ~200–250 chars.**

Template:
```
[What it does, third person]. Used when [user phrase 1], [user phrase 2], or when [trigger context]. [Optional: file types/tools]. [Optional: NOT for X — use Y instead].
```

Worked example for `qa`:
> Before:
> "Use when creating tests from specs, or analyzing test coverage in a codebase"
>
> After:
> "Test generation and coverage analysis. Used when the user asks to 'write tests', 'generate tests', 'add e2e tests', or mentions Playwright, Gherkin, `.feature` files, or coverage gaps. Also used after a Gherkin spec is approved to generate executable Playwright tests. Not for code style review — use /review."

**Effort:** ~3 hours for all 14. **Impact:** Highest single improvement to trigger reliability.

### P2 — Adopt `references/` progressive disclosure for the 3 heaviest skills

**3. Split `spelunk`, `qa`, `merge-up` into SKILL.md + `references/`.**
- `spelunk/SKILL.md` keeps the command syntax and quick examples; move LSP workflow code, lens descriptions, programmatic usage to `spelunk/references/`
- `qa/SKILL.md` keeps the workflow; move Gherkin→Playwright table, selector strategy, video config to `qa/references/playwright-mapping.md`
- `merge-up/SKILL.md` keeps the high-level flow; move bash recipes to `merge-up/scripts/` and conflict resolution to `merge-up/references/conflict-resolution.md`

**Effort:** ~2 hours per skill. **Impact:** Cuts per-turn token cost for the most-used skills.

### P3 — Add disambiguation across the merge/task family

**4. Add "Not for…" lines in `code`, `task-complete`, `merge-up` descriptions.**
- `code`: "Not for merging tasks — use /task-complete. Not for upward merges — use /merge-up."
- `task-complete`: "Not for implementing — use /code. Not for upward (epic→main) merges — use /merge-up."
- `merge-up`: "Not for task completion — use /task-complete handles the task→epic step automatically."

**Effort:** 20 minutes. **Impact:** Eliminates the most likely wrong-skill-fires.

### P4 — Standardize body voice and role framing

**5. Convert all bodies to imperative voice and add a one-sentence role frame at the top of each.**

Pattern:
```markdown
# /qa

You are the QA Agent: a test architect who generates executable tests from specs and audits coverage.

## When activated
Read the feature spec. Extract scenarios. Generate Playwright tests…
```

**Effort:** ~4 hours across all skills. **Impact:** Consistency, clearer agent persona, denser instructions.

### P5 — Add 2–3 `<example>` blocks per agent-facing skill

**6. Replace bash-snippet "Examples" sections with `<example>` XML tags showing realistic user input → skill behavior.**

Pattern:
```markdown
## Examples

<example>
User: "Generate tests for the login spec we just approved"
Skill response:
1. Reads docs/specs/features/login.feature
2. Detects Background → beforeEach
3. Writes tests/e2e/login.spec.ts with 3 scenarios + 1 outline
4. Reports missing data-testid attributes
</example>

<example>
User: "What's our test coverage on payments?"
Skill response:
1. Delegates: /code spelunk --for=qa --focus="payments"
2. Reads docs/spelunk/contracts/payments.md
3. Returns gap analysis: 4 contracts uncovered, list paths
</example>
```

**Effort:** ~2 hours total. **Impact:** Few-shot priming for output consistency.

### P6 — Test each skill with 3 realistic prompts

**7. For each skill, write 3 realistic user prompts and run them. Note which skill actually fires and whether the body's instructions actually work.**

Anthropic's skill-creator explicitly recommends this as the validation step. We almost certainly have skills that don't trigger when expected.

**Effort:** 1 day. **Impact:** Catches description and instruction bugs before users hit them.

### P7 — Adopt `allowed-tools` frontmatter as documentation

**8. Add `allowed-tools` to skills with explicit tool boundaries (architect, product, qa).**

Currently we use `<ACTIVE_BOUNDARY>` XML blocks ~15 lines long. Replace the top portion with:
```yaml
---
name: architect
description: ...
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - Task
---
```
Keep the documentation-layer enforcement language in the body but tighten it. Note: enforcement may not be hard-blocked by Claude Code currently (per [issue #37683](https://github.com/anthropics/claude-code/issues/37683)), but the field is the canonical signal and saves body tokens.

**Effort:** 1 hour. **Impact:** Idiomatic structure, slightly shorter bodies.

---

## 5. What We're Already Doing Well

- **Tables for structured data** — matches our CLAUDE.md style guide and is widely recommended.
- **Subcommand routing** (`/qa generate-tests`, `/product spec`) is a reasonable middle ground between "one skill one job" and "mega-skill."
- **Most bodies under 500 lines** — already inside Anthropic's recommended ceiling.
- **Mermaid/ASCII tree output formats** (visualize, decompose) — these match the "concrete output template" pattern from skill-creator.
- **`security`'s body** is short, role-clear, and references docs/spelunk for context — good template for the smaller skills to follow.

---

## Sources

- [Skill authoring best practices — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Agent Skills overview — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
- [anthropics/skills (official skill repo)](https://github.com/anthropics/skills)
- [anthropics/skills — skill-creator/SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [anthropics/claude-code — plugins/plugin-dev/skills/skill-development/SKILL.md](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md)
- [The Complete Guide to Building Skills for Claude (Anthropic PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf)
- [Equipping agents for the real world with Agent Skills — Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Agent Skills: A First Principles Deep Dive — Lee Hanchung](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
- [SKILL.md Specification — Agensi](https://www.agensi.io/learn/skill-md-format-reference)
- [Claude Code Skill Frontmatter: Every YAML Option Explained — Frontend Master](https://allahabadi.dev/blogs/ai/claude-code-skills-frontmatter-complete-guide/)
- [Inside Claude Code Skills — Mikhail Shilkov](https://mikhail.io/2025/10/claude-code-skills/)
- [7 Rules for Creating an Effective Claude Code Skill — Nick Babich, UX Planet](https://uxplanet.org/7-rules-for-creating-an-effective-claude-code-skill-2d81f61fc7cd)
- [Why Claude Code Skills Don't Trigger (and How to Fix Them) — DEV Community](https://dev.to/lizechengnet/why-claude-code-skills-dont-trigger-and-how-to-fix-them-in-2026-o7h)
- [Claude Code Skills Don't Auto-Activate — Scott Spence](https://scottspence.com/posts/claude-code-skills-dont-auto-activate)
- [VoltAgent/awesome-agent-skills (1000+ community skills)](https://github.com/VoltAgent/awesome-agent-skills)
- [VoltAgent/awesome-claude-code-subagents (100+ subagents)](https://github.com/VoltAgent/awesome-claude-code-subagents)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [Prompting best practices (XML tags / examples) — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [GitHub issue: allowed-tools not enforced in SKILL.md](https://github.com/anthropics/claude-code/issues/37683)
- [GitHub issue: 43/46 skill descriptions exceed 650-char silent-drop ceiling](https://github.com/danielmiessler/Personal_AI_Infrastructure/issues/1205)
- [GitHub issue: 250-char description display cap in /skills listing](https://github.com/anthropics/claude-code/issues/40121)
