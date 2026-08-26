# Sequential Phase Gating Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** August 24, 2026

---

## Quick Summary

Enforce explicit sequential phase-by-phase gating and turn-gating constraints across the `leap-dev`, `leap-finish`, and `leap-pr` skills, as well as the core LEAP methodology, to prevent AI agents from "jumping ahead" or making unilateral commits/PRs without human review.

## Executive Summary

During the development of previous features and as documented in GitHub Issue #23, a critical "agent jumping-ahead" vulnerability was identified. When agents have large token budgets or trigger "TDD Exceptions" (for non-functional tasks like documentation, styling, and configuration updates), they often bypass the natural halt-and-wait gates. Instead of pausing at the boundary of a requested phase, they proceed to implement multiple phases sequentially in a single turn.

Furthermore, this systemic jumping-ahead bug extends to feature finalization:

1. Under **`leap-finish`**, agents frequently compile the completion summary, assess success criteria, run linters, and perform the finalization git commit all in a single conversation turn—denying the developer any opportunity to review the documentation before it is committed.
2. Under **`leap-pr`**, agents often draft the description, generate the title, and immediately push the branch and programmatically submit the Pull Request without waiting for the user to confirm the details.

To solve this, we will introduce explicit, strict "Sequential Phase Gating" and "Mandatory Turn Gating" negative constraints into both the canonical LEAP methodology documentation (`kb/guide-methodology.md`) and the relevant skill instructions (`leap-dev`, `leap-finish`, and `leap-pr`). This ensures that each planned phase, finalization step, and PR submission is treated as an isolated, atomic unit of work requiring its own distinct user turn, review, and approval.

## Risk and Complexity Assessment

**Overall Risk:** LOW

This is a workflow, prompt, and documentation-only feature that does not modify application source code. There is zero risk of runtime software regression, but it heavily enhances human-in-the-loop control and alignment.

**Overall Complexity:** LOW

The changes are localized to `.skills/` instruction markdown files and `kb/guide-methodology.md`.

## Objectives

1. Prevent AI agents from executing multiple implementation phases of a plan in a single turn/session under `leap-dev`.
2. Eradicate the loophole where non-functional "TDD Exception" phases bypass halt-and-wait gates.
3. Prevent AI agents from compiling, auditing, and committing feature finalizations in a single turn under `leap-finish`.
4. Prevent AI agents from drafting, title-generating, and pushing/submitting PRs in a single turn under `leap-pr`.
5. Formally document and standardize these AI agent gating mandates in the LEAP methodology documentation (`kb/guide-methodology.md`).
6. Propagate all updated skills to active agent rule directories using the installation infrastructure.

## Requirements

### Functional Requirements

- **REQ-1 (leap-dev Update):** Update `.skills/leap-dev/SKILL.md` to:
  - Add a strict constraint prohibiting multi-phase execution in a single turn.
  - Require a mandatory pause and wait for approval at the end of every phase, including those executed under TDD Exceptions.
  - Enforce separate, dedicated commits per phase.
- **REQ-2 (leap-finish Update):** Update `.skills/leap-finish/SKILL.md` to:
  - Add a strict two-step finalization process.
  - Explicitly prohibit compiling the completion summary and executing the finalization git commit/checkbox updates in the same turn.
- **REQ-3 (leap-pr Update):** Update `.skills/leap-pr/SKILL.md` to:
  - Add a strict two-step PR submission workflow.
  - Explicitly prohibit running `git push` or `gh pr create` in the first turn of the skill without waiting for user confirmation on the title, summary mode, and PR draft status.
- **REQ-4 (Methodology Update):** Update `kb/guide-methodology.md` under "Gating Mandates for AI Agents" to add comprehensive documentation for:
  - Sequential Phase Gating.
  - Turn-Gated Feature Finalization (`leap-finish`).
  - Turn-Gated PR Submission (`leap-pr`).
- **REQ-5 (Skill Synchronization):** Ensure all updated skills are successfully propagated to active agent projection directories (such as `.gemini/`).

### Non-Functional Requirements

- **Clarity and Tone:** Maintain the professional, senior-engineer tone throughout.
- **Linter Compliance:** All modified markdown files must pass `check-md` with 0 violations.

### Testing Requirements

- **Markdown Validation:** Verify all updated markdown files pass the local `check-md` linter cleanly.
- **Installer Validation:** Run `scripts/install-skills.py` to verify successful linkage and propagation to `.gemini/` and other directories.

### Documentation Requirements

- All updated gating rules must be integrated cleanly into the LEAP guides, ensuring correct formatting and section linkages.

## Success Criteria

- [x] `.skills/leap-dev/SKILL.md` updated with strict sequential phase constraints.
- [x] `.skills/leap-finish/SKILL.md` updated with strict two-step turn-gated finalization rules.
- [x] `.skills/leap-pr/SKILL.md` updated with strict two-step turn-gated PR submission rules.
- [x] `kb/guide-methodology.md` contains comprehensive, formal gating documentation for all three skills.
- [x] `scripts/install-skills.py` runs successfully, propagating updated skills.
- [x] All new and modified markdown files pass `check-md` with 0 violations.

## Constraints

- No modification of application source code is permitted.

## Assumptions

- AI agents respect updated skill prompts and negative constraints during execution.

## Out of Scope

- Implementing automated pre-commit hook checks to block multi-phase commits (deferred to future LIP/Issue).
