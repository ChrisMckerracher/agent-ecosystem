# Agent Ecosystem

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue.svg)](https://claude.ai/code)

> 7 specialized AI agents that design, implement, review, and ship code with [Claude Code](https://claude.ai/code).

**Agents:** Orchestrator, Architect, Product, Coding, QA, Code Review, Security

**Features:**
- Merge tree workflows for parallel task execution
- Persistent codebase exploration (spelunk)
- Invisible task tracking via [beads](https://github.com/gastownhall/beads) (Dolt SQL, multi-agent coordination)

```bash
/architect    # Co-design with human
/decompose    # Break into parallel tasks
/code         # Implement (TDD)
/review       # Quality gate
```

[Full Documentation](docs/agent-ecosystem/README.md)

---

## Quick Start

```bash
/plugin marketplace add https://github.com/ChrisMckerracher/agent-ecosystem
/plugin install agent-ecosystem
```

Then in a fresh repo:

```bash
/init-harness    # Scaffold AGENTS.md + docs/standards/ + design-doc / spelunk homes
```

---

## Slash Commands

| Category | Command | What it does |
|---|---|---|
| **Init / setup** | `/init-harness` | Scaffold the universal harness (AGENTS.md, docs/standards, docs/plans/architect, docs/spelunk) into a target repo via a strict atomic-refuse installer |
| **Design & planning** | `/architect` | Co-design new features or analyze codebase architecture |
| | `/product` | Validate designs against product goals; write Gherkin specs |
| | `/decompose` | Break a design into a merge tree of dependent tasks |
| | `/rebalance` | Rebalance the task tree when tasks are too large or too small |
| **Implementation** | `/code` | Implement a task via TDD |
| | `/qa` | Generate tests from specs; analyze test coverage |
| | `/review` | Code review for style and quality |
| | `/security` | Security audit (OWASP, secrets, CVEs) — has VETO authority |
| | `/verify` | Run project-specific verification cycles |
| **Coordination** | `/orchestrator` | Route work between specialist agents |
| | `/merge-up` | Merge a completed leaf task up to its epic |
| | `/update-claude` | Update CLAUDE.md with new conventions or feedback |
| **Visibility** | `/visualize` | Show the task tree with progress and ready work |
| | `/dashboard` | Open the agent ecosystem dashboard |

---

## Requirements

- [Claude Code](https://claude.ai/code) 2.0.74+
- [beads](https://github.com/gastownhall/beads) 1.0+ — `brew install beads` (macOS/Linux) or `curl -sSL https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh | bash`
- Node.js 18+

---

## License

MIT
