"""
test_rule1_semantic_headings.py — Tests for Rule 1: Semantic Headings.

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

from typing import List

import pytest

from check_md.models import Severity, Violation
from check_md.rules import Rule1SemanticHeadings


@pytest.fixture
def rule() -> Rule1SemanticHeadings:
    """Create rule instance for testing."""
    return Rule1SemanticHeadings()


class TestRule1SemanticHeadings:
    """Test suite for Rule 1: Semantic Headings."""

    def test_detects_standalone_bold_as_heading(self, rule: Rule1SemanticHeadings) -> None:
        """Should detect standalone bold text that should be a heading."""
        lines = [
            "Some text here.",
            "",
            "**This Should Be A Heading**",
            "",
            "More text.",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1, f"Expected 1 violation, got {len(violations)}"

        violation = violations[0]
        assert violation.rule_id == "ADR-002-R1"
        assert violation.line_number == 3
        assert violation.severity == Severity.ERROR
        assert violation.message == "Standalone bold text should be a heading"
        assert violation.fix_hint == "Replace with: ## This Should Be A Heading"

    def test_detects_bold_with_colon_as_label(self, rule: Rule1SemanticHeadings) -> None:
        """Should NOT detect inline label-value pairs (intentional formatting)."""
        lines = [
            "",
            "**Purpose:** This is a label-value pair and should NOT be converted.",
        ]

        violations = rule.check_file(lines)

        # Inline label-value pairs should NOT be flagged as violations
        assert len(violations) == 0

    @pytest.mark.parametrize("test_case", [
        # ==================================================================
        # Valid Bold Usage - Should Not Generate Violations
        # ==================================================================
        pytest.param(
            [
                "This is a sentence with **bold emphasis** in the middle.\n",
                "Another sentence with **multiple bold** and **phrases**.\n",
            ],
            id="bold_for_emphasis_in_sentence"
        ),
        pytest.param(
            [
                "```markdown\n",
                "**This is an example**\n",
                "```\n",
            ],
            id="bold_in_code_blocks"
        ),
        pytest.param(
            [
                "Some intro text.\n",
                "\n",
                "- **Item 1:** Description\n",
                "- **Item 2:** Description\n",
            ],
            id="bold_in_list_items"
        ),
        pytest.param(
            [
                "# Heading 1\n",
                "\n",
                "## Heading 2\n",
                "\n",
                "### Heading 3\n",
                "\n",
                "Text content.\n",
            ],
            id="proper_markdown_headings"
        ),
    ])
    def test_ignores_valid_bold_usage(self, rule: Rule1SemanticHeadings, test_case: List[str]) -> None:
        """Should not flag valid uses of bold text per ADR-002."""
        violations = rule.check_file(test_case)

        assert len(violations) == 0, \
            f"Valid bold usage should not produce violations, but got: {violations}"

    def test_detects_multiple_violations(self, rule: Rule1SemanticHeadings) -> None:
        """Should detect multiple violations in same file."""
        lines = [
            "Text here.",
            "",
            "**First Heading**",
            "",
            "Some content.",
            "",
            "**Second Heading**",
            "",
            "More content.",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 2
        assert violations[0].line_number == 3
        assert violations[1].line_number == 7


    def test_handles_indented_bold(self, rule: Rule1SemanticHeadings) -> None:
        """Should detect indented standalone bold text."""
        lines = [
            "",
            "  **Indented Bold Text**",
            "",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1
        assert violations[0].line_number == 2

    def test_handles_file_start(self, rule: Rule1SemanticHeadings) -> None:
        """Should handle bold text at very start of file."""
        lines = [
            "**Bold At Start**",
            "",
            "Content follows.",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1
        assert violations[0].line_number == 1

    # Comprehensive tests for inline label-value pattern fix (tech-debt issue)
    def test_inline_author_label_not_converted(self, rule: Rule1SemanticHeadings) -> None:
        """Should NOT convert **Author:** [Name] pattern (tech-debt example 1)."""
        lines = [
            "",
            "**Author:** [F. Andy Seidl](https://linkedin.com)",
            "**Date:** 2025-11-14",
        ]

        violations = rule.check_file(lines)

        # Inline label-value pairs should NOT be flagged
        assert len(violations) == 0

    def test_inline_assessment_labels_not_converted(self, rule: Rule1SemanticHeadings) -> None:
        """Should NOT convert **Overall Risk:** MEDIUM pattern (tech-debt example 2)."""
        lines = [
            "",
            "**Overall Risk:** MEDIUM",
            "",
            "Risk description here.",
            "",
            "**Overall Complexity:** MEDIUM-HIGH",
            "",
            "Complexity description here.",
        ]

        violations = rule.check_file(lines)

        # Inline label-value pairs should NOT be flagged
        assert len(violations) == 0

    def test_standalone_with_colon_converted(self, rule: Rule1SemanticHeadings) -> None:
        """Should convert **Label:** when alone on line (tech-debt example 3)."""
        lines = [
            "",
            "**Overall Assessment:**",
            "- Item 1",
            "- Item 2",
        ]

        violations = rule.check_file(lines)

        # Standalone bold with colon SHOULD be flagged
        assert len(violations) == 1
        assert violations[0].line_number == 2

    def test_inline_label_in_list_not_converted(self, rule: Rule1SemanticHeadings) -> None:
        """Should NOT convert **Label:** value in lists."""
        lines = [
            "",
            "- **Complexity:** MEDIUM-HIGH - description",
            "- **Risk:** MEDIUM - description",
        ]

        violations = rule.check_file(lines)

        # List items with inline labels should NOT be flagged
        assert len(violations) == 0

    def test_standalone_bold_without_colon_converted(self, rule: Rule1SemanticHeadings) -> None:
        """Should convert **Standalone Bold** without colon."""
        lines = [
            "",
            "**Standalone Bold**",
            "",
            "Content here.",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1
        assert violations[0].line_number == 2

    def test_inline_content_after_colon_not_converted(self, rule: Rule1SemanticHeadings) -> None:
        """Should NOT convert when there's any content after colon on same line."""
        lines = [
            "",
            "**Not A Heading:** This has inline content so should NOT be converted.",
            "**Label:** value",
            "**Field:** [link](url)",
            "**Term:** definition text here",
        ]

        violations = rule.check_file(lines)

        # All have inline content after colon, so none should be flagged
        assert len(violations) == 0

    def test_multiple_patterns_mixed(self, rule: Rule1SemanticHeadings) -> None:
        """Should correctly handle mix of inline and standalone patterns."""
        lines = [
            "",                       # Line 1
            "**Author:** [Name]",     # Line 2 - Inline - NOT converted
            "**Date:** 2025-11-14",   # Line 3 - Inline - NOT converted
            "",                       # Line 4
            "**Overview:**",          # Line 5 - Standalone - SHOULD convert
            "",                       # Line 6
            "Content here.",          # Line 7
            "",                       # Line 8
            "**Risk:** MEDIUM",       # Line 9 - Inline - NOT converted
            "",                       # Line 10
            "**Another Section:**",   # Line 11 - Standalone - SHOULD convert
        ]

        violations = rule.check_file(lines)

        # Only lines 5 and 11 should be flagged (standalone bold with colon only)
        assert len(violations) == 2
        assert violations[0].line_number == 5
        assert violations[1].line_number == 11

    # ==================================================================
    # Edge Cases for fix_violation
    # ==================================================================

    def test_fix_handles_out_of_bounds_line_number(self, rule: Rule1SemanticHeadings) -> None:
        """Should handle violation with invalid line number gracefully."""
        lines = [
            "# Title\n",
            "\n",
            "**Bold**\n",
        ]

        # Create violation with out-of-bounds line number
        violation = Violation(
            rule_id="ADR-002-R1",
            line_number=999,  # Beyond file length
            severity=Severity.ERROR,
            message="Test",
            context="",
            fix_hint=""
        )

        fixed_lines = rule.fix_violation(lines, violation)

        # Should return lines unchanged when line number is invalid
        assert fixed_lines == lines

    def test_fix_handles_non_bold_line(self, rule: Rule1SemanticHeadings) -> None:
        """Should handle violation on line that doesn't match expected pattern."""
        lines = [
            "# Title\n",
            "\n",
            "Regular text\n",  # Not bold at all
        ]

        # Create violation for line that doesn't match pattern
        violation = Violation(
            rule_id="ADR-002-R1",
            line_number=3,
            severity=Severity.ERROR,
            message="Test",
            context="",
            fix_hint=""
        )

        fixed_lines = rule.fix_violation(lines, violation)

        # Should return lines unchanged when pattern doesn't match
        assert fixed_lines == lines

    # ==================================================================
    # Bold in List Items - Bug Fix Tests
    # ==================================================================

    def test_bold_at_start_of_list_item_not_flagged(self, rule: Rule1SemanticHeadings) -> None:
        """Bold text at start of list item should NOT be flagged as heading."""
        lines = [
            "### After Phase 1\n",
            "\n",
            "- **Continue to Phase 2 if:**\n",
            "  - All tests pass\n",
            "  - Coverage meets target\n",
        ]

        violations = rule.check_file(lines)

        # Bold text in list item should NOT be flagged
        assert len(violations) == 0, \
            f"Bold at start of list item should not be flagged, but got: {violations}"

    def test_bold_in_nested_list_not_flagged(self, rule: Rule1SemanticHeadings) -> None:
        """Bold text in nested list items should NOT be flagged (standalone bold in nested lists)."""
        lines = [
            "## Overview\n",
            "\n",
            "- **Outer item:**\n",
            "  - **Nested item 1:**\n",
            "  - **Nested item 2:**\n",
            "    - Sub-criterion a\n",
            "    - Sub-criterion b\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Bold in nested list should not be flagged, but got: {violations}"

    def test_bold_in_ordered_list_not_flagged(self, rule: Rule1SemanticHeadings) -> None:
        """Bold text at start of ordered list item should NOT be flagged."""
        lines = [
            "## Steps\n",
            "\n",
            "1. **First step:**\n",
            "   - Sub-step a\n",
            "2. **Second step:**\n",
            "   - Sub-step b\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Bold in ordered list should not be flagged, but got: {violations}"

    def test_bold_with_different_list_markers(self, rule: Rule1SemanticHeadings) -> None:
        """Bold text with different list markers (-, *, +) should NOT be flagged."""
        lines = [
            "## Items\n",
            "\n",
            "- **Dash item:**\n",
            "* **Star item:**\n",
            "+ **Plus item:**\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Bold with different list markers should not be flagged, but got: {violations}"

    def test_bold_in_list_without_colon_not_flagged(self, rule: Rule1SemanticHeadings) -> None:
        """Bold text in list item without colon should NOT be flagged."""
        lines = [
            "## Features\n",
            "\n",
            "- **Important Feature**\n",
            "- **Another Feature**\n",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Bold in list without colon should not be flagged, but got: {violations}"
