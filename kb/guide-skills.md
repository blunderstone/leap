# LEAP Custom Agent Skills Guide

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** August 23, 2026

---

## Overview

In a Literate (Extended-by-Agent) Programming (LEAP) environment, custom instructions and rule configurations—collectively referred to as **Skills**—help standardize and coordinate workflows across multiple developer-assisting AI agent tools. 

Because different AI assistants (such as Gemini CLI, Cursor, Windsurf, Claude Code, and Aider) consume custom rules in highly divergent, flat, or tool-specific folders, managing them individually leads to maintenance overhead and drift. 

To solve this while remaining fully portable and ready for future MCP (Model Context Protocol) server migrations, this project utilizes a **Canonical Source of Truth** architecture:

- All skills are authored as self-contained directories containing a `SKILL.md` instruction file inside a central `.skills/` directory.
- A portable, dependency-free installer script (`scripts/install-skills.py`) projects relative symlinks into target directories, instantly updating all active assistants whenever a skill is modified.

---

## Installation & Setup

Custom agent skills are integrated directly into our repository-level workspace configurator:

```bash
# Initialize the workspace and install skills interactively
bash scripts/setup-leap.sh
```

You can also run, refresh, or override skill installation directly using the Python installer script:

```bash
# Link all skills to all active agent target directories (default: relative symlinks)
python3 scripts/install-skills.py all

# Link skills to a specific agent target (e.g., cursor)
python3 scripts/install-skills.py cursor

# Copy skill files physically (no symlinks) instead of linking them
python3 scripts/install-skills.py all --copy
```

---

## Supported Agent Directories

The installer projects rules into each target agent's expected path using its default file extension:

| Agent Target                 | Rule Directory          | File Extension | Projection Mode     |
|:-----------------------------|:------------------------|:---------------|:--------------------|
| **Gemini CLI / Antigravity** | `.gemini/instructions/` | `.md`          | Flat File Namespace |
| **Cursor**                   | `.cursor/rules/`        | `.mdc`         | Flat File Namespace |
| **Windsurf**                 | `.windsurf/rules/`      | `.md`          | Flat File Namespace |
| **Claude Code**              | `.claude/commands/`     | `.md`          | Flat File Namespace |
| **Aider**                    | `.aider/prompts/`       | `.md`          | Flat File Namespace |

---

## The LEAP Skill Inventory

The workspace includes a standard suite of custom skills designed to enforce a highly disciplined, test-driven development lifecycle:

```
                   ┌──────────────┐
                   │  leap-start  │  <── Launch Branch & Plan
                   └──────┬───────┘
                          │
                          ▼
                   ┌──────────────┐  Session Pause (Write handoff file)
  ┌───────────────>│   leap-dev   ├────────────────────────────────┐
  │                └──────┬───────┘                                │
  │                       │                                        ▼
  │                       ▼                                 ┌──────────────┐
  │                ┌──────────────┐                         │ leap-handoff │
  │                │ leap-finish  │  <── Completion Summary └──────┬───────┘
  │                └──────┬───────┘                                │
  │                       │                                        ▼
  │                       ▼                                 [Clean Session]
  │                ┌──────────────┐                                │
  │                │   leap-pr    │  <── PR Description            ▼
  │                └──────────────┘                         ┌──────────────┐
  │                                                         │ leap-resume  │
  └─────────────────────────────────────────────────────────┴──────────────┘
                                     Session Resume & Cleanup handoff file
```

### 1. `leap-start` (Launch Phase)

* **Trigger:** "/leap-start" or "start a new feature branch for X".
* **What it does:** Automates the planning phase of a feature. It switches to a clean branch, creates the corresponding knowledge base directory `kb/feature/<username>/<feature-name>/`, and drafts the `goals.md` requirements specification from its template.
* **Review Gate:** Halts work and waits for human review and commit before drafting a phase-by-phase implementation `plan.md`.

### 2. `leap-dev` (Build Phase)

* **Trigger:** "/leap-dev" or "implement Phase 1 of our plan".
* **What it does:** Enforces a strict Test-Driven Development (TDD) workflow based on `kb/best-practices-tdd.md`.
* **The RED/GREEN Gating Loop:**
  1. **RED state:** Guides the agent to write failing tests, run them to verify failure, and **halt for review and commit** (`test(<module>): ... (TDD RED)`).
  2. **GREEN state:** Guides the agent to write the minimal code to satisfy tests, run them to verify success, and **halt for review and commit** (`fix(<module>): ... (TDD GREEN)`).
  3. **Refactor:** Perform cleanups and optimizations while ensuring tests remain green.

### 3. `leap-handoff` (Session Pause)

* **Trigger:** "/leap-handoff" or "pause session and write a handoff".
* **What it does:** Solves context bloating and high token overhead by capturing a high-signal, zero-noise snapshot of current git hashes, stashes, pending test states, and upcoming tasks into a transient `handoff-<phase>.md` file.
* **Benefit:** Allows the developer to completely clear the agent's context window and start a pristine new conversation session without losing progress.

### 4. `leap-resume` (Session Start)

* **Trigger:** "/leap-resume" or "resume session".
* **What it does:** Executed immediately upon launching a fresh conversation session. It scans active branches, reads `goals.md`, `plan.md`, and any transient `handoff-*.md` files to reconstruct a perfect context model, then cleans up/deletes the temporary handoff file to prevent clutter.

### 5. `leap-finish` (Verify & Close)

* **Trigger:** "/leap-finish" or "we are done, write the completion summary".
* **What it does:** Concludes the active task. It analyzes git histories and test coverages to draft the comprehensive `kb/feature/<username>/<feature-name>/completion-summary.md` document, and presents success criteria checkboxes to the developer.
* **Review Gate:** Reminds the agent that checking off criteria checkboxes is a human-aligned action requiring manual verification.

### 6. `leap-pr` (Review Phase)

* **Trigger:** "/leap-pr" or "draft our PR description".
* **What it does:** Reads the completed summary and generates a concise, high-signal, and reviewer-friendly `pr-description.md` pointing reviewers to exactly what to review and how to verify it locally.

---

## Workflow Boundaries & Execution Gates

To prevent process bleed and "racing ahead," the LEAP skill inventory operates as a strict, sequential state machine. Each skill enforces explicit logical boundaries on the agent's behavior to keep focus razor-sharp:

- **Planning Block (`leap-start`):** Strictly forbids writing or modifying any application code, running build tools, or performing implementation work. Once your requirements and plans are approved and committed, the agent must halt and prompt you to transition to `leap-dev`.
- **Implementation Block (`leap-dev`):** Focuses entirely on the RED-GREEN-REFACTOR TDD loop. It strictly forbids compiling completion summaries or finalization checks. Once all phases in your implementation plan are complete, green, and committed, the agent prompts you to transition to `leap-finish`.
- **Review & Verification Block (`leap-finish`):** Strictly forbids any code modifications or PR description drafting. It focuses solely on verifying success criteria and compiling `completion-summary.md`. If any tests or linter checks fail during verification, you must transition back to `leap-dev` to resolve them.
- **Review Generation Block (`leap-pr`):** Strictly forbids writing code or editing files under `kb/feature/` (other than drafting `pr-description.md`). It acts purely as a final copy-paste review description generator.

These boundaries are deliberate architectural safeguards that ensure your agent remains highly focused, eliminates context leakage, and complies perfectly with human-aligned verification gates at every transition.

---

## Developing New Skills

All new custom rules must follow the YAML frontmatter specification. To create a new skill:

1. Copy `.skills/SKILL-TEMPLATE.md` to a new directory under `.skills/<new-skill>/SKILL.md`.
2. Define the YAML frontmatter configuration (name, description, version, and parameters).
3. Draft the sections: Context & Purpose, Trigger Conditions, Operational Workflow, Constraints & Rules, Output Schema.
4. Run the installer to link the new skill to your workspace tools:

   ```bash
   python3 scripts/install-skills.py all
   ```

### Linter Compliance in Frontmatter

Our Markdown formatter `check-md` enforces linter rules on all workspace files. Because frontmatter parameters (such as `parameters:`) are formatted as standard Markdown lists, you must insert an **empty blank line** between frontmatter headings and list items, and before the closing frontmatter delimiter `---`.

#### Compliant Example:

```yaml
---
name: sample-skill-name
description: Clear description.
version: 1.0.0
parameters:

  - name: target_file
    type: string
    description: Path to file
    required: true

---
```
