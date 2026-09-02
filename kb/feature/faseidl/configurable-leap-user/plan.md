# Configurable LEAP User Implementation Plan

**Author:** AI CLI Agent<br>
**Date:** 2026-09-02

---

## Overview

The goal of this feature is to make the LEAP compliance directory username configurable. This prevents conflicts in multi-developer environments or machines where the local OS login name (e.g., `fseidl`) differs from the agreed project handle (e.g., `faseidl`).

### Development Approach
We will use Test-Driven Development (TDD) throughout. We will write failing tests for each phase's target behavior first, and then implement the minimal solution in our scripts to make the tests pass.

### Overall Assessment

- **Complexity:** LOW - The changes are isolated to configuration parsing in bash scripts (`pin-leap.sh` and `setup-leap.sh`) and writing/reading values to/from local Git configurations.
- **Risk:** LOW - Fallback behavior will preserve existing functionality completely.

---

## Phase 1: Hierarchical Username Resolution & Sanitization in `pin-leap.sh`

### Goals

- Implement the hierarchical resolution of the LEAP username in `scripts/pin-leap.sh`:
  1. `LEAP_USER` environment variable.
  2. `git config --get leap.user` (local or global).
  3. Existing OS login-based fallback logic (`USER` -> `id -un` -> `whoami` -> `developer`).
- Implement identical lowercase-and-strip normalization on whatever value is retrieved to ensure file path safety.
- Write unit tests in `scripts/tests/pin-leap.test.sh` verifying that all levels of the hierarchy and sanitization work correctly.

### Approach

- Update the username extraction section in `scripts/pin-leap.sh`:
  - Try fetching `LEAP_USER`.
  - If empty, try `git config --get leap.user`.
  - If still empty, fall back to the existing login-name detection.
  - Apply the lowercase-and-sanitize logic to clean the resolved name:
    ```bash
    LEAP_USER=$(echo "$LEAP_USER" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9._-]//g')
    ```
- Add test scenarios in `scripts/tests/pin-leap.test.sh` that mock:
  - `LEAP_USER` set as an environment variable.
  - `git config leap.user` set locally.
  - Sanitization of abnormal characters (e.g. spaces, uppercase letters, invalid symbols).

### Testing

- Run the unit tests to confirm the new resolution hierarchy.
- Ensure all existing tests in `scripts/tests/pin-leap.test.sh` continue to pass.

### Success Criteria

- [ ] `scripts/pin-leap.sh` implements `LEAP_USER` -> `git config` -> OS username fallback.
- [ ] Username is safely normalized and sanitized to lowercase alphanumeric, `.`, `_`, or `-` characters.
- [ ] Unit tests are written to verify resolution hierarchy and sanitization under simulated conditions.
- [ ] Test coverage is maintained/increased and all tests in `pin-leap.test.sh` pass.

---

## Phase 2: Configuration & Prompts in `setup-leap.sh`

### Goals

- In `scripts/setup-leap.sh`, prompt the user for their LEAP username during interactive setup.
- Scan the subdirectories under `kb/feature/` to propose a smart default for the prompt (falling back to the current OS username if none exists).
- If the session is non-interactive (e.g., stdin is not a terminal, or the `--yes` / `--no` flags are used), bypass the prompt and configure the default username.
- Write the final selected username to local git config: `git config leap.user "<username>"`.
- Update `scripts/tests/test_setup_flags.sh` to verify that the username prompt behaves correctly and saves the configuration.

### Approach

- Propose a smart default in `scripts/setup-leap.sh` by searching directories in `kb/feature/*`:
  - Extract the names of subdirectories under `kb/feature/`.
  - Filter out any generic paths.
  - If there is exactly one user-specific directory (or a dominant one), propose it as the default. Otherwise, fall back to detecting the OS user.
- Implement the interactive prompt:
  - Display the prompt: `Enter your LEAP username (used for feature directories) [default: <default_username>]: `.
  - Read input and fall back to the default if the user presses Enter.
- Sanitize the input to ensure it meets path-safety criteria.
- Run `git config leap.user "$SELECTED_USERNAME"` to persist the preference.
- Add test scenarios in `scripts/tests/test_setup_flags.sh` to verify:
  - Default selection when Enter is pressed.
  - Prompt bypass in non-interactive/headless environments.
  - Correct configuration saving in `.git/config`.

### Testing

- Run `scripts/tests/test_setup_flags.sh` to verify flag and non-interactive handling.
- Run interactive manual test of `setup-leap.sh` to verify prompt aesthetics.

### Success Criteria

- [ ] `setup-leap.sh` detects existing `kb/feature/` directories and proposes a smart default username.
- [ ] `setup-leap.sh` prompts for the LEAP username in interactive sessions, and saves the sanitized value in local `git config leap.user`.
- [ ] Non-interactive or flag-based execution does not block and configures the default username.
- [ ] Tests in `test_setup_flags.sh` are updated and pass successfully.

---

## Phase 3: Final Verification & Integration

### Goals

- Ensure there are no regressions across the entire workspace by running all tests.
- Verify that standard linting and formatting pass.
- Mark all items as complete and prepare handoff to `leap-dev`.

### Approach

- Execute `bash scripts/run-all-checks.sh` to run the entire workspace verification suite.
- Ensure everything is fully compliant and all tests pass.

### Success Criteria

- [ ] All tests in `scripts/tests/pin-leap.test.sh` pass.
- [ ] All tests in `scripts/tests/test_setup_flags.sh` pass.
- [ ] Workspace-wide linter check passes with 0 failures.

---

## Decision Points

### After Phase 1
- Verify that the resolution hierarchy is completely solid and covered by automated assertions before touching `setup-leap.sh`.

### After Phase 2
- Verify that the interactive prompts do not break non-interactive/CI environments. Ensure stdin redirect `/dev/null` tests in `test_setup_flags.sh` continue to run perfectly.
