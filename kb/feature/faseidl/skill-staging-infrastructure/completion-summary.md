# Skill Staging & Installation Infrastructure Completion Summary

**Branch:** `faseidl/skill-staging-infrastructure`<br>
**Base Branch:** `main`<br>
**Date:** 2026-08-23<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

---

## Overview

This feature introduces a robust, unified "Canonical Source of Truth" architecture for managing, projecting, and enforcing custom instruction sets ("skills") across multiple developer-assisting AI agent tools. 

To resolve the discrepancy between flat command/rules namespaces (Gemini CLI, Cursor, Windsurf, Claude Code, Aider) and the self-contained package directories required by modern MCP servers, all skills are canonically authored as `<skill-name>/SKILL.md` under a root `.skills/` directory. A portable, dependency-free Python 3 installer script (`scripts/install-skills.py`) then projects relative symlinks (or physical copies with `--copy`) into target rule directories with their correct respective extensions and structures.

A standard family of six custom LEAP skills (`leap-start`, `leap-dev`, `leap-handoff`, `leap-resume`, `leap-finish`, and `leap-pr`) were delivered to standardize workspace setup, requirements gathering, TDD code implementation, session pause transitions, clean session start orientations, and branch finalization under the LEAP methodology. Furthermore, the repository-wide workspace configurator (`scripts/setup-leap.sh`) has been integrated to prompt and deploy these skills and configure project `.gitignore` patterns automatically.

---

## What Changed

### High-Level Summary

- Established `.skills/` canonical staging directory.
- Created standard frontmatter-driven `.skills/SKILL-TEMPLATE.md`.
- Implemented executable, dependency-free `scripts/install-skills.py` with multi-agent projection support (Gemini, Cursor, Windsurf, Claude Code, Aider), featuring custom `--repo-root` and `--skills-dir` options to support Git submodule parent/consuming workspaces flawlessly.
- Authored six custom LEAP methodology state-machine workflow skills under `.skills/`.
- Updated `scripts/setup-leap.sh` to support optional custom agent skills installation and automatic `.gitignore` appending/backup.
- Created Python-native unit test suite `scripts/tests/test_install_skills.py`.
- Generalized and renamed the session guide to `kb/best-practices-agent-sessions.md`.
- Authored the core usage guide `kb/guide-skills.md` explaining the family of skills, setup instructions, and state-machine transition guardrails.

### Detailed Changes

#### Staging & Core Infrastructure

- **`.skills/`**: Root staging folder initialized.
- **`.skills/SKILL-TEMPLATE.md`**: Created standard template with YAML frontmatter parameters (name, description, version, parameters) and markdown sections. Handled check-md requirements by using compliant blank lines inside frontmatter.
- **`scripts/install-skills.py`**: Robust command-line utility. Parsed YAML frontmatter dynamically without external dependencies. Configured custom relative symlinking based on target directories. Supports dynamic argument overrides `--repo-root` and `--skills-dir` to enable flawless projection into parent repos when LEAP is consumed as a submodule. Safely deletes existing symlinks/rules to prevent write collisions on re-runs.

#### Custom LEAP Skills (Strict State-Machine)

- **`leap-start`**: Outlined strict workflow rules for starting feature branches, setting up feature directories, and drafting `goals.md` and `plan.md`. Strengthened rules around TDD and milestone commits. Added an explicit execution firewall to strictly forbid writing application code under this skill.
- **`leap-dev`**: Drives the test-driven development loop, highlighting the mandatory RED-GREEN-REFACTOR cycle, atomic RED/GREEN commits, and compliance with `kb/best-practices-tdd.md`. Autorizes optional Phase Documents (`phase-*.md`) to decompose complex phase execution. Grants explicit TDD exceptions for non-code tasks (such as documentation, static content, and asset reorganization).
- **`leap-handoff`**: Captures active git hashes, uncommitted edits, test states, and next tasks into a transient, committed `kb/feature/<username>/<feature-name>/handoff.md` file, allowing developers to completely reset the agent's context window. Requires staging and committing the handoff file before pausing.
- **`leap-resume`**: Automatically runs `git pull` on startup, ingests the active `handoff.md`, programmatically deletes and commits the handoff file deletion (via `git rm`), and orientates clean sessions.
- **`leap-finish`**: Standardized compiling `completion-summary.md` and prompting users to verify Success Criteria. Mandates staging and committing the finalized completion summary and checked success criteria.
- **`leap-pr`**: Standardized reading committed completion summaries to generate reviewer-focused, concise PR descriptions. Automatically carries over metadata and GitHub issue closure references. Offers to programmatically push and create Pull Requests using the GitHub CLI (`gh`).

#### Setup Integration & Verification

- **`scripts/setup-leap.sh`**: Added "4b. Configure Staged Agent Skills" prompt, triggering `install-skills.py` cleanly. Added "4c. Configure .gitignore" prompting to append standard LEAP rule ignores and backup `.gitignore` automatically.
- **`scripts/tests/test_install_skills.py`**: Added 7 unit tests checking symlink creation, copy mode, Selective Agent targets, and YAML parsing.

### New Files

- `.skills/SKILL-TEMPLATE.md` - Standard YAML frontmatter-driven skill specification.
- `.skills/leap-start/SKILL.md` - Bootstrapping and strict planning process enforcer.
- `.skills/leap-dev/SKILL.md` - Test-driven implementation driver with TDD exceptions and phase document support.
- `.skills/leap-handoff/SKILL.md` - Session pause state compiler and git commit checker.
- `.skills/leap-resume/SKILL.md` - Git puller and fresh session orientation synchronizer.
- `.skills/leap-finish/SKILL.md` - Completion compiler, linter verifier, and checklist update authorized.
- `.skills/leap-pr/SKILL.md` - PR description drafter and programmatic gh-pr submitter.
- `scripts/install-skills.py` - Portability-preserving, submodule-friendly Python installer script.
- `scripts/tests/test_install_skills.py` - Automated test suite for the Python installer.
- `kb/guide-skills.md` - Core guide document for the LEAP custom agent skills framework.
- `kb/best-practices-agent-sessions.md` - Renamed and generalized AI-agnostic session management guide.

### Modified Files

- `scripts/setup-leap.sh` - Workspace bootstrapper integrated with agent skills installation and gitignore management.
- `kb/best-practices-tdd.md` - Updated links pointing to the renamed AI-agnostic session guide.
- `.gitignore` - Ignored projected rules folders `.cursor/`, `.gemini/`, `.windsurf/`, `.claude/`, and `.aider/` to prevent git tree pollution.

---

## Key Implementation Details

### Zero-Dependency Submodule Portability

To guarantee that the workspace can be easily configured on any machine without installing pre-requisite libraries, `scripts/install-skills.py` and its tests were built entirely using the Python standard library. By exposing `--repo-root` and `--skills-dir` options, it fully decoupling rule directory projection from the script's physical location, allowing a parent repository consuming LEAP as a submodule to easily map and install rules at checkout.

### Clean YAML/Markdown Linter Compliance

The `check-md` linter enforces a blank line before horizontal rules and lists, which originally conflicted with standard flat YAML frontmatter lists. We discovered that inserting empty lines inside YAML frontmatter blocks successfully satisfies `check-md` linter Rule 2 while remaining fully valid YAML. We standardly applied this structure across all skills and templates.

---

## Testing

### Test Strategy

- **Automated Python Unit Tests:** 7 comprehensive tests executing in temporary directories, mocking different project configurations and verifying relative symlink pointer correctness.
- **Linter Coverage:** Multi-run validation of `check-md kb/` and `check-md .skills/` to guarantee perfect styling.

### Test Results

- **Automated Tests:** 7/7 passing cleanly.
- **`check-md` Validation:** PASSED with 100% clean check state.

---

## Documentation

### Inline Documentation

- `scripts/install-skills.py` contains exhaustive module docstrings, function signatures, and step-by-step logic comments.
- `scripts/tests/test_install_skills.py` contains standard test assertions and descriptions.

### Guides and Examples

- Provided an elegant example template in `.skills/SKILL-TEMPLATE.md`.
- Authored three fully functional workflow skills that act as live documentation of the system.
