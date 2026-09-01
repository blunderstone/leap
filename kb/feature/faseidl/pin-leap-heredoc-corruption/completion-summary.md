# Fix pin-leap.sh Heredoc Corruption and Path Nesting Completion Summary

**Branch:** `faseidl/pin-leap-heredoc-corruption`<br>
**Base Branch:** `main`<br>
**Date:** 2026-08-31<br>
**Author:** [faseidl](https://github.com/faseidl)

---

## Overview

The `scripts/pin-leap.sh` utility automates pinning the LEAP submodule in parent repositories and generating Level 1 compliance documentation (`goals.md` and `completion-summary.md`). However, it previously suffered from template corruption because it generated documents using unquoted heredocs (`cat <<EOF`), causing Bash to interpret inline markdown backticks as command substitutions. This resulted in empty/corrupted strings and a wall of silent terminal warnings. Furthermore, the base branch resolution crashed under `set -o pipefail` on local repositories without remotes, and the generated documents were placed directly under `kb/feature/` rather than nesting them under the developer's username folder per LEAP taxonomic conventions.

This change successfully resolves all these issues using a robust, function-based quoted heredoc (`cat <<'EOF'`) and `sed` pipeline strategy. It also safely handles dynamic base branch queries under `pipefail`, and nests generated compliance documents under a clean lowercase system username folder (e.g., `kb/feature/<username>/pin-leap-<version>/`).

## What Changed

### High-Level Summary

- **Heredoc & Backtick Preservation**: Encapsulated the template bodies within dedicated shell functions using quoted heredocs (`cat <<'EOF'`) to prevent evaluation of markdown backticks, piping the results through `sed` for safe placeholder interpolation.
- **Robust Base Branch Queries**: Handled `set -o pipefail` cleanly during origin symbolic ref checks by appending `|| echo ""` to ensure the pipeline returns a success code in any repository setting (e.g. local-only).
- **Taxonomic Directory Nesting**: Queried and cleaned the local system user's login username (`LEAP_USER`) and nested Level 1 compliance directories inside standard `kb/feature/<username>/` subdirectories.
- **Permanent Documentation Alignment**: Updated the permanent `kb/guide-installation.md` to document the correct nested paths.
- **Automated Verification**: Exported a deterministic `USER="testuser"` mock inside the integration test suite and updated assertions to verify directory structure, backtick integrity, and dynamic custom branch resolution.

### Detailed Changes

#### CLI Pinning Script (`scripts/pin-leap.sh`)

- Added dynamic, clean lowercase username resolution using `LEAP_USER="${USER:-...}"` logic.
- Nest compliance directory structure under `kb/feature/$LEAP_USER/pin-leap-$TARGET_VERSION`.
- Replaced unquoted heredocs with `generate_goals()` and `generate_completion_summary()` helper functions.
- Integrated safe `@LEAP_USER@` template variables and added exit code checks on file generation failure.

#### Integration Tests (`scripts/tests/pin-leap.test.sh`)

- Exported `USER="testuser"` at the top of the test suite to ensure consistent, sandbox-independent compliance paths.
- Replaced hardcoded `main` checkouts with `$INITIAL_BRANCH` to make tests resilient to local git configurations.
- Added Scenarios 5 and 6 assertions to verify backticks are verbatim and directories are nested under `testuser`.
- Simulated a symbolic ref under `refs/remotes/origin/HEAD` with a mock file write and verified that it dynamically resolves the base branch (`custom-main`) on demand.

#### Installation Guide (`kb/guide-installation.md`)

- Corrected the documented compliance folder path from `kb/feature/pin-leap-<version>/` to `kb/feature/<username>/pin-leap-<version>/`.

### New Files

None.

### Modified Files

- `scripts/pin-leap.sh` - Core pinning utility script.
- `scripts/tests/pin-leap.test.sh` - Integration test suite.
- `kb/guide-installation.md` - Permanent repository installation instructions.
- `kb/feature/faseidl/pin-leap-heredoc-corruption/goals.md` - Checklist updates.
- `kb/feature/faseidl/pin-leap-heredoc-corruption/plan.md` - Checklist updates.

### Deleted Files

None.

## Key Implementation Details

### Quoted Heredoc & `sed` Pipeline

To include markdown backticks intact without triggering command substitutions, we quote the heredoc delimiter (`<<'EOF'`). Because variables are not expanded in quoted heredocs, we use `@PLACEHOLDER@` markers and pipe the heredoc stream directly through a multi-expression `sed` replacement pipeline:

```bash
generate_goals() {
  cat <<'EOF' | sed \
    -e "s|@TARGET_VERSION@|${TARGET_VERSION}|g" \
    -e "s|@CURRENT_DATE@|${CURRENT_DATE}|g" \
    -e "s|@LEAP_USER@|${LEAP_USER}|g" \
    > "$COMPLIANCE_DIR/goals.md"
...
```

### Safe Pipeline under `pipefail`

With `set -o pipefail` enabled, a pipeline's exit status is set to the value of the last command to exit with a non-zero status. When `git symbolic-ref` exits with `1` (because there is no `origin/HEAD` configured), the entire pipeline's status is set to `1`, causing the script to exit on `set -e`. We solve this by ensuring the pipeline always returns `0` via `|| echo ""`:

```bash
BASE_BRANCH=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@' || echo "")
BASE_BRANCH="${BASE_BRANCH:-main}"
```

## Testing

### Test Coverage

The integration test suite does not use coverage tools since it is written in pure Bash, but it exhaustively verifies all critical execution paths and behavioral safeguards.

### Test Strategy

- **Safe Guard Checks**: Verified non-git directories, repositories without submodules, dirty working trees, and missing `.gitmodules` files exit with code `1`.
- **Scenario Testing**: Tested specific tags (`v1.0.0`) and "latest" stable release tag resolutions.
- **Content Verification**: Asserted that generated `goals.md` and `completion-summary.md` preserve backticks, interpolate versions, dynamically resolve symbolic base branches (`custom-main`), and do not emit command execution warnings.

### Test Results

- **Total tests**: 26 assertions
- **Passing**: 26 assertions
- **New tests added**: 10 assertions (nested path checks, backtick checks, symbolic ref base branch resolution)

## Permanent Documentation Assessment

### Assessment Questions

- **Did we learn something valuable about the technology or domain?**
  Yes, we documented how `set -o pipefail` interacts with assignment pipelines containing failing git queries, and how quoted heredocs solve markdown backtick execution issues.

- **Did we make an architectural decision that should be recorded?**
  No, we aligned the existing automated utility with LEAP conventions.

- **Did we discover a best practice worth sharing?**
  Yes, mocking `origin/HEAD` with direct file writes `.git/refs/remotes/origin/HEAD` provides incredibly lightweight, offline, and zero-dependency symbolic-ref mocking for test sandboxes.

- **Is there technical debt that needs tracking?**
  None.

- **Did we create implementation documentation that applies beyond this feature?**
  No.

### Documentation Preserved

- Updated the permanent `kb/guide-installation.md` to document the username-nested compliance folder structure.

## Breaking Changes

None.

## Migration Guide

No action required.

## Known Limitations

None.

## Future Work

None.

## Related Issues

- **Closes #60**: Fixes template heredoc corruption.
- **Related**: Addresses username-nested compliance directory requirements (as identified during development).

## Verification Steps

1. Run the test suite:
   ```bash
   bash scripts/tests/pin-leap.test.sh
   ```

2. Run project validations:
   ```bash
   bash scripts/run-all-checks.sh
   ```
