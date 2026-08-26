"""
checker.py — Markdown file checker orchestrating rule execution.

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
from typing import Union

from .models import FileResult
from .rules import Rule, build_ignore_set, get_all_rules


class MarkdownChecker:
    """Orchestrates checking of Markdown files against rules.

    Coordinates execution of multiple rules against Markdown files,
    aggregates violations, and returns results.
    """

    def __init__(self, rules: list[Rule] | None = None) -> None:
        """Initialize checker with rules.

        Args:
            rules: List of rules to check (defaults to all enabled rules)
        """
        self.rules = rules if rules is not None else get_all_rules()

    def check_file(self, file_path: Union[str, Path]) -> FileResult:
        """Check a single Markdown file against all rules.

        Reads the file, runs all configured rules, aggregates violations,
        and returns a FileResult.

        Args:
            file_path: Path to Markdown file (string or Path object)

        Returns:
            FileResult containing path, violations, and line count

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not a .md file
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix.lower() != ".md":
            raise ValueError(f"Not a Markdown file: {path}")

        # Read file
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Remove trailing newlines but preserve line structure
        lines = [line.rstrip("\n") for line in lines]

        # Build set of lines to ignore based on HTML comments
        ignored_lines = build_ignore_set(lines)

        # Run all rules
        all_violations = []
        for rule in self.rules:
            violations = rule.check_file(lines)
            # Filter out violations on ignored lines
            violations = [v for v in violations if v.line_number not in ignored_lines]
            all_violations.extend(violations)

        # Sort violations by line number
        all_violations.sort(key=lambda v: v.line_number)

        return FileResult(
            file_path=str(path),
            violations=all_violations,
            total_lines=len(lines),
        )

    def check_files(self, file_paths: list[Union[str, Path]]) -> list[FileResult]:
        """Check multiple Markdown files.

        Checks each file independently, skipping files that don't exist
        or aren't Markdown files (with a warning printed).

        Args:
            file_paths: List of paths to check

        Returns:
            List of FileResult objects (one per successfully checked file)
        """
        results = []
        for path in file_paths:
            try:
                result = self.check_file(path)
                results.append(result)
            except (FileNotFoundError, ValueError) as e:
                # Log error but continue with other files
                print(f"Warning: Skipping {path}: {e}")

        return results
