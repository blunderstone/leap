# README and Onboarding Polish Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-19

---

## Quick Summary

Streamline the onboarding experience for new LEAP adopters by simplifying installation instructions, moving advanced details to a dedicated guide, and updating the repository reference to `blunderstone/leap`.

---

## Executive Summary

The current `README.md` requires a developer to read through nested comments inside code blocks and manually choose installation paths. This creates cognitive load and friction for first-time adopters.

This feature will split the onboarding into a highly direct, copy-pasteable quick-start in the root `README.md` and a comprehensive `kb/guide-installation.md` for advanced users. It will also update the repository URLs to reflect the new repository name `blunderstone/leap`.

---

## Objectives

1. Simplify the root `README.md` "Getting Started" section to be instantly actionable with single-command copy-pastes.
2. Create a detailed `kb/guide-installation.md` containing all advanced parameters, manual setups, Windows troubleshooting, and verification steps.
3. Update all repository URL references in the onboarding docs from `faseidl/leap` to `blunderstone/leap`.

---

## Requirements

### Functional Requirements

- **REQ-1**: The root `README.md` must have two distinct, immediately copy-pasteable installation blocks (Submodule and Copy/Embed) without nested comments.
- **REQ-2**: All git repository submodule and clone URLs must use `blunderstone/leap` as the remote source.
- **REQ-3**: Detailed troubleshooting, environment-specific notes (Windows), manual virtualenv setups, and QMD configurations must be fully captured in `kb/guide-installation.md`.

### Non-Functional Requirements

- All Markdown documents must strictly conform to the five `check-md` rules.
- Ensure all hyperlinks between `README.md` and the new installation guide are robust and correct.

### Testing Requirements

- The new and modified markdown files must successfully pass `check-md` checks without any formatting violations.
- All newly introduced or modified hyperlinks must be manually or programmatically verified to prevent dead links.

### Documentation Requirements

- High-quality, clear, concise English with proper markdown styling.
- Comprehensive coverage of setup edge cases in the installation guide.

---

## Success Criteria

- [ ] `README.md` "Getting Started" section simplified to clear, single-command installation paths.
- [ ] All references to the repository path use `blunderstone/leap`.
- [ ] A comprehensive `kb/guide-installation.md` is fully documented and verified.
- [ ] `check-md kb/` passes without any violations.

---

## Constraints

- Must use only vanilla Markdown conforming to the linter's standards.

---

## Assumptions

- The repository will be hosted on GitHub under `blunderstone/leap`.

---

## Out of Scope

- Modifying the core functional logic of `setup-leap.sh` (this polish is focused on onboarding flow, although minor text/messaging changes in the script's final output to match the new guides are acceptable).
