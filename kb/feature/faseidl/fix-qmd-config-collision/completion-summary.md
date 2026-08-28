# Fix QMD-Config Collision Completion Summary

**Branch:** `faseidl/fix-qmd-config-collision`<br>
**Base Branch:** `main`<br>
**Date:** 2026-08-28<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

---

## Overview

We have resolved a critical issue where `qmd-config` incorrectly reported success (idempotent skip) when a collection registration failed due to a path/pattern collision with a different collection name. This occurred because `qmd-config` performed a loose string check for `"already exists"` on the stderr of `qmd collection add`, matching generic collision errors as well as name-specific registration skips. Furthermore, when registration failed or was skipped downstream, attempting to attach context to the missing collection caused `qmd-config` to crash entirely.

To fix these issues, we:

1. Updated `emit_collection` to strictly check for name-specific already-exists skip errors (e.g., `Collection '<name>' already exists.`).
2. Added an explicit error state that prints a helpful suggestion to run with `--remove-legacy` and aborts execution with exit code 1 on path/pattern collisions.
3. Added a collection existence guard in `emit_context` utilizing `qmd collection show <collection>` to warn instead of crash when registering context for a missing collection.
4. Created automated integration tests in `scripts/qmd/tests/qmd-config.test.sh` to reproduce and prevent these regression states.

## What Changed

### High-Level Summary

- **Stricter Idempotency Checking**: Enhanced `emit_collection` to distinguish name-specific skips from generic path/pattern collisions.
- **Fail-Fast & Actionable Suggestions**: Made the config script exit with 1 on path/pattern collisions and suggest the `--remove-legacy` option.
- **Context Existence Guard**: Shielded `emit_context` against downstream crashes by verifying collection existence.
- **Automated Regression Coverage**: Added three new integration test cases to target these conditions.

### Detailed Changes

#### scripts/qmd/qmd-config

- `emit_collection()`: Modified to query if `err_out` matches `"Collection '$1' already exists"` (case-insensitive) instead of the broad `"already exists"`.
- `emit_collection()`: Added error-handling path to suggest running with `--remove-legacy` if the error contains `"already exists"` but does not match the name-specific pattern, then exiting with 1.
- `emit_context()`: Implemented a parser to extract the collection name from `qmd://` URIs and check for collection existence using `qmd collection show "$collection"`. Warnings are now emitted to stderr, and context registration is safely skipped on failure.

#### scripts/qmd/tests/qmd-config.test.sh

- `Test 12`: Added a self-contained mock `qmd` executable that handles mock behaviors for `status`, `update`, `embed`, `collection add`, `collection show`, and `context add` arguments.
- `Test 12a`: Verifies that path/pattern collisions abort with exit code 1 and recommend the `--remove-legacy` option.
- `Test 12b`: Verifies that name-specific already-exists skips succeed with exit code 0.
- `Test 12c`: Verifies that attempting to register context for a missing collection warns and exits cleanly.

### New Files

- `kb/feature/faseidl/fix-qmd-config-collision/completion-summary.md` - Documents high-level and detailed changes, technical decisions, testing strategy, and verification results.

### Modified Files

- `scripts/qmd/qmd-config` - Implemented strict idempotent checks, suggesting `--remove-legacy`, and collection existence checks in `emit_context`.
- `scripts/qmd/tests/qmd-config.test.sh` - Added Test 12 covering collision, idempotency, and context guard behaviors.
- `kb/feature/faseidl/fix-qmd-config-collision/goals.md` - Updated success criteria checkboxes to completed.
- `kb/feature/faseidl/fix-qmd-config-collision/plan.md` - Updated success criteria checkboxes to completed.

### Deleted Files

- None.

## Key Implementation Details

### Strict Error Analysis in Bash

Instead of using a loose grep on `already exists`, we dynamically match against the collection name passed to the function: `Collection '$1' already exists`. This ensures that only a duplicate name error triggers an idempotent skip. Any other error containing `already exists` is treated as a collision, and the script exits with code 1.

### Robust POSIX-Compliant URI Parsing

To parse the collection name in `emit_context`, we avoid complex regex engines and use pure POSIX-compliant parameter expansions:

```bash
local without_scheme="${uri#qmd://}"
local collection="${without_scheme%%/*}"
```
This guarantees 100% compatibility across all Bash versions (especially macOS default Bash 3.2).

## Testing

### Test Coverage

- **Line/Statement/Branch Coverage**: N/A for Bash scripting natively, but all added and modified logic in `qmd-config` is fully covered and exercised by the new `Test 12` suite.

### Test Strategy

- Created a virtualized, isolated environment inside `qmd-config.test.sh` that mocks the `qmd` CLI.
- Verified both successful (0) and failing (1) exit statuses.
- Asserted stdout and stderr matches for specific error logs, suggestions, and skip notices.

### Test Results

- **Total tests**: 54
- **Passing**: 54
- **New tests added**: 3 (Test 12a, 12b, 12c)

## Documentation

### Structured API Documentation

- N/A (Script-level functions, not public APIs).

### Implementation Documentation

- Heavily commented `emit_collection` and `emit_context` in `scripts/qmd/qmd-config` to describe why the guards are needed and how they protect against the path/pattern collision.

### Source Comments

- All public functions in `qmd-config` have inline descriptions explaining parameters and behaviors.

### Usage Documentation

- None - usage of `qmd-config` remains identical.

## Permanent Documentation Assessment

### Assessment Questions

- **Did we learn something valuable?** No, standard Bash debugging.
- **Did we make an architectural decision?** No.
- **Did we discover a best practice?** Yes, mocking CLI programs by prepending a mock folder to `PATH` in Bash tests is a highly robust pattern.
- **Is there technical debt?** No.
- **Did we create implementation documentation that applies beyond this feature?** No.

### Documentation Preserved

- None - feature implementation was straightforward with no novel insights.

## Breaking Changes

- None (backward-compatible bug fix).

## Migration Guide

- No action required.

## Known Limitations

- None.

## Future Work

- None.

## Performance Impact

- **Baseline/After/Impact**: Neutral. Querying collection existence using `qmd collection show` in `emit_context` introduces negligible overhead because it is only called during configuration setup (which runs infrequently).

## Related Issues

- Closes #46: qmd-config reports success on path/pattern collision but crashes on context hints.

## Verification Steps

1. Checkout the branch: `git checkout faseidl/fix-qmd-config-collision`
2. Run tests: `bash scripts/qmd/tests/qmd-config.test.sh`
3. Run `check-md` to verify documentation: `check-md kb/feature/faseidl/fix-qmd-config-collision/`
