# LEAP Standard: Named Code Blocks

**Status:** Active Standard<br>
**Date:** 2025-11-08<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

---

## Executive Summary

**Named Code Blocks** are a **LEAP-specific commenting specification** developed by Phase Change. They are inline source comments that mark specific sections of code with human-readable identifiers. They enable precise references in documentation, discussions, and AI-friendly development without interfering with API documentation or generated doc sites.

**This is not based on existing comment tagging libraries**—it is a custom standard designed specifically for LEAP's documentation-first, AI-friendly development approach.

### Key Benefits

- **Precise communication**: Reference specific code sections by name, not line numbers
- **Stable references**: Names survive refactoring better than line numbers
- **Documentation anchors**: Implementation docs can link to specific code sections
- **AI targeting**: Enable AI agents to work on specific code blocks
- **Logical grouping**: Related code across files can share naming patterns

---

## Core Concepts

### What Are Named Code Blocks?

Named code blocks are arbitrary sections of code wrapped with special comment markers:

```kotlin
// @block: typedb-relation-separator
// @purpose: Handle TypeDB 3.x semicolon separator requirement
val separator = if (isRelation) ";" else ","
// @end-block: typedb-relation-separator
```

### Key Characteristics

1. **Non-invasive**: Just comments—don't affect compilation or runtime
2. **Tool-agnostic**: Don't appear in generated docs (Dokka, JavaDoc, Rustdoc)
3. **Language-agnostic**: Work in any language with comments
4. **Project-wide unique**: Block names should be unique across the entire project
5. **Optional metadata**: Can include context for humans and AI agents

---

## Syntax Specification

### Basic Block

```kotlin
// @block: block-name
[code content]
// @end-block: block-name
```

#### Example

```kotlin
// @block: exponential-backoff-retry
for (attempt in 1..5) {
    try {
        return operation()
    } catch (e: TransientException) {
        Thread.sleep(100L * (1 shl attempt))
    }
}
throw MaxRetriesExceededException()
// @end-block: exponential-backoff-retry
```

### Block with Metadata

```kotlin
// @block: block-name
// @purpose: One-line explanation of why this code exists
// @context: Additional context or constraints
// @related: kb/docs/related-doc.md
// @complexity: O(n²)
// @ai-context: Guidance for AI agents
// @ai-constraints: What AI should NOT change
[code content]
// @end-block: block-name
```

#### Example

```kotlin
// @block: concurrent-cache-access
// @purpose: Thread-safe cache with optimistic locking
// @complexity: O(1) average, O(n) worst case on collision
// @related: kb/caching-architecture.md
// @ai-context: This is performance-critical; profile before changes
// @ai-constraints: Must maintain thread safety guarantees
val cached = cacheMap.computeIfAbsent(key) {
    expensiveComputation(key)
}
// @end-block: concurrent-cache-access
```

### Multi-Fragment Blocks

Related code in different locations can use numbered suffixes:

```kotlin
// File: QueryBuilder.kt
// @block: typedb-query-construction
fun buildQuery(entities: List<Entity>): String {
    val buffer = StringBuilder("match\n")
    appendEntityPatterns(buffer, entities)
    return buffer.toString()
}
// @end-block: typedb-query-construction

// ... other code ...

// @block: typedb-query-construction(2)
private fun appendRelationPatterns(buffer: StringBuilder) {
    buffer.append(";")  // TypeDB 3.x separator
    relations.forEach { buffer.append("\n  ${it.pattern}") }
}
// @end-block: typedb-query-construction(2)
```

```kotlin
// File: QueryValidator.kt
// @block: typedb-query-construction(3)
fun validateQuerySyntax(query: String): ValidationResult {
    return TypeDBSyntaxValidator.validate(query)
}
// @end-block: typedb-query-construction(3)
```

The logical block `typedb-query-construction` consists of three physical fragments.

### Language-Specific Syntax

#### Kotlin/Java

```kotlin
// @block: block-name
// @end-block: block-name
```

#### Rust

```rust
// @block: block-name
// @end-block: block-name
```

#### JavaScript/TypeScript

```javascript
// @block: block-name
// @end-block: block-name
```

#### ReasonML

```reasonml
/* @block: block-name */
/* @end-block: block-name */
```

#### Bash

```bash
# @block: block-name
# @end-block: block-name
```

#### TypeQL

```typeql
# @block: schema-entity-definitions
# @end-block: schema-entity-definitions
```

---

## Naming Conventions

### Project-Wide Uniqueness

**Best Practice:** Block names should be unique across the entire project.

**Why?** So you can reference blocks without needing file context:

```markdown
✅ "Review the @typedb-relation-separator for performance"
❌ "Review the relation-separator in QueryBuilder.kt"
```

### Naming Strategy

Use domain-specific, descriptive names (2-5 words):

```
[domain/component]-[specific-function]-[optional-qualifier]
```

#### Good names

```kotlin
// @block: typedb-relation-separator        // Domain + function
// @block: meridian-content-deduplication   // Component + function
// @block: exponential-backoff-retry        // Function + qualifier
// @block: jwt-token-validation             // Domain + function
// @block: levenshtein-distance-calculation // Specific algorithm
```

#### Poor names (too generic)

```kotlin
// @block: helper-function     // ❌ Too generic
// @block: validation          // ❌ Too generic
// @block: processing          // ❌ Too generic
// @block: utils               // ❌ Too generic
```

### Naming Format

- **Use lowercase kebab-case**: `typedb-relation-separator`
- **Alphanumeric + hyphens**: `a-z`, `0-9`, `-`
- **No underscores or spaces**: Not `typedb_relation_separator` or `typedb relation separator`
- **Multi-fragment suffix**: `block-name(2)`, `block-name(3)`

### Handling Name Conflicts

If you discover two blocks with the same name, make them more specific:

```kotlin
// Before (conflict):
// @block: pattern-validation  // In QueryBuilder.kt
// @block: pattern-validation  // In SchemaValidator.kt

// After (resolved):
// @block: query-pattern-validation     // ✅ Unique
// @block: schema-pattern-validation    // ✅ Unique
```

### Verification Before Committing

Check for conflicts before committing:

```bash
# Verify block name is unique
git grep "@block: exponential-backoff-retry"

# If found, choose a more specific name
```

---

## Referencing Named Blocks

### The `@` Prefix Convention

When referring to named code blocks in documentation, use the **`@` prefix**:

```markdown
The @typedb-relation-separator handles TypeDB 3.x syntax requirements.
```

#### Why `@`?

- Mirrors source code: `// @block: block-name`
- Visually distinct from functions (`buildQuery()`), classes (`QueryBuilder`), files (`QueryBuilder.kt`)
- Familiar pattern (annotations, social handles, doc tags)
- Easy for humans and AI to recognize

### Reference Examples

#### In documentation

```markdown
The relation separator logic (@typedb-relation-separator) checks
pattern types and applies semicolons for TypeDB 3.x compatibility.
```

#### In commit messages

```
Fix relation separator edge case

- Updated @typedb-relation-separator to handle nested relations
- Added test cases for 3-level nesting

Fixes #567
```

#### In code reviews

```
Nice optimization in @exponential-backoff-retry!

Should the max retry count be configurable?
```

#### In AI prompts

```
Review @concurrent-cache-access and suggest optimizations
while maintaining thread safety constraints.
```

#### In Slack/chat

```
@sarah Can you review @jwt-token-validation?
Possible timing attack vulnerability.
```

### Multi-Fragment References

#### Referring to entire logical block

```markdown
The query construction pipeline (@typedb-query-construction)
spans three components...
```

#### Referring to specific fragment

```markdown
The relation handling in @typedb-query-construction(2)
applies semicolon separators...
```

### Optional File Context

Usually unnecessary with unique names, but can add clarity when introducing:

```markdown
The relation separator (@typedb-relation-separator in QueryBuilder.kt)
handles TypeDB 3.x compatibility...
```

---

## When to Use Named Blocks

### DO Use Named Blocks For

- ✅ **Complex algorithms** worth explaining in `kb/` docs
- ✅ **Performance-critical code** with optimization notes
- ✅ **Workarounds** or temporary solutions
- ✅ **Known hacks** requiring future attention
- ✅ **Tech debt implementations** documented elsewhere
- ✅ **Key architectural decisions** in code
- ✅ **Patterns that repeat** across the codebase
- ✅ **Code likely to be discussed** or referenced

### DON'T Use Named Blocks For

- ❌ **Every function or class** (use structured API docs instead)
- ❌ **Trivial or self-explanatory code**
- ❌ **Code unlikely to be referenced**
- ❌ **Over-granular blocks** (entire function body usually too small)

### Appropriate Block Scope

#### Good scope (5-50 lines, logically cohesive)

```kotlin
// @block: retry-with-exponential-backoff
// @purpose: Handle transient failures with backoff
for (attempt in 1..5) {
    try {
        return operation()
    } catch (e: TransientException) {
        Thread.sleep(100L * (1 shl attempt))
    }
}
throw MaxRetriesExceededException()
// @end-block: retry-with-exponential-backoff
```

#### Too small (trivial)

```kotlin
// @block: increment-counter  // ❌
counter++
// @end-block: increment-counter
```

#### Too large (use KDoc instead)

```kotlin
// @block: entire-class  // ❌
class MyClass {
    // 500 lines...
}
// @end-block: entire-class
```

---

## Metadata Reference

### Standard Metadata Attributes

- **`@purpose`**: One-line explanation of why this code exists
- **`@context`**: Broader context or constraints
- **`@related`**: Links to `kb/` docs, ADRs, or other blocks
- **`@complexity`**: Algorithmic complexity (e.g., O(n²))
- **`@performance`**: Performance characteristics or benchmarks
- **`@temporal`**: Time-sensitive info (e.g., "Remove after 2025-Q2")
- **`@author`**: Original author (when attribution useful)

### AI-Specific Metadata

- **`@ai-context`**: Guidance for AI agents on using this block
- **`@ai-constraints`**: What AI should NOT change
- **`@ai-examples`**: Example usage or test cases

#### Example

```kotlin
// @block: levenshtein-distance
// @purpose: Calculate edit distance between strings
// @complexity: O(m*n) time, O(min(m,n)) space
// @related: kb/string-matching-algorithms.md
// @ai-context: Space-optimized DP; changes must maintain O(min(m,n)) space
// @ai-constraints: Must handle Unicode correctly
[implementation]
// @end-block: levenshtein-distance
```

---

## Integration with LEAP Workflow

### During Implementation

#### Add named blocks while coding

```kotlin
// 1. Implement complex algorithm
// @block: typedb-relation-separator
// @purpose: TypeDB 3.x requires semicolons for relation patterns
val separator = if (isRelation) ";" else ","
// @end-block: typedb-relation-separator

// 2. Add structured API docs (KDoc)
/**
 * Builds TypeQL query with proper separators.
 *
 * See @typedb-relation-separator for separator logic.
 */
fun buildQuery(): String { ... }
```

### In Implementation Documentation

#### Reference blocks from `kb/` docs

```markdown
# kb/query-builder-architecture.md

## TypeDB 3.x Compatibility

The QueryBuilder handles TypeDB 3.x syntax in the
@typedb-relation-separator block, which checks pattern types
and applies semicolon separators for relations.

This addresses TypeDB 3.x requirement documented in
kb/adr/typedb-3-syntax-requirements.md.
```

### In Commit Messages

```
Optimize cache access pattern

- Refactored @concurrent-cache-access for better performance
- Reduced lock contention by 40% in benchmarks
- See kb/performance-optimization-patterns.md

Closes #234
```

### In Code Reviews

```
Review comments:

1. @typedb-hash-workaround - Can we add target removal date?
2. @concurrent-cache-access - Consider making retry count configurable
3. Great work on @exponential-backoff-retry! LGTM ✅
```

### With AI Agents

```
Prompt: "Review @concurrent-cache-access and suggest optimizations
while maintaining the thread safety constraints in the metadata."

Prompt: "Explain the @levenshtein-distance algorithm and create
implementation documentation at kb/string-matching-algorithms.md"

Prompt: "The @validation-logic fragments are scattered across files.
Should they be refactored into a single location?"
```

---

## LEAP Compliance Requirements

### Level 1: Essential

#### Named blocks: Not required

Level 1 projects may use named blocks opportunistically but are not required to.

### Level 2: Standard

#### Named blocks: Recommended for complex/critical code

Named blocks are **recommended** (but not required) for:

- Performance-critical code sections
- Workarounds or temporary solutions
- Known hacks requiring future attention
- Tech debt implementations
- Complex algorithms documented in `kb/`

**Rationale:** Level 2 projects benefit from precise code references, but adoption can be gradual.

### Level 3: Comprehensive

#### Named blocks: Required for complex/critical code

Named blocks are **required** for:

- All performance-critical code sections
- All workarounds or temporary solutions
- All known hacks requiring future attention
- All tech debt implementations
- Complex algorithms with `kb/` implementation documentation

#### Verification

- [ ] Do all performance-critical sections have named blocks?
- [ ] Do all workarounds have named blocks with @temporal or @related metadata?
- [ ] Do all tech debt implementations reference named blocks?
- [ ] Are block names unique (verified with git grep)?

**Rationale:** Level 3 requires comprehensive documentation practices, and named blocks ensure precise references for critical code sections.

---

## Code Review Checklist

When reviewing code with named blocks:

```markdown
## Named Blocks Review

- [ ] All new block names are project-wide unique (verify with git grep)
- [ ] Block names are descriptive and follow naming conventions (2-5 words, kebab-case)
- [ ] Blocks have appropriate scope (5-50 lines, logically cohesive)
- [ ] Metadata is helpful and accurate (especially @purpose)
- [ ] Multi-fragment blocks are truly related
- [ ] Block references in docs use @block-name notation
- [ ] No outdated block metadata (treat as bugs)
```

---

## Project Registry (Optional)

Consider maintaining a registry of named blocks:

```markdown
# kb/meta/named-blocks-registry.md

Last updated: 2025-11-08

## Core Infrastructure (15 blocks)

- @typedb-relation-separator - QueryBuilder.kt:47
- @typedb-hash-before-insert-workaround - DatabaseService.kt:123
- @meridian-content-deduplication - StorageService.kt:89
- @exponential-backoff-retry - RetryPolicy.kt:34
- ...

## Authentication & Security (8 blocks)

- @jwt-token-validation - AuthService.kt:67
- @oauth-token-refresh-flow - OAuthClient.kt:145
- ...
```

### Benefits

- Quick conflict detection
- Easy discovery of existing blocks
- Documentation of block locations
- Can be generated automatically (future tool)

---

## Examples

### Example 1: Algorithm Documentation

#### Code

```kotlin
// @block: levenshtein-distance-calculation
// @purpose: Calculate edit distance between strings
// @complexity: O(m*n) time, O(min(m,n)) space
// @related: kb/string-matching-algorithms.md
fun levenshteinDistance(s1: String, s2: String): Int {
    val m = s1.length
    val n = s2.length
    val dp = IntArray(n + 1) { it }

    for (i in 1..m) {
        var prev = dp[0]
        dp[0] = i
        for (j in 1..n) {
            val temp = dp[j]
            dp[j] = if (s1[i-1] == s2[j-1]) prev
                   else 1 + minOf(prev, dp[j], dp[j-1])
            prev = temp
        }
    }
    return dp[n]
}
// @end-block: levenshtein-distance-calculation
```

#### In `kb/string-matching-algorithms.md`

```markdown
## Levenshtein Distance Implementation

The @levenshtein-distance-calculation block uses space-optimized
dynamic programming. Instead of maintaining a full m×n matrix,
it uses a rolling array to reduce space from O(m*n) to O(min(m,n)).

The algorithm processes one row at a time, keeping only the previous
row's values needed for the current computation...
```

### Example 2: Performance-Critical Code

#### Code

```kotlin
// @block: fast-hash-calculation
// @purpose: Critical path for content deduplication
// @performance: Benchmarked at 2GB/s on typical hardware
// @ai-context: Any changes must be profiled; this is hot path
// @related: kb/performance-benchmarks.md
fun calculateContentHash(content: ByteArray): String {
    val digest = MessageDigest.getInstance("SHA-512")
    val bufferSize = 8192
    for (offset in content.indices step bufferSize) {
        val end = minOf(offset + bufferSize, content.size)
        digest.update(content, offset, end - offset)
    }
    return digest.digest().toHexString()
}
// @end-block: fast-hash-calculation
```

### Example 3: Workaround with Removal Date

#### Code

```kotlin
// @block: typedb-hash-before-insert-workaround
// @purpose: TypeDB 3.0 requires hash before insert (issue #1234)
// @temporal: Remove when TypeDB 3.1 released (expected Q2 2025)
// @related: kb/adr/typedb-hash-ordering.md
val hash = calculateHash(content)
database.insert(content, hash)
// @end-block: typedb-hash-before-insert-workaround
```

### Example 4: Multi-Fragment Pattern

#### QueryBuilder.kt

```kotlin
// @block: typedb-query-construction
fun buildQuery(entities: List<Entity>): String {
    val buffer = StringBuilder("match\n")
    appendEntityPatterns(buffer, entities)
    return buffer.toString()
}
// @end-block: typedb-query-construction

// ... other code ...

// @block: typedb-query-construction(2)
private fun appendRelationPatterns(buffer: StringBuilder) {
    buffer.append(";")  // TypeDB 3.x separator
    relations.forEach { buffer.append("\n  ${it.pattern}") }
}
// @end-block: typedb-query-construction(2)
```

#### QueryValidator.kt

```kotlin
// @block: typedb-query-construction(3)
fun validateQuerySyntax(query: String): ValidationResult {
    return TypeDBSyntaxValidator.validate(query)
}
// @end-block: typedb-query-construction(3)
```

#### In documentation

```markdown
The query construction pipeline (@typedb-query-construction)
spans three components:

1. Main builder creates match clause and entity patterns
2. Relation handler applies TypeDB 3.x semicolon separators
3. Validator ensures syntax compliance

This separation allows independent testing of each concern.
```

---

## Migration Path

### For Existing Codebases

#### Week 1-2: Pilot

- Add named blocks to 1-2 complex features
- Document with block references in `kb/`
- Gather team feedback

#### Week 3-4: Expand

- Add blocks to performance-critical code
- Create naming convention guide
- Update code review checklist

#### Month 2+: Normalize

- Named blocks become standard practice
- Include in onboarding materials
- Refine conventions based on experience

### Gradual Adoption

- **Start with new code**: Apply to new features first
- **Add retroactively when needed**: If discussing existing code, add blocks then
- **Prioritize complex code**: Focus on algorithms, workarounds, performance-critical sections
- **Don't retrofit everything**: Add blocks incrementally as code is touched

---

## Relationship to Other Documentation

### Named Blocks vs. API Documentation

#### Different purposes

- **API docs (KDoc, JSDoc, etc.)**: Explain what public APIs do, parameters, return values
- **Named blocks**: Mark specific implementation sections for reference

#### Use both together

```kotlin
/**
 * Calculates edit distance between two strings.
 *
 * Implementation uses space-optimized DP algorithm.
 * See @levenshtein-distance-calculation for details.
 *
 * @param s1 First string
 * @param s2 Second string
 * @return Edit distance
 */
fun levenshteinDistance(s1: String, s2: String): Int {
    // @block: levenshtein-distance-calculation
    // @complexity: O(m*n) time, O(min(m,n)) space
    [implementation]
    // @end-block: levenshtein-distance-calculation
}
```

### Named Blocks vs. Implementation Docs

#### Complementary

- **Implementation docs (`kb/*.md`)**: Explain architecture, design decisions, algorithms
- **Named blocks**: Provide precise anchors into code from those docs

#### Example flow

1. Implementation doc explains algorithm in prose
2. References specific code with @block-name
3. Reader can jump to exact code location
4. Block metadata provides additional context

---

## Future Tooling Possibilities

With standardized named blocks, future tools could provide:

### IDE Features

- **Jump to block**: Cmd+Shift+B → "typedb-relation-separator" → Jump to code
- **Find references**: Right-click block → Show all mentions in code and docs
- **Auto-completion**: Type @type... → Suggests @typedb-relation-separator
- **Hover documentation**: Hover @block-name → Show metadata tooltip

### Build Tools

```bash
# Generate block index
$ leap-blocks index
Created: kb/meta/named-blocks-registry.md
Found: 47 named blocks across 23 files

# Verify uniqueness
$ leap-blocks verify
✓ All block names unique
⚠ Warning: 3 blocks have generic names (consider renaming)
```

### Documentation Generators

- Convert @block-name references to clickable links
- Generate block index in documentation
- Validate block references (catch broken links)

---

## FAQ

### Q: Won't this clutter the code?

**A:** Named blocks are used selectively for code worth referencing, not every function. Most functions don't need them—just complex algorithms, workarounds, and performance-critical sections.

### Q: How do I choose good block names?

**A:** Use descriptive, domain-specific names (2-5 words). Think: "What would I call this if I were explaining it to a teammate?" Follow the pattern: `[domain]-[function]-[qualifier]`

### Q: What if block names conflict?

**A:** Make them more specific. Add component prefix (`querybuilder-validation` vs `schemavalidator-validation`) or functional distinction (`runtime-validation` vs `compile-time-validation`).

### Q: Do I need metadata on every block?

**A:** No. Metadata is optional. Use it when it adds value—especially `@purpose` for non-obvious code, and `@ai-context` for AI guidance.

### Q: Should blocks replace KDoc/JSDoc comments?

**A:** No. Named blocks and API docs serve different purposes. Use both:

- **KDoc/JSDoc**: Document public APIs (what, params, returns)
- **Named blocks**: Mark specific implementation sections for reference

### Q: What happens if I refactor and move code?

**A:** Update the block name if the purpose changes significantly. If you're just moving code, the block moves with it—that's the point! Block names are more stable than line numbers.

### Q: Can I use this with other documentation methods?

**A:** Yes! Named blocks complement existing practices:

- Work alongside KDoc, JSDoc, Rust docs
- Reference from LEAP `kb/` documentation
- Compatible with ADRs and other standards

### Q: How do I verify block name uniqueness?

**A:** Use git grep before committing:

```bash
git grep "@block: my-new-block-name"
```

If results appear:

- **Choose a more specific name** if this is an unintentional conflict
- **Use `(n)` suffix** if you're intentionally creating a multi-fragment block across multiple locations

---

## Summary

Named code blocks provide a simple, non-invasive way to:

- ✅ Reference specific code sections precisely
- ✅ Anchor implementation documentation to code
- ✅ Enable AI-assisted development with targeted prompts
- ✅ Create logical groupings across multiple files
- ✅ Maintain stable references through refactoring

### Key principles

1. Use project-wide unique names (no file context needed)
2. Follow naming conventions (`domain-function-qualifier`, kebab-case, 2-5 words)
3. Reference with `@` prefix (`@block-name`)
4. Add metadata when it provides value
5. Use selectively for code worth referencing
6. Keep blocks current (treat outdated metadata as bugs)

#### Get started

1. Add blocks to your next complex algorithm or workaround
2. Reference them in implementation docs using `@block-name`
3. Try using block references in your next code review
4. Gather feedback and refine your team's conventions

Named blocks are an optional LEAP enhancement—use them where they add value, not everywhere.
