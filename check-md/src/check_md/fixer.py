"""
fixer.py — File fixing functionality for auto-correcting violations.

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

from pathlib import Path
from typing import List

from .formatting import format_violation_display
from .models import FileResult, Violation
from .rules import FixStrategy, Rule, get_all_rules


class FileFixer:
    """Fixes violations in markdown files with backup support."""

    def __init__(self, strategy: FixStrategy = FixStrategy.CONSERVATIVE) -> None:
        """Initialize fixer with rules.

        Args:
            strategy: Fix strategy (CONSERVATIVE or AGGRESSIVE)
        """
        self.rules = {rule.rule_id: rule for rule in get_all_rules()}
        self.strategy = strategy

    def fix_file(
        self, file_path: Path, result: FileResult, create_backup: bool = True
    ) -> int:
        """Fix all violations in a file.

        In aggressive mode, applies fixes iteratively until the file is
        completely clean or max iterations reached. This ensures files with
        cascading violations are fully fixed in a single call.

        In conservative mode, applies fixes once (since conservative mode
        intentionally leaves TODO placeholders for manual review).

        Applies fixes bottom-up (highest line number first) to preserve
        line numbers during fixing.

        Args:
            file_path: Path to file to fix
            result: FileResult with violations to fix
            create_backup: Whether to create .bak file before modifying

        Returns:
            Number of violations fixed

        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read/written
            RuntimeError: If file can't be fixed after max iterations (indicates bug)
        """
        if not result.violations:
            return 0

        # Read file and create backup
        lines = self._read_file(file_path)
        if create_backup:
            self._create_backup(file_path, lines)

        # Determine max iterations based on strategy
        max_iterations = self._get_max_iterations()

        # Apply fixes iteratively
        total_fixed = 0
        for iteration in range(1, max_iterations + 1):
            lines, fixed_count = self._apply_fixes_pass(lines, result)
            total_fixed += fixed_count

            self._write_file(file_path, lines)

            # Conservative mode: single pass only
            if self.strategy == FixStrategy.CONSERVATIVE:
                break

            # Aggressive mode: re-check and continue if needed
            should_continue, result = self._should_continue_fixing(
                file_path, iteration, max_iterations, fixed_count
            )
            if not should_continue:
                break

        return total_fixed

    def _get_max_iterations(self) -> int:
        """Get maximum iterations based on fix strategy.

        Returns:
            6 for aggressive mode (worst case cascade through all heading levels),
            1 for conservative mode
        """
        return 6 if self.strategy == FixStrategy.AGGRESSIVE else 1

    def _apply_fixes_pass(self, lines: List[str], result: FileResult) -> tuple[List[str], int]:
        """Apply fixes for a single pass through violations.

        Args:
            lines: Current file lines
            result: FileResult with violations to fix

        Returns:
            Tuple of (updated lines, number of fixes applied)
        """
        # Sort violations by line number (descending) to preserve line numbers
        sorted_violations = sorted(result.violations, key=lambda v: v.line_number, reverse=True)

        fixed_count = 0
        for violation in sorted_violations:
            rule = self.rules.get(violation.rule_id)
            if rule:
                old_lines = lines.copy()
                lines = rule.fix_violation(lines, violation, strategy=self.strategy)
                if lines != old_lines:
                    fixed_count += 1

        return lines, fixed_count

    def _should_continue_fixing(
        self, file_path: Path, iteration: int, max_iterations: int, fixed_count: int
    ) -> tuple[bool, FileResult]:
        """Check if fixing should continue in aggressive mode.

        Args:
            file_path: Path being fixed
            iteration: Current iteration number
            max_iterations: Maximum allowed iterations
            fixed_count: Number of fixes applied in last pass

        Returns:
            Tuple of (should_continue, updated_result)

        Raises:
            RuntimeError: If fix logic is broken (no fixes applied but violations remain)
            RuntimeError: If max iterations exceeded with violations remaining
        """
        # Re-check for violations
        from .checker import MarkdownChecker

        checker = MarkdownChecker(rules=list(self.rules.values()))
        result = checker.check_file(file_path)

        # If no violations remain, we're done
        if not result.violations:
            return False, result

        # If we didn't fix anything but still have violations, fix logic is broken
        if fixed_count == 0:
            raise RuntimeError(
                f"Unable to fix violations in {file_path} after {iteration} iterations. "
                f"Remaining violations: {len(result.violations)}. "
                f"This indicates a bug in fix logic - fixes are not being applied."
            )

        # Check if we've hit max iterations
        if iteration >= max_iterations:
            raise RuntimeError(
                f"Could not completely fix {file_path} after {max_iterations} iterations. "
                f"Remaining violations: {len(result.violations)}. "
                f"This should not be possible and indicates a bug in fix logic."
            )

        return True, result

    def preview_fixes(self, file_path: Path, result: FileResult) -> List[str]:
        """Preview what fixes would be applied without modifying file.

        Args:
            file_path: Path to file
            result: FileResult with violations

        Returns:
            List of strings describing each fix that would be applied
        """
        if not result.violations:
            return []

        lines = self._read_file(file_path)
        previews: List[str] = []

        # Sort violations by line number (descending)
        sorted_violations = sorted(result.violations, key=lambda v: v.line_number, reverse=True)

        for violation in sorted_violations:
            rule = self.rules.get(violation.rule_id)
            if rule:
                old_lines = lines.copy()
                new_lines = rule.fix_violation(lines, violation, strategy=self.strategy)

                if new_lines != old_lines:
                    # Create a more detailed description
                    # Use shared formatting function for consistency with CLI output
                    formatted = format_violation_display(violation)
                    desc = f"Line {violation.line_number}: {formatted}"
                    if violation.fix_hint:
                        desc += f"\n  Fix: {violation.fix_hint}"

                    previews.append(desc)

                    # Update lines for next iteration
                    lines = new_lines

        return previews

    def _read_file(self, file_path: Path) -> List[str]:
        """Read file preserving line endings.

        Args:
            file_path: Path to file

        Returns:
            List of lines with preserved line endings

        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file can't be read
        """
        with open(file_path, "r", encoding="utf-8", newline="") as f:
            # Read with newline="" to preserve original line endings
            content = f.read()

        # Split into lines but keep line endings
        lines = []
        for line in content.splitlines(keepends=True):
            lines.append(line)

        # Handle case where file doesn't end with newline
        if content and not content.endswith(("\n", "\r\n", "\r")):
            # Last line has no line ending
            pass  # Already handled by splitlines(keepends=True)

        return lines

    def _write_file(self, file_path: Path, lines: List[str]) -> None:
        """Write file preserving line endings.

        Args:
            file_path: Path to file
            lines: Lines to write (with preserved line endings)

        Raises:
            PermissionError: If file can't be written
        """
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            f.writelines(lines)

    def _create_backup(self, file_path: Path, lines: List[str]) -> None:
        """Create backup file with .bak extension.

        Args:
            file_path: Original file path
            lines: Lines to back up

        Raises:
            PermissionError: If backup can't be created
        """
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        self._write_file(backup_path, lines)

    def rollback_file(self, file_path: Path) -> bool:
        """Restore file from backup.

        Args:
            file_path: Path to file to restore

        Returns:
            True if rollback successful, False if no backup exists

        Raises:
            PermissionError: If file can't be written
        """
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        if not backup_path.exists():
            return False

        # Read backup
        backup_lines = self._read_file(backup_path)

        # Restore original
        self._write_file(file_path, backup_lines)

        # Remove backup
        backup_path.unlink()

        return True

    def clean_backup(self, file_path: Path) -> bool:
        """Remove backup file.

        Args:
            file_path: Path to original file

        Returns:
            True if backup was removed, False if no backup exists
        """
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        if not backup_path.exists():
            return False

        backup_path.unlink()
        return True

    def has_backup(self, file_path: Path) -> bool:
        """Check if backup file exists.

        Args:
            file_path: Path to original file

        Returns:
            True if .bak file exists
        """
        backup_path = file_path.with_suffix(file_path.suffix + ".bak")
        return backup_path.exists()
