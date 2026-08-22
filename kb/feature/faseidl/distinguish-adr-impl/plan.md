# Distinguish ADRs from Implementation Documents Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-22

---

## Overview

This plan outlines the steps to integrate clear boundaries between Architecture Decision Records (ADRs) and descriptive implementation guides within the LEAP methodology.

**Development Approach:** Follow the LEAP methodology—applying incremental updates, validating the markdown files with the `check-md` linter at each stage, and verifying all documentation hyperlinks are valid.

### Overall Assessment

- **Complexity:** LOW - Documentation restructuring and template refinement.
- **Risk:** LOW - No impact on code behavior or build execution.

---

## Phase 1: Update the Taxonomy Guide

### Goals

- Integrate the four-question decision test, the splitting rule, the maintenance rule, and remediation guidance into `kb/guide-document-taxonomy.md`.

### Approach

- Open `kb/guide-document-taxonomy.md` and navigate to the `### Architecture Decision Records (ADRs)` section around line 145.
- Insert the new subsection `#### Choosing Between an ADR and an Implementation Document` right after the main ADR description and naming guidelines.
- Author the four decision questions with clear, descriptive explanations.
- Author the splitting rule and the maintenance rule clearly.
- Include the remediation guidelines for legacy ADRs.

### Testing

- Run the `check-md` linter on `kb/guide-document-taxonomy.md` to ensure zero formatting errors or broken links.

### Success Criteria

- [x] New guidelines successfully written into `kb/guide-document-taxonomy.md` and passes `check-md` cleanly.

---

## Phase 2: Refine the ADR Template

### Goals

- Update `kb/template-adr.md` to incorporate the pre-write gate, list disallowed sections, adjust the status workflow, and remove the mutable checklist from the migration section.

### Approach

- Open `kb/template-adr.md` and locate the `### Migration Strategy` section.
- Remove the `#### Migration Checklist` subsection and its task boxes entirely.
- Add a note in `### Migration Strategy` that task-by-task execution tracking belongs in feature docs/issues rather than the ADR.
- Locate the `### ADR Status Workflow` section in template guidance and add text clarifying that `accepted` means "this is established policy", removing the need to track implementation completion inside the ADR.
- Locate the `### Writing Tips` section and prepend the **Pre-Write Gate** and **No Living/Implementation Content** rules.

### Testing

- Run the `check-md` linter on `kb/template-adr.md` to verify zero violations.

### Success Criteria

- [x] `kb/template-adr.md` updated and passes `check-md` cleanly.

---

## Phase 3: Link ADR-001 Policy

### Goals

- Point `kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md` to the canonical definitions in the taxonomy guide to avoid duplicating the guidelines.

### Approach

- Open `kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md`.
- Locate the `## Note: Understanding ADRs vs Other Documentation` section.
- Add a new subsection `### Choosing and Remediation Guidance` with a relative hyperlink pointing to the new subsection in `kb/guide-document-taxonomy.md`.

### Testing

- Run the `check-md` linter to verify zero formatting violations.

### Success Criteria

- [x] Reference pointer added in `kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md` and passes `check-md` cleanly.

---

## Phase 4: Project-wide Validation

### Goals

- Validate the entire workspace's markdown files using `check-md` to ensure no regressions were introduced.

### Approach

- Run `uv run -m check_md check` on the root workspace.

### Success Criteria

- [x] All markdown documents in the workspace pass the `check-md` linter with zero errors.

---

## Decision Points

### After Phase 1

- Proceed to Phase 2 once the taxonomy updates are verified and pass local checks.

### After Phase 2

- Proceed to Phase 3 once the template changes are verified and pass local checks.

---

## Notes

- Keep all changes self-contained and highly focused on the specific boundaries defined in GitHub Issue #14.
