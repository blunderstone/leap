# Submodule Pinning Utility Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-27

---

## Overview

This plan details the development of the LEAP Submodule Pinning Utility (`scripts/pin-leap.sh`). Following the LEAP methodology, the development process is organized into distinct, sequential, and incremental phases, utilizing Test-Driven Development (TDD) principles via an automated bash-based testing harness.

**Development Approach:** We will implement the utility in Bash. Before implementing each feature, we will construct/expand our automated testing harness (`scripts/tests/pin-leap.test.sh`) to assert the correct behavior of the script in a simulated sandbox environment containing a mock parent git repository and mock submodule.

### Overall Assessment

- **Complexity:** LOW - The script performs Git operations and standard string manipulation in Bash, which is highly straightforward.
- **Risk:** LOW - All operations are executed in local feature branches, protecting parent repositories from disruption.

---

## Phase 1: Core Script & Environment Safeguards

### Goals

1. Establish the `scripts/pin-leap.sh` script with proper execution permissions, headers, and color utilities.
2. Implement robust environment and workspace checks (verifying the parent repo has Git initialized and a LEAP submodule exists).
3. Implement a strict working-tree safeguard: fail gracefully with an explanatory message if there are uncommitted or unstaged changes.
4. Implement input argument parsing to read the target tag/commit or prompt interactively if missing.

### Approach

- Create the `scripts/pin-leap.sh` file with standard POSIX/Bash boilerplate and helper functions.
- Use `git status --porcelain` to determine if the working directory is clean.
- Read CLI arguments and prompt the user for input if no arguments are provided.

### Testing

- Create `scripts/tests/pin-leap.test.sh`, which will:
  - Bootstrap a temporary sandbox directory.
  - Simulate a non-git directory and assert that `pin-leap.sh` fails.
  - Initialize a git repo without a LEAP submodule and assert failure.
  - Initialize a git repo with a mock LEAP submodule but make the tree dirty, asserting that `pin-leap.sh` rejects execution with an exit code of 1.

### Success Criteria

- [x] Script `scripts/pin-leap.sh` is initialized.
- [x] Script rejects execution under uninitialized git trees, missing submodules, or dirty working directories.
- [x] Test harness `scripts/tests/pin-leap.test.sh` is created and successfully verifies all validation paths.

**Rationale:** Establishing environment validations and the test harness first ensures we have a stable sandbox to safely test our Git-modifying operations in the subsequent phases.

---

## Phase 2: Auto-Branching, Latest Resolution & Submodule Checkout

### Goals

1. Implement resolving the `"latest"` tag keyword to the newest stable semantic release version.
2. Implement checking out and staging of the specified LEAP release tag/commit within the submodule.
3. Implement auto-branching to switch the host repository to a standard, clean LEAP feature/chore branch (`chore/pin-leap-<version>`) before applying changes.
4. Auto-generate a LEAP Compliance Level 1 feature directory structure (e.g., `kb/feature/pin-leap-<version>/`) and pre-populate both `goals.md` and `completion-summary.md` to ensure seamless LEAP compliance.
5. Stage the updated submodule pointer and generated documents (`git add leap kb/`) and output completion guidance.

### Approach

- Implement a tag fetcher and sorter using `git tag -l "v*" --sort=-v:refname` to resolve `"latest"`. Filter out pre-releases from the default resolution unless no stable tags exist.
- Determine the submodule's actual path dynamically (allowing support for custom directory naming if any, falling back to `leap`).
- Execute `git checkout -b chore/pin-leap-<version>` inside the parent repo.
- Auto-generate `kb/feature/pin-leap-<version>/goals.md` and `kb/feature/pin-leap-<version>/completion-summary.md` inside the consuming repository using standard HEREDOC templates.
- Navigate into the submodule, checkout the target commit/tag, and return.
- Stage the changes in the parent repo (submodule reference and the feature directory) and print explicit user instructions for pushing the branch.

### Testing

- Expand the testing harness in `scripts/tests/pin-leap.test.sh` to:
  - Simulate mock release tags (`v1.0.0`, `v1.1.0-beta.0`, `v1.1.0`) in the mock remote.
  - Verify that passing `"latest"` correctly resolves to the newest stable tag (`v1.1.0`).
  - Verify that running the script successfully checks out the new branch `chore/pin-leap-<target>` in the parent.
  - Verify that the LEAP feature folder is created with `goals.md` and `completion-summary.md`.
  - Verify that the submodule reference has been updated to the expected tag.
  - Verify that the updated submodule pointer and files are staged (`git status` shows staged changes).

### Success Criteria

- [x] Script correctly resolves `"latest"` semantic version tags.
- [x] Script automatically creates a Level 1 LEAP feature folder containing pre-populated `goals.md` and `completion-summary.md`.
- [x] Script successfully checks out a clean feature/chore branch, pins the submodule, and stages the modification.
- [x] Automated tests in `scripts/tests/pin-leap.test.sh` verify the entire branching, checkout, document generation, and resolution flow.

---

## Phase 3: Setup Documentation & Final Validation

### Goals

1. Integrate the new pinning workflow into existing documentation:
   - Document pinning instructions in `kb/guide-installation.md`.
   - Update `README.md` to reference `pin-leap.sh`.
2. Perform exhaustive end-to-end manual and automated validation of the script.
3. Clean up implementation, add rich comments, and perform final linter checks.

### Approach

- Edit `kb/guide-installation.md` and `README.md` with clear instructions and examples.
- Ensure all automated tests run and pass cleanly.

### Testing

- Run the full test suite `scripts/tests/pin-leap.test.sh` in various environments to ensure complete platform coverage (macOS and Linux).
- Verify markdown formatting of modified documentation using `check-md`.

### Success Criteria

- [x] `kb/guide-installation.md` contains clear pinning instructions.
- [x] `README.md` is updated with reference to `pin-leap.sh`.
- [x] `check-md` linter passes completely without errors across the entire knowledge base.
- [x] Test harness passes 100% of test cases.
