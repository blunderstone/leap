# LEAP Cheatsheet

## Quick reference for experienced LEAP users

---

## Templates

**Location:** `kb/template-*.md`

| Document | Template |
|----------|----------|
| Feature goals | `template-goals.md` |
| Feature plan | `template-plan.md` |
| Phase document | `template-phase.md` |
| Completion summary | `template-completion-summary.md` |
| ADR | `template-adr.md` |
| Tech debt | `template-tech-debt.md` |
| Best practices | `template-best-practices.md` |
| Lessons learned | `template-lessons.md` |
| Ideas | `template-idea.md` |
| PR description | `template-pr-description.md` |
| LEAP settings | `template-leap-settings.md` |

---

## Branch Naming

**Pattern:** `<username>/<feature-name>`

**Example:** `faseidl/query-builder-refactor`

---

## Feature Documentation

### Location

- **Top-level:** `kb/feature/<username>/<feature-name>/`
- **Module-specific:** `<module>/kb/feature/<username>/<feature-name>/`

#### Required files

- `goals.md` (before coding)
- `plan.md` (multi-phase features)
- `completion-summary.md` (before merge)

#### Optional files

- `phase-1.md`, `phase-2.md`, etc. (complex features)

---

## Document Naming

| Type | Location | Pattern | Example |
|------|----------|---------|---------|
| ADRs (top-level) | `kb/adr/` | `adr-NNN__description.md` | `leap-adr-001__adr-numbering-policy.md` |
| ADRs (module) | `<module>/kb/adr/` | `<module>-adr-NNN__description.md` | `cobol-tools-cli-adr-001__single-cli.md` |
| Tech debt | `kb/meta/` or `<module>/kb/` | `tech-debt-<topic>.md` | `tech-debt-test-coverage.md` |
| Best practices | `kb/meta/` | `best-practices-<topic>.md` | `best-practices-kotlin-code.md` |
| Lessons learned | `kb/meta/` | `lessons-<topic>.md` | `lessons-typedb-migration.md` |
| Ideas | `kb/meta/` | `idea-<topic>.md` | `idea-graphql-api.md` |
| Usage guides | `kb/` or `<module>/kb/` | `guide-<topic>.md` | `guide-cli-framework.md` |
| Implementation docs | `kb/` or `<module>/kb/` | `impl-<topic>.md` | `impl-query-builder.md` |

---

## Compliance Levels

| Level | Key Requirements |
|-------|-----------------|
| **Level 1: Essential** | goals.md, plan.md, completion-summary.md, 50% coverage, public API docs |
| **Level 2: Standard** | Level 1 + risk/complexity assessment, 90% coverage, comprehensive docs, guide/impl docs, local doc generation, named blocks (recommended), ADRs, tech debt |
| **Level 3: Comprehensive** | Level 2 + Quick Summary, phase docs, comprehensive comments, named blocks (required), CI publishes docs, consistent terminology |

**Details:** See [guide-compliance-levels.md](guide-compliance-levels.md)

**Project settings:** `kb/leap-settings.md`

---

## Test Coverage

**Level 1 minimum:** 50% OR project-defined minimums (whichever higher)

**Level 2+ target:** 90%+ (line, instruction, branch)

**Check project settings:** `kb/leap-settings.md` or build files (gradle.kts, pom.xml)

---

## Risk and Complexity

**Four-level scales:** LOW, MEDIUM, HIGH, VERY HIGH

**Risk:** External uncertainty (dependencies, integrations, new tech)

**Complexity:** Technical difficulty (components affected, algorithms, architecture)

### Only mention when NOT LOW

---

## Feature Workflow Quick Steps

1. Create feature branch: `git checkout -b <username>/<feature-name>`
2. Create feature directory: `kb/feature/<username>/<feature-name>/`
3. Write `goals.md` (use template)
4. Write `plan.md` if multi-phase (use template)
5. Implement in phases
6. Write tests during implementation
7. Write `completion-summary.md` (use template)
8. Create PR (use template for description)
9. Merge after review

---

## Git Workflow

**Feature branches:** `<username>/<feature-name>`

### Commit format

```
<imperative-summary>

- Detailed change 1
- Detailed change 2

Implements Phase N of <username>/<feature-name>
```

**DO NOT include:** AI assistant references in commits

---

## Documentation Best Practices

**API docs:** Required for all public APIs, interfaces, top-level constructs

**Inline comments:** Why, not what; complex logic only

**Implementation docs:** Complex algorithms, architectures (in `kb/`)

**Tech debt:** Document when discovered, move to feature dir when resolved

---

## Common File Locations

```
kb/
├── adr/                     # Architecture Decision Records
├── feature/                 # Feature branch documentation
│   └── <username>/
│       └── <feature-name>/
│           ├── goals.md
│           ├── plan.md
│           ├── phase-N.md
│           └── completion-summary.md
├── best-practices-*.md      # Best practices documentation
├── guide-*.md               # LEAP methodology guides and usage docs
├── impl-*.md                # Implementation documentation
├── lessons-*.md             # Lessons learned
├── tech-debt-*.md           # Technical debt documentation
├── idea-*.md                # Ideas for future work
├── leap-*.md                # LEAP configuration (e.g., leap-settings.md)
└── template-*.md            # Document templates
```

---

## Need More Detail?

- **Full methodology:** [guide-methodology.md](guide-methodology.md)
- **Compliance levels:** [guide-compliance-levels.md](guide-compliance-levels.md)
- **Document taxonomy:** [guide-document-taxonomy.md](guide-document-taxonomy.md)
- **Named code blocks:** [guide-named-code-blocks.md](guide-named-code-blocks.md)
- **Improvement proposals:** [guide-improvement-proposals.md](guide-improvement-proposals.md)
