# QMD Indexing (Shared LEAP Tooling)

[QMD](https://github.com/tobi/qmd) is a third-party, on-device semantic search engine for
markdown (the `@tobilu/qmd` npm package) that also backs AI-agent knowledge retrieval via MCP.
Using it is optional, but it gives fast local search over a repository's LEAP `kb/`
documentation and lets AI agents retrieve that knowledge directly.

This tooling is maintained once here and shared by every repository that includes the LEAP
submodule, so there is a single source of truth rather than per-repo copies that drift apart.

User-facing documentation lives in [`kb/guide-qmd-config.md`](../../kb/guide-qmd-config.md),
covering what QMD is, the `<project>-<collection>` naming convention, setup, embeddings,
migration from unprefixed collections, and troubleshooting. This file covers the tooling
itself.

## Files

| File | Role |
|------|------|
| `qmd-config` | Canonical setup script. Derives the project prefix, registers collections, configures MCP clients, wires the pre-commit hook, installs the refresh job, and indexes content. |
| `pre-commit-qmd` | Canonical pre-commit hook. Refreshes the full-text index when markdown is staged. Bounded and fail-safe: never blocks a commit, and never embeds. |
| `qmd-refresh` | Brings the index and embeddings up to date. Incremental, and safe to run on a schedule. |
| `qmd-config.wrapper` | Template installed into a consuming repo as `utils/qmd/qmd-config`. |
| `pre-commit-qmd.wrapper` | Template installed into a consuming repo as `.githooks/pre-commit-qmd`. |
| `tests/qmd-config.test.sh` | Behavioral verification. Needs no qmd install and has no side effects. |

## The project prefix

Collections are named `<project>-<collection>`, where `<project>` is the **project prefix**: a
short identifier for the repository the documents came from, derived from its git remote name.

The prefix exists because collection names are global to a QMD index, with one path per name
and a second registration under an existing name rejected. Every repository on a machine shares
one index, so an unprefixed name like `adrs` would be claimed by whichever repository ran setup
first, leaving every other repository unindexed. Prefixing also lets a search target a single
project: `qmd query "..." -c <project>-adrs`.

The full collection table, the derivation rules, and the shared-collection exception are in
[the guide](../../kb/guide-qmd-config.md).

## How a repository consumes this

A repository carries a three-file kit derived from the wrapper templates:
`utils/qmd/qmd-config`, `utils/qmd/README.md`, and `.githooks/pre-commit-qmd`. None of them
contain logic.

The wrappers locate the canonical script by searching for any directory matching `leap*` at the
repository root or one level below it, so no particular submodule name is assumed. They pass the
consuming repository's root explicitly via `--repo-root`, because this script may run from
inside a submodule whose own git toplevel differs from the repository being configured.

## Design notes

**Embedding is excluded from the pre-commit hook.** It needs model weights that QMD downloads
separately, takes minutes on a large index, and stalls when those weights are absent, so running
it per commit would hold every markdown commit open. The hook refreshes only the full-text
index; `qmd-refresh` and the scheduled job handle embeddings.

**The scheduled job sets `PATH` explicitly.** Scheduled jobs do not read a shell profile, so a
`qmd` installed under a global npm prefix would otherwise not be found, and the job would run
and silently do nothing.

**Shared collections are registered once.** `leap` and `leap-*` are unprefixed and belong to a
single owner repository, because every participating repository contains a copy of the same
submodule content.

## Tests

```bash
bash scripts/qmd/tests/qmd-config.test.sh   # expects PASS=N FAIL=0
```

The suite builds throwaway git repositories with synthetic remotes and `kb/` layouts, runs
`qmd-config --dry-run` against each, and asserts the emitted plan. One fixture reproduces the
shared-submodule topology using a nested git repository, so wrapper resolution is exercised for
real. `QMD_PLATFORM` is overridable, so both scheduling backends are covered on one machine.

## Portability

The scripts target bash 3.2 (the default on macOS) and avoid bash 4+ features.
