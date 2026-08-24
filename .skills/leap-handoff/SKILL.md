---
name: leap-handoff
description: Captures high-signal, zero-noise session state and pending tasks to facilitate clean workspace context transitions.
version: 1.0.0
parameters:

  - name: phase_name
    type: string
    description: Current plan phase being paused or handed off
    required: true

---

# Skill: LEAP Workspace Handoff (Session Pause)

## Context & Purpose

This skill helps manage AI agent session boundaries under the **[Literate (Extended-by-Agent) Programming (LEAP) Methodology](../../kb/guide-methodology.md)** as defined in **[AI Agent Session Management Best Practices](../../kb/best-practices-agent-sessions.md)**. It captures high-signal, zero-noise session state (modified files, exact git commit hashes, test status, and upcoming tasks) into a transient handoff document, allowing developers to completely reset the agent's context window without losing state or carrying over bloated conversational history.

## Trigger Conditions

- The user wants to pause development, switch sessions, or prepare a handoff (e.g., "let's pause here and write a handoff", "conclude this session", or `/leap-handoff`).

## Operational Workflow

1. **State Gathering:** Run `git status`, check active branch, check test status, and identify current phase.
2. **Draft Handoff:** Create a transient, committed markdown file inside the active feature directory: `kb/feature/<username>/<feature-name>/handoff.md`. (If an existing `handoff.md` is already present, simply overwrite it with the new current state). Populate the handoff file with:
   - **Active Branch & Last Commit:** Target git branch and HEAD hash.
   - **Current Status:** What was completed in this session.
   - **Tests State:** Pass rate and coverage.
   - **Stash/Pending edits:** Any uncommitted modifications or stashes.
   - **Next Actions:** Numbered, concrete list of what needs to be done next in the next session.
3. **Verify Compliance:** Ensure the handoff file complies with `check-md` rules.
4. **Milestone Commit (Collaboration Ready):** Stage and commit the handoff document along with any completed work of the active phase to Git. Committing the handoff document ensures that you or another developer can cleanly pull the branch and resume the session from any machine:
   - Commit message format: `doc(workflow): save session handoff and pause`

## Constraints & Rules

- **Zero Noise:** Focus strictly on high-signal context needed to resume. Avoid conversational filler or long, raw logs.
- **Commit Mandate:** You must stage and commit the drafted handoff document before exiting this skill.
- **Linter Compliance:** The handoff document must pass `check-md` cleanly.

## Output Schema / Format

Upon successful creation, print a summary in the following structure:

```
[leap-handoff] Successfully captured session state!

- Handoff File: kb/feature/<username>/<feature-name>/handoff.md
- Next Actions:
  1. [Next task 1]
  2. [Next task 2]

==> Clean Restart Ready:
You can now safely restart your agent conversation with a pristine, empty context window. Upon launching the new session, run `/leap-resume` to immediately orient the new agent context!
```
