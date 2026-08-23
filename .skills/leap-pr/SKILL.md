---
name: leap-pr
description: Reads completion-summary.md and drafts a reviewer-friendly PR description (pr-description.md).
version: 1.0.0
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

# Skill: LEAP PR Description Drafter

## Context & Purpose

This skill guides AI coding agents in drafting clear, reviewer-focused Pull Request descriptions under the **[Literate (Extended-by-Agent) Programming (LEAP) Methodology](../../kb/guide-methodology.md)**. Because detailed changes are already recorded in the feature branch's `completion-summary.md`, the PR description is kept highly concise, highlighting what reviewer focus areas and verification steps are needed.

## Trigger Conditions

- The user asks to prepare a Pull Request, prepare a commit, or write the PR description (e.g., "draft our PR description", "prepare the branch for PR", or `/leap-pr`).

## Operational Workflow

1. **Verify Completion Summary:** Ensure `completion-summary.md` has been successfully compiled and reviewed in `kb/feature/<username>/<feature-name>/`.
2. **Draft PR Description:** Create `kb/feature/<username>/<feature-name>/pr-description.md` using the canonical template (`kb/template-pr-description.md`). Read the compiled `completion-summary.md` to extract:
   - Summary of PR (2-3 sentences explaining what and why).
   - Key changes (3-5 bullet points of high-impact changes).
   - Testing outcomes (coverage percentages).
   - Breaking changes list.
   - Specific review focus areas.
   - Concrete instructions on how a reviewer can locally check out, build, and verify the changes.
3. **Verify Compliance:** Run `check-md` to ensure the generated document meets repository linter standards.

## Constraints & Rules

- **Reviewer-Focused:** Keep this document focused, high-signal, and concise. Do not duplicate the extensive details of `completion-summary.md`. Refer reviewers to the completion summary for deep implementation details.
- **Linter Compliance:** The compiled `pr-description.md` must pass `check-md` cleanly with zero violations.
- **No Code or Feature Edits:** You are strictly forbidden from writing or modifying any source code, running build/test commands, or editing any existing feature branch documents (such as `goals.md` or `plan.md`) under this skill. It is strictly a review documentation generator.
- **End of Lifecycle:** Once `pr-description.md` is compiled and approved, your work is complete. Explicitly congratulate the developer, present the PR description, and tell them they are fully prepared to commit, push, and submit their PR!

## Output Schema / Format

Upon successful execution, print a summary in the following structure:

```
[leap-pr] Successfully drafted PR description!

- PR Description File: kb/feature/<username>/<feature-name>/pr-description.md
- Markdown Validation: PASSED (check-md ran cleanly)

==> Ready for Review:
Please review the drafted pr-description.md. You can copy its contents directly into your GitHub or GitLab Pull Request form!
```
