# Release Management Guide

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-25

---

## Introduction

This guide outlines the automated release management workflow for the LEAP repository. We employ [**Release Please**](https://github.com/googleapis/release-please), an automated release manager that leverages Conventional Commits to parse version bumps, update changelogs, generate Release Pull Requests, and automate GitHub Releases upon merge.

We utilize a manifest-driven lockstep versioning strategy that covers the entire repository, including the nested `check-md` Python package, ensuring consistent pre-release validation and stable release synchronization.

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

The release management workflow described in this guide is **strictly scoped** to the LEAP repository itself. It operates entirely independently of any parent repositories that consume LEAP as a submodule. Downstream consuming repositories must manage their submodule pointers manually or use their own external versioning and integration workflows.
