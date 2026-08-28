#!/usr/bin/env bash
# run-all-checks.sh — Unified workspace check and testing suite runner.
#
# Runs all formatters, linters, and test suites in the workspace,
# exiting with a non-zero code on the first failure.
#
# Supports optional environment overrides for test mocking/isolation:
# - CHECK_MD: linter for markdown files
# - PYTEST: pytest suite for check-md
# - INSTALL_SKILLS_TEST: skills installation tests
# - QMD_TEST: QMD configuration shell tests
# - ASSERT_LIB_TEST: assertion library shell tests
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

# Determine repository root directory
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Helper function to execute a check with mock support
# Usage: run_check <name> <env_override_value> <real_command...>
run_check() {
  local name="$1"
  local override="$2"
  shift 2

  echo "=== Running check: $name ==="

  if [ -n "$override" ]; then
    if [ "$override" = "true" ]; then
      echo "✓ [MOCK] Check '$name' succeeded."
      echo ""
      return 0
    elif [ "$override" = "false" ]; then
      echo "✗ [MOCK] Check '$name' failed." >&2
      echo ""
      return 1
    else
      echo "Unknown mock override value for $name: $override. Running real command."
    fi
  fi

  # Execute the real command
  if "$@"; then
    echo "✓ Check '$name' passed."
    echo ""
    return 0
  else
    echo "✗ Check '$name' failed." >&2
    echo ""
    return 1
  fi
}

# Run the 4 checks
run_check "check-md (Markdown Linter)" "${CHECK_MD:-}" check-md || exit 1

if [ -f "check-md/.venv/bin/pytest" ]; then
  run_check "pytest (Python Linter tests)" "${PYTEST:-}" check-md/.venv/bin/pytest check-md/tests/ || exit 1
else
  run_check "pytest (Python Linter tests)" "${PYTEST:-}" pytest check-md/tests/ || exit 1
fi

run_check "install-skills (Python unit tests)" "${INSTALL_SKILLS_TEST:-}" python3 scripts/tests/test_install_skills.py || exit 1

run_check "setup-leap flags (Shell tests)" "${SETUP_FLAGS_TEST:-}" bash scripts/tests/test_setup_flags.sh || exit 1

run_check "QMD config (Shell tests)" "${QMD_TEST:-}" bash scripts/qmd/tests/qmd-config.test.sh || exit 1

run_check "assert-lib (Assertion library tests)" "${ASSERT_LIB_TEST:-}" bash scripts/tests/test_assert_lib.sh || exit 1

echo "=================================================="
echo "✓ All checks passed successfully!"
echo "=================================================="
exit 0
