# Distinguish ADRs from Implementation Documents Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-22

---

## Quick Summary

Define and integrate standard guidelines into the LEAP methodology to clearly distinguish Architecture Decision Records (ADRs) from implementation and usage documentation. This eliminates the common failure mode of "mixed documents" and prevents immutable historical ADRs from rotting with stale codebase walkthroughs.

---

## Executive Summary

When adopting Architecture Decision Records (ADRs) in practice, teams often fall into the trap of writing implementation documents (how a component works, usage examples, walkthroughs) and styling them as ADRs. This is actively harmful: ADRs are immutable historical records, while implementation details must track the active state of the codebase. When they are combined, the implementation walkthroughs silently rot, degrading documentation quality and trust.

To resolve this structural conflation, this feature establishes clear tests and rules within the LEAP taxonomy, updates the ADR template to enforce these limits at the writing phase, and provides a clear remediation path for existing mixed documents without compromising permanent ADR serial numbering.

---

## Objectives

1. Define a 4-question "decision test" inside the LEAP taxonomy to help authors verify whether a document is a genuine architectural policy decision or a descriptive implementation guide.
2. Formulate a "splitting rule" and "maintenance rule" to keep architectural policy separate from implementation mechanism.
3. Establish remediation guidelines for managing legacy, non-conforming, or mixed ADRs in a project.
4. Update the ADR template to incorporate these gates, remove mutable task checklists, and clarify that the `accepted` status represents established policy.

---

## Requirements

### Functional Requirements

- **REQ-1**: Add a new subsection under the Architecture Decision Records section in `kb/guide-document-taxonomy.md` explaining how to choose between an ADR and an implementation document based on the four-question test.
- **REQ-2**: Document the splitting rule, the consequences section boundary, and the maintenance rule (accepted ADRs do not change except for status/supersedence) in `kb/guide-document-taxonomy.md`.
- **REQ-3**: Provide clear, non-destructive remediation guidelines for legacy ADRs in `kb/guide-document-taxonomy.md`.
- **REQ-4**: Add a pre-write gate to `kb/template-adr.md` in the writing tips, listing disallowed section titles (e.g., *Implementation Details*, *Usage*, etc.).
- **REQ-5**: Refactor `kb/template-adr.md` to remove the execution-tracking "Migration Checklist" and replace it with guidance on high-level strategy.
- **REQ-6**: Clarify the meaning of `accepted` status in `kb/template-adr.md` as "this is policy".
- **REQ-7**: Update the definition note in `kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md` to point to the canonical definitions in `kb/guide-document-taxonomy.md`.

### Non-Functional Requirements

- All modified and new Markdown files must conform to the 5 rules enforced by the `check-md` tool.
- Maintain consistent, high-signal, and professional architectural tone.

### Testing Requirements

- Verify all new and modified documents pass `check-md` with 0 violations.
- Verify all modified links correctly resolve.

### Documentation Requirements

- Document the new guidelines with clear, practical examples.

---

## Success Criteria

- [x] Goals for distinguishing ADRs from implementation guides drafted and approved.
- [x] Subsection "Choosing Between an ADR and an Implementation Document" added to `kb/guide-document-taxonomy.md`.
- [x] ADR Template (`kb/template-adr.md`) updated with pre-write gate and migration strategy adjustments.
- [x] ADR-001 pointer to the taxonomy guide added and verified.
- [x] All new/modified markdown files pass `check-md` with 0 violations.

---

## Constraints

- No tooling changes are required; these guidelines are enforced during review.
- All documents must remain purely compliant with vanilla Markdown.

---

## Assumptions

- Consuming projects will adopt these guidelines incrementally as part of their standard development process.

---

## Out of Scope

- Performing the actual remediation of legacy ADRs across external repositories.
