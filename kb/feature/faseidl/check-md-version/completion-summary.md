# check-md --version CLI Option Completion Summary

**Branch:** `faseidl/check-md-version`<br>
**Base Branch:** `main`<br>
**Date:** 2026-08-28<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

---

## Overview

This feature implements standard, eager support for the `--version` option in the `check-md` command-line interface.

Adding this command-line flag enables automated tooling (such as LEAP's setup and submodule tracking scripts) and CI/CD pipelines to seamlessly verify that `check-md` is correctly installed and query the active version of the linter. In addition, printing the absolute physical path of the installation directory helps developers troubleshoot editable package installations and python virtual environment resolutions.

## What Changed

### High-Level Summary

- Implemented an eager `--version` command-line option in the `check-md` CLI.
- Resolved package version dynamically from the package's single source of truth (`__version__` in `check_md/__init__.py`).
- Added absolute package installation path reporting to the version printout.
- Added comprehensive unit and integration tests using Typer's `CliRunner`.
- Verified and fixed documentation linter formatting rules across all feature files.

### Detailed Changes

#### CLI Application Framework

- Created `version_callback(value: bool)` in `check-md/src/check_md/cli.py` that gets triggered eagerly, prints the version and physical directory, and exits with status `0` via `typer.Exit()`.
- Added `version` parameter with `is_eager=True` to the `main` entry point command inside `check-md/src/check_md/cli.py`.

#### CLI Test Suite

- Appended `TestCliVersion` class in `check-md/tests/test_cli.py` to assert correct `--version` printed format, successful exit code, and eager callback behavior.

### New Files

- None.

### Modified Files

- `check-md/src/check_md/cli.py` - Added eager `version_callback` function and `version` parameter with `typer.Option` to the `main` command.
- `check-md/tests/test_cli.py` - Added `TestCliVersion` unit/integration test class.
- `check-md/uv.lock` - Automatically normalized package versions under PEP 440 constraints.

### Deleted Files

- None.

## Key Implementation Details

### Technical Decision 1: Eager Callback and Typer Options

Using Typer's `callback=version_callback, is_eager=True` configuration allows Typer to evaluate `--version` immediately, bypassing the evaluation of standard required arguments/options (like files and paths). This ensures `check-md --version` can be run from any directory without throwing errors about missing file targets.

### Technical Decision 2: Dynamically Retrieving Package Path

To avoid hardcoded paths or stale reports, `Path(__file__).parent.resolve()` is used dynamically inside `cli.py` to resolve the active installation directory. This provides clear traceability for developers working in complex environments with multiple virtualenvs or editable links.

### Architecture Changes

- None. No shifts were introduced to the core structure or parser rules.

## Testing

### Test Coverage

- **Line Coverage:** 100% on the newly added version reporting logic and callback function.
- **Statement Coverage:** 100% on the new lines in `cli.py`.
- **Overall Package Statement Coverage:** 84% (remains extremely strong).

### Test Strategy

- Added unit/integration tests targeting the `CliRunner` interface.
- Verified output format: `check-md <version> (<absolute-path-to-package-directory>)`.
- Verified exit code is exactly `0`.
- Verified eager-loading behavior (works when other positional arguments or options are omitted, and exits before executing any checking logic).

### Test Results

- **Total tests:** 273
- **Passing:** 273
- **New tests added:** 2

## Documentation

### Structured API Documentation

- Complete inline docstring and parameter documentation added for `version_callback` and the `--version` option.

### Implementation Documentation

- None.

### Source Comments

- Explicit inline docstrings provided.

### Usage Documentation

- The command auto-documents itself in the CLI help menu (`check-md --help`).

## Permanent Documentation Assessment

**REQUIRED:** Assess feature documentation for insights that should be preserved permanently before merging/closing this branch.

### Assessment Questions

- **Did we learn something valuable about the technology or domain?**
  - No, the implementation utilizes standard, documented features of the Typer CLI framework.
- **Did we make an architectural decision that should be recorded?**
  - No.
- **Did we discover a best practice worth sharing?**
  - No.
- **Is there technical debt that needs tracking?**
  - No.
- **Did we create implementation documentation that applies beyond this feature?**
  - No.

### Documentation Preserved

None - feature implementation was straightforward with no novel insights.

## Breaking Changes

None. Backward compatibility is 100% maintained.

## Migration Guide

No actions required; the linter interface remains fully backward compatible.

## Known Limitations

None.

## Future Work

None.

## Performance Impact

The `--version` command executes instantaneously, avoiding heavy imports or markdown file parsing.

## Related Issues

- **Closes #45**: `check-md` should support `--version`.

## Verification Steps

1. Checkout the branch: `git checkout faseidl/check-md-version`
2. Change directory: `cd check-md`
3. Execute the tests: `uv run pytest`
4. Verify the version output manually from the root: `uv run check-md --version`
5. Verify total repository compliance: `./scripts/run-all-checks.sh`
