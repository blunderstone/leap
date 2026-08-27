# Submodule Pinning Utility Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-27

---

## Quick Summary

Provide a dedicated, easy-to-use shell script (`pin-leap.sh`) alongside the existing `setup-leap.sh` that allows consuming repositories to easily pin their LEAP submodule to a specific release tag, commit, or branch.

## Executive Summary

When a repository consumes LEAP as a git submodule, updating or pinning the submodule reference can be a manual, error-prone task. Developers need to ensure they have a clean working directory, checkout a new feature branch (specifically adhering to LEAP conventions), fetch the tags, checkout the submodule at the target pin, and commit the submodule pointer change.

This feature delivers a self-contained shell script `pin-leap.sh` located in the `scripts/` directory of the LEAP repo (which will be accessible under `leap/scripts/pin-leap.sh` in the consuming repo). This utility automates the branch creation, tag fetching, submodule checking out, and staging of changes—wrapping the process in a clean, interactive, and robust bash script.

## Risk and Complexity Assessment

**Overall Risk:** LOW

**Overall Complexity:** LOW

## Objectives

1. Automate the process of updating/pinning a LEAP submodule inside a consuming repository.
2. Ensure safety by verifying the host repository has a clean working tree before initiating any branch or submodule state changes.
3. Automatically create a standardized LEAP-compliant feature/chore branch (e.g., `chore/pin-leap-vX.Y.Z` or `faseidl/pin-leap-vX.Y.Z`) to isolate the pinning change.
4. Keep the LEAP workspace skill-space clean by delivering this low-frequency utility as a script rather than an agent skill.

## Requirements

### Functional Requirements

- **REQ-1 (Workspace Validation):** The script must check if it is being run from the root of a consuming repository containing a LEAP submodule.
- **REQ-2 (Working Tree Safeguard):** The script must check if the working tree is clean. If there are uncommitted/unstaged changes, it must fail safely with an explanatory message.
- **REQ-3 (Target Version Input):** The script must accept the target release/tag/commit as a command-line argument, or prompt the user interactively if omitted.
- **REQ-4 (Auto-Branching):** The script must automatically create and switch to a new branch named `chore/pin-leap-<version>` (or similar customizable prefix matching LEAP standards) starting from the current base branch.
- **REQ-5 (Submodule Checkout):** The script must navigate to the submodule directory, fetch latest tags, checkout the requested tag/commit, and return to the parent repo.
- **REQ-6 (Staging & Commit Guidance):** The script must automatically stage the submodule change (`git add leap`) and either commit it with a compliant message (`chore(deps): pin LEAP submodule to <version>`) or guide the developer on how to do so.
- **REQ-7 (Latest Tag Resolution):** The script must support resolving `"latest"` to the newest stable semantic version tag (and fall back gracefully to pre-releases if no stable releases exist), clearly printing the resolved tag before proceeding.
- **REQ-8 (Setup Documentation):** Add clear instructions on how to use `pin-leap.sh` to pin the submodule to `kb/guide-installation.md` and `README.md`, ensuring consumers have direct documentation on how to perform updates.
- **REQ-9 (LEAP Level 1 Compliance):** To ensure the pinning change adheres to LEAP practices inside the consuming repository, the script must automatically initialize and populate a LEAP Compliance Level 1 feature directory structure (e.g., `kb/feature/pin-leap-<version>/`), generating both a pre-populated `goals.md` and `completion-summary.md` file.

### Non-Functional Requirements

- **Compatibility:** The script must run on macOS (darwin) and Linux. It must use POSIX-compliant syntax or standard bash features compatible with macOS's default bash and standard Linux shells.
- **User Experience (UX):** Use ANSI colors for terminal feedback and output clear error messages with exit codes on failures.

### Testing Requirements

- Write a comprehensive automated test script (e.g., `scripts/tests/pin-leap.test.sh`) that simulates a parent repository with a nested LEAP submodule and verifies:
  - Detection of dirty working tree.
  - Successful checkout and creation of the `chore/` feature branch.
  - Correct checking out of the specified tag/commit within the mock submodule.
  - Staging and/or committing of the submodule pointer.

### Documentation Requirements

- Document the usage of `pin-leap.sh` in the repository's `README.md` and/or `kb/guide-installation.md`.
- Provide inline commentary in `pin-leap.sh` explaining complex or git-specific operations.

## Success Criteria

- [x] Command-line script `scripts/pin-leap.sh` is fully implemented and executable.
- [x] Script successfully rejects execution on dirty working directories.
- [x] Script automatically creates a standard `chore/pin-leap-<target>` branch and pins the submodule to the requested release tag.
- [x] Comprehensive shell-based test suite (`scripts/tests/pin-leap.test.sh`) is written and passes cleanly.
- [x] Documentation is updated to include the new pinning procedure.

## Constraints

- Must be delivered as a shell script in the `scripts/` directory to avoid bloating the agent skill space.
- Must not assume a specific directory name for the submodule (it might be `leap/`, but should fallback dynamically).

## Assumptions

- The consuming repository has the LEAP repo configured as a Git submodule.
- Git is installed and available on the user's system PATH.

## Out of Scope

- Upgrading other submodules or dependencies other than the LEAP submodule itself.
- Automatically pushing the branch to remote servers (leaves push action to user discretion).
