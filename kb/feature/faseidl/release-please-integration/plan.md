# Release Please Integration Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-25

---

## Overview

We will implement Google's Release Please for repository-wide release automation. The root project `.` (named `leap`) will use the `"simple"` release type. This allows the repository to generate clean, root-level release tags (e.g. `v1.0.0-beta.0`) instead of subdirectory-prefixed tags. We will use the `extra-files` configuration to propagate version updates in lockstep to the nested `check-md` Python tool files (`pyproject.toml`, `__init__.py`) and its lockfile (`uv.lock`).

**Development Approach:** Use Test-Driven Development (TDD) throughout - write and update tests and validation steps before completing implementation code.

### Overall Assessment

- **Complexity:** MEDIUM - Requires precise JSONPath-TOML mapping and Release Please configuration syntax.
- **Risk:** LOW - No modifications to core application logic are required. All configuration is declarative or documentation.

---

## Phase 1: Local Setup & Version Alignment (Dry-Run / Files)

### Goals

- Establish Release Please configuration files at the repository root.
- Align and update current package versions in `check-md/` to `1.0.0-beta.0` with correct Release Please update markers.
- Run local linting, testing, and schema validation to verify correctness.

### Approach

- Create `release-please-config.json` containing the schema, packages config (using `"simple"` release type for `.`), prerelease flag, prerelease-type as `beta`, and `extra-files` mappings.
- Create `.release-please-manifest.json` containing the initial version target: `{"." : "1.0.0-beta.0"}`.
- Surgical modification of `check-md/pyproject.toml` and `check-md/src/check_md/__init__.py` to update the version strings to `1.0.0-beta.0` and append `# x-release-please-version` comments.
- Update the version of `check-md` in `check-md/uv.lock` to `1.0.0-beta.0`.
- Run `check-md` linter and test suite to ensure no breakage.

### Testing

- Execute unit tests in `check-md/` to ensure the package works correctly with the updated version string.
- Perform a dry-run linter check on all modified code.
- Validate `release-please-config.json` against Google's official v4 config schema.

### Success Criteria

- [ ] `release-please-config.json` successfully drafted and validated.
- [ ] `.release-please-manifest.json` successfully created.
- [ ] Versions in `check-md/pyproject.toml`, `check-md/src/check_md/__init__.py`, and `check-md/uv.lock` updated and marked correctly.
- [ ] Python unit tests and `check-md` validation checks pass with zero errors.

### Explicitly Deferred

- None.

**Rationale:** Establishing correct, syntax-validated local files is the foundation of any automated CI/CD setup.

---

## Phase 2: GitHub Action Integration & Trigger Setup

### Goals

- Create the GitHub Actions workflow to run Release Please on every push to the default branch (`main`).
- Configure standard write/pull-request permissions required by Release Please.

### Approach

- Create `.github/workflows/release-please.yml` targeting pushes to `main`.
- Employ `googleapis/release-please-action@v4` with minimal required permissions:
  ```yaml
  permissions:
    contents: write
    pull-requests: write
  ```

- Structure the workflow action steps to output build status or run checks.

### Dependencies

- Depends on Phase 1 completion.

### Testing

- Validate the YAML schema of `.github/workflows/release-please.yml` using standard local syntax checking.
- Verify that permissions and triggers conform to security guidelines in the repository.

### Success Criteria

- [ ] `.github/workflows/release-please.yml` created and syntax-checked.
- [ ] Action triggers and GITHUB_TOKEN permissions properly restricted.

### Rationale

GitHub Actions is the execution engine that parses our Conventional Commits and automatically updates/opens our release PRs.

---

## Phase 3: Documentation & Guides

### Goals

- Produce clear, comprehensive developer guides detailing the release cycle.
- Explain how to perform lifecycle transitions (beta -> rc -> stable general release).

### Approach

- Create `kb/guide-release-management.md` explaining:
  - How Conventional Commits (e.g. `feat:`, `fix:`) trigger Release Please to generate changelogs and bump versions.
  - The step-by-step process of transitioning the pre-release type (from `beta` to `rc`, and then to a stable release by toggling the `"prerelease"` flag to `false`).
  - Clear boundaries regarding the submodule scope (releases concern only the LEAP repository, not parent submodules).
- Perform a full `check-md` audit on all new and modified Markdown files.

### Testing

- Verify that all modified Markdown files pass `check-md kb/` with zero violations.
- Run a broken link check to ensure all document connections are healthy.

### Success Criteria

- [ ] `kb/guide-release-management.md` successfully written and integrated.
- [ ] Transition procedures (beta -> rc -> stable) fully documented.
- [ ] `check-md` linter passes 100%.

### Rationale

Documentation ensures that humans can confidently run and maintain the automated system in the future, especially during critical transition periods.

---

## Risk Mitigation

### Risk 1: Version Synchronization Drift

A developer might manually edit the version files without updating `.release-please-manifest.json` or vice versa, causing version mismatches.

#### Mitigation

Document clearly in the release management guide that the version manifest is the single source of truth for Release Please, and provide instructions to keep local files synchronized.

---

## Decision Points

### After Phase 1 (Local Setup)

- Continue to Phase 2 if the config files are schema-compliant and local package tests pass perfectly.

### After Phase 2 (GitHub Actions)

- Continue to Phase 3 if the YAML workflow file is valid and security permissions are properly established.

---

## Notes

- Useful reference: [Googleapis Release Please Action](https://github.com/googleapis/release-please-action).
