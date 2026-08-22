# GitHub-Based LEAP Proposals Workflow Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-22

---

## Overview

This plan outlines the steps to transition LEAP's change proposal process from the legacy, local file-based register (`kb/guide-improvement-proposals.md`) to a modern, GitHub Issues-based workflow.

**Development Approach**: Follow the LEAP methodology—applying incremental updates, validating the markdown files with the `check-md` linter at each stage, and verifying all documentation hyperlinks are valid.

### Overall Assessment

- **Complexity:** LOW - Purely documentation restructuring and a GitHub configuration change.
- **Risk:** LOW - No impact on production code, linter execution, or core system behaviors.

---

## Phase 1: GitHub Issue Template Authoring

### Goals

- Create Markdown-based GitHub Issue Templates for both Bug Reports (`.github/ISSUE_TEMPLATE/bug-report.md`) and LEAP Improvement Proposals (`.github/ISSUE_TEMPLATE/leap-improvement-proposal.md`).

### Approach

- Author the issue templates following standard GitHub issue template structure.
- Pre-populate the proposal template with the core LEAP proposal fields (Context, Current State, Proposed Change, Benefits, Drawbacks, and optional Alternatives Considered).
- Pre-populate the bug report template with critical reproduction fields (Description, Steps to Reproduce, Actual Behavior, Expected Behavior, and Environment Details).
- Use visible square brackets (`[Instruction text]`) for user instructions to guarantee visibility across all Markdown editors and GitHub preview modes.
- Assign default metadata and labels (`bug` or `enhancement`).

### Testing

- Verify that the issue template formats are syntactically valid and that the files are placed correctly in the repository.

### Success Criteria

- [x] `.github/ISSUE_TEMPLATE/leap-improvement-proposal.md` and `bug-report.md` are authored, correctly formatted, and exists in the workspace.

---

## Phase 2: Modernizing the Proposals Guide

### Goals

- Redesign `kb/guide-improvement-proposals.md` to remove legacy active/historical registers and the internal Markdown template.
- Restructure the file to serve as a lean, instructions-only guide explaining how to write a good proposal and directing contributors to open an issue on GitHub.

### Approach

- Re-write `kb/guide-improvement-proposals.md` to explain the new GitHub Issues-based workflow.
- Preserve the "Guidelines for Proposals" section which remains highly valuable for quality control (e.g., Characteristics of a Good Proposal, When to Add, and When NOT to Add).
- Link directly to the GitHub Issues tracker at `https://github.com/blunderstone/leap/issues`.

### Testing

- Run the `check-md` linter on the modified `kb/guide-improvement-proposals.md` file to verify zero formatting violations.

### Success Criteria

- [x] `kb/guide-improvement-proposals.md` is complete, fully modernized, and passes `check-md` cleanly.

---

## Phase 3: Updating Global LEAP References & Validation

### Goals

- Identify and update all references to the old proposal registry across LEAP documentation files.
- Run a project-wide validation using the `check-md` linter.

### Approach

- Update references in `guide-cheatsheet.md`, `guide-compliance-levels.md`, `guide-document-taxonomy.md`, and `guide-methodology.md` to explain that LEAP improvement proposals are submitted via the repo's issue tracker rather than by editing a local file.
- Perform a thorough run of the `check-md` tool across the entire codebase to ensure total formatting and syntax compliance.

### Testing

- Execute `check-md` on the entire workspace.
- Validate that all updated internal links are correct and resolve successfully.

### Success Criteria

- [x] All cross-document references are updated to reflect the new GitHub Issues-based process.
- [x] The entire project's markdown files pass the `check-md` linter with zero violations.

---

## Decision Points

### After Phase 1

- Proceed to Phase 2 once the GitHub Issue Template is successfully created and verified.

### After Phase 2

- Proceed to Phase 3 once the proposal guide has been re-written, reviewed, and successfully linted.

---

## Notes

- The target issue template name is `.github/ISSUE_TEMPLATE/leap-improvement-proposal.md`.
- No legacy proposals need to be carried forward into the repository's files as the live issues are now tracked in GitHub under Issues #13 and #14.
