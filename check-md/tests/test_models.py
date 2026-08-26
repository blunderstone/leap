"""
test_models.py — Tests for data models.

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

from check_md.models import Severity, Violation


def test_violation_str_with_error_severity() -> None:
    """Should format ERROR violation correctly."""
    violation = Violation(
        rule_id="ADR-002-R1",
        line_number=42,
        severity=Severity.ERROR,
        message="Test error message",
        context="Test context line",
    )

    formatted = str(violation)

    expected = (
        "  Line 42: [Rule 1] ERROR\n"
        "    Test error message\n"
        "    Context: Test context line"
    )
    assert formatted == expected, f"Expected:\n{expected}\n\nActual:\n{formatted}"


def test_violation_str_with_warning_severity() -> None:
    """Should format WARNING violation correctly."""
    violation = Violation(
        rule_id="ADR-002-R2",
        line_number=10,
        severity=Severity.WARNING,
        message="Test warning message",
        context="Warning context",
    )

    formatted = str(violation)

    expected = (
        "  Line 10: [Rule 2] WARNING\n"
        "    Test warning message\n"
        "    Context: Warning context"
    )
    assert formatted == expected, f"Expected:\n{expected}\n\nActual:\n{formatted}"


def test_violation_str_with_fix_hint() -> None:
    """Should include fix hint when present."""
    violation = Violation(
        rule_id="ADR-002-R1",
        line_number=5,
        severity=Severity.ERROR,
        message="Test message",
        context="Test context",
        fix_hint="Replace with: ## Heading"
    )

    formatted = str(violation)

    expected = (
        "  Line 5: [Rule 1] ERROR\n"
        "    Test message\n"
        "    Context: Test context\n"
        "  Hint: Replace with: ## Heading"
    )
    assert formatted == expected, f"Expected:\n{expected}\n\nActual:\n{formatted}"


def test_violation_str_without_fix_hint() -> None:
    """Should not include hint section when fix_hint is None."""
    violation = Violation(
        rule_id="ADR-002-R1",
        line_number=5,
        severity=Severity.ERROR,
        message="Test message",
        context="Test context",
        fix_hint=None
    )

    formatted = str(violation)

    expected = (
        "  Line 5: [Rule 1] ERROR\n"
        "    Test message\n"
        "    Context: Test context"
    )
    assert formatted == expected, f"Expected:\n{expected}\n\nActual:\n{formatted}"


def test_format_rule_id_adr_002_r1() -> None:
    """Should format ADR-002-R1 as Rule 1."""
    violation = Violation(
        rule_id="ADR-002-R1",
        line_number=1,
        severity=Severity.ERROR,
        message="Test",
        context="Context"
    )

    formatted_id = violation._format_rule_id("ADR-002-R1")
    assert formatted_id == "Rule 1"


def test_format_rule_id_adr_002_r2() -> None:
    """Should format ADR-002-R2 as Rule 2."""
    violation = Violation(
        rule_id="ADR-002-R2",
        line_number=1,
        severity=Severity.ERROR,
        message="Test",
        context="Context"
    )

    formatted_id = violation._format_rule_id("ADR-002-R2")
    assert formatted_id == "Rule 2"


def test_format_rule_id_adr_002_r5() -> None:
    """Should format ADR-002-R5 as Rule 5."""
    violation = Violation(
        rule_id="ADR-002-R5",
        line_number=1,
        severity=Severity.ERROR,
        message="Test",
        context="Context"
    )

    formatted_id = violation._format_rule_id("ADR-002-R5")
    assert formatted_id == "Rule 5"


def test_format_rule_id_simple_r1() -> None:
    """Should format R1 as Rule 1."""
    violation = Violation(
        rule_id="R1",
        line_number=1,
        severity=Severity.ERROR,
        message="Test",
        context="Context"
    )

    formatted_id = violation._format_rule_id("R1")
    assert formatted_id == "Rule 1"


def test_format_rule_id_unknown_format() -> None:
    """Should preserve unknown rule ID formats."""
    violation = Violation(
        rule_id="CUSTOM-RULE",
        line_number=1,
        severity=Severity.ERROR,
        message="Test",
        context="Context"
    )

    formatted_id = violation._format_rule_id("CUSTOM-RULE")
    assert formatted_id == "CUSTOM-RULE"


def test_violation_preserves_original_rule_id() -> None:
    """Should preserve original rule_id in the violation object."""
    violation = Violation(
        rule_id="ADR-002-R1",
        line_number=1,
        severity=Severity.ERROR,
        message="Test",
        context="Context"
    )

    # The rule_id attribute should remain unchanged
    assert violation.rule_id == "ADR-002-R1"

    # But str() should format it
    assert "[Rule 1]" in str(violation)
    assert "[ADR-002-R1]" not in str(violation)
