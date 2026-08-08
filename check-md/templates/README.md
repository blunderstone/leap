# check-md Integration Templates

This directory contains templates for integrating check-md into various development workflows and CI/CD systems.

## Git Pre-commit Hook

### File

`pre-commit`

Runs check-md on staged markdown files before allowing a commit.

#### Installation

```bash
# From the check-md directory
cp templates/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

#### Features

- Checks only staged markdown files (`--staged` flag)
- Fails commit if violations found
- Provides clear error messages with fix instructions
- Can be bypassed with `git commit --no-verify` (not recommended)

#### Customization

Edit `.git/hooks/pre-commit` to:

- Change paths to check
- Add `--min-score` threshold
- Enable `--fix` mode for auto-fixing
- Adjust error messages

## GitHub Actions

### File

`github-actions.yml`

Workflow that runs check-md on pull requests and pushes.

#### Installation

```bash
# Create workflows directory if it doesn't exist
mkdir -p .github/workflows

# Copy template
cp templates/github-actions.yml .github/workflows/check-md.yml
```

#### Features

- Runs on markdown file changes
- Uses GitHub Actions annotations for inline errors
- Generates compliance report in job summary
- Configurable score threshold
- Works with pull requests and pushes

#### Customization

Edit `.github/workflows/check-md.yml` to:

- Change paths to check (line 19-21, 40)
- Adjust minimum score threshold (line 40)
- Add/remove branches to check (line 11-12, 14-15)
- Change output format

## GitLab CI

### File

`gitlab-ci.yml`

Job definition for GitLab CI pipelines.

#### Installation

Add the job to your `.gitlab-ci.yml`:

```yaml
include:
  - local: 'templates/gitlab-ci.yml'
```

Or copy the job definition directly into your existing `.gitlab-ci.yml`.

#### Features

- Runs only when markdown files change
- Generates JSON report artifacts
- Optional warning-only mode for development branches
- Configurable score threshold
- Artifact expiration

#### Customization

- Change paths to check
- Adjust minimum score threshold
- Modify artifact configuration
- Change rules for when to run

## Jenkins

### File

`Jenkinsfile`

Pipeline definition for Jenkins.

#### Installation

Option 1: Add to repository as `Jenkinsfile`
Option 2: Integrate stages into existing pipeline

#### Features

- Multi-stage pipeline (setup, check, report)
- Environment variable configuration
- Archived JSON reports
- Clear success/failure messages
- Error handling

#### Customization

Edit `Jenkinsfile` to:

- Change `MIN_SCORE` threshold (line 12)
- Adjust paths to check (line 27, 48)
- Modify report generation
- Add additional stages

## Common Customizations

### Change Paths

All templates check `kb/` and `docs/` by default. Update these to match your project:

```bash
# Example: Check only documentation directory
check-md documentation/ --min-score 80

# Example: Check multiple directories
check-md src/docs/ kb/ README.md --min-score 80

# Example: Use glob patterns
check-md "**/*.md" --exclude "node_modules/**" --min-score 80
```

### Adjust Score Thresholds

Default threshold is 80. Adjust based on your project's compliance:

```bash
# Strict: Require 90% compliance
check-md kb/ --min-score 90

# Lenient: Allow 70% compliance
check-md kb/ --min-score 70

# No threshold: Just report violations
check-md kb/
```

### Enable Auto-fix

For pre-commit hooks, you can enable auto-fix:

```bash
# Auto-fix staged files (use with caution)
check-md --staged --fix --quiet
```

#### Warning

Auto-fix modifies files. Review changes before committing.

### Configuration File

All templates respect `.check-md.yml` configuration:

```yaml
# .check-md.yml
rules:
  rule_1:
    enabled: true
    severity: error
  rule_2:
    enabled: true
    severity: warning
  rule_4:
    enabled: true
    severity: error

scoring:
  minimum_project_score: 85

exclude:
  - "node_modules/**"
  - "vendor/**"
  - "*.generated.md"
```

Place this file in your repository root to customize behavior across all integrations.

## Testing Templates

Before deploying to CI/CD, test templates locally:

```bash
# Test pre-commit hook
.git/hooks/pre-commit

# Test with staged files
git add some-file.md
check-md --staged

# Test with score threshold
check-md kb/ --min-score 80 --verbose
```

## Troubleshooting

### Hook not executing

```bash
# Ensure hook is executable
chmod +x .git/hooks/pre-commit

# Check for errors
.git/hooks/pre-commit
```

### check-md not found in CI

```bash
# Ensure installation step completes
pip install check-md

# Check PATH
export PATH="$HOME/.local/bin:$PATH"
```

### False positives

```bash
# Use ignore comments
<!-- check-md-ignore -->
**This:** won't be flagged

# Or configure rules
# In .check-md.yml:
rules:
  rule_1:
    enabled: false
```

## Support

For issues with templates or integration:

- Check check-md documentation: `check-md --help`
- Review configuration: `.check-md.yml`
- See examples in templates/
- Report issues: [GitHub Issues](https://github.com/your-org/check-md/issues)
