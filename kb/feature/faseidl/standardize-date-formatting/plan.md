# ISO 8601 Date Formatting Standardization Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-27

---

## Overview

We will standardize all date formatting in the LEAP repository to the ISO 8601 format (`YYYY-MM-DD`). To do this safely and maintain architectural decision integrity, we will follow a two-phase implementation approach.

**Development Approach:** We will apply incremental verification at each step. Every modified template and markdown file will be verified using the local `check-md` linter to ensure that no violations or syntax issues are introduced.

### Overall Assessment

- **Complexity:** LOW - The changes are structural, template-based, and straightforward documentation edits.
- **Risk:** LOW - No application logic is modified, ensuring zero chance of operational runtime regression.

---

## Phase 1: ADR, References, and Template Standardization

### Goals

1. Draft and publish the new architectural decision record: `kb/adr/leap-adr-003__standardize-date-formatting.md`.
2. Update the existing `kb/adr/leap-adr-002__markdown-formatting-standards.md` with a non-substantive update pointing to `leap-adr-003`.
3. Standardize all 11 documentation template files (`kb/template-*.md`) to use the `[YYYY-MM-DD]` placeholder format instead of `[Date]`.

### Approach

- **Step 1:** Create `kb/adr/leap-adr-003__standardize-date-formatting.md` adhering to the standard template (`kb/template-adr.md`) and setting the status to `accepted`.
- **Step 2:** Edit `kb/adr/leap-adr-002__markdown-formatting-standards.md` to append an update reference near the beginning or the "Reference: Document Header Template" section.
- **Step 3:** Systematically edit all 11 template files (`kb/template-*.md`) to replace `[Date]` (and variations) with `[YYYY-MM-DD]`.

### Testing

- Validate all edited files by running `check-md` specifically on the modified files to ensure 100% compliance.
- Run `git diff` to manually verify surgical edit accuracy.

### Success Criteria

- [x] `kb/adr/leap-adr-003__standardize-date-formatting.md` is successfully created with `accepted` status.
- [x] `kb/adr/leap-adr-002__markdown-formatting-standards.md` is updated with a non-substantive update pointer to ADR 003.
- [x] All 11 `kb/template-*.md` files are standardized with `[YYYY-MM-DD]` placeholders.
- [x] All updated files pass `check-md` cleanly with no violations.

**Rationale:** Establishing the architectural decision first creates the formal policy context for the subsequent template modifications.

---

## Phase 2: Script Validation & Automated Date Linter Enhancement Issue

### Goals

1. Verify and ensure that all automated scripts (such as `scripts/pin-leap.sh` and `scripts/setup-leap.sh`) output dates in the standard `YYYY-MM-DD` format.
2. Verify that running the feature creation/setup workflow results in correctly formatted dates.
3. **Formally File the GitHub Issue:** File a new issue directly in GitHub for adding an automated date linter rule to `check-md` so that the enhancement idea is permanently captured and tracked in the issue backlog.

### Approach

- **Step 1:** Audit `scripts/pin-leap.sh` and verify that `CURRENT_DATE=$(date "+%Y-%m-%d")` is correctly set and used.
- **Step 2:** Review `scripts/setup-leap.sh` and make sure it does not generate non-compliant dates on project initialization.
- **Step 3:** Create the detailed issue draft for the `check-md` automated date linter rule (covering validation constraints for metadata fields like Date, Updated, Created, and the behavior of `--fix` auto-correction) and file it directly on GitHub.

### Testing

- Execute `pin-leap.sh` or run script integration tests to confirm date-generation compliance.
- Run `pytest` on `check-md` tests to ensure no regressions.

### Success Criteria

- [x] Portability of `date "+%Y-%m-%d"` in scripts is verified.
- [x] The automated date-validation rule issue is successfully filed on GitHub.
- [x] All workspace tests and validation checks pass cleanly.

**Rationale:** Adding automated script checks and filing formal GitHub issues for tool enhancements ensures that standards are systematically enforced and future improvements are transparently tracked.

---

## Risk Mitigation

No high-risk items identified. Standard version control branches provide quick rollback capability if needed.

## Decision Points

### After Phase 1

- Proceed to Phase 2 once all templates are updated, validated by `check-md`, and committed.

### After Phase 2

- Complete the feature branch and prepare the final handoff/completion summary.
