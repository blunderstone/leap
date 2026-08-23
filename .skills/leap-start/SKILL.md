---
name: leap-start
description: Automates starting a new LEAP feature branch, creating feature folder, drafting goals.md, and establishing strict milestone/TDD commit guidelines.
version: 1.1.0
parameters:

  - name: feature_name
    type: string
    description: Name of the feature branch (e.g., custom-skill-loader)
    required: true

  - name: username
    type: string
    description: GitHub/author username
    required: true

---

# Skill: LEAP Feature Starter

## Context & Purpose

This skill guides AI coding agents in launching new work in a unified, standard manner under the **[Literate (Extended-by-Agent) Programming (LEAP) Methodology](../../kb/guide-methodology.md)**. It ensures the environment, feature branches, feature directories, and requirements documentation (`goals.md`) are bootstrapped according to repository standards before implementation code is written, and sets up a highly disciplined TDD and milestone-based git commit strategy.

## Trigger Conditions

- The user asks to start a new feature, bug fix, or chore (e.g., "let's start a new feature for X", "create a feature branch for Y", or `/leap-start`).

## Operational Workflow

1. **Verify Branch State:** Ensure the working directory is clean. Check out the latest base branch (usually `main`) and pull updates.
2. **Checkout Branch:** Create and switch to the new feature branch:
   - Branch format: `<username>/<feature-name>` (e.g., `faseidl/skill-staging-infrastructure`).
3. **Initialize Feature Directory:** Create the feature branch folder in the knowledge base:
   - Path: `kb/feature/<username>/<feature-name>/`
4. **Draft Goals Document:** Create `kb/feature/<username>/<feature-name>/goals.md` by populating the canonical template (`kb/template-goals.md`). Fill out all relevant details (Quick Summary, Objectives, Functional and Non-Functional Requirements, Testing Requirements, Success Criteria).
5. **Gating Pause (Goals Milestone):** Present the drafted `goals.md` to the user and **stop and wait for their explicit review and approval**. Once approved, perform a dedicated commit:
   - Commit message: `feat(workflow): establish goals for <feature-name>`
6. **Draft Plan Document:** Populating the canonical template (`kb/template-plan.md`), draft `plan.md` in the feature directory, clearly breaking the implementation down into incremental phases.
7. **Gating Pause (Plan Milestone):** Present the drafted `plan.md` to the user and **stop and wait for their explicit review and approval**. Once approved, perform a dedicated commit:
   - Commit message: `feat(workflow): establish implementation plan for <feature-name>`

## Constraints & Rules

### Strict Gating & Milestones

- **No Early Coding:** You must **NEVER** write implementation code or modify existing source files until `goals.md` and `plan.md` are drafted, reviewed, approved, and committed individually.
- **Milestone Commits:** You must check in and commit at every major milestone:
  1. Commit `goals.md` once approved.
  2. Commit `plan.md` once approved.
  3. Commit at the end of each implementation phase specified in the plan (once the phase's success criteria are met, tested, and reviewed by the user).

### Test-Driven Development (TDD) Mandate

- **No Implementation Under This Skill:** You are strictly forbidden from writing or modifying any application source code, running build/test commands, or performing implementation work under the `leap-start` skill.
- **Explicit Transition Gate:** Once `plan.md` is drafted, approved, and committed, your work under `leap-start` is fully complete. You must explicitly halt and direct the user to transition to the **`leap-dev`** skill (e.g., via `/leap-dev Phase 1`) to start implementation. Do not write a single line of feature code under this skill.

### Checklist Policy

- **Review and Self-Check:** While checkboxes are checked by you during finalization, you should **NEVER** check a box until you have manually run tests/linters, verified the criteria is 100% satisfied, and obtained developer confirmation. Checkboxes are modified only *after* human review and explicit alignment.

## Output Schema / Format

Upon successful initiation, print a summary in the following structure:

```
[leap-start] Successfully bootstrapped new feature branch!

- Branch Created: <username>/<feature-name>
- Directory Created: kb/feature/<username>/<feature-name>/
- Goals Drafted: kb/feature/<username>/<feature-name>/goals.md

==> Action Required: Please review the goals.md file. Reply with your approval to proceed to Phase B (Implementation & Testing Plan).
```
