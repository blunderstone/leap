#!/usr/bin/env bash
# assert.sh — Reusable, POSIX-friendly assertion library for shell test suites.
#
# Provides standard assertion functions that manage PASS/FAIL counters
# and output standard results in a format friendly to LEAP test runners.
#
# Documentation:
#   Refer to 'kb/guide-shell-assertion-library.md' for API signatures,
#   examples, and instructions for parent repository integration.
#   Please ensure any edits here are kept in sync with that guide.
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

# Initialize PASS and FAIL counters if they are not already defined by the parent test suite.
PASS=${PASS:-0}
FAIL=${FAIL:-0}

# assert_equals <label> <expected> <actual>
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

# assert_true <label> <value>
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

# assert_exit_code <label> <expected_code> <actual_code> [output]
assert_exit_code() {
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

# assert_exists <label> <path>
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

# assert_absent <label> <haystack_or_path> [needle]
# Dual-purpose assertion:
# 1. With 3 arguments: assert_absent <label> <haystack> <needle> (Assert string does NOT contain needle)
# 2. With 2 arguments: assert_absent <label> <path> (Assert file/directory does NOT exist)
assert_absent() {
  if [ "$#" -eq 3 ]; then
    local label="$1"
    local haystack="$2"
    local needle="$3"
    
    if printf '%s\n' "$haystack" | grep -qF -- "$needle"; then
      FAIL=$((FAIL+1))
      printf "  FAIL %s\n       expected NOT to find: %s\n" "$label" "$needle"
      printf '       ---- output ----\n%s\n       ----------------\n' "$haystack"
    else
      PASS=$((PASS+1))
      printf "  ok   %s\n" "$label"
    fi
  else
    local label="$1"
    local path="$2"
    
    if [ ! -e "$path" ]; then
      PASS=$((PASS+1))
      printf "  ok   %s does not exist (as expected): %s\n" "$label" "$path"
    else
      FAIL=$((FAIL+1))
      printf "  FAIL %s exists but should not: %s\n" "$label" "$path"
    fi
  fi
}

# Deprecated/compatibility alias for assert_absent (2 arguments)
assert_not_exists() {
  assert_absent "$@"
}

# assert_contains <label> <haystack> <needle>
assert_contains() {
  local label="$1"
  local haystack="$2"
  local needle="$3"
  
  if printf '%s\n' "$haystack" | grep -qF -- "$needle"; then
    PASS=$((PASS+1))
    printf "  ok   %s\n" "$label"
  else
    FAIL=$((FAIL+1))
    printf "  FAIL %s\n       expected to find: %s\n" "$label" "$needle"
    printf '       ---- output ----\n%s\n       ----------------\n' "$haystack"
  fi
}
