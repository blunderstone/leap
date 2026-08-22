# GitHub-Based LEAP Proposals Workflow Completion Summary

**Branch:** `feature/faseidl/github-issues-proposals`<br>
**Base Branch:** `main`<br>
**Date:** 2026-08-22<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

---

## Overview

We have successfully modernized the LEAP methodology's change proposal and defect reporting workflows. 

By decommissioning the antiquated, file-based proposal register and manual serial-numbering (`PROP-nnn`) system, we have transitioned the project into a modern, public, and open-source appropriate workflow. All proposals and bugs are now tracked dynamically using native GitHub Issues on the main repository (`blunderstone/leap`).

---

## What Changed

### High-Level Summary

- **Decommissioned Legacy File-Based Register**: Overwrote the local proposal registry in `kb/guide-improvement-proposals.md`, removing legacy active/historical registers and sequential numbering tables.
- **Created Public GitHub Templates**: Authored two distinct, highly polished GitHub issue templates with 100% visible, editor-agnostic square-bracket instruction placeholders:
  1. **Bug Report / Defect Template** (`bug-report.md`): Focuses on low-friction, empirical reproduction details, removing irrelevant metadata questions.
  2. **LEAP Improvement Proposal Template** (`leap-improvement-proposal.md`): Guides the contributor through structured methodology thinking (Context, Current State, Proposed Change, Benefits, Drawbacks, and optional Alternatives).
- **Purged Legacy Terminology**: Conducted a thorough codebase sweep and completely purged all references to the legacy internal serial-numbering convention (`PROP-nnn`), including its glossary definition in the methodology guide.
- **Updated Cross-Document References**: Updated internal links across global LEAP manuals to point to the new, modernized issue-based processes.

### Detailed Changes

#### Issue Templates (.github/ISSUE_TEMPLATE/)
- Created `.github/ISSUE_TEMPLATE/leap-improvement-proposal.md` with core LIP fields and visible square bracket placeholders.
- Created `.github/ISSUE_TEMPLATE/bug-report.md` focusing strictly on reproduction details, simplified environments, and visible square bracket placeholders.

#### Knowledge Base (kb/)
- Modernized `kb/guide-improvement-proposals.md` into an instructions-only guide describing how to submit issues and guidelines for writing high-quality proposals.
- Updated `kb/guide-compliance-levels.md` to change the legacy `PROP-001` link to point to `template-goals.md` directly.
- Updated `kb/guide-methodology.md` to rewrite the "LEAP Governance and Evolution" section (describing GitHub templates, community feedback, and labels) and removed the legacy `PROP-NNN` glossary entry.
- Completed all objectives and checked off success criteria in `kb/feature/faseidl/github-issues-proposals/goals.md` and `kb/feature/faseidl/github-issues-proposals/plan.md`.

---

## Technical Decisions

### Visible Placeholders vs HTML Comments
Replacing standard HTML comment wrappers (`<!-- -->`) with visible text in square brackets (`[Instruction text]`) prevents instruction text from being hidden in rich Markdown/WYSIWYG preview editors. This ensures helpers remain completely visible to users regardless of their chosen Markdown authoring tool.

### Separating Bugs and LIPs
Splitting bugs (empirical, reproduction-focused, minimal metadata) from proposals (structural, trade-off analysis, architectural design) minimizes user friction for issues while maintaining high technical rigor for proposed methodology changes.

---

## Testing

### Test Coverage
- **Markdown Compliance:** 100% of the modified and newly created markdown files pass the local `check-md` linter with zero violations.
- **Link Auditing:** All updated relative hyperlinks and remote repository links have been verified as correct.
