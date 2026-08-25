# Open Source Readiness and Agent Instructions Prep Completion Summary

**Branch:** `faseidl/open-source-readiness-prep`<br>
**Base Branch:** `main`<br>
**Date:** 2026-08-24<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

---

## Overview

In preparation for the public open-source launch of the LEAP repository, we have completed a comprehensive sanitization of outdated license/branding positioning, established clear guidelines for Markdown cross-referencing and hyperlinked GitHub issues, swept the repository for broken cross-document links, and updated the interactive setup configurations (`setup-leap.sh` and root-level `GEMINI.md`) to deliver a modern, skill-aware onboarding experience for incoming AI agents.

This work ensures that the repository is 100% ready for the open-source release under the Apache-2.0 license, while hard-locking and optimizing the behavior of incoming AI coding assistants to maintain documentation quality, practice progressive testing, and respect sequential phase-boundary gating.

---

## What Changed

### High-Level Summary

- **Purged Defunct Branding Positioning (REQ-1):** Swept the repository and verified the complete removal of obsolete references to "Source-Available" or "Community Scale License," ensuring consistent marketing of LEAP as a standard **Open Source** project under the Apache-2.0 license.
- **Enforced Hyperlinked GitHub Issues (REQ-3):** Created a brand-new "Hyperlink & Issue Referencing Standards" guideline section in `kb/best-practices-markdown.md` that mandates the explicit hyperlinking of all GitHub issue references (e.g. `[#14](https://github.com/blunderstone/leap/issues/14)`) and discourages fragile anchors.
- **Conducted a Hyperlink Integrity Sweep & Repair (REQ-5):**
  - Removed the emoji `⚖️` from the "Contribution Licensing Agreement" heading in `CONTRIBUTING.md` to establish a stable, clean anchor name.
  - Repaired the broken "Contributing Guide" link in the root `README.md` to point to `CONTRIBUTING.md#contribution-licensing-agreement-implicit-cla`.
  - Repaired a broken link in `kb/guide-methodology.md` pointing to the non-existent `markdown_formatting_best_practice.md`, directing it to the correct, existing file `best-practices-markdown.md`.
  - Repaired multiple broken links in `kb/best-practices-tdd.md` pointing to the non-existent `best-practices-testing.md`, redirecting developers to the core testing requirements section in `guide-methodology.md`.
  - Cleared several defunct/non-existent links in the "Related Documentation" section of `kb/best-practices-markdown.md` (such as `guide-markdown-quality-onboarding.md` and `metrics-markdown-quality-baseline.txt`).
- **Refined AI Agent Instructions (REQ-2 & REQ-4):**
  - Updated templates in `scripts/setup-leap.sh` (`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursorrules`) and the root-level `GEMINI.md` to inform incoming agents that `check-md` is globally runnable, promote specialized LEAP workspace skills (e.g., `leap-start`, `leap-dev`) as the preferred pathway, and provide concise, fallback gating summaries for phase-boundary checks when skills are not utilized.

### Detailed Changes

#### scripts/setup-leap.sh

- Updated `write_claude()`, `write_gemini()`, `write_copilot()`, and `write_cursor()` heredoc templates to incorporate global `check-md` runnable instructions, promote the specialized workspace skills, and define fallback phase-gating guides.

#### GEMINI.md

- Added an "AI Workspace Skills & Phase Gating" section to align root conventions with the updated configurator, promoting the workspace skills and listing concise fallback gating rules.
- Capitalized the formatting language name "Markdown."

#### kb/best-practices-markdown.md

- Added a new `## Hyperlink & Issue Referencing Standards` section.
- Added explicit rules for hyperlinking GitHub issues and avoiding fragile heading anchors with emojis.
- Cleaned the `## Related Documentation` list, removing broken links to `guide-markdown-quality-onboarding.md` and `metrics-markdown-quality-baseline.txt` and replacing them with existing active guides.

#### kb/best-practices-tdd.md

- Removed references and links to the non-existent `best-practices-testing.md` file.
- Redirected developers to the core validation and testing requirements section in `guide-methodology.md`.
- Converted step checklists into clean quality guideline bullet points.

#### kb/guide-methodology.md

- Corrected the broken link `markdown_formatting_best_practice.md` to `best-practices-markdown.md`.

#### CONTRIBUTING.md

- Removed the emoji `⚖️` from the licensing heading to create the stable, emoji-free anchor `#contribution-licensing-agreement-implicit-cla`.

#### README.md

- Corrected the Contributing Guide hyperlink to use the new stable anchor.

### New Files

- `kb/feature/faseidl/open-source-readiness-prep/goals.md` - APPROVED goals specifications.
- `kb/feature/faseidl/open-source-readiness-prep/plan.md` - APPROVED implementation plan.
- `kb/feature/faseidl/open-source-readiness-prep/completion-summary.md` - This completion summary report.

### Modified Files

- `CONTRIBUTING.md`
- `README.md`
- `GEMINI.md`
- `scripts/setup-leap.sh`
- `kb/best-practices-markdown.md`
- `kb/best-practices-tdd.md`
- `kb/guide-methodology.md`
- `.github/ISSUE_TEMPLATE/bug-report.md`
- `.github/ISSUE_TEMPLATE/leap-improvement-proposal.md`

---

## Key Implementation Details

### Eliminating Fragile Emoji Heading Anchors

Markdown heading anchors generated by different parsers (GitHub, launchd, IDEs) handle emojis very inconsistently (often stripping them, percent-encoding them, or ignoring them). We established a standard in `kb/best-practices-markdown.md` to avoid emojis in headers that are cross-referenced, and proactively removed the emoji from `CONTRIBUTING.md`'s header to resolve the broken Contributing Guide link in `README.md`.

### Promoting Specialized LEAP Skills in Agent Files

To keep agent-instruction files lean and prevent token-bloat, we refactored all agent heredocs in `scripts/setup-leap.sh` and root-level `GEMINI.md` to point directly to our specialized `/leap-*` skills as the preferred path. For agents or workflows where skills are not active, we provided a highly condensed fallback summary of the core LEAP workflow (Documentation-First, Sequential Gating, TDD Rigor), eliminating redundant instructions.

---

## Testing

### Test Coverage

All modified core python code in `check-md` and workspace scripts maintains its existing test coverage.

- `check-md` linter coverage: 84% (over 1020+ lines of code)
- `install-skills` unit tests: 100% success
- `QMD config` shell test scenarios: 48 passed, 100% success

### Test Strategy

- Ran `check-md` over every modified and newly created Markdown file in the workspace to verify 100% compliance.
- Ran the `scripts/tests/test_pre_commit_installation.sh` and `test_run_all_checks.sh` suites to verify that `setup-leap.sh` changes are syntax-clean, stable, and generate output files exactly matching our refined templates.
- Executed the global quality gating script `scripts/run-all-checks.sh` to confirm zero regressions across all repository components.

### Test Results

- Total unit/pytest tests: 268 (all passed)
- Total shell test scenarios: 48 (all passed)
- Total linter check: 58 Markdown files checked (all passed cleanly, zero violations)

---

## Permanent Documentation Assessment

We assessed all insights developed during this feature to ensure they are preserved permanently in the knowledge base:

- **Markdown Cross-Referencing Best Practices:** These have been integrated directly into `kb/best-practices-markdown.md` as permanent guidelines.
- **Agent Skill & Gating Integration Guidelines:** These have been codified permanently in `scripts/setup-leap.sh` templates and root-level `GEMINI.md`.
- No temporary/ephemeral insights were left untracked.

---

## Breaking Changes

None. All modifications are fully backward-compatible.

---

## Migration Guide

No action required. Submodule integrations will receive these updates on their next git pull and can run `setup-leap.sh` to update their agent guidelines.

---

## Known Limitations

None.

---

## Future Work

None. All requirements in `goals.md` are completely met.

---

## Related Issues

- Related to general open-source launch preparations, specifically optimizing agent onboarding instructions and setup scripts.

---

## Verification Steps

To verify that these changes are correct and function flawlessly:

1. Run the Markdown linter:
   ```bash
   check-md kb/ && check-md *.md
   ```

2. Run the full gating test suites:
   ```bash
   bash scripts/run-all-checks.sh
   ```

3. Run the interactive setup script tests:
   ```bash
   bash scripts/tests/test_pre_commit_installation.sh
   ```
