#!/usr/bin/env bash
# pin-leap.test.sh — Behavioral verification for LEAP submodule pinning utility.
#
# Validates that scripts/pin-leap.sh correctly enforces safeguards, processes inputs,
# and performs safe git operations in a simulated repository sandbox.
#
# Run: bash scripts/tests/pin-leap.test.sh
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
PIN_SCRIPT="$ROOT/scripts/pin-leap.sh"

PASS=0
FAIL=0

# ---- assertion helpers ------------------------------------------------------

assert_exit_code() { # label expected_code actual_code [output]
  local label="$1"
  local expected="$2"
  local actual="$3"
  local output="${4:-}"
  
  if [ "$actual" -eq "$expected" ]; then
    PASS=$((PASS+1))
    printf "  ok   %s (exit %d)\n" "$label" "$actual"
  else
    FAIL=$((FAIL+1))
    printf "  FAIL %s\n       expected exit code %d, but got %d\n" "$label" "$expected" "$actual"
    if [ -n "$output" ]; then
      printf '       ---- output ----\n%s\n       ----------------\n' "$output"
    fi
  fi
}

assert_exists() {
  local label="$1"
  local path="$2"
  if [ -f "$path" ] || [ -d "$path" ]; then
    PASS=$((PASS+1))
    printf "  ok   %s exists\n" "$label"
  else
    FAIL=$((FAIL+1))
    printf "  FAIL %s does not exist: %s\n" "$label" "$path"
  fi
}

assert_equals() {
  local label="$1"
  local expected="$2"
  local actual="$3"
  if [ "$actual" = "$expected" ]; then
    PASS=$((PASS+1))
    printf "  ok   %s matches expected: '%s'\n" "$label" "$expected"
  else
    FAIL=$((FAIL+1))
    printf "  FAIL %s\n       expected: '%s'\n       got:      '%s'\n" "$label" "$expected" "$actual"
  fi
}

assert_true() {
  local label="$1"
  local val="$2"
  if [ "$val" = "true" ]; then
    PASS=$((PASS+1))
    printf "  ok   %s\n" "$label"
  else
    FAIL=$((FAIL+1))
    printf "  FAIL %s\n" "$label"
  fi
}

# ---- main test runner --------------------------------------------------------

echo "Running TDD verification for pin-leap.sh..."

if [ ! -f "$PIN_SCRIPT" ]; then
  echo "Target script scripts/pin-leap.sh is missing (expected for TDD RED Phase)."
  FAIL=$((FAIL+1))
  printf "  FAIL target script exists\n"
  exit 1
fi

# Create a temporary sandbox directory for simulation
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Created temp workspace at $TEMP_DIR"

# Scenario 1: Run in non-git directory
echo "Scenario 1: Non-git directory validation"
cd "$TEMP_DIR"
set +e
out=$(bash "$PIN_SCRIPT" v1.0.0 2>&1)
code=$?
set -e
assert_exit_code "Fails outside of git repository" 1 "$code" "$out"

# Scenario 2: Run in git repository with no submodules
echo "Scenario 2: Git repository with no submodules"
git init -q
git config user.name "Test User"
git config user.email "test@example.com"
set +e
out=$(bash "$PIN_SCRIPT" v1.0.0 2>&1)
code=$?
set -e
assert_exit_code "Fails when run from repo without LEAP submodule" 1 "$code" "$out"

# Scenario 3: Run in git repository with LEAP submodule but dirty working tree
echo "Scenario 3: Dirty working tree safeguard"
# Create mock LEAP submodule directory and scripts path to simulate correct placement
mkdir -p leap/scripts
cp "$PIN_SCRIPT" leap/scripts/

# Create a dummy file in parent repo (dirty tree)
echo "dirty state" > dirty.txt

set +e
out=$(bash leap/scripts/pin-leap.sh v1.0.0 2>&1)
code=$?
set -e
assert_exit_code "Fails when working tree has unstaged changes" 1 "$code" "$out"

# Cleanup dirty file
rm dirty.txt

# Scenario 4: Clean working tree but missing from .gitmodules
echo "Scenario 4: Missing .gitmodules registration safeguard"
set +e
out=$(bash leap/scripts/pin-leap.sh v1.0.0 2>&1)
code=$?
set -e
assert_exit_code "Fails when submodule directory is not registered in .gitmodules" 1 "$code" "$out"

# Setup real mock remote repository for testing checkout and branch creation
echo "Setting up mock remote and parent repository with registered submodule..."

# 1. Create mock remote repository for LEAP submodule
MOCK_REMOTE="$TEMP_DIR/mock-remote-submodule"
mkdir -p "$MOCK_REMOTE"
cd "$MOCK_REMOTE"
git init -q
git config user.name "Test User"
git config user.email "test@example.com"
echo "submodule v1.0.0 text" > content.txt
git add content.txt
git commit -q -m "initial submodule commit"
git tag v1.0.0
v1_0_0_commit=$(git rev-parse HEAD)

echo "submodule v1.1.0-beta.0 text" > content.txt
git commit -q -a -m "second submodule commit"
git tag v1.1.0-beta.0

echo "submodule v1.1.0 text" > content.txt
git commit -q -a -m "third submodule commit"
git tag v1.1.0
v1_1_0_commit=$(git rev-parse HEAD)

# 2. Setup mock parent repository
PARENT_REPO="$TEMP_DIR/parent-repo"
mkdir -p "$PARENT_REPO"
cd "$PARENT_REPO"
git init -q
git config user.name "Test User"
git config user.email "test@example.com"
git config protocol.file.allow always # Allow file protocol for submodules in this test repo
# Need at least one commit in the parent repository to be able to checkout branches
echo "parent repo initial content" > readme.md
git add readme.md
git commit -q -m "initial parent commit"

# 3. Add submodule and register in .gitmodules
git -c protocol.file.allow=always submodule add "$MOCK_REMOTE" leap
git commit -q -m "Add LEAP submodule"

# Copy our pin-leap.sh script into the registered submodule scripts directory
mkdir -p leap/scripts
cp "$PIN_SCRIPT" leap/scripts/
chmod +x leap/scripts/pin-leap.sh

# Scenario 5: Success flow pinning to a specific tag (v1.0.0)
echo "Scenario 5: Successful pin to specific tag (v1.0.0)"
# Run the script to pin to v1.0.0
set +e
out=$(bash leap/scripts/pin-leap.sh v1.0.0 2>&1)
code=$?
set -e
assert_exit_code "Execution succeeds" 0 "$code" "$out"

# Verifications for Scenario 5:
# - Active parent branch is chore/pin-leap-v1.0.0
current_parent_branch=$(git branch --show-current)
assert_equals "Parent branch updated" "chore/pin-leap-v1.0.0" "$current_parent_branch"

# - Submodule head matches v1.0.0 commit
current_submodule_commit=$(cd leap && git rev-parse HEAD)
assert_equals "Submodule checked out at v1.0.0" "$v1_0_0_commit" "$current_submodule_commit"

# - LEAP Level 1 compliance folder and files exist
assert_exists "goals.md" "kb/feature/pin-leap-v1.0.0/goals.md"
assert_exists "completion-summary.md" "kb/feature/pin-leap-v1.0.0/completion-summary.md"

# - Submodule reference and files are staged
staged_status=$(git status --porcelain)
echo "DEBUG STAGED STATUS SCENARIO 5:"
echo "$staged_status"
echo "------------------------------"

assert_true "Submodule pointer change is staged" "$(echo "$staged_status" | grep -q "^M. leap" && echo "true" || echo "false")"
assert_true "Level 1 compliance folder is staged" "$(echo "$staged_status" | grep -q "^A  kb/feature/pin-leap-v1.0.0/" && echo "true" || echo "false")"

# Reset parent repo to main branch and clean working tree for next scenario
git checkout -q main
git branch -D chore/pin-leap-v1.0.0 || true
git reset --hard -q HEAD

# Reset submodule to v1.0.0 initially so that running "latest" resolves to v1.1.0 and modifies the pointer
(cd leap && git checkout -q v1.0.0)
git add leap
git commit -q -m "Reset submodule to v1.0.0 for Scenario 6"
git -c protocol.file.allow=always submodule update --init --recursive -q

# Scenario 6: Success flow with "latest" resolution
echo "Scenario 6: Successful pin with 'latest' keyword resolution"
set +e
out=$(bash leap/scripts/pin-leap.sh latest 2>&1)
code=$?
set -e
assert_exit_code "Execution succeeds with 'latest'" 0 "$code" "$out"

# Verifications for Scenario 6:
# - Active parent branch is chore/pin-leap-v1.1.0 (latest stable resolved)
current_parent_branch=$(git branch --show-current)
assert_equals "Parent branch updated to latest version" "chore/pin-leap-v1.1.0" "$current_parent_branch"

# - Submodule head matches v1.1.0 commit
current_submodule_commit=$(cd leap && git rev-parse HEAD)
assert_equals "Submodule checked out at latest stable v1.1.0" "$v1_1_0_commit" "$current_submodule_commit"

# - LEAP Level 1 compliance folder and files exist for v1.1.0
assert_exists "goals.md" "kb/feature/pin-leap-v1.1.0/goals.md"
assert_exists "completion-summary.md" "kb/feature/pin-leap-v1.1.0/completion-summary.md"

# - Staged changes check
staged_status=$(git status --porcelain)
echo "DEBUG STAGED STATUS SCENARIO 6:"
echo "$staged_status"
echo "------------------------------"

assert_true "Submodule pointer change is staged" "$(echo "$staged_status" | grep -q "^M. leap" && echo "true" || echo "false")"
assert_true "Level 1 compliance folder is staged" "$(echo "$staged_status" | grep -q "^A  kb/feature/pin-leap-v1.1.0/" && echo "true" || echo "false")"

# Print results
echo ""
echo "Test results: PASS=$PASS FAIL=$FAIL"
if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
