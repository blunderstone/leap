"""
models.py — Data models for check-md violations and results.

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

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Severity(Enum):
    """Violation severity levels."""

    ERROR = "error"
    WARNING = "warning"


@dataclass
class Violation:
    """Represents a single Markdown formatting violation.

    Attributes:
        rule_id: Rule identifier (e.g., "ADR-002-R1")
        line_number: Line number where violation occurs (1-indexed)
        severity: Violation severity (ERROR or WARNING)
        message: Human-readable description of the violation
        context: The offending line or relevant snippet
        fix_hint: Optional suggestion for auto-fix
    """

    rule_id: str
    line_number: int
    severity: Severity
    message: str
    context: str
    fix_hint: Optional[str] = None

    def __str__(self) -> str:
        """Format violation for display.

        Returns:
            Human-readable string representation with line number, severity,
            message, context, and optional fix hint.
        """
        severity_str = "ERROR" if self.severity == Severity.ERROR else "WARNING"
        fix = f"\n  Hint: {self.fix_hint}" if self.fix_hint else ""

        # Convert rule_id like "ADR-002-R1" to "Rule 1"
        rule_display = self._format_rule_id(self.rule_id)

        return (
            f"  Line {self.line_number}: [{rule_display}] {severity_str}\n"
            f"    {self.message}\n"
            f"    Context: {self.context[:80]}{fix}"
        )

    def _format_rule_id(self, rule_id: str) -> str:
        """Format rule ID for user-friendly display.

        Converts "ADR-002-R1" to "Rule 1", "ADR-002-R2" to "Rule 2", etc.

        Args:
            rule_id: Internal rule identifier

        Returns:
            User-friendly rule label
        """
        # Extract rule number from patterns like "ADR-002-R1"
        import re
        match = re.search(r'R(\d+)$', rule_id)
        if match:
            rule_num = match.group(1)
            return f"Rule {rule_num}"
        # Fallback to original if pattern doesn't match
        return rule_id


@dataclass
class FileResult:
    """Results from checking a single file.

    Attributes:
        file_path: Path to the checked file
        violations: List of violations found in the file
        total_lines: Total number of lines in the file
    """

    file_path: str
    violations: list[Violation]
    total_lines: int

    @property
    def has_violations(self) -> bool:
        """Check if file has any violations.

        Returns:
            True if violations were found, False otherwise
        """
        return len(self.violations) > 0

    @property
    def error_count(self) -> int:
        """Count ERROR severity violations.

        Returns:
            Number of ERROR severity violations
        """
        return sum(1 for v in self.violations if v.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        """Count WARNING severity violations.

        Returns:
            Number of WARNING severity violations
        """
        return sum(1 for v in self.violations if v.severity == Severity.WARNING)


@dataclass
class LineContext:
    """Context information for checking a single line.

    Provides the line being checked along with surrounding context
    and state information needed for rules to make decisions.

    Attributes:
        line_number: Line number (1-indexed)
        line: The line content
        prev_line: Previous line content (None if first line)
        next_line: Next line content (None if last line)
        in_code_block: Whether this line is inside a code block
        code_block_fence: The fence that opened current code block (e.g., "```" or "````")
    """

    line_number: int
    line: str
    prev_line: Optional[str] = None
    next_line: Optional[str] = None
    in_code_block: bool = False
    code_block_fence: Optional[str] = None


@dataclass
class FileScore:
    """Compliance score for a single file.

    Attributes:
        file_path: Path to the file
        score: Compliance score (0-100)
        total_lines: Total number of lines
        violation_lines: Number of lines with violations
        violations: List of violations
    """

    file_path: str
    score: float
    total_lines: int
    violation_lines: int
    violations: list[Violation]

    @staticmethod
    def from_file_result(result: FileResult) -> "FileScore":
        """Create FileScore from FileResult.

        Args:
            result: FileResult to score

        Returns:
            FileScore with calculated compliance score
        """
        # Count unique lines with violations
        violation_lines = len(set(v.line_number for v in result.violations))

        # Calculate score: (clean_lines / total_lines) * 100
        if result.total_lines == 0:
            score = 100.0
        else:
            score = ((result.total_lines - violation_lines) / result.total_lines) * 100

        return FileScore(
            file_path=result.file_path,
            score=score,
            total_lines=result.total_lines,
            violation_lines=violation_lines,
            violations=result.violations,
        )


@dataclass
class ModuleScore:
    """Compliance score for a module (directory).

    Attributes:
        module_path: Path to the module directory
        score: Average score of all files in module
        file_count: Number of files in module
        violation_count: Total violations across all files
        file_scores: List of FileScore objects for files in this module
    """

    module_path: str
    score: float
    file_count: int
    violation_count: int
    file_scores: list[FileScore]


@dataclass
class ProjectScore:
    """Compliance score for entire project.

    Attributes:
        score: Weighted average score across all files
        total_files: Total number of files checked
        total_lines: Total number of lines scanned
        total_violations: Total number of violations
        module_scores: List of ModuleScore objects by module
        violations_by_rule: Dict mapping rule_id to count
    """

    score: float
    total_files: int
    total_lines: int
    total_violations: int
    module_scores: list[ModuleScore]
    violations_by_rule: dict[str, int]
