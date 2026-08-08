# check-md Workflow Demonstration: Markdown Linting for ADR 008 Compliance

## Purpose

Demonstrates complete workflow for checking markdown files against ADR 008 formatting standards using the check-md CLI tool.

### Scope

Core check-md functionality including file selection, violation detection, output formatting, and CI/CD integration patterns.

#### Author

[F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

#### Date

2025-11-13

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Overview](#overview)
3. [Step 1: Check Single File](#step-1-check-single-file)
4. [Step 2: View Detailed Context](#step-2-view-detailed-context)
5. [Step 3: Check Directory Recursively](#step-3-check-directory-recursively)
6. [Step 4: JSON Output for Tooling](#step-4-json-output-for-tooling)
7. [Step 5: GitHub Actions Format](#step-5-github-actions-format)
8. [Step 6: Filter with Include/Exclude](#step-6-filter-with-includeexclude)
9. [Step 7: Check Staged Files](#step-7-check-staged-files)
10. [Step 8: Compliance Score Report](#step-8-compliance-score-report)
11. [Step 9: Sort Score Report](#step-9-sort-score-report)
12. [Step 10: Enforce Score Threshold](#step-10-enforce-score-threshold)
13. [Business Value Summary](#business-value-summary)
14. [Next Steps](#next-steps)
15. [Troubleshooting](#troubleshooting)

---

## Important: Running Commands

**All commands in this workflow assume you are in the `check-md` directory**. Commands use `..` to reference files in parent directories. This allows you to click the "run" icon next to any command in your IDE and have it execute correctly.

---

## Prerequisites

**Python 3.10+** installed:

```bash
# Verify Python version (must be 3.10 or higher)
python3 --version
```

Expected: Python 3.10.x or higher

### Install check-md

To prevent OS-level environment errors and resolve potential "command not found: pip" issues, install within a virtual environment:

#### Option A: Using Standard Python Virtual Environment

```bash
# 1. Create a virtual environment
python3 -m venv .venv

# 2. Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows (Command Prompt):
.venv\Scripts\activate.bat

# 3. Install in editable mode
pip install -e .
```

#### Option B: Using uv (Recommended)

If you use the `uv` package manager, the easiest way to install `check-md` as a global, standalone command while keeping local changes instantly synchronized is:

```bash
uv tool install --editable .
```

This places the standalone `check-md` executable on your path so you can run it directly from anywhere without virtual environment activation or `uv run` prefixes!

*(Note: Alternatively, you can run `uv sync` to create a local `.venv` and then use `uv run check-md` or run `source .venv/bin/activate`.)*

#### Verify installation

With your virtual environment active, verify that `check-md` is available:

```bash
check-md --help
```

Expected: Help text showing available options

---

## Overview

The **check-md** CLI enforces ADR 008 markdown formatting standards, detecting common issues:

- **Rule 1 (Semantic Headings)**: Detects bold text used instead of proper headings
- **Rule 2 (Block Separation)**: Detects missing blank lines before block elements
- **Rule 4 (Nested Code Blocks)**: Detects improper nested code block fencing

### Business Value

Maintains consistent documentation quality, catches formatting issues early, integrates seamlessly into CI/CD pipelines.

---

### Step 1: Check Single File

Check a single markdown file for violations.

#### Business Value

Quick validation during document authoring, immediate feedback on formatting issues.

#### Command

```bash
check-md ../kb/template-goals.md
```

#### Example Output

```
../kb/template-goals.md
  ../kb/template-goals.md:3: [ADR-002-R1] Bold text with colon may indicate improper heading usage
  ../kb/template-goals.md:15: [ADR-002-R2] Missing blank line before unordered list
  ../kb/template-goals.md:25: [ADR-002-R1] Bold text with colon may indicate improper heading usage

1 files checked
18 violations (15 errors, 3 warnings)
```

#### Expected Results

- Exit code: 1 (violations found)
- Output contains: file path and line numbers
- Output contains: violation rule IDs and messages

---

### Step 2: View Detailed Context

Show detailed context and fix hints for violations.

#### Business Value

Provides actionable guidance for fixing violations, reduces time spent understanding what's wrong.

#### Command

```bash
check-md ../kb/template-goals.md --verbose
```

#### Example Output

```
../kb/template-goals.md
  ../kb/template-goals.md:3: [ADR-002-R1] Bold text with colon may indicate improper heading usage
    Context: **Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
    Fix: Consider: ### Author
  ../kb/template-goals.md:15: [ADR-002-R2] Missing blank line before unordered list
    Context: - Bold text used instead of structural headers
    Fix: Add blank line before this element

1 files checked
18 violations (15 errors, 3 warnings)
```

#### Expected Results

- Exit code: 1
- Output contains: "Context:" and "Fix:" sections
- Output shows the actual line content and suggested fixes

---

### Step 3: Check Directory Recursively

Check all markdown files in a directory tree.

#### Business Value

Validates entire documentation sets, ensures consistency across feature documentation.

#### Command

```bash
check-md ../kb/
```

#### Example Output

```
../kb/template-goals.md
  ../kb/template-goals.md:3: [ADR-002-R1] Bold text with colon may indicate improper heading usage
  ../kb/template-goals.md:15: [ADR-002-R2] Missing blank line before unordered list

../kb/template-plan.md
  ../kb/template-plan.md:3: [ADR-002-R1] Bold text with colon may indicate improper heading usage
  ../kb/template-plan.md:13: [ADR-002-R2] Missing blank line before unordered list

2 files checked
82 violations (64 errors, 18 warnings)
```

#### Expected Results

- Exit code: 1
- Output contains: multiple file paths
- Output shows: file count and total violations

---

### Step 4: JSON Output for Tooling

Generate machine-parseable JSON output for integration with other tools.

#### Business Value

Enables automated processing, integration with issue trackers, dashboards, and reporting tools.

#### Command

```bash
check-md ../kb/template-goals.md --format json
```

#### Example Output

```json
[
  {
    "file": "../kb/template-goals.md",
    "line": 3,
    "rule": "ADR-002-R1",
    "severity": "warning",
    "message": "Bold text with colon may indicate improper heading usage",
    "context": "**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>",
    "fix_hint": "Consider: ### Author"
  },
  {
    "file": "../kb/template-goals.md",
    "line": 15,
    "rule": "ADR-002-R2",
    "severity": "error",
    "message": "Missing blank line before unordered list",
    "context": "- Bold text used instead of structural headers",
    "fix_hint": "Add blank line before this element"
  }
]
```

#### Expected Results

- Exit code: 1
- Output is valid JSON array
- Each violation includes: file, line, rule, severity, message, context, fix_hint

---

### Step 5: GitHub Actions Format

Generate GitHub Actions annotations for CI/CD integration.

#### Business Value

Violations appear as inline annotations in pull request diffs, providing immediate context to reviewers.

#### Command

```bash
check-md ../kb/template-goals.md --format github
```

#### Example Output

```
::warning file=../kb/template-goals.md,line=3,title=[ADR-002-R1]::Bold text with colon may indicate improper heading usage
::error file=../kb/template-goals.md,line=15,title=[ADR-002-R2]::Missing blank line before unordered list
::warning file=../kb/template-goals.md,line=25,title=[ADR-002-R1]::Bold text with colon may indicate improper heading usage
```

#### Expected Results

- Exit code: 1
- Output contains: `::error` and `::warning` annotations
- Each line includes: file, line, and message

---

### Step 6: Filter with Include/Exclude

Check only specific files using glob patterns.

#### Business Value

Focus on relevant files, exclude auto-generated content or work-in-progress docs.

#### Include Pattern

Check only goal files:

```bash
check-md ../kb/ --include "template-goals.md"
```

#### Exclude Pattern

Check everything except plans:

```bash
check-md ../kb/ --exclude "template-plan.md"
```

#### Example Output

```
../kb/template-goals.md
  ../kb/template-goals.md:3: [ADR-002-R1] Bold text with colon may indicate improper heading usage

1 files checked
18 violations (15 errors, 3 warnings)
```

#### Expected Results

- Exit code: 0 or 1 (depending on violations)
- Output only shows: files matching filter criteria

---

### Step 7: Check Staged Files

Check only files that are staged for commit.

#### Business Value

Pre-commit validation, catches formatting issues before they enter the repository.

#### Stage Some Files

```bash
cd ..
git add kb/template-goals.md
cd check-md
```

#### Check Staged Files

```bash
check-md --staged
```

#### Example Output

```
../kb/template-goals.md
  ../kb/template-goals.md:3: [ADR-002-R1] Bold text with colon may indicate improper heading usage
  ../kb/template-goals.md:15: [ADR-002-R2] Missing blank line before unordered list

1 files checked
18 violations (15 errors, 3 warnings)
```

#### Expected Results

- Exit code: 1
- Output contains: only staged markdown files
- If no staged markdown files: "No staged markdown files found"

---

### Step 8: Compliance Score Report

Generate comprehensive compliance scores for files and directories.

#### Business Value

Track documentation quality over time, identify problem areas, measure improvement progress, set quality gates for CI/CD.

#### Command

```bash
check-md ../kb/adr/ --report
```

#### Example Output

```
================================================================================
MARKDOWN FORMATTING COMPLIANCE REPORT
================================================================================

Overall Project Score:   92.8%
  Files Checked: 11
  Total Lines: 3573
  Total Violations: 256

Violations by Rule:
  ADR-002-R1: 151
  ADR-002-R2: 105

--------------------------------------------------------------------------------
MODULE SUMMARY
--------------------------------------------------------------------------------
   Score  Files   Viol  Path
--------------------------------------------------------------------------------
   92.4%     11    256  ../kb/adr

--------------------------------------------------------------------------------
FILE DETAILS
--------------------------------------------------------------------------------
   Score  Lines   Viol  Path
--------------------------------------------------------------------------------
✓  96.6%    416     14  ../kb/adr/leap-adr-002__markdown-formatting-standards.md
⚠  79.3%    271     56  ../kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md

================================================================================
Legend: ✓ = Excellent (95%+)  [space] = Good (80-94%)
        ⚠ = Needs Work (70-79%)  ✗ = Poor (<70%)
================================================================================

✓ Score 92.8% meets minimum threshold of 80.0%
```

#### Expected Results

- Exit code: 0 (score meets default 80% threshold)
- Overall project score calculated as weighted average by line count
- Module summary groups files by directory
- File details sorted by name (default)
- Visual indicators: ✓ (excellent), blank (good), ⚠ (needs work), ✗ (poor)
- Violations broken down by rule

#### Key Insights

- **Weighted scoring**: Larger files have more impact on overall score
- **Module grouping**: Identifies which directories need attention
- **Rule breakdown**: Shows which rules are most commonly violated
- **Visual indicators**: Quick scan to identify problem areas

---

### Step 9: Sort Score Report

Sort the score report by different criteria to focus on specific priorities.

#### Business Value

Prioritize remediation efforts, identify worst files first, track files alphabetically for auditing.

#### Sort by Score (Ascending - Worst First)

```bash
check-md ../kb/adr/ --report --sort score
```

#### Output

Files sorted from lowest to highest score, making it easy to identify files needing the most work.

```
FILE DETAILS
--------------------------------------------------------------------------------
   Score  Lines   Viol  Path
--------------------------------------------------------------------------------
⚠  79.3%    271     56  ../kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md
   ...
```

#### Sort by Violations (Most First)

```bash
check-md ../kb/adr/ --report --sort violations
```

#### Output

Files sorted by violation count (descending), highlighting files with the most issues.

```
FILE DETAILS
--------------------------------------------------------------------------------
   Score  Lines   Viol  Path
--------------------------------------------------------------------------------
⚠  79.3%    271     56  ../kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md
   ...
```

#### Sort by Name (Alphabetical)

```bash
check-md ../kb/adr/ --report --sort name
```

#### Output

Files sorted alphabetically (default), useful for systematic review or auditing.

#### Expected Results

- Exit code: 0 (if score meets threshold)
- Same data, different sort order
- Choose sort based on use case:
  - `score`: Find worst files quickly
  - `violations`: Focus on high-violation-count files
  - `name`: Systematic review, reproducible output

---

### Step 10: Enforce Score Threshold

Set minimum acceptable score and fail if not met (quality gate for CI/CD).

#### Business Value

Prevents quality degradation, enforces documentation standards in automated workflows, provides clear pass/fail criteria.

#### Command (Threshold Not Met)

```bash
check-md ../kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md --report --min-score 90
```

#### Example Output (Failure)

```
================================================================================
MARKDOWN FORMATTING COMPLIANCE REPORT
================================================================================

Overall Project Score: ⚠ 79.3%
  Files Checked: 1
  Total Lines: 271
  Total Violations: 56

...

✗ Score 79.3% below minimum threshold of 90.0%
```

#### Expected Results

- Exit code: 1 (score below threshold)
- Error message in red indicating failure
- Threshold violation clearly reported

#### Command (Threshold Met)

```bash
check-md ../kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md --report --min-score 90
```

#### Example Output (Success)

```
================================================================================
MARKDOWN FORMATTING COMPLIANCE REPORT
================================================================================

Overall Project Score: ✓ 98.0%
  Files Checked: 1
  Total Lines: 98
  Total Violations: 2

...

✓ Score 98.0% meets minimum threshold of 90.0%
```

#### Expected Results

- Exit code: 0 (score meets threshold)
- Success message in green
- CI/CD pipeline can proceed

#### Use Cases

- **CI/CD Quality Gates**: Fail builds if documentation quality drops
- **Pre-commit Hooks**: Prevent commits with low-quality documentation
- **Team Standards**: Enforce minimum quality levels for all documentation
- **Progressive Improvement**: Gradually increase threshold over time

#### Example CI/CD Integration

```yaml
# GitHub Actions
- name: Check Documentation Quality
  run: |
    cd check-md
    pip install -e .
    check-md ../kb/ --report --min-score 85
```

#### Exit Code Strategy

- Score below threshold: Exit code 1 (fail build)
- Score meets threshold: Exit code 0 (pass build)
- Error occurred: Exit code 2 (fail build with error)

---

## Business Value Summary

The **check-md** CLI workflow delivers value across multiple dimensions:

### Documentation Quality

- **Consistency**: Enforces ADR 008 standards across all markdown files
- **Readability**: Catches formatting issues that harm document comprehension
- **Maintainability**: Standardized formatting reduces cognitive load for readers

### Development Efficiency

- **Immediate Feedback**: Violations shown with line numbers and fix hints
- **Automation**: Integrates seamlessly into CI/CD pipelines
- **Time Savings**: Automated checks eliminate manual formatting review

### Team Collaboration

- **Standards Enforcement**: Objective, automated compliance checking
- **Pull Request Quality**: GitHub Actions annotations provide inline feedback
- **Onboarding**: New team members learn formatting standards through tool feedback

### CI/CD Integration

- **Pre-commit Hooks**: Catch issues before commit
- **Pull Request Checks**: Automated validation in GitHub Actions
- **Dashboard Integration**: JSON output enables custom reporting

---

## Next Steps

### For Documentation Authors

1. **Install check-md**: Run `pip install -e .` in check-md directory
2. **Check Before Commit**: Use `check-md --staged` before committing
3. **Fix Violations**: Use `--verbose` to see fix hints

### For Development Teams

1. **Add Pre-commit Hook**:
   ```bash
   echo '#!/bin/bash\ncd check-md && check-md --staged' > .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

2. **Add GitHub Actions Check**:
   ```yaml

   - name: Check markdown formatting
     run: |
       cd check-md
       pip install -e .
       check-md ../kb/ --format github
   ```

3. **Integrate into CI Pipeline**: Add check-md to existing workflows

### For Project Managers

1. **Documentation Audits**: Run `check-md kb/` to audit all documentation
2. **Track Compliance**: Use JSON output for metrics dashboards
3. **Set Standards**: Enforce ADR 008 compliance for all new documentation

---

## Troubleshooting

### Issue: "Command not found: check-md"

#### Symptom

Shell reports command not found

#### Solution

```bash
# Use module form instead
python -m check_md --help

# Or reinstall
pip install -e .

# Verify installation
which check-md
```

### Issue: "No markdown files found"

#### Symptom

Tool reports no files to check

#### Possible Causes

1. Wrong directory
2. No .md files in specified path
3. All files excluded by filter

#### Solution

```bash
# Verify you're in the correct directory
pwd

# Check that markdown files exist
ls ../kb/**/*.md

# Try without filters first
check-md ../kb/
```

### Issue: Exit code always 1

#### Symptom

Tool always exits with code 1 even on clean files

#### Explanation

Exit code 1 means violations were found (not an error)

#### Solution

```bash
# Check a known-clean file
echo "# Test\n\n## Section\n\nText." > /tmp/clean.md
check-md /tmp/clean.md

# Expected: Exit code 0, "No violations found"
```

### Issue: Colors not showing in output

#### Symptom

Output lacks color highlighting

#### Possible Causes

1. Terminal doesn't support colors
2. Output is redirected
3. NO_COLOR environment variable is set

#### Solution

```bash
# Check if NO_COLOR is set
echo $NO_COLOR

# Unset if needed
unset NO_COLOR

# Colors automatically disabled when piping output
check-md file.md | less  # No colors (expected)
check-md file.md         # Colors shown
```

### Issue: Verbose mode not showing fix hints

#### Symptom

`--verbose` shows context but no fix hints

#### Explanation

Not all violations have fix hints (some are judgement calls)

#### Examples

- Rule 1 warnings: "Bold text with colon may indicate..." (suggestion, not fix)
- Rule 1 errors: "Standalone bold text should be..." (clear fix provided)
- Rule 2 errors: Always provide fix hint ("Add blank line before...")
- Rule 4 errors: Provide fix hint with specific fence lengths

---

#### End of Workflow Demonstration
