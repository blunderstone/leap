---
name: leap-resume
description: Synchronizes and orients a brand-new, clean agent session with the active feature branch, goals, plan, and handoff files.
version: 1.0.0
parameters:

  - name: feature_name
    type: string
    description: Name of the active feature folder
    required: true

---

# Skill: LEAP Workspace Resumer (Session Start)

## Context & Purpose

This skill handles the critical "Session Start Orientation" process for AI coding agents under the **[Literate (Extended-by-Agent) Programming (LEAP) Methodology](../../kb/guide-methodology.md)** as defined in **[Claude Session Management Best Practices](../../kb/best-practices-claude-sessions.md)**. When starting a clean, pristine session with zero history, this skill immediately reads the active feature's goals, plans, and transient handoff files to establish a perfect, zero-noise context model.

## Trigger Conditions

- Activated immediately at the start of a new, clean agent conversation on an active branch (e.g., "let's resume", "orient context", or `/leap-resume`).

## Operational Workflow

1. **Locate Workspace Context:** Detect the current active git branch and locate the active feature folder under `kb/feature/`.
2. **Read Status Indicators:**
   - Read `goals.md` and `plan.md` to identify checked-off `[x]` versus pending `[ ]` phases/success criteria.
   - Scan the feature folder for any transient `handoff-*.md` or `dev-note-handoff-*.md` files.
3. **Establish Strategy Model:** Consolidate this information into a precise roadmap of the exact phase, test file, and next step to resume.
4. **Cleanup:** Once the transient handoff file has been read and digested, safely delete or archive it (via `git rm` or `rm`) so it does not clutter future sessions.
5. **Present Orientation:** Summarize findings clearly to the user, state current progress, and suggest the exact next command.

## Constraints & Rules

- **Strict Context Parsing:** Do NOT guess progress or ask the user redundant questions. Rely entirely on the written files to reconstruct the active state.
- **Linter Compliance:** Keep all read, modified, or generated files 100% compliant with linter rules.

## Output Schema / Format

Upon successful execution, print the orientation block:

```
[leap-resume] Session Synchronized! Active context established:

- Active Branch: <username>/<feature-name>
- Active Plan Phase: Phase <phase_number> (<phase_title>)
- Current Status: [Summarize what was completed before the handoff]
- Next Concrete Task: [Specify the very next step, e.g., implementing passed test, starting next phase TDD]

==> Alignment Achieved: Ready to begin work! Should we start implementing this step?
```
