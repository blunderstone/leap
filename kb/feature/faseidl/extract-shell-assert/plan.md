# Extract Shell Assert Library Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-28

---

## Overview

We will implement a reusable shell assertion library at `scripts/lib/assert.sh` and refactor four existing shell test suites to consume it. This will eliminate duplicated assertion functions, unify test failure formatting, and make a standard assertion framework available to parent repositories using LEAP as a submodule.

**Development Approach:** Use Test-Driven Development (TDD) throughout - write unit tests for the assertion library itself to prove its behavior under both success and failure states, and then perform sequential refactoring of existing test suites.

### Overall Assessment

- **Complexity:** LOW - The task involves refactoring shell script helpers into a shared file and updating calling references.
- **Risk:** LOW - All target scripts are test suites; any mistake will fail the test suite run, preventing regressions from leaking to production code.

---

## Phase 1: Core Library & Unit Tests

### Goals

- Implement `scripts/lib/assert.sh` with six core assertions: `assert_equals`, `assert_true`, `assert_exit_code`, `assert_exists`, `assert_absent`, and `assert_contains`.
- Create a dedicated unit test suite for the assertion library (`scripts/tests/test_assert_lib.sh`) to verify correct incrementing of `PASS`/`FAIL` counters and proper formatting under failure conditions.

### Approach

- Create `scripts/lib/assert.sh` ensuring it works under standard macOS Bash 3.2+ as well as standard POSIX shells.
- Code the assertion functions so they dynamically increment calling script's `PASS` and `FAIL` variables.
- Write `scripts/tests/test_assert_lib.sh` using TDD to verify the assertion helpers behave identically to the legacy helper functions and fail/pass correctly.

### Testing

- Verify assertion behavior for:
  - Equals (matching & mismatching strings)
  - True (value = "true" or not)
  - Exit code (matching & mismatching exit codes, including verbose exit-code output logging)
  - Exists (file/directory presence)
  - Absent (file/directory absence)
  - Contains (pattern matching / substring matching)
- Assert that `PASS` increments on success and `FAIL` increments on failure.

### Success Criteria

- [ ] `scripts/lib/assert.sh` successfully created with all functions implemented.
- [ ] Dedicated unit test suite `scripts/tests/test_assert_lib.sh` implemented and passing.
- [ ] API is documented via standardized shell header comments.

---

## Phase 2: Refactor Existing Test Suites & run-all-checks

### Goals

- Replace duplicate assertion definitions with sourcing of `scripts/lib/assert.sh` in the four targeted test suites:
  - `scripts/tests/pin-leap.test.sh`
  - `scripts/qmd/tests/qmd-config.test.sh`
  - `scripts/tests/test_pre_commit_installation.sh`
  - `scripts/tests/test_run_all_checks.sh`
- Integrate the new assertion library unit tests into `scripts/run-all-checks.sh` so they run automatically during CI/CD.

### Approach

- Sgurgically replace inline assertion functions in each target script with `source "$(dirname "${BASH_SOURCE[0]}")"/../lib/assert.sh` (or appropriate relative path).
- Adjust test execution logic as needed if slight formatting/naming alignments are required.
- Add the new assertion library test suite to `scripts/run-all-checks.sh`.

### Testing

- Execute each refactored test suite individually.
- Execute `scripts/run-all-checks.sh` to run the entire workspace test harness, ensuring all checks pass.

### Success Criteria

- [ ] All four legacy test suites refactored and passing completely.
- [ ] `scripts/run-all-checks.sh` includes the new assertion unit tests.
- [ ] Total workspace tests run and exit cleanly (exit code 0).

---

## Phase 3: Documentation and Handoff

### Goals

- Create a formal usage guide at `kb/guide-shell-assertion-library.md` (aligning with the LEAP document taxonomy) explaining how internal tests and parent repositories using LEAP as a submodule can import and use the assertion library.
- Format all new files with standard licensing and copyright blocks.

### Approach

- Document how a parent repo can source `leap/scripts/lib/assert.sh` from their own shell tests.
- Summarize the library interface (argument orders, return behaviors, PASS/FAIL counter usage).

### Testing

- Run markdown linting checks on the new documentation to verify formatting standards using `check-md`.

### Success Criteria

- [ ] Guide for parent repository and internal consumers written at `kb/guide-shell-assertion-library.md`.
- [ ] Markdown checks pass without errors.
- [ ] Handoff documentation complete.

---

## Decision Points

### After Phase 1

- Proceed if library unit tests pass.
- If macOS Bash 3.2 compatibility issues occur, refine variable and subshell usages.

### After Phase 2

- Proceed if `run-all-checks.sh` passes 100%.

## Notes

- Parent repositories can source the library using:
  `source path/to/leap/scripts/lib/assert.sh`
  which gives them direct access to standard assertions for their own hook and build scripting validation.
