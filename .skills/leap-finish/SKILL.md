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
   - Related GitHub issue numbers addressed or closed by this work (using standard closing keywords like "Closes #12" or "Fixes #12" in the metadata/overview section so they are automatically linked and closed when the branch merges).
   - Testing outcomes (total tests, passing tests, test coverage metrics for lines, statements, and branches).
3. **Verify Compliance:** Run `check-md` over the entire repository to ensure no markdown violations exist.
4. **Checkbox Review Gating:** Evaluate each success criterion in `goals.md` and `plan.md`. For each item, state whether it was fully met, partially met, or deferred (providing a clear, justified explanation for any deferred or partial items). Present this checklist assessment to the developer for review and seek their explicit agreement to check them off.
5. **Milestone Commit:** Once the developer approves the checklist assessment and completion summary, update the checkboxes to checked (`[x]`) on their behalf and perform a dedicated finalization commit including `completion-summary.md`, `goals.md`, and `plan.md`:
   - Commit message format: `doc(workflow): author completion summary and finalize success checkboxes`

## Constraints & Rules

- **Mandatory Turn Gating (No Jumping Ahead):**
  - **Two-Step Finalization Process:** You are strictly prohibited from compiling the `completion-summary.md` and performing the finalization git commit or checkbox updates in a single conversation turn. This is a mandatory hard gate.
  - **No Unilateral Finalization:** On the first turn of this skill, you must ONLY gather information, draft/compile the `completion-summary.md` (uncommitted), and present the checklist assessment. You MUST STOP and wait for the developer to explicitly review and approve your drafted files and checklist assessment before making any commits, staging files, or checking any checkboxes.
  - **Approval Required to Commit:** You may only proceed to stage and commit the files and update checkboxes to checked (`[x]`) on a subsequent turn AFTER the user has explicitly replied confirming their review and approval.
- **Checkbox Update Policy:** You must **NEVER** proactively check off checkboxes (`- [ ]` to `- [x]`) in `goals.md` or `plan.md` without first presenting your verification findings and obtaining explicit agreement from the developer. Once the developer has reviewed your work and confirmed agreement, you are authorized (and expected) to update the checkboxes to checked (`[x]`) on their behalf.
- **Milestone Commit Mandate:** You must stage and commit the finalized `completion-summary.md`, `goals.md`, and `plan.md` files immediately upon developer approval.
- **No Code Modifications:** You are strictly forbidden from writing, refactoring, or modifying any application source code under this skill. If any tests or linter checks fail, you must transition back to **`leap-dev`** to address them.
- **No PR Description Drafting:** You are strictly forbidden from drafting `pr-description.md` or PR-level review descriptions under this skill.
- **Transition Gate:** Once `completion-summary.md` is compiled, approved, committed, and success checkboxes are updated, your work under `leap-finish` is complete. You must explicitly direct the user to trigger the **`leap-pr`** skill (e.g., via `/leap-pr`) to draft the pull request description.

## Output Schema / Format

Upon successful execution, print a summary in the following structure:

```
[leap-finish] Successfully compiled completion-summary.md!

- Summary File: kb/feature/<username>/<feature-name>/completion-summary.md
- Markdown Validation: PASSED (check-md ran cleanly)

==> Gating Checklist Assessment:
Please review my assessment of the success criteria:
- [x] Criterion 1 (Fully met via...)
- [x] Criterion 2 (Fully met via...)
- [ ] Criterion 3 (Deferred because...)

Reply with your agreement. Once confirmed, I will automatically check off these success checkboxes in goals.md and plan.md on your behalf, and prepare you for PR drafting!
```
