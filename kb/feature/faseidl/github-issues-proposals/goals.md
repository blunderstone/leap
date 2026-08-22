# GitHub-Based LEAP Proposals Workflow Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-22

---

## Quick Summary

Transition the LEAP Improvement Proposal process from the legacy, file-based `kb/guide-improvement-proposals.md` registry to a modern, GitHub Issues-based workflow. This eliminates the need to maintain an internal proposal file registry and leverages native GitHub capabilities (such as issue templates, labels, and tracking) for public, open-source contribution.

---

## Executive Summary

LEAP was originally developed as an internal, team-centric methodology where changes and proposals were recorded locally in `kb/guide-improvement-proposals.md`. Now that LEAP has been extracted into its own public, open-source repository (`blunderstone/leap`), managing proposals as local markdown edits in a shared file is antiquated. It introduces friction and merge conflicts.

This feature will decommission the file-based proposal register, establish a new GitHub Issue template (`.github/ISSUE_TEMPLATE/leap-improvement-proposal.md`) on GitHub, and rewrite `kb/guide-improvement-proposals.md` to serve as an onboarding guide directing contributors to use GitHub Issues for all proposed methodology changes.

---

## Objectives

1. Decommission the file-based register inside `kb/guide-improvement-proposals.md` while preserving quality guidelines for what makes a good proposal.
2. Author GitHub Issue Templates for both Bug Reports (`.github/ISSUE_TEMPLATE/bug-report.md`) and LEAP Improvement Proposals (`.github/ISSUE_TEMPLATE/leap-improvement-proposal.md`) containing clear, user-friendly square-bracket placeholder instructions.
3. Update all internal LEAP documentation references (such as in methodology guides, compliance documents, and cheatsheets) to point to the new GitHub Issues-based workflow.

---

## Requirements

### Functional Requirements

- **REQ-1**: Create a Markdown-based GitHub Issue Template under `.github/ISSUE_TEMPLATE/leap-improvement-proposal.md` configured with appropriate default titles, descriptions, and labels.
- **REQ-2**: Redesign `kb/guide-improvement-proposals.md` to remove legacy active/historical proposal registers and templates. It must describe the new workflow and link to the GitHub repository's issue tracker.
- **REQ-3**: Update any references in existing `kb/` guides (`guide-cheatsheet.md`, `guide-compliance-levels.md`, `guide-document-taxonomy.md`, and `guide-methodology.md`) to reflect that LEAP is now open-source and that proposals are submitted directly as GitHub Issues.
- **REQ-4**: Create a Markdown-based GitHub Issue Template under `.github/ISSUE_TEMPLATE/bug-report.md` configured with default titles, descriptions, and the `bug` label to capture high-quality empirical bug reproductions.

### Non-Functional Requirements

- All Markdown documents must strictly conform to the five `check-md` rules.
- Ensure all hyperlinks between `README.md`, `guide-improvement-proposals.md`, and other guides are correct and robust.

### Testing Requirements

- The modified and newly introduced Markdown files must successfully pass the local `check-md` linter with zero violations.
- Verify that newly introduced issue templates render correctly and adhere to GitHub's issue template structure.

### Documentation Requirements

- Maintain the same high-signal, direct, and professional tone used throughout the LEAP codebase.
- Provide clear instructions for external contributors on how to draft proposals on GitHub.

---

## Success Criteria

- [x] GitHub Issue Templates for both Bug Reports and LEAP Improvement Proposals authored and verified.
- [x] `kb/guide-improvement-proposals.md` modernized into an instructions-only guide.
- [x] References in other `kb/` documents updated and verified.
- [x] All modified files pass `check-md` with 0 violations.

---

## Constraints

- Must use only vanilla Markdown conforming to the linter's standards.

---

## Assumptions

- The repository will continue to be hosted on GitHub under `blunderstone/leap`.

---

## Out of Scope

- Implementing the proposed changes themselves; this feature only standardizes the *process* of how proposals are made.
