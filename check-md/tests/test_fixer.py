"""
test_fixer.py — Tests for file fixing functionality.

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
from dataclasses import dataclass
from pathlib import Path

import pytest

from check_md.checker import MarkdownChecker
from check_md.fixer import FileFixer
from check_md.models import FileResult, Severity, Violation


@dataclass
class FixTestCase:
    """Test case for file fixing (mirrors Kotlin TestCase pattern)."""

    input_content: str
    expected_content: str
    expected_fixed_count: int
    create_backup: bool = False
    expected_previews: list = None  # Exact preview strings expected

    def __post_init__(self):
        if self.expected_previews is None:
            self.expected_previews = []


class TestFileFixer:
    """Tests for FileFixer class basic functionality."""

    @pytest.mark.parametrize("test_case", [
        pytest.param(
            FixTestCase(
                input_content="# Test\n\nNo violations here.\n",
                expected_content="# Test\n\nNo violations here.\n",
                expected_fixed_count=0,
                expected_previews=[]
            ),
            id="no_violations"
        ),
        pytest.param(
            FixTestCase(
                input_content="# Test\n\n**Bold Heading**\n",
                expected_content="# Test\n\n## Bold Heading\n",
                expected_fixed_count=2,  # R1 fix (bold → heading) + R3 fix (#### → ##) in multi-pass
                expected_previews=[
                    "Line 3: Standalone bold text should be a heading [Rule 1]\n  Fix: Replace with: ## Bold Heading"
                ]
            ),
            id="single_bold_heading"
        ),
        pytest.param(
            FixTestCase(
                input_content="# Test\n\n**Bold**\n",
                expected_content="# Test\n\n## Bold\n",
                expected_fixed_count=2,  # R1 fix (bold → heading) + R3 fix (#### → ##) in multi-pass
                expected_previews=[
                    "Line 3: Standalone bold text should be a heading [Rule 1]\n  Fix: Replace with: ## Bold"
                ]
            ),
            id="preserves_line_endings"
        ),
        pytest.param(
            FixTestCase(
                input_content="# Test\n\n**Bold Heading**\n",
                expected_content="# Test\n\n## Bold Heading\n",
                expected_fixed_count=2,
                create_backup=True,
                expected_previews=[
                    "Line 3: Standalone bold text should be a heading [Rule 1]\n  Fix: Replace with: ## Bold Heading"
                ]
            ),
            id="creates_backup_with_original_content"
        ),
        pytest.param(
            FixTestCase(
                input_content="# Test\n\n**Bold One**\n\n**Bold Two**\n",
                expected_content="# Test\n\n## Bold One\n\n### Bold Two\n",
                expected_fixed_count=4,  # Pass 1: R1 fixes both (→ ####), Pass 2: R3 downgrades first (→ ##), Pass 3: R3 downgrades second (→ ###)
                expected_previews=[
                    "Line 5: Standalone bold text should be a heading [Rule 1]\n  Fix: Replace with: ## Bold Two",
                    "Line 3: Standalone bold text should be a heading [Rule 1]\n  Fix: Replace with: ## Bold One"
                ]
            ),
            id="multiple_violations_multiple_passes"
        ),
        pytest.param(
            FixTestCase(
                input_content="# Test\n\n**Section:**\n",
                expected_content="# Test\n\n## Section\n",
                expected_fixed_count=2,  # R1 fix (bold with colon → ####), R3 fix (#### → ##)
                expected_previews=[
                    "Line 3: Standalone bold text should be a heading [Rule 1]\n  Fix: Replace with: ## Section:"
                ]
            ),
            id="colon_inside_bold"
        ),
        pytest.param(
            FixTestCase(
                input_content="# Test\n\n**Section**:\n",
                expected_content="# Test\n\n## Section\n",
                expected_fixed_count=2,  # R1 fix (bold with colon → ####), R3 fix (#### → ##)
                expected_previews=[
                    "Line 3: Standalone bold text should be a heading [Rule 1]\n  Fix: Replace with: ## Section"
                ]
            ),
            id="colon_outside_bold"
        ),
        pytest.param(
            FixTestCase(
                input_content="# Test\n\n**Label:** Some text here.\n",
                expected_content="# Test\n\n**Label:** Some text here.\n",
                expected_fixed_count=0,  # NOT a violation - inline label-value pair
                expected_previews=[]
            ),
            id="inline_label_value_not_violation"
        ),
        pytest.param(
            FixTestCase(
                input_content="# Test\n\n**Label**: Some text here.\n",
                expected_content="# Test\n\n**Label**: Some text here.\n",
                expected_fixed_count=0,  # NOT a violation - inline label-value pair
                expected_previews=[]
            ),
            id="inline_label_value_colon_outside_not_violation"
        ),
        pytest.param(
            FixTestCase(
                input_content="# Top\n\n##### Details\n",
                expected_content="# Top\n\n## Details\n",
                expected_fixed_count=1,  # Single pass: downgrade ##### to ##
                expected_previews=[
                    "Line 3: Heading level increased by 4 (from # to #####) [Rule 3]\n  Fix: Change ##### to ## or add intermediate ## heading"
                ]
            ),
            id="skip_four_levels"
        ),
        pytest.param(
            FixTestCase(
                input_content="## Section\n\n#### Subsection\n",
                expected_content="## Section\n\n### Subsection\n",
                expected_fixed_count=1,  # Single pass: just downgrade #### to ###
                expected_previews=[
                    "Line 3: Heading level increased by 2 (from ## to ####) [Rule 3]\n  Fix: Change #### to ### or add intermediate ### heading"
                ]
            ),
            id="single_pass_simple_downgrade"
        ),
        pytest.param(
            FixTestCase(
                input_content="## Section\n\n#### Subsection\n\n##### Details\n",
                expected_content="## Section\n\n### Subsection\n\n#### Details\n",
                expected_fixed_count=2,  # Two passes: #### → ###, then ##### → ####
                expected_previews=[
                    "Line 3: Heading level increased by 2 (from ## to ####) [Rule 3]\n  Fix: Change #### to ### or add intermediate ### heading"
                ]
            ),
            id="two_pass_cascade"
        ),
        pytest.param(
            FixTestCase(
                input_content="## Section\n\n#### Subsection\n\n##### Details\n\n###### More\n",
                expected_content="## Section\n\n### Subsection\n\n#### Details\n\n##### More\n",
                expected_fixed_count=3,  # Three passes: #### → ###, ##### → ####, ###### → #####
                expected_previews=[
                    "Line 3: Heading level increased by 2 (from ## to ####) [Rule 3]\n  Fix: Change #### to ### or add intermediate ### heading"
                ]
            ),
            id="three_pass_cascade"
        ),
    ])
    def test_fix_file(self, test_case: FixTestCase) -> None:
        """Parameterized test for fix_file behavior."""
        from check_md.rules import FixStrategy

        fixer = FileFixer(strategy=FixStrategy.AGGRESSIVE)
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, newline="") as f:
            f.write(test_case.input_content)
            temp_path = Path(f.name)

        backup_path = temp_path.with_suffix(temp_path.suffix + ".bak")

        try:
            # Get violations
            result = checker.check_file(temp_path)

            # Test preview (before modifying file)
            previews = fixer.preview_fixes(temp_path, result)

            # Verify exact preview match
            assert previews == test_case.expected_previews, \
                f"Expected previews:\n{test_case.expected_previews}\nActual:\n{previews}"

            # Verify preview doesn't modify file
            assert temp_path.read_text() == test_case.input_content, "Preview modified the file"

            # Apply fixes (with or without backup based on test case)
            fixed_count = fixer.fix_file(temp_path, result, create_backup=test_case.create_backup)

            # Verify fix count
            assert fixed_count == test_case.expected_fixed_count, \
                f"Expected {test_case.expected_fixed_count} fixes, got {fixed_count}"

            # Verify exact content match
            actual_content = temp_path.read_text()
            assert actual_content == test_case.expected_content, \
                f"Expected:\n{test_case.expected_content}\nActual:\n{actual_content}"

            # Verify backup if expected
            if test_case.create_backup:
                assert backup_path.exists(), "Expected backup file to exist"
                backup_content = backup_path.read_text()
                assert backup_content == test_case.input_content, \
                    f"Expected backup to contain original:\n{test_case.input_content}\nActual:\n{backup_content}"
            else:
                assert not backup_path.exists(), "Expected no backup file"

            # Verify no violations remain after fix
            result_after = checker.check_file(temp_path)
            assert len(result_after.violations) == 0, (
                f"Expected 0 violations after fix, got {len(result_after.violations)}: "
                f"{[v.message for v in result_after.violations]}"
            )

            # Verify line endings preserved (LF only, no CRLF)
            content_bytes = temp_path.read_bytes()
            assert b"\r\n" not in content_bytes, "Found CRLF line endings"
        finally:
            temp_path.unlink(missing_ok=True)
            backup_path.unlink(missing_ok=True)


class TestRule1Fixes:
    """Tests for Rule 1 (Semantic Headings) fixes."""

    def test_fix_standalone_bold(self) -> None:
        """Should convert standalone bold to heading."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\n**Section Title**\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)

            assert fixed_count == 1
            content = temp_path.read_text()
            assert "#### Section Title" in content
            assert "**Section Title**" not in content
        finally:
            temp_path.unlink()

    def test_fix_bold_with_colon(self) -> None:
        """Should convert standalone bold with colon to heading, but NOT inline labels."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            # This is an inline label-value pair and should NOT be converted
            f.write("# Test\n\n**Label:** This is some text.\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)

            # Inline label should NOT be fixed (no violations found)
            assert fixed_count == 0
            content = temp_path.read_text()
            # Original content should be preserved
            assert "**Label:** This is some text." in content
            assert "#### Label" not in content
        finally:
            temp_path.unlink()

    def test_fix_removes_trailing_colon(self) -> None:
        """Should remove trailing colon from converted heading."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\n**Section:**\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            fixer.fix_file(temp_path, result, create_backup=False)

            content = temp_path.read_text()
            assert "#### Section" in content
            assert "Section:" not in content  # Colon removed
        finally:
            temp_path.unlink()

    def test_fix_multiple_bold_headings(self) -> None:
        """Should fix multiple bold headings in same file."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\n**First**\n\nText.\n\n**Second**\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)

            assert fixed_count == 2
            content = temp_path.read_text()
            assert "#### First" in content
            assert "#### Second" in content
        finally:
            temp_path.unlink()


class TestRule2Fixes:
    """Tests for Rule 2 (Block Separation) fixes."""

    def test_fix_missing_blank_before_list(self) -> None:
        """Should insert blank line before list."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\nSome text\n- List item\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)

            assert fixed_count == 1
            content = temp_path.read_text()
            lines = content.split("\n")
            # Find "Some text" and verify blank line follows
            text_idx = lines.index("Some text")
            assert lines[text_idx + 1] == ""  # Blank line
            assert lines[text_idx + 2] == "- List item"
        finally:
            temp_path.unlink()

    def test_fix_missing_blank_before_code_block(self) -> None:
        """Should insert blank line before code block."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\nText here\n```python\ncode\n```\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)

            assert fixed_count == 1
            content = temp_path.read_text()
            lines = content.split("\n")
            text_idx = lines.index("Text here")
            assert lines[text_idx + 1] == ""  # Blank line
            assert lines[text_idx + 2] == "```python"
        finally:
            temp_path.unlink()

    def test_fix_multiple_block_separations(self) -> None:
        """Should fix multiple missing blank lines."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("Text\n- List\n\nMore text\n```\ncode\n```\n")
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)

            assert fixed_count == 2  # Before list and before code
            content = temp_path.read_text()
            # Verify blank lines were inserted
            assert "Text\n\n- List" in content
            assert "More text\n\n```" in content
        finally:
            temp_path.unlink()


class TestRule4Fixes:
    """Tests for Rule 4 (Nested Code Blocks) fixes."""

    def test_fix_nested_code_block_simple(self) -> None:
        """Should increase outer fence length for nested block."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                "# Test\n\n"
                "```markdown\n"
                "Example:\n"
                "```bash\n"
                "command\n"
                "```\n"
                "```\n"
            )
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)

            # Should fix the violation
            assert fixed_count >= 1

            content = temp_path.read_text()
            # Outer fences should now be 4 backticks
            assert "````markdown" in content
            assert "````\n" in content or content.endswith("````")
            # Inner fence stays at 3
            assert "```bash" in content
        finally:
            temp_path.unlink()


class TestBackupManagement:
    """Tests for backup management features."""

    def test_has_backup_true(self) -> None:
        """Should return True when backup exists."""
        fixer = FileFixer()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n")
            temp_path = Path(f.name)

        try:
            # Create backup
            backup_path = temp_path.with_suffix(temp_path.suffix + ".bak")
            backup_path.write_text("# Backup\n")

            assert fixer.has_backup(temp_path) is True

            backup_path.unlink()
        finally:
            temp_path.unlink()

    def test_has_backup_false(self) -> None:
        """Should return False when no backup exists."""
        fixer = FileFixer()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n")
            temp_path = Path(f.name)

        try:
            assert fixer.has_backup(temp_path) is False
        finally:
            temp_path.unlink()

    def test_rollback_file_success(self) -> None:
        """Should restore from backup and remove backup file."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            original_content = "# Test\n\n**Bold**\n"
            f.write(original_content)
            temp_path = Path(f.name)

        try:
            # Fix file (creates backup)
            result = checker.check_file(temp_path)
            fixer.fix_file(temp_path, result, create_backup=True)

            # Verify file was modified
            modified_content = temp_path.read_text()
            assert modified_content != original_content

            # Rollback
            rollback_success = fixer.rollback_file(temp_path)
            assert rollback_success is True

            # Verify restored to original
            restored_content = temp_path.read_text()
            assert restored_content == original_content

            # Verify backup removed
            backup_path = temp_path.with_suffix(temp_path.suffix + ".bak")
            assert not backup_path.exists()
        finally:
            temp_path.unlink(missing_ok=True)

    def test_rollback_file_no_backup(self) -> None:
        """Should return False when no backup exists."""
        fixer = FileFixer()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n")
            temp_path = Path(f.name)

        try:
            rollback_success = fixer.rollback_file(temp_path)
            assert rollback_success is False
        finally:
            temp_path.unlink()

    def test_clean_backup_success(self) -> None:
        """Should remove backup file."""
        fixer = FileFixer()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n")
            temp_path = Path(f.name)

        try:
            # Create backup
            backup_path = temp_path.with_suffix(temp_path.suffix + ".bak")
            backup_path.write_text("# Backup\n")

            # Clean backup
            clean_success = fixer.clean_backup(temp_path)
            assert clean_success is True
            assert not backup_path.exists()
        finally:
            temp_path.unlink()

    def test_clean_backup_no_backup(self) -> None:
        """Should return False when no backup exists."""
        fixer = FileFixer()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n")
            temp_path = Path(f.name)

        try:
            clean_success = fixer.clean_backup(temp_path)
            assert clean_success is False
        finally:
            temp_path.unlink()


class TestComplexFixes:
    """Tests for complex fix scenarios."""

    def test_fix_combines_multiple_rule_violations(self) -> None:
        """Should fix violations from multiple rules in same file."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                "# Test\n\n"
                "**Bold Heading**\n\n"
                "Text\n"
                "- List\n"
            )
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)

            # Rule 1 (bold) + Rule 2 (list)
            assert fixed_count == 2

            content = temp_path.read_text()
            assert "#### Bold Heading" in content
            assert "Text\n\n- List" in content
        finally:
            temp_path.unlink()

    def test_bottom_up_fixing_preserves_line_numbers(self) -> None:
        """Should fix from bottom up to preserve line numbers."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                "Text1\n"
                "- List1\n\n"
                "Text2\n"
                "- List2\n\n"
                "Text3\n"
                "- List3\n"
            )
            temp_path = Path(f.name)

        try:
            result = checker.check_file(temp_path)
            # Should have violations on lines 2, 5, 8
            assert len(result.violations) == 3

            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)
            assert fixed_count == 3

            # All lists should now have blank lines before them
            content = temp_path.read_text()
            assert "Text1\n\n- List1" in content
            assert "Text2\n\n- List2" in content
            assert "Text3\n\n- List3" in content
        finally:
            temp_path.unlink()

    def test_integration_with_checker(self) -> None:
        """Should successfully fix real violations found by checker."""
        fixer = FileFixer()
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                "# Document\n\n"
                "**Important**\n\n"
                "Paragraph text here.\n"
                "- Item 1\n"
                "- Item 2\n\n"
                "More text\n"
                "```python\n"
                "code\n"
                "```\n"
            )
            temp_path = Path(f.name)

        try:
            # Initial check
            result_before = checker.check_file(temp_path)
            initial_violations = len(result_before.violations)
            assert initial_violations > 0

            # Fix
            fixer.fix_file(temp_path, result_before, create_backup=False)

            # Re-check
            result_after = checker.check_file(temp_path)
            final_violations = len(result_after.violations)

            # Should have fewer violations (ideally 0)
            assert final_violations < initial_violations
        finally:
            temp_path.unlink()


class TestRule3CascadeIntegration:
    """Integration tests for Rule 3 cascade handling with FileFixer."""

    def test_conservative_mode_inserts_todo_for_cascade(self) -> None:
        """Should insert TODO heading when cascade is detected in conservative mode."""
        from check_md.rules import FixStrategy

        fixer = FileFixer(strategy=FixStrategy.CONSERVATIVE)
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                "## Section\n"
                "\n"
                "#### Subsection (violation)\n"
                "\n"
                "##### Details (would cascade)\n"
            )
            temp_path = Path(f.name)

        try:
            # Check for violations
            result = checker.check_file(temp_path)
            assert len(result.violations) == 1
            assert result.violations[0].line_number == 3

            # Fix in conservative mode
            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)
            assert fixed_count == 1

            # Should have inserted TODO
            content = temp_path.read_text()
            assert "TODO: check-md" in content
            assert "#### Subsection" in content  # Original preserved

            # Re-check: Now has 2 violations (TODO + original structure issue)
            # This is intentional - conservative mode nags user to fix structure
            result_after = checker.check_file(temp_path)
            assert len(result_after.violations) == 2

            # First violation is the TODO
            assert "TODO placeholder" in result_after.violations[0].message
            assert result_after.violations[0].line_number == 3

            # Second violation is the original structure issue (still present)
            assert "increased by 2" in result_after.violations[1].message
            assert result_after.violations[1].line_number == 5
        finally:
            temp_path.unlink()

    def test_aggressive_mode_applies_cascades(self) -> None:
        """Should apply cascade fixes in aggressive mode in a single call."""
        from check_md.rules import FixStrategy

        fixer = FileFixer(strategy=FixStrategy.AGGRESSIVE)
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                "## Section\n"
                "\n"
                "#### Subsection (violation)\n"
                "\n"
                "##### Details (cascade)\n"
                "\n"
                "###### More (cascade)\n"
            )
            temp_path = Path(f.name)

        try:
            # Check violations
            result = checker.check_file(temp_path)
            assert len(result.violations) == 1

            # Single fix call should handle all cascades
            fixer.fix_file(temp_path, result, create_backup=False)

            # Should be clean now (no manual re-runs needed!)
            result_final = checker.check_file(temp_path)
            assert len(result_final.violations) == 0

            # Verify cascades were applied
            content = temp_path.read_text()
            assert "### Subsection" in content
            assert "#### Details" in content
            assert "##### More" in content
            assert "TODO" not in content
        finally:
            temp_path.unlink()

    def test_todo_removal_workflow(self) -> None:
        """Should remove TODO violations when fixed."""
        from check_md.rules import FixStrategy

        fixer = FileFixer(strategy=FixStrategy.CONSERVATIVE)
        checker = MarkdownChecker()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                "## Section\n"
                "\n"
                "### TODO: check-md - add missing level 3 heading\n"
                "\n"
                "### Real Heading\n"
            )
            temp_path = Path(f.name)

        try:
            # Check: TODO is a violation
            result = checker.check_file(temp_path)
            assert len(result.violations) == 1
            assert "TODO placeholder" in result.violations[0].message

            # Fix: removes TODO
            fixed_count = fixer.fix_file(temp_path, result, create_backup=False)
            assert fixed_count == 1

            # Re-check: should be clean
            result_after = checker.check_file(temp_path)
            assert len(result_after.violations) == 0

            # Verify TODO was removed
            content = temp_path.read_text()
            assert "TODO" not in content
            assert "### Real Heading" in content
        finally:
            temp_path.unlink()

    def test_preview_fixes_with_no_violations(self) -> None:
        """Should return empty list when no violations to preview."""
        fixer = FileFixer()
        result = FileResult(file_path="test.md", violations=[], total_lines=10)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\nNo violations here.\n")
            temp_path = Path(f.name)

        try:
            previews = fixer.preview_fixes(temp_path, result)
            assert previews == []
        finally:
            temp_path.unlink()

    def test_read_file_without_newline_ending(self) -> None:
        """Should handle files without newline at end correctly."""
        fixer = FileFixer()

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            # Write file without trailing newline
            f.write("# Test")
            temp_path = Path(f.name)

        try:
            lines = fixer._read_file(temp_path)
            assert len(lines) == 1
            assert lines[0] == "# Test"
        finally:
            temp_path.unlink()

