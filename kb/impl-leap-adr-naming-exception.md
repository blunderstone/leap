# Implementation: LEAP ADR Naming Exception

**Author:** [David Landes]<br>
**Date:** 2026-02-04<br>
**Related:** [ADR leap-adr-001](kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md)

---

## Overview

This document explains why the LEAP repository intentionally deviates from its own ADR naming standard by treating its ADRs as module-scoped rather than top-level ADRs.

## Standard ADR Naming Convention

According to [ADR leap-adr-001](kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md), the LEAP methodology defines two ADR naming patterns:

- **Top-level/cross-cutting ADRs**: `adr-NNN__description.md`
- **Module-specific ADRs**: `<module>-adr-NNN__description.md`

The convention states that a repository's root-level ADRs should use the `adr-NNN__` pattern (no module prefix), while ADRs specific to modules within that repository should use the module prefix pattern.

## The LEAP Repository Exception

**Decision:** The LEAP repository uses `leap-adr-NNN__description.md` for its ADRs instead of `adr-NNN__description.md`.

This means LEAP treats its own ADRs as if they were module-scoped, even though LEAP is the repository root.

## Rationale

### LEAP as a Submodule

The LEAP repository is designed to be included as a **Git submodule** in other projects. When LEAP is incorporated into a parent project, it functions as a module within that project's structure, not as the top level.

Consider this structure:

```
my-project/
├── kb/adr/
│   ├── adr-001__database-choice.md              # Parent project's top-level ADR
│   └── adr-002__authentication-strategy.md      # Parent project's top-level ADR
└── leap/                                         # LEAP as a submodule
    └── kb/adr/
        ├── leap-adr-001__methodology-core.md    # LEAP module's ADR
        └── leap-adr-002__compliance-levels.md   # LEAP module's ADR
```

### Naming Collision Prevention

If LEAP used the standard `adr-NNN__` pattern for its ADRs, including LEAP as a submodule would create naming conflicts:

```
my-project/
├── kb/adr/
│   ├── adr-001__database-choice.md              # Collision!
│   └── adr-002__authentication-strategy.md      # Collision!
└── leap/
    └── kb/adr/
        ├── adr-001__methodology-core.md         # Collision!
        └── adr-002__compliance-levels.md        # Collision!
```

References like "ADR adr-001" would be ambiguous—which `adr-001` is being referenced?

### Consistent Identity Across Contexts

By using `leap-adr-NNN__`, LEAP's ADRs maintain consistent, unambiguous identifiers regardless of whether:

- LEAP is used as a standalone repository
- LEAP is included as a Git submodule
- LEAP ADRs are referenced from external projects

A reference to "ADR leap-adr-001" is always unambiguous and always refers to the same LEAP methodology decision.

## Implications

### Breaking Our Own Rule

This decision **intentionally violates** the standard that top-level repository ADRs use the `adr-NNN__` pattern. The LEAP repository is effectively saying: "Even though I am a repository root, my ADRs should be treated as module-scoped."

### Self-Aware Exception

The LEAP methodology acknowledges that its ADR naming convention assumes a traditional repository structure where:

1. The repository represents a single project
2. The project has a top level and potentially multiple modules
3. ADRs at the top level govern the entire project

LEAP, however, is a **methodology repository** designed for reuse. Its primary use case is to be embedded in other projects. Therefore, treating its ADRs as module-scoped is the correct implementation of the spirit of the ADR naming policy, even if it breaks the letter of the rule.

### Documentation Clarity

All LEAP documentation references to its own ADRs should use the full `leap-adr-NNN` identifier:

✅ **Correct:**

- "See ADR leap-adr-001 for methodology foundations"
- "Reference leap-adr-002__compliance-levels.md"

❌ **Incorrect:**

- "See ADR adr-001" (Ambiguous when LEAP is a submodule)
- "See ADR 001" (No prefix makes scope unclear)

### Searchability

The `leap-adr-*` pattern enables clear searches:

```bash
# Find all LEAP ADRs (works whether standalone or submodule)
git grep "leap-adr-"

# Find all LEAP ADR references
git grep "leap-adr-[0-9]"

# No ambiguity with parent project's ADRs
```

## Comparison with Other Modules

Most modules in a repository **don't** need module-prefixed ADRs because:

1. They're part of a single project's repository
2. They won't be extracted or reused in other projects
3. Top-level ADRs can govern cross-cutting concerns

LEAP is different because:

1. It's designed for reuse across multiple projects
2. It will be included as a submodule
3. Its ADRs need globally unique, portable identifiers

## Summary

The LEAP repository treats its ADRs as module-scoped (`leap-adr-NNN__`) rather than top-level (`adr-NNN__`) to:

1. **Prevent naming conflicts** when LEAP is used as a submodule
2. **Maintain consistent identity** across different usage contexts
3. **Enable unambiguous references** from both internal and external documentation
4. **Align with LEAP's purpose** as a reusable methodology framework

This is an intentional and justified deviation from the standard ADR naming convention. The deviation itself demonstrates the LEAP principle of documenting implementation decisions with clear rationale—even when those decisions involve breaking our own rules.