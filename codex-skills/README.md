# Codex Skills

This directory contains Codex-compatible copies of the Claude-oriented skills in `skills/`.

The original Claude skills are intentionally left unchanged. To install these for Codex, copy the desired skill directories into `${CODEX_HOME:-$HOME/.codex}/skills/`, preserving each directory's `SKILL.md` and `agents/openai.yaml`.

Conventions used here:

- `SKILL.md` frontmatter contains only `name` and `description`.
- Trigger descriptions are explicit because Codex reads them before loading the body.
- Bodies are concise playbooks with workflows, commands, outputs, and final checks.
- Claude-only tool calls such as `Task(...)` are replaced with Codex-compatible delegation guidance.
- `agents/openai.yaml` provides UI metadata and a default prompt for each skill.
