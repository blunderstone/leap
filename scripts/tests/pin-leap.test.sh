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

# Print results
echo ""
echo "Test results: PASS=$PASS FAIL=$FAIL"
if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
