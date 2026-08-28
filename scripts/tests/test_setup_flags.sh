#!/usr/bin/env bash
# test_setup_flags.sh — Behavioral verification for non-interactive setup-leap.sh flags.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$HERE/../.."

PASS=0
FAIL=0

# Sourcing assertion helpers
source "$(dirname "${BASH_SOURCE[0]}")/../lib/assert.sh"

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

# Test 4: --qmd flag passes --remove-legacy to qmd-config
echo "Testing setup-leap.sh --qmd passes --remove-legacy..."
# Create a spy qmd-config in the sandboxed workspace's scripts/qmd directory
rm -f qmd_args.log
cat > scripts/qmd/qmd-config << 'EOF'
#!/usr/bin/env bash
echo "$@" > qmd_args.log
exit 0
EOF
chmod +x scripts/qmd/qmd-config

set +e
out=$(bash scripts/setup-leap.sh --yes --qmd < /dev/null 2>&1)
code=$?
set -e
assert_exit_code "Setup with --qmd exits with 0" 0 "$code"
assert_exists "qmd_args.log" "qmd_args.log"
assert_contains "qmd-config was invoked with --remove-legacy" "$(cat qmd_args.log)" "--remove-legacy"

echo ""
echo "Test summary: PASS=$PASS FAIL=$FAIL"

if [ "$FAIL" -gt 0 ]; then
  exit 1
else
  exit 0
fi
