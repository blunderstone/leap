#!/usr/bin/env bash
# test_run_all_checks.sh — Behavioral verification for run-all-checks.sh script.
#
# Validates that scripts/run-all-checks.sh successfully aggregates check-md,
# python pytest, python unittests, and shell script tests, exiting with 0 on
# success, and immediately with 1 on any subcommand failure.
#
# Run: bash scripts/tests/test_run_all_checks.sh (expects PASS=5 FAIL=0)
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
SCRIPT="$HERE/../run-all-checks.sh"

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

# ---- verification scenarios --------------------------------------------------

echo "Running TDD verification for run-all-checks.sh..."

if [ ! -f "$SCRIPT" ]; then
  echo "Target script scripts/run-all-checks.sh is missing (expected for TDD RED Phase)."
  FAIL=$((FAIL+1))
  printf "  FAIL target script exists\n"
else
  # Scenario 1: All checks pass
  echo "Scenario 1: All checks pass"
  set +e
  out=$(CHECK_MD="true" PYTEST="true" INSTALL_SKILLS_TEST="true" QMD_TEST="true" bash "$SCRIPT" 2>&1)
  code=$?
  set -e
  assert_exit_code "All checks pass exits with 0" 0 "$code" "$out"

  # Scenario 2: check-md fails
  echo "Scenario 2: check-md fails"
  set +e
  out=$(CHECK_MD="false" PYTEST="true" INSTALL_SKILLS_TEST="true" QMD_TEST="true" bash "$SCRIPT" 2>&1)
  code=$?
  set -e
  assert_exit_code "Failing check-md exits with 1" 1 "$code" "$out"

  # Scenario 3: pytest fails
  echo "Scenario 3: pytest fails"
  set +e
  out=$(CHECK_MD="true" PYTEST="false" INSTALL_SKILLS_TEST="true" QMD_TEST="true" bash "$SCRIPT" 2>&1)
  code=$?
  set -e
  assert_exit_code "Failing pytest exits with 1" 1 "$code" "$out"

  # Scenario 4: install-skills tests fail
  echo "Scenario 4: install-skills tests fail"
  set +e
  out=$(CHECK_MD="true" PYTEST="true" INSTALL_SKILLS_TEST="false" QMD_TEST="true" bash "$SCRIPT" 2>&1)
  code=$?
  set -e
  assert_exit_code "Failing install-skills tests exits with 1" 1 "$code" "$out"

  # Scenario 5: QMD config tests fail
  echo "Scenario 5: QMD config tests fail"
  set +e
  out=$(CHECK_MD="true" PYTEST="true" INSTALL_SKILLS_TEST="true" QMD_TEST="false" bash "$SCRIPT" 2>&1)
  code=$?
  set -e
  assert_exit_code "Failing QMD config tests exits with 1" 1 "$code" "$out"
fi

# ---- report summary ---------------------------------------------------------
echo ""
echo "Test summary: PASS=$PASS FAIL=$FAIL"

if [ "$FAIL" -gt 0 ]; then
  exit 1
else
  exit 0
fi
