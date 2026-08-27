# LEAP: Literate (Extended-by-Agent) Programming™

[![Latest Release](https://img.shields.io/github/v/release/blunderstone/leap?include_prereleases)](https://github.com/blunderstone/leap/releases)

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

To adopt LEAP in your project, choose one of the two standard integration paths. In both cases, your project's custom documentation lives in an empty, root-level `kb/` directory (separate from `leap/kb/`), which the setup script will configure for you automatically.

### Path A: Git Submodule (Recommended)

If your project is managed under Git, run the following single command in your project root to add LEAP as a submodule and launch the interactive configurator:

```bash
git submodule add https://github.com/blunderstone/leap.git leap && bash leap/scripts/setup-leap.sh
```

*(Note: If you use GitHub SSH keys, you can run `git submodule add git@github.com:blunderstone/leap.git leap && bash leap/scripts/setup-leap.sh` instead. To easily pin or update the submodule to a specific release tag, commit, or the `'latest'` stable version while auto-generating LEAP compliance documents, use the automated pinning utility: `bash leap/scripts/pin-leap.sh latest`.)*

### Path B: Direct Copy / Embedding

If you are not using Git or prefer to copy files directly, download the LEAP repository, place it in a folder named `leap` at your project root, and run:

```bash
bash leap/scripts/setup-leap.sh
```

---

### Advanced Installations & Troubleshooting

For more details on custom configurations, manual workspace setup, and environments like Windows, refer to our comprehensive guide:

- **[LEAP Installation & Setup Guide](kb/guide-installation.md)**: Prerequisites, manual setups, Windows troubleshooting, and verification.

---

## AI Agent Integration

For LEAP to succeed, the AI agents operating in your workspace must be explicitly instructed to follow the **LEAP methodology**—including its documentation-first and testing-first lifecycles, and its structured `kb/` directory layout.

The interactive `setup-leap.sh` configurator will **automatically generate** pre-configured agent instruction files in your repository root during setup. It supports:

- **Claude** (`CLAUDE.md`): For Claude Code, Cline, and Roo Code.
- **Gemini & Antigravity** (`GEMINI.md`): For Gemini CLI and Antigravity CLI.
- **GitHub Copilot** (`.github/copilot-instructions.md`): For Copilot Chat.
- **Cursor & Windsurf** (`.cursorrules`): For AI-powered IDEs.

*(If you choose to configure your workspace manually, the raw template blocks for these agent instruction files can be found in our [LEAP Installation & Setup Guide](kb/guide-installation.md#ai-agent-integration-templates).)*

---

## More Information

For a complete explanation of the methodology, compliance requirements, and guides, refer to the following resources in the `kb/` directory:

- **[LEAP Methodology Guide](kb/guide-methodology.md)**: Comprehensive deep dive into LP history, agent workflows, and core principles.
- **[LEAP Cheatsheet](kb/guide-cheatsheet.md)**: Quick reference for branch names, folders, and markdown standards.
- **[Compliance Levels](kb/guide-compliance-levels.md)**: Essential, Standard, and Comprehensive criteria.
- **[Markdown Formatting Standards ADR](kb/adr/leap-adr-002__markdown-formatting-standards.md)**: Detailed reasoning behind `check-md` rules.
- **[QMD Configuration Guide](kb/guide-qmd-config.md)**: Setup instructions for semantic search.
- **[Changelog](CHANGELOG.md)**: Automated release and version history driven by Conventional Commits.

---

## License & Contribution

This project is licensed under the terms of **The Apache License, Version 2.0** (see [`LICENSE`](LICENSE)).

By contributing to this repository, you agree that your submissions are governed by the terms outlined in our [Contributing Guide](CONTRIBUTING.md#contribution-licensing-agreement-implicit-cla).

---

## Trademark Notice

LEAP™ and Literate (Extended-by-Agent) Programming™ are trademarks of [Blunderstone LLC](https://blunderstone.com).

