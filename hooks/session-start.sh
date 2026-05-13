#!/usr/bin/env bash
# Session start hook - load context and show ready tasks

# Read hook input
INPUT=$(cat)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

# Inject plugin root into Claude's context.
#
# Why: ${CLAUDE_PLUGIN_ROOT} does NOT expand in slash command markdown bodies
# (anthropics/claude-code#9354, open since Oct 2025; still unresolved as of
# May 2026). It DOES expand in hook JSON, so we print the resolved path here
# and command files reference it via the {AGENT_ECOSYSTEM_ROOT} text
# placeholder, which Claude substitutes when composing Bash calls.
#
# When #9354 ships, remove this block and revert commands/*.md to
# ${CLAUDE_PLUGIN_ROOT}.
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
    echo "AGENT_ECOSYSTEM_ROOT=\"${CLAUDE_PLUGIN_ROOT}\""
fi

# Check if beads initialized in project
if [ -d "$CWD/.beads" ]; then
    # Get ready tasks
    READY=$(cd "$CWD" && bd ready --json 2>/dev/null)

    if [ -n "$READY" ] && [ "$READY" != "[]" ]; then
        COUNT=$(echo "$READY" | jq 'length')

        # Output context for Claude
        echo "Project has beads task tracking. $COUNT task(s) ready to work on."
        echo "Use /visualize to see full task tree."
    fi
fi

# Always exit 0 for non-blocking
exit 0
