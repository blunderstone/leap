---
name: leap-dev
description: Guides agents through executing a plan phase using TDD (RED-GREEN-REFACTOR) and strict commit/review gating.
version: 1.0.0
parameters:

  - name: phase_name
    type: string
    description: The name or number of the plan phase to implement
    required: true

---

# Skill: LEAP Phase Implementer (TDD Loop)

## Context & Purpose

This skill guides AI coding agents in implementing code changes in a highly disciplined, test-driven manner under the **[Literate (Extended-by-Agent) Programming (LEAP) Methodology](../../kb/guide-methodology.md)**. It enforces the mandatory use of Test-Driven Development (TDD) as defined in **[TDD Best Practices](../../kb/best-practices-tdd.md)**, guarantees separate, atomic commits at RED and GREEN stages, and requires verification against project-specific testing standards if available.

## Trigger Conditions

- Explicit user invocation to begin development or implement a plan phase (e.g., "let's start implementing Phase 1", "run leap-dev for Phase 2", or `/leap-dev`).

## Operational Workflow

1. **Pre-Flight Check:** Verify that `goals.md` and `plan.md` have been approved and committed. Ensure the working directory is clean.
2. **Optionally Draft Phase Document:** For large, complex, or multi-step phases, you are highly encouraged to create a dedicated Phase Document inside the active feature directory: `kb/feature/<username>/<feature-name>/phase-<phase_name>.md` by populating the canonical template `[Phase Template](../../kb/template-phase.md)`. This document serves as a granular sub-plan, tracks sub-milestones, keeps you on track during long implementation phases, and acts as a precise state tracker during session pause/handoff transitions. (Note: Most standard phases do not require a separate phase document, but use them freely if a phase is highly complex).
3. **TDD RED Phase (Failing Tests First):**
   - **Draft Tests:** Analyze the requirements for the phase and write failing automated tests under the appropriate `tests/` directory following standard project patterns.
   - **Verify Failure (RED):** Run the test suite and confirm that the new tests fail as expected (and for the correct, verifiable reasons).
   - **Milestone Halt & Commit:** Present the failing tests and test failures to the user, **stop and wait for their review and approval**, and commit:
     - Commit message: `test(<module>): add failing test cases for <feature-or-fix> (TDD RED)`
4. **TDD GREEN Phase (Minimal Elegant Implementation):**
   - **Implement Minimal Code:** Write the absolute minimal implementation code required to satisfy the failing tests. Do not add speculative "just-in-case" functionality or diverge from established project architecture.
   - **Verify Success (GREEN):** Run the test suite and confirm that all tests pass cleanly.
   - **Milestone Halt & Commit:** Present the implementation code to the user, **stop and wait for their review and approval**, and commit:
     - Commit message: `fix(<module>): implement <feature-or-fix> to pass tests (TDD GREEN)`
5. **Refactor Phase:**
   - **Clean and Improve:** Clean up code duplication, improve naming, optimize performance, or add inline docs. Run tests continuously to ensure they remain green.
   - **Commit:** Commit refactoring changes separately if they are substantial.

## Constraints & Rules

- **TDD is Mandatory:** Do NOT write or modify application source code before writing failing tests, as per `[TDD Best Practices](../../kb/best-practices-tdd.md)`.
- **TDD Exceptions:** You are granted explicit permission to bypass the test-first TDD cycle for tasks that do not involve creating or modifying application source code (such as updating documentation, editing static markdown/content, tweaking configurations, or reorganizing assets). In these cases, verify your changes manually and document your manual validation steps clearly.
- **Atomic Commits:** You must **NEVER** combine RED (failing tests) and GREEN (implementation) into a single commit. They must be separate, sequential, and reviewed individually by the human developer.
- **Verification Rule:** Always run project-specific build and linter commands (e.g., `check-md kb/`, `ruff check`, etc.) before presenting work for review.
- **No Checklist Checking:** You must never check off a success criteria box in `goals.md` or `plan.md` without presenting test/linter verification results and getting explicit human authorization.
- **No Feature Finalization:** You are strictly forbidden from writing `completion-summary.md` or attempting to close/finalize the branch under this skill.
- **Phase Documents Authorization:** You are fully authorized and encouraged by the LEAP Methodology to create and use `phase-*.md` documents to decompose complex phase execution into granular, manageable sub-milestones.
- **Transition Gate:** Once all phases of your implementation plan are complete, green, and committed, your work under `leap-dev` is done. You must explicitly direct the user to trigger the **`leap-finish`** skill (e.g., via `/leap-finish`) to compile the completion summary and conduct the final gating review.

## Output Schema / Format

Upon initiating a phase, print a summary of the approach:

```
[leap-dev] Starting implementation of Phase <phase_name>...

- TDD Target: [Briefly describe the test scope]
- Next Step: Writing failing unit tests under tests/ (TDD RED Phase)
```
