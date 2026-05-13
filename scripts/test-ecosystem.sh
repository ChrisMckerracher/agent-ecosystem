#!/usr/bin/env bash
# Test the ecosystem installation

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

pass() { echo -e "${GREEN}PASS:${NC} $1"; }
fail() { echo -e "${RED}FAIL:${NC} $1"; exit 1; }

echo "Testing Agent Ecosystem..."
echo ""

# Check beads
if command -v bd &> /dev/null; then
    pass "beads installed"
else
    fail "beads not installed"
fi

# Plugin root = repo root (one level up from this script)
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
    pass "plugin root resolved: $PLUGIN_DIR"
else
    fail "plugin root missing .claude-plugin/plugin.json (looked in $PLUGIN_DIR)"
fi

# Check required agent files
AGENTS=(
    "agents/orchestrator.md"
    "agents/architect.md"
    "agents/product.md"
    "agents/coding.md"
    "agents/qa.md"
    "agents/code-review.md"
    "agents/security.md"
)

for file in "${AGENTS[@]}"; do
    if [ -f "$PLUGIN_DIR/$file" ]; then
        pass "$file"
    else
        fail "missing $file"
    fi
done

# Check required skill files (MVP: 5 user-facing skills + spelunk internal)
SKILLS=(
    "skills/architect/SKILL.md"
    "skills/product/SKILL.md"
    "skills/code/SKILL.md"
    "skills/review/SKILL.md"
    "skills/merge-up/SKILL.md"
    "skills/spelunk/SKILL.md"
)

for file in "${SKILLS[@]}"; do
    if [ -f "$PLUGIN_DIR/$file" ]; then
        pass "$file"
    else
        fail "missing $file"
    fi
done

# Check hooks
HOOKS=(
    "hooks/session-start.sh"
    "hooks/pre-push-security.sh"
)

for file in "${HOOKS[@]}"; do
    if [ -f "$PLUGIN_DIR/$file" ]; then
        if [ -x "$PLUGIN_DIR/$file" ]; then
            pass "$file (executable)"
        else
            fail "$file exists but not executable"
        fi
    else
        fail "missing $file"
    fi
done

# Check templates
TEMPLATES=(
    "templates/design-doc.md"
    "templates/mr-description.md"
)

for file in "${TEMPLATES[@]}"; do
    if [ -f "$PLUGIN_DIR/$file" ]; then
        pass "$file"
    else
        fail "missing $file"
    fi
done

# Check commands (slash commands — MVP set + orchestrator)
COMMANDS=(
    "commands/architect.md"
    "commands/code.md"
    "commands/review.md"
    "commands/product.md"
    "commands/merge-up.md"
    "commands/orchestrator.md"
)

for file in "${COMMANDS[@]}"; do
    if [ -f "$PLUGIN_DIR/$file" ]; then
        pass "$file"
    else
        fail "missing $file"
    fi
done

echo ""
echo -e "${GREEN}All tests passed!${NC}"
echo ""
echo "Agent Ecosystem is ready to use."
