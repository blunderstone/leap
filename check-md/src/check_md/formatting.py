"""
Formatting utilities for violation display.

This module contains shared formatting functions used across CLI output,
fixer previews, and other user-facing displays.
"""

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Violation


def format_rule_id_for_display(rule_id: str) -> str:
    """Format rule ID for user-friendly display.

    Converts "ADR-002-R1" to "Rule 1", "ADR-002-R2" to "Rule 2", etc.

    Args:
        rule_id: Internal rule identifier (e.g., "ADR-002-R1")

    Returns:
        User-friendly rule label (e.g., "Rule 1")

    Examples:
        >>> format_rule_id_for_display("ADR-002-R1")
        "Rule 1"
        >>> format_rule_id_for_display("ADR-002-R5")
        "Rule 5"
        >>> format_rule_id_for_display("CUSTOM-RULE")
        "CUSTOM-RULE"
    """
    match = re.search(r'R(\d+)$', rule_id)
    if match:
        rule_num = match.group(1)
        return f"Rule {rule_num}"
    # Fallback to original if pattern doesn't match
    return rule_id


def format_violation_display(violation: "Violation", separator: str = " ") -> str:
    """Format violation message and rule ID for display.

    FORMATTING CONVENTION: All user-facing output MUST display violations as:
        "message{separator}[Rule N]"

    This function enforces consistency across CLI output, fixer previews,
    and all other user-facing displays.

    Args:
        violation: The violation to format
        separator: String between message and rule
                  - " " (default) for text output
                  - "::" for GitHub Actions annotations

    Returns:
        Formatted string: "message{separator}[Rule N]"

    Examples:
        >>> from models import Violation, Severity
        >>> v = Violation("ADR-002-R1", 1, Severity.ERROR, "Test msg", "ctx")
        >>> format_violation_display(v)
        "Test msg [Rule 1]"
        >>> format_violation_display(v, separator="::")
        "Test msg::[Rule 1]"
    """
    rule_display = format_rule_id_for_display(violation.rule_id)
    return f"{violation.message}{separator}[{rule_display}]"