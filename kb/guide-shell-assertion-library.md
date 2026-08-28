# Shell Assertion Library Guide

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-28

---

## Table of Contents

- [Overview](#overview)
- [Library Location](#library-location)
- [Quick Start](#quick-start)
- [Variables & Counter Management](#variables--counter-management)
- [Function Reference](#function-reference)
  - [assert_equals](#assert_equals)
  - [assert_true](#assert_true)
  - [assert_exit_code](#assert_exit_code)
  - [assert_exists](#assert_exists)
  - [assert_absent](#assert_absent)
  - [assert_contains](#assert_contains)
- [Usage by Parent Repositories](#usage-by-parent-repositories)

---

## Overview

LEAP provides a reusable, lightweight, and POSIX-friendly assertion library for shell scripting and git hooks. It unifies output formatting, simplifies test suite implementation, and provides consistent diagnostic information upon failure without enforcing premature script termination.

## Library Location

The assertion library is located at:

```
scripts/lib/assert.sh
```

## Quick Start

To use the assertion library in a shell script, source the file relative to the script's directory and run assertion commands:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Source the assertion library
source "$(dirname "${BASH_SOURCE[0]}")/../lib/assert.sh"

# Perform assertions
assert_equals "math checks" "4" "$((2+2))"
assert_exists "License file exists" "LICENSE"

# Report outcomes and exit
echo "Test summary: PASS=$PASS FAIL=$FAIL"
if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
```

---

## Variables & Counter Management

The assertion library relies on two global/dynamic variables to track the status of assertions:

- **`PASS`**: Incremented by 1 every time an assertion succeeds.
- **`FAIL`**: Incremented by 1 every time an assertion fails.

### Initialization

Upon sourcing the library, `PASS` and `FAIL` are initialized to `0` if they are not already defined:

```bash
PASS=${PASS:-0}
FAIL=${FAIL:-0}
```

If your test suite aggregates several scripts or wants to track its own custom counters, you can define `PASS` and `FAIL` before sourcing the library.

---

## Function Reference

### `assert_equals`

Asserts that two strings match exactly.

#### Signature

```bash
assert_equals <label> <expected_string> <actual_string>
```

#### Parameters

- **`label`**: A descriptive name for the assertion (printed on output).
- **`expected_string`**: The expected literal text.
- **`actual_string`**: The actual value under test.

#### Example

```bash
assert_equals "correct user" "admin" "$CURRENT_USER"
```

---

### `assert_true`

Asserts that a value is literally `"true"`.

#### Signature

```bash
assert_true <label> <value>
```

#### Parameters

- **`label`**: A descriptive name for the assertion.
- **`value`**: The string value to verify (must be exactly `"true"` to pass).

#### Example

```bash
assert_true "is executable flag set" "$IS_EXEC"
```

---

### `assert_exit_code`

Asserts that the exit status code of a command matches the expected value, and prints optional command outputs on mismatch.

#### Signature

```bash
assert_exit_code <label> <expected_code> <actual_code> [output]
```

#### Parameters

- **`label`**: A descriptive name for the assertion.
- **`expected_code`**: The expected integer exit status (usually `0` for success).
- **`actual_code`**: The actual command exit code (often captured from `$?`).
- **`output`** *(Optional)*: Output log content to print as context if the code is a mismatch.

#### Example

```bash
set +e
output=$(bash run-script.sh 2>&1)
code=$?
set -e

assert_exit_code "run-script.sh executes cleanly" 0 "$code" "$output"
```

---

### `assert_exists`

Asserts that a file or directory exists.

#### Signature

```bash
assert_exists <label> <path>
```

#### Parameters

- **`label`**: A descriptive name for the assertion.
- **`path`**: The file or directory path to check.

#### Example

```bash
assert_exists "pre-commit hook file" ".git/hooks/pre-commit"
```

---

### `assert_absent`

A dual-purpose utility checking for either pattern absence inside a string or file/directory absence on disk.

#### Signature 1: String Absence

```bash
assert_absent <label> <haystack_string> <needle_string>
```
*Passes if `needle_string` is **not** found inside `haystack_string`.*

#### Signature 2: File Absence

```bash
assert_absent <label> <path>
```
*Passes if the file or directory at `path` does **not** exist.*

#### Compatibility Alias
The function `assert_not_exists` is supported as a direct alias for `assert_absent <label> <path>`.

#### Examples

```bash
# Verify substring absence
assert_absent "no error keyword" "$log_output" "ERROR"

# Verify file absence
assert_absent "CLAUDE.md excluded" "CLAUDE.md"
```

---

### `assert_contains`

Asserts that a string contains a specified substring (needle).

#### Signature

```bash
assert_contains <label> <haystack_string> <needle_string>
```

#### Parameters

- **`label`**: A descriptive name for the assertion.
- **`haystack_string`**: The text block to search.
- **`needle_string`**: The substring to look for.

#### Example

```bash
assert_contains "help output contains usage" "$help_out" "Usage:"
```

---

## Usage by Parent Repositories

For parent repositories that integrate LEAP as a git submodule (e.g., inside a directory named `leap/` or `submodules/leap/`), this assertion library is directly accessible to simplify the parent repository's own shell test suites and git hooks.

### Sourcing in Submodule Environments

Source the library from the parent test suite by referencing the relative path into the submodule:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Locate the parent repo directory
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source assert.sh from the nested LEAP submodule
source "$HERE/../submodules/leap/scripts/lib/assert.sh"

PASS=0
FAIL=0

# Perform assertions for the parent repo's tools
assert_exists "Package manifest exists" "package.json"

# Check status
if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
```
