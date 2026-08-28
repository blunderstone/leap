# check-md --version CLI Option Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-28

---

## Quick Summary

Add a standard, eager `--version` command-line flag to the `check-md` CLI that outputs the current version and physical installation path, reading from a single source of truth.

## Executive Summary

Currently, the `check-md` linter lacks a `--version` CLI flag. This lack of a version flag causes tooling issues:

1. LEAP's submodule conversion and setup tooling expect to run `check-md --version` for follow-up reports.
2. Downstream CI/CD pipelines cannot easily verify successful installation or query the linter's active version.
3. Because `check-md` is often installed in an "editable" mode during development, standard tools like `pip show` can report stale or misleading information. 

By implementing an eager `--version` option in the `check-md` command-line interface, users and automated tooling will be able to reliably identify the exact version and installation path of the active `check-md` executable.

## Risk and Complexity Assessment

**Overall Risk:** LOW

**Overall Complexity:** LOW

This is a standard CLI enhancement using Typer's built-in callback capabilities. There are no anticipated risks or major complexities.

## Objectives

1. **Eager Option:** Support `--version` (and optionally `-V` if standard, or just `--version`) as an eager callback option that exits immediately.
2. **Single Source of Truth:** Read the version dynamically from the package's `__version__` attribute.
3. **Traceability:** Print the physical path to the package alongside the version number to assist in diagnosing editable installations and virtual environment setups.
4. **Tooling & CI Compatibility:** Ensure other automated tools and pipelines can execute `check-md --version` and retrieve a clean, successful exit (status code 0).

## Requirements

### Functional Requirements

- **REQ-1:** Implement a `--version` flag using a Typer "eager" callback.
- **REQ-2:** When `--version` is provided, print the version and physical package directory in the following format:
  ```text
  check-md <version> (<absolute-path-to-package-directory>)
  ```

- **REQ-3:** Running `check-md --version` must immediately exit with status code 0, without requiring other command-line arguments (e.g. file paths) and without executing any linting logic.
- **REQ-4:** The printed version must dynamically read from the package's `__version__` attribute defined in `check_md/__init__.py`.

### Non-Functional Requirements

- **Performance:** Checking the version must execute instantaneously without importing heavy modules that are not required for printing the version.
- **Clean Exit:** Ensure clean exit status of 0 without writing to standard error.

### Testing Requirements

- **Unit/Integration Tests:** Add tests using Typer's `CliRunner` to verify:
  - Invoking `check-md --version` prints the version in the correct format.
  - Invoking `check-md --version` exits with code 0.
  - The path printed in the output is correct and absolute.
  - The `--version` flag works even when other positional arguments or options are omitted.
- **Code Coverage:** Maintain 90%+ code coverage on the new CLI version logic.

### Documentation Requirements

- Update `check-md` CLI documentation/help if necessary, though Typer auto-documents help menus.

## Success Criteria

- [x] `check-md --version` prints the version from `__version__` and the absolute package path.
- [x] `check-md --version` exits with status 0.
- [x] Command works without passing any paths or files.
- [x] CLI tests are implemented and pass successfully.
- [x] `check-md` linting and all existing test cases continue to pass.

## Constraints

- Must use Typer options and callbacks compatible with `typer>=0.27.1`.

## Assumptions

- Typer's callback structure with `is_eager=True` is the idiomatic way to handle version flags in Typer-based CLI applications.

## Out of Scope

- Adding custom telemetry or reporting during version check.
