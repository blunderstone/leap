# Standardize File Header Comments Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** August 24, 2026

---

## Quick Summary

Sweep the entire repository to define, audit, and ensure that all Python and Shell files have standard, consistent, and correct file header comments suitable for open-sourcing.

## Executive Summary

As we prepare the LEAP repository for public open-sourcing and release, maintaining a professional, compliant, and well-documented codebase is paramount. Standardizing source file headers is a key aspect of this preparation. Every source file should clearly communicate its name, its primary purpose, its author, and copyright/license information if necessary.

Currently, the codebase has file headers in various styles: some Python files have docstrings with author URLs, some scripts have plain text shebang-adjacent descriptions, and others have no header comments at all. This feature will:
1. Define clear, standardized templates for both Python (docstring-based) and Shell (comment-based) header blocks.
2. Perform a comprehensive sweep/audit of all source and test files in the repository.
3. Update existing headers and insert new headers where missing, ensuring that file names and purpose descriptions are exact, consistent, and fully accurate.
4. Ensure shebangs and file execution integrity are strictly preserved.

## Risk and Complexity Assessment

**Overall Risk:** LOW

Updating header comments carries very low risk as it does not modify runtime or business logic. The primary risk is breaking shebang placement (which must be at the very first line of a script) or introducing syntax errors in docstrings.

**Overall Complexity:** LOW

The task is conceptually simple but requires a meticulous, systematic sweep across all 26+ Python files and various Shell scripts in the repository.

## Objectives

1. Define the standardized header templates for Python files and Shell files.
2. Conduct a comprehensive repository audit to locate all Python (`.py`) and Shell (`.sh` or extensionless executable) files.
3. Apply standard headers to all identified files, ensuring they are consistent, complete, and accurate.
4. Validate that all modifications are syntactically valid, scripts remain executable, and existing tests continue to pass.

## Requirements

### Functional Requirements

- **REQ-1:** Define standardized, open-source-ready header block templates for Python files and Shell scripts.
- **REQ-2:** The standardized headers must include:
  - File name
  - Brief description of the file's purpose
  - Consistent author line: `Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)`
  - Apache License, Version 2.0 copyright and license boilerplate notice to protect IP.
- **REQ-3:** Audit and update all Python source files in `check-md/src/check_md/`.
- **REQ-4:** Audit and update all Python test files in `check-md/tests/`.
- **REQ-5:** Audit and update all Python and Shell scripts/tests in `scripts/` (e.g., `install-skills.py`, `setup-leap.sh`, `scripts/tests/test_install_skills.py`).
- **REQ-6:** Audit and update all Shell scripts in `scripts/qmd/` (including extensionless scripts like `pre-commit-qmd`, `qmd-config`, etc.).
- **REQ-7:** Shebang lines (`#!/usr/bin/env...`) must remain at line 1 of any script, preceding any header comment block.

### Non-Functional Requirements

- **Formatting Compliance:** Header docstrings/comments must not violate any `check-md` rules or standard style guides.
- **Syntactic Correctness:** All Python docstrings must be valid Python string literals (e.g., `"""triple-quoted"""`), and no shell script syntax errors should be introduced.
- **No Functional Changes:** The changes must be purely documentation-based with absolutely zero runtime/functional impact.

### Testing Requirements

- **Regression Testing:** Run the existing Python tests in `check-md/tests/` to verify zero functional impact.
- **Linter Check:** Run `check-md` across the repository to ensure no markdown formatting violations are introduced within the header blocks.
- **Execution Verification:** Verify that modified executable scripts (e.g., `install-skills.py`, `setup-leap.sh`, etc.) continue to run successfully.

### Documentation Requirements

- Document the standardized header format templates in the feature's `plan.md`.

## Success Criteria

- [ ] Standard header templates for Python and Shell files are formally defined.
- [ ] Every Python file in `check-md/src/check_md/`, `check-md/tests/`, and `scripts/` has a compliant, standardized header.
- [ ] Every Shell script in `scripts/` and `scripts/qmd/` has a compliant, standardized header.
- [ ] All existing tests in `check-md` pass cleanly.
- [ ] `check-md` runs cleanly over the modified repository files.
- [ ] All modified executable scripts run successfully without regression.

## Constraints

- **Shebang placement:** Shebangs must occupy line 1 exactly.
- **No external dependencies:** Do not introduce any new library or tool dependencies for comments.

## Assumptions

- Standardizing headers will not break any existing packaging or distribution of `check-md`.
- All Python files are safe to modify without affecting Python's internal docstring harvesting (such as for `__doc__` commands or help CLI).

## Out of Scope

- Autogenerating headers via a git hook or custom command (to be considered as a separate feature if needed).
- Adding headers to markdown files themselves (markdown files are governed by the LEAP document taxonomy and `check-md` standards, which are out of scope for this sweep).
