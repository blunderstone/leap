"""
Compliance scoring for markdown files.

Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)
"""

from pathlib import Path
from typing import Dict, List

from .models import FileResult, FileScore, ModuleScore, ProjectScore


def calculate_file_scores(results: List[FileResult]) -> List[FileScore]:
    """Calculate FileScore objects from FileResult objects.

    Args:
        results: List of FileResult objects to score

    Returns:
        List of FileScore objects with calculated scores
    """
    return [FileScore.from_file_result(result) for result in results]


def group_by_module(file_scores: List[FileScore]) -> Dict[str, List[FileScore]]:
    """Group file scores by their parent directory (module).

    Args:
        file_scores: List of FileScore objects to group

    Returns:
        Dictionary mapping module path to list of FileScore objects
    """
    modules: Dict[str, List[FileScore]] = {}

    for score in file_scores:
        module_path = str(Path(score.file_path).parent)
        if module_path not in modules:
            modules[module_path] = []
        modules[module_path].append(score)

    return modules


def calculate_module_score(module_path: str, file_scores: List[FileScore]) -> ModuleScore:
    """Calculate ModuleScore from list of FileScore objects.

    Args:
        module_path: Path to the module directory
        file_scores: List of FileScore objects in this module

    Returns:
        ModuleScore with aggregated statistics
    """
    if not file_scores:
        return ModuleScore(
            module_path=module_path,
            score=100.0,
            file_count=0,
            violation_count=0,
            file_scores=[],
        )

    # Calculate average score across files
    total_score = sum(fs.score for fs in file_scores)
    avg_score = total_score / len(file_scores)

    # Count total violations
    total_violations = sum(len(fs.violations) for fs in file_scores)

    return ModuleScore(
        module_path=module_path,
        score=avg_score,
        file_count=len(file_scores),
        violation_count=total_violations,
        file_scores=file_scores,
    )


def calculate_violations_by_rule(file_scores: List[FileScore]) -> Dict[str, int]:
    """Calculate violation counts grouped by rule ID.

    Args:
        file_scores: List of FileScore objects to analyze

    Returns:
        Dictionary mapping rule_id to count of violations
    """
    violations_by_rule: Dict[str, int] = {}

    for file_score in file_scores:
        for violation in file_score.violations:
            rule_id = violation.rule_id
            violations_by_rule[rule_id] = violations_by_rule.get(rule_id, 0) + 1

    return violations_by_rule


def calculate_project_score(results: List[FileResult]) -> ProjectScore:
    """Calculate ProjectScore from list of FileResult objects.

    Calculates weighted average score where each file is weighted by
    its line count. Also groups files by module and calculates
    per-module scores.

    Args:
        results: List of FileResult objects for entire project

    Returns:
        ProjectScore with comprehensive project statistics
    """
    if not results:
        return ProjectScore(
            score=100.0,
            total_files=0,
            total_lines=0,
            total_violations=0,
            module_scores=[],
            violations_by_rule={},
        )

    # Calculate file scores
    file_scores = calculate_file_scores(results)

    # Calculate weighted average score (weighted by line count)
    total_lines = sum(fs.total_lines for fs in file_scores)
    if total_lines == 0:
        weighted_score = 100.0
    else:
        weighted_score = sum(
            fs.score * fs.total_lines for fs in file_scores
        ) / total_lines

    # Count total violations
    total_violations = sum(len(fs.violations) for fs in file_scores)

    # Group by module and calculate module scores
    modules = group_by_module(file_scores)
    module_scores = [
        calculate_module_score(module_path, module_files)
        for module_path, module_files in modules.items()
    ]

    # Calculate violations by rule
    violations_by_rule = calculate_violations_by_rule(file_scores)

    return ProjectScore(
        score=weighted_score,
        total_files=len(results),
        total_lines=total_lines,
        total_violations=total_violations,
        module_scores=module_scores,
        violations_by_rule=violations_by_rule,
    )


def format_score_indicator(score: float) -> str:
    """Format visual indicator for score.

    Args:
        score: Compliance score (0-100)

    Returns:
        Visual indicator string:
        - "✓" for score >= 95
        - " " for score 80-94
        - "⚠" for score 70-79
        - "✗" for score < 70
    """
    if score >= 95:
        return "✓"
    elif score >= 80:
        return " "
    elif score >= 70:
        return "⚠"
    else:
        return "✗"
