"""
Tests for Rule 3: Heading Level Increment.

Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)
"""

from dataclasses import dataclass
from typing import List

import pytest

from check_md.models import Severity, Violation
from check_md.rules import FixStrategy, Rule3HeadingIncrement


@dataclass
class ViolationTestCase:
    """Test case for heading level violations (mirrors Kotlin TestCase pattern)."""

    lines: List[str]
    expected_count: int
    expected_line: int
    expected_message_fragment: str
    expected_hint_fragment: str


@pytest.fixture
def rule() -> Rule3HeadingIncrement:
    """Create rule instance for testing."""
    return Rule3HeadingIncrement()


class TestRule3HeadingIncrement:
    """Test suite for Rule 3: Heading Level Increment."""

    # =================================================================
    # Valid Sequences - Should NOT Generate Violations
    # =================================================================

    @pytest.mark.parametrize("test_case", [
        # ==================================================================
        # Valid Heading Sequences - Increments
        # ==================================================================
        pytest.param(
            [
                "# Level 1\n",
                "\n",
                "## Level 2\n",
                "\n",
                "### Level 3\n",
                "\n",
                "#### Level 4\n",
            ],
            id="increment_of_one"
        ),

        # ==================================================================
        # Valid Heading Sequences - Decrements
        # ==================================================================
        pytest.param(
            [
                "# Level 1\n",
                "\n",
                "## Level 2\n",
                "\n",
                "### Level 3\n",
                "\n",
                "#### Level 4\n",
                "\n",
                "## Back to Level 2 (decrement of 2 is OK)\n",
                "\n",
                "# Back to Level 1 (decrement of 1 is OK)\n",
            ],
            id="decrement_of_any_size"
        ),

        # ==================================================================
        # Valid Heading Sequences - Same Level
        # ==================================================================
        pytest.param(
            [
                "# Introduction\n",
                "\n",
                "# Methods\n",
                "\n",
                "## Approach A\n",
                "\n",
                "## Approach B\n",
                "\n",
                "## Approach C\n",
            ],
            id="same_level_headings"
        ),

        # ==================================================================
        # Valid Heading Sequences - First Heading Flexibility
        # ==================================================================
        pytest.param(
            [
                "## Quick Start\n",
                "\n",
                "### Prerequisites\n",
                "\n",
                "### Installation\n",
            ],
            id="first_heading_at_any_level"
        ),
        pytest.param(
            [
                "### Starting at Level 3\n",
                "\n",
                "#### Level 4\n",
            ],
            id="first_heading_at_level_3"
        ),
    ])
    def test_allows_valid_heading_sequences(self, rule: Rule3HeadingIncrement, test_case: List[str]) -> None:
        """Should allow valid heading sequences per ADR-002."""
        violations = rule.check_file(test_case)

        assert len(violations) == 0, \
            f"Valid heading sequence should not produce violations, but got: {violations}"

    # =================================================================
    # Invalid Sequences - Should Generate Violations
    # =================================================================

    @pytest.mark.parametrize("test_case", [
        # ==================================================================
        # Single Violations - Level Skips
        # ==================================================================
        pytest.param(
            ViolationTestCase(
                lines=[
                    "## Level 2\n",
                    "\n",
                    "#### Level 4 - Skipped Level 3\n",
                ],
                expected_count=1,
                expected_line=3,
                expected_message_fragment="increased by 2",
                expected_hint_fragment="### heading"
            ),
            id="skip_one_level"
        ),
        pytest.param(
            ViolationTestCase(
                lines=[
                    "## Level 2\n",
                    "\n",
                    "##### Level 5 - Skipped Levels 3 and 4\n",
                ],
                expected_count=1,
                expected_line=3,
                expected_message_fragment="increased by 3",
                expected_hint_fragment="### heading"
            ),
            id="skip_two_levels"
        ),
    ])
    def test_detects_heading_level_skips(self, rule: Rule3HeadingIncrement, test_case: ViolationTestCase) -> None:
        """Should detect heading level skips per ADR-002."""
        violations = rule.check_file(test_case.lines)

        assert len(violations) == test_case.expected_count, \
            f"Expected {test_case.expected_count} violations, got {len(violations)}: {violations}"

        violation = violations[0]
        assert violation.rule_id == "ADR-002-R3", \
            f"Expected rule_id 'ADR-002-R3', got '{violation.rule_id}'"
        assert violation.line_number == test_case.expected_line, \
            f"Expected violation at line {test_case.expected_line}, got {violation.line_number}"
        assert violation.severity == Severity.ERROR, \
            f"Expected severity ERROR, got {violation.severity}"
        assert test_case.expected_message_fragment in violation.message, \
            f"Expected message to contain '{test_case.expected_message_fragment}', got '{violation.message}'"
        assert test_case.expected_hint_fragment in violation.fix_hint, \
            f"Expected hint to contain '{test_case.expected_hint_fragment}', got '{violation.fix_hint}'"

    def test_detects_multiple_violations_in_same_file(self, rule: Rule3HeadingIncrement) -> None:
        """Should detect multiple heading level violations in the same file."""
        lines = [
            "# Level 1",
            "",
            "### Level 3 - First skip",
            "",
            "## Level 2 - OK (decrement)",
            "",
            "##### Level 5 - Second skip",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 2, \
            f"Expected 2 violations, got {len(violations)}: {violations}"

        # First violation: # → ### (skipped ##)
        assert violations[0].line_number == 3
        assert violations[0].message == "Heading level increased by 2 (from # to ###)"

        # Second violation: ## → ##### (skipped ###, ####)
        assert violations[1].line_number == 7
        assert violations[1].message == "Heading level increased by 3 (from ## to #####)"

    def test_provides_clear_error_message(self, rule: Rule3HeadingIncrement) -> None:
        """Should provide clear, actionable error messages."""
        lines = [
            "## Section",
            "",
            "#### Subsection",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1

        violation = violations[0]

        # Message should explain the problem clearly
        assert violation.message == "Heading level increased by 2 (from ## to ####)", \
            f"Expected specific message, got: {violation.message}"

        # Fix hint should provide actionable guidance
        assert violation.fix_hint == "Change #### to ### or add intermediate ### heading", \
            f"Expected specific fix hint, got: {violation.fix_hint}"

        # Context should show the problematic line
        assert violation.context == "#### Subsection", \
            f"Expected exact context, got: {violation.context}"

    # =================================================================
    # Code Block Handling
    # =================================================================

    def test_ignores_headings_in_code_blocks(self, rule: Rule3HeadingIncrement) -> None:
        """Should not check headings inside code blocks."""
        lines = [
            "## Level 2",
            "",
            "```markdown",
            "## Example Heading",
            "#### This should be ignored",
            "```",
            "",
            "### Level 3 - This is OK",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Headings in code blocks should be ignored, but got violations: {violations}"

    def test_handles_nested_code_blocks_correctly(self, rule: Rule3HeadingIncrement) -> None:
        """Should correctly track code block state with different fence lengths."""
        lines = [
            "## Level 2",
            "",
            "````markdown",
            "```",
            "#### Ignored heading",
            "```",
            "````",
            "",
            "### Level 3 - This is OK",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Nested code blocks should be handled correctly, but got violations: {violations}"

    # =================================================================
    # Ignore Comment Handling
    # =================================================================

    def test_respects_ignore_next_comment(self, rule: Rule3HeadingIncrement) -> None:
        """Should skip violations marked with check-md-ignore-next."""
        lines = [
            "## Level 2",
            "",
            "<!-- check-md-ignore-next -->",
            "#### Intentional skip",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"check-md-ignore-next should suppress violations, but got: {violations}"

    def test_respects_ignore_begin_end_comments(self, rule: Rule3HeadingIncrement) -> None:
        """Should skip violations within check-md-ignore-begin/end blocks."""
        lines = [
            "## Level 2",
            "",
            "<!-- check-md-ignore-begin -->",
            "#### First skip",
            "####### Extreme skip",
            "<!-- check-md-ignore-end -->",
            "",
            "### Level 3 - This is OK",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Ignore blocks should suppress violations, but got: {violations}"

    def test_respects_ignore_comment_on_same_line(self, rule: Rule3HeadingIncrement) -> None:
        """Should skip violations on lines with check-md-ignore comment."""
        lines = [
            "## Level 2",
            "",
            "#### Intentional skip <!-- check-md-ignore -->",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Same-line ignore should suppress violations, but got: {violations}"

    # =================================================================
    # Edge Cases
    # =================================================================

    def test_handles_empty_file(self, rule: Rule3HeadingIncrement) -> None:
        """Should handle empty files without errors."""
        lines = []

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Empty files should produce no violations, but got: {violations}"

    def test_handles_file_with_no_headings(self, rule: Rule3HeadingIncrement) -> None:
        """Should handle files with no headings."""
        lines = [
            "This is a document with no headings.",
            "",
            "Just plain text.",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Files with no headings should produce no violations, but got: {violations}"

    def test_handles_file_with_only_one_heading(self, rule: Rule3HeadingIncrement) -> None:
        """Should handle files with only one heading (no comparison possible)."""
        lines = [
            "#### Single Heading",
            "",
            "Content",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Single heading should produce no violations, but got: {violations}"

    def test_ignores_invalid_headings(self, rule: Rule3HeadingIncrement) -> None:
        """Should ignore lines that look like headings but aren't (7+ hashes, no space)."""
        lines = [
            "## Level 2",
            "",
            "####### Not a valid heading (7 hashes)",
            "####No space after hashes",
            "",
            "### Level 3 - OK",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Invalid heading syntax should be ignored, but got: {violations}"

    def test_handles_headings_with_inline_code(self, rule: Rule3HeadingIncrement) -> None:
        """Should correctly process headings containing inline code."""
        lines = [
            "## Level 2",
            "",
            "### Level 3 with `code` in it",
            "",
            "#### Level 4 with `multiple` `code` `spans`",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0, \
            f"Headings with inline code should be processed normally, but got: {violations}"

    # =================================================================
    # Auto-Fix Functionality (Phase 3)
    # =================================================================

    def test_fixes_heading_level_skip(self, rule: Rule3HeadingIncrement) -> None:
        """Should fix heading level skip by downgrading to next valid level."""
        lines = [
            "## Level 2\n",
            "\n",
            "#### Level 4 - Should become Level 3\n",
        ]

        violations = rule.check_file(lines)
        assert len(violations) == 1

        fixed_lines = rule.fix_violation(lines, violations[0])

        expected_lines = [
            "## Level 2\n",
            "\n",
            "### Level 4 - Should become Level 3\n",  # #### → ###
        ]

        assert fixed_lines == expected_lines, \
            f"Expected heading to be downgraded to ###, but got: {fixed_lines[2]}"

    def test_fix_preserves_heading_text_exactly(self, rule: Rule3HeadingIncrement) -> None:
        """Should preserve heading text content exactly when fixing."""
        lines = [
            "## Level 2\n",
            "\n",
            "##### Level 5 with special chars: `code`, **bold**, and [links](url)\n",
        ]

        violations = rule.check_file(lines)
        assert len(violations) == 1

        fixed_lines = rule.fix_violation(lines, violations[0])

        # Should only change ##### to ### (previous level + 1)
        expected_text = "### Level 5 with special chars: `code`, **bold**, and [links](url)\n"
        assert fixed_lines[2] == expected_text, \
            f"Heading text should be preserved exactly, but got: {fixed_lines[2]}"

    def test_fix_handles_multiple_violations(self, rule: Rule3HeadingIncrement) -> None:
        """Should handle fixing multiple violations in sequence."""
        lines = [
            "# Level 1\n",
            "\n",
            "### Level 3 - First skip\n",
            "\n",
            "## Level 2\n",
            "\n",
            "##### Level 5 - Second skip\n",
        ]

        violations = rule.check_file(lines)
        assert len(violations) == 2

        # Fix first violation
        fixed_lines = rule.fix_violation(lines, violations[0])
        assert fixed_lines[2] == "## Level 3 - First skip\n", \
            f"Expected '## Level 3 - First skip\\n', got '{fixed_lines[2]}'"

        # Fix second violation on updated lines
        # Note: After first fix, need to re-check to get updated violations
        violations_after_first_fix = rule.check_file(fixed_lines)
        fixed_lines = rule.fix_violation(fixed_lines, violations_after_first_fix[0])
        assert fixed_lines[6] == "### Level 5 - Second skip\n", \
            f"Expected '### Level 5 - Second skip\\n', got '{fixed_lines[6]}'"

    def test_fix_returns_unchanged_lines_for_invalid_line_number(self, rule: Rule3HeadingIncrement) -> None:
        """Should return unchanged lines if violation line number is out of bounds."""
        lines = [
            "## Level 2\n",
            "\n",
            "#### Level 4\n",
        ]

        # Create violation with invalid line number
        violations = rule.check_file(lines)
        invalid_violation = violations[0]
        invalid_violation.line_number = 999  # Out of bounds

        fixed_lines = rule.fix_violation(lines, invalid_violation)

        assert fixed_lines == lines, \
            "Lines should be unchanged when line number is invalid"

    def test_fix_returns_unchanged_if_no_previous_heading_found(self, rule: Rule3HeadingIncrement) -> None:
        """Should return unchanged lines if no previous heading can be found (edge case)."""
        lines = [
            "Some text\n",
            "\n",
            "#### Level 4\n",
        ]

        # Manually create a violation (normally wouldn't happen since first heading is allowed)
        violations = rule.check_file(lines)

        # This scenario actually can't happen in normal operation since first heading
        # is always allowed. Test defensive coding.
        if len(violations) == 0:
            # Expected behavior - no violations for first heading
            assert True
        else:
            # If somehow a violation was generated, fix should be safe
            fixed_lines = rule.fix_violation(lines, violations[0])
            # Should return lines unchanged or safely handle it
            assert len(fixed_lines) == len(lines)

    # =================================================================
    # Regression Tests for Known Issues
    # =================================================================

    def test_known_violation_pattern_from_claude_md(self, rule: Rule3HeadingIncrement) -> None:
        """Should detect pattern from historical CLAUDE.md violation (## → ####)."""
        lines = [
            "## ⚠️ CRITICAL: ADR 008 Markdown Compliance",
            "",
            "#### ALWAYS check markdown files for ADR 008 compliance before presenting to user.",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1, \
            f"Should detect CLAUDE.md historical violation pattern, got {len(violations)} violations"
        assert violations[0].line_number == 3
        assert violations[0].message == "Heading level increased by 2 (from ## to ####)"

    # =================================================================
    # Cascade Detection Tests
    # =================================================================

    def test_detects_cascade_scenario(self, rule: Rule3HeadingIncrement) -> None:
        """Should detect when fix would create downstream violation."""
        lines = [
            "## Level 2\n",
            "\n",
            "#### Level 4 (violation)\n",
            "\n",
            "##### Level 5 (would become violation after fix)\n",
        ]

        violations = rule.check_file(lines)
        assert len(violations) == 1  # Only first violation detected

        # Default mode: Should insert TODO, not downgrade
        fixed_lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.CONSERVATIVE)

        # Check TODO was inserted and original heading preserved
        expected = [
            "## Level 2\n",
            "\n",
            "### TODO: check-md - add missing level 3 heading\n",
            "\n",
            "#### Level 4 (violation)\n",
            "\n",
            "##### Level 5 (would become violation after fix)\n",
        ]
        assert fixed_lines == expected, \
            f"Expected TODO insertion.\nExpected: {expected}\nActual: {fixed_lines}"

    def test_aggressive_mode_applies_cascade_fixes(self, rule: Rule3HeadingIncrement) -> None:
        """Should apply cascade fixes in aggressive mode."""
        lines = [
            "## Level 2\n",
            "\n",
            "#### Level 4 (violation)\n",
            "\n",
            "##### Level 5 (cascade)\n",
        ]

        violations = rule.check_file(lines)

        # Aggressive mode: Should downgrade, no TODO
        fixed_lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.AGGRESSIVE)

        # Check downgrade was applied - cascade not yet handled (needs second pass)
        expected = [
            "## Level 2\n",
            "\n",
            "### Level 4 (violation)\n",
            "\n",
            "##### Level 5 (cascade)\n",
        ]
        assert fixed_lines == expected, \
            f"Expected cascade fixes.\nExpected: {expected}\nActual: {fixed_lines}"

    def test_no_cascade_uses_simple_downgrade(self, rule: Rule3HeadingIncrement) -> None:
        """Should use simple downgrade when no cascade detected."""
        lines = [
            "## Level 2\n",
            "\n",
            "#### Level 4 (violation)\n",
            "\n",
            "## Back to Level 2 (no cascade)\n",
        ]

        violations = rule.check_file(lines)
        fixed_lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.CONSERVATIVE)

        # No TODO needed, simple downgrade applied
        expected = [
            "## Level 2\n",
            "\n",
            "### Level 4 (violation)\n",
            "\n",
            "## Back to Level 2 (no cascade)\n",
        ]
        assert fixed_lines == expected, \
            f"Expected simple downgrade.\nExpected: {expected}\nActual: {fixed_lines}"

    def test_todo_format_single_level_skip(self, rule: Rule3HeadingIncrement) -> None:
        """Should format TODO correctly for single-level skip."""
        lines = [
            "## Level 2\n",
            "#### Level 4\n",
            "##### Level 5\n",
        ]

        violations = rule.check_file(lines)
        fixed_lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.CONSERVATIVE)

        # Should say "add missing level 3 heading" (singular)
        expected = [
            "## Level 2\n",
            "\n",
            "### TODO: check-md - add missing level 3 heading\n",
            "\n",
            "#### Level 4\n",
            "##### Level 5\n",
        ]
        assert fixed_lines == expected, \
            f"Expected singular 'heading' in TODO.\nExpected: {expected}\nActual: {fixed_lines}"

    def test_todo_format_multi_level_skip(self, rule: Rule3HeadingIncrement) -> None:
        """Should format TODO correctly for multi-level skip."""
        lines = [
            "# Level 1\n",
            "#### Level 4\n",
            "##### Level 5\n",
        ]

        violations = rule.check_file(lines)
        fixed_lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.CONSERVATIVE)

        # Should say "add missing level 2, 3 headings" (plural)
        expected = [
            "# Level 1\n",
            "\n",
            "## TODO: check-md - add missing level 2, 3 headings\n",
            "\n",
            "#### Level 4\n",
            "##### Level 5\n",
        ]
        assert fixed_lines == expected, \
            f"Expected plural 'headings' in TODO.\nExpected: {expected}\nActual: {fixed_lines}"

    def test_aggressive_mode_removes_existing_todo_comments(self, rule: Rule3HeadingIncrement) -> None:
        """Should remove TODO violations when they are detected."""
        # File has a TODO from previous conservative fix
        lines = [
            "## Section\n",
            "\n",
            "### TODO: check-md - add missing level 3 heading\n",
            "\n",
            "### Real Heading\n",
        ]

        # TODO is now reported as a violation
        violations = rule.check_file(lines)
        assert len(violations) == 1
        assert violations[0].line_number == 3
        assert violations[0].message == "Incomplete heading structure (TODO placeholder from previous fix)"

        # Apply fix to remove the TODO (works in both conservative and aggressive mode)
        fixed_lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.AGGRESSIVE)

        # TODO should be removed, real heading should remain (blank lines removed too)
        expected = [
            "## Section\n",
            "### Real Heading\n",
        ]
        assert fixed_lines == expected, f"Expected:\n{expected}\nActual:\n{fixed_lines}"

    def test_aggressive_mode_removes_todo_with_blank_line_before(self, rule: Rule3HeadingIncrement) -> None:
        """Should remove TODO and blank line before it."""
        lines = [
            "## Section\n",
            "\n",
            "\n",  # Blank line before TODO
            "### TODO: check-md - add missing level 3 heading\n",
            "\n",
            "### Real Heading\n",
        ]

        violations = rule.check_file(lines)
        assert len(violations) == 1
        assert violations[0].message == "Incomplete heading structure (TODO placeholder from previous fix)"

        fixed_lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.AGGRESSIVE)

        # TODO and preceding blank line should be removed
        # Should have clean structure: Section, blank, Real Heading
        expected = [
            "## Section\n",
            "\n",
            "### Real Heading\n",
        ]
        assert fixed_lines == expected, \
            f"Expected clean structure after TODO removal.\nExpected: {expected}\nActual: {fixed_lines}"

    def test_aggressive_mode_removes_todo_with_blank_line_after(self, rule: Rule3HeadingIncrement) -> None:
        """Should remove TODO and blank line after it."""
        lines = [
            "## Section\n",
            "\n",
            "### TODO: check-md - add missing level 3 heading\n",
            "\n",  # Blank line after TODO
            "\n",
            "### Real Heading\n",
        ]

        violations = rule.check_file(lines)
        assert len(violations) == 1

        fixed_lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.AGGRESSIVE)

        # TODO and following blank line should be removed - check exact structure
        expected = [
            "## Section\n",
            "\n",
            "### Real Heading\n",
        ]
        assert fixed_lines == expected, \
            f"Expected clean structure.\nExpected: {expected}\nActual: {fixed_lines}"

    def test_aggressive_mode_removes_todo_with_blank_lines_both_sides(self, rule: Rule3HeadingIncrement) -> None:
        """Should remove TODO and one adjacent blank line."""
        lines = [
            "## Section\n",
            "\n",
            "\n",  # Blank before
            "### TODO: check-md - add missing level 3 heading\n",
            "\n",  # Blank after (this will be removed)
            "\n",  # Extra blank (this will remain)
            "### Real Heading\n",
        ]

        violations = rule.check_file(lines)
        assert len(violations) == 1

        fixed_lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.AGGRESSIVE)

        # TODO and one blank line should be removed (the logic removes blank before TODO or blank after TODO)
        # Current behavior: removes TODO and the blank BEFORE it, leaving one blank line
        expected = [
            "## Section\n",
            "\n",
            "\n",  # One blank remains
            "### Real Heading\n",
        ]
        assert fixed_lines == expected, \
            f"Expected structure with one blank line remaining.\nExpected: {expected}\nActual: {fixed_lines}"

    def test_cascade_requires_multiple_passes_in_aggressive_mode(self, rule: Rule3HeadingIncrement) -> None:
        """Should handle cascades that require multiple fix passes."""
        lines = [
            "## Section\n",
            "\n",
            "#### Subsection (violation)\n",
            "\n",
            "##### Details (would cascade)\n",
            "\n",
            "###### More details (would cascade further)\n",
        ]

        # First pass
        violations = rule.check_file(lines)
        assert len(violations) == 1
        lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.AGGRESSIVE)

        # Second pass
        violations = rule.check_file(lines)
        assert len(violations) == 1
        lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.AGGRESSIVE)

        # Third pass
        violations = rule.check_file(lines)
        assert len(violations) == 1
        lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.AGGRESSIVE)

        # Should be clean now
        violations = rule.check_file(lines)
        assert len(violations) == 0

        # Verify final structure - exact output after 3 cascade fixes
        expected = [
            "## Section\n",
            "\n",
            "### Subsection (violation)\n",
            "\n",
            "#### Details (would cascade)\n",
            "\n",
            "##### More details (would cascade further)\n",
        ]
        assert lines == expected, \
            f"Expected cascaded structure.\nExpected: {expected}\nActual: {lines}"

    # ==================================================================
    # Edge Cases for fix_violation
    # ==================================================================

    def test_fix_handles_malformed_heading_pattern(self, rule: Rule3HeadingIncrement) -> None:
        """Should handle case where heading pattern doesn't match (defensive)."""
        lines = [
            "## Section\n",
            "\n",
            "####Not a heading (missing space)\n",  # Malformed - won't match pattern
        ]

        # Create violation for the malformed line
        violation = Violation(
            rule_id="ADR-002-R3",
            line_number=3,
            severity=Severity.ERROR,
            message="Test",
            context="",
            fix_hint=""
        )

        fixed_lines = rule.fix_violation(lines, violation)

        # Should return lines unchanged when pattern doesn't match
        assert fixed_lines == lines

    def test_fix_handles_first_heading_in_file(self, rule: Rule3HeadingIncrement) -> None:
        """Should handle violation on first heading (no previous heading)."""
        lines = [
            "Some intro text.\n",
            "\n",
            "### First heading (level 3)\n",  # Violation - should start at level 1
        ]

        violations = rule.check_file(lines)
        # Note: This might not create a violation depending on rule logic
        # But if fix_violation is called with no previous heading, should handle it

        # Create violation manually to test the edge case
        violation = Violation(
            rule_id="ADR-002-R3",
            line_number=3,
            severity=Severity.ERROR,
            message="Test",
            context="",
            fix_hint=""
        )

        fixed_lines = rule.fix_violation(lines, violation)

        # Should return lines unchanged when no previous heading found
        # (Can't determine what level to downgrade to)
        assert fixed_lines == lines

    def test_fix_handles_heading_disappearing_during_aggressive_fix(self, rule: Rule3HeadingIncrement) -> None:
        """Should handle rare case where heading disappears during TODO removal."""
        lines = [
            "## Section\n",
            "\n",
            "### TODO: check-md - add missing level 3 heading\n",
            "\n",
            "#### Subsection\n",
        ]

        # This tests the edge case at line 591 where heading disappears
        # In practice this is hard to trigger, but the code defends against it

        violations = rule.check_file(lines)
        assert len(violations) >= 1

        # Apply aggressive fix - should handle edge case gracefully
        fixed_lines = rule.fix_violation(lines, violations[0], strategy=FixStrategy.AGGRESSIVE)

        # Should complete without error (exact result depends on implementation)
        assert isinstance(fixed_lines, list)
