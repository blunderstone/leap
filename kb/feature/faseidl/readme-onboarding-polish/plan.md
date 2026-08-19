# README and Onboarding Polish Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-19

---

## Overview

This plan outlines the steps to streamline the LEAP onboarding experience by simplifying the primary `README.md` and introducing a dedicated, comprehensive installation guide. We will also perform a surgical update of the repository remote URLs from `faseidl/leap` to `blunderstone/leap`.

**Development Approach**: Follow the LEAP methodology—applying incremental updates, validating the markdown files with the `check-md` linter at each stage, and verifying all documentation hyperlinks are valid.

### Overall Assessment

- **Complexity:** LOW - Purely documentation restructuring and URL updates.
- **Risk:** LOW - No impact on production code, tooling execution, or system behaviors.

---

## Phase 1: Advanced Installation Guide & URL Renaming

### Goals

- Create a fully-compliant `kb/guide-installation.md` capturing all manual setup paths, prerequisites, Windows considerations, and linter/QMD instructions.
- Update the Git submodule and repository URLs in `README.md` and related files to point to `blunderstone/leap` instead of `faseidl/leap`.

### Approach

- Build a highly readable `kb/guide-installation.md` following standard templates and complying fully with the five formatting rules of `check-md`.
- Replace the remote repository URLs in `README.md` to use the new `blunderstone/leap` namespace.

### Testing

- Run the `check-md` linter on `kb/guide-installation.md` to verify zero violations.
- Verify that the URLs point to the correct future repository structure.

### Success Criteria

- [ ] `kb/guide-installation.md` is complete and has zero formatting violations.
- [ ] All remote repository references in `README.md` are updated to `blunderstone/leap`.

### Explicitly Deferred

- None.

**Rationale:** Establishing the comprehensive guide and the correct repository coordinates first ensures the foundational resources are ready and correct before we simplify the main README.

---

## Phase 2: README Simplification & Validation

### Goals

- Simplify the `README.md` "Getting Started" section to offer Path A (Git Submodule) and Path B (Copy/Embed) with direct, single-command copy-pastes, removing inline commentary.
- Link cleanly to the new `kb/guide-installation.md` for advanced options.
- Ensure the entire repository's markdown files pass the `check-md` linter without errors.

### Approach

- Re-write the "Getting Started" section of the root `README.md` to prioritize instant copy-paste setup paths.
- Add clear links referencing `kb/guide-installation.md` for Windows troubleshooting, manual setups, and custom virtual environments.
- Run a project-wide `check-md` to ensure total compliance.

### Testing

- Run `check-md kb/` and `check-md README.md` to guarantee perfect adherence.
- Manually check every link introduced or modified in both files.

### Success Criteria

- [ ] `README.md` "Getting Started" section is simplified, clear, and direct.
- [ ] All links between `README.md` and `kb/guide-installation.md` work perfectly.
- [ ] `check-md kb/` passes with 100% compliance.

### Explicitly Deferred

- None.

**Rationale:** Polishing the README last allows us to ensure all references, anchors, and file links point to validated, lint-free targets.

---

## Decision Points

### After Phase 1

- Proceed to Phase 2 once the installation guide is written, reviewed, and passes markdown linting.

---

## Notes

- The target repository URL is `https://github.com/blunderstone/leap.git` (or the equivalent SSH path `git@github.com:blunderstone/leap.git`).
