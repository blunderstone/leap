# Extract Shell Assert Library Completion Summary

**Branch:** `faseidl/extract-shell-assert`<br>
**Base Branch:** `main`<br>
**Date:** 2026-08-28<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

---

## Overview

Consolidated all duplicated shell assertion helpers across existing test suites into a robust, POSIX-friendly, and fully documented shared assertion library located at `scripts/lib/assert.sh`. This library provides unified output formatting and consistent failure tracking, and is also made directly available to parent repositories that consume LEAP as a git submodule.

## What Changed

### High-Level Summary

- **Created Reusable Library:** Sourced a unified shell assertion library at `scripts/lib/assert.sh`.
- **Created Unit Test Suite:** Developed a subshell-safe unit test suite at `scripts/tests/test_assert_lib.sh` verifying all assertions under success and failure states.
- **Refactored Existing Test Suites:** Migrated four legacy test suites to import the new library, eliminating 150+ lines of duplicated helper code.
- **Integrated checks:** Integrated the new assertion library unit tests into `scripts/run-all-checks.sh` and updated `scripts/tests/test_run_all_checks.sh` to mock them properly.
- **Created Usage Guide:** Authored a complete, linter-compliant usage guide at `kb/guide-shell-assertion-library.md` following the LEAP document taxonomy.

### Detailed Changes

#### scripts/lib/assert.sh

- Implemented core assertions: `assert_equals`, `assert_true`, `assert_exit_code`, `assert_exists`, `assert_absent`, and `assert_contains`.
- Added dynamic initialization for `PASS` and `FAIL` status counters.
- Added polymorphic behavior in `assert_absent` to support both string absence (3 arguments) and path/file absence (2 arguments).
- Provided an `assert_not_exists` alias to preserve compatibility with existing tests.

#### scripts/tests/test_assert_lib.sh

- Created 29 subshell-safe unit tests verifying proper incrementation of `PASS`/`FAIL` counters and correct console output.

#### Refactored Test Suites

- `scripts/tests/pin-leap.test.sh`: Removed duplicated assertions, sourced `assert.sh` instead.
- `scripts/qmd/tests/qmd-config.test.sh`: Sourced `assert.sh` with a correct relative path and cleaned up duplicate helpers.
- `scripts/tests/test_pre_commit_installation.sh`: Migrated assertions to the library.
- `scripts/tests/test_run_all_checks.sh`: Updated to source the library and added Scenario 7 verifying assertion library failures.

### New Files

- `scripts/lib/assert.sh` - Standardized, POSIX-friendly assertion helpers for shell test suites.
- `scripts/tests/test_assert_lib.sh` - Unit test suite for verifying individual assertion behaviors.
- `kb/guide-shell-assertion-library.md` - Complete usage documentation for contributors and parent repositories.

### Modified Files

- `scripts/run-all-checks.sh` - Added assertion unit tests execution and mocking options.
- `scripts/tests/test_run_all_checks.sh` - Refactored to source library and mock the new `ASSERT_LIB_TEST` check.
- `scripts/tests/test_setup_flags.sh` - Sourced shared library and removed duplicate code.
- `scripts/qmd/tests/qmd-config.test.sh` - Sourced shared library and removed duplicate code.
- `scripts/tests/pin-leap.test.sh` - Sourced shared library and removed duplicate code.
- `scripts/tests/test_pre_commit_installation.sh` - Sourced shared library and removed duplicate code.
- `kb/feature/faseidl/extract-shell-assert/plan.md` - Updated to reflect taxonomic documentation and checked off all success criteria.

## Key Implementation Details

### Dual-Purpose `assert_absent`
The utility `assert_absent` was implemented polymorphically:

1. When passed 3 arguments, it evaluates string/output pattern absence (`assert_absent <label> <haystack> <needle>`).
2. When passed 2 arguments, it evaluates file/directory absence (`assert_absent <label> <path>`), and exposes an alias `assert_not_exists` for backwards compatibility.

### Subshell-Safe Test Design
To test that assertions correctly modify `PASS`/`FAIL` variables inside the parent shell, the unit tests were implemented without using command-substitution subshells `$(...)` for assertions. Instead, standard output is redirected to a temporary file via a parent-shell wrapper, leaving parent-shell environment modifications visible.

---

## Testing

### Test Strategy

- **Unit Testing:** Created a dedicated test script (`scripts/tests/test_assert_lib.sh`) specifically to verify each of the 6 assertion behaviors, including counter updates.
- **Regression Testing:** Ran all legacy shell test suites to verify that sourcing the new library did not alter their correctness or outcomes.
- **Aggregated Testing:** Integrated the assertion library tests into `run-all-checks.sh` and ran the entire workspace verification suite.

### Test Results

- **Total unit tests:** 29 (all passing)
- **Total workspace tests:** 115 test cases across 6 test suites (all passing)
- **New tests added:** 30+ new test cases

---

## Documentation

### Structured API Documentation
The library `scripts/lib/assert.sh` is thoroughly documented with structured, standard shell header blocks describing its interface, input parameters, and behaviors.

### Usage Documentation
Created `kb/guide-shell-assertion-library.md` explaining sourcing conventions, variable expectations, and function signatures with examples, fully matching the LEAP document taxonomy.

---

## Permanent Documentation Assessment

### Documentation Preserved

- Created `kb/guide-shell-assertion-library.md` to permanently document the shell assertions for internal tests and parent repositories.

---

## Breaking Changes

None. All refactorings are 100% backward-compatible and preserve existing assertion interfaces.

## Migration Guide

No manual migration is required for existing internal tests as they have been fully refactored. 

### For Developers

Developers creating new shell tests or working on parent repositories can source `assert.sh`:

```bash
source path/to/leap/scripts/lib/assert.sh
```

---

## Known Limitations

None.

## Future Work

None planned. The library is feature-complete and covers all required assertions.

## Performance Impact

Neutral. Sourcing is extremely lightweight and pure POSIX, carrying no measurable performance overhead.

## Related Issues

- Closes #44: Extract the shell test assertions into a reusable, documented library.

## Verification Steps

1. Checkout the branch: `git checkout faseidl/extract-shell-assert`
2. Run the main check script: `bash scripts/run-all-checks.sh`
3. Verify that the assertion library tests are executed and pass successfully.
