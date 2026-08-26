---
name: leap-pr
description: Reads completion-summary.md and drafts a reviewer-friendly PR description (pr-description.md).
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

  - name: pr_title
    type: string
    description: Optional custom title for the Pull Request. If omitted, dynamically generated from the feature's title.
    required: false

  - name: draft
    type: boolean
    description: Whether to create the Pull Request as a draft (default is true)
    required: false

---

# Skill: LEAP PR Description Drafter & Submitter

## Context & Purpose

This skill guides AI coding agents in drafting clear, reviewer-focused Pull Request descriptions and programmatically creating PRs under the **[Literate (Extended-by-Agent) Programming (LEAP) Methodology](../../kb/guide-methodology.md)**. 

### PR Body Flexibility:

- **`pr-description.md` is OPTIONAL:** A dedicated `pr-description.md` file is not strictly required. For small-to-medium features, you should advise using the contents of `completion-summary.md` directly as the PR body to maximize efficiency.
- **When to create `pr-description.md`:** For large, complex features where `completion-summary.md` contains extensive implementation details that might overwhelm reviewers, you must draft `pr-description.md` as a concise summary of the completion summary.
- **PR Body Content:** In any case, the final body of the Pull Request submitted to GitHub must contain either the `completion-summary.md` or the `pr-description.md` contents.

## Trigger Conditions

- The user asks to prepare a Pull Request, prepare a commit, or write the PR description (e.g., "draft our PR description", "prepare the branch for PR", or `/leap-pr`).

## Operational Workflow

1. **Verify Committed Completion Summary (Prerequisite):** Verify that the completed and approved `completion-summary.md` has been successfully compiled, finalized, and committed to Git inside `kb/feature/<username>/<feature-name>/`. You must never run this skill on an uncommitted completion summary, as the PR needs to link to tracked, immutable branch histories.
2. **Draft PR Summary (Optional):** Discuss with the developer if they want to use `completion-summary.md` directly (recommended for small-to-medium branches) or draft a dedicated `pr-description.md` (recommended for large branches). If drafting:
   - Create `kb/feature/<username>/<feature-name>/pr-description.md` using the canonical template (`kb/template-pr-description.md`). 
   - Read the committed `completion-summary.md` to extract the overview, key changes, testing outcomes, and breaking changes.
   - **Carry Over Metadata & Issue Closures:** Ensure that `pr-description.md` carries forward the exact same metadata as the completion summary (branch, base branch, etc.) and **critically, all GitHub issue closing keywords (such as "Closes #12" or "Fixes #12")**. Since GitHub/GitLab parse the PR body itself to trigger auto-closures, these references must reside in the final PR description to function.
   - Run `check-md` to ensure `pr-description.md` meets repository linter standards.
3. **Determine PR Title & Draft Options:**
   - **Dynamic PR Title Generation:** Do not use the last commit message or a generic placeholder. Instead, generate an intelligent, descriptive title by reading the primary H1 heading of `completion-summary.md` (or `goals.md`). Extract the core feature description, strip words like "Completion Summary" or "Goals", convert the description to lowercase, and prefix it with an appropriate conventional commit prefix (e.g., `feat(workflow): <feature-description>`, `fix(api): <feature-description>`). Always present this generated title to the user for confirmation or editing. If `pr_title` is supplied as a parameter, use it directly.
   - **Draft Mode Choice:** Ask the developer whether they want to submit the Pull Request as a **Draft** or as **Ready for Review**. If the `draft` parameter is explicitly provided, respect it.
4. **Offer Programmatic PR Creation:** Offer to create the Pull Request on behalf of the developer:

   - **Check for GitHub CLI (`gh`):** Check if the GitHub CLI is installed and authenticated (`which gh` and `gh auth status`).
   - **Programmatic PR:** If `gh` is available, offer to execute `gh pr create` using either the committed `completion-summary.md` or `pr-description.md` as the body file:
     ```bash
     # Example command (as draft)
     gh pr create --title "<approved-title>" --body-file kb/feature/<user>/<feature>/completion-summary.md --draft

     # Example command (ready for review)
     gh pr create --title "<approved-title>" --body-file kb/feature/<user>/<feature>/completion-summary.md
     ```

   - **Manual Fallback:** If `gh` is not available, push the branch (`git push -u origin <branch>`) and print a pre-filled Git push command and a direct link to open the browser PR creation page.

## Constraints & Rules

- **Mandatory Turn Gating (No Jumping Ahead):**
  - **Two-Step Submission Process:** You are strictly prohibited from generating the PR title, drafting the description, and executing a branch push or `gh pr create` in a single conversation turn. This is a mandatory hard gate.
  - **No Unilateral Pushing/Submission:** On the first turn of this skill, you must ONLY draft the `pr-description.md` (if requested), generate the proposed conventional PR title, and present them along with the programmatic PR options. You MUST STOP and wait for the developer to review and approve the title and settings before executing `git push` or `gh pr create`.
  - **Approval Required to Submit:** You may only execute the branch push or programmatically create the Pull Request on a subsequent turn AFTER the user has explicitly reviewed and approved your proposed title, description, and submission settings.
- **Reviewer-Focused:** If drafting `pr-description.md`, keep it focused, high-signal, and concise. Refer reviewers to `completion-summary.md` for deep implementation details.
- **Issue-Closing Porting Mandate:** If drafting `pr-description.md`, you must ensure any issue-closing keywords from `completion-summary.md` are carried forward into the PR description body so they are parsed and auto-closed on merge.
- **Committed Prerequisite:** You must confirm that `completion-summary.md` is fully tracked and committed in Git before drafting `pr-description.md`. If it is uncommitted, you must halt and instruct the developer to run `leap-finish` or commit the summary first.
- **Linter Compliance:** If created, `pr-description.md` must pass `check-md` cleanly with zero violations.
- **No Code or Feature Edits:** You are strictly forbidden from writing or modifying any source code, running build/test commands, or editing any existing feature branch documents (such as `goals.md` or `plan.md`) under this skill. It is strictly a review documentation generator.
- **End of Lifecycle:** Once the PR is drafted and submitted (either programmatically or via browser link), your work is complete. Explicitly congratulate the developer, present the PR URL, and celebrate!

## Output Schema / Format

Upon successful execution, print a summary in the following structure:

```
[leap-pr] Pull Request Preparation Complete!

- Summary Mode: [e.g., Using completion-summary.md directly / Drafted pr-description.md]
- PR Title: <approved-title>
- Submission Mode: [Draft / Ready for Review]
- Markdown Validation: PASSED (check-md ran cleanly)

==> Programmatic PR Option:
I detected that the GitHub CLI (gh) is [available/not available]. 
Would you like me to push this branch and programmatically create the PR as a [draft / standard pull request] for you?
```
