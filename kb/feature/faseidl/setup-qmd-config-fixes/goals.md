# Setup and QMD Configuration Fixes Goals

**Author:** [F. Andy Seidl](https://github.com/faseidl)<br>
**Date:** 2026-08-28

---

## Quick Summary

Enhance `setup-leap.sh` to resolve initial migration failures by passing `--remove-legacy` to `qmd-config`, and refactor `qmd-config` to write a workstation-safe, generic LEAP convention description instead of a project-specific description to the global `/` context slot.

## Executive Summary

This feature addresses two related issues in the repository setup and QMD index configuration tools.

Issue #52: When migrating repositories to the new LEAP conventions, `setup-leap.sh` invokes `qmd-config` without `--remove-legacy`. This causes first-run configuration failures because pre-convention unprefixed collections (e.g., `readmes`) collide with the new prefixed ones. By passing `--remove-legacy` when calling `qmd-config` from `setup-leap.sh` and in its failure retry recommendation, we eliminate this guaranteed first-run failure.

Issue #53: Currently, `qmd-config` writes a project-specific description into the single workstation-global context slot (`/`). In a multi-project developer workstation, each project's run overwrites this global slot, leading to inaccurate headers when searching other projects. We will change this to write a generic, idempotent description of the LEAP document taxonomy conventions, making last-writer-wins harmless while keeping the helpful developer orientation.

## Objectives

1. Fix the setup-leap first-run failure by updating `setup-leap.sh` and its recommended retry command to include `--remove-legacy` when configuring QMD.
2. Prevent project-specific metadata pollution of the global QMD context slot by replacing the project-specific text in `qmd-config` with a generic, workstation-safe LEAP convention description.
3. Ensure existing tests remain fully functional, and add/update tests verifying the correct execution and output of the scripts.

## Requirements

### Functional Requirements

- **REQ-1:** `setup-leap.sh` must call `qmd-config` with the `--remove-legacy` option.
- **REQ-2:** The warning/retry command printed on failure by `setup-leap.sh` must include `--remove-legacy`.
- **REQ-3:** `qmd-config` must write a generic description of the LEAP conventions to the workstation-global `/` context slot, rather than a project-specific one.

### Non-Functional Requirements

- **Performance targets:** Setup execution time should not be negatively impacted.
- **Maintainability requirements:** The changes must be written clearly and robustly in bash, following existing scripting conventions.

### Testing Requirements

- **Critical paths:** Verify `setup-leap.sh` invokes the configurator with `--remove-legacy`. Verify `qmd-config` emits the generic description to the `/` context slot.
- **Edge cases:** Ensure the configuration behaves gracefully in both fresh setups and migration setups.
- **Verification:** Run all setup and QMD config tests.

### Documentation Requirements

- Ensure inline comments in scripts explain the flags and options used.

## Success Criteria

- [ ] `setup-leap.sh` passes `--remove-legacy` to `qmd-config`.
- [ ] The retry warning printed by `setup-leap.sh` specifies `--remove-legacy`.
- [ ] `qmd-config` writes the generic LEAP convention description to the global `/` context slot instead of a project-specific string.
- [ ] Existing pre-commit/setup and QMD configuration test suites pass successfully.
- [ ] New or updated tests cover the changed behavior.

## Constraints

- Must remain fully compatible with POSIX shell or standard macOS/Linux bash features already used in the scripts.

## Assumptions

- The developer's workstation has standard GNU/BSD command line utilities.
- Removing pre-convention legacy collections for the repository is safe during setup.

## Out of Scope

- Changing the core behavior of `qmd` context lists or query logic itself.
