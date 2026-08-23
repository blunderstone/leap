# Rule 2 Block Separation Blockquote Continuation Fix Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-23

---

## Quick Summary

Correct the `check-md` Rule 2 linter behavior to treat consecutive block quote lines as part of a single multi-line block quote construct, preventing `--fix` from silently corrupting paragraph wrapping in block quotes.

---

## Executive Summary

Currently, the `check-md` Rule 2 linter (`Rule2BlockSeparation`) incorrectly flags every continuation line of a multi-line block quote (lines starting with `>`) as a new block-level construct requiring a preceding blank line. This leads to false-positive style violations on standard multi-line block quotes. More critically, when run with `--fix`, the linter silently corrupts these block quotes by inserting blank lines before every continuation line, converting a single multi-line quoted paragraph into multiple separate single-line quoted paragraphs.

This issue is particularly damaging because the resulting corrupted document passes subsequent linter runs cleanly, and the original paragraph structure is permanently lost. This feature branch implements a continuation guard for block quotes in `Rule2BlockSeparation`, analogous to existing guards for lists and tables, preventing this silent corruption while retaining the correct requirement for a blank line before the block quote as a whole begins.

---

## Objectives

1. Update `Rule2BlockSeparation` in `src/check_md/rules.py` to recognize contiguous block quote markers as a single multi-line block quote block.
2. Implement a robust `BLOCKQUOTE_CONTINUATION_PATTERN` that correctly identifies continuation lines (including empty block quote lines containing a bare `>`) without triggering false-positive new block detections.
3. Author robust tests to prevent future regressions under both checker and fixer modes.
4. Ensure all modified Markdown documentation complies with the updated linter rules and passes `check-md` cleanly.

---

## Requirements

### Functional Requirements

- **REQ-1 (Continuation Guard):** Prevent `Rule2BlockSeparation` from flagging block quote lines as missing a blank line if the previous line was also part of the block quote.
- **REQ-2 (Paragraph-Break Guard):** Correctly handle internal paragraph breaks inside a block quote (such as a bare `>` on a line by itself) as block quote continuations, so they do not get incorrectly split.
- **REQ-3 (Fixer Non-Regression):** Ensure `--fix` does not modify or insert blank lines inside any valid multi-line block quote.

### Non-Functional Requirements

- **Zero performance overhead:** Match compilation speed of the existing regex-based line checking.
- **Standard compliance:** Maintain full compliance with CommonMark standards regarding block quotes.

### Testing Requirements

- Code coverage targets: Maintain 90%+ coverage for all modified check-md code and test-case structures.
- Add unit tests verifying a multi-line block quote preceded by a paragraph reports exactly one violation, on its first line.
- Add unit tests verifying a block quote containing a bare `>` paragraph break reports exactly one violation, on its first line.
- Add unit tests verifying a block quote at the start of a document, or after a blank line, reports zero violations.
- Add unit tests verifying that running the fixer over a multi-line block quote leaves the quote unchanged (round-trip test).

### Documentation Requirements

- Complete inline docstrings for the new patterns and logic in `src/check_md/rules.py`.
- Explicitly cite GitHub issue #12 in commit and feature notes.

---

## Success Criteria

- [ ] Contiguous block quote continuation lines do not report Rule 2 violations.
- [ ] Block quotes with internal empty-line paragraph breaks (bare `>`) do not report Rule 2 violations.
- [ ] A block quote preceded by normal paragraph text correctly reports exactly one violation on its first line.
- [ ] Running `--fix` over multi-line block quotes does not insert blank lines between contiguous quote lines.
- [ ] All unit tests in `tests/test_rule2_block_separation.py` pass successfully.
- [ ] Standard linter checks (`check-md kb/`) run cleanly with zero violations.

---

## Constraints

- Must remain within the existing structure and architecture of the Python `check-md` project.

---

## Assumptions

- Existing Markdown documentation uses correct CommonMark block quote structures.

---

## Out of Scope

- Refactoring other linter rules or fixing unrelated bugs in `check-md`.
