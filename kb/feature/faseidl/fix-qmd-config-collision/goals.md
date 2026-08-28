# Fix QMD-Config Collision Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-28

---

## Quick Summary

Prevent `qmd-config` from reporting success when collection creation fails due to path/pattern collision, and safeguard context hint registration.

## Executive Summary

`qmd-config` currently detects idempotent registration by checking if the stdout/stderr of `qmd collection add` contains the string `"already exists"`. However, if a path or pattern collision occurs with a *different* collection name, `qmd` also outputs "already exists" in its warning message (e.g. `A collection already exists for this path and pattern:`), but does *not* create the collection. Under this situation, `qmd-config` falsely reports success (e.g. `✓ <collection> already exists (skipped)`). It later crashes with `Collection not found` when attempting to attach context to the non-existent collection.

We will:

1. Make `qmd-config` distinguish between actual idempotent skip (where the collection with the desired name already exists) and a path/pattern collision with a different collection name.
2. Ensure that `qmd-config` fails gracefully and explicitly when a collision occurs, outputting a clear, actionable message that suggests running with `--remove-legacy`.
3. Add a validation guard to `emit_context` to verify that a collection actually exists before attempting to register context on it, preventing downstream crashes if a registration fails or is skipped.
4. Add automated test coverage in `scripts/qmd/tests/qmd-config.test.sh` to prevent regressions.

## Objectives

1. Fix the false positive "already exists" detection in `emit_collection`.
2. Add a verification check to `emit_context` to avoid crashes on non-existent collections.
3. Improve troubleshooting output when a path/pattern collision is detected, suggesting `--remove-legacy`.
4. Implement automated tests to verify the behavior and ensure robustness.

## Requirements

### Functional Requirements

- REQ-1: `emit_collection` must only treat a registration as an idempotent skip if the error from `qmd collection add` explicitly states that the requested collection name already exists (e.g., matching the message format `Collection '<name>' already exists.`).
- REQ-2: If `qmd collection add` fails because of a path/pattern collision with a different collection name, `qmd-config` must fail explicitly with an exit status of 1 and print a helpful suggestion recommending `--remove-legacy`.
- REQ-3: `emit_context` must verify that the target collection exists before attempting to attach context to it, warning rather than crashing if the collection is missing.

### Non-Functional Requirements

- Performance: No noticeable performance regression during configuration.
- Security: No credential leaks.
- Maintainability: Simple, readable Bash scripting aligned with Bash 3.2 compatibility.

### Testing Requirements

- Write a unit/integration test case in the existing test suite (`scripts/qmd/tests/qmd-config.test.sh`) to reproduce the collision bug and verify that the script fails correctly and suggests `--remove-legacy`.
- Verify that correct idempotent skip still works.

### Documentation Requirements

- Update inline comments in `scripts/qmd/qmd-config` explaining the collision checks and why the validation guard is needed.

## Success Criteria

- [x] `qmd-config` correctly identifies and reports actual idempotent skips when a collection with the same name already exists.
- [x] `qmd-config` aborts execution and returns exit code 1 when a path/pattern collision with a different collection name is detected.
- [x] When a path/pattern collision occurs, the output suggests running with `--remove-legacy`.
- [x] `emit_context` does not crash when attempting to add context to a non-existent collection, but instead prints a warning.
- [x] New automated tests are added and pass successfully.

## Constraints

- Must remain fully compatible with Bash 3.2 (macOS default).
- Must not require external tools beyond what is already standard in the repo.

## Assumptions

- The QMD CLI is installed and available in the testing environment.

## Out of Scope

- Modifying the underlying `qmd` CLI tool itself.
