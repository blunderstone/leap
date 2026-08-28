# check-md --version CLI Option Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-28

---

## Overview

We will implement the standard, eager `--version` command-line flag in the `check-md` CLI. The CLI is built using the `typer` library, which provides robust support for eager option callbacks. We will execute this feature in two distinct phases to ensure strict validation, high test coverage, and complete compatibility with existing system scripts.

**Development Approach:** Use Test-Driven Development (TDD) throughout:
1. Write failing integration/CLI tests validating `--version` behavior (RED).
2. Implement the version callback and flag in `cli.py` (GREEN).
3. Refactor and verify (REFACTOR).

### Overall Assessment

- **Complexity:** LOW - Straightforward addition of a Typer CLI option and an associated callback.
- **Risk:** LOW - No disruption to the core markdown parsing, linting, or formatting logic.

---

## Phase 1: Implement `--version` CLI Option and Unit/Integration Tests

### Goals

1. Write automated test cases in `check-md/tests/test_cli.py` that invoke `check-md --version` and assert the output structure and exit code.
2. Implement `version_callback` using Typer's eager callback system to retrieve the version dynamically from `__init__.py` and the absolute directory path using `Path(__file__).parent.resolve()`.
3. Add the `version` option with `is_eager=True` to the `main` entrypoint command in `cli.py`.
4. Ensure all tests in `check-md` run and pass cleanly with 100% success and high coverage (90%+).

### Approach

- **Step 1 (TDD RED):** Edit `check-md/tests/test_cli.py` to add tests for the `--version` option using Typer's `CliRunner`.
- **Step 2 (TDD GREEN):** Define `version_callback(value: bool)` in `check-md/src/check_md/cli.py` and register it on the new `--version` option in `main`.
- **Step 3 (Validation):** Run the `pytest` test suite to verify tests pass and coverage is maintained.

### Testing

- Write unit tests targeting `CliRunner` invocations:
  - `runner.invoke(app, ["--version"])`
- Assert that output matches: `check-md <version> (<absolute-path-to-package-directory>)`
- Assert that exit code is `0`.
- Verify the `--version` works when called both by itself and when combined with other mock arguments.

### Success Criteria

- [ ] Unit tests for the `--version` flag are written and fail before implementation (RED state).
- [ ] Implement the callback and register option to make tests pass (GREEN state).
- [ ] Coverage for the newly introduced code matches or exceeds the 90% target.
- [ ] `check-md` linter runs successfully across its own codebase.

**Rationale:** Implementing this via TDD ensures the interface behaves precisely as specified before it is integrated into downstream scripts.

---

## Phase 2: Global Workspace Verification & Tooling Integration

### Goals

1. Manually verify `check-md --version` from the workspace CLI to confirm correct local output.
2. Verify that there are no regressions or conflicts in the pre-commit hooks or global installation configurations.
3. Validate that the entire `check-md` test suite and standard checks pass cleanly.

### Approach

- **Step 1:** Run a global verification check: executing the newly built `check-md --version` in terminal.
- **Step 2:** Ensure the printed absolute path points accurately to the active package directory under `src/check_md`.
- **Step 3:** Run `scripts/run-all-checks.sh` to ensure overall workspace health is perfect.

### Testing

- Manual execution tests in terminal.
- Workspace linter execution.

### Success Criteria

- [ ] `check-md --version` output contains the correct absolute path on the host system.
- [ ] All workspace tests and checkers run and pass cleanly without any regression.
- [ ] Success checkboxes in `goals.md` and `plan.md` are evaluated, confirmed, and updated.

**Rationale:** Manual verification from the shell ensures that editable installs and absolute path resolution function exactly as expected on real file systems.

---

## Risk Mitigation

No high-risk items identified. Using `is_eager=True` prevents Typer from parsing or requiring other missing positional arguments, eliminating standard CLI arg errors when checking the version.

## Decision Points

### After Phase 1

- Proceed to Phase 2 once the tests are implemented, passing, and coverage targets are fully met.

### After Phase 2

- Author the completion summary and prepare the final pull request using the `leap-finish` and `leap-pr` workflows.
