# Configurable LEAP User Completion Summary

**Branch:** `faseidl/configurable-leap-user`<br>
**Base Branch:** `main`<br>
**Date:** 2026-09-02<br>
**Author:** [AI CLI Agent](https://github.com/google/gemini-cli)

---

## Overview

Previously, the compliance directory username in `pin-leap.sh` was derived solely from the local OS login name. In environments where the developer's OS username (e.g., `fseidl`) differs from their project/GitHub handle (e.g., `faseidl`), or in CI/CD pipelines running as `root`/`runner`, this mismatch caused work to be split across different feature folders and created friction in repository synchronization.

To solve this, we introduced a highly configurable username resolution hierarchy and integrated it seamlessly into the setup flow. Developers can now explicitly configure their preferred LEAP username via the `LEAP_USER` environment variable, a local `git config leap.user` setting, or interactively during project bootstrap via `setup-leap.sh`.

## What Changed

### High-Level Summary

- **Hierarchical Username Resolution:** Added a prioritized lookup order in `scripts/pin-leap.sh` (`LEAP_USER` env var → `git config leap.user` → OS login fallback).
- **Lowercase & Path Sanitization:** Normalized all resolved usernames to lowercase alphanumeric characters, dots (`.`), underscores (`_`), and hyphens (`-`) for guaranteed path safety.
- **Smart Directory Setup Prompt:** Updated `scripts/setup-leap.sh` to detect existing directories under `kb/feature/` to propose an intelligent, context-aware default.
- **Interactive Username Config:** Prompted the developer for their handle during setup and saved the finalized, sanitized selection in local git configuration (`git config leap.user`).
- **Headless & Non-Interactive Support:** Guaranteed that non-interactive runs (CI/CD or via `--yes` / `--no` flags) do not block on prompts and resolve the correct fallback or environment overrides.

### Detailed Changes

#### scripts/pin-leap.sh

- Replaced standard `$USER`/`whoami` resolution with a fallback-aware loop checking `LEAP_USER` first, then `git config --get leap.user`, and finally OS-level login names.
- Added path normalization using `tr` and `sed` to filter safe directory characters.
- Implemented a final safety fallback to `"developer"` if sanitization yields an empty name.

#### scripts/setup-leap.sh

- Added Step 2c ("Configuring LEAP Username") right after creating the `kb/` directory.
- Implemented folder globbing of `kb/feature/*` to guess default usernames if a single folder is present.
- Added prompt support reading from file descriptor 3 (`<&3`) to preserve interactive keyboard input when standard input is piped.
- Programmed automatic configuration saving to local `.git/config` using `git config leap.user`.

#### Test Suites

- **scripts/tests/pin-leap.test.sh**:
  - Added **Scenario 7** (resolves from `LEAP_USER` env var).
  - Added **Scenario 8** (resolves from `git config leap.user`).
  - Added **Scenario 9** (tests uppercase normalization and character-stripping sanitization).
  - Added **Scenario 10** (tests ultimate fallback to `"developer"` when OS user commands fail and environment is stripped).
- **scripts/tests/test_setup_flags.sh**:
  - Added **Test 6** (non-interactive configuration via `LEAP_USER` env var).
  - Added **Test 7** (smart folder detection from existing features).
  - Added **Test 8** (interactive prompts with custom inputs and pipelining).

### New Files

None.

### Modified Files

- `scripts/pin-leap.sh` - Username resolution hierarchy, sanitization, and fallback.
- `scripts/setup-leap.sh` - Step 2c interactive prompt, folder scanning, and config saving.
- `scripts/tests/pin-leap.test.sh` - Added 4 failing/passing scenarios for TDD.
- `scripts/tests/test_setup_flags.sh` - Added 3 failing/passing tests for TDD.

### Deleted Files

None.

## Key Implementation Details

### Smart Default Directory Fallback
During setup, `setup-leap.sh` scans the subdirectories under `kb/feature/`. If exactly one user-specific directory exists (e.g. `faseidl`), it proposes that folder name as the default username. This is highly effective for teams onboarding new developers onto existing checkouts, as the script automatically aligns with the active developer's existing workspace foldering.

### FD 3 Keyboard Prompts
To handle piped execution (e.g. piping default configurations into `setup-leap.sh`), the interactive username prompt reads from file descriptor 3 (`<&3`), which setup-leap duplicates from the original stdin at startup (`exec 3<&0`). This prevents piped streams from consuming the interactive username prompt and allows robust CLI user-input handling.

## Testing

### Test Strategy

- **Unit Testing (TDD):** Created rigorous red-green unit tests prior to implementation.
- **Integration Validation:** Executed the entire repository test pipeline to verify that all related tools (`check-md`, `pytest`, `qmd-config`, and custom skills) operate perfectly with zero regressions.

### Test Results

- **Total workspace tests executed:** 58 (34 in `pin-leap.test.sh` and 24 in `test_setup_flags.sh`).
- **Passing tests:** 58.
- **New tests added:** 7 comprehensive scenarios.

## Documentation

- Explanatory inline comments were added to both `pin-leap.sh` and `setup-leap.sh` detailing the resolution order and sanitization rules.

## Permanent Documentation Assessment

### Assessment Questions

- **Did we learn something valuable about the technology or domain?** No.
- **Did we make an architectural decision that should be recorded?** No, the changes follow existing patterns.
- **Did we discover a best practice worth sharing?** Yes, utilizing FD 3 duplication to handle keyboard prompts under input pipes is a useful bash pattern, but is standard for setup-leap.sh and does not require a new ADR.
- **Is there technical debt that needs tracking?** No.
- **Did we create implementation documentation that applies beyond this feature?** No.

### Documentation Preserved

None - feature implementation was straightforward with no novel insights requiring permanent preservation.

## Breaking Changes

None. All fallbacks preserve backward compatibility 100% with existing OS-based usernames.

## Related Issues

- Closes #71: pin-leap.sh: make the compliance directory username configurable instead of deriving it from $USER
