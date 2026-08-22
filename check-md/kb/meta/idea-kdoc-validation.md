# Idea: KDoc Markdown Validation

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2025-12-08<br>
**Status:** Proposed

---

## Overview

Extend check-md to detect and optionally fix ADR 008 markdown violations within KDoc comments in Kotlin source files.

## Context

During code review, ADR 008 violations were discovered in KDoc comments (e.g., using `**bold**` for structural headers instead of proper markdown headers). Currently, check-md only validates standalone markdown files, missing violations embedded in source code documentation.

## Motivation

- **Consistency**: KDoc comments often contain markdown that should follow the same standards as standalone documentation
- **Code Review Efficiency**: Automated detection reduces manual review burden
- **Documentation Quality**: Ensures inline documentation meets professional standards
- **Early Detection**: Catch violations during development, not during review

## Proposed Solution

Add KDoc validation capability to check-md:

### Detection Strategy

1. **File Pattern Matching**: Identify `.kt` files during scanning
2. **KDoc Extraction**: Parse Kotlin files to extract KDoc comment blocks (`/** ... */`)
3. **Markdown Validation**: Apply existing ADR 008 rules to extracted markdown
4. **Source Location Tracking**: Report violations with file name, line numbers, and KDoc context

### Auto-Fix Strategy

When `--fix` flag is used:

1. Extract KDoc blocks with precise line/column locations
2. Apply ADR 008 fixes to markdown content
3. Replace original KDoc blocks in source file
4. Preserve surrounding code and formatting

### Configuration

Add to `.check-md.yml`:

```yaml
# Enable KDoc validation
validate_kdoc: true

# File patterns to scan for KDoc
kdoc_patterns:
  - "**/*.kt"

# Exclude patterns
kdoc_exclude:
  - "**/test/**"
  - "**/generated/**"
```

## Examples

### Violation Detection

**File:** `src/main/kotlin/com/example/util/Throttler.kt`

#### Current (violation)

```kotlin
/**
 * **Timing behavior:**
 * Multiple threads attempt to execute simultaneously...
 */
```

#### Fixed

```kotlin
/**
 * ## Timing behavior
 *
 * Multiple threads attempt to execute simultaneously...
 */
```

### Output Format

```
src/main/kotlin/com/example/util/Throttler.kt:67
  ✗ kdoc-bold-for-structure: Don't use bold for structural headings
    | **Timing behavior:**
    Suggestion: Use markdown header (## Timing behavior)
```

## Benefits

1. **Automated Compliance**: Catch ADR 008 violations in KDoc automatically
2. **Consistent Documentation**: Same standards for standalone docs and code comments
3. **Developer Experience**: Fix violations with `--fix` flag
4. **CI Integration**: Block PRs with KDoc violations
5. **Reduced Review Burden**: Fewer style issues in code reviews

## Considerations

### Scope

- Focus exclusively on Kotlin KDoc comments
- Apply all ADR 008 markdown formatting rules
- No support for JavaDoc (uses HTML, not markdown)

### Technical Challenges

1. **KDoc Extraction**: Regex-based extraction of `/** ... */` blocks
   - Handle nested examples (KDoc containing code blocks with KDoc examples)
   - Track line numbers for accurate violation reporting
2. **Fix Precision**: Must preserve surrounding code exactly
3. **Performance**: Scanning source files is slower than markdown files
4. **Testing**: Need comprehensive test suite for various KDoc patterns including nested examples

### Alternatives Considered

1. **Separate Tool**: Create kdoc-check instead of extending check-md
   - ❌ Duplication of ADR 008 rules
   - ❌ Separate configuration and CI integration

2. **IDE Plugin**: Rely on IDE linting
   - ❌ Not enforced in CI
   - ❌ Developers can ignore warnings

3. **Pre-commit Hook Only**: Check only changed files
   - ❌ Doesn't catch existing violations
   - ❌ Can be bypassed

## Implementation Phases

### Phase 1: Detection Only

- Parse `.kt` files and extract KDoc blocks
- Apply ADR 008 rules to extracted markdown
- Report violations with line numbers
- No auto-fix capability

### Phase 2: Auto-Fix

- Implement precise source location tracking
- Add `--fix` support for KDoc
- Preserve code formatting and structure

## Success Criteria

1. Detect ADR 008 violations in KDoc with 100% accuracy
2. Auto-fix violations without corrupting source code
3. Performance: < 5s for 1000 Kotlin files
4. Zero false positives in test suite
5. CI integration working smoothly

## Design Decisions

1. **Scope**: Only validate KDoc comments (`/** ... */`), not regular comments - KDoc generates documentation
2. **Generated Code**: Excluded via patterns (`**/generated/**`) - no special handling needed
3. **Fix Application**: Tool applies fixes in-place with `--fix` flag
   - Developers run tool during development
   - Changes tracked in version control like all code changes
   - AI agents should validate KDoc they create/update (same as markdown documents)
4. **Severity Level**: Report violations as warnings, not errors

## Related Documents

- `kb/adr/leap-adr-002__markdown-formatting-standards.md` - The standard being enforced
- `check-md/README.md` - Current check-md documentation

## Next Steps

1. Validate idea with team
2. Prototype regex-based KDoc extraction
   - Handle nested KDoc examples in code blocks
   - Verify line number tracking accuracy
3. Create spike/POC for validation integration
4. Write detailed implementation plan if approved
