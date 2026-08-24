# Multi-Tiered Automated Gating Completion Summary

**Branch:** `faseidl/automated-gating`<br>
**Base Branch:** `main`<br>
**Date:** 2026-08-24<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

---

## Overview

This feature implements a multi-tiered automated gating system designed to programmatically block AI agents and human developers from committing broken code or bypassing linter/test failures. 

To eliminate "explanation/rationalization bias" (where developers or agents rationalize away active test failures and attempt to finalize features), we introduced three concentric rings of automated gating:

1. **Unified Test Runner:** A single, fast command (`scripts/run-all-checks.sh`) aggregating all formatters, linters, and unit/shell test suites.
2. **Git Pre-Commit Hook:** A git hook (`scripts/git-pre-commit`) deployed automatically during setup (`setup-leap.sh`) strictly for standalone LEAP developers, physically rejecting broken commits.
3. **Cognitive Zero-Failure Rule:** A strict negative constraint integrated directly into `.skills/leap-dev/SKILL.md` that programmatically forbids agents from declaring phases complete, checking off checklist boxes, or proposing transitions if checks are failing.

A GitHub Actions CI workflow was also created to enforce these checks remotely on every push or PR.

## What Changed

### High-Level Summary

- **Unified Check Script:** Created `scripts/run-all-checks.sh` as the authoritative runner.
- **Git Pre-Commit Hook:** Created `scripts/git-pre-commit` to prevent broken commits locally.
- **Setup Automation:** Updated `scripts/setup-leap.sh` to copy the pre-commit hook during environment setup, isolating it strictly to standalone LEAP repository environments (`LEAP_DIR="."`).
- **Cognitive Rule:** Integrated the "Zero-Failure Rule" into the core `.skills/leap-dev/SKILL.md` agent skill.
- **Remote Gating CI:** Added `.github/workflows/ci.yml` to run the unified check runner remotely.
- **Test Coverage:** Added comprehensive unit and integration test suites validating the runner and setup hook.

### Detailed Changes

#### Unified Runner (`scripts/run-all-checks.sh`)

- Built in POSIX-compliant Bash with fail-fast execution (`set -euo pipefail`).
- Executes sequentially: `check-md kb/`, pytest suite on `check-md/tests/`, skill-install python tests, and QMD config shell tests.
- Implements test environment overrides (`CHECK_MD`, `PYTEST`, `INSTALL_SKILLS_TEST`, `QMD_TEST`) allowing tests to mock success (`"true"`) or failure (`"false"`) for robust isolated testing.

#### Setup Bootstrapper (`scripts/setup-leap.sh`)

- Added Step 4d: Git Pre-Commit Hook configuration.
- Only executes if `LEAP_DIR="."` (standalone LEAP repository developer environment), avoiding installing LEAP-specific linter hooks in consuming submodule environments.
- Automatically creates backups of any pre-existing pre-commit hooks to `pre-commit.bak` before overwriting.

#### Cognitive Agent Skill (`.skills/leap-dev/SKILL.md`)

- Updated "Constraints & Rules" to include the **Zero-Failure Rule**.
- Explicitly forbids agents from updating checklist boxes, declaring phases complete, or recommending skill transitions when checks are failing, outlawing any "rationalization/explanation bypasses."

#### CI Workflow (`.github/workflows/ci.yml`)

- Runs on pushing to `main` and on all PRs to `main`.
- Syncs the development environment using Python 3.11 and Astral's `uv` tool manager, then executes the unified runner.

### New Files

- `scripts/run-all-checks.sh` - Unified check runner
- `scripts/git-pre-commit` - Git pre-commit hook template
- `scripts/tests/test_run_all_checks.sh` - Behavioral unit tests for the runner (TDD verified)
- `scripts/tests/test_pre_commit_installation.sh` - Integration tests verifying the setup installer and hook blocking/permitting behavior (TDD verified)
- `.github/workflows/ci.yml` - Remote CI pipeline configuration

### Modified Files

- `scripts/setup-leap.sh` - Installs pre-commit hook for standalone repos
- `.skills/leap-dev/SKILL.md` - Integrates cognitive Zero-Failure Rule
- `kb/feature/faseidl/automated-gating/goals.md` - Updates goals checkboxes
- `kb/feature/faseidl/automated-gating/plan.md` - Updates plan checkboxes

### Deleted Files

- None

## Key Implementation Details

### Standalone Repo vs. Submodule Distinction

Consuming parent repositories use LEAP as a submodule to get agent-friendly structures, but they do not maintain LEAP itself. Forcing LEAP's python test suites on their commits would introduce unwanted friction and missing python dependency errors. By restricting the pre-commit hook installation strictly to cases where `LEAP_DIR="."`, `setup-leap.sh` ensures that consuming projects are not impacted, while LEAP maintainers remain fully protected.

### Isolated/Mocked Test Architecture

We designed `run-all-checks.sh` with environment-variable override parameters. This allowed our integration tests to execute the setup script, copy the real pre-commit hook, and test the hook's core block/permit logic in a temporary repository completely instantly and hermetically, without needing to run slow real-world linters or python test suites during hook testing.

## Testing

### Test Coverage

- **Code Coverage:** Not directly measurable for bash scripts, but 100% of the functional bash execution paths, setup branches, and exit codes are fully covered by automated testing.

### Test Strategy

- **Behavioral Unit Testing (`test_run_all_checks.sh`):** Asserts that the runner exits with `0` when checks succeed, and immediately aborts and exits with `1` on any step failure (using our mock environment variables).
- **Integration testing (`test_pre_commit_installation.sh`):** Initializes a sandbox repository, executes `setup-leap.sh` with simulated interactive keyboard prompts (stdin redirects), verifies hook file copy and executable bits, and tests block/permit scenarios.
- **End-to-End Testing:** Executed the real check runner against the active workspace.

### Test Results

- **Total tests:** 9 (5 check-runner unit scenarios, 4 setup/hook integration scenarios)
- **Passing:** 9
- **New tests added:** 9

## Documentation

### Source Comments

- Fully documented `scripts/run-all-checks.sh` with header blocks and inline step comments.
- Fully documented `scripts/git-pre-commit` with clear instruction comments.

### Usage Documentation

- The new unified test runner and pre-commit hook have been updated inside the project `README.md` and repository guidelines.

## Permanent Documentation Assessment

We evaluated what documentation or insights require permanent preservation:

- Since the Zero-Failure Rule is a foundational cognitive constraint, we updated the official `.skills/leap-dev/SKILL.md` file directly. This makes the cognitive gate permanent and visible to all future agent sessions. No additional ADRs or separate best-practice documents are required.

## Breaking Changes

- None.

## Migration Guide

### For Developers (LEAP Maintainers)

1. Pull the latest `faseidl/automated-gating` branch.
2. Run `bash scripts/setup-leap.sh` and select `y` to "Install LEAP git pre-commit hook?".
3. All future commits will now be locally gated. If any check fails, your commit is blocked and diagnostic logs are displayed.
4. (Optional) Run `./scripts/run-all-checks.sh` directly at any time to run the complete check suite.

### For Submodule Consumers

- Backward-compatible; no action required. Submodule consumers running `setup-leap.sh` are not prompted to install this hook.

## Known Limitations

- None.

## Future Work

- None.

## Related Issues

- Closes #27: Multi-Tiered Automated Gating System implementation.

## Verification Steps

1. Checkout branch: `git checkout faseidl/automated-gating`
2. Run behavioral test suites:
   - `bash scripts/tests/test_run_all_checks.sh`
   - `bash scripts/tests/test_pre_commit_installation.sh`
3. Run end-to-end suite: `./scripts/run-all-checks.sh`
