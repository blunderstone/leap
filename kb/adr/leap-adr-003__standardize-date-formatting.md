# Date Formatting Standardization

**Status:** accepted<br>
**Deciders:** F. Andy Seidl<br>
**Date:** 2026-08-27

---

## Issue

Inconsistent date formats (e.g., DD/MM vs. MM/DD vs. natural-language names) across various markdown templates and active feature files create confusion, git diff noise, and regional ambiguity. Vague placeholders also lead to inconsistent inputs during document creation.

### Current State

- Templates use inconsistent or vague placeholders.
- Active feature documents and guides use natural-language, localized, or varied numeric formats.
- Workspace tooling and generation systems use inconsistent format patterns, leading to styling differences.

#### Problems with Current Approach

1. **Regional Ambiguity**: Numeric formats like `08/12/2026` are ambiguous (representing August 12 or December 8 depending on the region).
2. **Git Diff Noise**: Regenerating or updating documents changes header dates using different formatting styles, creating unnecessary git noise.
3. **Machine Unparseability**: Varied formats are difficult for automated linter and compliance tooling to parse and validate.

## Decision

We adopt the ISO 8601 standardized format `YYYY-MM-DD` for all dates and timestamps across all LEAP-compliant documentation, templates, and generated files.

### Format Requirements

1. **Template Placeholders**: All documentation templates containing date or timestamp fields must use `[YYYY-MM-DD]` as the standardized placeholder format.
2. **Metadata Headers**: When populating document metadata (e.g., `Date`, `Last Updated`, `Date Created`, `Date Started`, `Date Completed`), authors and automated content generators must format these fields strictly as `YYYY-MM-DD`.

## Rationale

- **No Ambiguity**: ISO 8601 (`YYYY-MM-DD`) is globally recognized and eliminates all regional date confusion (year-month-day).
- **Tool Friendly**: The standard format is easily parseable by existing and future automated linter tooling (such as `check-md`).
- **Git Hygiene**: Restricting dates to a single predictable format minimizes stylistic diff churn on document updates.

## Options Considered

### Option A: Standardize on ISO 8601 (YYYY-MM-DD)

#### Approach

Enforce the strict standard format `YYYY-MM-DD` for all template placeholders, manual entries, and automated content generators.

#### Pros

- Universal and unambiguous.
- Extremely easy to validate with regex and standard parsing tools.
- Matches existing standard conventions in major software engineering ecosystems.

#### Cons

- Less personal than natural-language or localized formats (e.g., "Thursday, August 27, 2026").

---

### Option B: Keep Flexible Natural-Language/Localized Formats

#### Approach

Allow developers to use any clear date format, including localized formats like "August 27, 2026" or "27-Aug-2026".

#### Pros

- High human-readability at a glance.
- Minimal transition effort for existing files.

#### Cons

- High regional ambiguity (e.g., DD/MM/YY vs MM/DD/YY).
- Unnecessary git diff churn.
- Extremely difficult to write automated linting validation rules.

## Evaluation Criteria

1. **Ambiguity Elimination**: Does it prevent regional confusion?
2. **Tool Support**: Is it easily parseable and verifiable by automated linters?
3. **Generator Compatibility**: Can standard development tools and workspace templates easily support the format?

## Comparison Matrix

| Criterion | Option A (ISO 8601) | Option B (Flexible) |
|-----------|--------------------|---------------------|
| Ambiguity Elimination | ✓ | |
| Tool Support | ✓ | |
| Generator Compatibility | ✓ | ✓ |

---

## Consequences

### Positive

- **Clarity**: Total elimination of date-format ambiguity.
- **Maintainability**: Clear and simple linting rule creation path.
- **Consistency**: Content generation tools can reliably output compliant metadata.

### Negative

- **Aesthetics**: Some users may find ISO-formatted dates less expressive than written-out localized days.

## Migration Strategy

### High-Level Policy

Document templates will be updated immediately to use the standardized placeholder. Future workspace tools and metadata generation systems must output compliant dates adhering to the `YYYY-MM-DD` format. Existing active feature files are encouraged to adopt the standard during their active development cycle; retroactive conversion of archived or historical documents is not required.

---

## References

- ADR leap-adr-002: [Markdown Formatting Standards for Documentation](leap-adr-002__markdown-formatting-standards.md)
