# Open-Source Readiness Cleanup Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-22

---

## Quick Summary

Sanitize the LEAP repository for public, open-source release by purging all proprietary references (specifically "Ghee" project names and "Phase Change Software" corporate entities/emails), resolving license mismatches, and fixing broken documentation links.

---

## Executive Summary

As LEAP prepares for its public open-source debut under Blunderstone LLC, the repository must be audited and cleaned of any legacy artifacts from its initial internal development context. Currently, the codebase contains active references to its origin project (**Ghee**), its original corporate sponsor (**Phase Change Software**), and Andy Seidl's corporate email address (`fseidl@phasechange.ai`). Furthermore, there are internal enterprise publishing URLs, broken links to removed documentation, and a license mismatch in the `check-md` linter's packaging metadata.

By addressing these red and yellow flags in a dedicated feature branch, we will ensure that when the history is squashed for the initial release, the repository will be completely clean, legally sound, and professional.

---

## Objectives

1. Completely eliminate references to the proprietary **Ghee** project family (`ghee-app`, `ghee-server`, `ghee-ui`, `ghee-commons`) and replace them with generic or educational examples.
2. Remove any references to **Phase Change Software** or Andy's former corporate email address, replacing them with personal or Blunderstone-appropriate contact information.
3. Replace all internal enterprise URLs with generic, developer-friendly placeholders.
4. Align the licensing metadata in `check-md` with the parent repository's Apache-2.0 license.
5. Fix broken internal markdown links to ensure 100% navigation integrity.

---

## Requirements

### Functional Requirements

- **REQ-1 (Proprietary Removal):** All instances of the string `Ghee`, `ghee-app`, `ghee-server`, `ghee-ui`, and `ghee-commons` must be replaced in documentation, linter rules, and configuration templates with generic, developer-friendly names (e.g., `your-project`, `your-app`, `sample-service`).
- **REQ-2 (Corporate Affiliation Cleanup):** 
  - Change the author email in `check-md/pyproject.toml` from `fseidl@phasechange.ai` to `andy@seidlweb.com`.
  - Replace GitHub API repository paths in `kb/impl-dependency-security-audit.md` (pointing to `PhaseChangeSoftware/leap`) with clean, generic paths or `blunderstone/leap`.
  - Clean references to `ai.phasechange.ghee` in `check-md/kb/meta/idea-kdoc-validation.md` with generic class paths (e.g., `com.example`).
- **REQ-3 (Internal URL Cleanup):** Change the internal example link `https://docs.internal.company.com/ghee-app/` in `kb/template-leap-settings.md` to a generic, public domain mockup (e.g., `https://docs.yourcompany.com/your-app/`).
- **REQ-4 (License Alignment):** Change the `"License :: OSI Approved :: MIT License"` classifier in `check-md/pyproject.toml` to specify the Apache-2.0 license, ensuring packaging metadata is consistent with the root `LICENSE` file.
- **REQ-5 (Link Resolution):** Fix or remove links to the missing `leap-implementation-guide-ghee.md` file in `kb/best-practices-claude-sessions.md` and `kb/best-practices-tdd.md`.

### Non-Functional Requirements

- All modified Markdown files must strictly pass `check-md kb/` with zero formatting violations.
- Maintain high-quality, professional English and formatting standards throughout all documentation.

### Testing Requirements

- Verify that the modified python files and `check-md` configuration still load and run correctly.
- Run `check-md` to verify that no new formatting issues are introduced.

---

## Success Criteria

- [x] All instances of "Ghee" project references removed or replaced with generic placeholders.
- [x] All Phase Change Software corporate email and name occurrences replaced.
- [x] Example documentation URL pointing to `internal.company.com` updated to a generic domain.
- [x] License classifier in `check-md/pyproject.toml` updated to match Apache-2.0.
- [x] All broken markdown documentation links resolved.
- [x] Linter check `check-md` passes successfully over the entire `kb/` directory.

---

## Constraints

- Changes must be implemented entirely within this feature branch and conform to the project's standard Markdown standards.

---

## Assumptions

- Commits made on this feature branch will be squashed and purged along with historical commits during the final "initial release" preparation.

---

## Out of Scope

- Implementing the final git squashing and purging of commit history (this feature is strictly for the codebase cleanup itself).
- Modifying the core logic of `check-md` or the `setup-leap.sh` configurator.
