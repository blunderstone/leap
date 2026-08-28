#!/usr/bin/env bash
# test_assert_lib.sh — Unit tests for the reusable shell assertion library (assert.sh).
#
# Validates that each assertion function correctly manages PASS and FAIL counters
# and produces standard output formatting under passing and failing scenarios.
#
# Run: bash scripts/tests/test_assert_lib.sh
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
LIB_ASSERT="$HERE/../lib/assert.sh"

# Sourcing the library under test (expected to fail in TDD RED phase as lib doesn't exist yet)
if [ ! -f "$LIB_ASSERT" ]; then
  echo "Assertion library scripts/lib/assert.sh is missing (expected for TDD RED Phase)."
  exit 1
fi

source "$LIB_ASSERT"

# Setup local PASS/FAIL counters to track our unit test progress
UNIT_PASS=0
UNIT_FAIL=0

# Temporary file to capture assertion output without using subshells
TEMP_OUT=$(mktemp)
trap 'rm -f "$TEMP_OUT"' EXIT

# Helper to execute an assertion in the main shell environment, capturing stdout/stderr
run_test_assertion() {
  : > "$TEMP_OUT"
  "$@" > "$TEMP_OUT" 2>&1
}

# Helper to assert unit test outcomes
unit_assert() {
  local label="$1"
  local condition="$2"
  if eval "$condition"; then
    UNIT_PASS=$((UNIT_PASS+1))
    echo "  ok   $label"
  else
    UNIT_FAIL=$((UNIT_FAIL+1))
    echo "  FAIL $label"
  fi
}

echo "Running unit tests for scripts/lib/assert.sh..."

# -----------------------------------------------------------------------------
# 1. Test assert_equals
# -----------------------------------------------------------------------------
echo "Testing assert_equals..."
PASS=0; FAIL=0
# Passing case
run_test_assertion assert_equals "equal strings" "hello" "hello"
unit_assert "assert_equals passing increments PASS" '[ "$PASS" -eq 1 ]'
unit_assert "assert_equals passing keeps FAIL at 0" '[ "$FAIL" -eq 0 ]'
unit_assert "assert_equals passing prints ok message" 'grep -q "ok   equal strings" "$TEMP_OUT"'

# Failing case
PASS=0; FAIL=0
run_test_assertion assert_equals "different strings" "hello" "world"
unit_assert "assert_equals failing keeps PASS at 0" '[ "$PASS" -eq 0 ]'
unit_assert "assert_equals failing increments FAIL" '[ "$FAIL" -eq 1 ]'
unit_assert "assert_equals failing prints FAIL message" 'grep -q "FAIL different strings" "$TEMP_OUT"'

# -----------------------------------------------------------------------------
# 2. Test assert_true
# -----------------------------------------------------------------------------
echo "Testing assert_true..."
PASS=0; FAIL=0
# Passing case
run_test_assertion assert_true "is true" "true"
unit_assert "assert_true passing increments PASS" '[ "$PASS" -eq 1 ]'
unit_assert "assert_true passing keeps FAIL at 0" '[ "$FAIL" -eq 0 ]'

# Failing case
PASS=0; FAIL=0
run_test_assertion assert_true "is not true" "false"
unit_assert "assert_true failing keeps PASS at 0" '[ "$PASS" -eq 0 ]'
unit_assert "assert_true failing increments FAIL" '[ "$FAIL" -eq 1 ]'

# -----------------------------------------------------------------------------
# 3. Test assert_exit_code
# -----------------------------------------------------------------------------
echo "Testing assert_exit_code..."
PASS=0; FAIL=0
# Passing case
run_test_assertion assert_exit_code "exit 0" 0 0
unit_assert "assert_exit_code passing increments PASS" '[ "$PASS" -eq 1 ]'
unit_assert "assert_exit_code passing keeps FAIL at 0" '[ "$FAIL" -eq 0 ]'

# Failing case with output dump
PASS=0; FAIL=0
run_test_assertion assert_exit_code "exit mismatch" 0 1 "some output log"
unit_assert "assert_exit_code failing keeps PASS at 0" '[ "$PASS" -eq 0 ]'
unit_assert "assert_exit_code failing increments FAIL" '[ "$FAIL" -eq 1 ]'
unit_assert "assert_exit_code failing prints failure details" 'grep -q "expected exit code 0" "$TEMP_OUT"'
unit_assert "assert_exit_code failing dumps output" 'grep -q "some output log" "$TEMP_OUT"'

# -----------------------------------------------------------------------------
# 4. Test assert_exists
# -----------------------------------------------------------------------------
echo "Testing assert_exists..."
PASS=0; FAIL=0
TEMP_FILE=$(mktemp)
# Passing case
run_test_assertion assert_exists "file exists" "$TEMP_FILE"
unit_assert "assert_exists passing increments PASS" '[ "$PASS" -eq 1 ]'
unit_assert "assert_exists passing keeps FAIL at 0" '[ "$FAIL" -eq 0 ]'

# Failing case
PASS=0; FAIL=0
run_test_assertion assert_exists "missing file" "/nonexistent/path/file"
unit_assert "assert_exists failing keeps PASS at 0" '[ "$PASS" -eq 0 ]'
unit_assert "assert_exists failing increments FAIL" '[ "$FAIL" -eq 1 ]'
rm -f "$TEMP_FILE"

# -----------------------------------------------------------------------------
# 5. Test assert_absent
# -----------------------------------------------------------------------------
echo "Testing assert_absent..."
PASS=0; FAIL=0
# Passing case
run_test_assertion assert_absent "file absent" "/nonexistent/path/file"
unit_assert "assert_absent passing increments PASS" '[ "$PASS" -eq 1 ]'
unit_assert "assert_absent passing keeps FAIL at 0" '[ "$FAIL" -eq 0 ]'

# Failing case
PASS=0; FAIL=0
TEMP_FILE=$(mktemp)
run_test_assertion assert_absent "existing file is absent" "$TEMP_FILE"
unit_assert "assert_absent failing keeps PASS at 0" '[ "$PASS" -eq 0 ]'
unit_assert "assert_absent failing increments FAIL" '[ "$FAIL" -eq 1 ]'
rm -f "$TEMP_FILE"

# -----------------------------------------------------------------------------
# 6. Test assert_contains
# -----------------------------------------------------------------------------
echo "Testing assert_contains..."
PASS=0; FAIL=0
# Passing case
run_test_assertion assert_contains "contains word" "the quick brown fox" "brown"
unit_assert "assert_contains passing increments PASS" '[ "$PASS" -eq 1 ]'
unit_assert "assert_contains passing keeps FAIL at 0" '[ "$FAIL" -eq 0 ]'

# Failing case
PASS=0; FAIL=0
run_test_assertion assert_contains "contains word fail" "the quick brown fox" "lazy"
unit_assert "assert_contains failing keeps PASS at 0" '[ "$PASS" -eq 0 ]'
unit_assert "assert_contains failing increments FAIL" '[ "$FAIL" -eq 1 ]'
unit_assert "assert_contains failing prints expected needle" 'grep -q "expected to find: lazy" "$TEMP_OUT"'

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------
echo ""
echo "Assertion library unit tests summary: PASS=$UNIT_PASS FAIL=$UNIT_FAIL"
if [ "$UNIT_FAIL" -gt 0 ]; then
  exit 1
else
  exit 0
fi
