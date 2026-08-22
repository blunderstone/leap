# LEAP Repository & Agent Conventions

This document outlines repo-specific conventions, development guidelines, and commands for both human developers and AI coding agents.

---

## Development Commands

### Markdown Validation (check-md)

`check-md` is a fast Python-based markdown linter that enforces the five LEAP documentation rules. It is globally installed and can be run **directly** from any directory in the workspace:

- **Check specific directory/file:** `check-md kb/` or `check-md kb/guide-document-taxonomy.md`
- **Auto-fix violations:** `check-md kb/ --fix`
- **Verify staged files (for pre-commit):** `check-md --staged`

---

## Architectural Guidelines

- Refer to `kb/guide-document-taxonomy.md` for naming and organization rules.
- Refer to `kb/template-adr.md` for Architecture Decision Records (ADRs).
- Refer to `kb/guide-methodology.md` for feature branch lifecycle and Gating Mandates for AI Agents.
