# Release Management Guide

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-25

---

## Introduction

This guide outlines the automated release management workflow for the LEAP repository. We employ [**Release Please**](https://github.com/googleapis/release-please), an automated release manager that leverages Conventional Commits to parse version bumps, update changelogs, generate Release Pull Requests, and automate GitHub Releases upon merge.

We utilize a manifest-driven lockstep versioning strategy that covers the entire repository, including the nested `check-md` Python package, ensuring consistent pre-release validation and stable release synchronization.

---

## The Release Please Workflow (Step-by-Step)

Release Please does not publish releases the instant a code PR is merged. Instead, it maintains a **rolling Release Pull Request** that acts as a release preparation stage.

The publication workflow operates in four clear steps:

### Step 1: Developers Push Conventional Commits

All feature and fix branches are merged into the default branch (`main`) using Conventional Commits (e.g., `feat(api): ...` or `fix(linter): ...`).

### Step 2: Release Please Opens or Updates a Rolling Release PR

On every push to `main`, the Release Please GitHub Action triggers. It scans the commit history since the last release tag:

1. If there are eligible changes (like `feat` or `fix`), it automatically **opens a new Release Pull Request** (typically titled `chore(main): release vX.Y.Z-beta.N`).
2. If a Release PR is already open, it automatically **appends new commits** to that existing PR, updates the draft changelog, and recalculates the next version bump.

### Step 3: Merging the Release PR Publishes the Release

The Release PR acts as your release staging ground. To actually execute and publish a release:

1. Review the automated `CHANGELOG.md` edits and version bumps in the open Release PR.
2. When ready to publish, **simply merge the Release Pull Request** into `main`!

### Step 4: Automated Tagging and GitHub Release

Upon merging the Release PR, the Release Please Action triggers again. It detects that a release branch has been merged and automatically:

1. Creates the corresponding git version tag (e.g., `v1.0.0-beta.0`) on `main`.
2. Creates and publishes an official, beautiful **GitHub Release** containing the compiled changelog notes.
3. This published release is what shields.io and other badge services query to display the current version.

---

## Conventional Commits

Version increments and changelog entries are completely driven by **Conventional Commits** pushed to the default branch (`main`).

### Commit Types

- `fix:` — Bumps the patch version (e.g., `1.0.0-beta.0` -> `1.0.0-beta.1` or `1.0.0` -> `1.0.1`). Maps to **Bug Fixes** in the changelog.
- `feat:` — Bumps the minor version (e.g., `1.0.0-beta.0` -> `1.1.0-beta.0` or `1.0.0` -> `1.1.0`). Maps to **Features** in the changelog.
- `feat!:` or adding `BREAKING CHANGE:` in the commit footer — Bumps the major version (e.g., `1.0.0-beta.0` -> `2.0.0-beta.0` or `1.0.0` -> `2.0.0`). Maps to **BREAKING CHANGES** in the changelog.

### Format

```text
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

For example:

```text
feat(check-md): add version-alignment check to ensure lockstep releases
```

---

## Configuration

We use a manifest-driven Release Please setup located at the root of the repository.

### Config File (`release-please-config.json`)

The config specifies the root package `.` using the `"simple"` release-type. It manages the global repository version and maps nested Python files as `extra-files` to keep them synchronized in lockstep:

```json
{
  "$schema": "https://raw.githubusercontent.com/googleapis/release-please/main/resources/schema.json",
  "packages": {
    ".": {
      "release-type": "simple",
      "prerelease": true,
      "prerelease-type": "beta",
      "extra-files": [
        {
          "type": "toml",
          "path": "check-md/pyproject.toml"
        },
        "check-md/src/check_md/__init__.py",
        {
          "type": "toml",
          "path": "check-md/uv.lock",
          "jsonpath": "$.package[?(@.name=='check-md')].version"
        }
      ]
    }
  }
}
```

### Manifest File (`.release-please-manifest.json`)

The manifest acts as the single source of truth for the active repository release version:

```json
{
  ".": "1.0.0-beta.0"
}
```

---

## Release Lifecycle & Transitions

Automated releases progress through three distinct states: **Beta Pre-releases**, **Release Candidates (RC)**, and **Stable General Releases**.

### State 1: Beta Pre-releases

Initially, the repository is configured for beta pre-releases.

- **Config Settings:**
  - `"prerelease": true`
  - `"prerelease-type": "beta"`
- **Version Suffix:** `x.y.z-beta.n`
- **Behavior:** Merging conventional commits will open/update a release PR bumping the beta suffix (e.g., `1.0.0-beta.0` to `1.0.0-beta.1`). Merging the release PR tags a GitHub Release and triggers any downstream CD pipelines.

### State 2: Transitioning to Release Candidates (RC)

When the beta cycle is complete, and we enter stabilization, the release-type transitions to `rc`.

1. Edit `release-please-config.json` to change `"prerelease-type"` to `"rc"`:
   ```json
   "prerelease": true,
   "prerelease-type": "rc"
   ```

2. Commit and merge this change into `main`.
3. Subsequent Conventional Commits or manual manifest bumps will transition the release PR versioning pattern to `rc` (e.g., `1.0.0-rc.0`).

### State 3: Transitioning to Stable General Releases

When the RC is verified, and we are ready for a general, stable launch.

1. Edit `release-please-config.json` to toggle `"prerelease"` to `false` and remove `"prerelease-type"`:
   ```json
   "prerelease": false
   ```

2. Commit and merge this change into `main`.
3. Release Please will automatically open a release PR that removes the pre-release suffix entirely, proposing a stable, general-purpose release (e.g., `1.0.0`).

---

## Submodule Boundaries

The release management workflow described in this guide is **strictly scoped** to the LEAP repository itself. It operates entirely independently of any parent repositories that consume LEAP as a submodule.

### Submodule Version Locking Best Practice

Because the `main` branch acts as an active, rolling development stream (the equivalent of a `SNAPSHOT` release), pointing a parent project's Git submodule directly to the `main` branch introduces the risk of consuming unreleased, in-development changes.

For this reason, we strongly recommend that **all consuming repositories lock their submodule pointers to specific tagged release versions** (e.g., `v1.0.0-beta.0`) rather than tracking the `main` branch:

1. **Locking to a Tag:**

   ```bash
   # Switch the submodule to a specific release tag
   cd leap
   git checkout tags/v1.0.0-beta.0
   cd ..
   git add leap
   git commit -m "chore: lock LEAP submodule to v1.0.0-beta.0"
   ```

2. **Updating to New Releases:** When a new release is published (e.g., `v1.0.0`), developers should explicitly pull the tags, checkout the new tag in the submodule, and commit the updated submodule pointer. This ensures that the parent codebase is always building against a stable, immutable, and fully validated release.
