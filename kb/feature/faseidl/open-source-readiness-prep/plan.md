# Open Source Readiness and Agent Instructions Prep Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-24

---

## Overview

This implementation plan details a systematic approach to cleaning up obsolete branding, updating developer instructions, enforcing hyperlinked issues in Markdown files, promoting our specialized workspace skills, and sweeping for broken cross-document links.

**Development Approach:** Since this task focuses on Markdown guidelines, agent configurations, and bash setup templates, our approach will center on manual code reviews, regex-based hyperlink audits, and testing script execution to verify generated outputs. We will run the `check-md` linter after every phase to ensure 100% compliance.

### Overall Assessment

- **Complexity:** LOW - Primarily involves text editing, Markdown guidelines, and modifying setup script heredocs.
- **Risk:** LOW - Changes are self-contained and do not modify core runtime logic of the linter or build tools.

---

## Phase 1: Brand Audit & Guideline Updates

### Goals

- Audit the repository and remove/replace any defunct references to "Source-Available" or "Community Scale License" with clean Open Source (Apache-2.0) messaging.
- Add an explicit documentation guideline in `kb/best-practices-markdown.md` stating that any mention of a GitHub issue must be formatted as an explicit hyperlink (e.g., `[#14](https://github.com/blunderstone/leap/issues/14)`).
- Perform a comprehensive audit and sweep of all internal hyperlinks across the repository's Markdown documents (such as the Contributing Guide link in `README.md`) to guarantee that all cross-references are 100% valid.

### Approach

- Search the repository for strings like `Source-Available` and `Community Scale` and replace them where applicable.
- Edit `kb/best-practices-markdown.md` to document the GitHub issue hyperlinking standard.
- Manually audit and resolve broken or fragile anchors (such as the Contribution Licensing Agreement link in `README.md` pointing to `CONTRIBUTING.md#⚖️-contribution-licensing-agreement-implicit-cla`, simplifying it to a robust link).

### Testing

- Run `check-md` over all modified files.
- Verify that updated Markdown files parse cleanly and have no broken links.

### Success Criteria

- [ ] All defunct references to "Source-Available" or "Community Scale License" purged or corrected.
- [ ] `kb/best-practices-markdown.md` successfully updated with the GitHub issue hyperlinking guideline.
- [ ] All cross-document links audited, and fragile or broken links (including the Contributing Guide link in `README.md`) resolved.
- [ ] Modified Markdown files pass `check-md kb/` linter with zero errors.

---

## Phase 2: Agent Instructions & Setup Refinement

### Goals

- Update the agent template heredocs in `scripts/setup-leap.sh` (`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursorrules`) to:
  - Inform incoming agents that `check-md` is globally installed and runnable from any subdirectory.
  - Promote the specialized LEAP `/leap-*` workspace skills (like `leap-start`, `leap-dev`, `leap-pr`, etc.) as the primary path, and provide concise fallback gating guidelines if skills are not utilized.
- Update root-level `GEMINI.md` to align with the same global linter instructions and skill-centric gating guidance.

### Approach

- Surgically edit `scripts/setup-leap.sh` to update the file-writing functions (`write_claude`, `write_gemini`, `write_copilot`, `write_cursor`).
- Edit root-level `GEMINI.md` to reflect these updates.
- Run `scripts/setup-leap.sh` locally in a test directory to verify that the generated files (`CLAUDE.md`, `GEMINI.md`, etc.) match our updated templates perfectly.

### Testing

- Execute `scripts/setup-leap.sh` to verify script syntax correctness and that it runs without errors.
- Inspect generated agent configuration files to verify correctness.

### Success Criteria

- [ ] `scripts/setup-leap.sh` templates updated with global linter instructions, LEAP skills promotion, and concise fallback gating guidelines.
- [ ] Root `GEMINI.md` updated and synchronized with the same guidance.
- [ ] Local execution of `setup-leap.sh` verified and runs cleanly.
- [ ] Modified files pass `check-md kb/` with zero errors.

---

## Phase 3: Final Verification & Compliance

### Goals

- Perform a workspace-wide linter validation to ensure 100% compliance across all 30+ Markdown files in the repository.
- Complete and compile the final feature documentation.

### Approach

- Run `check-md kb/` and `check-md *.md` to verify all documentation meets strict formatting standards.
- Draft the `completion-summary.md` detailing all changes made.
- Request final human developer review.

### Testing

- Run the full workspace test suite (`scripts/run-all-checks.sh` or similar if available) to ensure zero regressions.

### Success Criteria

- [ ] All Markdown files in the repository pass `check-md` with zero violations.
- [ ] Final `completion-summary.md` compiled and presented to the developer.
- [ ] Checkboxes in `goals.md` and `plan.md` updated to checked upon developer agreement.
- [ ] Features folder is clean and organized.

---

## Decision Points

### After Phase 1

- Proceed if the Markdown guidelines and link sweep are verified and linter checks pass.

### After Phase 2

- Proceed if `setup-leap.sh` execution is validated and generated files are verified as correct.

## Notes

- All changes will be committed by milestone at the end of each phase.
