# Standardize File Header Comments Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** August 24, 2026

---

## Overview

This implementation plan outlines the systematic strategy to audit, standardise, and verify file header comments across all Python and Shell files in the LEAP repository. We will establish clear formatting templates for Python files and Shell scripts, audit every source file, update existing headers, insert missing ones, and thoroughly validate the entire workspace for compliance and syntactic correctness.

**Development Approach:** Use Test-Driven Development (TDD) / Test-First validation. Before modifying each file set, we will confirm existing tests pass. After making surgical updates, we will run both compiler/syntax checks, linter checks (`check-md`), and execute relevant verification tests to guarantee zero regression or functional impact.

### Overall Assessment

- **Complexity:** LOW - The task is conceptually simple, consisting entirely of non-functional documentation adjustments.
- **Risk:** LOW - No business or application logic is affected. The only risk is breaking a shebang or introducing a docstring syntax error, which will be caught by automated validation checks.

---

## Standardized Header Templates

### 1. Python File Header Template

All Python files (`.py`) must begin with a triple-quoted docstring. If a shebang line exists, it must occupy line 1, followed by a single blank line, and then the docstring.

```python
"""
<filename> — <short description of the file's purpose>

<Optional: longer description or usage instructions if helpful>

Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)

Copyright 2026 Blunderstone LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
```

### 2. Shell/Bash Script Header Template

All Shell scripts (`.sh` or extensionless executable scripts) must use `#` comments for the header. If a shebang line exists, it must occupy line 1, followed by a single blank line, and then the header comment block.

```bash
#!/usr/bin/env bash
# <filename> — <short description of the script's purpose>
#
# <Optional: longer description or usage instructions if helpful>
#
# Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)
#
# Copyright 2026 Blunderstone LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```

---

## Phase 1: Audit and Standardize Python Package Source Files

### Goals

- Define standard header blocks (detailed above).
- Create a standardized, copy-pasteable `COPYRIGHT` template file at the repository root.
- Audit and standardize all Python files in the primary package folder `check-md/src/check_md/`.
- Verify package integrity and ensure python compiles cleanly.

### Approach

1. Verify that the Python package tests are currently passing.
2. For each Python file under `check-md/src/check_md/`:
   - `__init__.py`
   - `__main__.py`
   - `checker.py`
   - `cli.py`
   - `config.py`
   - `fixer.py`
   - `formatting.py`
   - `models.py`
   - `rules.py`
   - `scorer.py`
3. Edit the file to replace or insert the standardized docstring header at the top, ensuring proper description, file name, and author details.
4. Run python compilation checks and verify tests.

### Testing

- Run python compiler syntax check on edited files (e.g. `python -m py_compile`).
- Run `check-md` over the modified python files to ensure docstring markdown formatting is clean.
- Run `pytest` to ensure zero functional regressions are introduced.

### Success Criteria

- [x] A standardized `COPYRIGHT` template file is created at the repository root.
- [x] All 10 Python files under `check-md/src/check_md/` have standard, accurate header docstrings.
- [x] No syntax or import errors exist.
- [x] `check-md` runs clean on all modified files.
- [x] All package test suites pass successfully.

---

## Phase 2: Audit and Standardize Python Tests & Scripts

### Goals

- Audit and standardize all Python test files in `check-md/tests/`.
- Audit and standardize all Python scripts and tests in the `scripts/` directory (e.g. `install-skills.py` and `scripts/tests/test_install_skills.py`).

### Approach

1. For each Python test file in `check-md/tests/`:
   - `__init__.py`
   - `test_checker.py`
   - `test_cli.py`
   - `test_config.py`
   - `test_fixer.py`
   - `test_ignore_comments.py`
   - `test_main.py`
   - `test_models.py`
   - `test_rule1_semantic_headings.py`
   - `test_rule2_block_separation.py`
   - `test_rule3_heading_increment.py`
   - `test_rule4_nested_code_blocks.py`
   - `test_rule5_label_value_sequences.py`
   - `test_scorer.py`
2. For each Python file/test in `scripts/`:
   - `scripts/install-skills.py` (Must preserve shebang)
   - `scripts/tests/test_install_skills.py`
3. Edit files to insert/align with the standardized python header format.

### Testing

- Compile all edited python files using `python -m py_compile`.
- Run the full pytest suite (`pytest check-md/tests/` and `pytest scripts/tests/`).
- Run `check-md` on the updated files to ensure markdown compatibility.

### Success Criteria

- [x] All 14 Python test files in `check-md/tests/` have the standardized header format.
- [x] Both python scripts (`scripts/install-skills.py` and `scripts/tests/test_install_skills.py`) have the standardized header format, preserving shebangs where applicable.
- [x] `pytest` passes 100%.
- [x] `check-md` runs clean.

---

## Phase 3: Audit and Standardize Shell/Bash Scripts

### Goals

- Audit and standardize all Shell/Bash scripts (`.sh` and extensionless scripts) across the workspace.

### Approach

1. Locate and audit all Shell script files:
   - `scripts/setup-leap.sh`
   - `scripts/qmd/tests/qmd-config.test.sh`
   - `scripts/qmd/pre-commit-qmd` (extensionless)
   - `scripts/qmd/pre-commit-qmd.wrapper` (extensionless)
   - `scripts/qmd/qmd-config` (extensionless)
   - `scripts/qmd/qmd-config.wrapper` (extensionless)
   - `scripts/qmd/qmd-refresh` (extensionless)
2. Update/insert standardized comment-based headers, ensuring the shebang is kept at line 1.
3. Validate script syntax and execute script-based test runners.

### Testing

- Run `bash -n` to perform syntax checking on each modified script.
- Execute script-based tests: `bash scripts/qmd/tests/qmd-config.test.sh`.
- Run a dry-run or verification of `setup-leap.sh`.
- Run `check-md` on updated files.

### Success Criteria

- [ ] Every bash script in `scripts/` and `scripts/qmd/` has standard, accurate, and consistent header comments.
- [ ] Shebang lines are perfectly preserved at line 1.
- `qmd-config.test.sh` passes successfully.
- [ ] `check-md` runs cleanly on all modified script files.

---

## Risk Mitigation

### Risk 1: Shebang Misplacement
If a shebang line (`#!/usr/bin/env bash` or `#!/usr/bin/env python3`) is moved below the header comment block, the operating system will not recognize the script as executable with the appropriate interpreter.

#### Mitigation
We must strictly verify that the shebang remains at line 1 of any script during the edits, and we will perform immediate syntax/execution checks after editing.

### Risk 2: Docstring Markdown Linter Violations
Python docstrings are treated as markdown by some checkers or editors, and running `check-md` on Python files could flag violations (e.g. if we have nested backticks or bad spacing inside docstrings).

#### Mitigation
We will run `check-md kb/` and `check-md check-md/src` and other folders to verify that our header docstrings are perfectly compliant with the linter rules.

---

## Decision Points

### After Phase 1

- Proceed to Phase 2 if all `check-md/src/check_md/` files compile, pass existing tests, and comply with the linter.

### After Phase 2

- Proceed to Phase 3 if all python tests and scripts compile, pass existing tests, and comply with the linter.

## Notes

- All changes will be purely docstring/comment additions or corrections; no functional logic, signatures, or exports will be touched.
