# LEAP: Literate (Extended-by-Agent) Programming

**Status:** Stable<br>
**Author:** F. Andy Seidl<br>
**Date:** 2026-08-08

---

## Overview

**Literate (Extended-by-Agent) Programming (LEAP)** is a modern, AI-centric evolution of Donald Knuth's foundational concept of Literate Programming. Where traditional LP relied on complex, specialized compilation tools (like WEB, noweb, or Docco) to weave together source code and documentation, LEAP leverages conversational AI coding agents (such as Claude, Gemini, GPT) to naturally bridge explanation, intent, and implementation.

With LEAP, documentation and code co-evolve through an iterative, agent-friendly development lifecycle. By structuring your project's knowledge base and instructing your AI assistants to recognize and respect it, you ensure that your codebase remains fully comprehensible, maintainable, and aligned for both human engineers and AI coding agents.

### Core Principles

- **Documentation First**: Define feature goals and execution plans before writing a single line of implementation code.
- **Iterative Refinement**: Code in discrete, logical phases with clear verification checkpoints.
- **Test Throughout**: Maintain high unit test and integration coverage (targeting 90%+) at every phase.
- **Transparent Evolution**: Track design decisions, architecture choices, and deferred technical debt in real time.
- **Agent-Friendly Conventions**: Style markdown consistently so that parsing, indexing, and LLM comprehension are frictionless.

---

## Key Components

The LEAP repository contains three key pillars to bootstrap your project's agent-extended development workflow:

### 1. Knowledge Base (kb) Layout and Templates

A standardized directory structure for maintaining usage guides, architecture specifications, Architecture Decision Records (ADRs), and feature development progress.

- **`kb/guide-*.md`**: End-user or developer usage documentation (APIs, CLI syntax, configuration).
- **`kb/impl-*.md`**: Technical design and implementation details (algorithms, data structures).
- **`kb/adr/`**: Architecture Decision Records to track the "why" behind system design.
- **`kb/feature/<username>/<feature-name>/`**: Standardized directory containing the goals, plans, and completion summaries of active features.
- **Templates**: Pre-structured markdown templates for goals, plans, ADRs, tech debt, and more, located directly in `leap/kb/template-*.md`.

### 2. check-md (Markdown Linter)

A fast, Python-based CLI tool located in `/check-md` that ensures your documentation conforms to strict CommonMark and agent-friendly guidelines. It enforces five core formatting rules:

- **Rule 1: Semantic Headings**: Structure documents using proper markdown headings (`#`, `##`, etc.) instead of bold text, facilitating document outlines and outline-based navigation.
- **Rule 2: Block Separation**: Separate all block elements (lists, code blocks, blockquotes, tables) from preceding paragraph text with empty lines to prevent visual wrapping or rendering errors.
- **Rule 3: Heading Level Increment**: Maintain sequential heading hierarchy; never skip heading levels (e.g., from `##` to `####`).
- **Rule 4: Nested Code Blocks**: Correctly escape and nest code block formatting when writing documentation that demonstrates code examples.
- **Rule 5: Label-Value Sequences**: Use HTML `<br>` tags rather than implicit spaces or empty lines to group contiguous bold-prefixed metadata lists (e.g., Status, Author, Date).

### 3. Shared QMD Indexing Scripts

On-device semantic search tooling located in `/scripts/qmd` utilizing [QMD](https://github.com/tobi/qmd) to build local full-text search indexes of your documentation, allowing AI agents to query your knowledge base programmatically.

---

## Getting Started

To adopt LEAP in your project, choose one of the two standard integration models to place LEAP inside a `leap/` subdirectory:

- **Git Submodule (Recommended)**: Ideal for Git-based repositories. Keeps the LEAP codebase, formatting rules, and search scripts isolated and easy to update.
- **Embedding / Copying**: Ideal for non-Git repositories or projects requiring a flat directory structure. Just download and copy the LEAP folder into your codebase.

In both cases, your project's custom documentation lives in an empty, root-level `kb/` directory (separate from `leap/kb/`), which does not need to be pre-populated.

### Interactive Workspace Setup (Recommended)

After instantiating the `leap/` directory (via Submodule or Embedding), you can configure your entire workspace—creating the `kb/` folder, installing the `check-md` linter, automatically generating configuration files for your preferred AI agents, and setting up QMD semantic search—with a single interactive setup script:

```bash
# 1. Instantiate the leap/ folder
# EITHER via Git Submodule:
# SSH (Recommended for developers with GitHub SSH keys):
git submodule add git@github.com:faseidl/leap.git leap
# HTTPS (Alternative):
git submodule add https://github.com/faseidl/leap.git leap

# OR via Embedding (copying files in):
cp -R /path/to/downloaded/leap leap

# 2. Run the interactive workspace configurator
bash leap/scripts/setup-leap.sh
```

#### Note for Windows Users

Running `.sh` scripts on Windows requires a Bash-compatible shell:

- **Git Bash (Recommended)**: Comes pre-installed with [Git for Windows](https://git-scm.com/download/win). If you are using Git, you almost certainly already have this. Open Git Bash and run the commands exactly as shown.
- **Windows Subsystem for Linux (WSL)** or **MSYS2**: Run the commands inside your active Linux distribution or shell.
- **PowerShell / CMD**: If you do not have a Bash environment, you can configure your workspace manually using standard Windows commands (e.g., `mkdir kb`, `pip install -e .\leap\check-md`) by following the [Manual Workspace Setup](#manual-workspace-setup-reference) section below.

---

### Manual Workspace Setup (Reference)

If you prefer to configure your workspace manually instead of using the setup helper, follow these steps after instantiating the `leap/` subdirectory.

#### 1. Create your Knowledge Base

Create an empty `kb/` directory at your project root:

```bash
mkdir kb
```

#### 2. Install check-md

Install `check-md` in your project's Python environment from the `leap/` subdirectory:

```bash
# Option A: Fast & Modern with uv (Recommended)
uv tool install --editable leap/check-md

# Option B: Standard Python Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
pip install -e "leap/check-md[dev]"
```

Verify the installation:

```bash
check-md --help
```

#### 3. Configure QMD Semantic Search (Optional)

If you wish to configure local semantic search over your project's markdown files, run the QMD configuration script:

```bash
bash leap/scripts/qmd/qmd-config
```

---

## AI Agent Integration

For LEAP to succeed, the AI agents operating in your workspace must be explicitly instructed to find, read, and write documentation within the `kb/` structure. This recognition is accomplished by adding configuration files in your project root.

The `setup-leap.sh` script can automatically generate any of these files for you, or you can create them manually.

### 1. Claude (CLAUDE.md)

Use this if your team uses **Claude Code**, **Claude CLI**, **Cline**, or **Roo Code**.

Create a `CLAUDE.md` file in your repository root with the following contents:

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

Use this if your team uses **Gemini CLI** or the next-generation **Antigravity CLI** (`agy`). Both environments natively recognize and parse a root-level `GEMINI.md` (or `AGENTS.md`) file on startup to guide agent behavior.

Create a `GEMINI.md` in your repository root with the following contents:

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

Use this to ensure **GitHub Copilot Chat** (in VS Code or JetBrains) is aware of LEAP. Copilot automatically parses `.github/copilot-instructions.md` to align answers with your guidelines.

Create a `.github/copilot-instructions.md` in your repository root with the following contents:

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

Use this if your team uses the **Cursor** or **Windsurf** IDEs. These editors read `.cursorrules` (and `.windsurfrules`) to enforce contextual boundaries for inline agents and chat sidebars.

Create a `.cursorrules` in your repository root with the following contents:

````markdown
# Cursor Rules (LEAP Compliant)

This project follows the **Literate (Extended-by-Agent) Programming (LEAP)** methodology. Please respect the following guidelines for all code changes, architecture decisions, and feature implementations.

- **Documentation First**: Always check `kb/feature/<username>/<feature-name>/goals.md` and `plan.md` before modifying or creating code.
- **Markdown Standards**: Ensure markdown files comply with check-md rules (proper headings, blank lines around code blocks/lists, <br> for metadata). Run `check-md kb/ --fix` to verify.
- **Testing**: Proactively write unit and integration tests. Target 90%+ coverage.
````

---

## More Information

For a complete explanation of the methodology, compliance requirements, and guides, refer to the following resources in the `leap/kb/` directory:

- **[LEAP Methodology Guide](leap/kb/guide-methodology.md)**: Comprehensive deep dive into LP history, agent workflows, and core principles.
- **[LEAP Cheatsheet](leap/kb/guide-cheatsheet.md)**: Quick reference for branch names, folders, and markdown standards.
- **[Compliance Levels](leap/kb/guide-compliance-levels.md)**: Essential, Standard, and Comprehensive criteria.
- **[Markdown Formatting Standards ADR](leap/kb/adr/leap-adr-002__markdown-formatting-standards.md)**: Detailed reasoning behind `check-md` rules.
- **[QMD Configuration Guide](leap/kb/guide-qmd-config.md)**: Setup instructions for semantic search.
