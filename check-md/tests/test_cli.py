"""
test_cli.py — Tests for CLI functionality.

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
from typing import List

import pytest
from typer.testing import CliRunner

from check_md.cli import (
    app,
    find_markdown_files,
    format_github_output,
    format_json_output,
    format_text_output,
)
from check_md.formatting import format_rule_id_for_display
from check_md.models import FileResult, Severity, Violation

runner = CliRunner()


class TestFindMarkdownFiles:
    """Test markdown file discovery."""

    def test_finds_single_file(self, tmp_path: Path) -> None:
        """Should find a single markdown file."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test")

        files = find_markdown_files([str(md_file)], None, None)

        assert len(files) == 1
        assert files[0] == md_file

    def test_finds_directory_recursively(self, tmp_path: Path) -> None:
        """Should find all markdown files in directory recursively."""
        (tmp_path / "file1.md").write_text("# File 1")
        (tmp_path / "file2.md").write_text("# File 2")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file3.md").write_text("# File 3")
        (tmp_path / "other.txt").write_text("Not markdown")

        files = find_markdown_files([str(tmp_path)], None, None)

        assert len(files) == 3
        assert all(f.suffix == ".md" for f in files)

    def test_applies_include_filter(self, tmp_path: Path) -> None:
        """Should include only files matching pattern."""
        (tmp_path / "feature1.md").write_text("# Feature 1")
        (tmp_path / "feature2.md").write_text("# Feature 2")
        (tmp_path / "other.md").write_text("# Other")

        files = find_markdown_files([str(tmp_path)], "**/feature*.md", None)

        assert len(files) == 2
        assert all("feature" in f.name for f in files)

    def test_applies_exclude_filter(self, tmp_path: Path) -> None:
        """Should exclude files matching pattern."""
        (tmp_path / "keep1.md").write_text("# Keep 1")
        (tmp_path / "keep2.md").write_text("# Keep 2")
        (tmp_path / "skip.md").write_text("# Skip")

        files = find_markdown_files([str(tmp_path)], None, ["**/skip.md"])

        assert len(files) == 2
        assert all("skip" not in f.name for f in files)

    def test_applies_multiple_exclude_patterns(self, tmp_path: Path) -> None:
        """Should exclude files matching multiple distinct patterns via CLI."""
        # Create structure with two different exclusion areas
        (tmp_path / "keep.md").write_text("# Keep")

        # Feature dir to exclude
        feature_dir = tmp_path / "kb" / "feature" / "test"
        feature_dir.mkdir(parents=True)
        (feature_dir / "goals.md").write_text("# Goals")

        # Build dir to exclude (different pattern)
        build_dir = tmp_path / "build"
        build_dir.mkdir()
        (build_dir / "generated.md").write_text("# Generated")

        # Both should be excluded when passing multiple --exclude patterns
        files = find_markdown_files(
            [str(tmp_path)],
            None,
            ["**/kb/feature/**", "**/build/**"]
        )

        assert len(files) == 1
        assert files[0].name == "keep.md"

    def test_doublestar_pattern_matches_at_any_depth(self, tmp_path: Path) -> None:
        """Should support gitignore-style ** patterns that match at any depth."""
        # Create nested structure
        (tmp_path / "keep.md").write_text("# Keep")

        # Top-level feature dir
        feature_dir = tmp_path / "kb" / "feature" / "test"
        feature_dir.mkdir(parents=True)
        (feature_dir / "goals.md").write_text("# Goals")

        # Module-level feature dir (one level deep)
        module_feature_dir = tmp_path / "mymodule" / "kb" / "feature" / "test"
        module_feature_dir.mkdir(parents=True)
        (module_feature_dir / "plan.md").write_text("# Plan")

        # Deeper nested feature dir (two levels deep)
        deep_feature_dir = tmp_path / "some" / "deep" / "kb" / "feature" / "test"
        deep_feature_dir.mkdir(parents=True)
        (deep_feature_dir / "notes.md").write_text("# Notes")

        # Single pattern **/kb/feature/** should match at ANY depth (including zero)
        files = find_markdown_files(
            [str(tmp_path)],
            None,
            ["**/kb/feature/**"]
        )

        assert len(files) == 1
        assert files[0].name == "keep.md"

    def test_handles_glob_pattern(self, tmp_path: Path) -> None:
        """Should handle glob patterns."""
        (tmp_path / "test1.md").write_text("# Test 1")
        (tmp_path / "test2.md").write_text("# Test 2")
        (tmp_path / "other.md").write_text("# Other")

        # Use relative glob pattern from tmp_path
        import os
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            files = find_markdown_files(["test*.md"], None, None)
            assert len(files) == 2
        finally:
            os.chdir(old_cwd)


class TestFormatJsonOutput:
    """Test JSON output formatting."""

    def test_formats_single_violation(self) -> None:
        """Should format single violation as JSON."""
        violation = Violation(
            rule_id="TEST-R1",
            line_number=42,
            severity=Severity.ERROR,
            message="Test message",
            context="Test context",
            fix_hint="Test fix",
        )
        result = FileResult(
            file_path="test.md",
            violations=[violation],
            total_lines=100,
        )

        output = format_json_output([result])
        data = json.loads(output)

        assert len(data) == 1
        assert data[0]["file"] == "test.md"
        assert data[0]["line"] == 42
        assert data[0]["rule"] == "Rule 1"
        assert data[0]["severity"] == "error"
        assert data[0]["message"] == "Test message"

    def test_formats_multiple_violations(self) -> None:
        """Should format multiple violations as JSON array."""
        violations = [
            Violation("R1", 1, Severity.ERROR, "Msg 1", "Ctx 1", "Fix 1"),
            Violation("R2", 2, Severity.WARNING, "Msg 2", "Ctx 2", "Fix 2"),
        ]
        result = FileResult("test.md", violations, 100)

        output = format_json_output([result])
        data = json.loads(output)

        assert len(data) == 2
        assert data[0]["rule"] == "Rule 1"
        assert data[1]["rule"] == "Rule 2"

    def test_formats_empty_results(self) -> None:
        """Should format empty results as empty JSON array."""
        output = format_json_output([])
        data = json.loads(output)

        assert data == []


class TestFormatRuleId:
    """Test rule ID formatting for user-friendly display."""

    def test_formats_adr_002_r1(self) -> None:
        """Should format ADR-002-R1 as Rule 1."""
        result = format_rule_id_for_display("ADR-002-R1")
        assert result == "Rule 1"

    def test_formats_adr_002_r2(self) -> None:
        """Should format ADR-002-R2 as Rule 2."""
        result = format_rule_id_for_display("ADR-002-R2")
        assert result == "Rule 2"

    def test_formats_adr_002_r3(self) -> None:
        """Should format ADR-002-R3 as Rule 3."""
        result = format_rule_id_for_display("ADR-002-R3")
        assert result == "Rule 3"

    def test_formats_adr_002_r4(self) -> None:
        """Should format ADR-002-R4 as Rule 4."""
        result = format_rule_id_for_display("ADR-002-R4")
        assert result == "Rule 4"

    def test_formats_adr_002_r5(self) -> None:
        """Should format ADR-002-R5 as Rule 5."""
        result = format_rule_id_for_display("ADR-002-R5")
        assert result == "Rule 5"

    def test_formats_simple_r1(self) -> None:
        """Should format R1 as Rule 1."""
        result = format_rule_id_for_display("R1")
        assert result == "Rule 1"

    def test_formats_simple_r10(self) -> None:
        """Should format R10 as Rule 10."""
        result = format_rule_id_for_display("R10")
        assert result == "Rule 10"

    def test_preserves_unknown_format(self) -> None:
        """Should preserve unknown rule ID formats."""
        result = format_rule_id_for_display("CUSTOM-RULE")
        assert result == "CUSTOM-RULE"

    def test_preserves_format_without_r_suffix(self) -> None:
        """Should preserve formats without R suffix."""
        result = format_rule_id_for_display("ADR-002-X1")
        assert result == "ADR-002-X1"


class TestJsonOutputUsesFormattedRuleIds:
    """Test that JSON output uses user-friendly rule IDs."""

    def test_json_uses_rule_1_not_adr_002_r1(self) -> None:
        """JSON output should use 'Rule 1', not 'ADR-002-R1'."""
        violation = Violation(
            "ADR-002-R1", 1, Severity.ERROR, "Test message", "context", None
        )
        result = FileResult("test.md", [violation], 10)

        output = format_json_output([result])
        data = json.loads(output)

        assert len(data) == 1
        assert data[0]["rule"] == "Rule 1", \
            f"Expected 'Rule 1' but got '{data[0]['rule']}'"

    def test_json_formats_all_rule_ids(self) -> None:
        """JSON output should format all rule IDs consistently."""
        violations = [
            Violation("ADR-002-R1", 1, Severity.ERROR, "Msg 1", "ctx", None),
            Violation("ADR-002-R2", 2, Severity.ERROR, "Msg 2", "ctx", None),
            Violation("ADR-002-R3", 3, Severity.ERROR, "Msg 3", "ctx", None),
            Violation("ADR-002-R4", 4, Severity.ERROR, "Msg 4", "ctx", None),
            Violation("ADR-002-R5", 5, Severity.ERROR, "Msg 5", "ctx", None),
        ]
        result = FileResult("test.md", violations, 10)

        output = format_json_output([result])
        data = json.loads(output)

        assert data[0]["rule"] == "Rule 1"
        assert data[1]["rule"] == "Rule 2"
        assert data[2]["rule"] == "Rule 3"
        assert data[3]["rule"] == "Rule 4"
        assert data[4]["rule"] == "Rule 5"


class TestGithubOutputUsesFormattedRuleIds:
    """Test that GitHub Actions output uses user-friendly rule IDs."""

    def test_github_uses_rule_1_not_adr_002_r1(self) -> None:
        """GitHub output should use 'Rule 1', not 'ADR-002-R1'."""
        violation = Violation(
            "ADR-002-R1", 1, Severity.ERROR, "Test message", "context", None
        )
        result = FileResult("test.md", [violation], 10)

        output = format_github_output([result])

        assert "[Rule 1]" in output, \
            f"Expected '[Rule 1]' in output but got: {output}"
        assert "[ADR-002-R1]" not in output, \
            f"Should not contain '[ADR-002-R1]' but got: {output}"

    def test_github_formats_all_rule_ids(self) -> None:
        """GitHub output should format all rule IDs consistently."""
        violations = [
            Violation("ADR-002-R1", 1, Severity.ERROR, "Msg 1", "ctx", None),
            Violation("ADR-002-R2", 2, Severity.ERROR, "Msg 2", "ctx", None),
            Violation("ADR-002-R5", 3, Severity.ERROR, "Msg 5", "ctx", None),
        ]
        result = FileResult("test.md", violations, 10)

        output = format_github_output([result])

        assert "[Rule 1]" in output
        assert "[Rule 2]" in output
        assert "[Rule 5]" in output
        assert "[ADR-002-" not in output


class TestFormatGithubOutput:
    """Test GitHub Actions output formatting."""

    def test_formats_error_annotation(self) -> None:
        """Should format error as GitHub annotation."""
        violation = Violation(
            "TEST-R1", 42, Severity.ERROR, "Test message", "context", None
        )
        result = FileResult("test.md", [violation], 100)

        output = format_github_output([result])

        expected = "::error file=test.md,line=42,title=Test message::[Rule 1]"
        assert output == expected, \
            f"Expected GitHub annotation format.\nExpected: {expected}\nActual: {output}"

    def test_formats_warning_annotation(self) -> None:
        """Should format warning as GitHub annotation."""
        violation = Violation(
            "TEST-R1", 42, Severity.WARNING, "Test message", "context", None
        )
        result = FileResult("test.md", [violation], 100)

        output = format_github_output([result])

        expected = "::warning file=test.md,line=42,title=Test message::[Rule 1]"
        assert output == expected, \
            f"Expected GitHub annotation format.\nExpected: {expected}\nActual: {output}"

    def test_formats_multiple_annotations(self) -> None:
        """Should format multiple violations as separate annotations."""
        violations = [
            Violation("R1", 1, Severity.ERROR, "Msg 1", "Ctx", None),
            Violation("R2", 2, Severity.WARNING, "Msg 2", "Ctx", None),
        ]
        result = FileResult("test.md", violations, 100)

        output = format_github_output([result])

        expected = (
            "::error file=test.md,line=1,title=Msg 1::[Rule 1]\n"
            "::warning file=test.md,line=2,title=Msg 2::[Rule 2]"
        )
        assert output == expected, \
            f"Expected multiple annotations.\nExpected: {expected}\nActual: {output}"


class TestOutputFormatConsistency:
    """Test that all output formats follow consistent conventions."""

    def test_all_formats_use_same_rule_display(self) -> None:
        """All output formats should display rule IDs consistently as 'Rule N'."""
        violation = Violation(
            "ADR-002-R1", 1, Severity.ERROR, "Test message", "context", None
        )
        result = FileResult("test.md", [violation], 10)

        # Text output
        text_output = format_text_output([result], verbose=False)
        assert "Rule 1" in text_output, "Text output should use 'Rule 1'"

        # JSON output
        json_output = format_json_output([result])
        json_data = json.loads(json_output)
        assert json_data[0]["rule"] == "Rule 1", "JSON output should use 'Rule 1'"

        # GitHub output
        github_output = format_github_output([result])
        assert "[Rule 1]" in github_output, "GitHub output should use '[Rule 1]'"

    def test_all_formats_show_message_before_rule(self) -> None:
        """All output formats should show message before rule ID for readability."""
        violation = Violation(
            "ADR-002-R1", 1, Severity.ERROR, "Test message", "context", None
        )
        result = FileResult("test.md", [violation], 10)

        # Text output: message [Rule 1]
        text_output = format_text_output([result], verbose=False)
        assert "Test message" in text_output
        # Rule should appear after message
        msg_pos = text_output.find("Test message")
        rule_pos = text_output.find("[Rule 1]")
        assert msg_pos < rule_pos, "Text: message should come before rule"

        # GitHub output: title=message::[Rule 1]
        github_output = format_github_output([result])
        assert "title=Test message::[Rule 1]" in github_output, \
            "GitHub: message should come before rule in title"


class TestCliBasicUsage:
    """Test basic CLI invocations."""

    def test_shows_help(self) -> None:
        """Should display help with --help."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        assert "Check markdown files" in result.stdout
        assert "--verbose" in result.stdout
        assert "--format" in result.stdout

    def test_checks_single_file(self, tmp_path: Path) -> None:
        """Should check a single markdown file."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\n**Bold heading**\n")

        result = runner.invoke(app, [str(md_file)])

        assert result.exit_code == 1  # Violations found
        assert "Rule 1" in result.stdout
        assert "1 files checked" in result.stdout

    def test_checks_clean_file(self, tmp_path: Path) -> None:
        """Should pass on clean markdown file."""
        md_file = tmp_path / "clean.md"
        md_file.write_text("# Title\n\n## Section\n\nParagraph text.\n")

        result = runner.invoke(app, [str(md_file)])

        assert result.exit_code == 0
        assert "No violations found" in result.stdout

    def test_checks_directory(self, tmp_path: Path) -> None:
        """Should check all markdown files in directory."""
        (tmp_path / "file1.md").write_text("# Clean")
        (tmp_path / "file2.md").write_text("# Test\n\n**Bad**")

        result = runner.invoke(app, [str(tmp_path)])

        assert result.exit_code == 1
        assert "2 files checked" in result.stdout

    def test_quiet_mode_suppresses_summary(self, tmp_path: Path) -> None:
        """Should suppress summary with --quiet."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\n**Bad**\n")

        result = runner.invoke(app, [str(md_file), "--quiet"])

        assert result.exit_code == 1
        assert "files checked" not in result.stdout
        assert "Rule 1" in result.stdout  # Violations still shown

    def test_verbose_mode_shows_context(self, tmp_path: Path) -> None:
        """Should show detailed context with --verbose."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\n**Bad**\n")

        result = runner.invoke(app, [str(md_file), "--verbose"])

        assert result.exit_code == 1
        assert "Context:" in result.stdout
        assert "Fix:" in result.stdout


class TestCliOutputFormats:
    """Test different output format options."""

    def test_json_format(self, tmp_path: Path) -> None:
        """Should output JSON with --format json."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\n**Bad**\n")

        result = runner.invoke(app, [str(md_file), "--format", "json"])

        assert result.exit_code == 1
        data = json.loads(result.stdout)

        # Verify exact JSON structure
        assert isinstance(data, list), "JSON output should be a list"
        assert len(data) == 1, f"Expected 1 violation, got {len(data)}"

        violation = data[0]
        assert set(violation.keys()) == {"file", "line", "rule", "severity", "message", "context", "fix_hint"}, \
            f"JSON keys mismatch. Expected: {{file, line, rule, severity, message, context, fix_hint}}, Got: {set(violation.keys())}"
        assert violation["file"] == str(md_file)
        assert violation["rule"] == "Rule 1"
        assert violation["severity"] == "error"
        assert violation["message"] == "Standalone bold text should be a heading"

    def test_github_format(self, tmp_path: Path) -> None:
        """Should output GitHub annotations with --format github."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n\n**Bad**\n")

        result = runner.invoke(app, [str(md_file), "--format", "github"])

        assert result.exit_code == 1
        assert "::" in result.stdout
        assert "file=" in result.stdout
        assert "line=" in result.stdout


class TestCliErrorHandling:
    """Test CLI error handling."""

    def test_exits_with_error_on_no_files(self, tmp_path: Path) -> None:
        """Should exit with code 2 when no markdown files found."""
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = runner.invoke(app, [str(empty_dir)])

        assert result.exit_code == 2
        # Typer writes errors to stderr
        assert "No markdown files found" in result.stderr or result.exit_code == 2

    def test_handles_invalid_format(self, tmp_path: Path) -> None:
        """Should reject invalid format option."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Test")

        result = runner.invoke(app, [str(md_file), "--format", "invalid"])

        assert result.exit_code != 0
        # Typer will show error about invalid choice


class TestCliFixStrategies:
    """Test CLI fix strategy options."""

    def test_no_fix_flag_only_checks(self, tmp_path: Path) -> None:
        """Should only check without --fix flag."""
        md_file = tmp_path / "test.md"
        md_file.write_text("## Section\n\n#### Violation\n")

        result = runner.invoke(app, [str(md_file)])

        assert result.exit_code == 1  # Has violations
        assert "Violation" in md_file.read_text()  # File unchanged
        assert "Rule 3" in result.stdout

    def test_fix_shorthand_uses_conservative(self, tmp_path: Path) -> None:
        """Should use conservative strategy with --fix (shorthand)."""
        md_file = tmp_path / "test.md"
        md_file.write_text("## Section\n\n#### Violation\n\n##### Cascade\n")

        result = runner.invoke(app, [str(md_file), "--fix"])

        # Conservative mode fixes the violation but creates TODO, which is also a violation
        assert result.exit_code == 1  # Still has violations (TODO + cascade)
        content = md_file.read_text()
        # Conservative mode should insert TODO for cascade
        assert "TODO: check-md" in content
        assert "#### Violation" in content  # Original preserved

    def test_fix_strategy_none_only_checks(self, tmp_path: Path) -> None:
        """Should only check with --fix-strategy none."""
        md_file = tmp_path / "test.md"
        md_file.write_text("## Section\n\n#### Violation\n")

        result = runner.invoke(app, [str(md_file), "--fix-strategy", "none"])

        assert result.exit_code == 1  # Has violations
        assert "Violation" in md_file.read_text()  # File unchanged

    def test_fix_strategy_conservative_inserts_todos(self, tmp_path: Path) -> None:
        """Should insert TODOs with --fix-strategy conservative."""
        md_file = tmp_path / "test.md"
        md_file.write_text("## Section\n\n#### Violation\n\n##### Cascade\n")

        result = runner.invoke(app, [str(md_file), "--fix-strategy", "conservative"])

        # Conservative mode fixes the violation but creates TODO, which is also a violation
        assert result.exit_code == 1  # Still has violations (TODO + cascade)
        content = md_file.read_text()
        assert "TODO: check-md" in content
        assert "#### Violation" in content

    def test_fix_strategy_aggressive_applies_cascades(self, tmp_path: Path) -> None:
        """Should apply cascades with --fix-strategy aggressive in single call."""
        md_file = tmp_path / "test.md"
        md_file.write_text("## Section\n\n#### Violation\n\n##### Cascade\n")

        # Single call should completely fix file (multi-pass happens internally)
        result = runner.invoke(app, [str(md_file), "--fix-strategy", "aggressive"])
        assert result.exit_code == 0  # Clean after single call

        content = md_file.read_text()
        assert "### Violation" in content  # Downgraded
        assert "#### Cascade" in content  # Downgraded
        assert "TODO" not in content  # No TODOs in aggressive

    def test_fix_strategy_invalid_errors(self, tmp_path: Path) -> None:
        """Should error on invalid strategy."""
        md_file = tmp_path / "test.md"
        md_file.write_text("## Section\n")

        result = runner.invoke(app, [str(md_file), "--fix-strategy", "invalid"])

        assert result.exit_code == 2
        assert "Invalid fix strategy" in result.stderr or "Invalid fix strategy" in result.stdout

    def test_dry_run_with_fix_previews(self, tmp_path: Path) -> None:
        """Should preview fixes with --fix --dry-run."""
        md_file = tmp_path / "test.md"
        md_file.write_text("## Section\n\n#### Violation\n")

        result = runner.invoke(app, [str(md_file), "--fix", "--dry-run"])

        assert result.exit_code == 0
        # File should be unchanged
        assert "#### Violation" in md_file.read_text()
        # Should show preview
        assert "would be modified" in result.stdout.lower() or "dry run" in result.stdout.lower()
