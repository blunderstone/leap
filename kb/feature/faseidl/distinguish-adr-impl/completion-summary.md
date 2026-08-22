# Distinguish ADRs from Implementation Documents Completion Summary

**Branch:** `feature/faseidl/distinguish-adr-impl`<br>
**Base Branch:** `main`<br>
**Date:** 2026-08-22<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

---

## Overview

We have successfully resolved GitHub Issue #14 by defining and integrating strict standard guidelines to distinguish Architecture Decision Records (ADRs) from descriptive implementation documents in the LEAP methodology. 

By defining a canonical four-question test, introducing the splitting and maintenance rules, refining the template to remove execution tracking, and establishing non-destructive remediation pathways, we have addressed the common practical failure mode where immutable historical records (ADRs) are combined with mutable codebase walkthroughs and end up rotting over time.

---

## What Changed

### High-Level Summary

- **Introduced the Decision Test**: Established a four-question test inside the Taxonomy Guide to help document authors determine if their content is a policy decision or a description of mechanism.
- **Formulated Splitting and Maintenance Rules**: Created strict rules specifying that complex decisions must be split into an ADR (immutable policy) and an implementation document (mutable description), and that accepted ADRs should only be edited to change status or record supersedence.
- **Refined the ADR Template**: Add a pre-write gate and list of disallowed sections to the template's writing tips, removed the mutable `Migration Checklist` task boxes, and clarified the `accepted` status meaning as "this is official policy".
- **Linked Cross-References**: Linked the high-level policy in `leap-adr-001` directly to the new canonical definition in the Taxonomy Guide, avoiding duplication.
- **Purged Obsolete Terminology Clarification**: Added explicit clarification notes in the Taxonomy Guide explaining that the `leap-` prefix is omitted in the core `leap` repository since the entire repository is dedicated to the methodology.

### Detailed Changes

#### Document Taxonomy (`kb/guide-document-taxonomy.md`)

- Inserted the new subsection `#### Choosing Between an ADR and an Implementation Document` after the ADR naming guidelines.
- Authored the 4-question test, the Consequences boundary, the Splitting Rule, the Maintenance Rule, and Remediation Guidance for legacy non-conforming ADRs.
- Clarified that the `leap-` prefix for methodology and best practices is omitted in the core `leap` repository itself.

#### ADR Template (`kb/template-adr.md`)

- Removed the `#### Migration Checklist` section and its task boxes, instructing authors to track execution in feature docs or issues.
- Added a **Pre-Write Gate** and **No Living/Implementation Content** guidelines to the Writing Tips.
- Clarified the `accepted` status to signify "this is established policy", removing the temptation to add custom completion-tracking fields.

#### ADR-001 Policy (`kb/adr/leap-adr-001__adr-numbering-and-naming-policy.md`)

- Added the `### Choosing and Remediation Guidance` section pointing via a relative markdown link to the new section in `kb/guide-document-taxonomy.md`.

#### Agent Instructions (`GEMINI.md`)

- Created a local, git-staged `GEMINI.md` file in the root workspace to help future AI coding agents know they can run `check-md` directly from any directory.

#### Private Memory (`~/.gemini/tmp/leap/memory/leap-open-source-todo.md`)

- Added a permanent task under Section 7 of the private preparation checklist to remind us to integrate direct agent instruction capabilities globally in the project setup scripts (`setup-leap.sh`) post-merge.

---

## Technical Decisions

### Splitting Over Living ADRs
Allowing implementation walkthroughs to live inside an ADR forces authors to edit accepted ADRs to match code changes, which directly violates the immutable nature of historical decision records. Splitting the document ensures the "policy" remains unchanged while the "mechanism" guide is updated as the codebase evolves.

---

## Testing

### Test Coverage

- **Markdown Compliance:** 100% of the modified and newly created markdown files pass the local `check-md` linter with zero violations.
- **Link Auditing:** All relative hyperlinks and section anchors have been verified as correct.
