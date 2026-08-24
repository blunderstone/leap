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

This skill handles the critical "Session Start Orientation" process for AI coding agents under the **[Literate (Extended-by-Agent) Programming (LEAP) Methodology](../../kb/guide-methodology.md)** as defined in **[AI Agent Session Management Best Practices](../../kb/best-practices-agent-sessions.md)**. When starting a clean, pristine session with zero history, this skill immediately reads the active feature's goals, plans, and transient handoff files to establish a perfect, zero-noise context model.

## Trigger Conditions

- Activated immediately at the start of a new, clean agent conversation on an active branch (e.g., "let's resume", "orient context", or `/leap-resume`).

## Operational Workflow

0. **Pull Latest Changes (Prerequisite):** Run `git pull` to fetch and integrate any new commits/updates from GitHub/GitLab. This ensures that if the session was paused on another machine (or by another developer), you have the very latest branch updates and the committed handoff document locally before proceeding.
1. **Locate Workspace Context:** Detect the current active git branch and locate the active feature folder under `kb/feature/`.
2. **Read Status Indicators:**
   - Read `goals.md` and `plan.md` to identify checked-off `[x]` versus pending `[ ]` phases/success criteria.
   - Scan the feature folder for the transient `handoff.md` file.
3. **Establish Strategy Model:** Consolidate this information into a precise roadmap of the exact phase, test file, and next step to resume.
4. **Cleanup:** Once the transient `handoff.md` file has been read and digested, safely delete it and commit the deletion (via `git rm handoff.md` and a dedicated git commit `doc(workflow): consume handoff and resume`) so that the transient file is cleanly removed from the active tree and does not clutter future sessions.
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
