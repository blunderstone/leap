#!/usr/bin/env bash
# test_setup_flags.sh — Behavioral verification for non-interactive setup-leap.sh flags.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$HERE/../.."

PASS=0
FAIL=0

assert_exit_code() {
  local label="$1"
  local expected="$2"
  local actual="$3"
  if [ "$actual" -eq "$expected" ]; then
    PASS=$((PASS+1))
    printf "  ok   %s (exit %d)\n" "$label" "$actual"
  else
    FAIL=$((FAIL+1))
    printf "  FAIL %s: expected %d, got %d\n" "$label" "$expected" "$actual"
  fi
}

assert_exists() {
  local label="$1"
  local path="$2"
  if [ -e "$path" ]; then
    PASS=$((PASS+1))
    printf "  ok   %s exists: %s\n" "$label" "$path"
  else
    FAIL=$((FAIL+1))
    printf "  FAIL %s does not exist: %s\n" "$label" "$path"
  fi
}

assert_not_exists() {
  local label="$1"
  local path="$2"
  if [ ! -e "$path" ]; then
    PASS=$((PASS+1))
    printf "  ok   %s does not exist (as expected): %s\n" "$label" "$path"
  else
    FAIL=$((FAIL+1))
    printf "  FAIL %s exists but should not: %s\n" "$label" "$path"
  fi
}

# Create temp workspace
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Created temp workspace at $TEMP_DIR"

cd "$TEMP_DIR"
git init -q
git config user.name "Test User"
git config user.email "test@example.com"

# Replicate structures
mkdir -p scripts/qmd
cp "$ROOT/scripts/setup-leap.sh" scripts/
cp "$ROOT/scripts/install-skills.py" scripts/
cp -r "$ROOT/.skills" .skills
cp -r "$ROOT/scripts/qmd" scripts/

# Test 1: Help flag
echo "Testing setup-leap.sh --help..."
set +e
out=$(bash scripts/setup-leap.sh --help 2>&1)
code=$?
set -e
assert_exit_code "--help exits with 0" 0 "$code"
if [[ "$out" =~ "Usage:" ]] && [[ "$out" =~ "--yes" ]]; then
  PASS=$((PASS+1))
  echo "  ok   --help output contains Usage and --yes"
else
  FAIL=$((FAIL+1))
  echo "  FAIL --help output missing key sections: $out"
fi

# Test 2: Non-interactive --no mode (rejects everything)
echo "Testing setup-leap.sh --no (non-interactive, stdin from /dev/null)..."
set +e
# Run with stdin redirected to /dev/null to guarantee it cannot read from terminal
out=$(bash scripts/setup-leap.sh --no < /dev/null 2>&1)
code=$?
set -e
assert_exit_code "--no exits with 0" 0 "$code"
assert_not_exists "CLAUDE.md" "CLAUDE.md"
assert_not_exists "GEMINI.md" "GEMINI.md"
assert_not_exists ".cursorrules" ".cursorrules"

# Test 3: Selective component non-interactive mode
echo "Testing selective setup-leap.sh --no --claude --gemini (stdin from /dev/null)..."
# Clean up files if any
rm -f CLAUDE.md GEMINI.md .cursorrules
set +e
out=$(bash scripts/setup-leap.sh --no --claude --gemini < /dev/null 2>&1)
code=$?
set -e
assert_exit_code "Selective override exits with 0" 0 "$code"
assert_exists "CLAUDE.md" "CLAUDE.md"
assert_exists "GEMINI.md" "GEMINI.md"
assert_not_exists ".cursorrules" ".cursorrules"

echo ""
echo "Test summary: PASS=$PASS FAIL=$FAIL"

if [ "$FAIL" -gt 0 ]; then
  exit 1
else
  exit 0
fi
