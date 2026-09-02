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

# Test 5: Interactive default behavior (pressing Enter defaults to "yes" for standard options)
echo "Testing setup-leap.sh interactive defaults (piping empty input)..."
# Clean up files first
rm -f CLAUDE.md GEMINI.md .cursorrules .github/copilot-instructions.md .gitignore .git/hooks/pre-commit
# Create an empty .gitignore and pre-commit hook destination directory
touch .gitignore
mkdir -p .git/hooks

set +e
# Disable pipefail temporarily because yes "" will receive SIGPIPE (141) when setup-leap.sh exits
set +o pipefail
out=$(yes "" | bash scripts/setup-leap.sh 2>&1)
code=$?
set -o pipefail
set -e

assert_exit_code "Interactive setup with empty input exits with 0" 0 "$code"
assert_exists "CLAUDE.md" "CLAUDE.md"
assert_exists "GEMINI.md" "GEMINI.md"
assert_exists ".cursorrules" ".cursorrules"
assert_exists ".github/copilot-instructions.md" ".github/copilot-instructions.md"

# Test 6: Non-interactive username configuration via LEAP_USER env var
echo "Testing setup-leap.sh username config via LEAP_USER env var (non-interactive)..."
git config --unset leap.user || true
set +e
out=$(LEAP_USER="Env_User.123!" bash scripts/setup-leap.sh --yes < /dev/null 2>&1)
code=$?
set -e
assert_exit_code "Setup exits with 0 under LEAP_USER" 0 "$code"
cfg_user=$(git config leap.user || echo "")
assert_equals "Saves sanitized LEAP_USER in git config" "env_user.123" "$cfg_user"

# Test 7: Propose smart default from existing directory when no git config is set
echo "Testing setup-leap.sh smart default detection..."
git config --unset leap.user || true
# Create a single user directory in kb/feature/
mkdir -p kb/feature/smartuser
set +e
out=$(bash scripts/setup-leap.sh --yes < /dev/null 2>&1)
code=$?
set -e
assert_exit_code "Setup exits with 0" 0 "$code"
cfg_user=$(git config leap.user || echo "")
assert_equals "Resolves smart default from existing folder" "smartuser" "$cfg_user"
rm -rf kb/feature/smartuser

# Test 8: Interactive prompt for username
echo "Testing setup-leap.sh interactive username prompt (entering custom username)..."
git config --unset leap.user || true
set +o pipefail
out=$((echo "custom.User_7"; yes "") | bash scripts/setup-leap.sh 2>&1)
code=$?
set -o pipefail
set -e
assert_exit_code "Interactive setup with custom username exits with 0" 0 "$code"
cfg_user=$(git config leap.user || echo "")
assert_equals "Saves sanitized custom username from interactive prompt" "custom.user_7" "$cfg_user"

echo ""
echo "Test summary: PASS=$PASS FAIL=$FAIL"

if [ "$FAIL" -gt 0 ]; then
  exit 1
else
  exit 0
fi
