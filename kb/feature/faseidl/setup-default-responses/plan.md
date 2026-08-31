# setup-leap.sh Default Responses Implementation Plan

**Author:** [F. Andy Seidl](https://github.com/faseidl)<br>
**Date:** 2026-08-30

---

## Overview

We will update the interactive default answers in `scripts/setup-leap.sh` so that running the setup script interactively and pressing Enter (the default selection) chooses "Yes" (`y`) for standard, non-destructive configurations. This provides a fast, frictionless setup path for first-time users. Destructive operations (such as completely overwriting an existing customized file) will remain defaulting to "No" (`n`) for safety.

**Development Approach:** Use Test-Driven Development (TDD) principles - update/write tests first to define the new expectations, then modify the main setup script until the tests pass cleanly.

### Overall Assessment

- **Complexity:** LOW - Direct adjustments to default arguments in bash function calls and updating existing bash test scripts.
- **Risk:** LOW - Changes are localized to `scripts/setup-leap.sh` and its associated unit test file.

---

## Phase 1: Update Prompt Defaults in `setup-leap.sh`

### Goals

- Change standard, non-destructive interactive prompt defaults from "n" to "y".
- Keep dangerous/destructive interactive prompts (overwrites) defaulting to "n".
- Ensure backward compatibility with all non-interactive flags (`--yes`, `--no`, and selective components).

### Approach

- Modify `scripts/setup-leap.sh` lines where `ask_yes_no` is invoked for:
  - Submodule recurse setup.
  - check-md global/local installation.
  - AI guides generation (CLAUDE.md, GEMINI.md, copilot-instructions.md, .cursorrules).
  - Custom skills installation.
  - .gitignore configuration.
  - git pre-commit hook installation.
  - QMD configuration.
- Verify that `ask_yes_no` calls for file overwrite warnings remain using `"n"` as default.

### Testing

- Confirm the script executes without syntax errors.
- Confirm that existing CLI flag tests in `test_setup_flags.sh` are not broken by the default changes.

### Success Criteria

- [ ] All standard prompt calls to `ask_yes_no` in `setup-leap.sh` use `"y"` as their default parameter.
- [ ] Overwrite confirmation prompt calls to `ask_yes_no` in `setup-leap.sh` use `"n"` as their default parameter.
- [ ] No regression is introduced in syntax or basic flow.

---

## Phase 2: Add and Verify Behavioral Tests

### Goals

- Add test coverage for interactive prompt defaults.
- Ensure all existing and new tests pass cleanly.

### Approach

- Edit `scripts/tests/test_setup_flags.sh` to include a new test case:
  - Run `setup-leap.sh` interactively, but pipe a series of empty carriage returns (newlines) into it.
  - Assert that all expected standard files (CLAUDE.md, GEMINI.md, .cursorrules, .github/copilot-instructions.md) are successfully created.
  - This verifies that empty carriage returns resolve to their new "yes" defaults.
- Execute the test suite using `scripts/run-all-checks.sh` to guarantee all project checks continue to pass cleanly.

### Success Criteria

- [ ] New carriage return interactive default test is implemented.
- [ ] Test suite executes and passes 100% cleanly.
- [ ] Project-wide check runner (`run-all-checks.sh`) succeeds.

---

## Phase 3: Documentation Audit and Updates

### Goals

- Identify any repo documentation mentioning the setup defaults.
- Correct references to the previous "n" defaults to accurately reflect the new "y" default behavior.

### Approach

- Use `grep_search` to search the `kb/` directory and repo-level files (such as `README.md` or `CONTRIBUTING.md`) for mentions of the setup script prompts, their default values, or instructions on how to run it.
- Update any found files to align with the new, frictionless "default to yes" interactive setup behavior.

### Success Criteria

- [ ] Documentation audit completed.
- [ ] All occurrences of old setup prompt behaviors or defaults updated in the guides and readmes.

---

## Decision Points

### After Phase 1

- Proceed if the bash script's syntax is valid and standard manual verification is successful.

### After Phase 2

- Feature is complete and ready for PR summary once all tests are passing and coverage/checks are green.
