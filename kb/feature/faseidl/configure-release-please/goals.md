# Configure release-please for LEAP Documentation & Methodology Goals

**Author:** [Andy Seidl](https://github.com/faseidl)<br>
**Date:** 2026-08-28

---

## Quick Summary

Configure `release-please` to formally recognize and categorize documentation (ADRs, templates, guides) and refactoring commits as release-worthy, and establish developer commit guidelines in `GEMINI.md`.

## Executive Summary

LEAP is a Literate Programming framework, which means structured Markdown standards, architectural decision records (ADRs), templates, and guides are primary deliverables and features of the repository rather than auxiliary documentation. Standard conventional commit configurations, such as our current `release-please` setup, only recognize `feat(...)` and `fix(...)` as release-triggering and completely filter out `docs(...)` and `refactor(...)` commits.

To resolve this issue, we will implement a dual-action solution:

1. Update `release-please-config.json` with custom `changelog-sections` that formally map `docs` and `refactor` commit types to visible sections in the generated `CHANGELOG.md`.
2. Update the developer conventions in `GEMINI.md` to establish guidelines on using appropriate conventional commit prefixes for LEAP methodology features (`feat(kb):`, `feat(templates):`, etc.) to trigger appropriate releases while reserving the raw `docs(...)` prefix for purely auxiliary, non-release-worthy changes.

## Objectives

1. Configure `release-please` to display documentation changes in the changelog.
2. Establish clear guidelines in `GEMINI.md` for developers on commit prefix usage for LEAP deliverables.
3. Keep the repo release cycle integrated seamlessly with both code and non-code framework features.

## Requirements

### Functional Requirements

- **REQ-1:** Update `release-please-config.json` to configure custom `changelog-sections` that include:
  - `feat` -> "Features"
  - `fix` -> "Bug Fixes"
  - `docs` -> "Documentation Standards & Guides"
  - `refactor` -> "Refactoring & Cleanup"
- **REQ-2:** Update `GEMINI.md` to specify when to use `feat(kb):` or `feat(templates):` (release-triggering) versus raw `docs(...)` (non-release-triggering/auxiliary edits) for documenting framework-level deliverables.
- **REQ-3:** Update `GEMINI.md` to explicitly state that commits to ephemeral directories (such as `kb/feature/`) must NEVER use `feat` or `fix` prefixes, and must always use non-release-triggering prefixes like `chore(workflow):` or `docs(workflow):`.

### Non-Functional Requirements

- **Maintainability:** Standard configurations should remain JSON-schema compliant.
- **Consistency:** Conventions added to `GEMINI.md` must align with existing architectural guidelines and LEAP taxonomy.

### Testing Requirements

- Verify that the `release-please-config.json` changes match the official schema.
- Validate markdown files (`GEMINI.md` and the goals document) using `check-md` to ensure zero violations.

### Documentation Requirements

- All adjustments to developer workflows and commit guidelines must be explicitly documented in `GEMINI.md`.

## Success Criteria

- [x] `release-please-config.json` is updated with a custom `changelog-sections` array.
- [x] `GEMINI.md` is updated with clear developer guidelines on conventional commit prefixes for LEAP-specific deliverables.
- [x] No `check-md` formatting or rules violations in updated or newly created files.

## Constraints

- Standard `release-please` limitations on release triggers: only `feat` and `fix` commits can trigger a release/version bump. This constraint makes the clear separation of `feat(kb):`/`feat(templates):` versus `docs:` essential to enforce.

## Assumptions

- We assume the existing release-please action will respect the custom configuration defined in `release-please-config.json` at the next run.

## Out of Scope

- Modifying the GitHub Actions release workflow files themselves (unless a configuration-related bug requires it).
- Introducing custom commits or release triggers that are not natively supported by `release-please` (e.g. `perf`, `chore`, etc. as release-triggering unless they are standard/easy to map).
