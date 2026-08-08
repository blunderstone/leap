"""
Tests for Rule 2: Block Separation.

Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)
"""

from dataclasses import dataclass
from typing import List

import pytest

from check_md.models import Severity, Violation
from check_md.rules import Rule2BlockSeparation


@dataclass
class BlockTypeTestCase:
    """Test case for block type violations (mirrors Kotlin TestCase pattern)."""

    lines: List[str]
    expected_line: int
    expected_message_fragment: str


@pytest.fixture
def rule() -> Rule2BlockSeparation:
    """Create rule instance for testing."""
    return Rule2BlockSeparation()


class TestRule2BlockSeparation:
    """Test suite for Rule 2: Block Separation."""

    @pytest.mark.parametrize("test_case", [
        # ==================================================================
        # Missing Blank Lines Before Various Block Types
        # ==================================================================
        pytest.param(
            BlockTypeTestCase(
                lines=[
                    "This is some text.\n",
                    "- List item 1\n",
                    "- List item 2\n",
                ],
                expected_line=2,
                expected_message_fragment="unordered list"
            ),
            id="unordered_list"
        ),
        pytest.param(
            BlockTypeTestCase(
                lines=[
                    "Here's a numbered list:\n",
                    "1. First item\n",
                    "2. Second item\n",
                ],
                expected_line=2,
                expected_message_fragment="ordered list"
            ),
            id="ordered_list"
        ),
        pytest.param(
            BlockTypeTestCase(
                lines=[
                    "Here's some code:\n",
                    "```python\n",
                    "print('hello')\n",
                    "```\n",
                ],
                expected_line=2,
                expected_message_fragment="code block"
            ),
            id="code_block"
        ),
        pytest.param(
            BlockTypeTestCase(
                lines=[
                    "Some text here.\n",
                    "> This is a quote\n",
                ],
                expected_line=2,
                expected_message_fragment="block quote"
            ),
            id="blockquote"
        ),
        pytest.param(
            BlockTypeTestCase(
                lines=[
                    "Section one.\n",
                    "---\n",
                    "Section two.\n",
                ],
                expected_line=2,
                expected_message_fragment="horizontal rule"
            ),
            id="horizontal_rule"
        ),
        pytest.param(
            BlockTypeTestCase(
                lines=[
                    "Here's a table:\n",
                    "| Column 1 | Column 2 |\n",
                    "| -------- | -------- |\n",
                    "| Data 1   | Data 2   |\n",
                ],
                expected_line=2,
                expected_message_fragment="table"
            ),
            id="table"
        ),
    ])
    def test_detects_missing_blank_before_blocks(
        self, rule: Rule2BlockSeparation, test_case: BlockTypeTestCase
    ) -> None:
        """Should detect missing blank lines before various block types per ADR-002."""
        violations = rule.check_file(test_case.lines)

        assert len(violations) == 1, \
            f"Expected 1 violation, got {len(violations)}: {violations}"
        assert violations[0].rule_id == "ADR-002-R2", \
            f"Expected rule_id 'ADR-002-R2', got '{violations[0].rule_id}'"
        assert violations[0].line_number == test_case.expected_line, \
            f"Expected violation at line {test_case.expected_line}, got {violations[0].line_number}"
        assert violations[0].severity == Severity.ERROR, \
            f"Expected severity ERROR, got {violations[0].severity}"
        assert test_case.expected_message_fragment in violations[0].message.lower(), \
            f"Expected message to contain '{test_case.expected_message_fragment}', got '{violations[0].message}'"

    def test_allows_blank_line_before_list(self, rule: Rule2BlockSeparation) -> None:
        """Should not flag when blank line exists before list."""
        lines = [
            "This is some text.",
            "",
            "- List item 1",
            "- List item 2",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_allows_blank_line_before_code_block(self, rule: Rule2BlockSeparation) -> None:
        """Should not flag when blank line exists before code block."""
        lines = [
            "Here's some code:",
            "",
            "```python",
            "print('hello')",
            "```",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_ignores_list_at_file_start(self, rule: Rule2BlockSeparation) -> None:
        """Should not flag list at very start of file."""
        lines = [
            "- First item",
            "- Second item",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_ignores_list_continuation(self, rule: Rule2BlockSeparation) -> None:
        """Should not flag continuation of list items."""
        lines = [
            "Text before.",
            "",
            "- First item",
            "- Second item",
            "- Third item",
        ]

        violations = rule.check_file(lines)

        # Should only flag if first item was missing blank line (it's not)
        assert len(violations) == 0

    def test_detects_multiple_violations(self, rule: Rule2BlockSeparation) -> None:
        """Should detect multiple violations in same file."""
        lines = [
            "Text.",
            "- List 1",
            "",
            "More text.",
            "```python",
            "code",
            "```",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 2
        assert violations[0].line_number == 2  # List
        assert violations[1].line_number == 5  # Code block

    def test_handles_indented_lists(self, rule: Rule2BlockSeparation) -> None:
        """Should detect violations in indented lists."""
        lines = [
            "Text.",
            "  - Indented list",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1
        assert violations[0].line_number == 2

    def test_handles_different_list_markers(self, rule: Rule2BlockSeparation) -> None:
        """Should detect violations with -, *, + list markers."""
        lines = [
            "Text.",
            "- Dash list",
            "",
            "Text.",
            "* Star list",
            "",
            "Text.",
            "+ Plus list",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 3

    def test_ignores_violations_inside_code_blocks(self, rule: Rule2BlockSeparation) -> None:
        """Should not check inside code blocks."""
        lines = [
            "```markdown",
            "Text here.",
            "- List without blank line",
            "```",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    # ==================================================================
    # Edge Cases for fix_violation
    # ==================================================================

    def test_fix_handles_out_of_bounds_line_number(self, rule: Rule2BlockSeparation) -> None:
        """Should handle violation with invalid line number gracefully."""
        lines = [
            "Text.\n",
            "- List\n",
        ]

        # Create violation with out-of-bounds line number
        violation = Violation(
            rule_id="ADR-002-R2",
            line_number=999,  # Beyond file length
            severity=Severity.ERROR,
            message="Test",
            context="",
            fix_hint=""
        )

        fixed_lines = rule.fix_violation(lines, violation)

        # Should return lines unchanged when line number is invalid
        assert fixed_lines == lines

    def test_fix_inserts_blank_line_correctly(self, rule: Rule2BlockSeparation) -> None:
        """Should insert blank line before block construct."""
        lines = [
            "Text.\n",
            "- List\n",
        ]

        violations = rule.check_file(lines)
        assert len(violations) == 1

        fixed_lines = rule.fix_violation(lines, violations[0])

        # Should have blank line inserted before list
        expected = [
            "Text.\n",
            "\n",
            "- List\n",
        ]
        assert fixed_lines == expected
