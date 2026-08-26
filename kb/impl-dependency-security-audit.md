# Implementation: Dependency Security Audit

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-06<br>
**Related:** [check-md README](../check-md/README.md)

---

## Overview

This document explains how dependency security scanning works in the LEAP repository, and records the non-obvious constraints that govern it.

LEAP contains one body of source code, `check-md/`, a Python project managed with `uv`. Everything described here exists to keep that project's dependencies free of known vulnerabilities.

Several of the constraints below share a property worth noting up front: when violated, they fail **silently**. A misconfigured scanner does not error, it simply reports nothing, which is indistinguishable from a clean result. Verifying that a check can still fail is therefore part of maintaining it.

## The Three Layers

Dependency security rests on three independent mechanisms. They fail independently, so knowing which one is reporting matters when diagnosing a finding.

| Layer                   | Configured by                          | What it does                                                       | Failure mode                                         |
|-------------------------|----------------------------------------|--------------------------------------------------------------------|------------------------------------------------------|
| Dependency graph alerts | Nothing (on by default)                | Scans `check-md/uv.lock` against GitHub Advisory DB, raises alerts | Reports vulnerabilities but fixes nothing            |
| Dependabot update PRs   | `.github/dependabot.yml`               | Opens PRs bumping outdated dependencies                            | Silent if ecosystem or directory is wrong            |
| `pip-audit` workflow    | `.github/workflows/security-audit.yml` | Fails CI when locked versions have advisories                      | Silent if the workflow is not at the repository root |

Alerts arrive whether or not the other two layers exist. A repository with alerts but no configuration file accumulates findings that nobody is prompted to fix.

## Workflows Must Live at the Repository Root

GitHub reads workflow definitions **only** from `.github/workflows/` at the root of the repository. A workflow file placed in a subdirectory is inert: it is not scheduled, not triggered, and does not appear in the Actions tab. Nothing reports the file as misplaced.

Placing the audit under `check-md/` looks correct if you think of that directory as a self-contained project. It is not, for this purpose. The workflow belongs at the root and reaches down into `check-md/`.

To confirm which workflows GitHub actually recognizes:

```bash
gh api /repos/blunderstone/leap/actions/workflows \
  --jq '.workflows[] | "\(.name) | \(.path) | \(.state)"'
```

Anything absent from that list is not running, regardless of what the file contains. Dependabot's own `dynamic/dependabot/*` entries always appear and are not repository workflows.

### Path Filters Are Root-Relative

Trigger paths resolve against the repository root, never against the workflow file's own location. The audit therefore names `check-md/pyproject.toml` and `check-md/uv.lock`, and the job sets `working-directory: check-md` so build commands resolve correctly.

A path filter matching nothing produces the same silent non-execution as a misplaced file. When editing triggers, confirm the paths exist:

```bash
git ls-files check-md/pyproject.toml check-md/uv.lock
```

### LEAP as a Submodule

LEAP is designed to be embedded in other projects as a Git submodule, as described in [impl-leap-adr-naming-exception](impl-leap-adr-naming-exception.md). Neither root-level configuration file travels with it:

- `.github/workflows/` is read only from the checked-out repository, so LEAP's audit workflow does not run in a parent project
- `.github/dependabot.yml` is read only from the repository root's default branch, so LEAP's update configuration is likewise ignored

A parent project embedding LEAP and wanting `check-md` covered must add its own entries pointing at the submodule path, such as `/leap/check-md`. This is the same portability concern that motivates LEAP's ADR naming exception, applied to CI configuration.

## Why the `uv` Ecosystem, Not `pip`

Dependabot treats `uv` as a distinct ecosystem from `pip`. The distinction matters: `check-md` is a `uv` project, and only the `uv` ecosystem updates `pyproject.toml` and `uv.lock` together.

Configuring `pip` against a `uv` project yields a configuration that appears valid and accomplishes nothing useful, because `uv.lock` is the file alerts fire against and `pip` does not maintain it.

Advisory metadata still reports `"ecosystem": "pip"`, because that field names the PyPI advisory source rather than the update mechanism. Do not read it as guidance for `package-ecosystem`.

## Why the Audit Reads the Lockfile

The audit exports pinned versions from `uv.lock` and scans those, rather than installing the project and scanning the result:

```bash
uv export --frozen --all-extras --no-emit-project -o requirements-audit.txt
uvx pip-audit --progress-spinner off -r requirements-audit.txt
```

Installing the project first — `pip install -e '.[dev]'` followed by a bare `pip-audit` — audits a **fresh resolution** from PyPI instead of the committed lockfile. Those are different dependency sets. A fresh install pulls current releases and can report clean while `uv.lock` still pins vulnerable versions, which is exactly what the alerts are reporting. Always audit the lockfile.

When changing these steps, verify both directions. A security job that cannot fail reads as coverage that does not exist:

```bash
# Should exit 0
uv export --frozen --all-extras --no-emit-project -o /tmp/current.txt
uvx pip-audit -r /tmp/current.txt; echo "exit $?"

# Should exit 1
printf 'black==25.11.0\npytest==8.4.2\n' > /tmp/known-bad.txt
uvx pip-audit -r /tmp/known-bad.txt; echo "exit $?"
```

The `--no-emit-project` flag omits `check-md` itself from the export, avoiding a spurious "dependency not found on PyPI" warning for the local project.

## The `requires-python` Trap

This is the subtlest failure mode, and the reason a lockfile can hold pins that no upgrade command will advance.

When `requires-python` spans a boundary where dependencies drop Python versions, `uv` splits resolution into **forks** and records a separate pinned version per fork. Given `requires-python = ">=3.9"` and a dependency whose patched releases require Python 3.10 or newer, `uv.lock` holds two entries for that package:

```toml
requires-python = ">=3.9"

# black 26.3.1   marker: python_full_version >= '3.10'   <- patched
# black 25.11.0  marker: python_full_version <  '3.10'   <- permanently vulnerable
```

The sub-3.10 fork cannot be upgraded, because no patched release supports 3.9. Dependabot reads every entry in the lockfile without evaluating environment markers, so it flags the stale fork indefinitely. Running `uv lock --upgrade` changes nothing.

### How to Recognize It

Three signals together indicate a resolution fork rather than an ordinary stale dependency:

1. The same package appears more than once in `uv.lock` with different `resolution-markers`
2. The advisory's first patched version is already present in the lockfile
3. `uv lock --upgrade` reports no change for the flagged package

To check for forks directly:

```bash
grep -c '^name = "black"' check-md/uv.lock
```

A count above one means the package is forked.

### How to Fix It

Raise the `requires-python` floor past the boundary. Moving to `requires-python = ">=3.10"` collapses both forks into a single resolution and removes the vulnerable pins outright.

Raising the floor is a supported-platform decision, not merely a lockfile edit. It is defensible when the dropped version is end-of-life, since an interpreter receiving no security patches of its own is a poor reason to pin vulnerable libraries.

When changing the floor, update every declaration naming a Python version, or the tooling silently disagrees with the manifest:

- `requires-python` and the `Programming Language :: Python :: *` classifiers
- `[tool.black] target-version`
- `[tool.ruff] target-version`
- `[tool.mypy] python_version`
- The stated requirement in `check-md/README.md` and `check-md/WORKFLOW-DEMONSTRATION.md`

## Operating the Pipeline

To review open alerts, including advisory detail and the manifest each came from:

```bash
gh api /repos/blunderstone/leap/dependabot/alerts \
  --jq '.[] | select(.state == "open") |
        "\(.number) \(.security_advisory.severity) \(.dependency.package.name) \(.dependency.manifest_path)"'
```

To reproduce the CI audit locally, from `check-md/`:

```bash
uv export --frozen --all-extras --no-emit-project -o /tmp/requirements-audit.txt
uvx pip-audit --progress-spinner off -r /tmp/requirements-audit.txt
```

After any dependency change, confirm the test suite and the CLI both still work:

```bash
uv run --extra dev pytest -q
uv run --extra dev check-md --help
```

The second command is not redundant. `typer` sits on `click`, so a `click` major bump can break the CLI while the test suite still passes.

## Known Gaps

The audit covers advisories for Python dependencies only. It does not check:

- Transitive vulnerabilities in the `uv` or `uvx` toolchain itself
- Actions pinned by major tag rather than commit SHA, which trades supply-chain precision for readable diffs
- Anything outside `check-md/`, since no other source code exists in this repository yet

`pip-audit` reports advisories present in its data sources at the time of the run. A clean run means nothing was known, not that nothing exists.

## Summary

1. Workflows run only from `.github/workflows/` at the repository root
2. Path filters are root-relative, not relative to the workflow file
3. Neither root configuration file travels with LEAP when it is embedded as a submodule
4. Use `package-ecosystem: uv`, not `pip`, or `uv.lock` goes unmaintained
5. Audit the lockfile, not a fresh install, or the audit checks a different dependency set than the one raising alerts
6. A package appearing twice in `uv.lock` signals a `requires-python` fork whose stale side cannot be upgraded
