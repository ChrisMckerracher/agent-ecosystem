#!/usr/bin/env bash
# init-harness: strict, atomic copy of universal harness templates into a target repo.
#
# Strictness contract:
#   - If ANY target path already exists, abort with exit 2 and write nothing.
#     Use --force to overwrite (the only way past the abort).
#   - --dry-run prints the planned copies and exits 0 without writing.
#   - Language preset controls which docs/standards/<lang>.md file is included.
#   - Per-file copy is atomic (write to <target>.tmp then mv into place).
#
# Required: bash 4+, coreutils (cp, mkdir, mv).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/templates"

ROOT="."
PROJECT_NAME=""
LANGUAGE="polyglot"      # python | typescript | polyglot
DRY_RUN=0
FORCE=0

usage() {
  cat <<'EOF'
Usage: install.sh [--root PATH] [--project-name NAME]
                  [--language python|typescript|polyglot]
                  [--dry-run] [--force]

Installs the universal harness templates (AGENTS.md, CLAUDE.md, CODEX.md, and
docs/) into the target repo. Strictly refuses to overwrite existing files
unless --force is passed; on any conflict without --force, exits 2 without
writing anything.

Flags:
  --root PATH           Target dir to install into (default: current dir)
  --project-name NAME   Used in placeholder text (default: directory basename)
  --language LANG       Adds docs/standards/<lang>.md when applicable
                        Values: python | typescript | polyglot (default)
  --dry-run             Print the planned copies and exit 0; write nothing
  --force               Overwrite existing files (the only way past conflicts)
  -h, --help            Show this help
EOF
}

die() { echo "ERROR: $*" >&2; exit 2; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --root) ROOT="$2"; shift 2 ;;
    --project-name) PROJECT_NAME="$2"; shift 2 ;;
    --language) LANGUAGE="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --force) FORCE=1; shift ;;
    *) die "Unknown flag: $1 (try --help)" ;;
  esac
done

case "$LANGUAGE" in
  python|typescript|polyglot) ;;
  *) die "Invalid --language: $LANGUAGE (expected python|typescript|polyglot)" ;;
esac

[[ -d "$TEMPLATE_DIR" ]] || die "Template directory not found: $TEMPLATE_DIR"

if [[ ! -d "$ROOT" ]]; then
  die "Target root does not exist: $ROOT"
fi
ROOT="$(cd "$ROOT" && pwd)"

if [[ -z "$PROJECT_NAME" ]]; then
  PROJECT_NAME="$(basename "$ROOT")"
fi

# ---- Build (source, target) pair list ----
# Walk TEMPLATE_DIR; skip language-specific files that don't match the preset.
PAIRS=()
while IFS= read -r src; do
  rel="${src#"$TEMPLATE_DIR"/}"

  # Language filtering for docs/standards/{python,typescript}.md
  case "$rel" in
    docs/standards/python.md)
      [[ "$LANGUAGE" == "python" || "$LANGUAGE" == "polyglot" ]] || continue
      ;;
    docs/standards/typescript.md)
      [[ "$LANGUAGE" == "typescript" || "$LANGUAGE" == "polyglot" ]] || continue
      ;;
  esac

  PAIRS+=("$src|$ROOT/$rel")
done < <(find "$TEMPLATE_DIR" -type f \! -name '.DS_Store' | sort)

if [[ ${#PAIRS[@]} -eq 0 ]]; then
  die "No templates resolved (check TEMPLATE_DIR and --language)"
fi

# ---- Pre-flight: detect conflicts ----
CONFLICTS=()
for pair in "${PAIRS[@]}"; do
  target="${pair#*|}"
  if [[ -e "$target" ]]; then
    CONFLICTS+=("${target#"$ROOT"/}")
  fi
done

if [[ ${#CONFLICTS[@]} -gt 0 && "$FORCE" -eq 0 ]]; then
  {
    echo "ERROR: ${#CONFLICTS[@]} target path(s) already exist:"
    for c in "${CONFLICTS[@]}"; do echo "  - $c"; done
    echo "No files written. Use --force to overwrite, or remove the existing"
    echo "files first."
  } >&2
  exit 2
fi

# ---- Plan summary ----
echo "init-harness plan"
echo "  root:         $ROOT"
echo "  project name: $PROJECT_NAME"
echo "  language:     $LANGUAGE"
echo "  dry-run:      $([[ $DRY_RUN -eq 1 ]] && echo yes || echo no)"
echo "  force:        $([[ $FORCE -eq 1 ]] && echo yes || echo no)"
echo "  files:        ${#PAIRS[@]}"
echo

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "Would create/overwrite:"
  for pair in "${PAIRS[@]}"; do
    src="${pair%|*}"; target="${pair#*|}"
    flag="+"
    [[ -e "$target" ]] && flag="!"
    echo "  $flag ${target#"$ROOT"/}"
  done
  echo
  echo "(no files written; --dry-run)"
  exit 0
fi

# ---- Atomic per-file copy ----
CREATED=()
OVERWROTE=()
for pair in "${PAIRS[@]}"; do
  src="${pair%|*}"
  target="${pair#*|}"
  mkdir -p "$(dirname "$target")"
  tmp="$target.tmp.$$"
  cp "$src" "$tmp"
  if [[ -e "$target" ]]; then
    mv -f "$tmp" "$target"
    OVERWROTE+=("${target#"$ROOT"/}")
  else
    mv "$tmp" "$target"
    CREATED+=("${target#"$ROOT"/}")
  fi
done

# ---- Report ----
echo "Created (${#CREATED[@]}):"
for f in "${CREATED[@]:-}"; do
  [[ -n "$f" ]] && echo "  + $f"
done

if [[ ${#OVERWROTE[@]} -gt 0 ]]; then
  echo
  echo "Overwrote with --force (${#OVERWROTE[@]}):"
  for f in "${OVERWROTE[@]}"; do
    echo "  * $f"
  done
fi

echo
echo "Next steps:"
echo "  1. Read AGENTS.md and tighten rules that don't fit your project."
echo "  2. Fill in docs/repo-map.md with real packages once they exist."
echo "  3. Write your first design doc into docs/plans/architect/."
echo "  4. bd create --design=docs/plans/architect/<doc>.md --type=epic ..."
