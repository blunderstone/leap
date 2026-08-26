"""
cli.py — Command-line interface for check-md.

Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)

Copyright 2026 Blunderstone LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import json
import subprocess
from pathlib import Path
from typing import List, Literal, Optional

import pathspec
import typer

from .checker import MarkdownChecker
from .config import CheckMdConfig
from .fixer import FileFixer
from .formatting import format_rule_id_for_display, format_violation_display
from .models import FileResult
from .scorer import calculate_project_score, format_score_indicator

app = typer.Typer(
    name="check-md",
    help="Check Markdown files for LEAP ADR 002 formatting compliance",
    add_completion=False,
)


def find_config_file() -> Optional[Path]:
    """Find .check-md.yml config file starting from current directory.

    Searches upward through directory tree until finding config or reaching root.

    Returns:
        Path to config file or None if not found
    """
    current = Path.cwd().resolve()

    while True:
        config_path = current / ".check-md.yml"
        if config_path.exists():
            return config_path

        parent = current.parent
        if parent == current:  # Reached root
            break
        current = parent

    return None


def load_config() -> Optional[CheckMdConfig]:
    """Load configuration from .check-md.yml if it exists.

    Returns:
        CheckMdConfig object or None if no config file found
    """
    config_path = find_config_file()
    if config_path:
        try:
            return CheckMdConfig.load(config_path)
        except Exception as e:
            typer.echo(f"Warning: Failed to load config from {config_path}: {e}", err=True)
            return None
    return None


def find_markdown_files(
    paths: List[str],
    include: Optional[str],
    exclude: Optional[List[str]],
    exclude_patterns: Optional[List[str]] = None,
) -> List[Path]:
    """Find all Markdown files from given paths.

    Args:
        paths: List of file/directory paths or glob patterns
        include: Optional glob pattern to include
        exclude: Optional list of glob patterns to exclude (CLI)
        exclude_patterns: Optional list of glob patterns to exclude (from config)

    Returns:
        List of Path objects for Markdown files
    """
    found_files: set[Path] = set()

    for path_str in paths:
        path = Path(path_str)

        if path.is_file():
            if path.suffix.lower() == ".md":
                found_files.add(path)
        elif path.is_dir():
            # Recursively find all .md files
            found_files.update(path.rglob("*.md"))
        else:
            # Try as glob pattern
            found_files.update(Path(".").glob(path_str))

    # Apply include/exclude filters using gitignore-style glob patterns
    # Convert to relative paths for pattern matching when possible
    cwd = Path.cwd()
    filtered_files = found_files

    def get_match_path(f: Path) -> str:
        """Get path string for pattern matching."""
        try:
            # Try to get relative path from cwd
            return str(f.relative_to(cwd))
        except ValueError:
            # Not relative to cwd, use absolute path
            return str(f)

    if include:
        # Use pathspec for proper gitignore-style ** matching
        spec = pathspec.PathSpec.from_lines('gitignore', [include])
        filtered_files = {
            f for f in filtered_files
            if spec.match_file(get_match_path(f))
        }

    # Apply CLI exclude patterns
    if exclude:
        # Use pathspec for proper gitignore-style ** matching
        spec = pathspec.PathSpec.from_lines('gitignore', exclude)
        filtered_files = {
            f for f in filtered_files
            if not spec.match_file(get_match_path(f))
        }

    # Apply config exclude patterns
    if exclude_patterns:
        # Use pathspec for proper gitignore-style ** matching
        spec = pathspec.PathSpec.from_lines('gitignore', exclude_patterns)
        filtered_files = {
            f for f in filtered_files
            if not spec.match_file(get_match_path(f))
        }

    return sorted(filtered_files)


def get_staged_files() -> List[Path]:
    """Get list of staged Markdown files from git.

    Returns:
        List of Path objects for staged .md files

    Raises:
        RuntimeError: If git command fails
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True,
        )
        files = [
            Path(f.strip())
            for f in result.stdout.strip().split("\n")
            if f.strip() and f.strip().endswith(".md")
        ]
        return files
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to get staged files: {e}") from e


### OUTPUT FORMATTERS ###
# All formatters below should follow the convention: "message [Rule N]"
# To change violation formatting, search for: "OUTPUT FORMATTERS"
# See format_violation_display() for the shared formatting logic

def format_text_output(results: List[FileResult], verbose: bool) -> str:
    """Format results as human-readable text with colors.

    Uses Typer's color functions which automatically respect NO_COLOR.

    Args:
        results: List of FileResult objects
        verbose: Show detailed context

    Returns:
        Formatted text output
    """
    output_lines: List[str] = []

    for result in results:
        if not result.violations:
            continue

        # File path in bold
        output_lines.append(f"\n{typer.style(result.file_path, bold=True)}")

        for violation in result.violations:
            # Format: file.md:42: message [Rule 1]
            formatted = format_violation_display(violation)
            severity_color = typer.colors.RED if violation.severity.value == "error" else typer.colors.YELLOW
            styled = typer.style(formatted, fg=severity_color)

            output_lines.append(
                f"  {result.file_path}:{violation.line_number}: {styled}"
            )

            if verbose:
                # Show context with line numbers
                output_lines.append(f"    Context: {violation.context}")
                if violation.fix_hint:
                    fix_text = typer.style(violation.fix_hint, fg=typer.colors.GREEN)
                    output_lines.append(f"    Fix: {fix_text}")

    return "\n".join(output_lines)


def format_json_output(results: List[FileResult]) -> str:
    """Format results as JSON.

    Args:
        results: List of FileResult objects

    Returns:
        JSON string
    """
    output = []
    for result in results:
        for violation in result.violations:
            rule_display = format_rule_id_for_display(violation.rule_id)
            output.append(
                {
                    "file": result.file_path,
                    "line": violation.line_number,
                    "rule": rule_display,
                    "severity": violation.severity.value,
                    "message": violation.message,
                    "context": violation.context,
                    "fix_hint": violation.fix_hint,
                }
            )
    return json.dumps(output, indent=2)


def format_github_output(results: List[FileResult]) -> str:
    """Format results as GitHub Actions annotations.

    Args:
        results: List of FileResult objects

    Returns:
        GitHub Actions annotation commands
    """
    output_lines: List[str] = []
    for result in results:
        for violation in result.violations:
            # GitHub Actions annotation format: title=message::[Rule N]
            level = "error" if violation.severity.value == "error" else "warning"
            formatted = format_violation_display(violation, separator="::")
            output_lines.append(
                f"::{level} file={result.file_path},line={violation.line_number},"
                f"title={formatted}"
            )
    return "\n".join(output_lines)


def format_score_report(
    results: List[FileResult], sort_by: Literal["score", "name", "violations"]
) -> str:
    """Format compliance score report with summary table.

    Args:
        results: List of FileResult objects
        sort_by: How to sort the results (score, name, violations)

    Returns:
        Formatted score report with table
    """
    if not results:
        return "No files to score"

    # Calculate project score
    project = calculate_project_score(results)

    output_lines: List[str] = []

    # Header
    output_lines.append("\n" + "=" * 80)
    output_lines.append("MARKDOWN FORMATTING COMPLIANCE REPORT")
    output_lines.append("=" * 80)

    # Overall project score
    indicator = format_score_indicator(project.score)
    score_text = typer.style(f"{project.score:.1f}%", bold=True)
    output_lines.append(f"\nOverall Project Score: {indicator} {score_text}")
    output_lines.append(f"  Files Checked: {project.total_files}")
    output_lines.append(f"  Total Lines: {project.total_lines}")
    output_lines.append(f"  Total Violations: {project.total_violations}")

    # Violations by rule
    if project.violations_by_rule:
        output_lines.append("\nViolations by Rule:")
        for rule_id in sorted(project.violations_by_rule.keys()):
            count = project.violations_by_rule[rule_id]
            rule_display = format_rule_id_for_display(rule_id)
            output_lines.append(f"  {rule_display}: {count}")

    # Sort module scores
    sorted_modules = project.module_scores
    if sort_by == "score":
        sorted_modules = sorted(sorted_modules, key=lambda m: m.score)
    elif sort_by == "name":
        sorted_modules = sorted(sorted_modules, key=lambda m: m.module_path)
    elif sort_by == "violations":
        sorted_modules = sorted(sorted_modules, key=lambda m: m.violation_count, reverse=True)

    # Module summary table
    output_lines.append("\n" + "-" * 80)
    output_lines.append("MODULE SUMMARY")
    output_lines.append("-" * 80)
    output_lines.append(f"{'':1} {'Score':>6}  {'Files':>5}  {'Viol':>5}  {'Path'}")
    output_lines.append("-" * 80)

    for module in sorted_modules:
        indicator = format_score_indicator(module.score)
        score_str = f"{module.score:.1f}%"
        output_lines.append(
            f"{indicator} {score_str:>6}  {module.file_count:>5}  "
            f"{module.violation_count:>5}  {module.module_path}"
        )

    # File details (sorted)
    output_lines.append("\n" + "-" * 80)
    output_lines.append("FILE DETAILS")
    output_lines.append("-" * 80)
    output_lines.append(f"{'':1} {'Score':>6}  {'Lines':>5}  {'Viol':>5}  {'Path'}")
    output_lines.append("-" * 80)

    # Collect all file scores
    all_file_scores = []
    for module in project.module_scores:
        all_file_scores.extend(module.file_scores)

    # Sort file scores
    if sort_by == "score":
        all_file_scores = sorted(all_file_scores, key=lambda f: f.score)
    elif sort_by == "name":
        all_file_scores = sorted(all_file_scores, key=lambda f: f.file_path)
    elif sort_by == "violations":
        all_file_scores = sorted(
            all_file_scores, key=lambda f: len(f.violations), reverse=True
        )

    for file_score in all_file_scores:
        indicator = format_score_indicator(file_score.score)
        score_str = f"{file_score.score:.1f}%"
        viol_count = len(file_score.violations)
        output_lines.append(
            f"{indicator} {score_str:>6}  {file_score.total_lines:>5}  "
            f"{viol_count:>5}  {file_score.file_path}"
        )

    # Legend
    output_lines.append("\n" + "=" * 80)
    output_lines.append("Legend: ✓ = Excellent (95%+)  [space] = Good (80-94%)  ")
    output_lines.append("        ⚠ = Needs Work (70-79%)  ✗ = Poor (<70%)")
    output_lines.append("=" * 80)

    return "\n".join(output_lines)


@app.command()
def main(
    files: Optional[List[str]] = typer.Argument(
        None,
        help="Files or directories to check (default: current directory)",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Only show violations, no summary",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed context for violations",
    ),
    include: Optional[str] = typer.Option(
        None,
        "--include",
        help="Include files matching pattern (glob)",
    ),
    exclude: Optional[List[str]] = typer.Option(
        None,
        "--exclude",
        help="Exclude files matching pattern (glob), can be specified multiple times",
    ),
    staged: bool = typer.Option(
        False,
        "--staged",
        help="Check only git-staged Markdown files",
    ),
    format: Literal["text", "json", "github"] = typer.Option(
        "text",
        "--format",
        help="Output format",
    ),
    report: bool = typer.Option(
        False,
        "--report",
        help="Show compliance score report with summary tables",
    ),
    sort_by: Literal["score", "name", "violations"] = typer.Option(
        "name",
        "--sort",
        help="Sort order for score report (requires --report)",
    ),
    min_score: float = typer.Option(
        80.0,
        "--min-score",
        help="Minimum acceptable score (exit code 1 if below)",
    ),
    fix: bool = typer.Option(
        False,
        "--fix",
        help="Shorthand for --fix-strategy conservative",
    ),
    fix_strategy: Optional[str] = typer.Option(
        None,
        "--fix-strategy",
        help="Fix strategy: conservative (insert TODOs for cascades), aggressive (apply all fixes including cascades), none (check only)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview fixes without modifying files (requires --fix)",
    ),
    rollback: bool = typer.Option(
        False,
        "--rollback",
        help="Restore files from .bak backups and remove backups",
    ),
    clean_backups: bool = typer.Option(
        False,
        "--clean-backups",
        help="Remove .bak files for checked files only (verifies no violations unless --force). To clean all backups project-wide: find . -name '*.bak' -delete",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Force cleanup of backups without verification (use with --clean-backups)",
    ),
) -> None:
    """Check Markdown files for LEAP ADR 002 formatting compliance.

    Examples:

      check-md file.md              # Check single file

      check-md kb/                  # Check directory recursively

      check-md 'kb/**/*.md'         # Check with glob pattern

      check-md --staged             # Check git-staged files

    Exit codes:

      0: No violations found

      1: Violations found

      2: Error occurred
    """
    try:
        # Load configuration if available
        config = load_config()
        exclude_patterns = config.exclude if config else None

        # Determine which files to check
        if staged:
            file_list = get_staged_files()
            if not file_list:
                typer.echo("No staged Markdown files found", err=True)
                raise typer.Exit(code=0)
        elif files:
            file_list = find_markdown_files(files, include, exclude, exclude_patterns)
        else:
            # Default: current directory
            file_list = find_markdown_files(["."], include, exclude, exclude_patterns)

        if not file_list:
            typer.echo("No Markdown files found", err=True)
            raise typer.Exit(code=2)

        # Handle rollback operation
        if rollback:
            from check_md.rules import FixStrategy
            fixer = FileFixer(strategy=FixStrategy.NONE)  # Strategy doesn't matter for rollback
            rollback_count = 0
            for file_path in file_list:
                if fixer.has_backup(file_path):
                    if fixer.rollback_file(file_path):
                        rollback_count += 1
                        if not quiet:
                            typer.echo(f"Rolled back {file_path}")

            if rollback_count == 0:
                typer.echo("No backup files found to rollback", err=True)
                raise typer.Exit(code=2)
            else:
                typer.secho(f"\n✓ Rolled back {rollback_count} files", fg=typer.colors.GREEN)
                raise typer.Exit(code=0)

        # Handle clean-backups operation (without fix)
        if clean_backups and not fix:
            from check_md.rules import FixStrategy
            checker = MarkdownChecker()
            fixer = FileFixer(strategy=FixStrategy.NONE)  # Strategy doesn't matter for cleanup
            cleaned_count = 0
            skipped_count = 0

            for file_path in file_list:
                if not fixer.has_backup(file_path):
                    continue

                # Verify file has no violations unless --force
                if not force:
                    result = checker.check_file(file_path)
                    if result.violations:
                        skipped_count += 1
                        if not quiet:
                            typer.secho(
                                f"Skipped {file_path}: {len(result.violations)} violations remain",
                                fg=typer.colors.YELLOW
                            )
                        continue

                # Clean backup
                if fixer.clean_backup(file_path):
                    cleaned_count += 1
                    if not quiet:
                        typer.echo(f"Cleaned backup for {file_path}")

            if cleaned_count == 0 and skipped_count == 0:
                typer.echo("No backup files found to clean", err=True)
                raise typer.Exit(code=2)
            else:
                if cleaned_count > 0:
                    typer.secho(f"\n✓ Cleaned {cleaned_count} backup files", fg=typer.colors.GREEN)
                if skipped_count > 0:
                    typer.secho(f"⚠ Skipped {skipped_count} files with violations", fg=typer.colors.YELLOW)
                raise typer.Exit(code=0 if skipped_count == 0 else 1)

        # Check all files
        checker = MarkdownChecker()
        results = checker.check_files(file_list)

        # Determine fix strategy
        from check_md.rules import FixStrategy

        # Parse fix strategy
        if fix_strategy is not None:
            # --fix-strategy overrides --fix
            if fix_strategy == "none":
                strategy = FixStrategy.NONE
            elif fix_strategy == "conservative":
                strategy = FixStrategy.CONSERVATIVE
            elif fix_strategy == "aggressive":
                strategy = FixStrategy.AGGRESSIVE
            else:
                typer.secho(
                    f"Error: Invalid fix strategy '{fix_strategy}'. Use 'none', 'conservative', or 'aggressive'.",
                    fg=typer.colors.RED,
                    err=True
                )
                raise typer.Exit(code=2)
        elif fix:
            # --fix flag without explicit strategy = conservative
            strategy = FixStrategy.CONSERVATIVE
        else:
            # No fix flags = check only
            strategy = FixStrategy.NONE

        # Apply fixes if requested (but not if strategy is NONE)
        if strategy != FixStrategy.NONE:
            if dry_run:
                # Preview mode: show what would be fixed
                fixer = FileFixer(strategy=strategy)
                for result in results:
                    if result.violations:
                        typer.echo(f"\n{typer.style(result.file_path, bold=True)}")
                        previews = fixer.preview_fixes(Path(result.file_path), result)
                        for preview in previews:
                            typer.echo(preview)
                typer.echo(f"\n{len([r for r in results if r.violations])} files would be modified (dry run)")
                raise typer.Exit(code=0)
            else:
                # Actually fix files
                fixer = FileFixer(strategy=strategy)
                total_fixed = 0
                for result in results:
                    if result.violations:
                        fixed_count = fixer.fix_file(Path(result.file_path), result, create_backup=True)
                        total_fixed += fixed_count
                        if not quiet:
                            typer.echo(f"Fixed {fixed_count} violations in {result.file_path}")

                if not quiet:
                    typer.secho(f"\n✓ Fixed {total_fixed} violations", fg=typer.colors.GREEN)

                # Re-check files to see if any violations remain
                results = checker.check_files(file_list)

                # Auto-clean backups if requested and files are clean
                if clean_backups:
                    cleaned_count = 0
                    for result in results:
                        if not result.violations:  # File is clean
                            if fixer.clean_backup(Path(result.file_path)):
                                cleaned_count += 1
                                if not quiet:
                                    typer.echo(f"Cleaned backup for {result.file_path}")

                    if cleaned_count > 0 and not quiet:
                        typer.secho(f"✓ Cleaned {cleaned_count} backup files", fg=typer.colors.GREEN)

        # Calculate totals
        total_violations = sum(len(r.violations) for r in results)
        total_errors = sum(r.error_count for r in results)
        total_warnings = sum(r.warning_count for r in results)
        files_with_violations = sum(1 for r in results if r.violations)

        # Show score report if requested
        if report:
            score_output = format_score_report(results, sort_by)
            typer.echo(score_output)

            # Check minimum score threshold
            project = calculate_project_score(results)
            if project.score < min_score:
                typer.secho(
                    f"\n✗ Score {project.score:.1f}% below minimum threshold of {min_score:.1f}%",
                    fg=typer.colors.RED,
                    err=True,
                )
                raise typer.Exit(code=1)
            else:
                typer.secho(
                    f"\n✓ Score {project.score:.1f}% meets minimum threshold of {min_score:.1f}%",
                    fg=typer.colors.GREEN,
                )
                raise typer.Exit(code=0)

        # Format output (non-report mode)
        if format == "json":
            output = format_json_output(results)
            typer.echo(output)
        elif format == "github":
            output = format_github_output(results)
            typer.echo(output)
        else:  # text
            output = format_text_output(results, verbose)
            if output:
                typer.echo(output)

            # Print summary unless --quiet
            if not quiet:
                typer.echo(f"\n{len(file_list)} files checked")
                if total_violations > 0:
                    typer.echo(
                        f"{total_violations} violations in {files_with_violations} files "
                        f"({total_errors} errors, {total_warnings} warnings)"
                    )
                else:
                    typer.secho("✓ No violations found", fg=typer.colors.GREEN)

        # Exit with appropriate code
        if total_violations > 0:
            raise typer.Exit(code=1)
        else:
            raise typer.Exit(code=0)

    except typer.Exit:
        # Re-raise typer exits (clean exit with code)
        raise
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=2)


if __name__ == "__main__":
    app()
