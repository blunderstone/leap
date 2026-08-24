# Skill Staging & Installation Infrastructure Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-23

---

## Overview

We will implement the Skill Staging and Multi-Agent Installation Infrastructure using a phased development approach. We will write standard, dependency-free Python code for the installer script and tests, followed by the markdown-based AI agent skills. Finally, we will integrate skill installation directly into the existing `scripts/setup-leap.sh` workspace bootstrapper.

**Development Approach:** We will follow a strict Literate Programming workflow. Each phase will have concrete goals, approach details, testing strategies, and success criteria. We will write a complete automated test suite to verify the installer script across all execution paths.

### Overall Assessment

- **Complexity:** MEDIUM - Requires parsing markdown files, creating portable relative symlinks, creating new agent rules directories, and cleanly integrating with a shell-based installer prompt.
- **Risk:** LOW - No external runtime or library dependencies; operates entirely on project-local configuration paths.

---

## Phase 1: Canonical Directories, Template, and Installer Script

### Goals

- Initialize `.skills/` directory structure and publish `.skills/SKILL-TEMPLATE.md`.
- Implement a robust, dependency-free `scripts/install-skills.py` command-line utility.

### Approach

- **Directory Structure:** Create `.skills/` in the repository root. Write `.skills/SKILL-TEMPLATE.md` containing YAML frontmatter and standard sections.
- **Installer implementation (`scripts/install-skills.py`):**
  - Read each subdirectory of `.skills/` that contains a `SKILL.md` file.
  - Extract the skill name: parse the yaml frontmatter's `name:` attribute if present, otherwise fall back to the subdirectory's name.
  - Maintain an agent configuration mapping:
    - `gemini`: target `.gemini/instructions/`, extension `.md`
    - `cursor`: target `.cursor/rules/`, extension `.mdc`
    - `windsurf`: target `.windsurf/rules/`, extension `.md`
    - `claude`: target `.claude/commands/`, extension `.md`
    - `aider`: target `.aider/prompts/`, extension `.md`
  - Implement a symlink logic using `os.path.relpath` to compute portable relative paths from target agent directories to the source `SKILL.md`.
  - Handle physical copy fallback if `--copy` is passed, using standard `shutil.copy2`.
  - Implement robust cleanups: if a file or symlink already exists at the target, safely unlink/delete it before recreation to allow seamless re-runs.

### Testing

- Manual execution checks in empty directories.
- We will build a complete automated test suite in Phase 3.

### Success Criteria

- [x] Directory `.skills/` and template `SKILL-TEMPLATE.md` exist.
- [x] Script `scripts/install-skills.py` is implemented and syntax-error free.
- [x] Running `python3 scripts/install-skills.py` successfully parses skill packages.

---

## Phase 2: Authoring LEAP Native Skills

### Goals

- Create our family of high-value LEAP custom instruction skills (`leap-start`, `leap-dev`, `leap-resume`, `leap-handoff`, `leap-finish`, and `leap-pr`) using the official template.

### Approach

- **`leap-start` skill (`.skills/leap-start/SKILL.md`):**
  - Context/Purpose: Bootstrap a new LEAP feature branch.
- **`leap-dev` skill (`.skills/leap-dev/SKILL.md`):**
  - Context/Purpose: Drive implementation phases following standard TDD.
- **`leap-handoff` skill (`.skills/leap-handoff/SKILL.md`):**
  - Context/Purpose: Capture and commit session pause state in `handoff.md`.
- **`leap-resume` skill (`.skills/leap-resume/SKILL.md`):**
  - Context/Purpose: Automate pulling changes, reading and deleting the handoff document, and orienting clean sessions.
- **`leap-finish` skill (`.skills/leap-finish/SKILL.md`):**
  - Context/Purpose: Close out feature branches, update checkboxes, and compile `completion-summary.md` on approval.
- **`leap-pr` skill (`.skills/leap-pr/SKILL.md`):**
  - Context/Purpose: Draft reviewer-friendly PR summaries and programmatically create Pull Requests.

### Testing

- Verify that all written skills are syntactically valid and pass `check-md` with zero linting issues.

### Success Criteria

- [x] `.skills/leap-start/SKILL.md` fully authored and compliant with the template.
- [x] `.skills/leap-dev/SKILL.md`, `.skills/leap-handoff/SKILL.md`, and `.skills/leap-resume/SKILL.md` fully authored.
- [x] `.skills/leap-finish/SKILL.md` and `.skills/leap-pr/SKILL.md` fully authored.
- [x] All skills pass the `check-md` linter.

---

## Phase 3: Integration, Test Suite, and Verification

### Goals

- Build an automated test suite verifying `install-skills.py`.
- Integrate skill installation into `scripts/setup-leap.sh`.
- Validate entire workspace compliance.

### Approach

- **Automated Tests (`scripts/tests/test_install_skills.py` or similar):**
  - Write standard Python `unittest` unit tests inside `scripts/tests/test_install_skills.py`.
  - Test case: extracting skill name (YAML frontmatter parsing vs fallback).
  - Test case: target path and file extension configuration for all 5 target agents.
  - Test case: symlink creation using relative paths (verify symlink target is correct and matches expectation).
  - Test case: physical file copy option using `--copy`.
  - Test case: overwriting pre-existing targets (ensure re-running the script cleans up old symlinks or files).
- **Setup Integration (`scripts/setup-leap.sh`):**
  - Add a new "Configuring Agent Skills" section into `scripts/setup-leap.sh`.
  - Prompt the developer: "Would you like to install the LEAP custom agent skills into your configured agent directories?"
  - If yes, run `python3 scripts/install-skills.py all`.
- **Validation:**
  - Run the Python test suite to verify the installer script behavior.
  - Run `check-md kb/` across the entire codebase to ensure total compliance.

### Testing

- Run the automated installer test suite.
- Run `scripts/setup-leap.sh` interactively to verify prompting, option selection, and successful symlink/copy execution.

### Success Criteria

- [x] Python test suite written and passing with 100% pass rate.
- [x] `setup-leap.sh` updated and cleanly prompts and runs the installer script.
- [x] All success criteria from `goals.md` are completely met and verified.
- [x] `check-md` passes successfully across the entire repository.
