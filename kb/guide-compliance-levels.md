# LEAP Compliance Levels

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2025-11-07

---

## Overview

This document defines the three LEAP compliance levels and their requirements. Use this to understand what practices are required at each level and to choose the right compliance level for your project.

### LEAP compliance levels support incremental adoption

- **Level 1: Essential** - Minimum viable LEAP practices
- **Level 2: Standard** - Recommended for most projects
- **Level 3: Comprehensive** - Full LEAP methodology adoption

#### Choose your level based on

- Project maturity and complexity
- Team size and experience
- Documentation needs
- Quality and maintainability goals

---

## Quick Reference Table

| Practice                             | Level 1 | Level 2                   | Level 3 |
|--------------------------------------|---------|---------------------------|---------|
| **Feature Branch Documentation**     | |                           | |
| `goals.md` before coding             | ✅ Required | ✅ Required                | ✅ Required |
| `plan.md` (multi-phase features)     | ✅ Required | ✅ Required                | ✅ Required |
| `completion-summary.md` before merge | ✅ Required | ✅ Required                | ✅ Required |
| Quick Summary in goals.md            | |                           | ✅ Required |
| Phase documents (phase-N.md)         | |                           | ✅ Required |
| Risk/complexity assessment           | | ✅ Required                | ✅ Required |
| **Test Coverage**                    | |                           | |
| Minimum coverage                     | 50% or project min | 80%+ target               | 90%+ target |
| Coverage metrics                     | Line, instruction, branch | Line, instruction, branch | Line, instruction, branch |
| **Code Documentation**               | |                           | |
| Public API docs                      | ✅ Required | ✅ Required                | ✅ Required |
| All top-level constructs             | | ✅ Required                | ✅ Required |
| All public methods                   | | ✅ If not self-evident     | ✅ If not self-evident |
| Comprehensive inline comments        | |                           | ✅ Required |
| Named code blocks                    | | Recommended*              | Required* |
| **Usage & Implementation Docs**      | |                           | |
| Guide docs for major features        | | ✅ Required                | ✅ Required |
| Impl docs for non-self-evident code  | | ✅ Required                | ✅ Required |
| **Code Documentation Publishing**    | |                           | |
| Local doc generation capability      | | ✅ Required*               | ✅ Required* |
| CI publishes docs automatically      | |                           | ✅ Required* |
| **Architecture & Design**            | |                           | |
| ADRs for significant decisions       | | ✅ Required                | ✅ Required |
| Tech debt documentation              | | ✅ Required                | ✅ Required |
| **Process**                          | |                           | |
| Feature branch workflow              | ✅ Required | ✅ Required                | ✅ Required |
| LEAP terminology (internal)          | |                           | ✅ Consistent use |
| **Markdown Quality**                 | |                           | |
| Markdown best practices              | | ✅ Required                | ✅ Required |

### Notes

- **\* Named code blocks:** For complex/critical code (performance-critical, workarounds, hacks, tech debt, complex algorithms). See [guide-named-code-blocks.md](guide-named-code-blocks.md).
- **\* Code Documentation Publishing:** Required for projects with code artifacts. Projects without code (e.g., marketing sites, documentation-only projects) may declare exemption in `leap-settings.md`.

---

## Level 1: Essential

**Target audience:** Teams starting with LEAP, proof-of-concept projects, experimental features

### Required Practices

#### Feature Branch Documentation

- **goals.md** must be created before writing code
  - See: [Feature Branch Documentation](guide-methodology.md#feature-branch-documentation)
- **plan.md** required for features with multiple implementation phases
  - See: [plan.md template](template-plan.md)
- **completion-summary.md** required before merge/PR creation
  - See: [completion-summary.md template](template-completion-summary.md)

#### Test Coverage

- **Minimum: At least 50% across all metrics** (line, instruction, branch)
- **Projects may define higher minimums** in:
  - `kb/leap-settings.md` (preferred for documentation)
  - Build files: `gradle.kts` (Gradle) or `pom.xml` (Maven)
- **Apply whichever is higher**: 50% baseline or project-defined minimum
- See: [LEAP Settings Template](template-leap-settings.md)

#### Code Documentation

- **Structured API documentation** for all public APIs
  - KDoc for Kotlin, JSDoc for JavaScript/ReasonML, etc.
  - See: [Source Code Comments Best Practices](guide-methodology.md#source-code-comments-best-practices)

#### Git Workflow

- **Feature branch workflow** with descriptive branch names
  - Pattern: `<username>/<feature-name>`
  - See: [LEAP Development Workflow](guide-methodology.md#leap-development-workflow)

---

## Level 2: Standard

**Target audience:** Production projects, established codebases, teams comfortable with LEAP

### Includes all Level 1 requirements, plus

### Additional Required Practices

#### Risk and Complexity Assessment

- **Document risk and complexity** in goals.md or plan.md
  - Use four-level scales: LOW, MEDIUM, HIGH, VERY HIGH
  - See: [Risk and Complexity Assessment](guide-methodology.md#risk-and-complexity-assessment)

#### Test Coverage

- **Target: 90%+ coverage** across all metrics
  - Exceptions documented with rationale
  - See: [Testing Requirements in goals.md](guide-methodology.md#feature-documents)

#### Comprehensive Code Documentation

- **KDocs for all top-level constructs**: classes, interfaces, objects, functions
- **KDocs for all public methods** (unless self-evident)
  - See: [Source Code Comments Best Practices](guide-methodology.md#source-code-comments-best-practices)

#### Usage and Implementation Documentation

- **Guide documents** (`guide-*.md`) for all major features
  - How to use the feature, API, or component
  - See: [Implementation Documentation](guide-methodology.md#implementation-documentation)
- **Implementation docs** (`impl-*.md`) for non-self-evident implementations
  - Complex algorithms, architectures, design patterns
  - Non-obvious implementation choices
  - Required when code comments alone are insufficient
  - See: [Implementation Documentation](guide-methodology.md#implementation-documentation)

#### Code Documentation Publishing

- #### Ability to generate documentation site locally
  - Developers can run a command to generate browsable HTML documentation
  - Build configuration exists for documentation generation (e.g., Dokka, Javadoc, JSDoc)
  - Project README explains: how to generate, where docs are located, how to view
  - Exemption: Projects without code artifacts may declare exemption in `leap-settings.md`

#### Recommended for Kotlin projects

- Use Dokka: `./gradlew dokkaHtml`
- Output location: `build/dokka/html/`
- README includes generation instructions

#### Named Code Blocks

- #### Recommended for complex and critical code
  - Performance-critical code sections
  - Workarounds or temporary solutions
  - Known hacks requiring future attention
  - Tech debt implementations
  - Complex algorithms documented in `kb/`
- **Benefits**: Precise code references, stable through refactoring, AI targeting
  - See: [Named Code Blocks Standard](guide-named-code-blocks.md)

#### Architecture and Design

- #### ADRs for significant architectural decisions
  - See: [Architecture Decision Records](guide-methodology.md#architecture-decision-records-adrs)
  - Template: [template-adr.md](template-adr.md)
- **Tech debt documented** when discovered
  - See: [Tech Debt Management](guide-methodology.md#tech-debt-management)
  - Template: [template-tech-debt.md](template-tech-debt.md)

#### Markdown Quality

- #### Follow markdown formatting standards
  - Use semantic headings for structure (not bold text)
  - Separate block elements with blank lines
  - Use `<br>` tags for consecutive metadata lines
  - Handle nested code blocks correctly
  - See: [Best Practices: Markdown Formatting](best-practices-markdown.md)
  - Enforcement: [ADR leap-adr-002](adr/leap-adr-002__markdown-formatting-standards.md)
- **Run check-md before committing** markdown files
  - Auto-fix violations: `check-md <file> --fix`
  - Check staged files: `check-md --staged`
  - See: [Best Practices: Markdown Quality Checks](best-practices-markdown.md)
  - Tool: [check-md README](../check-md/README.md)

---

## Level 3: Comprehensive

**Target audience:** Critical systems, highly complex projects, teams deeply invested in LEAP

### Includes all Level 2 requirements, plus

### Additional Required Practices

#### Enhanced Feature Documentation

- **Quick Summary** in all goals.md documents
  - 2-3 sentences at top of goals.md for quick orientation
  - See: [PROP-001](guide-improvement-proposals.md#prop-001-quick-summary-section-in-goalsmd)
- **Phase documents** (phase-N.md) for complex multi-phase features
  - Detailed documentation for each implementation phase
  - Template: [template-phase.md](template-phase.md)

#### Comprehensive Code Comments

- **Inline comments** for all complex logic and non-obvious decisions
- **Why-focused comments** explaining rationale, not just what
  - See: [Inline Comments](guide-methodology.md#inline-comments)

#### Automated Documentation Publishing

- #### CI automatically publishes documentation
  - Documentation published when PRs are merged
  - Hosted on internal server accessible to all staff
  - Automated refresh ensures docs stay current with code
  - Project README provides URL to published docs
  - Exemption: Projects without code artifacts may declare exemption in `leap-settings.md`

#### Named Code Blocks

- #### Required for complex and critical code
  - All performance-critical code sections
  - All workarounds or temporary solutions
  - All known hacks requiring future attention
  - All tech debt implementations
  - Complex algorithms with `kb/` implementation documentation
- **Block names must be project-wide unique** (verify with git grep)
  - See: [Named Code Blocks Standard](guide-named-code-blocks.md)

#### Consistent LEAP Terminology

- **LEAP terminology** used consistently in all internal documentation
  - Feature docs, ADRs, code comments, team discussions
  - See: [LEAP Terminology Usage](guide-methodology.md#leap-terminology-usage)

---

## Choosing Your Compliance Level

### Start with Level 1 if:

- You're new to LEAP methodology
- Project is in early/experimental stage
- Team is small or learning the practices
- Documentation overhead needs to be minimal

### Adopt Level 2 when:

- Project is moving to production
- Team is comfortable with Level 1 practices
- Code quality and maintainability are priorities
- You need comprehensive documentation for onboarding

### Pursue Level 3 when:

- System is business-critical or high-complexity
- Team is experienced with LEAP practices
- Maximum documentation and quality are required
- Long-term maintainability is essential

---

## Progressive Adoption

You can adopt LEAP incrementally:

1. **Start at Level 1** for all new features
2. **Gradually increase** practices as team becomes comfortable
3. **Move to Level 2** when ready for higher standards
4. **Adopt Level 3** practices for critical components first

**Remember:** Even Level 1 compliance provides significant value. Don't let perfect be the enemy of good.

---

## Compliance Verification

### Self-Assessment Questions

#### Level 1

- [ ] Do all features have goals.md created before coding?
- [ ] Do multi-phase features have plan.md?
- [ ] Do all merged features have completion-summary.md?
- [ ] Does test coverage meet at least 50% across all metrics (line, instruction, branch) or higher project minimums (defined in leap-settings.md, gradle.kts, or pom.xml)?
- [ ] Do all public APIs have structured documentation?

#### Level 2

- [ ] All Level 1 practices followed?
- [ ] Is risk/complexity documented when higher than LOW?
- [ ] Is test coverage at 90%+ (or exceptions documented)?
- [ ] Do all top-level constructs have KDocs?
- [ ] Are all public methods documented (unless self-evident)?
- [ ] Do all major features have guide documents (guide-*.md)?
- [ ] Are non-self-evident implementations documented (impl-*.md)?
- [ ] Can developers generate documentation locally (if project has code)?
- [ ] Does project README explain how to generate and view docs?
- [ ] Are named code blocks used for complex/critical code?
- [ ] Are ADRs created for architectural decisions?
- [ ] Is tech debt documented when discovered?
- [ ] Do markdown files follow formatting standards (semantic headings, block separation, etc.)?
- [ ] Does check-md pass without violations on all markdown files?

#### Level 3

- [ ] All Level 2 practices followed?
- [ ] Do all goals.md have Quick Summary?
- [ ] Do complex features have phase documents?
- [ ] Is complex logic thoroughly commented?
- [ ] Are named code blocks required for all complex/critical code?
- [ ] Does CI automatically publish documentation (if project has code)?
- [ ] Does README provide URL to published docs?
- [ ] Is LEAP terminology used consistently?

---

## Project Configuration

To configure your project's LEAP compliance level and requirements:

1. Create `kb/leap-settings.md` from [template](template-leap-settings.md)
2. Document your target compliance level
3. Specify test coverage thresholds (if above 50%)
4. Document any project-specific LEAP conventions

---

## Additional Resources

- **Full Methodology**: [guide-methodology.md](guide-methodology.md)
- **Templates**: All templates in `kb/template-*.md`
- **Document Taxonomy**: [guide-document-taxonomy.md](guide-document-taxonomy.md)
- **Improvement Proposals**: [guide-improvement-proposals.md](guide-improvement-proposals.md)

---

**Questions or feedback?** LEAP is a living methodology. Propose improvements via [LEAP Improvement Proposals](guide-improvement-proposals.md).
