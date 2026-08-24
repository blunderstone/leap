# Sequential Phase Gating Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** August 24, 2026

---

## Overview

We will implement Sequential Phase Gating and turn-gating constraints across the custom agent skills and methodology documentation. Because this is a process and documentation enhancement, we will follow a multi-phase Literate Programming execution plan, verifying both linter conformance and skill propagation after each phase.

**Development Approach:** Since these changes do not affect application source code, we will operate under **TDD Exceptions** for each phase, verifying formatting manually with `check-md` and verifying integration by checking the symlinked skill files and running the test suites.

### Overall Assessment

- **Complexity:** LOW - The updates are localized to `.skills/` files and `kb/guide-methodology.md`.
- **Risk:** LOW - No application runtime logic is modified, ensuring zero chance of behavioral regression for check-md.

---

## Phase 1: Update Custom Agent Skills

### Goals

- Update `.skills/leap-dev/SKILL.md` to enforce strict sequential phase gating.
- Update `.skills/leap-finish/SKILL.md` to enforce a mandatory two-step finalization turn gate.
- Update `.skills/leap-pr/SKILL.md` to enforce a mandatory two-step PR submission turn gate.
- Verify that `scripts/install-skills.py` propagates these updates cleanly to `.gemini/` without error.

### Approach

- **Update `leap-dev`:** Add a dedicated subsection inside the "Constraints & Rules" section detailing strict sequential phase gating, turn restrictions (maximum of one phase per turn), mandatory approval pausing at phase boundaries (even for TDD Exceptions), separate atomic commits per phase, and negative constraints on checking off checkboxes proactively.
- **Update `leap-finish`:** Restructure the rules and workflow in `leap-finish` to explicitly break down finalization into a strict two-step turn-gated workflow. Prohibit compiling the completion summary and executing the finalization git commit/checkbox updates in a single turn.
- **Update `leap-pr`:** Restructure the rules and workflow in `leap-pr` to explicitly break down PR submission into a strict two-step turn-gated workflow. Prohibit running `git push` or `gh pr create` in the first turn without user confirmation.
- **Run Skill Installation:** Execute `python3 scripts/install-skills.py all` to propagate the updated skills.

### Testing

- Run `check-md` on each updated skill file to ensure perfect linter score.
- Run `python3 -m unittest discover -s scripts/tests` to verify that installer tests still pass cleanly.
- Verify that the target symlink files (e.g., in `.gemini/skills/`) exist and contain the updated rules.

### Success Criteria

- [x] `.skills/leap-dev/SKILL.md` updated and lints with 0 errors.
- [x] `.skills/leap-finish/SKILL.md` updated and lints with 0 errors.
- [x] `.skills/leap-pr/SKILL.md` updated and lints with 0 errors.
- [x] `scripts/install-skills.py` runs successfully, propagating the updated rules.

### Explicitly Deferred

- None.

**Rationale:** The skills are our primary interface with the agents; locking down their instruction sets immediately establishes the new constraints.

---

## Phase 2: Update LEAP Methodology Documentation

### Goals

- Formally document sequential phase gating, turn-gated feature finalization, and turn-gated PR submission inside `kb/guide-methodology.md`.

### Approach

- **Update `kb/guide-methodology.md`:** Navigate to the "Gating Mandates for AI Agents" section and add comprehensive new subsections describing:
  1. **Sequential Phase Gating:** Mandating one phase per turn during execution, explicit pausing at boundaries, and extending gating rules to TDD Exceptions.
  2. **Turn-Gated Feature Finalization:** Mandating that `leap-finish` is executed as a strict two-step process to allow the developer to review and approve the draft completion summary and checklist assessment before commits are made.
  3. **Turn-Gated PR Submission:** Mandating that `leap-pr` is executed as a strict two-step process to allow the developer to review the generated PR title, description, and settings before submission.

### Dependencies

- Depends on Phase 1 completion.

### Testing

- Run `check-md kb/guide-methodology.md` to verify that all links, headings, and formatting conform perfectly to standard.

### Success Criteria

- [x] `kb/guide-methodology.md` updated with comprehensive gating standards.
- [x] Updated methodology file passes `check-md` with 0 violations.

### Explicitly Deferred

- None.

**Rationale:** Formalizing the gating rules in the methodology establishes them as repo-wide standards and ensures they are permanent.

---

## Phase 3: Final Validation and Integration Testing

### Goals

- Ensure the entire codebase, tests, and documentation are pristine.
- Confirm full workspace compliance with the updated rules.

### Approach

- Run the full test suite for `check-md` using `pytest`.
- Run the full scripts test suite.
- Run `check-md kb/` over all knowledge base files to ensure 100% compliance.

### Testing

- Run python test suite: `check-md/.venv/bin/pytest -c check-md/pyproject.toml check-md/tests/`
- Run scripts test suite: `python3 -m unittest discover -s scripts/tests`
- Run shell script test suite: `bash scripts/qmd/tests/qmd-config.test.sh`
- Run global markdown linter check: `check-md kb/`

### Success Criteria

- [x] All check-md tests pass cleanly.
- [x] All installer script tests pass cleanly.
- [x] Shell script test suite passes cleanly.
- [x] Workspace linter check `check-md kb/` reports 0 violations.

### Explicitly Deferred

- None.

**Rationale:** Exhaustive validation is mandatory under the LEAP methodology to guarantee zero regressions.

---

## Risk Mitigation

### Risk 1: Agents ignore the updated rules and continue to jump ahead.

#### Mitigation

By placing these rules as explicit negative constraints in the skill system prompts (which are loaded as system-level instructions in every turn), we leverage the LLM's highest-priority attention layers to enforce turn-gating.

---

## Decision Points

### After Phase 1

- Proceed if skill changes are complete, propagate cleanly, and all linter checks are green.

### After Phase 2

- Proceed if methodology guides are fully documented and have 0 linter violations.
