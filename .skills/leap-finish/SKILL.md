---
name: leap-finish
description: Guides agents in finalizing a feature, compiling the completion-summary.md, and requesting final linter/gating reviews.
version: 1.1.0
parameters:

  - name: feature_name
    type: string
    description: Name of the active feature folder
    required: true

  - name: username
    type: string
    description: GitHub/author username
    required: true

---

# Skill: LEAP Feature Finisher

## Context & Purpose

This skill guides AI coding agents in closing out an active development task in accordance with the **[Literate (Extended-by-Agent) Programming (LEAP) Methodology](../../kb/guide-methodology.md)**. It ensures all changes, technical decisions, architectural shifts, and verification outcomes (test coverage, linting) are comprehensively documented in the feature's `completion-summary.md` before finalization.

## Trigger Conditions

- The user indicates that they have finished implementing and testing the feature and are ready to merge or close the branch (e.g., "we are done, write the completion summary", "conclude this branch", or `/leap-finish`).

## Operational Workflow

1. **Information Gathering:** Analyze the git history, `git status`, modified files, added tests, and test results.
2. **Draft Completion Summary:** Create `kb/feature/<username>/<feature-name>/completion-summary.md` by populating the canonical template (`kb/template-completion-summary.md`). Ensure you document:
   - High-level and detailed code changes.
   - Files added, modified, or deleted.
   - Key implementation decisions and architectural changes.
   - Testing outcomes (total tests, passing tests, test coverage metrics for lines, statements, and branches).
3. **Verify Compliance:** Run `check-md` over the entire repository to ensure no markdown violations exist.
4. **Checkbox Review Gating:** Present the list of success criteria checkboxes from `goals.md` to the user. **Explicitly remind the user that marking checkboxes complete is a human-aligned action**, and ask them to verify and mark the checkboxes as complete in `goals.md` and `plan.md`.

## Constraints & Rules

- **Gating Mandate:** You must **NEVER** modify or check off incomplete checkboxes (`- [ ]`) in any goals or plan files yourself. Marking checkboxes complete is a **human-aligned** action requiring developer review first.
- **No Code Modifications:** You are strictly forbidden from writing, refactoring, or modifying any application source code under this skill. If any tests or linter checks fail, you must transition back to **`leap-dev`** to address them.
- **No PR Description Drafting:** You are strictly forbidden from drafting `pr-description.md` or PR-level review descriptions under this skill.
- **Transition Gate:** Once `completion-summary.md` is compiled, approved, and all checkboxes are manually checked off by the developer, your work under `leap-finish` is complete. You must explicitly direct the user to trigger the **`leap-pr`** skill (e.g., via `/leap-pr`) to draft the pull request description.

## Output Schema / Format

Upon successful execution, print a summary in the following structure:

```
[leap-finish] Successfully compiled completion-summary.md!

- Summary File: kb/feature/<username>/<feature-name>/completion-summary.md
- Markdown Validation: PASSED (check-md ran cleanly)

==> Gating Checklist Verification:
Please open goals.md and plan.md, review the implemented behavior, and manually mark the success criteria checkboxes as complete (- [x]). 

Once you have verified and checked off all items, reply to this message to authorize finalization of this branch!
```
