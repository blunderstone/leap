#!/usr/bin/env bash
# test_pre_commit_installation.sh — Behavioral verification for git pre-commit hook.
#
# Validates that scripts/setup-leap.sh correctly installs the pre-commit hook,
# and that the hook successfully permits/rejects commits based on run-all-checks.sh.
#
# Run: bash scripts/tests/test_pre_commit_installation.sh
#
# Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)
#
# Copyright 2026 Blunderstone LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

# Initialize git repository
cd "$TEMP_DIR"
git init -q
git config user.name "Test User"
git config user.email "test@example.com"

# Replicate LEAP repo structure inside TEMP_DIR
mkdir -p scripts/tests
cp "$ROOT/scripts/setup-leap.sh" scripts/
# We copy git-pre-commit (if it exists, if not, copy will fail which is correct for TDD RED)
if [ -f "$ROOT/scripts/git-pre-commit" ]; then
  cp "$ROOT/scripts/git-pre-commit" scripts/
fi
# Replicate run-all-checks.sh
mkdir -p scripts
cp "$ROOT/scripts/run-all-checks.sh" scripts/

# Prepare simulated user input for setup-leap.sh:
# Answer 'n' to Claude, 'n' to Gemini, 'n' to Copilot, 'n' to Cursor, 'n' to skills, 'n' to gitignore, 'y' to pre-commit hook, 'n' to QMD.
echo "Running setup-leap.sh inside temp repository..."
set +e
bash scripts/setup-leap.sh << 'EOF'
n
n
n
n
n
n
y
n
EOF
SETUP_CODE=$?
set -e

# Assertions
assert_exists "pre-commit hook file" ".git/hooks/pre-commit"

if [ -f ".git/hooks/pre-commit" ]; then
  # Verify it is executable
  [ -x ".git/hooks/pre-commit" ] && IS_EXEC="true" || IS_EXEC="false"
  assert_true "pre-commit hook is executable" "$IS_EXEC"

  # Test Hook Execution - Scenario A: run-all-checks succeeds
  echo "Testing Hook Scenario A: run-all-checks succeeds"
  # Mock run-all-checks.sh to always succeed
  echo -e '#!/bin/sh\nexit 0' > scripts/run-all-checks.sh
  chmod +x scripts/run-all-checks.sh
  
  set +e
  bash .git/hooks/pre-commit 2>&1
  HOOK_CODE_PASS=$?
  set -e
  [ "$HOOK_CODE_PASS" -eq 0 ] && HOOK_PASSES="true" || HOOK_PASSES="false"
  assert_true "Hook permits commit when checks pass" "$HOOK_PASSES"

  # Test Hook Execution - Scenario B: run-all-checks fails
  echo "Testing Hook Scenario B: run-all-checks fails"
  # Mock run-all-checks.sh to always fail
  echo -e '#!/bin/sh\nexit 1' > scripts/run-all-checks.sh
  chmod +x scripts/run-all-checks.sh
  
  set +e
  bash .git/hooks/pre-commit 2>&1
  HOOK_CODE_FAIL=$?
  set -e
  [ "$HOOK_CODE_FAIL" -ne 0 ] && HOOK_FAILS="true" || HOOK_FAILS="false"
  assert_true "Hook blocks commit when checks fail" "$HOOK_FAILS"
fi

echo ""
echo "Test summary: PASS=$PASS FAIL=$FAIL"

if [ "$FAIL" -gt 0 ]; then
  exit 1
else
  exit 0
fi
