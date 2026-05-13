#!/usr/bin/env bash
# Run the trigger-rate eval pipeline across every skill that has an eval-set.
#
# Outputs evals/results/skill-trigger-rates.json and a human-readable table
# on stderr. Exits non-zero if any skill misses the >=60% positive / <=10%
# false-positive thresholds.
#
# Requires: python3, claude CLI on PATH (the pipeline shells out to `claude -p`).

set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v claude >/dev/null 2>&1; then
  echo "ERROR: claude CLI not found on PATH. Install Claude Code first." >&2
  echo "       https://docs.anthropic.com/en/docs/claude-code" >&2
  exit 2
fi

RUNS_PER_QUERY="${RUNS_PER_QUERY:-3}"
TIMEOUT="${TIMEOUT:-30}"
NUM_WORKERS="${NUM_WORKERS:-10}"
OUTPUT="${OUTPUT:-evals/results/skill-trigger-rates.json}"
EXTRA_ARGS=()
if [[ -n "${MODEL:-}" ]]; then
  EXTRA_ARGS+=(--model "$MODEL")
fi

# Restrict to specific skills via positional args, or run them all.
for s in "$@"; do
  EXTRA_ARGS+=(--skill "$s")
done

cd evals/skill-creator
exec python3 -m scripts.aggregate_skills \
  --runs-per-query "$RUNS_PER_QUERY" \
  --timeout "$TIMEOUT" \
  --num-workers "$NUM_WORKERS" \
  --output "$OUTPUT" \
  ${EXTRA_ARGS[@]+"${EXTRA_ARGS[@]}"}
