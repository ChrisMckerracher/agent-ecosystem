---
name: rebalance
description: Rebalance the beads task merge tree when tasks are too large (>500 lines, max 1000) or too small (<50 lines). Used when the user says 'tasks too big', 'rebalance', 'split this task', 'tasks too granular', or when /code reports scope overflow. Adjusts task tree without losing work.
---

# /rebalance

Rebalance merge tree to maintain 500 line target per task.

## Triggers

- Task estimated > 500 lines → Split
- Task estimated > 1000 lines → **Must split**
- Multiple tiny tasks (< 50 lines each) → Consider consolidating

## Split Process

1. Identify oversized task
2. Find natural split points:
   - Separate concerns
   - Different files
   - Independent operations
3. Create child beads
4. Update dependencies
5. Report new tree structure

## Estimation Heuristics

| Indicator | Likely Size |
|-----------|-------------|
| Single function change | < 100 lines |
| New component | 200-400 lines |
| New feature with tests | 400-600 lines |
| Multiple components | > 500 lines (split!) |
| "And" in description | Probably too big |

## Output

Rebalanced: Task X

Before: 1 task (~1200 lines estimated)
After: 3 tasks (~400 lines each)

New tree:
├── Task X.1 - Component A (ready)
├── Task X.2 - Component B (ready)
└── Task X.3 - Integration (blocked by X.1, X.2)

## Commands

# Create sub-tasks
bd create "Subtask" -t task -p 1 --json

# Link as child
bd dep add <new-id> <parent-id> --type blocks

# Update original to "epic" if needed
bd update <parent-id> -t epic
