# Obsolete ADR 008 Cleanup and Markdown Capitalization Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-25

---

## Overview

This implementation plan outlines the systematic cleanup of the obsolete ADR 008 references across the LEAP codebase, and the standardization of "Markdown" as a proper noun with correct capitalization. 

**Development Approach:** We will use Test-Driven Development (TDD) principles. First, we will adjust the test cases in `check-md` to reflect the expected "ADR 002" references and proper "Markdown" capitalization. Next, we will implement the changes in the linter rules, CLI help text, integration templates, and documentation, ensuring the updated tests pass (Red-Green-Refactor). Finally, we will run the global check suite to confirm all modified Markdown files comply with our linter.

### Overall Assessment

- **Complexity:** LOW - Simple text/prose replacement, but requires extreme care to avoid breaking code syntax, variables, command names, file extensions, or URLs.
- **Risk:** LOW - Self-contained documentation and linter text updates. No functional behavior changes are being introduced to linter parsing logic.

---

## Phase 1: Obsolete ADR 008 Purge

### Goals

- Replace all occurrences of "ADR 008" and "ADR-008" with "ADR 002" and "ADR-002" across the entire repository.
- Ensure the `check-md` linter correctly displays references to "ADR 002" in help text, comments, rules, and error messages.
- Update package definition files and integration templates to point to ADR 002.
- Keep tests passing perfectly under the updated references.

### Approach

- Identify all files referencing "ADR 008" or "ADR-008".
- Update the linter CLI help and Rule definitions in `check-md/src/check_md/`.
- Update the test suite assertions in `check-md/tests/` to expect the updated "ADR 002" phrasing (especially Rule 3 tests containing historical Claude compliance patterns).
- Update integration templates (e.g., `pre-commit`, `Jenkinsfile`) and build configurations (e.g., `pyproject.toml`).
- Update related documentation files (e.g., `WORKFLOW-DEMONSTRATION.md` and `kb/adr/leap-adr-002__markdown-formatting-standards.md`).

### Testing

- Run the pytest suite in `check-md/` to verify correctness.
- Ensure tests validating "ADR 002" compliance rules run and pass successfully.

### Success Criteria

- [ ] Every "ADR 008" / "ADR-008" reference is purged and updated to "ADR 002" / "ADR-002" across python source code, config files, test cases, templates, and documentation.
- [ ] All `check-md` test suites pass cleanly.

---

## Phase 2: Proper Noun "Markdown" Capitalization

### Goals

- Capitalize natural language occurrences of "markdown" to "Markdown" across all documentation, source code comments, CLI outputs, help strings, and templates.
- Enforce strict separation between code syntax (e.g. `markdown_lines`, `.md` extension, `check-md` executable) and proper English prose (e.g. "Markdown files", "Markdown linter").

### Approach

- Conduct a targeted sweep for occurrences of lowercase "markdown" in help texts, logs, and markdown files.
- Replace lowercase "markdown" with proper-case "Markdown" where it represents the language name.
- Carefully skip code-level constructs (e.g., packages, imports, command names, variables) to ensure zero compilation or execution regressions.
- Run `check-md --staged` and `check-md kb/` to ensure all modified knowledge base files comply with local style rules.

### Testing

- Execute all python tests to ensure no unintentional syntax issues or broken logging checks.
- Verify CLI outputs of `check-md --help` display capitalized "Markdown" consistently.

### Success Criteria

- [ ] Capitalization of "Markdown" is standardized as a proper noun across all prose in the repository.
- [ ] All tests in `check-md` pass successfully.
- [ ] All modified documentation files pass `check-md` validation with zero errors.
