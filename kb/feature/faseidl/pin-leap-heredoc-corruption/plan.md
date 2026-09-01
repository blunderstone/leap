# Fix pin-leap.sh Heredoc Corruption Implementation Plan

**Author:** [faseidl](https://github.com/faseidl)<br>
**Date:** 2026-08-31

---

## Overview

The goal is to fix the Markdown inline code (backtick) corruption bug in `scripts/pin-leap.sh`, dynamically resolve the host default branch, and prevent false-positive success messages. We will strictly follow the Test-Driven Development (TDD) cycle (Red-Green-Refactor) by writing/updating tests first to reproduce the issues (RED phase), then implementing the fixes to make them pass (GREEN phase), and finally checking for any code improvements (REFACTOR phase).

**Development Approach:** Use Test-Driven Development (TDD) throughout - write or update tests before implementation code, following the Red-Green-Refactor cycle.

### Overall Assessment

- **Complexity:** LOW - The fix is local to `scripts/pin-leap.sh` and `scripts/tests/pin-leap.test.sh`.
- **Risk:** LOW - This is a helper script for pinning; any changes will be verified with the existing robust integration test suite.

---

## Phase 1: Test-Driven Development (RED Phase)

### Goals

- Update the integration test runner `scripts/tests/pin-leap.test.sh` to include assertions verifying backtick preservation, dynamic base branch resolution, and status checking.
- Execute the tests and confirm they fail (RED) due to the reported issues in `scripts/pin-leap.sh`.

### Approach

1. Analyze `scripts/tests/pin-leap.test.sh` where Scenario 5 and Scenario 6 verify successful pinning.
2. Add assertions to verify that:
   - Generated `goals.md` and `completion-summary.md` files contain the expected backticks intact (not corrupted or stripped).
   - Generated `completion-summary.md` dynamically shows the default/base branch (e.g. `main` or `master` depending on HEAD) instead of hardcoding `main`.
3. Run the automated tests locally using `bash scripts/tests/pin-leap.test.sh`.
4. Verify that the test run fails (reproducing the bugs described in Issue #60) and outputs RED results.

### Testing

- Run `bash scripts/tests/pin-leap.test.sh` and observe failures specifically targeting backtick removal or hardcoded branch names.

### Success Criteria

- [ ] New assertions added to `scripts/tests/pin-leap.test.sh`.
- [ ] Test run fails with clear, descriptive assertion errors reflecting the bugs in Issue #60 (RED state reached).

---

## Phase 2: Fix Heredoc Corruption and Base Branch (GREEN Phase)

### Goals

- Replace unquoted heredocs (`cat <<EOF`) in `scripts/pin-leap.sh` with a piped quoted heredoc strategy (`cat <<'EOF' | sed ...`) to prevent command execution of markdown backticks while performing safe variable substitution.
- Dynamically detect the parent repository's base branch.
- Wrap file generation commands in status-checking logic to ensure errors trigger failure exits.
- Run tests and confirm they pass successfully (GREEN).

### Approach

1. Refactor the `cat <<EOF` blocks for `goals.md` and `completion-summary.md` in `scripts/pin-leap.sh`.
2. Replace dynamic bash variables inside the heredoc body with `@PLACEHOLDER@` syntax (e.g., `@TARGET_VERSION@`, `@CURRENT_DATE@`, `@SUBMODULE_REL_PATH@`, `@BASE_BRANCH@`).
3. Pipe the quoted heredoc (`cat <<'EOF'`) through `sed` to interpolate the actual values:
   ```bash
   cat <<'EOF' | sed -e "s|@TARGET_VERSION@|${TARGET_VERSION}|g" -e ... > "$COMPLIANCE_DIR/goals.md"
   ```

4. Query the base branch dynamically:
   ```bash
   BASE_BRANCH=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
   BASE_BRANCH=${BASE_BRANCH:-main}
   ```

5. Ensure file generation checks for execution errors: if `cat` or `sed` fails, the script should terminate with an error code instead of printing "Generated goals.md and completion-summary.md ...".
6. Run `bash scripts/tests/pin-leap.test.sh` and confirm all tests now pass (GREEN state reached).

### Success Criteria

- [ ] Unquoted heredocs in `scripts/pin-leap.sh` are refactored to use quoted heredocs piped through `sed`.
- [ ] Base branch is dynamically queried and inserted into `completion-summary.md`.
- [ ] No command execution or evaluation errors occur during document generation.
- [ ] If directory creation or document generation fails, the script fails safely.
- [ ] All automated tests in `scripts/tests/pin-leap.test.sh` pass successfully.

---

## Phase 3: Final Verification & Refactoring (REFACTOR Phase)

### Goals

- Ensure there is no redundant or inefficient logic in the script.
- Verify the entire workspace-wide validation suite passes.

### Approach

1. Review modifications in `scripts/pin-leap.sh` for clean bash coding style and documentation/comments.
2. Run `scripts/run-all-checks.sh` to run the entire project's validation checks (including Python linter `ruff` and Markdown check `check-md` etc.).

### Success Criteria

- [ ] High-quality comments explaining the quoted-heredoc-to-sed pipeline strategy are in place.
- [ ] All project validation checks via `scripts/run-all-checks.sh` run and pass.

---

## Risk Mitigation

### Risk 1: Unescaped character conflicts in `sed`

If a variable (like `TARGET_VERSION` or `SUBMODULE_REL_PATH`) contains special characters like `/`, it could break standard `sed` substitute command delimiter `s/old/new/`.

#### Mitigation

Use `|` as the `sed` delimiter (e.g. `s|@PLACEHOLDER@|${VALUE}|g`), as tag names and relative paths do not contain `|`.

---

## Decision Points

### After Phase 1

- Proceed only once tests fail with descriptive messages representing the reported issues.

### After Phase 2

- Proceed only when all tests pass in GREEN state.
