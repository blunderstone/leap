# Setup and QMD Configuration Fixes Implementation Plan

**Author:** [F. Andy Seidl](https://github.com/faseidl)<br>
**Date:** 2026-08-28

---

## Overview

This implementation plan covers updating `setup-leap.sh` to pass the `--remove-legacy` flag to `qmd-config` and updating `qmd-config` to write an idempotent, workstation-safe generic description to the workstation-global `/` context slot instead of a project-specific one.

**Development Approach:** Use Test-Driven Development (TDD) where applicable, making surgical edits and validating the changes with mock-based verification and the existing test suites.

### Overall Assessment

- **Complexity:** LOW - The changes are scoped to bash scripting edits in setup and configuration files.
- **Risk:** LOW - The `--remove-legacy` flag is already implemented and proven safe in `qmd-config`. Writing generic text to `/` prevents inter-project metadata collision and is fully compatible.

---

## Phase 1: Implementation & Local Verification

### Goals

- **Goal 1:** Update `scripts/setup-leap.sh` to call `qmd-config` with the `--remove-legacy` flag.
- **Goal 2:** Update the warnings/retry instructions printed by `scripts/setup-leap.sh` to include `--remove-legacy`.
- **Goal 3:** Refactor the workstation-global `/` context initialization in `scripts/qmd/qmd-config` to output a generic description of the LEAP document taxonomy conventions rather than project-specific text.
- **Goal 4:** Update the automated test suites to verify that the correct `/` context hint is emitted and that `setup-leap.sh` correctly passes the `--remove-legacy` flag when `--qmd` is selected.

### Approach

1. **Update `setup-leap.sh`:**
   - Modify line 639 to: `bash "$LEAP_DIR/scripts/qmd/qmd-config" --repo-root "$REPO_ROOT" --remove-legacy`
   - Modify line 642 to include `--remove-legacy`.
   - Modify line 653 to include `--remove-legacy`.
2. **Update `qmd-config`:**
   - Locate the `/` context registration on lines 615-617.
   - Replace the project-specific text with the workstation-safe generic LEAP taxonomy description.
3. **Verify via Tests:**
   - Modify `scripts/qmd/tests/qmd-config.test.sh` to assert that the global `/` context is registered with the new generic message structure.
   - Add a test in `scripts/tests/test_setup_flags.sh` that mocks `scripts/qmd/qmd-config` as a spy script and runs `setup-leap.sh --qmd` to verify it is called with `--remove-legacy`.

### Testing

- Run `bash scripts/qmd/tests/qmd-config.test.sh` to verify QMD-specific test coverage and correctness.
- Run `bash scripts/tests/test_setup_flags.sh` to verify setup script execution and flag handling.
- Run the workspace integration suite: `bash scripts/run-all-checks.sh`.

### Success Criteria

- [x] `setup-leap.sh` invokes `qmd-config` with `--remove-legacy`.
- [x] Warning retry advice printed by `setup-leap.sh` includes `--remove-legacy`.
- [x] `qmd-config` writes a generic description to `/`.
- [x] New behavioral test in `test_setup_flags.sh` asserts that `--remove-legacy` is correctly passed.
- [x] Existing test suites and the overall check-runner pass with 100% success.

### Explicitly Deferred

- None.

**Rationale:** Combining these updates in one phase is optimal as both issues concern setup-time configuration of QMD and have low complexity.
