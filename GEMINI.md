# LEAP Repository & Agent Conventions

This document outlines repo-specific conventions, development guidelines, and commands for both human developers and AI coding agents.

---

## Development Commands

### Markdown Validation (check-md)

`check-md` is a fast Python-based Markdown linter that enforces the five LEAP documentation rules. It is globally installed and can be run **directly** from any directory in the workspace:

- **Check specific directory/file:** `check-md kb/` or `check-md kb/guide-document-taxonomy.md`
- **Auto-fix violations:** `check-md kb/ --fix`
- **Verify staged files (for pre-commit):** `check-md --staged`

---

## AI Workspace Skills & Phase Gating

If specialized workspace skills are available (e.g., `leap-start`, `leap-dev`, `leap-pr`, `leap-handoff`, `leap-finish`), you **MUST** prioritize activating and following them.

### Concise Fallback Gating

If workspace skills are not active, you must follow these core guidelines:

- **Documentation First:** Review goals (`goals.md`) and execution phases (`plan.md`) before writing any code.
- **Sequential Phase Gating:** Implement only one planned phase at a time. After completing a phase, halt and wait for explicit human review and approval before starting on the next.
- **TDD Rigor:** Write tests during each phase (TDD). Maintain a target of 90%+ coverage.

---

## Architectural Guidelines

- Refer to `kb/guide-document-taxonomy.md` for naming and organization rules.
- Refer to `kb/template-adr.md` for Architecture Decision Records (ADRs).
- Refer to `kb/guide-methodology.md` for feature branch lifecycle and Gating Mandates for AI Agents.

---

## Metadata & Formatting Standards

- **Date Formatting:** Always format dates using the ISO 8601 standard (`YYYY-MM-DD`) across all markdown documents (such as goals, plans, completion summaries, ADRs, and guides) instead of natural-language or localized formats (e.g., 'Thursday, August 27, 2026').
