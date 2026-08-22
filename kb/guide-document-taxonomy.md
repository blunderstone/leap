# Document Taxonomy and Naming Guide

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2025-11-07<br>
**Last Updated:** 2026-01-20

---

## Table of Contents

- [Overview](#overview)
- [Quick Reference](#quick-reference)
- [File Naming Patterns](#file-naming-patterns)
  - [Prefix-First Pattern](#prefix-first-pattern)
  - [Rationale](#rationale)
  - [Standard Prefixes](#standard-prefixes)
  - [Custom Prefixes](#custom-prefixes)
- [Document Types and Locations](#document-types-and-locations)
  - [Architecture Decision Records (ADRs)](#architecture-decision-records-adrs)
  - [LEAP Feature Documentation](#leap-feature-documentation)
  - [Best Practices](#best-practices)
  - [Lessons Learned](#lessons-learned)
  - [Technical Debt](#technical-debt)
  - [Ideas](#ideas)
  - [Templates](#templates)
  - [LEAP Methodology Documentation](#leap-methodology-documentation)
  - [Usage and Implementation Guides](#usage-and-implementation-guides)
  - [User Guides and README Files](#user-guides-and-readme-files)
- [Standard Prefixes](#standard-prefixes)
  - [Prefixes for Meta-Documentation](#prefixes-for-meta-documentation-about-our-workprocess)
  - [Prefixes for System Documentation](#prefixes-for-system-documentation-about-the-productcode)
  - [Custom Prefixes](#custom-prefixes)
- [Naming Convention Principles](#naming-convention-principles)
  - [General Rules](#general-rules)
  - [When to Use Numbers](#when-to-use-numbers)
  - [Identifier vs Description](#identifier-vs-description)
- [Summary of Document Naming Conventions](#summary-of-document-naming-conventions)
  - [By Location](#by-location)

---

## Overview

This guide defines the taxonomy of documents in a LEAP-compliant project's knowledge base and establishes naming conventions for each document type.

## Quick Reference

| Document Type | Location | Naming Pattern | Example |
|---------------|----------|----------------|---------|
| ADRs (top-level) | `kb/adr/` | `adr-NNN__description.md` | `leap-adr-001__adr-numbering-policy.md` |
| ADRs (module) | `<module>/kb/adr/` | `<module>-adr-NNN__description.md` | `cobol-tools-cli-adr-001__single-cli.md` |
| LEAP features (top-level) | `kb/feature/<user>/<name>/` | `goals.md`, `plan.md`, `phase-N.md` (with hierarchical sections OR separate `phase-N.M-<topic>.md` files for complex phases), `completion-summary.md`, `pr-description.md`, others | `kb/feature/faseidl/leap-1/goals.md`, `kb/feature/faseidl/ontology/phase-1.2-evaluation.md` |
| LEAP features (module) | `<module>/kb/feature/<user>/<name>/` | Same as top-level | `fileset-manager-cli/kb/feature/faseidl/scale/goals.md` |
| LEAP methodology | `kb/meta/` | `leap-<topic>.md` | `leap-best-practices.md` |
| Templates | `kb/meta/` | `template-<type>.md` | `template-adr.md` |
| Best practices (project) | `kb/meta/` | `best-practices-<topic>.md` | `best-practices-kotlin-coding.md` |
| Best practices (module) | `<module>/kb/` or `<module>/kb/meta/` | `best-practices-<topic>.md` | `web-ui/kb/best-practices-reasonml.md` |
| Lessons learned (project) | `kb/meta/` | `lessons-<topic>.md` | `lessons-typedb-performance.md` |
| Lessons learned (module) | `<module>/kb/` or `<module>/kb/meta/` | `lessons-<topic>.md` | `fileset-manager-cli/kb/meta/lessons-parallel-upload.md` |
| Technical debt (project) | `kb/meta/` | `tech-debt-<topic>.md` | `tech-debt-test-coverage.md` |
| Technical debt (module) | `<module>/kb/` or `<module>/kb/meta/` | `tech-debt-<topic>.md` | `api-server/kb/tech-debt-auth-refactor.md` |
| Ideas (project) | `kb/meta/` | `idea-<topic>.md` | `idea-graphql-api.md` |
| Ideas (module) | `<module>/kb/` or `<module>/kb/meta/` | `idea-<topic>.md` | `web-ui/kb/idea-dark-mode.md` |
| Benchmarks (project) | `kb/meta/` | `benchmark-<topic>.md` or `benchmark-<topic>-YYYY-MM-DD.md` | `benchmark-query-performance.md` |
| Benchmarks (module) | `<module>/kb/` or `<module>/kb/meta/` | `benchmark-<topic>.md` or `benchmark-<topic>-YYYY-MM-DD.md` | `api-server/kb/benchmark-api-throughput-2025-12-15.md` |
| Dev notes (local only) | Anywhere (gitignored) | `dev-note-<topic>.md` | `dev-note-debugging-session.md` |
| Usage guides | `kb/` or `<module>/kb/` | `guide-<topic>.md` | `guide-cli-framework.md`, `api-server/kb/guide-api.md` |
| Implementation docs | `kb/` or `<module>/kb/` | `impl-<topic>.md` | `impl-query-builder.md`, `api-server/kb/impl-pooling.md` |
| Primary documentation | Module root | `!ReadMe.<tool-name>.md` | `!ReadMe.kg-tools.md` |
| Categorized guides | Module root | `!ReadMe.<category>.<tool-name>.md` | `!ReadMe.quickstart.cobol-tools.md` |
| Test resource docs | Test resource directories | `!ReadMe.md` | `src/jvmTest/resources/dependency-analyzer-tests/!ReadMe.md` |
| GitHub auto-display (rare) | Module root | `README.md` (document rationale) | `repository-root/README.md` |

**Note:** Custom prefixes permitted when content doesn't fit standard categories.

---

## File Naming Patterns

### Prefix-First Pattern

**All knowledge base documents must use the prefix-first naming pattern.** The category prefix always comes first, followed by the descriptive topic.

#### Correct pattern

```
<prefix>-<descriptive-topic>.md
```

#### Examples

✅ **Correct:**

- `impl-content-deduplication.md` - Implementation document
- `guide-coverage-reporting.md` - Usage guide
- `best-practices-logging.md` - Best practices document
- `lessons-parallel-upload-performance.md` - Lessons learned
- `tech-debt-test-coverage.md` - Technical debt tracking

❌ **Incorrect:**

- `content-deduplication-implementation.md` - Suffix pattern (WRONG)
- `coverage-reporting-guide.md` - Suffix pattern (WRONG)
- `logging-best-practices.md` - Suffix pattern (WRONG)

### Rationale

The prefix-first pattern provides several benefits:

1. **Alphabetical grouping:** Files sort by category in directory listings
2. **Instant categorization:** Category is immediately visible
3. **Consistency:** One standard pattern across all document types
4. **Discoverability:** Easy to find all documents of a given type
5. **Tool compatibility:** Predictable patterns for scripts and automation

### Standard Prefixes

Common prefixes used in the knowledge base:

- `impl-` - Implementation documentation
- `guide-` - Usage guides and how-tos
- `best-practices-` - Coding standards and practices
- `lessons-` - Lessons learned from experience
- `tech-debt-` - Technical debt tracking
- `idea-` - Ideas and proposals
- `benchmark-` - Performance benchmarks
- `leap-` - LEAP methodology documentation
- `template-` - Document templates
- `adr-NNN__` - Architecture Decision Records (numbered)
- `dev-note-` - Temporary developer notes (gitignored)

### Custom Prefixes

When content doesn't fit standard categories, custom prefixes are permitted. Follow these guidelines:

- Use lowercase with hyphens: `custom-prefix-topic.md`
- Keep prefix concise (1-2 words)
- Document the prefix purpose in the file itself
- Consider whether content should use an existing category instead

---

## Document Types and Locations

### Architecture Decision Records (ADRs)

**Purpose:** Document significant architectural and design decisions with rationale.

#### Naming Convention

- **Top-level ADRs**: `adr-NNN__description.md`
- **Module-specific ADRs**: `<module>-adr-NNN__description.md`
- Double underscore `__` separates identifier from description
- Use exact module directory name as prefix

#### Location

- Top-level/cross-cutting: `kb/adr/`
- Module-specific: `<module>/kb/adr/`

#### Examples

- `kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md`
- `cobol-tools-cli/kb/adr/cobol-tools-cli-adr-001__single-cli-architecture.md`

**Reference:** ADR leap-adr-001 for complete policy

#### Choosing Between an ADR and an Implementation Document

To determine whether a proposed document should be written as an Architecture Decision Record (ADR) or as an implementation document (such as `impl-` or `guide-`), apply these four questions to the content in front of you:

1. **Could a competent architect have reasonably chosen otherwise?**
   If no other alternative can be named that someone would actually defend, there is no real decision, and the document is describing a mechanism, not establishing a policy. "Straw-man" options in the *Options Considered* section are a reliable tell that the document is not a genuine ADR.

2. **Is it binding on work not yet written?**
   An ADR constrains future code, establishing a standard or policy. A reviewer can cite an accepted ADR to reject a pull request. An implementation document, on the other hand, cannot be violated—it can only become outdated.

3. **Would a code change make this document wrong, or merely make it history?**
   An ADR is a historical record of a decision made at a specific point in time; it remains true as of its date forever. An implementation document stops matching the code and becomes false when the code changes. If your answer to a code change is "we would edit this document to update it," it is an implementation document, not an ADR.

4. **Does the title assert something one could disagree with?**
   A title that is a claim or an imperative (e.g., *Serve HTTP/1.1 Only on TLS Connectors*, *Retire the Deprecated command__calls Relation*, *Stored Line Offsets Are Source Truth*) describes a decision. A title that is a noun phrase naming a subsystem (e.g., *API Server Architecture*, *Storage Abstraction Layer*) describes a component and belongs in an implementation or guide document. This heuristic typically sorts documents perfectly.

##### The Consequences Boundary

The *Consequences* section of an ADR states effects, not instructions. For example, "Callers must now handle a body on a 503" is a consequence. "Here is how to handle a 503 response in Python..." is implementation content and does not belong in an ADR.

##### The Splitting Rule

When a decision requires substantial explanation, write two documents:

1. **The ADR** which keeps the *Issue*, *Decision*, *Options Considered*, and *Consequences* sections, and links forward to the implementation document.
2. **The Implementation Document** (using `impl-` or `guide-`) which keeps the mechanism, code examples, usage, pitfalls, and troubleshooting details, and cites the ADR for the "why".

A section titled *Implementation Details*, *Usage*, *How to Run*, *Common Pitfalls*, *Best Practices*, or *Future Enhancements* does not belong in an ADR.

##### The Maintenance Rule

An accepted ADR should never need editing except to change its status or to record that it was superseded. If you are editing an ADR because the code changed, the edited content was never ADR content.

##### Remediation Guidance

When a project reviews its documentation and discovers existing ADRs that do not conform to these standards, follow these remediation rules to clean them up without damaging the historical record:

- **ADR numbers are permanent.** Never renumber, delete, or reuse ADR numbers. Other documents, commit messages, and source comments cite them.
- **If the document contains a real decision, split it.** Trim the original ADR to include only the *Issue*, *Decision*, *Options Considered*, and *Consequences* sections. Move the removed explanation, walkthrough, or setup guide into a new `impl-` or `guide-` document in the appropriate `kb/` folder and cross-link them. The ADR retains its original number and date.
- **If the document contains no decision at all, supersede it.** Mark the status of the ADR as `superseded` and provide a forward pointer to the `impl-` or `guide-` document that replaces it, rather than deleting the file.
- **Record remediation as ordinary feature work.** Do not make silent edits. Trimming changes what a permanent document says, and the reasoning for the remediation belongs in a normal development branch.

---

### LEAP Feature Documentation

**Purpose:** Document feature development following LEAP methodology.

#### Naming Convention

- `goals.md` - Feature goals and requirements (REQUIRED)
- `plan.md` - Implementation plan (RECOMMENDED for complex features)
- `phase-N.md` - Detailed phase documentation (e.g., `phase-1.md`, `phase-2.md`)
- `completion-summary.md` - Results and metrics (REQUIRED before merge)
- `pr-description.md` - Pull request description
- Other supporting documents as needed (use descriptive names)

#### Hierarchical Phase Numbering

For complex phases requiring decomposition, choose between two approaches based on complexity:

##### Approach 1: Hierarchical Sections (Moderate Complexity)

Use hierarchical numbering **within** a single phase document:

- Document file: `phase-2.md`
- Within the document: Use "Phase 2.1", "Phase 2.2", "Phase 2.3" as section headings
- This enables recursive breakdown of complex phases while maintaining simple file naming
- Good for: Phases with logical sub-components that are closely related

#### Example structure within `phase-2.md`

```markdown
# Phase 2: Implement Core Features

## Phase 2.1: Database Schema

...

## Phase 2.2: API Endpoints

...

## Phase 2.3: Integration Tests

...
```

##### Approach 2: Separate Files with Topic Suffixes (High Complexity)

Create separate phase documents with hierarchical numbering and descriptive topic suffixes:

- Document files: `phase-1.1-<topic>.md`, `phase-1.2-<topic>.md`, `phase-1.3-<topic>.md`
- Format: `phase-N.M-<descriptive-topic>.md`
- Topic suffix provides semantic context for navigation
- Good for: Phases with substantial sub-phases that are independently valuable, lengthy, or require separate review

#### Example file structure

```
kb/feature/faseidl/ontology-namespace-framework-enhancement/
  goals.md
  plan.md
  phase-1.1-research-findings.md
  phase-1.2-source-of-truth-evaluation.md
  phase-1.3-source-of-truth-detailed-analysis.md
  phase-1.4-ai-integration-considerations.md
  completion-summary.md
```

#### Benefits of separate files

- Clear document progression (1.1 → 1.2 → 1.3 → 1.4)
- Each sub-phase can be substantial without creating unwieldy single file
- Easy to understand relationships between documents
- Topic suffixes provide semantic context (what, not just which)
- Better for incremental review and discussion

#### When to use separate files

- Sub-phases produce 5+ pages each (separate files easier to navigate)
- Sub-phases are independently reviewable or discussable
- Clear progression where each sub-phase builds on previous
- Phase decomposition is known upfront in planning

#### When to use hierarchical sections

- Sub-phases are short (1-3 pages each)
- Sub-phases are tightly coupled and hard to separate
- Single document flow is more important than modularity
- Total phase content < 15 pages

#### Location

- Top-level/cross-cutting features: `kb/feature/<username>/<feature-name>/`
- Module-specific features: `<module>/kb/feature/<username>/<feature-name>/`

#### Examples

- `kb/feature/faseidl/leap-1/goals.md`
- `kb/feature/faseidl/leap-1/plan.md`
- `kb/feature/faseidl/leap-1/phase-1.md`
- `kb/feature/faseidl/leap-1/completion-summary.md`
- `cobol-tools-cli/kb/feature/jsmith/new-command/goals.md`

#### Directory Naming

- Use lowercase with hyphens
- Format: `<username>/<feature-name>`
- Keep feature names concise and descriptive

---

### Best Practices

**Purpose:** Document recommended patterns, conventions, and approaches for how we work and develop.

#### Naming Convention

- LEAP-specific: Prefix `leap-` (Note: Omitted in the core `leap` repository itself, where all guides are LEAP-specific by definition)
- Project-specific: Prefix `best-practices-`
- Format: `best-practices-<topic>.md`
- Self-describing prefix for clarity

#### Location

- Project-wide: `kb/meta`
- Module-specific: `<module>/kb/`

#### Examples

- `kb/meta/leap-best-practices.md` (LEAP methodology)
- `kb/meta/best-practices-kotlin-coding.md` (project-wide coding standards)
- `api-server/kb/best-practices-api-design.md` (module-specific practices)

---

### Lessons Learned

**Purpose:** Capture insights, discoveries, and learnings about our development.

#### Naming Convention

- Prefix: `lessons-`
- Format: `lessons-<topic>.md`
- Edit document if new lessons learned on same topic
- GitHub manages history, documents reflect latest information

#### Location

- Project-wide: `kb/meta/`
- Module-specific: `<module>/kb/`

#### Examples

- `kb/meta/lessons-typedb-performance.md` (project-wide)
- `kb/meta/lessons-query-optimization.md` (project-wide)
- `web-ui/kb/lessons-reasonml-interop.md` (module-specific)

#### Notes

- Different from retrospectives (which are process-focused)
- Update existing file rather than create new one for same topic
- If topic grows large, consider splitting into more specific topics or promoting to best practices, ADRs, or guides

---

### Technical Debt

**Purpose:** Document technical debt items with context and rationale (reflection on what we built).

#### Naming Convention

- Prefix: `tech-debt-`
- Format: `tech-debt-<topic>.md`
- Self-describing prefix for clarity
- Edit document to update status or add details

#### Location

- Project-wide: `kb/meta/`
- Module-specific: `<module>/kb/`

#### Examples

- `kb/meta/tech-debt-test-coverage.md` (project-wide)
- `kb/meta/tech-debt-error-handling.md` (project-wide)
- `api-server/kb/tech-debt-authentication-refactor.md` (module-specific)

#### Notes

- Should be linkable from code comments
- TODOs in code should reference relevant tech debt docs when they exist (TODOs don't require a doc, but significant debt should be documented)
- Document should include a status (`open`, `in-progress`, or `done`) and a `Tracking Issue:` value (`none` is a valid value — it marks the debt as findable for later triage)
- When resolved, set status to `done` and move the document to the feature branch directory that resolved it; location is authoritative, so a document still in `kb/meta/` or `<module>/kb/` is unresolved whatever its status says, and an absent status is inferred from location
- Tech debt docs are temporary - resolved debt becomes part of feature documentation
- Consider converting to `idea-` if debt resolution suggests new enhancement opportunities

---

### Ideas

**Purpose:** Capture exploratory ideas and thinking about future direction.

#### Naming Convention

- Prefix: `idea-`
- Format: `idea-<topic>.md`
- Self-describing prefix for clarity

#### Location

- Project-wide: `kb/meta/`
- Module-specific: `<module>/kb/`

#### Examples

- `kb/meta/idea-graphql-api.md` (project-wide)
- `kb/meta/idea-plugin-system.md` (project-wide)
- `web-ui/kb/idea-dark-mode.md` (module-specific)

#### Notes

- Different from tech debt (ideas are speculative, debt is known issues)
- May evolve into feature proposals or ADRs if pursued
- Can include pros/cons, initial thoughts, references

---

### Templates

**Purpose:** Provide starting points for document creation.

#### Naming Convention

- Prefix: `template-`
- Format: `template-<document-type>.md`
- Document type can be: prefixes (adr, best-practices, lessons, tech-debt, idea), LEAP feature doc names (goals, plan, completion-summary, pr-description), or other document types
- Use singular form
- Use hyphen separators

#### Location

- All templates in `kb/meta/`

#### Examples

- `kb/meta/template-adr.md`
- `kb/meta/template-goals.md`
- `kb/meta/template-plan.md`
- `kb/meta/template-completion-summary.md`
- `kb/meta/template-pr-description.md`
- `kb/meta/template-best-practices.md`
- `kb/meta/template-lessons.md`
- `kb/meta/template-tech-debt.md`
- `kb/meta/template-idea.md`

---

### LEAP Methodology Documentation

**Purpose:** Documentation about LEAP methodology, process, and guidelines.

#### Naming Convention

- Prefix: `leap-` (Note: Omitted in the core `leap` repository itself, where the entire repository is dedicated to LEAP)
- Format: `leap-<topic>.md`
- Descriptive names with hyphens

#### Location

- `kb/meta/`

#### Examples

- `kb/meta/guide-document-taxonomy.md` (this document)
- `kb/meta/leap-best-practices.md`
- `kb/meta/guide-improvement-proposals.md`
- `kb/meta/leap-compliance-cheatsheet.md` (future)

---

### Usage and Implementation Guides

**Purpose:** Documentation of the actual system - how to use features (usage) and how they work internally (implementation).

#### Naming Convention

- Prefix: `guide-` for usage docs, `impl-` for implementation docs
- Format: `guide-<topic>.md` or `impl-<topic>.md`

#### Location

- `kb/` or `<module>/kb/` (system documentation, not meta)

#### Examples

- `kb/guide-kg-repository-usage.md`
- `kb/impl-query-builder-architecture.md`
- `api-server/kb/guide-api-endpoints.md`
- `api-server/kb/impl-database-connection-pooling.md`

---

### User Guides and README Files

**Purpose:** Documentation for end users, developers, and test resources.

#### The !ReadMe Pattern

The project uses `!ReadMe` (with exclamation prefix) as the standard pattern for readme files. The `!` prefix ensures readme files sort to the top of directory listings, making them immediately discoverable.

#### Naming Convention

##### Module root (with tool/category context)

- **Primary documentation**: `!ReadMe.<tool-name>.md`
- **Categorized documentation**: `!ReadMe.<category>.<tool-name>.md`
- **Rare exception**: `README.md` (only when GitHub auto-display is specifically valuable)

##### Subdirectories (context from directory name)

- **Default**: `!ReadMe.md` (directory name provides context)
- Examples: `src/jvmTest/resources/dependency-analyzer-tests/!ReadMe.md`

#### Why Tool/Category Decorations?

The decorations between `!ReadMe` and `.md` serve important purposes:

1. **Search discoverability**: `rg "!ReadMe.*kg-tools"` finds relevant docs immediately
2. **Agent navigation**: Agents can identify relevant files before reading content
3. **Multi-tool modules**: Distinguishes multiple tools/guides in same directory

#### When to Use README.md

`README.md` should be used **rarely** and only when GitHub auto-display provides specific value. Document the rationale when choosing `README.md`:

- **External contributor onboarding** - GitHub is the entry point for new contributors
- **Frequently shared via GitHub links** - Direct linking to GitHub web interface is common
- **Repository root** - Project-level overview for GitHub visitors
- **Standalone library** - Module intended for external consumption via GitHub

**Default assumption**: Use `!ReadMe.<tool-name>.md` unless you can articulate why GitHub auto-display matters for your specific use case.

#### Module Root Documentation

**Primary documentation** (`!ReadMe.<tool-name>.md`):

- Comprehensive reference for using the tool
- Tool name decoration aids search and agent navigation
- Examples:
  - `kg-tools-cli/!ReadMe.kg-tools.md`
  - `cobol-tools-cli/!ReadMe.cobol-tools.md`
  - `check-md/!ReadMe.check-md.md`

**Categorized documentation** (`!ReadMe.<category>.<tool-name>.md`):

- Focused guides for specific scenarios, workflows, or getting started
- Breaks large documentation into logical, maintainable chunks
- Tool name decoration maintains search discoverability
- Examples:
  - `cobol-tools-cli/!ReadMe.quickstart.cobol-tools.md`
  - `kg-tools-cli/!ReadMe.demo-repl.kg-tools.md`
  - `cobol-tools-cli/!ReadMe.workflow-classification.cobol-tools.md`

#### Subdirectory Documentation

**Test resource directories** (`!ReadMe.md`):

- No tool decoration needed (directory name provides context)
- Documents test case format, structure, and usage
- Examples:
  - `src/jvmTest/resources/dependency-analyzer-tests/!ReadMe.md`
  - `src/jvmTest/resources/tql-parser-tests/!ReadMe.md`

##### Content should include

- Test case file format and structure
- Schema references (if applicable)
- How to add new test cases
- What the tests cover
- Examples

#### Standard Categories

- **`quickstart`** - Getting started quickly with a tool
  - Example: `!ReadMe.quickstart.cobol-tools.md`
  - Purpose: Step-by-step tutorial for new users (typically < 10 steps)
  - Can double as integration test specification via markdown-driven test framework

- **`demo`** or **`demo-<topic>`** - Demonstrating the tool or a feature
  - Example: `!ReadMe.demo.kg-tools.md`
  - Example: `!ReadMe.demo-repl.kg-tools.md` (topic-specific)
  - Purpose: Show capabilities, feature demonstrations
  - Can include executable examples for validation

- **`workflow`** or **`workflow-<topic>`** - Documenting a standard workflow
  - Example: `!ReadMe.workflow.cobol-tools.md`
  - Example: `!ReadMe.workflow-classification.cobol-tools.md` (topic-specific)
  - Purpose: End-to-end workflows, common use cases
  - Can include multiple scenarios and decision points

#### Custom Categories

Developers can create custom categories as needed. Use descriptive, lowercase category names with optional topic suffix (`<category>-<topic>`).

---

### Benchmark Data

**Purpose:** Document performance benchmarks and measurement data for the system.

#### Naming Convention

- Prefix: `benchmark-`
- Format: `benchmark-<topic>.md`
- **Dating:** Benchmark documents can be either dated or undated depending on use case:
  - **Dated** (`benchmark-<topic>-YYYY-MM-DD.md`): When benchmark represents point-in-time measurement tied to specific code version
  - **Undated** (`benchmark-<topic>.md`): When benchmark document is maintained as living reference, updated with latest measurements
- Self-describing prefix for clarity

#### Location

- Project-wide: `kb/meta/`
- Module-specific: `<module>/kb/`

#### Examples

- `kb/meta/benchmark-query-performance-2025-12-15.md` (dated: specific measurement)
- `kb/meta/benchmark-typedb-scaling.md` (undated: living reference)
- `api-server/kb/benchmark-api-throughput.md` (module-specific)

#### Notes

- Includes performance measurements, test methodology, hardware/configuration details
- May reference code commits or versions
- Can include charts, tables, comparative data
- Dated benchmarks provide historical record; undated benchmarks track current performance

#### Markdown-Driven Test Framework

The markdown-driven test framework can validate commands in ANY markdown document (not just quickstarts). This allows:

- Executable documentation that stays accurate
- Living documentation tested in CI/CD
- Clear examples with verified output

Any `!ReadMe` file with executable command examples can be validated automatically.

---

## Standard Prefixes

All documents use prefix-first naming for consistent sorting and categorization.

### Prefixes for Meta-Documentation (about our work/process)

Meta-documentation is about our work, process, learning, and reflection.

#### Project-wide only (`kb/meta` only)

- **`leap-`** - LEAP methodology and process documentation
  - Example: `kb/meta/guide-document-taxonomy.md` (this document)
  - Example: `kb/meta/leap-best-practices.md`
  - Example: `kb/meta/leap-compliance-cheatsheet.md`

- **`template-`** - Document templates
  - Example: `kb/meta/template-adr.md`
  - Example: `kb/meta/template-goals.md`
  - Example: `kb/meta/template-plan.md`

#### Project-wide or module-specific (`kb/meta` or `<module>/kb`)

- **`best-practices-`** - How we work and develop
  - Example: `kb/meta/best-practices-kotlin-coding.md` (project-wide)
  - Example: `api-server/kb/best-practices-api-design.md` (module-specific)

- **`lessons-`** - What we learned about our development
  - Example: `kb/meta/lessons-typedb-performance.md` (project-wide)
  - Example: `web-ui/kb/lessons-reasonml-interop.md` (module-specific)

- **`tech-debt-`** - Reflection on what we built (temporary; location is authoritative, so moving the document to the feature branch directory that resolved it is what marks it resolved)
  - Example: `kb/meta/tech-debt-test-coverage.md` (project-wide)
  - Example: `api-server/kb/tech-debt-authentication-refactor.md` (module-specific)

- **`idea-`** - Ideas about future direction
  - Example: `kb/meta/idea-graphql-api.md` (project-wide)
  - Example: `web-ui/kb/idea-dark-mode.md` (module-specific)

- **`dev-note-`** - Temporary developer notes (NEVER COMMITTED)
  - Example: `dev-note-debugging-session.md` (local only, in .gitignore)
  - Example: `dev-note-performance-investigation.md` (local only, in .gitignore)
  - Purpose: Scratch notes, debugging logs, temporary analysis
  - Location: Anywhere in project (always gitignored)
  - These are ephemeral working documents that should never be committed
  - When insights are valuable, migrate content to appropriate permanent document type

### Prefixes for System Documentation (about the product/code)

System documentation is about the actual product/code.

#### Project-wide or module-specific (`kb` or `<module>/kb`)

- **`guide-`** - How to use features and patterns (usage documentation)
  - Example: `kb/guide-cli-framework.md` (project-wide)
  - Example: `api-server/kb/guide-api-endpoints.md` (module-specific)

- **`impl-`** - How the system works internally (implementation documentation)
  - Example: `kb/impl-query-builder-architecture.md` (project-wide)
  - Example: `api-server/kb/impl-database-connection-pooling.md` (module-specific)

### Custom Prefixes

Custom prefixes are permitted when content doesn't fit standard categories:

- Must be lowercase with hyphen separator
- Should be semantically meaningful
- Use consistently if creating multiple docs in same category
- Becomes "standard" if used frequently

Examples of potential custom prefixes:

- `troubleshooting-` for diagnostic guides
- `reference-` for reference documentation
- `tutorial-` for step-by-step tutorials

## Naming Convention Principles

### General Rules

1. **Prefix comes first** for consistent sorting within categories (exception: !ReadMe and README files use special naming patterns)
2. **Use lowercase** with hyphens as word separators (exception: !ReadMe and README files use mixed case)
3. **Be descriptive** but concise
4. **Use consistent patterns** within document types
5. **Avoid dates in names** unless chronological ordering is primary purpose
6. **Use double underscore `__`** only for ADRs (ontology convention)

### When to Use Numbers

- **ADRs**: Always numbered (chronological, permanent)
- **Feature branches**: Never numbered (use descriptive names)
- **Best practices**: No numbering (use descriptive topics)
- **Lessons learned**: No numbering (use descriptive topics)
- **Tech debt**: No numbering (use descriptive topics)
- **Ideas**: No numbering (use descriptive topics)

### Identifier vs Description

For ADRs:

- **Identifier** (before `__`): Used for references, must be unique
- **Description** (after `__`): For keyword discovery, not required in references
- Example: Reference as "ADR adr-010" but file is `adr-010__adr-numbering-policy.md`

---

## Summary of Document Naming Conventions

### By Location

#### `kb/adr/` and `<module>/kb/adr/` (Architecture Decision Records)

- `adr-NNN__description.md` (top-level)
- `<module>-adr-NNN__description.md` (module-specific)
- Uses numbered format with `__` separator

#### `kb/feature/<username>/<feature-name>/` (LEAP Feature Docs)

- `goals.md`, `plan.md`, `phase-N.md` (or `phase-N.M-<topic>.md` for complex phases), `completion-summary.md`, `pr-description.md`
- Uses fixed names (no prefixes)
- Phase documents can use hierarchical sections OR separate files with topic suffixes
- Other supporting documents as needed

#### `kb/meta/` (Meta-Documentation - about our work/process)

- `leap-<topic>.md` - LEAP methodology (project-wide only)
- `template-<type>.md` - Document templates (project-wide only)
- `best-practices-<topic>.md` - How we work/develop (project-wide or can be in `<module>/kb/`)
- `lessons-<topic>.md` - What we learned (project-wide or can be in `<module>/kb/`)
- `tech-debt-<topic>.md` - Reflection on what we built (temporary) (project-wide or can be in `<module>/kb/`)
- `idea-<topic>.md` - Ideas about future direction (project-wide or can be in `<module>/kb/`)
- `benchmark-<topic>.md` or `benchmark-<topic>-YYYY-MM-DD.md` - Performance measurements (project-wide or can be in `<module>/kb/`)
- `dev-note-<topic>.md` - Temporary developer notes (NEVER COMMITTED, always in .gitignore)

#### `kb/` or `<module>/kb/` (System Documentation - about the product/code)

- `guide-<topic>.md` - How to use features/patterns
- `impl-<topic>.md` - How the system works internally

#### Module root (!ReadMe files)

- `!ReadMe.<tool-name>.md` - Primary documentation (comprehensive user guide)
- `!ReadMe.<category>.<tool-name>.md` - Categorized documentation (focused guides)
- `README.md` - **Rare exception** (only when GitHub auto-display provides specific value, document rationale)

#### Test resource directories

- `!ReadMe.md` - Test case format and usage documentation
- No tool decoration (directory name provides context)
- Examples: `src/jvmTest/resources/dependency-analyzer-tests/!ReadMe.md`

#### Standard Categories for Categorized Guides

- **`quickstart`** - Getting started quickly (< 10 steps, doubles as test specification)
- **`demo`** or **`demo-<topic>`** - Demonstrating tool capabilities or features
- **`workflow`** or **`workflow-<topic>`** - End-to-end workflows and common use cases
- **Custom categories** - Developers can create additional categories as needed

#### Why !ReadMe Pattern

- `!` prefix sorts to top of directory listings
- Tool/category decorations aid search discoverability and agent navigation
- Consistent pattern across all readme files

#### When to Use README.md

Only when GitHub auto-display provides specific value:

- External contributor onboarding (GitHub is entry point)
- Frequently shared via GitHub links
- Repository root (project-level overview)
- Standalone library for external consumption

**Default**: Use `!ReadMe.<tool-name>.md` unless you can articulate why GitHub auto-display matters.

#### Custom prefixes permitted when needed
