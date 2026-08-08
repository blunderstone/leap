"""Tests for ignore comments support."""

import tempfile
from pathlib import Path

from check_md.checker import MarkdownChecker
from check_md.rules import build_ignore_set


class TestBuildIgnoreSet:
    """Tests for build_ignore_set() function."""

    def test_empty_file(self) -> None:
        """Should return empty set for file with no ignore comments."""
        lines = ["# Title\n", "\n", "**Bold**\n"]
        ignored = build_ignore_set(lines)
        assert ignored == set()

    def test_ignore_comment_on_same_line(self) -> None:
        """Should ignore line with check-md-ignore comment."""
        lines = [
            "# Title\n",
            "\n",
            "**Bold** <!-- check-md-ignore -->\n",
            "**Another**\n",
        ]
        ignored = build_ignore_set(lines)
        assert ignored == {3}  # Line 3 has the ignore comment

    def test_ignore_next_comment(self) -> None:
        """Should ignore next line after check-md-ignore-next comment."""
        lines = [
            "# Title\n",
            "\n",
            "<!-- check-md-ignore-next -->\n",
            "**Bold**\n",
            "**Another**\n",
        ]
        ignored = build_ignore_set(lines)
        assert ignored == {4}  # Line 4 is after the ignore-next comment

    def test_ignore_with_whitespace(self) -> None:
        """Should handle ignore comments with varying whitespace."""
        lines = [
            "<!--check-md-ignore-->\n",  # No spaces
            "<!-- check-md-ignore -->\n",  # Normal spaces
            "<!--  check-md-ignore  -->\n",  # Extra spaces
        ]
        ignored = build_ignore_set(lines)
        assert ignored == {1, 2, 3}

    def test_multiple_ignore_comments(self) -> None:
        """Should handle multiple ignore comments in one file."""
        lines = [
            "# Title\n",
            "**Bold1** <!-- check-md-ignore -->\n",
            "\n",
            "<!-- check-md-ignore-next -->\n",
            "**Bold2**\n",
            "\n",
            "**Bold3** <!-- check-md-ignore -->\n",
        ]
        ignored = build_ignore_set(lines)
        assert ignored == {2, 5, 7}

    def test_ignore_next_at_end_of_file(self) -> None:
        """Should handle ignore-next at end of file gracefully."""
        lines = [
            "# Title\n",
            "<!-- check-md-ignore-next -->\n",
        ]
        ignored = build_ignore_set(lines)
        # No line after comment, so nothing ignored
        assert ignored == set()

    def test_ignore_range_basic(self) -> None:
        """Should ignore all lines between begin and end markers."""
        lines = [
            "# Title\n",
            "**Bold1**\n",
            "<!-- check-md-ignore-begin -->\n",
            "**Bold2**\n",
            "**Bold3**\n",
            "<!-- check-md-ignore-end -->\n",
            "**Bold4**\n",
        ]
        ignored = build_ignore_set(lines)
        # Lines 3-6 should be ignored (including markers)
        assert ignored == {3, 4, 5, 6}

    def test_ignore_range_multiple(self) -> None:
        """Should handle multiple ignore ranges in same file."""
        lines = [
            "**Bold1**\n",
            "<!-- check-md-ignore-begin -->\n",
            "**Bold2**\n",
            "<!-- check-md-ignore-end -->\n",
            "**Bold3**\n",
            "<!-- check-md-ignore-begin -->\n",
            "**Bold4**\n",
            "<!-- check-md-ignore-end -->\n",
            "**Bold5**\n",
        ]
        ignored = build_ignore_set(lines)
        assert ignored == {2, 3, 4, 6, 7, 8}

    def test_ignore_range_unclosed(self) -> None:
        """Should ignore all lines after begin if no end marker."""
        lines = [
            "**Bold1**\n",
            "<!-- check-md-ignore-begin -->\n",
            "**Bold2**\n",
            "**Bold3**\n",
        ]
        ignored = build_ignore_set(lines)
        # Lines 2-4 should all be ignored
        assert ignored == {2, 3, 4}

    def test_ignore_range_with_single_line_comments(self) -> None:
        """Should handle mix of range and single-line ignores."""
        lines = [
            "**Bold1** <!-- check-md-ignore -->\n",
            "<!-- check-md-ignore-begin -->\n",
            "**Bold2**\n",
            "<!-- check-md-ignore-end -->\n",
            "<!-- check-md-ignore-next -->\n",
            "**Bold3**\n",
            "**Bold4**\n",
        ]
        ignored = build_ignore_set(lines)
        assert ignored == {1, 2, 3, 4, 6}


class TestIgnoreCommentsIntegration:
    """Integration tests for ignore comments with checker."""

    def test_ignore_prevents_rule1_violation(self) -> None:
        """Should not report Rule 1 violation on ignored line."""
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\n")
            f.write("**Bold** <!-- check-md-ignore -->\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            # Should have no violations (Bold is ignored)
            assert len(result.violations) == 0
        finally:
            temp_path.unlink()

    def test_ignore_next_prevents_rule1_violation(self) -> None:
        """Should not report Rule 1 violation on line after ignore-next."""
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\n")
            f.write("<!-- check-md-ignore-next -->\n")
            f.write("**Bold**\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            # Should have no violations (line after ignore-next is ignored)
            assert len(result.violations) == 0
        finally:
            temp_path.unlink()

    def test_ignore_selective(self) -> None:
        """Should ignore only specified lines, not all violations."""
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\n")
            f.write("**Bold1** <!-- check-md-ignore -->\n")
            f.write("\n")
            f.write("**Bold2**\n")  # This should still be flagged
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            # Should have 1 violation (Bold2 on line 5)
            assert len(result.violations) == 1
            assert result.violations[0].line_number == 5
            assert "Bold2" in result.violations[0].context
        finally:
            temp_path.unlink()

    def test_ignore_prevents_rule2_violation(self) -> None:
        """Should not report Rule 2 violation on ignored line."""
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\n")
            f.write("Some text\n")
            f.write("- List item <!-- check-md-ignore -->\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            # Should have no violations (list on line 4 is ignored)
            assert len(result.violations) == 0
        finally:
            temp_path.unlink()

    def test_ignore_prevents_rule4_violation(self) -> None:
        """Should not report Rule 4 violation on ignored line."""
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\n")
            f.write("```markdown <!-- check-md-ignore -->\n")
            f.write("Example:\n")
            f.write("```bash\n")
            f.write("command\n")
            f.write("```\n")
            f.write("```\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            # Should have no Rule 4 violations (line 3 is ignored)
            rule4_violations = [v for v in result.violations if v.rule_id == "ADR-002-R4"]
            assert len(rule4_violations) == 0
        finally:
            temp_path.unlink()

    def test_ignore_range_integration(self) -> None:
        """Should ignore all violations in range."""
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\n")
            f.write("**Bold1**\n")  # Should be flagged
            f.write("\n")
            f.write("<!-- check-md-ignore-begin -->\n")
            f.write("**Bold2**\n")  # Should be ignored
            f.write("**Bold3**\n")  # Should be ignored
            f.write("<!-- check-md-ignore-end -->\n")
            f.write("\n")
            f.write("**Bold4**\n")  # Should be flagged
            f.write("\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            # Should have 2 violations (Bold1 on line 3, Bold4 on line 10)
            assert len(result.violations) == 2
            assert result.violations[0].line_number == 3
            assert result.violations[1].line_number == 10
        finally:
            temp_path.unlink()
