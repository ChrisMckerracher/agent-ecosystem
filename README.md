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

---

## Requirements

- [Claude Code](https://claude.ai/code) 2.0.74+
- [beads](https://github.com/gastownhall/beads) 1.0+ — `brew install beads` (macOS/Linux) or `curl -sSL https://raw.githubusercontent.com/gastownhall/beads/main/scripts/install.sh | bash`
- Node.js 18+

---

## License

MIT
