# Best Practices: Markdown

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2025-11-13<br>
**Last Updated:** 2026-02-04

---

## Overview

This guide documents best practices for writing and maintaining markdown documentation in LEAP projects. The `check-md` tool automatically enforces markdown formatting standards defined in [ADR leap-adr-002](../adr/leap-adr-002__markdown-formatting-standards.md).

## Markdown Formatting Standards

The `check-md` tool enforces these core formatting standards:

### Rule 1: Semantic Headings

Use proper heading levels (`#`, `##`, `###`) for document structure, not bold text.

**Why:** Screen readers and document outlines recognize headings as structural elements. Bold text is not semantic markup.

#### Example violation

```markdown
**Goals:**
- Goal 1
```

#### Correct

```markdown
#### Goals

- Goal 1
```

### Rule 2: Block Separation

Separate block elements (code blocks, lists, tables) from paragraphs with blank lines.

**Why:** CommonMark specification requires blank lines to prevent block elements from wrapping into paragraphs.

#### Example violation

<!-- check-md-ignore-begin -->
````markdown
Here's an example:
```python
code()
```
````
<!-- check-md-ignore-end -->

#### Correct

````markdown
Here's an example:

```python
code()
```
````

### Rule 3: Heading Hierarchy

Heading levels should increment by one (don't skip levels). This follows WCAG 2.1 accessibility guidelines.

#### Example violation

```markdown
## Section
#### Subsection
```

#### Correct

```markdown
## Section
### Subsection
```

### Rule 4: Nested Code Blocks

Use longer fences (four backticks) for outer blocks when nesting code blocks.

**Why:** Inner triple-backticks will prematurely close outer triple-backtick blocks.

### Rule 5: Label-Value Line Breaks

Consecutive label-value pairs need `<br>` tags to prevent unwanted wrapping.

#### Example

```markdown
**Author:** [Name](link)<br>
**Date:** 2026-02-04<br>
**Status:** Active
```

**See:** [ADR leap-adr-002](../adr/leap-adr-002__markdown-formatting-standards.md) for complete formatting standards.

## When to Run check-md

### During Development

After creating or editing markdown:

```bash
check-md kb/feature/my-feature/goals.md --fix --quiet
```

Before committing:

```bash
check-md --staged --fix
```

### In CI/CD Pipelines

Enforce compliance automatically:

```yaml
# GitHub Actions example
- name: Check Markdown Quality
  run: check-md kb/ docs/ --min-score 80 --format github
```

See `leap/check-md/templates/` for complete CI/CD examples.

### As Pre-commit Hook

Install the hook:

```bash
cp leap/check-md/templates/pre-commit .git/hooks/pre-commit
```

```bash
chmod +x .git/hooks/pre-commit
```

The hook checks staged files and prevents commits with violations.

## Interpreting Results

### Violation Messages

check-md reports violations in this format:

```
file.md:42: [ADR-002-R1] Standalone bold text should be a heading
  Context: **Source:**
  Fix: Replace with: #### Source
```

#### Components

- **Location**: `file.md:42` - File and line number
- **Rule**: `[ADR-002-R1]` - Rule identifier
- **Message**: Clear description of the issue
- **Context**: The problematic line
- **Fix hint**: Suggested correction

### Compliance Scores

Scores range from 0-100:

| Score | Status | Meaning |
|-------|--------|---------|
| 95-100 | ✓ Excellent | Near-perfect compliance |
| 90-94 | ✓ Good | Minor violations, easy to fix |
| 80-89 | Acceptable | Some violations, needs attention |
| 70-79 | ⚠ Poor | Many violations, requires cleanup |
| < 70 | ✗ Critical | Significant compliance issues |

#### Example output

```
PROJECT SCORE: 87.3 (Acceptable)

Violations by Rule:
  Rule 1 (Semantic Headings)    12 violations in  8 files
  Rule 2 (Block Separation)      5 violations in  3 files
  Rule 4 (Nested Code Blocks)    1 violation  in  1 file
```

### Exit Codes

- `0` - Success (no violations or score ≥ threshold)
- `1` - Violations found or score < threshold
- `2` - Error (file not found, invalid arguments)

Use exit codes in scripts:

```bash
if check-md kb/ --min-score 80; then
    echo "Markdown quality is good"
else
    echo "Please fix violations"
fi
```

## Fixing Common Violations

### Rule 1: Semantic Headings

#### Problem

Bold text used for structure

❌ **Wrong:**

```markdown
**Goals:**
- Goal 1
- Goal 2
```

✅ **Correct:**

```markdown
#### Goals

- Goal 1
- Goal 2
```

#### Auto-fix

```bash
check-md file.md --fix
```

Converts standalone bold to level-4 headers automatically.

### Rule 2: Block Separation

#### Problem

Block elements missing blank lines

❌ **Wrong:**

<!-- check-md-ignore-next -->
```markdown
Here's an example:
```python
code()

```
```

✅ **Correct:**

<!-- check-md-ignore-next -->
```markdown
Here's an example:

```python
code()

```
```

#### Auto-fix

```bash
check-md file.md --fix
```

Inserts blank lines before block elements automatically.

### Rule 4: Nested Code Blocks

#### Problem

Insufficient fence length for nesting

❌ **Wrong:**

<!-- check-md-ignore-begin -->
````markdown
```markdown
Example:
```bash
command
```
```
````
<!-- check-md-ignore-end -->

✅ **Correct:**

<!-- check-md-ignore-begin -->
`````markdown
````markdown
Example:
```bash
command
```
````
`````
<!-- check-md-ignore-end -->

#### Auto-fix

```bash
check-md file.md --fix
```

Increases outer fence length to 4 backticks automatically.

## AI Assistant Workflow

### Recommended Pattern

AI assistants should check markdown before presenting to users:

1. Create/edit file
2. Run check-md with auto-fix:

```bash
check-md file.md --fix --quiet
```

3. If exit code 0, present file
4. If exit code 1, review remaining violations

This catches 90%+ of violations automatically.

### Integration in CLAUDE.md

The project's CLAUDE.md includes:

- Prominent "⚠️ CRITICAL: ADR leap-adr-002 Compliance" section
- Quick check workflow
- Common violations with examples
- Tool usage commands
- Ignore comment reference

AI assistants should follow this workflow for all markdown files.

### Performance Considerations

check-md is optimized for AI workflows:

- **Target**: < 100ms per file
- **Actual**: Typically 10-50ms for average files
- **Parallel**: Checks multiple files efficiently

Fast enough to run before every file presentation.

## Handling False Positives

### Use Ignore Comments

When violations are intentional:

```markdown
<!-- check-md-ignore -->
**Intentional bold:** for emphasis, not structure

<!-- check-md-ignore-next -->
**Next line:** also intentional

<!-- check-md-ignore-begin -->
**Multiple lines**
**All intentional**
<!-- check-md-ignore-end -->
```

### Configure Rules

Disable specific rules via `.check-md.yml`:

```yaml
rules:
  rule_1:
    enabled: false  # Disable semantic headings check
  rule_2:
    enabled: true
    severity: warning  # Make it a warning instead of error
  rule_4:
    enabled: true
```

### Exclude Files

Exclude generated or external files:

```yaml
exclude:
  - "node_modules/**"
  - "build/**"
  - "*.generated.md"
  - "vendor/**"
```

## Team Adoption Strategies

### Gradual Rollout

1. **Phase 1: Documentation**
   - Share README and this guide
   - Demonstrate tool in team meeting
   - Answer questions

2. **Phase 2: Optional Usage**
   - Make tool available for voluntary use
   - Fix violations in new files only
   - Collect feedback

3. **Phase 3: CI/CD Integration**
   - Add check-md to CI pipeline
   - Set low threshold initially (e.g., 70)
   - Gradually increase threshold

4. **Phase 4: Pre-commit Hooks**
   - Provide opt-in pre-commit hook
   - Make mandatory after team is comfortable
   - Support users encountering issues

### Communication

#### Initial Announcement

```
We've added check-md to enforce ADR leap-adr-002 markdown standards.

What it does:
- Detects 3 common markdown issues
- Auto-fixes 90%+ of violations
- Fast: < 100ms per file

Getting started:
1. cd leap/check-md && pip install -e .
2. check-md kb/your-feature/ --fix
3. See leap/check-md/README.md for details

Questions? Ask in #dev-tools
```

#### Ongoing Support

- Add to onboarding checklist
- Include in documentation guidelines
- Reference in PR templates
- Provide troubleshooting channel

### Measuring Success

Track these metrics:

1. **Violation Rate**: Total violations per 1000 lines
2. **Compliance Score**: Average project score over time
3. **Adoption Rate**: % of PRs that pass check-md
4. **Fix Rate**: % of violations fixed automatically

#### Updating Baseline Metrics

To update the project baseline metrics:

```bash
./scripts/check-md-update-baseline
```

#### When to update

- Before creating `completion-summary.md` for a feature branch
- After bulk cleanup of markdown violations
- Before major releases/milestones
- Anytime you want to see current project status

The script generates `kb/meta/metrics-markdown-quality-baseline.txt` which tracks progress over time through git diffs.

#### Example dashboard

```
Week 1: Score 72 → Week 4: Score 85 → Week 8: Score 92
Violations: 127 → 45 → 12
Auto-fix rate: 89% → 93% → 95%
```

## Troubleshooting

### "check-md: command not found"

Install check-md:

```bash
cd check-md
```

```bash
pip install -e .
```

Verify installation:

```bash
check-md --version
```

### Hook not executing

Ensure executable:

```bash
chmod +x .git/hooks/pre-commit
```

Test manually:

```bash
.git/hooks/pre-commit
```

### Too many false positives

Use ignore comments for specific lines:

```markdown
<!-- check-md-ignore -->
**Intentional:** violation
```

Or disable rule in `.check-md.yml`:

```yaml
rules:
  rule_1:
    enabled: false
```

### Performance issues

Check specific directories only:

```bash
check-md kb/feature/ --exclude "build/**"
```

Use --quiet for faster output:

```bash
check-md kb/ --quiet
```

Profile with verbose mode:

```bash
check-md kb/ --verbose
```

### Backup files accumulating

Clean backups after verification:

```bash
check-md kb/ --clean-backups
```

Auto-clean when fixing:

```bash
check-md kb/ --fix --clean-backups
```

Rollback if needed:

```bash
check-md kb/ --rollback
```

## Advanced Usage

### Custom Workflows

#### Pre-commit with auto-fix

```bash
#!/bin/sh
check-md --staged --fix --quiet
if [ $? -ne 0 ]; then
    echo "Some violations couldn't be auto-fixed"
    check-md --staged
    exit 1
fi
git add -u  # Stage fixes
```

#### CI with score trending

```yaml
- name: Check markdown and save score
  run: |
    SCORE=$(check-md kb/ --format json | jq '.project_score')
    echo "score=$SCORE" >> $GITHUB_OUTPUT

- name: Compare with baseline
  run: |
    if [ "${{ steps.check.outputs.score }}" -lt 80 ]; then
      echo "Score below threshold!"
      exit 1
    fi
```

#### Batch fixing

Fix all features:

```bash
for dir in kb/feature/*/; do
    echo "Fixing $dir"
    check-md "$dir" --fix --quiet
done
```

Clean all backups after verification:

```bash
check-md kb/ --clean-backups
```

### Integration with Other Tools

#### With markdownlint

Run both tools:

```bash
check-md kb/ && markdownlint kb/
```

Combine reports:

```bash
check-md kb/ --format json > check-md-report.json
```

```bash
markdownlint kb/ --json > markdownlint-report.json
```

#### With CI status checks

```yaml
# GitHub Actions
- name: Markdown Quality Gate
  run: |
    check-md kb/ docs/ --min-score 85
  continue-on-error: false
```

## Related Documentation

- [ADR leap-adr-002: Markdown Formatting Standards](../adr/leap-adr-002__markdown-formatting-standards.md)
- [Onboarding Guide](guide-markdown-quality-onboarding.md)
- [Baseline Metrics](metrics-markdown-quality-baseline.txt) - Current project status
- [check-md README](../../leap/check-md/README.md)
- [Integration Templates](../../leap/check-md/templates/README.md)
- [CLAUDE.md ADR leap-adr-002 Section](../../CLAUDE.md#️-critical-adr-002-markdown-compliance)

## Summary

### Key Takeaways

1. ✅ Run `check-md --fix` before committing markdown
2. ✅ Install pre-commit hook for automatic checking
3. ✅ Use ignore comments for intentional violations
4. ✅ Configure `.check-md.yml` for project needs
5. ✅ Integrate into CI/CD for team enforcement

#### Quick Commands

Check and fix:

```bash
check-md file.md --fix
```

Before commit:

```bash
check-md --staged
```

Project score:

```bash
check-md kb/ --min-score 80
```

CI/CD:

```bash
check-md kb/ --format github --min-score 85
```

Maintaining markdown quality ensures documentation is readable, consistent, and professional across the entire project.
