# Configurable LEAP User Goals

**Author:** AI CLI Agent<br>
**Date:** 2026-09-02

---

## Quick Summary

Make the compliance directory username configurable via environment variables or git config in `pin-leap.sh` and prompt for it during setup in `setup-leap.sh` to prevent mismatches between OS usernames and project conventions.

## Executive Summary

Currently, `pin-leap.sh` derives the per-user compliance directory name under `kb/feature/` solely from the OS login name. In environments like this repository where the LEAP username is `faseidl` but the local machine username is `fseidl`, this mismatch results in work being split across two separate folders (`kb/feature/faseidl/` and `kb/feature/fseidl/`). A similar issue occurs in CI/CD environments (which typically run as `root` or `runner`) and on shared corporate-imaged machines.

This feature addresses the issue by introducing a clear resolution hierarchy for configuring the LEAP user:

1. `LEAP_USER` environment variable.
2. `git config leap.user` configuration value.
3. Current fallback behavior: `$USER` -> `id -un` -> `whoami` -> `developer`.

Additionally, `setup-leap.sh` will prompt for this username and write it to `git config leap.user` at setup time, guessing an appropriate default from existing `kb/feature/` subdirectories if they exist.

## Risk and Complexity Assessment

**Overall Risk:** LOW

**Overall Complexity:** LOW

## Objectives

1. Enable explicit configuration of the LEAP username to map compliance directories to agreed-upon project usernames.
2. Maintain compatibility with the existing derivation mechanism as a fallback.
3. Integrate configuration into `setup-leap.sh` to prompt and configure `git config leap.user` automatically.
4. Normalize and sanitize the configured username to guarantee safe directory paths.

## Requirements

### Functional Requirements

- **REQ-1:** In `scripts/pin-leap.sh`, resolve the LEAP username using the following prioritized hierarchy:
  1. `LEAP_USER` environment variable.
  2. `git config --get leap.user` configuration value (local or global).
  3. Existing OS login-based fallback logic (`USER` -> `id -un` -> `whoami` -> `developer`).
- **REQ-2:** Normalize and sanitize the resolved username by converting it to lowercase and removing any characters that are not lowercase alphanumeric, `.`, `_`, or `-` (to match existing directory naming safety).
- **REQ-3:** Update `scripts/setup-leap.sh` to prompt the user for their LEAP username (used for feature directories and branch names) during setup, suggesting a default value.
- **REQ-4:** In `scripts/setup-leap.sh`, search existing subdirectories of `kb/feature/` (excluding generic names or non-user folders if applicable) to propose the most likely default username for the prompt.
- **REQ-5:** Save the user's input/selected username in local git configuration via `git config leap.user "<username>"` during `scripts/setup-leap.sh`.
- **REQ-6:** Support automated/headless execution of `scripts/setup-leap.sh` (e.g., via flags or env vars) without blocking on the interactive prompt.

### Non-Functional Requirements

- **Portability:** Shell scripts must remain compatible across Darwin/macOS, Linux, and Windows (Git Bash/MSYS2).
- **Maintainability:** Ensure code added to bash scripts is clean, commented, and uses existing error handling or logging conventions.

### Testing Requirements

- Verify the username resolution hierarchy in automated shell assertion tests (e.g., `scripts/tests/pin-leap.test.sh` and/or `scripts/tests/test_setup_flags.sh`).
- Test that sanitization correctly normalizes names containing uppercase letters, spaces, and special characters.
- Test that mock environments (empty `USER`, mock `git config`) are handled correctly and fall back to "developer" when all else is missing.

### Documentation Requirements

- Document the new configuration options (`LEAP_USER` and `git config leap.user`) in relevant guide/README files if applicable.
- Add comments explaining the resolution order and sanitization steps in the shell scripts.

## Success Criteria

- [x] `pin-leap.sh` successfully resolves username using the hierarchical lookup (LEAP_USER > git config > OS fallbacks).
- [x] `setup-leap.sh` correctly prompts for the username, offers a smart default based on existing `kb/feature/` folders, and writes it to `git config leap.user`.
- [x] Sanitization works identically across all sources, ensuring only clean and safe directory/file paths are created.
- [x] All updated and new automated tests pass.

## Constraints

- Must not introduce any external binary dependencies. Must use standard POSIX shell tools or Git commands.

## Assumptions

- Git is installed and configured on the developer machine where these scripts are run.
- The project follows the `kb/feature/<username>/` directory convention.

## Out of Scope

- Integrating other config managers or remote configuration sync.
- Automated creation of remote folders or Git branch renaming.
