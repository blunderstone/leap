"""
Tests for compliance scoring functionality.

Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)
"""

import pytest

from check_md.models import FileResult, Severity, Violation
from check_md.scorer import (
    calculate_file_scores,
    calculate_module_score,
    calculate_project_score,
    calculate_violations_by_rule,
    format_score_indicator,
    group_by_module,
)


def test_calculate_file_scores_empty_list() -> None:
    """Should return empty list for empty input."""
    results = calculate_file_scores([])
    assert results == []


def test_calculate_file_scores_single_file() -> None:
    """Should calculate score for single file."""
    # Given: File with 10 lines, 2 violations on different lines
    result = FileResult(
        file_path="test.md",
        violations=[
            Violation("R1", 1, Severity.ERROR, "Error 1", "context"),
            Violation("R1", 5, Severity.ERROR, "Error 2", "context"),
        ],
        total_lines=10,
    )

    # When
    scores = calculate_file_scores([result])

    # Then
    assert len(scores) == 1
    assert scores[0].file_path == "test.md"
    assert scores[0].score == 80.0  # 8 clean lines out of 10 = 80%
    assert scores[0].total_lines == 10
    assert scores[0].violation_lines == 2


def test_calculate_file_scores_perfect_file() -> None:
    """Should give 100% score for file with no violations."""
    # Given: Perfect file
    result = FileResult(file_path="perfect.md", violations=[], total_lines=20)

    # When
    scores = calculate_file_scores([result])

    # Then
    assert scores[0].score == 100.0
    assert scores[0].violation_lines == 0


def test_calculate_file_scores_multiple_violations_same_line() -> None:
    """Should count line once even with multiple violations."""
    # Given: 2 violations on same line
    result = FileResult(
        file_path="test.md",
        violations=[
            Violation("R1", 5, Severity.ERROR, "Error 1", "context"),
            Violation("R2", 5, Severity.WARNING, "Warning 1", "context"),
        ],
        total_lines=10,
    )

    # When
    scores = calculate_file_scores([result])

    # Then
    assert scores[0].violation_lines == 1  # Only count line 5 once
    assert scores[0].score == 90.0  # 9 clean lines out of 10


def test_group_by_module_single_directory() -> None:
    """Should group files in same directory together."""
    # Given: Two files in same directory
    from check_md.models import FileScore

    scores = [
        FileScore("kb/adr/file1.md", 85.0, 100, 15, []),
        FileScore("kb/adr/file2.md", 90.0, 100, 10, []),
    ]

    # When
    modules = group_by_module(scores)

    # Then
    assert len(modules) == 1
    assert "kb/adr" in modules
    assert len(modules["kb/adr"]) == 2


def test_group_by_module_multiple_directories() -> None:
    """Should separate files in different directories."""
    # Given: Files in different directories
    from check_md.models import FileScore

    scores = [
        FileScore("kb/adr/file1.md", 85.0, 100, 15, []),
        FileScore("kb/feature/file2.md", 90.0, 100, 10, []),
        FileScore("kb/meta/file3.md", 95.0, 100, 5, []),
    ]

    # When
    modules = group_by_module(scores)

    # Then
    assert len(modules) == 3
    assert "kb/adr" in modules
    assert "kb/feature" in modules
    assert "kb/meta" in modules


def test_calculate_module_score_empty_module() -> None:
    """Should handle empty module gracefully."""
    # When
    module = calculate_module_score("empty/", [])

    # Then
    assert module.module_path == "empty/"
    assert module.score == 100.0
    assert module.file_count == 0
    assert module.violation_count == 0


def test_calculate_module_score_single_file() -> None:
    """Should calculate module score from single file."""
    # Given
    from check_md.models import FileScore, Violation

    violations = [Violation("R1", 1, Severity.ERROR, "Error", "context")]
    file_score = FileScore("kb/adr/file.md", 80.0, 100, 20, violations)

    # When
    module = calculate_module_score("kb/adr", [file_score])

    # Then
    assert module.module_path == "kb/adr"
    assert module.score == 80.0
    assert module.file_count == 1
    assert module.violation_count == 1


def test_calculate_module_score_multiple_files() -> None:
    """Should average scores across multiple files."""
    # Given
    from check_md.models import FileScore, Violation

    v1 = [Violation("R1", 1, Severity.ERROR, "Error 1", "context")]
    v2 = [
        Violation("R1", 1, Severity.ERROR, "Error 2", "context"),
        Violation("R2", 2, Severity.ERROR, "Error 3", "context"),
    ]

    file_scores = [
        FileScore("kb/adr/file1.md", 80.0, 100, 20, v1),
        FileScore("kb/adr/file2.md", 90.0, 100, 10, v2),
        FileScore("kb/adr/file3.md", 100.0, 100, 0, []),
    ]

    # When
    module = calculate_module_score("kb/adr", file_scores)

    # Then
    assert module.module_path == "kb/adr"
    assert module.score == 90.0  # Average of 80, 90, 100
    assert module.file_count == 3
    assert module.violation_count == 3  # 1 + 2 + 0


def test_calculate_violations_by_rule_empty() -> None:
    """Should return empty dict for no violations."""
    violations = calculate_violations_by_rule([])
    assert violations == {}


def test_calculate_violations_by_rule_single_rule() -> None:
    """Should count violations for single rule."""
    # Given
    from check_md.models import FileScore, Violation

    v1 = Violation("ADR-002-R1", 1, Severity.ERROR, "Error", "context")
    v2 = Violation("ADR-002-R1", 2, Severity.ERROR, "Error", "context")
    file_score = FileScore("test.md", 80.0, 10, 2, [v1, v2])

    # When
    violations = calculate_violations_by_rule([file_score])

    # Then
    assert violations == {"ADR-002-R1": 2}


def test_calculate_violations_by_rule_multiple_rules() -> None:
    """Should count violations across multiple rules."""
    # Given
    from check_md.models import FileScore, Violation

    violations_list = [
        Violation("ADR-002-R1", 1, Severity.ERROR, "Error", "context"),
        Violation("ADR-002-R1", 2, Severity.ERROR, "Error", "context"),
        Violation("ADR-002-R2", 3, Severity.ERROR, "Error", "context"),
        Violation("ADR-002-R4", 4, Severity.ERROR, "Error", "context"),
        Violation("ADR-002-R4", 5, Severity.ERROR, "Error", "context"),
        Violation("ADR-002-R4", 6, Severity.ERROR, "Error", "context"),
    ]
    file_score = FileScore("test.md", 40.0, 10, 6, violations_list)

    # When
    violations = calculate_violations_by_rule([file_score])

    # Then
    assert violations == {"ADR-002-R1": 2, "ADR-002-R2": 1, "ADR-002-R4": 3}


def test_calculate_project_score_empty_project() -> None:
    """Should handle empty project gracefully."""
    # When
    project = calculate_project_score([])

    # Then
    assert project.score == 100.0
    assert project.total_files == 0
    assert project.total_lines == 0
    assert project.total_violations == 0
    assert project.module_scores == []
    assert project.violations_by_rule == {}


def test_calculate_project_score_single_file() -> None:
    """Should calculate project score from single file."""
    # Given
    result = FileResult(
        file_path="test.md",
        violations=[Violation("R1", 1, Severity.ERROR, "Error", "context")],
        total_lines=10,
    )

    # When
    project = calculate_project_score([result])

    # Then
    assert project.score == 90.0  # 9 clean lines out of 10
    assert project.total_files == 1
    assert project.total_lines == 10
    assert project.total_violations == 1
    assert len(project.module_scores) == 1


def test_calculate_project_score_weighted_average() -> None:
    """Should calculate weighted average by line count."""
    # Given: Two files with different sizes
    results = [
        FileResult(
            file_path="small.md",
            violations=[Violation("R1", 1, Severity.ERROR, "Error", "context")],
            total_lines=10,  # Score: 90%
        ),
        FileResult(
            file_path="large.md",
            violations=[Violation("R1", 1, Severity.ERROR, "Error", "context")],
            total_lines=90,  # Score: ~98.9%
        ),
    ]

    # When
    project = calculate_project_score(results)

    # Then
    # Weighted average: (90% * 10 + 98.89% * 90) / 100 = ~98%
    assert project.score == pytest.approx(98.0, abs=1.0)
    assert project.total_files == 2
    assert project.total_lines == 100
    assert project.total_violations == 2


def test_calculate_project_score_groups_by_module() -> None:
    """Should group files by directory in project score."""
    # Given: Files in different directories
    results = [
        FileResult("kb/adr/file1.md", [], 10),
        FileResult("kb/adr/file2.md", [], 10),
        FileResult("kb/feature/file3.md", [], 10),
    ]

    # When
    project = calculate_project_score(results)

    # Then
    assert len(project.module_scores) == 2
    module_paths = [m.module_path for m in project.module_scores]
    assert "kb/adr" in module_paths
    assert "kb/feature" in module_paths


def test_format_score_indicator_excellent() -> None:
    """Should return checkmark for score >= 95."""
    assert format_score_indicator(100.0) == "✓"
    assert format_score_indicator(95.0) == "✓"
    assert format_score_indicator(95.1) == "✓"


def test_format_score_indicator_good() -> None:
    """Should return blank for score 80-94."""
    assert format_score_indicator(94.9) == " "
    assert format_score_indicator(90.0) == " "
    assert format_score_indicator(80.0) == " "


def test_format_score_indicator_warning() -> None:
    """Should return warning for score 70-79."""
    assert format_score_indicator(79.9) == "⚠"
    assert format_score_indicator(75.0) == "⚠"
    assert format_score_indicator(70.0) == "⚠"


def test_format_score_indicator_poor() -> None:
    """Should return X for score < 70."""
    assert format_score_indicator(69.9) == "✗"
    assert format_score_indicator(50.0) == "✗"
    assert format_score_indicator(0.0) == "✗"


def test_calculate_project_score_zero_lines() -> None:
    """Should handle project with zero total lines gracefully."""
    # Given: File results with zero lines
    results = [
        FileResult("empty1.md", [], 0),
        FileResult("empty2.md", [], 0),
    ]

    # When
    project = calculate_project_score(results)

    # Then
    assert project.score == 100.0  # Zero lines = perfect score
    assert project.total_files == 2
    assert project.total_lines == 0
    assert project.total_violations == 0


def test_calculate_file_scores_zero_lines() -> None:
    """Should handle file with zero lines gracefully."""
    # Given: File with 0 lines
    result = FileResult("empty.md", [], 0)

    # When
    scores = calculate_file_scores([result])

    # Then
    assert len(scores) == 1
    assert scores[0].score == 100.0  # Zero lines = perfect score
    assert scores[0].total_lines == 0
    assert scores[0].violation_lines == 0
