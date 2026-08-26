# LEAP Installation & Setup Guide

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-19

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Integration Methods](#integration-methods)
  - [Path A: Git Submodule (Recommended)](#path-a-git-submodule-recommended)
  - [Path B: Direct Copy / Embedding](#path-b-direct-copy--embedding)
- [Interactive Workspace Setup](#interactive-workspace-setup)
- [Manual Workspace Setup (Reference)](#manual-workspace-setup-reference)
  - [1. Create your Knowledge Base](#1-create-your-knowledge-base)
  - [2. Install check-md](#2-install-check-md)
  - [3. Configure QMD Semantic Search](#3-configure-qmd-semantic-search)
- [Note for Windows Users](#note-for-windows-users)
  - [Git Bash (Recommended)](#git-bash-recommended)
  - [Windows Subsystem for Linux (WSL)](#windows-subsystem-for-linux-wsl)
  - [PowerShell / CMD (Manual Setup Only)](#powershell--cmd-manual-setup-only)
- [Verification & Next Steps](#verification--next-steps)
- [AI Agent Integration Templates](#ai-agent-integration-templates)
  - [1. Claude (CLAUDE.md)](#1-claude-claudemd)
  - [2. Gemini & Antigravity (GEMINI.md)](#2-gemini--antigravity-geminimd)
  - [3. GitHub Copilot (.github/copilot-instructions.md)](#3-github-copilot-githubcopilot-instructionsmd)
  - [4. Cursor & Windsurf (.cursorrules)](#4-cursor--windsurf-cursorrules)

---

## Overview

This guide provides comprehensive, step-by-step instructions for installing and setting up **Literate (Extended-by-Agent) Programming (LEAP)** inside your software repositories.

By integrating LEAP, you configure an agent-friendly workspace that bridges your documentation with your code, ensuring that both human developers and AI coding agents can work together seamlessly.

---

## Prerequisites

Before beginning, ensure your local development environment has the following prerequisites installed:

- **Git**: (Required for Path A) Git 2.30 or newer.
- **Python**: Python 3.10 or newer (required to run the `check-md` linter).
- **uv** (Optional, but highly recommended): A fast, modern Python package manager that handles global tool installations seamlessly.

---

## Integration Methods

To adopt LEAP, you must place the LEAP folder into a directory named `leap/` at the root of your repository. Choose one of the two following integration paths.

### Path A: Git Submodule (Recommended)

If your project is managed under a Git repository, adding LEAP as a submodule is the recommended approach. This isolates LEAP's code and tooling while keeping it simple to pull updates.

#### 1. Add Submodule

Run one of the following commands in your project's root directory, depending on your preferred protocol:

Using HTTPS (Standard):

```bash
git submodule add https://github.com/blunderstone/leap.git leap
```

Using SSH (For developers with GitHub SSH keys configured):

```bash
git submodule add git@github.com:blunderstone/leap.git leap
```

#### 2. Configure Submodule Updates

By default, Git does not automatically update submodules when pulling changes or switching branches. You can configure Git to automatically update the `leap/` directory by running:

```bash
git config submodule.recurse true
```

#### 3. Pin Submodule to a Stable Release (Highly Recommended)

By default, the submodule tracks the latest development commit on the remote's primary branch (`main`). For team environments and long-term stability, we highly recommend pinning the submodule to a specific stable release tag (e.g., `v1.1.0-beta.0`):

```bash
# Navigate into the submodule directory
cd leap

# Check out the stable release tag
git checkout v1.1.0-beta.0

# Return to your project root and stage the pin update
cd ..
git add leap
git commit -m "chore: pin leap submodule to stable release v1.1.0-beta.0"
```

---

### Path B: Direct Copy / Embedding

If your project does not use Git, or you prefer a flat structure without git submodules, you can embed LEAP by copying the repository files directly.

1. Download the latest release of LEAP from the [LEAP Releases Page](https://github.com/blunderstone/leap/releases).
2. Extract the archive.
3. Move or copy the extracted folder into your project root under the folder name `leap`.

For example, on macOS or Linux:

```bash
cp -R /path/to/extracted/leap leap
```

---

## Interactive Workspace Setup

Once you have instantiated the `leap/` folder via Path A or Path B, you can configure your entire workspace—creating your empty `kb/` directory, installing the `check-md` markdown linter, automatically generating configuration files for your preferred AI agents, and configuring QMD semantic search—using the interactive bootstrapper:

```bash
bash leap/scripts/setup-leap.sh
```

Follow the prompts on your screen. The configurator is designed with safe defaults and will not overwrite any of your custom-written agent guides unless you explicitly give it permission.

---

## Manual Workspace Setup (Reference)

If you prefer to configure your workspace manually instead of using the interactive setup helper, follow these steps after instantiating the `leap/` subdirectory.

### 1. Create your Knowledge Base

Create an empty `kb/` directory at your project root. This is where your custom project documentation, feature goals, plans, and ADRs will reside:

```bash
mkdir kb
```

### 2. Install check-md

Install `check-md` in your project's Python environment from the `leap/` subdirectory.

#### Option A: Global or Tool Installation with uv (Recommended)

If you have `uv` installed, run:

```bash
uv tool install --editable leap/check-md
```

#### Option B: Standard Python Virtual Environment

If you prefer using a virtual environment and standard pip, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e "leap/check-md[dev]"
```

Verify that the linter was successfully installed:

```bash
check-md --help
```

### 3. Configure QMD Semantic Search

If you want to enable on-device semantic search over your project's markdown documents so that AI agents can query your knowledge base programmatically, run the QMD configuration script:

```bash
bash leap/scripts/qmd/qmd-config
```

---

## Note for Windows Users

Running `.sh` scripts and setup tooling on Windows requires a Bash-compatible environment. Use one of the following approaches:

### Git Bash (Recommended)

Git Bash comes pre-installed with [Git for Windows](https://git-scm.com/download/win). If you use Git, you almost certainly already have Git Bash installed.

1. Open Git Bash.
2. Navigate to your project directory.
3. Run the interactive setup command:
   ```bash
   bash leap/scripts/setup-leap.sh
   ```

### Windows Subsystem for Linux (WSL)

If you are developing inside a Linux distribution under WSL (e.g., Ubuntu):

1. Open your WSL terminal.
2. Ensure Python 3.10+ is installed in your WSL environment (`sudo apt install python3 python3-pip`).
3. Run the setup script:
   ```bash
   bash leap/scripts/setup-leap.sh
   ```

### PowerShell / CMD (Manual Setup Only)

If you do not have Git Bash or WSL, you cannot run the `.sh` shell scripts directly. Instead, configure your workspace manually using PowerShell or Command Prompt:

1. Create the `kb` directory:
   ```powershell
   New-Item -ItemType Directory -Path kb
   ```

2. Install `check-md`:
   ```powershell
   pip install -e .\leap\check-md[dev]
   ```

3. Manually create your AI agent integration files (e.g., `CLAUDE.md`, `GEMINI.md`) by copying the templates provided in the [AI Agent Integration](#ai-agent-integration) section of the main `README.md`.

---

## Verification & Next Steps

To verify that your workspace is fully LEAP-compliant, run the markdown linter against your newly created `kb/` directory:

```bash
check-md kb/
```

If the linter exits with no errors, your workspace setup is verified and complete.

### How to Start a New Task (Agent-First Workflow)

Under the LEAP paradigm, you do not need to run complex Git or file-system commands manually to start working on a task. Instead, you can have your AI assistant bootstrap the environment for you!

Once your workspace setup is complete:

1. **Activate your AI agent** (e.g., Gemini CLI, Claude Code, Cline, or Cursor) inside your repository.
2. **Prompt your agent to initiate the feature**. Use a prompt like:
   ```text
   "We are starting a new task to [brief description]. Please create a feature branch, create our feature directory under kb/feature/, and draft the goals.md file for my review."
   ```

3. **Review and Approve**: Your agent will autonomously check out the branch, create the folder structure, and draft a compliant `goals.md`. Once you approve, instruct the agent to draft the `plan.md` and proceed with the execution phase!

---

## AI Agent Integration Templates

If you choose to configure your workspace manually instead of using the interactive setup script, you must create the necessary agent instruction files in your repository root. These files instruct your AI assistants to follow the **LEAP methodology**—including its documentation-first and testing-first lifecycles, and its structured `kb/` directory layout.

### 1. Claude (CLAUDE.md)

Use this if your team uses **Claude Code**, **Claude CLI**, **Cline**, or **Roo Code**. Create a `CLAUDE.md` file in your repository root with the following contents:

````markdown
# Claude Developer Guide (LEAP Compliant)

This project follows the **Literate (Extended-by-Agent) Programming (LEAP)** methodology. Please respect the following guidelines for all code changes, architecture decisions, and feature implementations.

## LEAP Principles

1. **Documentation First**: Before modifying or creating code, check if there is an active feature branch folder in `kb/feature/<username>/<feature-name>/`.
   - Ensure a `goals.md` exists outlining the requirements.
   - For complex, multi-phase changes, verify there is an execution `plan.md`.
   - Update plans and document phase completions as you work.
2. **Test Throughout**: Write unit and integration tests for every implemented phase. Target 90%+ coverage.
3. **Completion Summary**: Create or update `completion-summary.md` in the feature folder before considering the implementation complete.
4. **Agent-Friendly Style**: All Markdown documents in `kb/` must conform to LEAP Markdown standards (semantic headings, blank line block separation, consecutive metadata `<br>` tags).

## Markdown Compliance (check-md)

Always lint and format markdown documents before finalizing them. This project uses the `check-md` utility.

- **Check files**: `check-md kb/`
- **Auto-fix violations**: `check-md kb/ --fix`

Run `check-md` to verify formatting compliance. Do not bypass markdown errors.

## Build and Test Commands

List your project-specific build and test commands here.
For example:
- **Build**: `npm run build` or `cargo build`
- **Test**: `npm run test` or `cargo test`
````

### 2. Gemini & Antigravity (GEMINI.md)

Use this if your team uses **Gemini CLI** or the next-generation **Antigravity CLI** (`agy`). Both environments natively recognize and parse a root-level `GEMINI.md` file on startup to guide agent behavior. Create a `GEMINI.md` in your repository root with the following contents:

````markdown
# Gemini & Antigravity Developer Guide (LEAP Compliant)

This project adopts the **Literate (Extended-by-Agent) Programming (LEAP)** paradigm. Every task must be carried out following our documentation-first and testing-first lifecycle.

## LEAP Paradigm Guidelines

1. **Knowledge Retrieval**: Always scan the project's root `kb/` directory first. Familiarize yourself with design constraints, guide documents (`leap/kb/guide-*.md`), and implementation blueprints (`leap/kb/impl-*.md`).
2. **Feature Branch Lifecycle**:
   - Locate your feature directory at `kb/feature/<username>/<feature-name>/`.
   - Read `goals.md` and `plan.md` before coding.
   - Author detailed phase journals (`phase-1.md`, etc.) for complex features.
   - Document a comprehensive summary in `completion-summary.md` on completion.
3. **Testing Rigor**: All code edits must be backed by automated test coverage. Proactively run the test commands.
4. **Markdown Standards**: Markdown files must strictly comply with `check-md` Rules 1-5.

## Tooling Commands

- **Check MD Compliance**: `check-md kb/`
- **Auto-Fix MD Errors**: `check-md kb/ --fix`
- **Build Project**: [Insert project build command]
- **Run Tests**: [Insert project test command]
````

### 3. GitHub Copilot (.github/copilot-instructions.md)

Use this to ensure **GitHub Copilot Chat** is aware of LEAP. Copilot automatically parses `.github/copilot-instructions.md` to align answers with your guidelines. Create a `.github/copilot-instructions.md` in your repository root with the following contents:

````markdown
# GitHub Copilot Custom Instructions (LEAP Compliant)

This project follows the **Literate (Extended-by-Agent) Programming (LEAP)** methodology. Please respect the following guidelines for all code changes, architecture decisions, and feature implementations.

- **Documentation First**: Always respect and follow requirements and plans inside the `kb/` directory, specifically `kb/feature/<username>/<feature-name>/goals.md` and `plan.md`.
- **Markdown Standards**: Ensure markdown changes comply with check-md standards:
  - Separate block elements with empty lines.
  - Use proper headings (# for title, ##, ###, etc.) instead of bold text.
  - Use <br> tags for consecutive metadata lists.
- **Testing**: Maintain high test coverage (90%+). Proactively verify code behaves correctly.
````

### 4. Cursor & Windsurf (.cursorrules)

Use this if your team uses the **Cursor** or **Windsurf** IDEs. These editors read `.cursorrules` to enforce contextual boundaries for inline agents and chat sidebars. Create a `.cursorrules` in your repository root with the following contents:

````markdown
# Cursor Rules (LEAP Compliant)

This project follows the **Literate (Extended-by-Agent) Programming (LEAP)** methodology. Please respect the following guidelines for all code changes, architecture decisions, and feature implementations.

- **Documentation First**: Always check `kb/feature/<username>/<feature-name>/goals.md` and `plan.md` before modifying or creating code.
- **Markdown Standards**: Ensure markdown files comply with check-md rules (proper headings, blank lines around code blocks/lists, <br> for metadata). Run `check-md kb/ --fix` to verify.
- **Testing**: Proactively write unit and integration tests. Target 90%+ coverage.
````
