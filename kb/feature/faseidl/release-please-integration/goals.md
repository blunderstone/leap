# Release Please Integration Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-25

---

## Quick Summary

Design, document, and implement Google's Release Please automated release management approach for this repository, establishing a repo-wide release workflow that supports a smooth transition from an initial beta pre-release cycle to release candidates and stable general releases as we prepare for open-sourcing.

---

## Executive Summary

As the LEAP repository prepares for its public open-source launch, manual release overhead and the risk of mismatched version numbers between the repository as a whole and its nested Python linter package (`check-md`) must be eliminated. Implementing **Release Please** provides a highly disciplined, automated, and standard-compliant release management process.

By analyzing Conventional Commits (e.g., `feat:`, `fix:`) and structured merge PRs on the default branch (`main`), Release Please automatically generates and maintains a rolling Release PR. This PR updates `CHANGELOG.md` files, bumps versions across all relevant descriptors, and—once merged—automates tagging and GitHub Release creation for this repository.

Our first open-source release will be a repository-wide **beta** release. This feature will design and deploy a manifest-driven Release Please setup that is highly flexible: starting with a `beta` pre-release cycle, supporting simple configuration updates to progress through Release Candidates (`rc`), and transitioning cleanly to stable general releases. It will version the LEAP repository itself while keeping the nested `check-md` package versions (`pyproject.toml`, `src/check_md/__init__.py`, and `uv.lock`) perfectly synchronized in lockstep. This setup is strictly concerned with LEAP-maintained releases of this repository and is entirely independent of any parent projects that consume LEAP as a submodule.

---

## Objectives

1. Automate repository-wide release management, changelog generation, and tagging using **Release Please** (v4+).
2. Configure a unified manifest-driven release strategy that tracks the version of the entire LEAP repository and keeps the nested `check-md` package in lockstep.
3. Establish a pre-release (`beta`) configuration to support initial open-source beta releases (e.g., transitioning from `1.0.0` to `1.0.0-beta.0` or bumping to future beta increments).
4. Ensure the release approach supports smooth, simple transitions from beta to release candidates (`rc`) and stable general releases.
5. Synchronize version numbers automatically across the repository manifest and all relevant python package metadata and lock files (`pyproject.toml`, `__init__.py`, and `uv.lock`).
6. Set up a modern GitHub Actions workflow to run Release Please on push events to the default branch (`main`).
7. Provide comprehensive developer documentation outlining Conventional Commits, Release Please lifecycle, and release workflows (including pre-release to stable transition instructions).

---

## Requirements

### Functional Requirements

- **REQ-1 (Manifest Configuration):** Create a root `release-please-config.json` defining a manifest-driven release structure for the LEAP repository (the root) and the nested `check-md` package, ensuring they are versioned in lockstep.
- **REQ-2 (Flexible Pre-release & Transition Support):** Enable pre-release configuration (initially `beta` pre-release), but ensure the setup supports simple, well-documented config changes to transition smoothly to RC releases (`rc`) and stable general releases.
- **REQ-3 (File Synchronization):** Configure `extra-files` within Release Please using JSONPath/TOML-path matching to keep `check-md/uv.lock` synchronized with the target version of `check-md`.
- **REQ-4 (GitHub Action Workflow):** Create `.github/workflows/release-please.yml` employing the official `googleapis/release-please-action@v4` with required write/pull-request permissions.
- **REQ-5 (Developer Documentation & Guides):** Create a detailed release management guide explaining how Conventional Commits drive versioning, how Release Please works, and step-by-step procedures to trigger/finalize beta, RC, and stable general releases.

### Non-Functional Requirements

- **Linter Compliance:** All modified and created Markdown files must strictly pass `check-md` with zero violations.
- **Schema Conformity:** All JSON/YAML configuration files must conform to their respective JSON schemas (e.g., Google's official Release Please schema).
- **Security & Permissions:** The GitHub Action must utilize strict, minimal, and secure permissions (`contents: write`, `pull-requests: write`).

### Testing Requirements

- Validate the JSON schema of `release-please-config.json` using an ecosystem JSON validator.
- Verify that `check-md` passes successfully over all modified and created documents.
- Verify that `uv.lock` is structurally valid and the package metadata is consistent.

### Documentation Requirements

- A dedicated, thorough release management guide (`kb/guide-release-management.md`) integrated into the knowledge base document taxonomy.
- Update root development guidelines or onboarding guides to point developers to this release workflow.

---

## Success Criteria

- [ ] `release-please-config.json` successfully drafted and validated against Google's official v4 schema.
- [ ] `.release-please-manifest.json` initialized with the first beta version target.
- [ ] Versions in `check-md/pyproject.toml`, `check-md/src/check_md/__init__.py`, and `check-md/uv.lock` aligned to the target beta version.
- [ ] `.github/workflows/release-please.yml` successfully created with correct event triggers and minimal security permissions.
- [ ] Complete developer guide (`kb/guide-release-management.md`) written and integrated, including explicit beta -> rc -> stable transition guides.
- [ ] All created and modified Markdown files pass `check-md kb/` with zero errors.

---

## Constraints

- Release Please configuration must support a nested Python project in a subdirectory (`check-md/`), maintaining lockstep versioning with the main repo release.
- Must operate entirely within standard Git/GitHub ecosystems.
- Release configurations must be decoupled from, and independent of, any downstream parent repositories that include LEAP as a submodule.

---

## Assumptions

- The repository itself is developed and maintained using the LEAP Methodology. Consequently, Release Please can confidently rely on highly structured, consistent, and LEAP-compliant commits and PR merges on the default branch (`main`).
- Standard `GITHUB_TOKEN` permissions in the target repo are sufficient or can be elevated if needed to trigger secondary actions (such as PyPI publish workflows).
- Releases are strictly concerned with LEAP-maintained releases of this repository, not downstream submodule parent repositories.

---

## Out of Scope

- Setting up automated PyPI publishing within this feature branch (this will be handled separately in the actual publication pipelines).
- Automating Docker image publication or other non-version-bumping publication steps.
- Any direct version management or workflow logic inside external parent repositories consuming this repo as a submodule.
