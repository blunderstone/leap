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

---

## Conventional Commit Guidelines

LEAP is a Literate Programming framework. Structured Markdown files (such as ADRs, templates, and guides) are primary deliverables of the repository. To ensure our automated release workflow handles documentation and development commits appropriately, all contributors must follow these guidelines:

### Release-Triggering Prefixes (`feat` / `fix`)

Only `feat(...)` and `fix(...)` conventional commits trigger automated releases and version bumps.

- **Framework Deliverables:** When adding or updating primary documentation deliverables (such as standardized templates, architectural guidelines, or core guides under `kb/`), use release-triggering prefixes:
  - `feat(kb): add guide for ...`
  - `feat(templates): create template for ...`
  - `fix(kb): correct instructions in ...`
- **Application Code:** Use standard prefixes for Python tool or codebase changes:
  - `feat(cli): add new rule ...`
  - `fix(checker): resolve parsing bug in ...`

### Non-Release-Triggering Prefixes (`docs` / `chore` / `refactor` / etc.)

These prefixes are visible in the changelog (if configured) but **do not** trigger a release.

- **Auxiliary Documentation:** Use the raw `docs(...)` or `docs:` prefix *only* for auxiliary, non-release-worthy changes (e.g., correcting typos, formatting files, or updating repository-level READMEs):
  - `docs(readme): update installation instructions`
  - `docs: fix typo in CONTRIBUTING.md`
- **Refactoring & Workflow:** Use `refactor(...)` or `chore(...)` for maintenance and tooling changes:
  - `refactor(checker): simplify rules engine`
  - `chore(deps): bump dependencies`

### Strict Ephemeral Directory Rules

- **Drafting & Development:** Commits modifying files in ephemeral directories (such as `kb/feature/` where goals, plans, and completion summaries are drafted) **MUST NEVER** use `feat` or `fix` prefixes.
- **Allowed Prefixes:** Always use non-release-triggering prefixes for ephemeral drafts, such as:
  - `chore(workflow): establish goals for <feature>`
  - `docs(workflow): draft implementation plan for <feature>`

