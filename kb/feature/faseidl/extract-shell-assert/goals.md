# Extract Shell Assert Library Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-28

---

## Quick Summary

Consolidate duplicated shell assertion helpers across LEAP test suites into a reusable, POSIX-friendly, and fully-documented shared library.

## Executive Summary

Currently, several shell test suites (such as `pin-leap.test.sh`, `qmd-config.test.sh`, `test_pre_commit_installation.sh`, and `test_run_all_checks.sh`) implement their own standalone versions of basic assertion utilities. This duplication increases the maintenance overhead, leads to slight behavior inconsistencies, and complicates writing new shell tests.

By extracting these assertions into a single reusable library (`scripts/lib/assert.sh`), we will simplify existing test suites, guarantee consistent failure reporting, and make a high-quality, reusable assertion framework directly available to parent repositories that consume LEAP as a submodule.

## Objectives

1. Create a POSIX-friendly shell assertion library `scripts/lib/assert.sh`.
2. Refactor existing test suites to import and use the new library.
3. Establish robust documentation for internal and external consumers of the assertion library, explicitly detailing how parent repositories can consume it.
4. Verify all existing tests run and pass without regressions.

## Requirements

### Functional Requirements

- **REQ-1:** Provide a unified shell assertion library at `scripts/lib/assert.sh`.
- **REQ-2:** Support the following assertion functions:
  - `assert_equals`
  - `assert_true`
  - `assert_exit_code`
  - `assert_exists`
  - `assert_absent`
  - `assert_contains`
- **REQ-3:** Support dynamic pass/fail counters (`PASS` and `FAIL`) that integrate seamlessly into existing test runners.
- **REQ-4:** Standardize error/output messaging when assertions fail, including contextual dumps (like command output) for diagnostics.

### Non-Functional Requirements

- **Compatibility:** Must be compatible with macOS standard shell (Bash 3.2+) and modern POSIX shells.
- **Maintainability:** Pure shell implementation, clean of external dependencies (e.g., no Node.js/Python required during assertions).
- **Usability:** Simple argument orders with clear error explanations for assertion failures.

### Testing Requirements

- The extracted library must be verified by refactoring the following test suites, ensuring they pass completely:
  - `scripts/tests/pin-leap.test.sh`
  - `scripts/qmd/tests/qmd-config.test.sh`
  - `scripts/tests/test_pre_commit_installation.sh`
  - `scripts/tests/test_run_all_checks.sh`
- A dedicated test suite for `scripts/lib/assert.sh` itself should be created or integrated to guarantee individual assertion functions behave as expected (e.g., matching exact output formatting and return codes).

### Documentation Requirements

- Full API documentation for all public functions in `scripts/lib/assert.sh`.
- A dedicated usage guide (e.g. within a README or guide document) explaining argument order, variable assumptions (`PASS`/`FAIL`), and stability guarantees.

## Success Criteria

- [ ] Reusable assertion library `scripts/lib/assert.sh` implemented with all required assertion functions.
- [ ] All four existing test suites refactored and executing successfully.
- [ ] New test cases created to verify correctness of assertion functions under both passing and failing conditions.
- [ ] Library API and usage documented clearly for internal and external developers.

## Constraints

- Must maintain compatibility with macOS default Bash 3.2.
- The assertion library must not force the exit of the calling script upon a single assertion failure; it should increment `FAIL` and let the test runner decide when to exit (consistent with the current test behavior).

## Assumptions

- Test suites using the library will initialize the `PASS` and `FAIL` variables prior to invoking assertion helper functions.
- The output format can be slightly refined to be uniform across all tests while keeping existing output semantics intact.

## Out of Scope

- Refactoring non-shell test suites (e.g., Python pytest or unit tests).
