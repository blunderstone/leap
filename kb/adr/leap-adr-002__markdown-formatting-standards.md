# Markdown Formatting Standards for Documentation

**Status:** accepted

**Deciders:** F. Andy Seidl

## Issue

Markdown documentation in our projects must render consistently across multiple viewers (GitHub, GitLab, IDE markdown previewers, CommonMark processors). Inconsistent formatting practices can lead to:

1. **Rendering Issues**: Code blocks, lists, and tables wrapped into paragraph text
2. **Navigation Problems**: Document structure not exposed to outline/TOC tools
3. **Accessibility Issues**: Screen readers unable to navigate document hierarchy
4. **Maintenance Burden**: Invisible formatting (trailing spaces) accidentally removed by editors
5. **Inconsistent Structure**: Some documents use headings, others use bold text for structure

Without clear standards, documentation becomes harder to read, navigate, and maintain. We need formatting practices that ensure consistent rendering across all Markdown processors while maximizing accessibility and maintainability.

## Decision

We adopt the following Markdown formatting standards for all documentation in our projects:

### 1. Use Semantic Headings for Structure

**Principle:** All structural elements must use proper heading levels (`#`, `##`, etc.) rather than bold text.

#### Bad Practice

```markdown
**Business Question:**
> "What is the question?"

**Value:**
- Benefit 1
- Benefit 2
```

#### Good Practice

```markdown
##### Business Question

> "What is the question?"

##### Value

- Benefit 1
- Benefit 2
```

#### Rationale

- **Semantic Meaning**: Screen readers and document outlines recognize headings as structural elements
- **Navigation**: IDE outline views, TOC generators, and screen readers can navigate by heading
- **No Wrapping Risk**: Headings never wrap with following text, unlike bold text
- **Hierarchy**: Clear visual and structural document hierarchy
- **Accessibility**: WCAG compliance for document structure

#### Heading Hierarchy Guidelines

Use appropriate heading levels based on document structure:

- **Level 1 (`#`)**: Document title only
- **Level 2 (`##`)**: Major sections
- **Level 3 (`###`)**: Subsections within major sections
- **Level 4 (`####`)**: Individual items or topics
- **Level 5 (`#####`)**: Item subsections (e.g., "Business Question", "Value", "Example")
- **Level 6 (`######`)**: Fine-grained subsections (e.g., "Rationale", "Test Data")

Never skip heading levels (e.g., don't jump from `##` to `####`).

**Validation:** check-md Rule 3 (Heading Level Increment) enforces this requirement.

---

### 2. Separate Block Elements with Blank Lines

**Principle:** Always insert a blank line between paragraph text and block elements (code blocks, lists, tables, etc.).

**Note:** Headings are self-terminating block elements and do not require blank lines after them. However, blank lines after headings improve readability and are recommended.

#### Block Elements Requiring Separation (when preceded by paragraph text)

- Code blocks (` ```language `)
- Lists (`-`, `*`, `1.`)
- Tables (`| column |`)
- Blockquotes (`>`)
- Horizontal rules (`---`)

#### Bad Practice

````markdown
Section comments render as box comments:
```typeql
# This code block may wrap into the paragraph
```
````

#### Good Practice

````markdown
Section comments render as box comments:

```typeql
# This code block renders correctly as a separate block
```
````

#### Headings Don't Require Blank Lines

Headings are self-terminating, so this works fine:

```markdown
##### Business Question
> "What is the question?"
```

However, adding blank lines after headings improves readability:

```markdown
##### Business Question

> "What is the question?"
```

#### Rationale

The CommonMark specification requires blank lines to separate block-level elements from paragraph text. Without this separation, many Markdown processors will wrap block elements into the preceding paragraph, breaking rendering. Headings are an exception because they are self-terminating block elements.

---

### 3. Use Hard Line Breaks for Consecutive Metadata

**Principle:** For consecutive lines of bold-prefixed metadata that should appear as separate lines, use `<br>` tags.

#### Bad Practice

```markdown
**Feature**: JCL Phase 1
**Author**: F. Andy Seidl
**Date**: 2025-11-02
```

**Result:** Renders as a single wrapped paragraph:

**Feature**: JCL Phase 1 **Author**: F. Andy Seidl **Date**: 2025-11-02

#### Good Practice

```markdown
**Feature**: JCL Phase 1<br>
**Author**: F. Andy Seidl<br>
**Date**: 2025-11-02
```

**Result:** Renders as separate lines:

**Feature**: JCL Phase 1<br>
**Author**: F. Andy Seidl<br>
**Date**: 2025-11-02

#### Rationale

- **Explicit**: `<br>` tags are visible and won't be accidentally removed
- **Reliable**: Works consistently across all Markdown processors
- **Maintainable**: Better than trailing spaces (which are invisible and fragile)

#### When to Use

Use `<br>` tags for:

- Document metadata sections (feature, phase, author, date, status)
- Multiple consecutive labeled items that must appear as separate lines
- Any bold-prefixed lines requiring visual separation but not separate paragraphs

#### Alternatives (Not Recommended)

- **Trailing Spaces**: Invisible and often removed by editors/formatters
- **Blank Lines**: Creates too much vertical space, disrupts visual grouping
- **Tables**: Overly formal for simple metadata

---

### 4. Handle Nested Code Blocks Correctly

**Principle:** When documenting code that contains code examples, use the appropriate technique based on context.

#### The General Solution: Four Backticks

When showing code examples in markdown that themselves contain code blocks, use four backticks for the outer block and three for the inner:

`````markdown
Here's how to use the authentication function:

````kotlin
fun main() {
    val code = """
        ```kotlin
        val result = authenticate("user", "pass")
        ```
    """
}
````
`````

This allows proper nesting without premature closure of the outer block.

#### The KDoc-Specific Case: Use Standard Indentation

When writing or documenting KDoc comments, follow the KDoc/JavaDoc convention of 4-space indentation for code examples:

````markdown
```kotlin
/**
 * Example class
 *
 * ## Usage
 *
 *     val example = Example()  // ✅ Standard KDoc indentation
 *     example.doSomething()
 */
class Example
```
````

This is both the **standard KDoc convention** AND avoids the nesting problem.

#### Bad Practice: Triple Backticks Everywhere

````markdown
```kotlin
/**
 * Example class
 *
 * ## Usage
 *
 * ```kotlin
 * val example = Example()  // ❌ This closes the outer code block!
 * ```
 */
class Example
```
````

**Result:** The inner ` ``` ` prematurely closes the outer Kotlin code block, breaking rendering.

#### When to Use Each Approach

| Context | Approach | Reason |
|---------|----------|--------|
| **Documenting KDoc examples** | 4-space indentation | KDoc/JavaDoc standard convention |
| **Showing nested code blocks** | Four backticks | Allows proper nesting in markdown |
| **Writing actual KDoc in source code** | 4-space indentation | Standard convention, what IDEs expect |
| **Markdown examples with code** | Four backticks | Most flexible, explicit nesting |

#### Rationale

- **Standards Compliance**: KDoc/JavaDoc conventions use 4-space indentation
- **Prevents Parsing Issues**: Both approaches avoid premature closure of outer blocks
- **Consistent Rendering**: Works correctly across all Markdown processors
- **Context Appropriate**: Use the right tool for the right job
- **Readability**: Clear visual hierarchy without parsing ambiguity

---

## Consequences

### Positive

1. **Consistent Rendering**: Documentation renders identically across GitHub, GitLab, IDE previewers, and CommonMark processors
2. **Improved Accessibility**: Screen readers can properly navigate document structure via semantic headings
3. **Better Navigation**: IDE outline views, TOC generators, and document viewers expose complete structure
4. **Maintainability**: Explicit formatting (`<br>` tags, headings) prevents accidental corruption
5. **Developer Experience**: Clear hierarchy and structure makes documents easier to read and navigate
6. **Onboarding**: New team members can follow consistent patterns across all documentation
7. **AI-Friendly**: Clear structure helps AI assistants understand and generate documentation correctly

### Negative

1. **More Verbose**: Using proper headings and `<br>` tags adds more markup compared to bold text
2. **Migration Effort**: Existing documentation needs updating to follow new standards
3. **Learning Curve**: Developers must learn proper heading hierarchy (though this is best practice anyway)
4. **Spacing Trade-off**: For consecutive metadata, authors must choose between `<br>` tags (tight spacing, uses HTML) or blank lines (pure Markdown, more vertical space)

### Migration Strategy

For existing documentation:

1. **Priority 1**: Update feature documentation and ADRs (highest visibility)
2. **Priority 2**: Update README files and developer guides
3. **Priority 3**: Update internal notes and low-traffic documentation
4. **Automated Detection**: Consider linting rules to detect violations

Example lint rules:

- Flag consecutive bold lines without `<br>` tags
- Flag "heading-like" bold text (e.g., `**Value:**`, `**Example:**`)
- Flag code blocks without preceding blank line

---

## Examples and References

### Complete Example: Use Case Documentation

````markdown
## Proposed Features

### Priority 0 (P0) - Critical Features

#### Feature 1: User Authentication

##### Business Question

> "How should users authenticate with the system?"

##### Value

- **Security**: Protects sensitive data
- **Compliance**: Meets regulatory requirements
- **User Experience**: Simple login flow

##### Implementation Approach

```kotlin
/**
 * Authenticates a user
 *
 * ## Example
 *
 *     val result = authenticate("user@example.com", "password")
 *     if (result.success) {
 *         println("Authenticated!")
 *     }
 */
fun authenticate(email: String, password: String): AuthResult
```

##### Priority

**P0** - Essential for production launch

###### Rationale

Authentication is required before any user features can be deployed securely.

###### Estimated Effort

2-3 days including OAuth integration and testing.
````

### Reference: Document Header Template

```markdown
# Document Title

**Status:** Draft<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2025-11-02<br>
**Last Updated:** 2025-11-02

---

## Overview

Brief document overview...

## Section 1

Content...
```

---

## Enforcement

### Code Review Checklist

All documentation PRs should verify:

- [ ] All structural elements use proper headings (not bold text)
- [ ] Blank lines separate all block elements from paragraphs
- [ ] Consecutive metadata lines use `<br>` tags
- [ ] No nested fenced code blocks in KDoc comments
- [ ] Heading hierarchy is logical (no skipped levels)

### Tooling

#### check-md (Primary Tool)

The project uses `check-md` - a custom Python linter that enforces Rules 1, 2, and 4:

#### Installation

For detailed and bulletproof installation instructions (including virtual environments and modern `uv` workflows), refer to the **[check-md README](../../check-md/README.md)**.

Quick setup:

Using `uv` (Recommended):

```bash
# Installs check-md globally as an editable command on your PATH
cd check-md
uv tool install --editable .
```

Using standard Python:

```bash
cd check-md
python3 -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -e .
```

#### Basic Usage

```bash
# Check files
check-md kb/feature/my-feature/

# Auto-fix violations
check-md kb/feature/my-feature/ --fix

# Check staged files (for git hooks)
check-md --staged
```

#### Features

- Detects all Rule 1, 2, and 4 violations
- Auto-fix mode with backup creation
- Compliance scoring (0-100)
- Configuration via `.check-md.yml`
- Ignore comments for intentional violations
- CI/CD integration templates

#### Documentation

- Full guide: `check-md/README.md`
- Integration: `check-md/templates/README.md`
- Workflow: See CLAUDE.md "ADR 008 Compliance" section

#### Complementary Tools

1. **markdownlint**: For additional style rules
2. **IDE Plugins**: Markdown preview to verify rendering
3. **Pre-commit Hooks**: Template provided in `check-md/templates/pre-commit`

### AI Assistant Context

This ADR is integrated into CLAUDE.md with automated enforcement via `check-md`:

- AI assistants run `check-md <file> --fix --quiet` before presenting files
- Common violations documented with ❌/✅ examples
- Ignore comments available for intentional violations
- Auto-fix handles 90%+ of violations automatically

See CLAUDE.md "⚠️ CRITICAL: ADR 008 Markdown Compliance" section for complete workflow.

---

## Related Documents

- **LEAP Methodology**: `kb/meta/best-practices-for-leap-programming.md`
- **Goals Template**: `kb/meta/goals-template.md`
- **Plan Template**: `kb/meta/plan-template.md`
- **Completion Summary Template**: `kb/meta/completion-summary-template.md`

---

## History

- **2025-11-02**: Initial ADR creation incorporating existing best practices and new heading standard
- **2025-11-13**: Added `check-md` automated enforcement tool with auto-fix capabilities
- **Test Case**: `kb/feature/faseidl/jcl-phase-1/transitive-query-use-cases.md` demonstrates all standards

---

**Status:** accepted<br>
**Deciders:** F. Andy Seidl<br>
**Date:** 2025-11-02
