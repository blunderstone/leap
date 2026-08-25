# Obsolete ADR 008 Cleanup and Markdown Capitalization Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-25

---

## Quick Summary

Clean up all obsolete references to "ADR 008" across the codebase and standardise the capitalization of "Markdown" as a proper noun in all prose and documentation.

## Executive Summary

The project's markdown formatting standards are officially governed by ADR 002 (`leap-adr-002__markdown-formatting-standards.md`). However, numerous legacy references to "ADR 008" (a previous designation) persist across the linter tool `check-md` (including its codebase, tests, pyproject.toml, and template files) and some files in the root/knowledge base. This discrepancy is confusing for developers and should be modernized to point directly to ADR 002.

Additionally, the term "Markdown" should be consistently treated as a proper noun in all English prose and documentation across the codebase. Lowercase uses of "markdown" (e.g. "markdown linter", "markdown files") will be capitalized to "Markdown" (e.g. "Markdown linter", "Markdown files"), while keeping command names, file extensions, URLs, and code identifiers unchanged.

## Objectives

1. Replace all legacy, obsolete references to "ADR 008" with "ADR 002" across all files (source code, tests, documentation, templates).
2. Standardize the capitalization of "Markdown" as a proper noun across all repository prose, including linter output logs, template comments, and documentation.
3. Ensure 100% test coverage and validation of `check-md` after these updates.
4. Verify that all updated Markdown documents are completely compliant with the LEAP linter standards.

## Requirements

### Functional Requirements

- **REQ-1 (Purge ADR 008):** Update every reference to "ADR 008" or "ADR-008" across the entire repository.
  - In public-facing messages (such as CLI help descriptions, user logs, pre-commit hook templates, and package descriptions), refer to it as **"LEAP ADR 002"** (instead of just "ADR 002") to ensure users understand the context.
  - In code identifiers, comments, and internal docstrings, update "ADR 008" to "LEAP ADR 002" or "ADR 002" as appropriate.
  - This includes:
    - Linter implementation code (`check-md/src/check_md/rules.py`, `check-md/src/check_md/cli.py`, etc.)
    - Tests (`check-md/tests/`)
    - Integration templates (`check-md/templates/`)
    - Build/package configuration (`check-md/pyproject.toml`)
    - Documentation files (such as `kb/adr/leap-adr-002__markdown-formatting-standards.md` and `check-md/WORKFLOW-DEMONSTRATION.md`)
- **REQ-2 (Capitalize Markdown):** Audit and capitalize "markdown" to "Markdown" as a proper noun in all natural language text (documentation, comments, help strings, CLI output logs, templates).
  - Code identifiers (such as variables, function names, types, e.g. `markdown_lines`), command executions (like `check-md`), file extensions (`.md`), URLs, and path names should not be changed where it would cause syntax or execution errors.

### Non-Functional Requirements

- All modified Markdown files must strictly pass `check-md kb/` linter checks with zero violations.
- Maintain high-quality, professional English formatting throughout all altered documentation.

### Testing Requirements

- Run all existing `check-md` tests to verify that no functional behavior was broken.
- Ensure that the tests are updated to assert on "ADR 002" and "Markdown" consistently.
- Run `scripts/run-all-checks.sh` or equivalent check tools to verify overall health.

### Documentation Requirements

- Cleanly document this transition in the feature documentation folder.

## Success Criteria

- [x] Every reference to "ADR 008" or "ADR-008" is updated to "ADR 002" or "ADR-002" across the codebase.
- [x] Natural language occurrences of "markdown" are capitalized to "Markdown" across all documentation and source code prose.
- [x] No regression in linter functionality: all Python tests pass successfully.
- [x] All modified Markdown files pass the `check-md` linter with zero errors.

## Constraints

- Changes must be backward compatible and not affect existing linter command usage (such as running `check-md`).
- Code names and system paths must remain valid.

## Assumptions

- "ADR 002" is the correct, definitive reference for Markdown formatting standards.

## Out of Scope

- Refactoring of rules logic that is not related to ADR numbering or proper-noun capitalization.
- Downstream repository submodules (they will receive updates via git).
