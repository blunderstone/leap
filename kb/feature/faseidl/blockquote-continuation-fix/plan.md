# Rule 2 Block Separation Blockquote Continuation Fix Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-23

---

## Overview

This implementation plan outlines the steps required to resolve GitHub Issue #12 in the `check-md` linter. The plan is divided into two distinct, sequential phases following disciplined Test-Driven Development (TDD) practices: a Red phase (test authoring and verification of baseline failure) and a Green/Refactor phase (implementation and validation).

**Development Approach:** Use Test-Driven Development (TDD) throughout - write tests before implementation code, following the Red-Green-Refactor cycle.

### Overall Assessment

- **Complexity:** LOW - The bug is well-diagnosed and has a localized fix in `src/check_md/rules.py` and accompanying unit tests in `tests/test_rule2_block_separation.py`.
- **Risk:** LOW - Although the fixer can modify files, the localized nature of the fix and our extensive round-trip unit test assertions minimize risk.

---

## Phase 1: Test Case Authoring and Regression Verification (RED Phase)

### Goals

- Author comprehensive test cases that precisely reproduce the reported defect in both linter checking and fixer modes.
- Verify that the tests run and fail appropriately (establishing the TDD RED baseline) before making any code modifications.
- Commit the failing tests as a baseline.

### Approach

- Update `check-md/tests/test_rule2_block_separation.py` to add new test cases:
  - **Multi-line Block Quote checking:** A multi-line block quote preceded by a paragraph should report exactly one violation, on its first line (not on continuation lines).
  - **Paragraph-Break checking:** A block quote containing a bare `>` paragraph break should report exactly one violation, on its first line (not on the bare `>` or subsequent lines).
  - **Correct separation checking:** A multi-line block quote at the start of a document, or after a blank line, should report zero violations.
  - **Fixer round-trip verification:** A fixer test case verifying that running the linter's `--fix` on a valid multi-line block quote (and a block quote with a bare `>` paragraph break) leaves the input completely unchanged.
- Execute the test suite using pytest to observe the expected assertion failures.

### Testing

- Execute tests: Run the `pytest` runner specifically targeting `test_rule2_block_separation.py`.
- Check for expected RED failures (violations reported on continuation lines, and fixer incorrectly introducing blank lines).

### Success Criteria

- [x] New test cases compile and run successfully.
- [x] Pytest suite fails on blockquote continuation line assertions as expected (TDD RED).
- [x] Baseline test state is committed to git.

**Rationale:** Writing tests first ensures we have a precise, executable requirement specification for what constitutes "correct" behavior, completely eliminating guessing and preventing regressions.

---

## Phase 2: Bug Fix Implementation and Linter Validation (GREEN & REFACTOR Phases)

### Goals

- Define a robust pattern for identifying block quote continuation lines.
- Update `Rule2BlockSeparation.check_line` to use this continuation pattern to skip false-positive checks on block quote continuation lines.
- Verify all unit and round-trip tests pass cleanly.
- Run `check-md` over the workspace to ensure no regressions are introduced and that the linter runs successfully.

### Approach

- Modify `check-md/src/check_md/rules.py`:
  - Define `BLOCKQUOTE_CONTINUATION_PATTERN = re.compile(r"^\s*>")` to correctly match standard and bare blockquote continuation lines.
  - In `Rule2BlockSeparation.check_line`, inside the `BLOCKQUOTE_PATTERN` branch, add a continuation guard:
    ```python
    elif self.BLOCKQUOTE_PATTERN.match(line):
        # Only flag first line of block quote
        if not self.BLOCKQUOTE_CONTINUATION_PATTERN.match(prev):
            violations.append(self._create_violation(context, "block quote"))
    ```
- Run pytest to ensure all test cases (both existing and new) now pass cleanly (TDD GREEN).
- Refactor and clean up code if necessary, ensuring no regressions.
- Verify workspace compliance by running `check-md kb/` over the repository knowledge base.

### Testing

- Run the full pytest test suite to ensure 100% test success across all rules.
- Validate workspace integrity using `check-md kb/` to ensure no unforeseen file conflicts or regressions exist.

### Success Criteria

- [ ] Linter continuation guard is implemented.
- [ ] Pytest test suite runs and passes cleanly with 100% success.
- [ ] Workspace linter check (`check-md kb/`) passes with zero violations.

**Rationale:** The proposed continuation guard directly targets the root cause of the bug by mirroring the existing, proven guards for lists and tables.

---

## Decision Points

### After Phase 1

- Proceed to Phase 2 only if the new tests fail *only* on the expected assertions (block quote continuation lines and fixer corruption) and the baseline is committed.

### After Phase 2

- Feature is ready for final human verification and checkbox checkoff once all tests are passing and the workspace linter runs cleanly.
