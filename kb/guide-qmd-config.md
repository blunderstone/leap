# QMD Configuration Guide

**Purpose:** Set up QMD documentation indexing for a repository<br>
**Author:** Rashaad Mirza<br>
**Date:** 2026-07-31

---

## What QMD is and why you would use it

[QMD](https://github.com/tobi/qmd) is a local semantic search engine for markdown
documentation. It combines full-text search, vector embeddings, and re-ranking, all running
on-device, and it also serves as a knowledge retrieval layer for AI agents via MCP (Model
Context Protocol). It is a third-party tool, distributed as the `@tobilu/qmd` npm package, and
the setup script installs it globally via npm.

Adopting it is optional, and nothing in the LEAP methodology depends on it, but a repository
that does adopt it gains:

- **Semantic search over your own documentation.** Ask questions in natural language and get
  relevant `kb/` documents back, without needing to recall exact wording or file names.

- **Knowledge retrieval for AI agents.** Agents working in the repository can query the
  documentation directly through MCP instead of guessing at file locations.

- **Scoped results.** Collections are namespaced per project, so a query aimed at one
  repository does not return another repository's documents.

- **An index that stays current.** A pre-commit hook refreshes the full-text index when
  markdown is staged, without slowing the commit down.

## What running the setup script does

Be aware that setup has machine-level effects. Running `qmd-config`:

1. Installs QMD globally via npm, if it is not already installed.
2. Registers this repository's collections in the QMD index.
3. Attaches context hints describing each collection.
4. Registers the QMD MCP server with the AI coding agents you have installed:
   Claude Code (`~/.claude.json`) and Gemini CLI (`~/.gemini/settings.json`).

5. Wires a QMD pre-commit hook into `.git/hooks/pre-commit`.
6. Installs a daily background job that keeps embeddings current.

7. Indexes the repository's content and attempts to generate embeddings.

The QMD index is **global per developer machine**, not per repository. Every repository you set
up shares one index, which is why collection names must be unique across repositories.

Preview everything without changing anything:

```bash
# In a consuming repository (using the installed wrapper):
./utils/qmd/qmd-config --dry-run

# In the standalone leap repository (using the canonical script):
./scripts/qmd/qmd-config --dry-run
```

## Collection naming convention

Collections are named `<project>-<collection>`.

QMD allows exactly one path per collection name, and a second registration under an existing
name is rejected. Unprefixed names such as `adrs` would therefore let the first repository
registered claim them for every repository. Prefixing with the project name lets every
repository coexist in the shared index and lets queries target a specific project.

| Collection | Content |
|------------|---------|
| `<project>-adrs` | Architecture Decision Records in any `*/kb/adr/` |
| `<project>-features` | LEAP feature docs: goals, plans, phase docs, summaries |
| `<project>-planning` | LEAP Planning extension documents |
| `<project>-guides` | All `.md` files directly in any `kb/` directory |
| `<project>-meta` | Process docs: `best-practices-*`, `lessons-*`, `tech-debt-*`, `idea-*`, `benchmark-*` |
| `<project>-readmes` | Module entry-point docs: `!ReadMe*.md` and `README.md` |

### How the project prefix is derived

Resolution follows this precedence:

1. An explicit `--prefix <name>` argument.
2. The git remote name, for example `webapp` from
   `https://github.com/example-org/webapp.git`.

3. The repository directory name, used only when no remote is configured.

The remote name is preferred because it is identical in every clone, whereas a directory name
is whatever the developer chose at clone time. Since collection names are global to the shared
index, a name that varied per machine would defeat the purpose.

### Shared LEAP collections

The `leap` and `leap-*` submodule collections are **not** prefixed. They are registered exactly
once, by a single owner repository (`commons` by default).

The reason is that these collections index the LEAP submodule, and every participating
repository includes a copy of that same submodule. Registering it in each repository would add
the same documents to the index over and over, so a single search would return several
identical hits. Registering it once keeps one copy in the index, shared by every project.

Override the default when needed:

```bash
# In a consuming repository (using the installed wrapper):
./utils/qmd/qmd-config --with-shared   # register the shared collections here
./utils/qmd/qmd-config --no-shared     # skip them

# In the standalone leap repository (using the canonical script):
./scripts/qmd/qmd-config --with-shared   # register the shared collections here
./scripts/qmd/qmd-config --no-shared     # skip them
```

## Setting up a repository

### Prerequisites

- `npm` and Node.js, for installing QMD and for editing the MCP client configs
- The LEAP submodule initialized: `git submodule update --init`

### The per-repo kit

A participating repository carries three small files:

| File | Role |
|------|------|
| `utils/qmd/qmd-config` | Thin wrapper that runs the shared canonical script against this repo |
| `utils/qmd/README.md` | Repository-specific setup notes |
| `.githooks/pre-commit-qmd` | Thin wrapper that runs the shared canonical hook |

None of them contain logic. The canonical implementation lives once in the LEAP submodule at
`scripts/qmd/`, so a fix applied there reaches every repository through a submodule update
rather than by editing copies. Wrapper templates for the two wrappers are in
`scripts/qmd/qmd-config.wrapper` and `scripts/qmd/pre-commit-qmd.wrapper`.

### Running setup

Once per development machine:

```bash
# In a consuming repository (using the installed wrapper):
./utils/qmd/qmd-config

# In the standalone leap repository (using the canonical script):
./scripts/qmd/qmd-config
```

After reorganizing modules, rebuild the collection masks from the current structure:

```bash
# In a consuming repository (using the installed wrapper):
./utils/qmd/qmd-config --clean

# In the standalone leap repository (using the canonical script):
./scripts/qmd/qmd-config --clean
```

## The two ways QMD searches

**Full-text search** matches the words you type, the way most search boxes do.

**Semantic search** matches meaning instead, so asking "how do I load data" can surface a
document that never uses those words. It works by converting each document into a list of
numbers (an **embedding**) that represents what the document is about, then finding the
documents whose numbers sit closest to your question. Those numbers are generated once per
document and regenerated whenever the document changes.

Full-text search works the moment setup finishes. Semantic search needs the embeddings, which
is what the next two sections are about.

## Semantic search needs model weights

**Action required, once per machine:** run `qmd pull`, then `qmd embed`. Skip this and
full-text search still works, but semantic search returns nothing.

QMD runs its embedding, re-ranking, and query-expansion models on-device, and it downloads
those weights separately from the npm package. Until they are present, `qmd embed` fails:

```bash
qmd pull     # fetch model weights (a substantial download, once per machine)
qmd embed    # build vectors for indexed documents
qmd doctor   # diagnose model cache, index, and embedding freshness
```

Full-text search (`qmd search`) works without any of this, so a repository is useful the moment
setup finishes. Setup reports a warning rather than failing when embedding cannot complete, and
the pre-commit hook never runs embedding at all, so missing weights slow nothing down and block
nothing.

### Keeping embeddings current

Embeddings go stale as documentation changes, and nothing refreshes them on its own, since the
pre-commit hook deliberately skips embedding to keep commits fast. Bring them up to date with:

```bash
scripts/qmd/qmd-refresh          # index plus embeddings, incremental
scripts/qmd/qmd-refresh --pull   # also fetch model weights, for a first run
```

Setup installs a daily background job that does this for you, so semantic search stays current
without anyone remembering to run anything. It logs to `/tmp/qmd-refresh.log`. Skip it with
`--no-schedule`, or take an existing one away with `--remove-schedule`.

### Model downloads behind a TLS-inspecting proxy

If your organization routes traffic through a TLS-inspecting proxy (Zscaler, Netskope, and
similar products re-sign HTTPS traffic), `qmd pull` can fail while ordinary browsing and `curl`
work fine:

```text
UNABLE_TO_GET_ISSUER_CERT_LOCALLY
```

The cause is that Node.js ships its own certificate bundle rather than consulting the operating
system trust store. Your OS trusts the proxy's root certificate because IT installed it, but
Node does not know about it, so it rejects the re-signed certificate.

Point Node at that root explicitly. On macOS, export it from the keychain and set
`NODE_EXTRA_CA_CERTS`:

```bash
security find-certificate -a -c "<proxy vendor>" -p \
  /Library/Keychains/System.keychain > ~/.config/corporate-ca.pem

export NODE_EXTRA_CA_CERTS="$HOME/.config/corporate-ca.pem"
qmd pull
```

Add the `export` line to your shell profile to make it persistent. Confirm it worked with:

```bash
node -e 'fetch("https://huggingface.co",{method:"HEAD"}).then(r=>console.log(r.status))'
```

`NODE_EXTRA_CA_CERTS` adds the certificate your system already trusts and leaves verification
fully intact. Do not reach for `NODE_TLS_REJECT_UNAUTHORIZED=0`: it disables certificate
validation for every connection the process makes, which is a far broader change than the
problem warrants.

## Migrating from unprefixed collections

Setups that predate this convention registered collections under bare names such as `adrs`
and `features`. Because collection names are global to the index, whichever repository ran
first claimed those names for every repository, and queries meant for another project silently
returned that repository's documents.

Clearing them is a one-time step, and because the index is per developer machine, **each
developer runs it on their own machine**:

```bash
# In a consuming repository (using the installed wrapper):
./utils/qmd/qmd-config --remove-legacy --clean

# In the standalone leap repository (using the canonical script):
./scripts/qmd/qmd-config --remove-legacy --clean
```

`--remove-legacy` drops the bare project collection names; `--clean` drops this project's
prefixed collections so they are rebuilt from the current structure. The shared `leap` and
`leap-*` collections are never removed by `--remove-legacy`, since they are unprefixed by
design rather than legacy.

## Everyday use

```bash
# Hybrid search with re-ranking, restricted to one collection
qmd query "architecture decisions" -c <project>-adrs
qmd query "lessons learned" -c <project>-meta

# Refresh the full-text index (the pre-commit hook does this on markdown commits)
qmd update

# Refresh semantic vectors (out of band; see "Semantic search needs model weights")
qmd embed

qmd status
```

## Options reference

| Option | Effect |
|--------|--------|
| `--dry-run` | Print the intended plan and exit; no installation, registration, or indexing |
| `--clean` | Remove this project's collections before re-registering |
| `--remove-legacy` | Remove unprefixed project collections left by pre-convention setups |
| `--no-schedule` | Do not install the daily embedding refresh |
| `--remove-schedule` | Remove a previously installed refresh job |
| `--prefix <name>` | Override the derived project prefix |
| `--with-shared` | Register the shared `leap`/`leap-*` collections here |
| `--no-shared` | Skip the shared collections |
| `--repo-root <dir>` | Target a specific repository root; supplied automatically by the wrapper |

## Notes for maintainers

- The scripts target bash 3.2, the default on macOS, and avoid bash 4+ features.
- Verify changes with `bash scripts/qmd/tests/qmd-config.test.sh`, which builds throwaway
  repositories and asserts against `--dry-run` output. It requires no QMD installation and
  leaves no machine state behind.

- Because the index is global per machine, renaming collections requires every developer to
  re-run `qmd-config --clean` to converge.
