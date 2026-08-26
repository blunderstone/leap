# Skill Staging & Installation Infrastructure Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-23

---

## Quick Summary

Establish a canonical `.skills/` directory for managing self-contained AI agent skills, implement a robust python-based `install-skills.py` installer to link them to target agents (including Gemini, Cursor, Claude, Aider, and Windsurf), and author native skills for bootstrapping (`leap-new`), completing (`leap-complete`), and PR authoring (`leap-pr`) under the LEAP methodology.

---

## Executive Summary

As AI coding agents (such as Claude Code, Gemini CLI, Cursor, Windsurf, and Aider) become key participants in our development lifecycles, establishing unified, reusable custom instructions ("skills") is critical. However, target agents consume custom rules in highly divergent, flat, or agent-specific formats.

To solve this while preparing for future Tool/MCP server migrations, this feature implements a "Canonical Source of Truth" pattern. All skills will be co-located as self-contained directories under a unified `.skills/` workspace folder, containing the instruction `SKILL.md` file (conforming to a standard frontmatter-driven template) and any related assets. A robust, portable `scripts/install-skills.py` script will orchestrate relative symlink projection into agent-specific paths (e.g. `.gemini/skills/`, `.cursor/rules/`, `.windsurf/rules/`, `.claude/commands/`, `.aider/prompts/`).

Additionally, three native LEAP skills will be delivered: `leap-new` (to automate starting a new feature branch and drafting `goals.md`), `leap-complete` (to automate drafting the LEAP `completion-summary.md`), and `leap-pr` (to automate drafting the reviewer-facing `pr-description.md`). The workspace's `setup-leap.sh` will be updated to optionally install these skills for whatever agents the developer chooses.

---

## Objectives

1. Setup the canonical `.skills/` directory structure and publish the canonical `SKILL-TEMPLATE.md` for future skill development.
2. Implement `scripts/install-skills.py` in Python to link or copy skills from `.skills/` to target agent directories, with native support for Gemini, Cursor, Windsurf, Claude, and Aider.
3. Author the `leap-new` skill at `.skills/leap-new/SKILL.md` to bootstrap LEAP feature branches.
4. Author the `leap-complete` skill at `.skills/leap-complete/SKILL.md` to bootstrap `completion-summary.md`.
5. Author the `leap-pr` skill at `.skills/leap-pr/SKILL.md` to bootstrap `pr-description.md`.
6. Update `scripts/setup-leap.sh` to prompt and configure these skills for selected agents.
7. Implement automated tests to verify `install-skills.py` installation behavior.

---

## Requirements

### Functional Requirements

- **REQ-1 (Staging Directory & Template):** Initialize `.skills/` in the repository root as the canonical source of truth, and provide a standardized `SKILL-TEMPLATE.md` inside it with structured YAML frontmatter (name, description, version, parameters) and standard sections (Context & Purpose, Trigger Conditions, Operational Workflow, Constraints & Rules, Output Schema).
- **REQ-2 (Installer Script):** Implement `scripts/install-skills.py` in Python 3.
  - Automatically extract skill names from the folder or YAML frontmatter if present.
  - Support targeting specific agents (`gemini`, `cursor`, `windsurf`, `claude`, `aider`, or `all`).
  - Use portable, relative symlinks by default.
  - Support physical copies with a `--copy` flag.
  - Safely overwrite pre-existing links or files to allow seamless re-installation.
- **REQ-3 (leap-new Skill):** Include a `leap-new` skill instructing agents how to create feature branches, establish feature directories under `kb/feature/`, and draft `goals.md` adhering to `guide-methodology.md`.
- **REQ-4 (leap-complete Skill):** Include a `leap-complete` skill instructing agents how to draft `completion-summary.md` and prompt for manual checklist validation in compliance with LEAP gating rules.
- **REQ-5 (leap-pr Skill):** Include a `leap-pr` skill instructing agents how to draft `pr-description.md`.
- **REQ-6 (Setup Bootstrapping):** Update `scripts/setup-leap.sh` to prompt the developer to install these skills during workspace initialization.

### Non-Functional Requirements

- **Portability:** Symlinks created by `install-skills.py` must use relative paths to remain fully portable across clones and environments.
- **Python 3 Compatibility:** The installer and tests must run on any environment with Python 3.8+.
- **Zero External Dependencies:** The installer script must use only Python standard libraries to avoid pre-requisite installations.

### Testing Requirements

- Implement an automated test suite verifying `install-skills.py` options (symlinks vs copies, selective targets, empty directories, overwrite behavior).
- Ensure all newly added markdown files conform perfectly to linter rules and pass `check-md` cleanly.

### Documentation Requirements

- Detailed inline docstrings and comments in `install-skills.py`.
- Ensure all skills are documented with clear usage and integration instructions.

---

## Success Criteria

- [x] Canonical directory structure `.skills/` initialized in the workspace.
- [x] Canonical template `SKILL-TEMPLATE.md` placed in `.skills/` for future developers.
- [x] `scripts/install-skills.py` fully implemented and executable.
- [x] Running `./scripts/install-skills.py gemini` creates functional relative symlinks in `.gemini/skills/` under nested skill directories.
- [x] Running `./scripts/install-skills.py cursor` creates functional relative symlinks in `.cursor/rules/` with the `.mdc` file extension.
- [x] Running `./scripts/install-skills.py windsurf` creates functional relative symlinks in `.windsurf/rules/`.
- [x] Running `./scripts/install-skills.py claude` creates functional relative symlinks in `.claude/commands/`.
- [x] Running `./scripts/install-skills.py aider` creates functional relative symlinks in `.aider/prompts/`.
- [x] `leap-start`, `leap-dev`, `leap-resume`, `leap-handoff`, `leap-finish`, and `leap-pr` skills implemented under `.skills/` and functional.
- [x] `scripts/setup-leap.sh` successfully integrates with the new installer, prompting and configuring agent skills.
- [x] Test suite for `install-skills.py` created and passing successfully.
- [x] All workspace markdown documents pass `check-md` cleanly.

---

## Constraints

- Built entirely with standard Python libraries.
- Must respect the exact directory layout and flat namespaces specified in `skill_staging_and_installation_architecture.md`.

---

## Assumptions

- Python 3 is installed and available on systems initializing the LEAP environment.

---

## Out of Scope

- Implementing an MCP server (reserved for a future milestone).
- Managing global system-wide agent configuration paths (focused on project-local directories).
- Implementing GitHub Copilot support (deferred to a later iteration).
