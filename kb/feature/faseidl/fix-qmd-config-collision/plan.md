# Fix QMD-Config Collision Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-28

---

## Overview

We will fix the issue where `qmd-config` incorrectly reports success (e.g., as an idempotent skip) when a collection registration fails due to a path/pattern collision with a different collection name. This occurs because the registration script uses a loose check for `"already exists"` in the stderr of `qmd collection add`, which matches the collision error message even though the desired collection was not created.

Our approach will employ Test-Driven Development (TDD):

1. Write a failing test in the test suite (`scripts/qmd/tests/qmd-config.test.sh`) that simulates a path/pattern collision when registering a collection (TDD RED).
2. Fix the detection in `emit_collection` to check for specific, name-matched success/skip patterns (TDD GREEN).
3. Add a verification guard to `emit_context` to verify the collection exists before adding context (TDD GREEN).
4. Run the test suite and verify that the tests pass.

**Development Approach:** Use Test-Driven Development (TDD) throughout - write tests before implementation code, following the Red-Green-Refactor cycle.

### Overall Assessment

- **Complexity:** LOW - This is a straightforward change to standard bash scripting.
- **Risk:** LOW - No external systems or major structural changes are involved.

---

## Phase 1: Reproduce via Tests (TDD RED)

### Goals

- Create a test case in `scripts/qmd/tests/qmd-config.test.sh` that mocks or replicates the `qmd collection add` output during a path/pattern collision.
- Confirm the new test fails correctly under the current implementation (RED state).

### Approach

- Examine how `qmd-config.test.sh` isolates tests and runs the script.
- Since `qmd-config` is run with `--dry-run` in current tests, it never actually invokes `qmd collection add`. However, we want to test the runtime behavior of the real script when invoking `qmd`.
- To test the real bash functions or simulate the environment without actually invoking a real global database or needing a complex environment, we can either:
  1. Add a mocked helper/subcommand for `qmd`, or mock `qmd` function/executable on the `PATH` during testing to output the collision/already exists messages.
  2. Implement a dedicated test case that runs a mocked `qmd` executable in a fake bin folder added to `PATH`. This is an extremely standard and safe way to mock external commands in Bash!
- Let's design a mock `qmd` executable for the test. When called as `qmd collection add`, we can make it output the specific "A collection already exists for this path and pattern" error and exit with code 1.
- We will verify that running `qmd-config` in this state (without `--dry-run`) reports a registration failure and exits with code 1 rather than claiming success.

### Testing

- Run `bash scripts/qmd/tests/qmd-config.test.sh` to see the new test fail (RED).

### Success Criteria

- [x] A new test case is added to `scripts/qmd/tests/qmd-config.test.sh` targeting path/pattern collision behavior.
- [x] The test case successfully triggers the bug where `qmd-config` incorrectly reports success/skip on collision.
- [x] The test fails on the current implementation (TDD RED verified).

### Explicitly Deferred

- None.

**Rationale:** Reproducing the bug with an automated test ensures we understand the exact failure mode and prevents regressions.

---

## Phase 2: Fix Registration and Context Validation (TDD GREEN & REFACTOR)

### Goals

- Resolve the registration false-positive by distinguishing name-specific idempotent skip from generic path/pattern collisions.
- Fail explicitly with exit code 1 when a path/pattern collision with a different collection name is detected and print a helpful `--remove-legacy` suggestion.
- Prevent downstream context registration crashes by validating that the target collection exists.
- Run tests and confirm all tests pass (GREEN).

### Approach

- Update `emit_collection` in `scripts/qmd/qmd-config` to check if `err_out` matches `Collection '<name>' already exists.` specifically instead of the broad `already exists`.
- If a path/pattern collision is detected, output an explicit error message and suggest running with `--remove-legacy`.
- Update `emit_context` in `scripts/qmd/qmd-config` to parse the collection name from the URI (if it starts with `qmd://`) and run `qmd collection show <collection>` to verify its existence before running `qmd context add`.
- If the collection does not exist, warn and skip cleanly instead of allowing `qmd context add` to fail and crash.

### Testing

- Run `bash scripts/qmd/tests/qmd-config.test.sh` to confirm all tests (including the new test case) pass.
- Verify that `check-md` passes on all modified markdown files.

### Success Criteria

- [x] `emit_collection` correctly distinguishes idempotent skip from path/pattern collisions.
- [x] `emit_collection` suggests running with `--remove-legacy` on path/pattern collision.
- [x] `emit_context` safely guards against registering context for non-existent collections.
- [x] All automated tests pass successfully (TDD GREEN verified).
- [x] Workspace remains clean and linter (`check-md`) passes.

### Explicitly Deferred

- None.

### Rationale

This completes the required fixes outlined in Issue #46 in an elegant, backward-compatible, and well-tested manner.

---

## Decision Points

### After Phase 1

- Proceed to Phase 2 once the test successfully fails in the expected RED state.

### After Phase 2

- Finish and prepare the PR once all tests pass green and linters are clean.
