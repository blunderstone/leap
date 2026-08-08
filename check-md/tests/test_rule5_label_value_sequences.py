"""
Tests for Rule 5: Label-Value Sequence Line Breaks.

Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)
"""

import pytest

from check_md.models import Severity
from check_md.rules import Rule5LabelValueSequences


@pytest.fixture
def rule() -> Rule5LabelValueSequences:
    """Create rule instance for testing."""
    return Rule5LabelValueSequences()


class TestRule5LabelValueSequences:
    """Test suite for Rule 5: Label-Value Sequence Line Breaks."""

    def test_detects_missing_br_in_label_sequence(self, rule: Rule5LabelValueSequences) -> None:
        """Should detect missing <br> when label-value lines are consecutive."""
        lines = [
            "**Author:** [F. Andy Seidl](https://linkedin.com)\n",
            "**Date:** 2025-12-18\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1, f"Expected 1 violation, got {len(violations)}"
        assert violations[0].rule_id == "ADR-002-R5"
        assert violations[0].line_number == 1
        assert violations[0].severity == Severity.ERROR
        assert "missing <br>" in violations[0].message.lower()

    def test_allows_br_at_end_of_label_line(self, rule: Rule5LabelValueSequences) -> None:
        """Should NOT flag when label-value line ends with <br>."""
        lines = [
            "**Author:** [F. Andy Seidl](https://linkedin.com)<br>\n",
            "**Date:** 2025-12-18\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, f"Should not flag with <br>, but got: {violations}"

    def test_allows_last_line_without_br(self, rule: Rule5LabelValueSequences) -> None:
        """Should NOT flag last label-value line in sequence without <br>."""
        lines = [
            "**Author:** [F. Andy Seidl](https://linkedin.com)<br>\n",
            "**Date:** 2025-12-18\n",
            "\n",
            "Some content.\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, f"Last line doesn't need <br>, but got: {violations}"

    def test_detects_multiple_missing_br_tags(self, rule: Rule5LabelValueSequences) -> None:
        """Should detect multiple missing <br> tags in sequence."""
        lines = [
            "**Author:** John Doe\n",
            "**Date:** 2025-12-18\n",
            "**Status:** Active\n",
            "\n",
            "Content.\n",
        ]

        violations = rule.check_file(lines)

        # Lines 1 and 2 should be flagged (line 3 is last in sequence)
        assert len(violations) == 2
        assert violations[0].line_number == 1
        assert violations[1].line_number == 2

    def test_handles_colon_outside_bold(self, rule: Rule5LabelValueSequences) -> None:
        """Should detect pattern with colon outside bold: **Label**: value."""
        lines = [
            "**Author**: John Doe\n",
            "**Date**: 2025-12-18\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1
        assert violations[0].line_number == 1

    def test_ignores_single_label_value_line(self, rule: Rule5LabelValueSequences) -> None:
        """Should NOT flag single label-value line with no following label."""
        lines = [
            "**Author:** John Doe\n",
            "\n",
            "Regular paragraph text.\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_ignores_non_label_value_patterns(self, rule: Rule5LabelValueSequences) -> None:
        """Should NOT flag lines that don't match label-value pattern."""
        lines = [
            "**This is bold text** in a sentence.\n",
            "Another **bold** word here.\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_ignores_label_value_in_code_blocks(self, rule: Rule5LabelValueSequences) -> None:
        """Should NOT flag label-value patterns inside code blocks."""
        lines = [
            "```\n",
            "**Author:** John Doe\n",
            "**Date:** 2025-12-18\n",
            "```\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_handles_sequence_broken_by_blank_line(self, rule: Rule5LabelValueSequences) -> None:
        """Should treat blank lines as breaking the sequence."""
        lines = [
            "**Author:** John Doe\n",
            "\n",
            "**Date:** 2025-12-18\n",
        ]

        violations = rule.check_file(lines)

        # Both lines are "single" in their own sequences
        assert len(violations) == 0

    def test_detects_in_middle_of_document(self, rule: Rule5LabelValueSequences) -> None:
        """Should detect label-value sequences anywhere in document."""
        lines = [
            "# Heading\n",
            "\n",
            "Some content.\n",
            "\n",
            "**Risk:** MEDIUM\n",
            "**Complexity:** HIGH\n",
            "\n",
            "More content.\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1
        assert violations[0].line_number == 5

    def test_handles_mixed_sequences_with_and_without_br(self, rule: Rule5LabelValueSequences) -> None:
        """Should handle sequences where some lines have <br> and some don't."""
        lines = [
            "**First:** value<br>\n",
            "**Second:** value\n",
            "**Third:** value\n",
        ]

        violations = rule.check_file(lines)

        # Line 2 is missing <br> (line 3 is last in sequence)
        assert len(violations) == 1
        assert violations[0].line_number == 2

    def test_allows_html_br_variations(self, rule: Rule5LabelValueSequences) -> None:
        """Should recognize various <br> tag formats."""
        lines = [
            "**Author:** John<br>\n",
            "**Date:** 2025<br/>\n",
            "**Status:** Active<br />\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, f"Should recognize all <br> formats, but got: {violations}"


class TestRule5Fixes:
    """Test suite for Rule 5 auto-fix functionality."""

    def test_fix_adds_br_to_line(self, rule: Rule5LabelValueSequences) -> None:
        """Should add <br> at end of line missing it."""
        lines = [
            "**Author:** John Doe\n",
            "**Date:** 2025-12-18\n",
        ]

        violations = rule.check_file(lines)
        assert len(violations) == 1

        fixed_lines = rule.fix_violation(lines, violations[0])

        assert fixed_lines[0] == "**Author:** John Doe<br>\n"
        assert fixed_lines[1] == "**Date:** 2025-12-18\n"

    def test_fix_preserves_existing_content(self, rule: Rule5LabelValueSequences) -> None:
        """Should preserve all existing content when adding <br>."""
        lines = [
            "**Author:** [F. Andy Seidl](https://linkedin.com)\n",
            "**Date:** 2025-12-18\n",
        ]

        violations = rule.check_file(lines)
        fixed_lines = rule.fix_violation(lines, violations[0])

        assert fixed_lines[0] == "**Author:** [F. Andy Seidl](https://linkedin.com)<br>\n"

    def test_fix_handles_line_without_newline(self, rule: Rule5LabelValueSequences) -> None:
        """Should handle lines that don't end with newline."""
        lines = [
            "**Author:** John Doe",
            "**Date:** 2025-12-18",
        ]

        violations = rule.check_file(lines)
        fixed_lines = rule.fix_violation(lines, violations[0])

        assert fixed_lines[0] == "**Author:** John Doe<br>"

    def test_fix_multiple_violations(self, rule: Rule5LabelValueSequences) -> None:
        """Should fix multiple violations in sequence."""
        lines = [
            "**First:** value1\n",
            "**Second:** value2\n",
            "**Third:** value3\n",
            "\n",
        ]

        violations = rule.check_file(lines)
        assert len(violations) == 2

        # Fix in reverse order (bottom-up) to preserve line numbers
        for violation in reversed(violations):
            lines = rule.fix_violation(lines, violation)

        assert lines[0] == "**First:** value1<br>\n"
        assert lines[1] == "**Second:** value2<br>\n"
        assert lines[2] == "**Third:** value3\n"

    def test_fix_strips_trailing_whitespace(self, rule: Rule5LabelValueSequences) -> None:
        """Should strip trailing whitespace before adding <br>."""
        lines = [
            "**Author:** John Doe  \n",
            "**Date:** 2025-12-18\n",
        ]

        violations = rule.check_file(lines)
        fixed_lines = rule.fix_violation(lines, violations[0])

        # Should strip trailing whitespace and add <br>
        assert fixed_lines[0] == "**Author:** John Doe<br>\n"

    def test_fix_handles_out_of_bounds(self, rule: Rule5LabelValueSequences) -> None:
        """Should handle invalid line number gracefully."""
        lines = [
            "**Author:** John Doe\n",
        ]

        from check_md.models import Violation, Severity
        violation = Violation(
            rule_id="ADR-002-R5",
            line_number=999,
            severity=Severity.ERROR,
            message="Test",
            context="",
            fix_hint=""
        )

        fixed_lines = rule.fix_violation(lines, violation)
        assert fixed_lines == lines  # Unchanged
