# ISO 8601 Date Formatting Standardization Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-27

---

## Quick Summary

Standardize all date formatting in the LEAP methodology to the ISO 8601 standard (`YYYY-MM-DD`) across templates, standards documentation, and setup scripts, establishing a new ADR (`leap-adr-003`) and referencing it from the existing standards ADR (`leap-adr-002`).

## Executive Summary

This feature implements the proposal from GitHub Issue #37. Currently, LEAP documentation templates and scripts use inconsistent date formatting or vague placeholders (such as `[Date]`). This inconsistency leads to variation in how dates are populated, creating noise in git diffs, regional ambiguity (e.g., DD/MM vs. MM/DD), and reducing machine parseability.

To maintain the integrity of our architectural decision records, we will not modify the accepted `leap-adr-002` in-place for this new standard. Instead, we will draft a brand-new architectural decision record: `leap-adr-003__standardize-date-formatting.md`. We will then add a non-substantive update/pointer in `leap-adr-002` referencing this new standard.

All 11 knowledge base template files will be updated to use the standardized `[YYYY-MM-DD]` placeholder format, and our automated workspace scripts will be updated to generate complying dates.

## Risk and Complexity Assessment

**Overall Risk:** LOW

**Overall Complexity:** LOW

This is a straightforward, high-impact standardization task with minimal risk of system disruption.

## Objectives

1. **Establish New ADR:** Draft and accept `kb/adr/leap-adr-003__standardize-date-formatting.md` to formally ratify the ISO 8601 standard for all LEAP-compliant documentation.
2. **Update Templates:** Update all `kb/template-*.md` files to use the standardized placeholder: `[YYYY-MM-DD]`.
3. **Reference in ADR 002:** Add a non-substantive reference pointer in `kb/adr/leap-adr-002__markdown-formatting-standards.md` to cross-reference the new decision.
4. **Automate Script Generation:** Update scripts (like `scripts/setup-leap.sh`) to generate dates using conforming shell patterns (`$(date "+%Y-%m-%d")`).

## Requirements

### Functional Requirements

- **REQ-1:** Create and document the new architectural decision `kb/adr/leap-adr-003__standardize-date-formatting.md` defining the ISO 8601 date standard.
- **REQ-2:** Update `kb/adr/leap-adr-002__markdown-formatting-standards.md` with a clean update pointer pointing to the new standard.
- **REQ-3:** All files matching `kb/template-*.md` that contain date placeholders must be updated to use the standardized `[YYYY-MM-DD]` placeholder format.
- **REQ-4:** `scripts/setup-leap.sh` (and any other setup or feature creation scripts) must be updated to output generated dates strictly in `YYYY-MM-DD` format.
- **REQ-5:** The `check-md` linter must continue to pass cleanly across all templates and edited files.

### Non-Functional Requirements

- **Consistency:** Every template placeholder for a date or timestamp should adhere to the `[YYYY-MM-DD]` pattern.
- **Portability:** Date generation in scripts must be portable across different POSIX-compliant environments (including macOS and Linux).

### Testing Requirements

- **Template Verification:** Check that templates compile and are properly validated by `check-md`.
- **Script Verification:** Run script tests or manually verify that `scripts/setup-leap.sh` generates headers with correctly formatted dates.

### Documentation Requirements

- Formalize the ISO 8601 requirement in `kb/adr/leap-adr-003__standardize-date-formatting.md`.

## Success Criteria

- [ ] ADR `kb/adr/leap-adr-003__standardize-date-formatting.md` is drafted and accepted.
- [ ] All `kb/template-*.md` files use the standardized `[YYYY-MM-DD]` placeholder.
- [ ] `kb/adr/leap-adr-002__markdown-formatting-standards.md` is updated with a non-substantive pointer to the new ADR 003.
- [ ] Automated setup scripts output dates strictly in `YYYY-MM-DD` format.
- [ ] `check-md` runs and passes successfully on all modified files.

## Constraints

- Changes must be backward-compatible with any existing markdown parsing toolchains.

## Assumptions

- Standardizing placeholders in templates is fully supported by all IDEs and current workflow scripts.

## Out of Scope

- Retroactively converting existing historical dates in older documentation (beyond templates, guides, and active features), unless easily automated or naturally updated.
- **check-md Rule Addition (Future Enhancement):** Implementing an automated `check-md` linter rule that validates `Date` metadata fields against the `YYYY-MM-DD` format and auto-corrects them with `--fix`. This will be recorded as a future enhancement request in a separate issue.
