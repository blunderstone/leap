"""
test_checker.py — Tests for MarkdownChecker.

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

import tempfile
from pathlib import Path

import pytest

from check_md.checker import MarkdownChecker
from check_md.models import Severity


@pytest.fixture
def checker() -> MarkdownChecker:
    """Create checker instance with all rules."""
    return MarkdownChecker()


class TestMarkdownChecker:
    """Test suite for MarkdownChecker."""

    def test_check_file_returns_file_result(self, checker: MarkdownChecker) -> None:
        """Should return FileResult with violations."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Text\n")
            f.write("- List without blank line\n")
            temp_path = f.name

        try:
            result = checker.check_file(temp_path)

            assert result.file_path == temp_path
            assert result.total_lines == 2
            assert result.has_violations
            assert result.error_count > 0
        finally:
            Path(temp_path).unlink()

    def test_check_file_counts_violations(self, checker: MarkdownChecker) -> None:
        """Should correctly count errors and warnings."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            # Write content with known violations
            f.write("\n")  # Blank line to make next line flagged
            f.write("**Bold Label:**\n")  # ERROR: Rule 1 (standalone bold after blank)
            f.write("- List item\n")  # ERROR: Rule 2
            temp_path = f.name

        try:
            result = checker.check_file(temp_path)

            assert result.error_count == 2  # Rule 1 + Rule 2
            assert result.warning_count == 0  # No warnings
        finally:
            Path(temp_path).unlink()

    def test_check_file_raises_on_missing_file(self, checker: MarkdownChecker) -> None:
        """Should raise FileNotFoundError for missing files."""
        with pytest.raises(FileNotFoundError):
            checker.check_file("/nonexistent/file.md")

    def test_check_file_raises_on_non_markdown(self, checker: MarkdownChecker) -> None:
        """Should raise ValueError for non-.md files."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_path = f.name

        try:
            with pytest.raises(ValueError, match="Not a markdown file"):
                checker.check_file(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_check_file_sorts_violations_by_line(self, checker: MarkdownChecker) -> None:
        """Should return violations sorted by line number."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Text\n")
            f.write("- List 1\n")  # Line 2: violation
            f.write("\n")
            f.write("Text\n")
            f.write("- List 2\n")  # Line 5: violation
            temp_path = f.name

        try:
            result = checker.check_file(temp_path)

            # Should be sorted by line number
            for i in range(len(result.violations) - 1):
                assert result.violations[i].line_number <= result.violations[i + 1].line_number
        finally:
            Path(temp_path).unlink()

    def test_check_files_handles_multiple_files(self, checker: MarkdownChecker) -> None:
        """Should check multiple files and return list of results."""
        temp_files = []

        try:
            # Create two temp files
            for i in range(2):
                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".md", delete=False
                ) as f:
                    f.write(f"File {i}\n")
                    f.write("- List item\n")
                    temp_files.append(f.name)

            results = checker.check_files(temp_files)

            assert len(results) == 2
            assert all(r.has_violations for r in results)
        finally:
            for path in temp_files:
                Path(path).unlink()

    def test_check_files_skips_invalid_files(
        self, checker: MarkdownChecker, capsys: pytest.CaptureFixture
    ) -> None:
        """Should skip invalid files and continue with others."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Valid file\n")
            valid_file = f.name

        try:
            # Mix valid and invalid files
            files = ["/nonexistent.md", valid_file]
            results = checker.check_files(files)

            # Should only have result for valid file
            assert len(results) == 1
            assert results[0].file_path == valid_file

            # Should print warning
            captured = capsys.readouterr()
            assert "Warning" in captured.out
        finally:
            Path(valid_file).unlink()

    def test_check_file_handles_empty_file(self, checker: MarkdownChecker) -> None:
        """Should handle empty markdown files."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            temp_path = f.name  # Empty file

        try:
            result = checker.check_file(temp_path)

            assert result.total_lines == 0
            assert not result.has_violations
        finally:
            Path(temp_path).unlink()

    def test_check_file_handles_clean_markdown(self, checker: MarkdownChecker) -> None:
        """Should return no violations for properly formatted markdown."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Heading\n")
            f.write("\n")
            f.write("Some text here.\n")
            f.write("\n")
            f.write("- List item 1\n")
            f.write("- List item 2\n")
            temp_path = f.name

        try:
            result = checker.check_file(temp_path)

            assert not result.has_violations
            assert result.error_count == 0
            assert result.warning_count == 0
        finally:
            Path(temp_path).unlink()

    def test_check_file_handles_unicode(self, checker: MarkdownChecker) -> None:
        """Should handle markdown files with unicode characters."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("# Heading with émojis 🎉\n")
            f.write("\n")
            f.write("Text with ñoñ-ÂSCII çhäracters.\n")
            temp_path = f.name

        try:
            result = checker.check_file(temp_path)

            # Should not crash
            assert isinstance(result.violations, list)
        finally:
            Path(temp_path).unlink()

    def test_rules_no_adr_008_references(self, checker: MarkdownChecker) -> None:
        """Should ensure that no loaded rules contain references to the obsolete 'ADR 008'."""
        for rule in checker.rules:
            # Check rule descriptions and docstrings
            rule_id = rule.rule_id
            description = rule.description or ""
            docstring = rule.__doc__ or ""

            assert "ADR 008" not in description, f"Rule {rule_id} description contains 'ADR 008'"
            assert "ADR-008" not in description, f"Rule {rule_id} description contains 'ADR-008'"
            assert "ADR 008" not in docstring, f"Rule {rule_id} docstring contains 'ADR 008'"
            assert "ADR-008" not in docstring, f"Rule {rule_id} docstring contains 'ADR-008'"

