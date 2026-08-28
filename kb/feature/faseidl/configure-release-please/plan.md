# Configure release-please for LEAP Documentation & Methodology Implementation Plan

**Author:** [Andy Seidl](https://github.com/faseidl)<br>
**Date:** 2026-08-28

---

## Overview

The goal is to customize the automated `release-please` configuration and developer conventions so that LEAP framework-level documentation, ADRs, templates, and guides are recognized as release-triggering and beautifully categorized in generated changelogs.

**Development Approach:** We will follow a sequential, phased approach, validating the config structure and markdown formatting at each milestone using `check-md`.

### Overall Assessment

- **Complexity:** LOW - Config changes are standard JSON additions and the documentation changes are straightforward markdown.
- **Risk:** LOW - No direct impact on production software runtime.

---

## Phase 1: Customize release-please-config.json

### Goals

- Update `release-please-config.json` with a custom `changelog-sections` array.
- Group conventional commit types appropriately (`feat`, `fix`, `docs`, `refactor`).

### Approach

- Add `"changelog-sections"` array under the root package in `release-please-config.json`.
- Keep configuration schema-compliant.

### Testing

- Verify syntactical correctness of JSON.
- Verify that standard JSON schema-validator rules (if any exist locally) or formatting is correct.

### Success Criteria

- [ ] `release-please-config.json` is updated and matches the desired structure.
- [ ] JSON syntax is valid.

**Rationale:** Customizing `changelog-sections` enables `release-please` to display non-standard categories in the markdown output instead of ignoring them.

---

## Phase 2: Update GEMINI.md Commit Prefixes & Guidelines

### Goals

- Establish guidelines in `GEMINI.md` for developers on commit prefix usage for LEAP-specific deliverables.
- Define release-triggering prefixes (`feat(kb):`, `feat(templates):`) versus non-release-triggering prefixes (`docs(...)`).
- Establish a strict policy that commits to ephemeral directories (such as `kb/feature/`) must NEVER use `feat` or `fix` prefixes, and must always use non-release-triggering prefixes like `chore(workflow):` or `docs(workflow):`.

### Approach

- Append or integrate a dedicated conventional commit guidelines section in `GEMINI.md`.
- Clearly explain the difference in release impact between `feat(...)` and `docs(...)` for Literate Programming files.
- Document the rule for ephemeral feature branch directories to prevent accidental release triggers during drafting and development.

### Testing

- Run `check-md` on `GEMINI.md` to ensure zero linter or style violations.
- Verify that the resulting documentation is easy to read and logically consistent.

### Success Criteria

- [ ] `GEMINI.md` contains the updated guidelines.
- [ ] No `check-md` linter violations in modified or added files.

**Rationale:** Updating developer guidelines is crucial to ensure team consensus and consistent use of appropriate commit prefixes to trigger releases correctly.

---

## Decision Points

### After Phase 1

- Proceed to Phase 2 once configuration changes are complete and JSON format is verified.

### After Phase 2

- Complete the feature by reviewing the overall checklist and drafting the completion summary.
