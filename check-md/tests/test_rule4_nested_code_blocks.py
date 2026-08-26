"""
test_rule4_nested_code_blocks.py — Tests for Rule 4: Nested Code Blocks.

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

import pytest

from check_md.models import Severity
from check_md.rules import Rule4NestedCodeBlocks


@pytest.fixture
def rule() -> Rule4NestedCodeBlocks:
    """Create rule instance for testing."""
    return Rule4NestedCodeBlocks()


class TestRule4NestedCodeBlocks:
    """Test suite for Rule 4: Nested Code Blocks."""

    def test_detects_nested_code_block_with_same_fence(
        self, rule: Rule4NestedCodeBlocks
    ) -> None:
        """Should detect nested code block using same fence length."""
        lines = [
            "Outer block:",
            "",
            "```markdown",
            "Inner block:",
            "```python",
            "code",
            "```",
            "```",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1
        assert violations[0].rule_id == "ADR-002-R4"
        assert violations[0].line_number == 3  # Points to outer block
        assert violations[0].severity == Severity.ERROR
        assert "nested code block" in violations[0].message.lower()
        assert "5" in violations[0].message  # Inner block at line 5

    def test_suggests_longer_fence(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should suggest using longer fence for outer block."""
        lines = [
            "```markdown",
            "```python",
            "code",
            "```",
            "```",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1
        assert "4 backticks" in violations[0].fix_hint

    def test_allows_proper_nested_code_blocks(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should not flag when outer fence is longer than inner."""
        lines = [
            "````markdown",
            "Inner block:",
            "```python",
            "code",
            "```",
            "````",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_allows_non_nested_code_blocks(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should not flag separate (non-nested) code blocks."""
        lines = [
            "```python",
            "code1",
            "```",
            "",
            "```python",
            "code2",
            "```",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_handles_deeply_nested_blocks(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should detect violations in deeply nested blocks."""
        lines = [
            "`````markdown",
            "````markdown",
            "```python",
            "code",
            "```",
            "````",
            "`````",
        ]

        violations = rule.check_file(lines)

        # Should be valid (each level uses longer fence)
        assert len(violations) == 0

    def test_detects_multiple_nested_violations(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should detect multiple nested code block violations."""
        lines = [
            "```markdown",
            "```python",
            "code",
            "```",
            "```",
            "",
            "```markdown",
            "```java",
            "code",
            "```",
            "```",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 2
        assert violations[0].line_number == 1
        assert violations[1].line_number == 7

    def test_handles_four_backtick_fences(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should handle code blocks with 4+ backticks."""
        lines = [
            "````markdown",
            "```python",
            "code",
            "```",
            "````",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_handles_five_backtick_fences(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should handle code blocks with 5+ backticks."""
        lines = [
            "`````markdown",
            "````markdown",
            "```python",
            "code",
            "```",
            "````",
            "`````",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_detects_equal_length_inner_fence(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should detect when inner fence equals outer fence length."""
        lines = [
            "````markdown",
            "````python",  # Equal length - this is a violation
            "code",
            "````",
            "````",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 1
        assert violations[0].line_number == 1

    def test_handles_unclosed_code_blocks(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should handle files with unclosed code blocks gracefully."""
        lines = [
            "```markdown",
            "```python",
            "code",
            # Missing closing fences
        ]

        # Should not crash, but may detect violations
        violations = rule.check_file(lines)

        # Implementation detail: unclosed blocks are treated as nested
        assert isinstance(violations, list)

    def test_ignores_inline_code(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should ignore inline code (`code`) - only check fenced blocks."""
        lines = [
            "This text has `inline code` with backticks.",
            "And more `code` here.",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_handles_code_fences_with_language_specifier(
        self, rule: Rule4NestedCodeBlocks
    ) -> None:
        """Should properly parse fences with language specifiers."""
        lines = [
            "````markdown",
            "```python",
            "print('hello')",
            "```",
            "````",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0

    def test_real_world_example_from_goals(self, rule: Rule4NestedCodeBlocks) -> None:
        """Should handle real-world example from goals.md."""
        lines = [
            "Example:",
            "",
            "`````markdown",
            "Here's the correct format:",
            "",
            "````markdown",
            "```kotlin",
            "fun example() {}",
            "```",
            "````",
            "`````",
        ]

        violations = rule.check_file(lines)

        assert len(violations) == 0
