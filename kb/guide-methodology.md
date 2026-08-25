# LEAP Methodology

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** October 2025 (updated 2025-11-07)

---

**Quick Reference:** For fast lookups while working, see **[LEAP Cheatsheet](guide-cheatsheet.md)**

---

## Table of Contents

- [What is LEAP?](#what-is-leap)
- [Core Principles](#core-principles)
- [Project Structure](#project-structure)
- [Risk and Complexity Assessment](#risk-and-complexity-assessment)
- [Feature Branch Documentation](#feature-branch-documentation)
- [Tech Debt Management](#tech-debt-management)
- [Architecture Decision Records (ADRs)](#architecture-decision-records-adrs)
- [Implementation Documentation](#implementation-documentation)
- [Source Code Comments Best Practices](#source-code-comments-best-practices)
- [LEAP Development Workflow](#leap-development-workflow)
- [Working with AI Coding Agents](#working-with-ai-coding-agents)
- [LEAP Compliance Levels](#leap-compliance-levels)
- [Best Practices](#best-practices)
- [Common Pitfalls](#common-pitfalls)
- [Example: Complete Feature Workflow](#example-complete-feature-workflow)
- [Tools and Templates](#tools-and-templates)
- [LEAP Terminology Usage](#leap-terminology-usage)
- [LEAP Governance and Evolution](#leap-governance-and-evolution)
- [Glossary](#glossary)
- [Conclusion](#conclusion)

---

## What is LEAP?

**Literate (Extended-by-Agent) Programming (LEAP)** builds on the foundational goals of
Donald Knuth's Literate Programming—creating well-documented, maintainable, and usable
codebases—while embracing the transformative capabilities of AI coding agents.
Where traditional LP required specialized tools like WEB, noweb, or Docco to weave together
code and documentation, LEAP leverages conversational AI to naturally integrate explanation,
intent, and implementation. The result is a development approach where documentation and
code evolve together through iterative dialogue, making codebases not only more understandable
to human developers but also more accessible to the AI agents that increasingly assist
in their creation and maintenance. LEAP represents an evolution rather than a revolution:
the principles remain timeless, but the process has been dramatically streamlined for the
modern development environment.

## Core Principles

1. **Documentation First**: Begin with clear goals and requirements before writing code
2. **Iterative Refinement**: Develop through phased implementations with clear checkpoints
3. **Test Throughout**: Write tests during each phase, maintaining high coverage (target 90%+ for classes, statements, and branches)
4. **Comprehensive Context**: Maintain knowledge documents that enable both humans and AI agents to understand the codebase
5. **Transparent Evolution**: Track decisions, learnings, and rationale throughout the development process
6. **Agent-Friendly**: Structure documentation to be easily consumed by AI coding assistants

## Project Structure

### Knowledge Base (`kb`) Directory

A `kb` directory is a _knowledge base_ consisting of a structured collection of Markdown
_knowledge documents_. These documents should follow [markdown best practices](best-practices-markdown.md),
particularly ensuring blank lines separate block elements (code blocks, lists, tables) from
paragraph text for consistent rendering across different Markdown processors.

A project-wide `kb` directory must be located in the root of the project. Each project module
may contain a module-specific `kb` directory.

### Standard `kb` Directory Structure

```
kb/
├── guide-*.md                         # Usage documentation (how to use APIs, configure, deploy)
├── impl-*.md                          # Implementation documentation (architecture, design patterns, algorithms)
├── feature/                           # Feature branch documentation
│   └── <username>/<feature-name>/     # Per-feature subdirectory
│       ├── goals.md                   # Feature requirements (REQUIRED)
│       ├── plan.md                    # Implementation plan (RECOMMENDED)
│       ├── phase-1.md, phase-2.md     # Detailed phase documentation (optional)
│       ├── completion-summary.md      # Completion summary (REQUIRED before merge)
│       ├── pr-description.md          # Pull request description (concise summary of completion-summary)
│       └── tech-debt-*.md             # Resolved tech debt items (moved here when resolved)
├── adr/                               # Architecture Decision Records
│   └── adr-NNN__description.md        # ADRs with numeric identifier and description
└── meta/                              # LEAP process and methodology documentation
    ├── leap-*.md                      # LEAP methodology and guidelines
    ├── template-*.md                  # Document templates
    ├── best-practices-*.md            # Project-specific best practices
    ├── lessons-*.md                   # Lessons learned
    ├── tech-debt-*.md                 # Active technical debt (open issues)
    └── idea-*.md                      # Exploratory ideas
```

#### Directory Purposes

- **`.` (root `kb` directory)**: Contains **usage documentation** (`guide-*.md`) and **implementation documentation** (`impl-*.md`) about the actual product/code
- **`feature/<username>/<feature-name>/`**: LEAP feature development documentation
  - Fixed filenames: `goals.md` (required), `plan.md` (recommended), `phase-N.md` (optional), `completion-summary.md` (required), `pr-description.md`
  - Resolved tech debt items (`tech-debt-*.md`) moved here when resolved
- **`adr/`**: Architecture Decision Records (`adr-NNN__description.md`) documenting significant architectural choices
- **`meta/`**: LEAP process and methodology documentation (about our work, process, learning, and reflection)
  - `leap-*.md`: LEAP methodology documents
  - `template-*.md`: Document templates
  - `best-practices-*.md`: Project-specific best practices
  - `lessons-*.md`: Lessons learned
  - `tech-debt-*.md`: Active technical debt (open issues)
  - `idea-*.md`: Exploratory ideas

## Risk and Complexity Assessment

LEAP uses risk and complexity assessments instead of time estimates to characterize features and phases. These are distinct concepts that help plan and communicate about work:

### Risk

**Risk** measures external uncertainty and factors outside your control:

- **LOW**: Well-understood approach with proven technologies; minimal dependencies
- **MEDIUM**: Some external dependencies or integration points; approach mostly proven
- **HIGH**: Significant external dependencies; integration with unfamiliar systems; unproven approaches
- **VERY HIGH**: Multiple high-risk factors; critical external dependencies; experimental technologies

#### Risk Factors

- External API dependencies
- Integration complexity with other systems
- Unproven or experimental technologies
- Critical dependencies on other teams' work
- Regulatory or compliance requirements
- Data migration or compatibility concerns

### Complexity

**Complexity** measures technical difficulty and internal factors:

- **LOW**: Straightforward implementation; few components affected; well-established patterns
- **MEDIUM**: Moderate implementation challenges; multiple components; some design decisions needed
- **HIGH**: Significant technical challenges; many components affected; non-trivial design decisions
- **VERY HIGH**: Highly complex implementation; architectural changes; novel algorithms or data structures

#### Complexity Factors

- Number of components/modules affected
- Algorithmic or data structure complexity
- Architectural impact
- Need for new design patterns
- Performance optimization requirements
- Testing difficulty

### Risk vs Complexity

- **High Risk, Low Complexity**: Simple code but depends on unreliable external API
- **Low Risk, High Complexity**: Complex algorithm using well-established techniques
- **High Risk, High Complexity**: Novel distributed system with external dependencies

### Documentation Practice

Only mention risk or complexity when NOT LOW. If both are LOW, no assessment is needed in the documentation. This keeps documentation concise and highlights the notable aspects.

#### Example in goals.md

```markdown
## Risk and Complexity Assessment

**Overall Risk:** MEDIUM - Depends on integration with external payment gateway

**Overall Complexity:** HIGH - Requires new distributed transaction handling
```

#### Example in plan.md Phase

```markdown
**Risk:** MEDIUM - External API may change during development

**Complexity:** HIGH - Complex state machine with many edge cases
```

## Feature Branch Documentation

### Overview

All development work on a codebase must occur in a feature branch. Each active feature branch
has a correspondingly named `kb/feature/<feature-branch-name>` subdirectory.

### Feature Directory Placement

For projects with multiple modules, feature documentation can be placed in either the top-level
`kb/feature/` directory or a module-specific `<module>/kb/feature/` directory based on the
scope of the feature.

#### Decision Criteria

Use **top-level** `kb/feature/<feature-branch-name>/` when:

- The feature touches multiple modules
- The feature involves cross-cutting concerns (build system, CI/CD, documentation standards)
- The feature affects project-wide architecture or infrastructure

Use **module-specific** `<module>/kb/feature/<feature-branch-name>/` when:

- The feature only modifies a single module
- All changes are isolated to one module's codebase
- The feature is a module-internal refactoring or enhancement

#### Examples

```
# Top-level: Multi-module CLI framework refactoring
kb/feature/faseidl/meridian-7/
  ├── goals.md
  ├── plan.md
  └── completion-summary.md

# Module-specific: Meridian-only storage service enhancement
meridian/kb/feature/faseidl/meridian-4/
  ├── goals.md
  ├── plan.md
  └── completion-summary.md
```

#### Best Practices

- When in doubt, start in module-specific location and move to top-level if scope expands
- Feature directory location should match the git branch name pattern
- Document cross-module dependencies clearly in goals.md regardless of location
- Both locations follow the same structure (goals.md, plan.md, etc.)

#### Example Directory Structure

For a branch named `faseidl/my-feature`:

- If top-level: `kb/feature/faseidl/my-feature/`
- If module-specific: `<module>/kb/feature/faseidl/my-feature/`

### Feature Documents

#### `goals.md` (required)

The **goals document** specifies the goals and requirements of the development effort. This is
essentially a requirements document for the feature branch.

**Template:** Use the standalone template at `kb/template-goals.md` as a starting point.

#### Purpose

- Define clear, measurable objectives for the feature
- Establish success criteria
- Identify constraints and assumptions
- Provide context for why this feature is needed

#### Contents should include

- **Executive Summary**: 1-2 paragraphs explaining what and why
- **Objectives**: Numbered list of specific goals to achieve
- **Requirements**: Detailed functional and non-functional requirements
- **Success Criteria**: How will we know when this feature is complete?
- **Constraints**: Technical limitations, dependencies
- **Assumptions**: What we're assuming to be true
- **Out of Scope**: Explicitly state what this feature will NOT do

**Illustrative example** (the template at `kb/template-goals.md` is the authoritative source):

```markdown
# <Feature Name> Goals

**Author:** [Your Name](https://www.linkedin.com/in/your-profile/)

**Date:** [Date]

---

## Executive Summary
[What and why in 1-2 paragraphs. Briefly explain what this feature accomplishes and why it's needed.]

## Objectives
1. Primary objective
2. Secondary objective
3. Tertiary objective

## Requirements

### Functional Requirements
- REQ-1: Description
- REQ-2: Description
- REQ-3: Description

### Non-Functional Requirements
- Performance targets
- Security requirements
- Scalability needs
- Maintainability requirements

### Testing Requirements
- Code coverage targets (aim for 90%+ for classes, statements, and branches)
- Critical paths that must be tested
- Performance test requirements
- Integration test requirements
- Edge cases and error conditions

### Documentation Requirements
- Structured API documentation (KDoc, JSDoc, Rust docs, etc.) for all public APIs, interfaces, and primary classes
- Implementation docs for complex algorithms and data structures
- Inline comments for complex logic and non-obvious decisions
- Usage examples and guides

## Success Criteria
- [ ] Measurable criterion 1
- [ ] Measurable criterion 2
- [ ] Code coverage meets or exceeds targets
- [ ] All public APIs, interfaces, and primary classes have structured documentation
- [ ] Integration tests pass with real dependencies

## Constraints
- Technical constraints (e.g., compatibility requirements, technology limitations)
- Dependency constraints (e.g., external APIs, libraries)

## Assumptions
- Assumption 1
- Assumption 2
- Assumption 3

## Out of Scope
- Feature X (reason: deferred to Phase 2)
- Capability Y (reason: not needed for this iteration)
- Optimization Z (reason: premature at this stage)
```

#### `plan.md` (recommended)

The **plan document** specifies the high-level implementation strategy for achieving the stated
goals. A plan typically organizes the effort into a series of numbered phases.

**Template:** Use the standalone template at `kb/template-plan.md` as a starting point.

#### Purpose

- Break down large features into manageable chunks
- Establish a logical sequence of implementation
- Identify dependencies between phases
- Provide a roadmap for tracking progress

#### Contents should include

- **Overview**: Brief recap of goals and approach with overall risk/complexity assessment
- **Phase Descriptions**: For each phase:
  - Goals and deliverables
  - Risk and complexity assessment (only mention if NOT LOW)
  - Dependencies
  - Testing approach (tests created during this phase, not deferred)
  - Success criteria (including coverage targets)
  - What's explicitly deferred
- **Risk Assessment**: Potential issues and mitigation strategies
- **Decision Points**: When to proceed vs. reassess

#### Key principles for planning

- **Minimal Viable Increments**: Each phase should deliver working functionality
- **Early Unblocking**: Prioritize work that unblocks other teams or features
- **Explicit Deferrals**: Clearly state what's NOT included in each phase
- **Decision Points**: Include checkpoints where progress is evaluated

#### `phase-<n>.md` (optional)

Each **phase document** contains a detailed implementation plan for a specific phase. Create
these when a phase requires substantial detail beyond what fits in `plan.md`.

#### Purpose

- Provide detailed implementation guidance for complex phases
- Document specific technical decisions
- Include code structure, API designs, or algorithms
- Serve as a comprehensive guide for implementation

#### When to create

- Phase involves multiple sub-components
- Technical complexity requires detailed explanation
- Multiple developers will work on the phase
- Phase requires specific examples or templates

#### Contents should include

- **Phase Goals**: Recap from `plan.md`
- **Implementation Approach**: Technical strategy
- **Component Breakdown**: Detailed structure
- **Code Organization**: File structure, module organization
- **Examples**: Code snippets, API usage examples
- **Testing Strategy**: How to verify this phase
- **Integration Points**: How this phase connects to others

#### `completion-summary.md` (required)

The **completion summary document** describes the results of the development effort. This document will
be used to create the merge request description when the feature work is ready to merge, and serves
as a permanent record of what was accomplished in the feature branch.

**Template:** Use the standalone template at `kb/template-completion-summary.md` as a starting point.

#### Purpose

- Provide a complete record of what was accomplished
- Document key decisions and their rationale
- Highlight important changes for reviewers
- Create pull request description content

#### Contents should include

- **Overview**: What was built and why
- **Changes Summary**: High-level description of modifications
- **Key Implementation Details**: Important technical decisions
- **Testing**: What was tested and how
- **Breaking Changes**: Any incompatibilities (if applicable)
- **Migration Guide**: Steps for users to adapt (if needed)
- **Known Limitations**: Issues deferred or still outstanding
- **Related Issues**: References to tickets, discussions

#### Best practices

- Write after feature is complete but before creating merge request
- Be concise but comprehensive
- Focus on "what changed" and "why" not "how" (code shows how)
- Include enough context for reviewers unfamiliar with the feature
- Highlight areas needing special review attention

## Tech Debt Management

### Overview

Tech debt items are discovered issues that require future work. LEAP practices provide clear conventions for creating, tracking, and resolving tech debt documentation.

### Creating Tech Debt Documents

**Template:** Use the standalone template at `kb/template-tech-debt.md` as a starting point.

When discovering issues that cannot be immediately resolved:

1. **Create tech debt document**:
   - Project-wide: `kb/meta/tech-debt-<topic>.md`
   - Module-specific: `<module>/kb/tech-debt-<topic>.md`
2. **Document the issue** with context, impact, and proposed solutions
3. **Record ownership** in the document's `Tracking Issue:` header field — the issue that owns remediation, in your tracking system's canonical form, or `none` if no issue has been filed
4. **Reference from feature docs** where the issue was discovered

An issue that merely records where the debt was discovered is not a tracking issue. Provenance belongs in the document's own "Related Issues" section, under "References"; when the discovering work closes, an unowned document is left behind with nothing driving it. `none` is the honest value in that case, and it makes the document findable when untracked debt is triaged.

### Resolving Tech Debt

When resolving tech debt items in a feature branch:

1. **Update the document** with resolution details:
   - Change Status to `done`, optionally qualified after an em-dash, hyphen, or double hyphen (e.g., `done - resolved in phase 3`)
   - Add "Resolved" date
   - Add "Resolution" section with implementation details, verification, and files modified
   - Close the tracking issue, if the document names one

2. **Move to feature directory**: `kb/feature/<username>/<feature-name>/tech-debt-<topic>.md`
   - The document sits directly in the feature directory, alongside `goals.md` and `completion-summary.md`
   - Location is authoritative: the move is what marks the debt resolved, and the Status value simply agrees with it. A document still in `kb/meta/` or `<module>/kb/` is unresolved whatever its Status says, and a document with no Status field takes its status from its location.
   - Keeps `kb/meta/` and `<module>/kb/` clean (only unresolved items)
   - Preserves resolution context with the feature that fixed it
   - Enables natural garbage collection when feature branches are archived

3. **Reference in completion summary**: List resolved tech debt in the feature's completion summary

#### Example

```
# When resolving tech debt in feature branch faseidl/jcl-phase-1
git mv kb/meta/tech-debt-program-id-extraction-missing.md \
       kb/feature/faseidl/jcl-phase-1/
```

#### Benefits of this convention

- ✅ Clear separation: Tech debt files in `kb/meta/` or `<module>/kb/` show only unresolved items
- ✅ Contextual documentation: Resolution details stay with the feature
- ✅ Natural lifecycle: Archived feature branches take resolved tech debt with them
- ✅ Discoverability: Easy to see open vs resolved at a glance
- ✅ LEAP alignment: Branch-specific documentation in branch directory

## Architecture Decision Records (ADRs)

Architecture Decision Records (ADRs) document significant architectural and design decisions made during development. ADRs capture the context, decision, rationale, and consequences of important technical choices.

**Template:** Use the standalone template at `kb/template-adr.md` as a starting point.

**For complete ADR guidance**, including when to create ADRs, naming conventions, lifecycle, and numbering policy, see:

- **ADR leap-adr-001**: `kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md`

## Implementation Documentation

### What is Implementation Documentation?

Implementation documentation explains **HOW** the code works internally, preserving the core principle of Donald Knuth's Literate Programming: code should be written to explain to humans how it works, not just to instruct computers.

#### Implementation docs cover

- Data structures and their design rationale
- Algorithms and their complexity characteristics
- Design patterns and architectural decisions
- System architecture and component interactions
- Performance considerations and trade-offs
- Non-obvious implementation choices

**Implementation docs live in** `kb/` as markdown files alongside usage documentation.

### When to Write Implementation Docs

#### Do create implementation documentation for

- Complex algorithms that aren't obvious from code alone
- Non-trivial data structures and their relationships
- System architecture and how components interact
- Design patterns and why they were chosen
- Performance-critical code with optimization rationale
- Architectural constraints and requirements

#### Examples from the codebase

- `kb/meridian/meridian_api.md` - Meridian API design and architecture
- `kb/meridian/meridian-typedb-integration.md` - Integration architecture
- `kb/query-builder-architecture.md` (proposed) - DSL design and implementation

### What Belongs in Source Comments Instead

Implementation documentation in `kb/` is for broad architecture and complex algorithms. The following belong in source code comments, not in separate `kb/` documents:

- Line-by-line code explanations
- API documentation (use structured doc comments: KDoc for Kotlin, JSDoc for ReasonML/JavaScript, Rust doc comments, etc.)
- Simple utility function descriptions
- Inline explanations of complex logic

#### Source comments are free to reference kb/ documents for additional context

```kotlin
// TypeDB 3.x requires semicolons to separate relation patterns from entity patterns
// See: kb/adr/typedb-3-syntax-requirements.md for full design rationale
val separator = if (isRelation) ";" else ","
```

### Integration with Feature Development

Implementation documentation should be written:

- **During implementation phases**: As you build complex components, document the architecture
- **During documentation phase**: Ensure all complex algorithms and data structures are documented
- **Before merge request creation**: Implementation docs should be complete before submitting merge request

Include implementation documentation in:

- **Merge request checklists**: Authors should verify implementation docs are current
- **Review checklists**: Reviewers should check for adequate implementation documentation
- **completion-summary.md**: List key implementation docs created or updated

## Source Code Comments Best Practices

### Overview

Source code comments are the second layer of documentation in LEAP, complementing the kb/ documentation. While implementation docs in `kb/` explain broad architecture, source comments provide detailed explanations within the code itself.

The project uses multiple languages, each with their own comment conventions:

- **Kotlin**: KDoc (`/** ... */`)
- **ReasonML/JavaScript**: JSDoc (`/** ... */`)
- **Rust**: Doc comments (`/// ...` or `//! ...`)
- **Bash**: Comment headers (`# ...`)
- **TypeQL**: Schema comments (`# ...`)

Throughout this section, we use KDoc examples as the canonical reference, but the same principles apply to all languages.

### When to Write Comments

#### DO write comments for

- **All public APIs** (required): Structured doc comments for all public functions, classes, interfaces
- **All interface definitions** (required): Complete documentation of all interfaces
- **All "primary" classes** (required): Class `Foo` in file `Foo.kt` must have structured documentation
- **Complex algorithms**: Non-obvious logic or business rules
- **Non-obvious design decisions**: Why this approach was chosen
- **Workarounds**: For bugs, limitations, or constraints
- **Performance-critical code**: With explanation of trade-offs
- **Security-sensitive operations**: With security rationale

#### DON'T comment

- Obvious code ("increment i", "loop through items")
- Redundant information already in function names
- What the code does (code shows that) - comment WHY instead

### Structured API Documentation

#### Required for

- All public APIs (functions, methods, properties)
- All interface definitions
- All "primary" classes (e.g., class Foo in file Foo.kt)

#### Kotlin (KDoc) example

```kotlin
/**
 * Builds TypeQL queries using a fluent DSL.
 *
 * This builder uses semicolon separation for relation patterns
 * to comply with TypeDB 3.x syntax requirements.
 *
 * @param database The TypeDB database connection
 * @constructor Creates a QueryBuilder with the specified database connection
 * @author [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)
 * @see [TypeDB 3.x Documentation](https://typedb.com/docs)
 */
class QueryBuilder(private val database: Database) {
    /**
     * Creates a match clause for querying entities.
     *
     * @param block Builder block for constructing match patterns
     * @return This builder for method chaining
     * @throws IllegalStateException if match clause already exists
     */
    fun match(block: MatchBuilder.() -> Unit): QueryBuilder {
        // Implementation
    }
}
```

#### Required elements

- **Classes/interfaces**: Purpose, key responsibilities, related components
- **Public functions/methods**: What it does, parameters, return value, exceptions
- **Public properties/fields**: Purpose and valid values
- **Complex algorithms**: Approach and why chosen

#### Language-specific variations

- **ReasonML/JSDoc**: Similar structure, uses `@param`, `@returns`, `@throws`
- **Rust**: Doc comments with markdown, examples tested by compiler
- **Bash**: Function documentation headers with parameter descriptions
- **TypeQL**: Schema element descriptions with usage notes

### Inline Comments

#### Good inline comments explain WHY and reference broader context

```kotlin
// TypeDB 3.x requires semicolons to separate relation patterns from entity patterns
// See: kb/adr/typedb-3-syntax-requirements.md
val separator = if (isRelation) ";" else ","

// Performance optimization: reuse builder instead of allocating new one
// Benchmarked 2x faster for queries with 100+ elements
val builder = builderCache.getOrPut(key) { StringBuilder(256) }

// Workaround for TypeDB issue #1234: hash calculation must happen before insert
// TODO: Remove when TypeDB 3.1 is released (Q2 2025)
val hash = calculateHash(content)
```

#### Poor inline comments (avoid these)

```kotlin
// Set x to 5
val x = 5

// Loop through items
items.forEach { item ->
    // Process the item
    process(item)
}
```

### Architecture Comments

For complex files/modules, add file-level architecture comments (examples shown in Kotlin, adapt to each language):

```kotlin
/**
 * QueryBuilder Implementation
 *
 * Architecture:
 * - MatchBuilder: Handles entity and relation patterns
 * - SelectBuilder: Handles projection of results
 * - InsertBuilder: Handles data insertion
 *
 * Key Design Decision: Relations tracked separately to enable
 * proper semicolon separation per TypeDB 3.x requirements.
 *
 * See: kb/query-builder-architecture.md for full details
 */
```

Similar patterns in other languages:

- **ReasonML**: Module-level comments at file start
- **Rust**: Module doc comments (`//!`)
- **Bash**: Header comment block explaining script purpose

### TODO and FIXME Comments

Use language-agnostic format (works in all languages with `//` or `#` comments):

#### TODO format

```kotlin
// TODO(faseidl): Add support for nested relations (Phase 2)
// TODO: Optimize for large result sets (low priority)
// TODO(2025-Q2): Remove workaround after TypeDB 3.1 upgrade
```

#### FIXME format

```kotlin
// FIXME: Race condition possible with concurrent writes
//        Reproduces under heavy load (see issue #456)
//        Mitigation: Use optimistic locking
```

### Keep Comments Current

#### Outdated comments are bugs and should be treated as such.

#### Anti-pattern

```kotlin
// Returns the user's email address
fun getUserName(): String {  // ← Function was refactored but comment wasn't updated!
    return user.name
}
```

#### Best practices

- Update comments when refactoring code
- Remove obsolete comments immediately
- Treat outdated comments as bugs in code reviews
- This applies equally to all languages: Kotlin, ReasonML, Rust, Bash, TypeQL

## LEAP Development Workflow

### Phase 1: Planning

1. **Create Feature Branch**

   ```bash
   git checkout -b <username>/<feature-name>
   ```

2. **Create Feature Directory**

   ```bash
   mkdir -p kb/feature/<username>/<feature-name>
   ```

3. **Draft Goals Document**

   Create `kb/feature/<username>/<feature-name>/goals.md` with comprehensive requirements.

   #### Work iteratively with AI agent

   - Start with high-level objectives
   - Refine through dialogue to identify edge cases
   - Clarify ambiguities and unstated assumptions
   - Validate against similar features or prior work

4. **Review and Refine Goals**

   Share goals document with stakeholders or team for feedback. Update based on input.

5. **Commit Goals**

   ```bash
   git add kb/feature/<username>/<feature-name>/goals.md
   git commit -m "Add goals for <feature-name> feature"
   ```

### Phase 2: Design

1. **Create Implementation Plan**

   Create `kb/feature/<username>/<feature-name>/plan.md` breaking work into phases.

   #### Principles for good plans

   - Start with smallest viable increment
   - Each phase should be completable in days not weeks
   - Early phases unblock other teams
   - Explicitly defer complex features to later phases
   - Include decision points for course correction

2. **Review Plan**

   Discuss plan with team, especially if it affects other components or teams.

3. **Commit Plan**

   ```bash
   git add kb/feature/<username>/<feature-name>/plan.md
   git commit -m "Add implementation plan for <feature-name>"
   ```

### Phase 3: Implementation

For each phase in your plan:

1. **Create Phase Document (if needed)**

   If the phase is complex, create `kb/feature/<username>/<feature-name>/phase-<n>.md`
   with detailed implementation guidance.

2. **Implement Phase**

   Write code according to the plan, iterating with your AI agent:

   #### Agent collaboration tips

   - Reference the goals and plan documents in conversations
   - Ask agent to review phase completion before moving on
   - Have agent help identify test cases from requirements
   - Use agent to validate against best practices

   #### Key practices

   - Write tests during each phase (not at the end)
   - Aim for 90%+ coverage across classes, statements, and branches
   - Tests can be written before code (TDD) or alongside it, but never defer to the end
   - Verify coverage after completing each phase
   - Write structured API documentation (KDoc, JSDoc, Rust docs, etc.) for all public APIs, interfaces, and primary classes as you code
   - Add inline comments for complex logic and non-obvious decisions
   - Create implementation docs for complex algorithms and data structures
   - Update usage and implementation documentation as you go
   - Document significant architectural decisions in ADRs
   - **Commit by Milestone**: Make separate, logical commits after completing each major milestone of the branch lifecycle (e.g., once goals are approved, once the plan is approved, and as each phase of the plan is completed). This creates a highly readable, incremental git history.
   - Keep commits focused and well-described

3. **Commit Phase Work**

   After completing a phase, commit with a comprehensive message:

   ```bash
   git add .
   git commit -m "$(cat <<'EOF'
   Implement Phase N: <phase-name>

   - Key change 1
   - Key change 2
   - Key change 3

   Phase N of the <feature-name> feature plan.
   See kb/feature/<username>/<feature-name>/plan.md for full context.
   EOF
   )"
   ```

   #### Commit message guidelines

   - First line: Brief summary (imperative mood, <72 chars)
   - Blank line
   - Detailed description with bullet points for key changes
   - Reference relevant documentation
   - Never credit AI agents as authors

### Phase 4: Documentation

1. **Verify Source Comments**

   Ensure all code has appropriate comments:

   - All public APIs have structured documentation (KDoc, JSDoc, Rust docs, etc.)
   - All interfaces have complete documentation
   - All primary classes (e.g., class Foo in Foo.kt) have structured documentation
   - Complex logic has inline comments explaining WHY
   - No outdated comments (treat as bugs)

2. **Update Usage Documentation**

   Update main `kb/` documentation to reflect new capabilities:

   - API documentation
   - Configuration guides
   - Usage examples
   - Migration guides (if breaking changes)

3. **Create or Update Implementation Documentation**

   Document complex internals in `kb/`:

   - Architecture overviews for complex components
   - Data structure designs and rationale
   - Algorithm descriptions and complexity analysis
   - Design pattern usage and justification
   - Performance trade-offs and optimization strategies

4. **Create ADRs (if applicable)**

   If you made significant architectural decisions, document them in `kb/adr/`:

   ```bash
   kb/adr/<feature-name>-decision-description.md
   ```

5. **Document Lessons Learned (if applicable)**

   If you discovered important patterns or anti-patterns, add to:

   ```bash
   kb/meta/lessons-learned-<topic>.md
   ```

### Phase 5: Completion

1. **Create Completion Summary Document**

   Create `kb/feature/<username>/<feature-name>/completion-summary.md` documenting what was accomplished.

2. **Commit Completion Summary**

   ```bash
   git add kb/feature/<username>/<feature-name>/completion-summary.md
   git commit -m "Add completion summary for <feature-name>"
   ```

3. **Push Feature Branch**

   ```bash
   git push origin <username>/<feature-name>
   ```

4. **Create Merge Request**

   Use the `completion-summary.md` content as the merge request description. The completion summary provides reviewers with:

   - Complete context on what changed and why
   - Highlights of key implementation decisions
   - Testing approach and results
   - Areas needing specific review attention

## Working with AI Coding Agents

### Effective Agent Collaboration

LEAP is designed to work seamlessly with AI coding agents like Claude. Here's how to collaborate effectively:

#### 1. Provide Comprehensive Context

At the start of a session, point the agent to relevant documentation:

```
I'm working on implementing Phase 2 of the storage service feature.
Please read:
- kb/feature/faseidl/storage-service/goals.md
- kb/feature/faseidl/storage-service/plan.md
- kb/meta/best-practices-for-quality-kotlin-code.md

Let's implement the database schema as outlined in the plan.
```

#### 2. Reference Documentation Throughout

Keep the agent aligned with your plan:

```
Looking at the plan.md, Phase 2 includes database schema and basic CRUD operations.
Let's focus on the schema first, ensuring it matches the requirements in goals.md.
```

#### 3. Leverage Agent Expertise

Use the agent to validate your approach:

```
Review this implementation against the goals document.
Are we meeting all the requirements? Any edge cases we're missing?
```

#### 4. Iterate on Documentation

Refine documentation with agent help:

```
Review this goals document. Are the requirements clear? Any ambiguities?
Help me identify constraints or assumptions I haven't explicitly stated.
```

#### 5. Request Implementation Documentation Drafts

Have the agent create initial implementation documentation:

```
Review the QueryBuilder implementation and create a draft of
kb/query-builder-architecture.md explaining:
- Overall architecture and key components
- Data structures (MatchBuilder, relationElements tracking)
- Why semicolons are used for relation separation
- How the DSL pattern works
```

#### 6. Review Comment Quality

Ask the agent to assess documentation completeness:

```
Review the comments in FilesetQueries.kt:
- Are structured docs (KDoc) complete for all public APIs, interfaces, and the primary class?
- Are inline comments helpful or redundant?
- Are there complex sections that need comments?
- Any outdated comments that don't match the code?
```

#### 7. Identify Documentation Needs

Have the agent suggest what documentation to create:

```
Looking at the changes in this phase, what implementation
documentation should I create in kb/? Consider:
- Are there complex algorithms that need explanation?
- New data structures that aren't obvious from code?
- Non-obvious design decisions that should be documented?
```

#### 8. Provide Documentation Context

When refactoring, give the agent both code and docs:

```
I'm refactoring the QueryBuilder. Please read:
- kb/query-builder-architecture.md (implementation overview)
- kb/adr/typedb-3-syntax-requirements.md (why semicolons)
- QueryBuilder.kt (current implementation with KDoc)

Now help me refactor the relation separator logic while
maintaining the architecture and design constraints.
```

### Agent-Friendly Documentation

#### Write for Both Humans and Agents

- Use clear headings and structure
- Include explicit context and motivation
- Link related documents
- Provide concrete examples
- State assumptions explicitly
- Mark TODOs and deferred items clearly

#### Good Example

```markdown
## Phase 1a Goals

Implement basic file storage API to unblock Knowledge Graph team.

**Requirements:**
- POST /files endpoint for upload
- GET /files endpoint for download
- Calculate SHA-512 hash server-side
- Store metadata in SQLite

**Explicitly Deferred to Phase 1b:**
- Authentication (local use only)
- Content deduplication
- PostgreSQL migration
```

#### Poor Example

```markdown
## Phase 1a

Do the basic stuff. Add auth later.
```

### Gating Mandates for AI Agents

While AI coding agents are highly proactive and capable, they must operate under a strict **collaborative gating mandate** to prevent project drift and maintain human alignment. If you are an AI agent reading this guide, you are required to strictly adhere to the following execution gates:

#### 1. The Multi-Step Gating Sequence
You must never "race ahead" or combine drafting and execution into a single, unilateral step. You are a peer programmer, and the human developer is the sole authority for project progression:

- **Phase A: Goals**: Draft the `goals.md` file in the feature directory. **Stop and wait for explicit human review and approval** before doing anything else.
- **Phase B: Plan**: Once goals are approved, draft the `plan.md` file outlining the implementation and testing steps. **Stop and wait for explicit human review and approval** of the plan.
- **Phase C: Execution**: Only after the plan is approved may you proceed to write code, implement tests, and modify existing files.

#### 2. Checkbox Control (Success Criteria)

- Under no circumstances may you modify incomplete checkboxes (`- [ ]`) to complete (`- [x]`) in any `goals.md`, `plan.md`, or project checklists on your own.
- Marking a checkbox as complete requires **explicit human review and authorization**. You may only update a checkbox to completed (`[x]`) on the developer's behalf after they have explicitly reviewed the implemented behavior and instructed you to do so.

#### 3. Feature Branch Finalization

- You must never unilaterally decide that a feature is complete.
- Do not write the `completion-summary.md` or stage any commits until the human developer has verified all success criteria, checked off the success checkboxes, and explicitly directed you to finalize the feature branch.

#### 4. Sequential Phase Gating (No Jumping Ahead)

- **One Phase Per Turn:** During the feature execution phase, you must strictly limit your implementation scope to the single planned Phase requested by the human developer. You must NEVER write code, add tests, or modify files for any other phase in the same conversational turn or session.
- **Mandatory Pausing at Phase Boundaries:** At the end of every planned phase, you must halt, present your completed work (e.g., code, tests, or documentation) along with linter and validation results, and **stop and wait for explicit human review and approval** before starting any work on the next phase. This is a hard gate.
- **TDD Exceptions Still Gate:** Permitting a bypass of test-first TDD for non-functional tasks (such as editing markdown, tweaking configurations, or reorganizing assets) is NOT a loophole to bypass gating. Non-functional phases must still stop, present their completed work, and wait for human review/approval before committing and ending their turn.
- **Atomic Phase Commits:** Every planned phase must have its own separate, dedicated git commit. You are strictly prohibited from combining or staging changes from multiple phases into a single commit.

#### 5. Turn-Gated Feature Finalization

- **Two-Step Finalization:** The feature finalization process (compiling completion summaries, final success criteria assessments, and performing the final git commit) is a strict two-step, turn-gated workflow. You are strictly prohibited from compiling the `completion-summary.md` and performing the finalization git commit or success checkbox updates in a single conversation turn.
- **First-Turn Gating:** On the first turn of feature finalization, you must only gather git information, draft the `completion-summary.md` file (uncommitted), and present the checklist assessment. You MUST STOP and wait for the developer's explicit review and approval of these files and checklist assessment.
- **Second-Turn Commit:** You may only update the success checkboxes in `goals.md`/`plan.md` on the developer's behalf and perform the final milestone commit on a subsequent turn AFTER the user has explicitly confirmed their approval.

#### 6. Turn-Gated PR Preparation and Submission

- **Two-Step Submission:** Preparing and submitting a Pull Request (generating titles, drafting descriptions, pushing branches, and creating the pull request) is a strict two-step, turn-gated workflow. You are strictly prohibited from generating titles, drafting descriptions, and executing a branch push or PR creation in a single conversation turn.
- **First-Turn Gating:** On the first turn of PR preparation, you must only draft the PR description (if requested), generate the proposed conventional PR title, and present them along with the PR creation options. You MUST STOP and wait for the developer to review and approve the title and settings.
- **Second-Turn Submission:** You may only execute the branch push or create the Pull Request on a subsequent turn AFTER the user has explicitly reviewed and approved your proposed title, description, and submission settings.

## LEAP Compliance Levels

LEAP supports incremental adoption through three compliance levels. Teams can start with essential practices (Level 1) and progressively adopt more comprehensive standards as they mature.

### The Three Levels

**Level 1: Essential** - Minimum viable LEAP practices

- Required feature documentation (goals.md, plan.md, completion-summary.md)
- Basic test coverage (50% or project minimums)
- Public API documentation
- Feature branch workflow

**Level 2: Standard** - Recommended for most projects

- All Level 1 requirements
- Risk/complexity assessment
- 90%+ test coverage target
- Comprehensive code documentation
- Guide docs for major features, impl docs for complex code
- Local documentation generation capability
- Named code blocks (recommended for complex/critical code)
- ADRs and tech debt documentation

**Level 3: Comprehensive** - Full LEAP adoption

- All Level 2 requirements
- Quick summaries and phase documents
- Comprehensive inline comments
- Named code blocks (required for complex/critical code)
- CI automatically publishes documentation
- Consistent LEAP terminology usage

### Choosing Your Level

- **Start with Level 1** if you're new to LEAP or have a small team
- **Adopt Level 2** for production projects requiring high quality
- **Pursue Level 3** for business-critical or highly complex systems

### Detailed Requirements

For complete requirements, checklists, and guidance:

- **[LEAP Compliance Levels](guide-compliance-levels.md)** - Detailed requirements, verification checklists, and choosing guidance
- **[LEAP Settings Template](template-leap-settings.md)** - Configure project-specific compliance requirements

## Best Practices

### Commit Messages

#### Format

```
<imperative-summary>

- Detailed change 1
- Detailed change 2
- Detailed change 3

[Optional: Reference to documentation or context]
```

#### Guidelines

- Use imperative mood ("Add feature" not "Added feature")
- First line under 72 characters
- Body provides context on what and why
- Never credit AI agents ("Co-authored-by: Claude")
- Reference relevant documentation or phases

#### Examples

```
Fix TypeQL relation separator for TypeDB 3.x syntax

- Relations now use semicolons to separate from entity patterns
- Added tests to verify relation separator behavior
- Updated existing tests with incorrect expectations
- Fixed FilesetFile.fileId type from Long to String (UUID)

Fixes the QueryBuilder to comply with TypeDB 3.x requirements.
```

### Progressive Documentation

#### Don't wait until the end to document

- Write goals.md BEFORE coding
- Write plan.md BEFORE implementing
- Update usage docs AS YOU code
- Write completion-summary.md AFTER completion

#### This approach

- Clarifies thinking before implementation
- Provides checkpoints for course correction
- Reduces "catch-up" documentation burden
- Keeps documentation accurate and fresh

### Testing Throughout Development

#### Tests are not an afterthought

- Write tests DURING each phase, not at the end
- Target 90%+ coverage for classes, statements, and branches
- Test-Driven Development (TDD) is encouraged but not required
- What matters: tests written progressively, not deferred
- Verify coverage after each phase before moving to the next

#### Anti-pattern to avoid

- Implementing all features first, then writing tests
- This leads to:
  - Lower quality tests (designed around implementation, not requirements)
  - Missed edge cases and error conditions
  - Difficulty achieving coverage goals
  - Untested code merged to main branch

#### Best approach

- Write tests as you implement each component
- Use requirements from goals.md to identify test cases
- Ensure each phase includes both code and tests
- Review coverage metrics before considering phase complete

### Phased Development

#### Break large features into phases

- **Phase 1**: Minimal viable increment that provides value
- **Phase 2**: Production readiness improvements
- **Phase 3**: Advanced features and optimizations

#### Benefits

- Unblock dependent teams early
- Get feedback sooner
- Reduce risk of major rework
- Maintain team momentum

#### Example from Meridian

- **Phase 1a (5 days)**: Local file storage with SQLite - unblocks teams
- **Phase 1b (2 weeks)**: Add PostgreSQL, S3, auth - production basics
- **Phase 1c (2 weeks)**: Enhanced metadata, operations - production ready

### Living Documentation

#### Documentation should evolve with code

- Update usage docs when APIs change
- Add lessons learned when discovering patterns
- Create ADRs for significant decisions
- Refine best practices based on experience

#### Keep kb/ organized

- Feature branch documentation remains useful after merge for understanding recent changes
- Periodically clean out old feature branch documentation once it has outlived its usefulness
- Archive significant feature documentation if needed for historical reference
- Consolidate related lessons learned into meta/ documents
- Update main documentation after each feature

## Common Pitfalls

### 1. Documentation After the Fact

**Problem:** Writing goals/plan after coding begins

**Solution:** Resist urge to "just start coding." Spend time on goals.md first.

### 2. Vague Requirements

**Problem:** Goals like "make it better" or "add feature X"

**Solution:** Define specific, measurable success criteria and explicit constraints.

### 3. No Decision Points

**Problem:** Plans that assume everything goes perfectly

**Solution:** Include checkpoints: "After Phase 1a, evaluate if approach is working."

### 4. Skipping the Completion Summary

**Problem:** Creating merge request without completion summary

**Solution:** Write completion-summary.md before pushing. It helps you and reviewers.

### 5. Missing Context for Agents

**Problem:** Agent doesn't understand your codebase conventions

**Solution:** Create and reference meta/ documents for patterns and practices.

### 6. Deferring Tests to the End

**Problem:** Writing all code first, then adding tests as an afterthought

**Solution:** Write tests during each phase. Verify coverage before moving to next phase. Treat untested code as incomplete.

### 7. Inadequate or Outdated Comments

**Problem:** No structured documentation on public APIs, interfaces, and primary classes. Missing inline comments for complex logic. Outdated comments that don't match the code.

#### Solution

- Write structured API documentation (KDoc, JSDoc, Rust docs, etc.) as you define public APIs, interfaces, and primary classes
- Add inline comments for complex logic and non-obvious decisions immediately
- Update comments during refactoring—treat outdated comments as bugs
- Include comment quality in merge request reviews (both author and reviewer checklists)
- Use AI agent to review comment quality and completeness

## Example: Complete Feature Workflow

Let's walk through a complete example of implementing a new feature using LEAP.

**Scenario:** Add file versioning to the Meridian storage service.

### 1. Create Feature Branch and Directory

```
git checkout -b faseidl/file-versioning
mkdir -p kb/feature/faseidl/file-versioning
```

### 2. Draft Goals Document

Create `kb/feature/faseidl/file-versioning/goals.md`:

```markdown
# File Versioning Feature Goals

## Executive Summary
Add support for storing and retrieving multiple versions of the same file,
enabling temporal analysis of source code changes over time. This supports
the Knowledge Graph team's need to track how programs evolve.

## Objectives
1. Store multiple versions of files at the same logical path
2. Retrieve any historical version by version identifier
3. List all versions of a file
4. Maintain content deduplication across versions

## Requirements

### Functional Requirements
- REQ-1: Each file upload creates a new version
- REQ-2: Versions identified by timestamp and sequential number
- REQ-3: API to retrieve specific version
- REQ-4: API to list all versions with metadata
- REQ-5: Content deduplication works across versions

### Non-Functional Requirements
- Performance: Version queries < 200ms (95th percentile)
- Storage: Deduplication prevents significant storage increase
- Backward compatible: Existing APIs continue to work

### Testing Requirements
- Maintain 90%+ coverage for all new code (classes, statements, branches)
- Test version creation, retrieval, and listing
- Test deduplication across versions
- Performance tests with 100+ versions per file
- Integration tests with existing API clients

## Success Criteria
- [ ] Can upload 10 versions of same file
- [ ] Can retrieve any historical version
- [ ] Can list all versions with timestamps
- [ ] Storage only increases for actual content changes
- [ ] Existing clients work without modification
- [ ] Test coverage meets 90%+ targets

## Constraints
- Must use existing database schema patterns
- Cannot break existing API contracts

## Assumptions
- Most file updates contain some content changes
- Version listings typically retrieve recent versions
- Clients can handle version identifiers in responses

## Out of Scope
- Version comparison/diff API (Phase 2)
- Branching/merging across versions (future)
- Automatic version expiration (future)
```

### 3. Review and Commit Goals

```
# After team review and refinement
git add kb/feature/faseidl/file-versioning/goals.md
git commit -m "Add goals for file versioning feature"
```

### 4. Create Implementation Plan

Create `kb/feature/faseidl/file-versioning/plan.md`:

```markdown
# File Versioning Implementation Plan

## Overview
Implement file versioning in three phases.

## Phase 1: Database Schema

**Goals:**
- Extend database schema to support versions
- Implement migration from existing schema
- Verify performance with test data

**Approach:**
- Add versions table with foreign key to files
- Update content deduplication to reference versions
- Create indexes for common queries

**Testing:**
- Unit tests for schema operations
- Migration tests with sample data
- Performance tests for version queries

**Success Criteria:**
- [ ] Schema supports all requirements
- [ ] Migration completes without data loss
- [ ] Version queries meet performance targets
- [ ] Phase tests achieve 90%+ coverage

**Explicitly Deferred:**
- API implementation
- UI changes
- Client library updates

## Phase 2: Core APIs

**Goals:**
- Implement version creation on upload
- Add version retrieval endpoint
- Add version listing endpoint

**New Endpoints:**
- `POST /files` - Enhanced to create versions
- `GET /files/versions` - List all versions
- `GET /files?version=<id>` - Get specific version

**Testing:**
- Unit tests for each endpoint
- Integration tests for full workflows
- Backward compatibility tests with existing clients
- Edge case tests (invalid versions, missing files)

**Success Criteria:**
- [ ] Upload creates new version
- [ ] Can retrieve any version
- [ ] Version list includes metadata
- [ ] Backward compatibility maintained
- [ ] Phase tests achieve 90%+ coverage

**Explicitly Deferred:**
- Version comparison API
- Bulk operations
- Version retention policies

## Phase 3: Final Validation and Documentation

**Goals:**
- Verify overall test coverage meets targets
- Fill any remaining coverage gaps
- Update documentation
- Integration testing with Knowledge Graph team

**Testing:**
- Review combined coverage from all phases
- Add tests for any gaps (should be minimal if phases tested well)
- Performance tests with 100+ versions
- End-to-end integration tests

**Documentation:**
- API reference updates
- Usage examples
- Migration guide for clients

## Risk Mitigation

**Risk:** Schema migration fails on production data
**Mitigation:** Test migration on copy of production DB first

**Risk:** Performance degrades with many versions
**Mitigation:** Include performance tests in Phase 1

**Risk:** Breaking existing clients
**Mitigation:** Extensive backward compatibility testing

## Decision Points

After Phase 1:
- Continue if migration works and performance acceptable
- Reassess schema if performance issues discovered

After Phase 2:
- Continue if APIs work and backward compatible
- Extend timeline if integration issues found
```

### 5. Commit Plan

```
git add kb/feature/faseidl/file-versioning/plan.md
git commit -m "Add implementation plan for file versioning"
```

### 6. Implement Phases

For each phase, work with AI agent to implement, test, and commit.

### 7. Create Completion Summary

After completion, create `kb/feature/faseidl/file-versioning/completion-summary.md`:

```markdown
# File Versioning Feature Summary

## Overview
Implemented full file versioning support for Meridian storage service,
enabling temporal analysis of source code evolution.

## Changes

### Database Schema
- Added `file_versions` table with version metadata
- Enhanced content deduplication to work across versions
- Created indexes for version queries

### API Endpoints
- Enhanced `POST /files` to create versions automatically
- Added `GET /files/versions` to list all versions
- Added `version` query parameter to `GET /files`

### Backward Compatibility
- Existing API calls work unchanged
- Clients receive version info in response headers
- Content deduplication continues working

## Key Implementation Details

**Version Identification:**
- Each version assigned monotonic sequence number
- Versions also include upload timestamp
- Version IDs are globally unique UUIDs

**Deduplication:**
- Content hash used across all versions
- Only changed content stored as new blobs
- Unchanged files create new version metadata only

## Testing
- 93% code coverage achieved (classes: 95%, statements: 92%, branches: 91%)
- Performance tests verify < 200ms queries (95th percentile: 145ms)
- Integration tested with Knowledge Graph team
- Backward compatibility verified with existing clients
- Tests written progressively during each phase, not deferred to end

## Known Limitations
- No version comparison API (deferred to Phase 2)
- No automatic version expiration (future work)
- Maximum 10,000 versions per file (implementation limit)

## Migration Guide
No action required for existing clients. New version information
available in response headers:
- `X-File-Version-Number`: Sequential version number
- `X-File-Version-Id`: Unique version identifier

To use new capabilities:
- List versions: `GET /files/versions?path=<path>`
- Get version: `GET /files?path=<path>&version=<id>`

## Related Issues
- Closes #123: Support file versioning
- Enables #456: Temporal code analysis
```

### 8. Create Merge Request

```
git push origin faseidl/file-versioning

# Create merge request using completion-summary.md as description
```

## Tools and Templates

### Standalone Template Files

LEAP templates are available as standalone files for easy copying and use by both humans and AI agents:

#### Feature Development Templates

- **Goals Template:** `kb/template-goals.md`
- **Plan Template:** `kb/template-plan.md`
- **Phase Template:** `kb/template-phase.md`
- **Completion Summary Template:** `kb/template-completion-summary.md`
- **PR Description Template:** `kb/template-pr-description.md`

#### Other Document Templates

- **ADR Template:** `kb/template-adr.md`
- **Best Practices Template:** `kb/template-best-practices.md`
- **Lessons Learned Template:** `kb/template-lessons.md`
- **Tech Debt Template:** `kb/template-tech-debt.md`
- **Idea Template:** `kb/template-idea.md`

These templates reflect LEAP best practices and are the authoritative source for document structure.

#### Using Templates

1. Copy the appropriate template from `kb/template-*.md`
2. Follow the structure and guidance provided in the template
3. Delete any template guidance sections marked for deletion
4. See the "Example: Complete Feature Workflow" section below for how all documents work together

## LEAP Terminology Usage

LEAP is an **internal development methodology** for our team. Understanding when and where to use LEAP terminology helps maintain clear communication:

### Internal Use (Encouraged)

Use LEAP terminology freely in:

- Knowledge base documentation (`kb/` directories)
- Feature branch documentation (goals, plans, completion summaries)
- Architecture Decision Records (ADRs)
- Code comments explaining documentation structure
- Team discussions and planning sessions
- Development process documentation

**Example:** "This feature follows LEAP practices with goals.md, plan.md, and completion-summary.md."

### User-Facing Contexts (Avoid)

Do NOT expose LEAP terminology in:

- End-user documentation or help pages
- Public-facing API documentation
- Customer release notes
- Marketing materials
- Product UI or error messages

**Why:** Users care about features and capabilities, not our internal development process. LEAP helps us build better software, but users benefit from the outcomes, not the methodology itself.

**Instead of:** "This feature was developed using LEAP methodology."<br>
**Use:** "This feature includes comprehensive documentation and testing."

### Exception: Open Source and Technical Audiences

When contributing to open source projects or writing for technical audiences (blog posts, conference talks), you may explain LEAP as a development practice. The focus should be on the value it provides (better documentation, iterative development, high test coverage) rather than the acronym itself.

## LEAP Governance and Evolution

LEAP is a living, open-source methodology that evolves based on community experience. We use a lightweight, public governance model to propose, evaluate, and adopt improvements:

### LEAP Improvement Proposals (LIPs)

When you identify a potential improvement to LEAP methodology:

1. **Submit a Proposal**: Create a **GitHub Issue** on the [blunderstone/leap](https://github.com/blunderstone/leap) repository using the dedicated **LEAP Improvement Proposal** template.
2. **Community Feedback**: Maintainers and community members will review, discuss, and evaluate the proposal directly in the issue thread.
3. **Continue with current work**: Do not implement proposed changes immediately in project work until they are formally accepted.

#### Proposal Format

The GitHub issue template pre-populates standard fields to keep proposal signals high:

- **Context**: What situation prompted this idea? (Include concrete examples from actual features).
- **Current State**: How does LEAP work today?
- **Proposed Change**: What improvement are you suggesting?
- **Benefits & Drawbacks**: Honest, explicit assessment of trade-offs.
- **Alternatives Considered (Optional)**: Other options that were considered and rejected.

### Review and Adoption Process

1. **Proposal**: Anyone can propose a LEAP improvement via GitHub Issues.
2. **Review**: Proposals are evaluated based on:
   - Whether they address a real, recurring pain point from actual development.
   - Alignment with LEAP core principles (such as minimality, explicit composition, and self-enforcing conventions).
   - Practicality of implementation cost and mental overhead.
3. **Decision & Labeling**: Proposals are assigned standard labels and status tags (such as `accepted`, `deferred`, or `implemented`) directly within GitHub.
4. **Implementation**: Accepted proposals are scheduled and implemented via standard feature branches.
5. **Documentation**: Once implemented, core templates, taxonomy guides, and best practices are updated.

### When to Propose Improvements

#### Do Propose When

- You notice repeated friction or confusion in the LEAP workflow.
- You implement the same workaround multiple times across different features.
- You identify missing guidance or ambiguities in the LEAP guides.

#### Don't Propose For

- One-time, highly specific edge cases.
- Personal preferences without structural or functional benefit.
- Ideas that conflict with LEAP's core principles.

### Current Governance

LEAP governance is managed by the maintainers of the `blunderstone/leap` repository with community input. Propose improvements or discuss ideas on the official [GitHub Issues](https://github.com/blunderstone/leap/issues) tracker.

## Glossary

### LEAP Terms

#### LEAP (Literate (Extended-by-Agent) Programming)
: A methodology for software development that combines comprehensive documentation with AI-assisted coding, building on Donald Knuth's Literate Programming principles.

#### LIP (LEAP Improvement Proposal)
: A proposal to improve or change the LEAP methodology itself, tracked publicly as a GitHub Issue on the `blunderstone/leap` repository. See `kb/guide-improvement-proposals.md`.

### Document Types

#### goals.md
: REQUIRED feature document defining objectives, requirements, success criteria, and constraints. Must include Quick Summary and Executive Summary.

#### plan.md
: RECOMMENDED feature document breaking work into phases with goals, approach, testing strategy, and success criteria for each phase.

#### phase-N.md
: OPTIONAL detailed documentation for a specific implementation phase (e.g., phase-1.md, phase-2.md).

#### completion-summary.md
: REQUIRED feature document describing implementation results, testing metrics, and documentation created. Written before creating merge/pull request.

#### pr-description.md
: Concise pull request description summarizing completion-summary.md for reviewers. Should be brief with link to full completion summary.

#### ADR (Architecture Decision Record)
: Document recording a significant architectural decision, its context, rationale, and consequences. Named `adr-NNN__description.md`.

### Directory Structure

#### kb/ (Knowledge Base)
: Root directory for all project documentation. Contains usage docs, implementation docs, and subdirectories for features, ADRs, and meta-documentation.

#### kb/feature/<username>/<feature-name>/
: Directory for LEAP feature branch documentation. Contains goals.md, plan.md, completion-summary.md, etc.

#### kb/adr/
: Directory for Architecture Decision Records.

#### kb/meta/
: Directory for LEAP methodology documentation, templates, best practices, lessons learned, tech debt, and ideas.

#### Feature Branch
: Git branch for developing a specific feature, with corresponding documentation in `kb/feature/<username>/<feature-name>/`.

### Risk and Complexity

#### Risk
: Measures external uncertainty and factors outside your control (external dependencies, unproven approaches, integration complexity).

#### Complexity
: Measures technical difficulty and internal factors (number of components, algorithms, architectural impact).

#### Risk/Complexity Levels
: LOW, MEDIUM, HIGH, VERY HIGH. Only mention in documentation when NOT LOW.

### Documentation Categories

**Usage Documentation (guide-*.md)**
: Documentation about how to use APIs, configure systems, or deploy applications.

**Implementation Documentation (impl-*.md)**
: Documentation about how code works internally: architecture, data structures, algorithms, design patterns.

#### Meta-Documentation
: Documentation about our development process, learning, and reflection (lives in kb/meta/).

### Other Terms

#### Knowledge Document
: Any Markdown document in the kb/ directory structure that contributes to project knowledge.

#### Chief Architect
: Role responsible for LEAP governance and methodology decisions.

#### Structured API Documentation
: Formal documentation using KDoc (Kotlin), JSDoc (JavaScript), Rust docs, etc. for all public APIs and interfaces.

#### Coverage Targets
: Aim for 90%+ coverage for classes, statements, and branches. Project minimums: 87% line, 84% instruction, 57% branch.

## Conclusion

LEAP programming combines the best of traditional software engineering documentation practices
with modern AI-assisted development. By maintaining comprehensive, structured knowledge documents,
teams can:

- Clarify thinking before coding
- Collaborate more effectively with AI agents
- Maintain institutional knowledge
- Onboard new developers quickly
- Make better technical decisions
- Reduce documentation burden through progressive writing

The key is to embrace documentation as a natural part of the development process, not an
afterthought. When documentation guides development rather than following it, both code
and documentation benefit.
