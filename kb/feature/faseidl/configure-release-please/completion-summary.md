# Configure release-please for LEAP Documentation & Methodology Completion Summary

**Branch:** `faseidl/configure-release-please`<br>
**Base Branch:** `main`<br>
**Date:** 2026-08-28<br>
**Author:** [Andy Seidl](https://github.com/faseidl)

---

## Overview

LEAP is a Literate Programming framework where structured Markdown documents (such as ADRs, templates, and guides under `kb/`) serve as primary, release-worthy deliverables rather than simple auxiliary files. Our standard `release-please` setup previously only tracked standard code prefixes like `feat(...)` and `fix(...)` for version bumping and release note generation, completely filtering out other conventional commit types.

To integrate non-code deliverables seamlessly into our automated release cycles, we customized `release-please-config.json` to recognize `docs` and `refactor` commit types as release-worthy sections in generated changelogs. Furthermore, we updated developer conventions in `GEMINI.md` to specify the precise usage of release-triggering prefixes (e.g., `feat(kb):`, `feat(templates):`) versus non-releasing ones (e.g., raw `docs:`, and strict formatting policies for ephemeral directory drafts under `kb/feature/` to prevent accidental releases).

## What Changed

### High-Level Summary

- Configured `release-please` to display custom changelog sections.
- Documented guidelines for conventional commit prefixes within `GEMINI.md`.
- Established strict naming policies for commits to ephemeral `kb/feature/` subdirectories.

### Detailed Changes

#### Release Please Configuration

- Updated `release-please-config.json` to map `docs` and `refactor` commit types to custom headings: `"Documentation Standards & Guides"` and `"Refactoring & Cleanup"`.

#### Developer Guidelines

- Appended `Conventional Commit Guidelines` section to `GEMINI.md`, detailing release-triggering versus non-triggering prefixes and rules for ephemeral drafting files.

### New Files

- `kb/feature/faseidl/configure-release-please/completion-summary.md` - Complete summary of the feature implementation, technical decisions, and gating compliance.

### Modified Files

- `release-please-config.json` - Custom `changelog-sections` array added under root package.
- `GEMINI.md` - Added "Conventional Commit Guidelines" detailing commit prefixes and ephemeral drafting rules.

### Deleted Files

None.

## Key Implementation Details

### Custom Changelog Mapping

Defining a custom `changelog-sections` array overrides standard defaults. This ensures that when releases are prepared, the generated `CHANGELOG.md` correctly exposes `docs` commits as "Documentation Standards & Guides" and `refactor` commits as "Refactoring & Cleanup".

### Scope-Based Release Triggering

While `release-please` natively restricts automated version bumps and release triggering to `feat` and `fix` prefixes, developers can use these prefixes on documentation files to represent deliverable features (e.g., `feat(kb): add ADR-003`). General typos or repository README updates must use `docs(...)` or `docs:` which do not trigger releases but appear in the documentation section of the next release changelog.

## Testing

### Test Coverage

This is a configuration and documentation feature that does not modify application code. Therefore, standard code coverage does not apply (TDD Exception).

### Test Strategy

- **JSON Validation:** Verified `release-please-config.json` syntax using Python's JSON parser.
- **Markdown Validation:** Verified `GEMINI.md` and feature branch files using `check-md`.

### Test Results

- `python3 -m json.tool release-please-config.json` -> `JSON is valid`
- `check-md GEMINI.md` -> `✓ No violations found`
- `check-md kb/feature/faseidl/configure-release-please/` -> `✓ No violations found`

## Documentation

### Implementation Documentation

- `GEMINI.md` - Updated to establish conventional commit standards for the repository.

### Source Comments

- Not applicable (no application source code modified).

## Permanent Documentation Assessment

### Assessment Questions

- **Did we learn something valuable about the technology or domain?**

  - Yes: we documented custom `changelog-sections` format mapping for `release-please`.

- **Did we make an architectural decision that should be recorded?**

  - No: this aligns with existing ADRs and standard `release-please` schema capabilities.

- **Did we discover a best practice worth sharing?**

  - Yes: using scoped prefixes (`feat(kb):`, `feat(templates):`) vs raw `docs:` is a best practice for Literate Programming. This has been permanently documented in the repository guidelines (`GEMINI.md`).

- **Is there technical debt that needs tracking?**

  - No.

- **Did we create implementation documentation that applies beyond this feature?**

  - Yes: the commit prefix conventions in `GEMINI.md` apply repo-wide to all future features and development.

### Documentation Preserved

- Appended Conventional Commit Guidelines permanently to `GEMINI.md`.

## Breaking Changes

None.

## Migration Guide

No action required.

## Known Limitations

None.

## Future Work

None.

## Performance Impact

None.

## Related Issues

None.

## Verification Steps

1. Checkout branch `faseidl/configure-release-please`.

2. Confirm `release-please-config.json` is syntactically valid JSON:

   ```bash
   python3 -m json.tool release-please-config.json
   ```

3. Run `check-md` to verify markdown files:

   ```bash
   check-md GEMINI.md
   check-md kb/feature/faseidl/configure-release-please/
   ```
