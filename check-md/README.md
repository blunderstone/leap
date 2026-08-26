# check-md

A fast, Python-based markdown linter that enforces [ADR leap-adr-002](../kb/adr/leap-adr-002__markdown-formatting-standards.md) formatting standards for LEAP-compliant documentation.

## Features

- 🔍 **Five Core Rules**: Semantic headings (Rule 1), block separation (Rule 2), heading hierarchy (Rule 3), nested code blocks (Rule 4), label-value sequences (Rule 5)
- 🔧 **Auto-fix Mode**: Automatically correct violations with `--fix`
- 📊 **Compliance Scoring**: Project and module-level scores (0-100)
- ⚙️ **Configuration**: `.check-md.yml` for project-specific settings
- 🚫 **Ignore Comments**: Selective disabling with HTML comments
- 🔗 **CI/CD Integration**: Templates for GitHub Actions, GitLab CI, Jenkins
- 🪝 **Git Hooks**: Pre-commit hook template included
- 📝 **Multiple Output Formats**: Text, JSON, GitHub Actions annotations

## Quick Start

### Installation

`check-md` requires **Python 3.10 or higher**.

Because modern operating systems restrict global `pip` installations (PEP 668), it is highly recommended to install `check-md` inside a virtual environment, or use a tool like `uv` or `pipx`.

#### Option A: Fast & Modern with `uv` (Recommended)

[`uv`](https://github.com/astral-sh/uv) is an extremely fast Python package manager that automatically handles Python versions and virtual environments.

The absolute best way to install `check-md` for local development is using `uv tool install --editable .`. This installs it in an isolated global environment, places the standalone `check-md` executable directly on your system's `PATH`, and automatically reflects any local code changes instantly without needing a `uv run` prefix.

```bash
# 1. Install uv (if not already installed)
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Or via package managers (Homebrew / winget):
brew install uv              # macOS/Linux
winget install astral-sh.uv  # Windows

# 2. Install check-md globally in editable mode
cd check-md
uv tool install --editable .

# 3. Ensure your shell PATH is permanently configured (if not already)
# If check-md is not found, you can have uv update your shell profile/environment permanently:
uv tool update-shell
# Or add it manually to your shell configuration:
# macOS/Linux (e.g., ~/.zshrc or ~/.bashrc): export PATH="$HOME/.local/bin:$PATH"
# Windows (PowerShell): Add "$env:USERPROFILE\.local\bin" to your user PATH environment variable

# 4. Reload your terminal and run check-md directly from anywhere!
check-md --help
```

*(Note: If you prefer to keep everything strictly local to the folder, you can run `uv sync` to create a local `.venv` and then use `uv run check-md` or run `source .venv/bin/activate` to add the executable to your path.)*

#### Option B: Standard Python Virtual Environment

If you prefer standard Python tooling, use Python's built-in `venv` module:

```bash
# 1. Navigate to the check-md directory
cd check-md

# 2. Create a virtual environment with Python 3.10+
python3 -m venv .venv

# 3. Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows (Command Prompt):
.venv\Scripts\activate.bat
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 4. Install check-md with development dependencies in editable mode
pip install -e ".[dev]"

# 5. Verify and run (within active virtual environment)
check-md --help
```

#### Option C: Production Installation (from PyPI)

Once published to PyPI, you can install `check-md` globally using `pipx` (highly recommended for Python CLI tools) or via standard pip:

```bash
# Install globally via pipx
pipx install check-md

# Or via standard pip inside a virtual environment
pip install check-md
```

### Basic Usage

```bash
# Check a single file
check-md README.md

# Check a directory (recursive)
check-md kb/

# Check with glob patterns
check-md "kb/**/*.md"

# Auto-fix violations
check-md README.md --fix

# Check staged files (for git hooks)
check-md --staged
```

## Rules

### Rule 1: Semantic Headings

#### Purpose

Use markdown headers for structure, not bold text.

❌ **Wrong:**

```markdown
**Source:**
- item 1
```

✅ **Correct:**

```markdown
#### Source

- item 1
```

#### Valid Use Cases

Bold text is allowed for emphasis in these contexts:

- **In sentences:** `This is a sentence with **bold emphasis** in the middle.`
- **In list items:** `- **Important:** description text`
- **In code blocks:** (all markdown inside code blocks is ignored)

#### Auto-fix

Converts standalone bold text to level-4 headers.

### Rule 2: Block Separation

#### Purpose

Separate block elements from paragraphs with blank lines.

❌ **Wrong:**

<!-- check-md-ignore-begin -->
````markdown
Here's the code:
```python
def hello():
    print("Hello")
```
````
<!-- check-md-ignore-end -->

✅ **Correct:**

````markdown
Here's the code:

```python
def hello():
    print("Hello")
```
````

#### Auto-fix

Inserts blank line before block elements.


### Rule 3: Heading Level Increment

#### Purpose

Heading levels should only increase by one level at a time. This ensures proper document structure for accessibility (screen readers) and follows WCAG 2.1 guidelines.

❌ **Wrong** - skips level 3:

```markdown
## Section

#### Subsection
```

✅ **Correct** - increments by 1:

```markdown
## Section

### Subsection
```

#### Valid sequences

- Increments of 1: `# → ##`, `## → ###`, `### → ####`
- Decrements of any size: `#### → ##` (closing sections)
- Same level: `## → ##` (sibling sections)

#### Invalid sequences

- Increments > 1: `## → ####` (skipped `###`)

#### Auto-fix

**Conservative mode** (`check-md --fix` or `--fix-strategy conservative`):

- Downgrades skipped heading to next valid level (e.g., `## → ####` becomes `## → ###`)
- If fix would create cascade, inserts TODO placeholder instead
- Format: `### TODO: check-md - add missing level 3 heading`
- TODO placeholders are reported as violations to remind you to fix structure

**Aggressive mode** (`check-md --fix-strategy aggressive`):

- Removes any existing TODO placeholders
- Applies cascading fixes (downgrades multiple sequential violations)
- Use when document structure is known to be correct

#### Example

```bash
# Conservative: Safe mode with TODO insertion
check-md docs/ --fix

# Aggressive: Apply all cascade fixes
check-md docs/ --fix-strategy aggressive
```

### Rule 4: Nested Code Blocks

#### Purpose

Use longer fences for outer blocks when nesting code blocks.

❌ **Wrong** - inner fence closes outer:

<!-- check-md-ignore-begin -->
````text
```markdown
Example:

```bash
command
```
```
````
<!-- check-md-ignore-end -->

✅ **Correct** - outer fence is longer:

`````text
````markdown
Example:

```bash
command
```
````
`````

#### Auto-fix

Increases outer fence length to 4 backticks.

### Rule 5: Label-Value Sequence Line Breaks

#### Purpose

Ensure consecutive label-value lines have `<br>` tags to prevent unwanted wrapping.

When multiple label-value pairs appear consecutively (like in frontmatter or metadata sections), they need `<br>` tags between them. Without these tags, markdown renderers may wrap them together, making them hard to read.

❌ **Wrong** - missing `<br>` tags:

```markdown
**Author:** [F. Andy Seidl](https://linkedin.com)
**Date:** 2025-12-18
**Status:** Active
```

This renders as: **Author:** [F. Andy Seidl](https://linkedin.com) **Date:** 2025-12-18 **Status:** Active (all on one wrapped line)

✅ **Correct** - with `<br>` tags:

```markdown
**Author:** [F. Andy Seidl](https://linkedin.com)<br>
**Date:** 2025-12-18<br>
**Status:** Active
```

This renders with each pair on its own line, improving readability.

#### Pattern Detection

Rule 5 detects label-value patterns in these formats:

- `**Label:** value` - colon inside bold
- `**Label**: value` - colon outside bold

The rule flags consecutive label-value lines missing `<br>` tags. The last line in a sequence doesn't need a `<br>` tag since the sequence naturally ends.

#### Valid Use Cases

Label-value lines that DON'T need `<br>` tags:

- **Single label-value line** (no following label-value line)
- **Last line in sequence** (sequence naturally ends)
- **Separated by blank line** (blank lines break the sequence)
- **In code blocks** (all markdown inside code blocks is ignored)

#### Auto-fix

Automatically adds `<br>` tags to the end of label-value lines (except the last line in a sequence). Also strips any trailing whitespace before adding the `<br>` tag.

## Command-Line Options

### Basic Options

```bash
check-md [PATH...] [OPTIONS]
```

#### Positional Arguments

- `PATH`: Files or directories to check (default: current directory)

#### Common Options

- `--fix`: Automatically fix violations (shorthand for `--fix-strategy conservative`)
- `--fix-strategy <strategy>`: Fix strategy - `conservative` (insert TODOs for cascades), `aggressive` (apply all fixes including cascades), or `none` (check only)
- `--dry-run`: Preview fixes without modifying files (requires `--fix` or `--fix-strategy`)
- `--quiet`: Suppress summary output
- `--verbose`: Show detailed context for violations
- `--staged`: Check only git-staged files

### Output Options

```bash
# Different output formats
check-md kb/ --format text      # Human-readable (default)
check-md kb/ --format json      # Machine-readable JSON
check-md kb/ --format github    # GitHub Actions annotations
```

### Scoring Options

```bash
# Compliance scoring
check-md kb/ --min-score 80     # Exit 1 if score < 80
check-md kb/ --sort score       # Sort by score (default)
check-md kb/ --sort name        # Sort by module name
check-md kb/ --sort violations  # Sort by violation count
```

### Backup Management

```bash
# Backup file operations
check-md kb/ --fix --clean-backups    # Auto-clean after fix
check-md kb/ --rollback               # Restore from .bak files
check-md kb/ --clean-backups          # Remove .bak files (verifies)
check-md kb/ --clean-backups --force  # Remove .bak without verification
```

### File Selection

```bash
# Include/exclude patterns
check-md kb/ --include "*.md" --exclude "node_modules/**"

# Only staged files
check-md --staged
```

## Configuration

Create `.check-md.yml` in your repository root:

```yaml
# Rule configuration
rules:
  rule_1:
    enabled: true
    severity: error  # error, warning, info
  rule_2:
    enabled: true
    severity: error
  rule_4:
    enabled: true
    severity: error
  rule_5:
    enabled: true
    severity: error

# Scoring thresholds
scoring:
  minimum_project_score: 80
  minimum_module_score: 75

# Exclusion patterns
exclude:
  - "node_modules/**"
  - "build/**"
  - "*.generated.md"
```

## Ignore Comments

Selectively disable checking with HTML comments:

```markdown
<!-- check-md-ignore -->
**This:** won't be flagged

<!-- check-md-ignore-next -->
**Next line:** won't be flagged

<!-- check-md-ignore-begin -->
**Multiple lines:** not flagged
**More lines:** not flagged
<!-- check-md-ignore-end -->
```

## Integration

### Git Pre-commit Hook

Install the pre-commit hook to check files before committing:

```bash
# From check-md directory
cp templates/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

The hook will prevent commits with markdown violations.

### GitHub Actions

Add to `.github/workflows/check-md.yml`:

```yaml
name: Markdown Quality

on: [push, pull_request]

jobs:
  check-markdown:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install check-md
      - run: check-md kb/ docs/ --format github --min-score 80
```

### CI/CD Templates

See `templates/` directory for:

- `github-actions.yml` - GitHub Actions workflow
- `gitlab-ci.yml` - GitLab CI job
- `Jenkinsfile` - Jenkins pipeline
- `README.md` - Complete integration guide

## Exit Codes

- `0` - Success (no violations or score above threshold)
- `1` - Violations found or score below threshold
- `2` - Error (file not found, invalid arguments, etc.)

## Examples

### Check and Fix

```bash
# Check files, show violations
check-md kb/feature/my-feature/

# Preview fixes
check-md kb/feature/my-feature/ --fix --dry-run

# Apply fixes
check-md kb/feature/my-feature/ --fix

# Fix and clean backups automatically
check-md kb/feature/my-feature/ --fix --clean-backups
```

### Compliance Reporting

```bash
# Get project compliance score
check-md kb/ --min-score 80

# Detailed report with context
check-md kb/ --verbose

# JSON output for parsing
check-md kb/ --format json > report.json
```

### Workflow Integration

```bash
# Pre-commit: check staged files
check-md --staged --quiet

# CI/CD: enforce threshold
check-md kb/ docs/ --min-score 85 --format github

# Development: auto-fix on save
check-md src/docs/ --fix --quiet
```

## Troubleshooting

### False Positives

Use ignore comments to disable checking:

```markdown
<!-- check-md-ignore -->
**Intentional bold:** for emphasis
```

Or disable rules in `.check-md.yml`:

```yaml
rules:
  rule_1:
    enabled: false
```

### Backup Files

After fixing, `.bak` files are created:

```bash
# Remove backups for checked files (verifies no violations)
check-md kb/ --clean-backups

# Restore from backups
check-md kb/ --rollback

# Force cleanup without verification
check-md kb/ --clean-backups --force

# Clean ALL backups project-wide (use after fixing everything)
find . -name "*.bak" -type f -delete
```

**Note:** `--clean-backups` only removes backups for files that were just checked. To clean orphaned backups across the entire project, use the `find` command above.

### Hook Not Running

```bash
# Ensure hook is executable
chmod +x .git/hooks/pre-commit

# Test hook manually
.git/hooks/pre-commit
```

## Development

### Running Tests

```bash
# All tests
pytest tests/

# With coverage
pytest tests/ --cov=check_md --cov-report=html

# Specific test file
pytest tests/test_rules.py -v
```

### Code Style

```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Linting
ruff src/ tests/
```

## Project Information

- **Author:** F. Andy Seidl
- **License:** Apache-2.0
- **Python:** 3.10+
- **Dependencies:** typer, pyyaml
- **Repository:** Part of the LEAP methodology and tooling repository

## Related Documentation

- [ADR leap-adr-002: Markdown Formatting Standards](../kb/adr/leap-adr-002__markdown-formatting-standards.md)
- [Integration Templates](templates/README.md)
- [LEAP Methodology](../kb/guide-methodology.md)

## Support

For issues or questions:

1. Check this README
2. Review configuration: `.check-md.yml`
3. See integration templates: `templates/`
4. Report issues to the team
