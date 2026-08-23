"""
Rule implementations for ADR 008 markdown formatting standards.

Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)
"""

import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Set

from .models import LineContext, Severity, Violation


class FixStrategy(Enum):
    """Strategy for applying auto-fixes to violations.

    NONE: Do not apply fixes (check-only mode)
    CONSERVATIVE: Safe fixes only, insert placeholders when uncertain
    AGGRESSIVE: Apply all fixes including cascading changes
    """

    NONE = "none"
    CONSERVATIVE = "conservative"
    AGGRESSIVE = "aggressive"


# Patterns for ignore comments
IGNORE_COMMENT_PATTERN = re.compile(r"<!--\s*check-md-ignore\s*-->")
IGNORE_NEXT_PATTERN = re.compile(r"<!--\s*check-md-ignore-next\s*-->")
IGNORE_BEGIN_PATTERN = re.compile(r"<!--\s*check-md-ignore-begin\s*-->")
IGNORE_END_PATTERN = re.compile(r"<!--\s*check-md-ignore-end\s*-->")


def build_ignore_set(lines: list[str]) -> Set[int]:
    """Build set of line numbers to ignore based on HTML comments.

    Supports four comment formats:
    - `<!-- check-md-ignore -->` - ignores the line with the comment
    - `<!-- check-md-ignore-next -->` - ignores the next line
    - `<!-- check-md-ignore-begin -->` - start ignoring all lines
    - `<!-- check-md-ignore-end -->` - stop ignoring

    Args:
        lines: List of file lines (1-indexed line numbers will be returned)

    Returns:
        Set of 1-indexed line numbers to ignore
    """
    ignored_lines: Set[int] = set()
    ignoring_range = False

    for i, line in enumerate(lines):
        line_num = i + 1  # Convert to 1-indexed

        # Check for range begin/end
        if IGNORE_BEGIN_PATTERN.search(line):
            ignoring_range = True
            ignored_lines.add(line_num)  # Ignore the begin comment line itself
            continue

        if IGNORE_END_PATTERN.search(line):
            ignoring_range = False
            ignored_lines.add(line_num)  # Ignore the end comment line itself
            continue

        # If we're in an ignore range, ignore this line
        if ignoring_range:
            ignored_lines.add(line_num)
            continue

        # Check for single-line ignore comment on current line
        if IGNORE_COMMENT_PATTERN.search(line):
            ignored_lines.add(line_num)

        # Check for ignore-next comment
        if IGNORE_NEXT_PATTERN.search(line):
            # Ignore the next line (if it exists)
            if i + 1 < len(lines):
                ignored_lines.add(line_num + 1)

    return ignored_lines


class Rule(ABC):
    """Base class for all markdown linting rules.

    Subclasses must implement check_line() for line-by-line checking.
    Can override check_file() for rules requiring full file analysis.
    """

    def __init__(self, rule_id: str, description: str) -> None:
        """Initialize rule.

        Args:
            rule_id: Unique identifier (e.g., "ADR-002-R1")
            description: Human-readable description
        """
        self.rule_id = rule_id
        self.description = description

    @abstractmethod
    def check_line(self, context: LineContext) -> list[Violation]:
        """Check a single line for violations.

        Args:
            context: Line context with surrounding information

        Returns:
            List of violations found (empty if none)
        """
        pass

    def fix_violation(
        self, lines: list[str], violation: Violation, strategy: FixStrategy = FixStrategy.CONSERVATIVE
    ) -> list[str]:
        """Fix a violation in the file.

        Default implementation returns lines unchanged (no auto-fix available).
        Rules that support auto-fix should override this method.

        Args:
            lines: All lines in the file (0-indexed)
            violation: The violation to fix
            strategy: Fix strategy (CONSERVATIVE or AGGRESSIVE)

        Returns:
            Modified lines with violation fixed
        """
        return lines

    def check_file(self, lines: list[str]) -> list[Violation]:
        """Check entire file for violations.

        Default implementation iterates through lines building context
        and calling check_line() for each. Rules requiring full file
        analysis (e.g., nested code blocks) should override this.

        Automatically tracks code block state for rules to use.

        Args:
            lines: All lines in the file

        Returns:
            List of all violations found
        """
        violations: list[Violation] = []
        in_code_block = False
        code_block_fence: Optional[str] = None

        for i, line in enumerate(lines):
            # Build context with CURRENT code block state (before processing this line)
            context = LineContext(
                line_number=i + 1,
                line=line,
                prev_line=lines[i - 1] if i > 0 else None,
                next_line=lines[i + 1] if i < len(lines) - 1 else None,
                in_code_block=in_code_block,
                code_block_fence=code_block_fence,
            )

            # Check line with rules
            violations.extend(self.check_line(context))

            # Update code block state AFTER checking the line
            fence_match = re.match(r"^(`{3,})", line)
            if fence_match:
                fence = fence_match.group(1)
                if not in_code_block:
                    in_code_block = True
                    code_block_fence = fence
                elif fence == code_block_fence:
                    in_code_block = False
                    code_block_fence = None

        return violations


class Rule1SemanticHeadings(Rule):
    """
    ADR 008 Rule 1: Use proper heading levels, not bold text for structure.

    Detects:
    - Standalone bold text that should be a heading
    - Bold text at start of line (likely pseudo-heading)
    """

    # Pattern: Line starting with **text** (possibly with leading spaces/list markers)
    # This matches standalone bold text that should be converted to a heading.
    # It only matches when there's NO content after the bold text (except optional colon).
    BOLD_HEADING_PATTERN = re.compile(r"^(\s*(?:[-*+]\s+)?)\*\*([^*]+)\*\*\s*:?\s*$")

    def __init__(self) -> None:
        super().__init__(
            rule_id="ADR-002-R1",
            description="Use semantic headings (##, ###) not bold text for structure",
        )

    def check_line(self, context: LineContext) -> list[Violation]:
        """Check for bold text used as pseudo-headings.

        Detects standalone bold text (entire line is **text** or **text:**) that
        should be converted to a semantic heading. Does NOT flag inline label-value
        pairs like **Author:** [Name] as these are intentional formatting.

        Does NOT flag bold text within list items (e.g., "- **Item:**") as these
        are legitimate emphasis, not pseudo-headings.

        Args:
            context: Line context

        Returns:
            List of violations (0-1 violations per line)
        """
        if context.in_code_block:
            return []

        violations: list[Violation] = []
        line = context.line

        # Check for standalone bold text (entire line is **text** or **text:**)
        # This pattern ONLY matches when there's no content after the bold text
        # (except optional colon and whitespace), so inline patterns like
        # **Author:** [Name] will NOT match.
        standalone_match = self.BOLD_HEADING_PATTERN.match(line)
        if standalone_match:
            prefix = standalone_match.group(1)  # Leading spaces/list markers
            bold_text = standalone_match.group(2)

            # Check if this is within a list item (has list marker)
            # List markers: -, *, +, or numbered (captured in prefix group)
            has_list_marker = bool(prefix.strip())  # Has list marker if prefix contains non-whitespace

            # Don't flag bold text within list items
            if has_list_marker:
                return []

            # Check if previous line is blank (indicates start of section)
            is_section_start = context.prev_line is None or context.prev_line.strip() == ""

            if is_section_start:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        line_number=context.line_number,
                        severity=Severity.ERROR,
                        message="Standalone bold text should be a heading",
                        context=line.strip(),
                        fix_hint=f"Replace with: ## {bold_text}",
                    )
                )

        return violations

    def fix_violation(
        self, lines: list[str], violation: Violation, strategy: FixStrategy = FixStrategy.CONSERVATIVE
    ) -> list[str]:
        """Fix bold text to proper heading.

        Converts **Text** or **Text:** to #### Text (removes bold and trailing colon).

        Args:
            lines: All lines in file (0-indexed)
            violation: Violation to fix
            strategy: Fix strategy (not used by this rule)

        Returns:
            Modified lines with fix applied
        """
        line_idx = violation.line_number - 1  # Convert to 0-indexed
        if line_idx < 0 or line_idx >= len(lines):
            return lines

        line = lines[line_idx]

        # Match standalone bold pattern (only pattern we detect now)
        standalone_match = self.BOLD_HEADING_PATTERN.match(line)
        if standalone_match:
            prefix = standalone_match.group(1)  # Leading spaces/list markers
            bold_text = standalone_match.group(2).strip()
            # Remove trailing colon if present
            if bold_text.endswith(':'):
                bold_text = bold_text[:-1].strip()
            lines[line_idx] = f"{prefix}#### {bold_text}\n"
            return lines

        return lines


class Rule2BlockSeparation(Rule):
    """
    ADR 008 Rule 2: Blank lines before block constructs.

    Detects missing blank lines before:
    - Lists (-, *, +, 1.)
    - Code blocks (```)
    - Block quotes (>)
    - Horizontal rules (---, ***)
    - Tables (|)
    """

    # Patterns for block-level constructs
    LIST_PATTERN = re.compile(r"^\s*[-*+]\s+\S")  # Unordered list
    ORDERED_LIST_PATTERN = re.compile(r"^\s*\d+\.\s+\S")  # Ordered list
    CODE_FENCE_PATTERN = re.compile(r"^`{3,}")  # Code fence
    BLOCKQUOTE_PATTERN = re.compile(r"^\s*>\s")  # Block quote
    BLOCKQUOTE_CONTINUATION_PATTERN = re.compile(r"^\s*>")  # Block quote continuation
    HORIZONTAL_RULE_PATTERN = re.compile(r"^\s*(?:---+|\*\*\*+|___+)\s*$")  # HR
    TABLE_PATTERN = re.compile(r"^\s*\|")  # Table row

    def __init__(self) -> None:
        super().__init__(
            rule_id="ADR-002-R2",
            description="Blank lines required before block-level constructs",
        )

    def check_line(self, context: LineContext) -> list[Violation]:
        """Check for missing blank lines before block constructs.

        Per CommonMark spec, block-level elements require blank lines
        before them when preceded by paragraph text. This prevents
        the block from being wrapped into the paragraph.

        Args:
            context: Line context

        Returns:
            List containing 0 or 1 violation
        """
        if context.in_code_block:
            return []

        line = context.line
        prev = context.prev_line

        # Skip if this is first line or previous line is blank
        if prev is None or prev.strip() == "":
            return []

        violations: list[Violation] = []

        # Check each block construct type
        if self.LIST_PATTERN.match(line):
            # Don't flag if previous line is also a list item (continuation)
            if not (
                self.LIST_PATTERN.match(prev) or self.ORDERED_LIST_PATTERN.match(prev)
            ):
                violations.append(self._create_violation(context, "unordered list"))
        elif self.ORDERED_LIST_PATTERN.match(line):
            # Don't flag if previous line is also a list item (continuation)
            if not (
                self.LIST_PATTERN.match(prev) or self.ORDERED_LIST_PATTERN.match(prev)
            ):
                violations.append(self._create_violation(context, "ordered list"))
        elif self.CODE_FENCE_PATTERN.match(line):
            violations.append(self._create_violation(context, "code block"))
        elif self.BLOCKQUOTE_PATTERN.match(line):
            # Only flag first line of block quote
            if not self.BLOCKQUOTE_CONTINUATION_PATTERN.match(prev):
                violations.append(self._create_violation(context, "block quote"))
        elif self.HORIZONTAL_RULE_PATTERN.match(line):
            violations.append(self._create_violation(context, "horizontal rule"))
        elif self.TABLE_PATTERN.match(line):
            # Only flag first row of table
            if not self.TABLE_PATTERN.match(prev):
                violations.append(self._create_violation(context, "table"))

        return violations

    def _create_violation(self, context: LineContext, construct_type: str) -> Violation:
        """Create violation for missing blank line before construct.

        Args:
            context: Line context
            construct_type: Human-readable name of construct (e.g., "unordered list")

        Returns:
            Violation object with appropriate message and fix hint
        """
        return Violation(
            rule_id=self.rule_id,
            line_number=context.line_number,
            severity=Severity.ERROR,
            message=f"Missing blank line before {construct_type}",
            context=context.line.strip(),
            fix_hint="Add blank line before this element",
        )

    def fix_violation(
        self, lines: list[str], violation: Violation, strategy: FixStrategy = FixStrategy.CONSERVATIVE
    ) -> list[str]:
        """Fix missing blank line before block construct.

        Inserts a blank line before the violation line.

        Args:
            lines: All lines in file (0-indexed)
            violation: Violation to fix
            strategy: Fix strategy (not used by this rule)

        Returns:
            Modified lines with blank line inserted
        """
        line_idx = violation.line_number - 1  # Convert to 0-indexed
        if line_idx < 0 or line_idx >= len(lines):
            return lines

        # Insert blank line before the block construct
        lines.insert(line_idx, "\n")
        return lines


class Rule3HeadingIncrement(Rule):
    """
    ADR 008 Rule 3: Heading levels should only increment by 1.

    Aligned with MD001 (markdownlint) and remark-lint heading-increment.
    Enforces ADR 008 line 70: "Never skip heading levels".

    Valid sequences:
    - Increments of 1: # → ##, ## → ### → ####
    - Decrements of any size: #### → ## (closing sections)
    - Same level: ## → ## (sibling sections)

    Invalid sequences:
    - Increments > 1: ## → #### (skipped ###)
    """

    # Pattern to match heading lines: ^#{1,6}\s+
    HEADING_PATTERN = re.compile(r"^(#{1,6})\s+")

    def __init__(self) -> None:
        super().__init__(
            rule_id="ADR-002-R3",
            description="Heading levels should only increment by 1",
        )

    def check_line(self, context: LineContext) -> list[Violation]:
        """Not used - Rule3 overrides check_file() for full file analysis."""
        return []

    def check_file(self, lines: list[str]) -> list[Violation]:
        """Check entire file for heading level increment violations.

        Maintains heading level state across the document to detect when
        headings skip levels (e.g., ## → ####).

        Args:
            lines: All lines in the file

        Returns:
            List of all violations found
        """
        violations: list[Violation] = []
        previous_heading_level: Optional[int] = None
        in_code_block = False
        code_block_fence: Optional[str] = None

        # Build ignore set once for the whole file
        ignored_lines = build_ignore_set(lines)

        for i, line in enumerate(lines):
            line_num = i + 1  # Convert to 1-indexed

            # Skip ignored lines
            if line_num in ignored_lines:
                continue

            # Track code block state
            fence_match = re.match(r"^(`{3,})", line)
            if fence_match:
                fence = fence_match.group(1)
                if not in_code_block:
                    in_code_block = True
                    code_block_fence = fence
                elif fence == code_block_fence:
                    in_code_block = False
                    code_block_fence = None
                continue

            # Skip lines inside code blocks
            if in_code_block:
                continue

            # Check for heading
            heading_match = self.HEADING_PATTERN.match(line)
            if not heading_match:
                continue

            current_level = len(heading_match.group(1))

            # Check if this is a TODO heading from check-md
            if "TODO: check-md" in line:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        line_number=line_num,
                        severity=Severity.ERROR,
                        message="Incomplete heading structure (TODO placeholder from previous fix)",
                        context=line.strip(),
                        fix_hint="Resolve document structure or use --aggressive to apply cascade fixes",
                    )
                )
                # Don't update previous_heading_level - TODOs don't count as real headings
                continue

            # First heading in document can be any level
            if previous_heading_level is None:
                previous_heading_level = current_level
                continue

            # Check for invalid increment (skipped levels)
            if current_level > previous_heading_level + 1:
                increment = current_level - previous_heading_level
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        line_number=line_num,
                        severity=Severity.ERROR,
                        message=f"Heading level increased by {increment} "
                        f"(from {'#' * previous_heading_level} to {'#' * current_level})",
                        context=line.strip(),
                        fix_hint=f"Change {'#' * current_level} to {'#' * (previous_heading_level + 1)} "
                        f"or add intermediate {'#' * (previous_heading_level + 1)} heading",
                    )
                )

            # Update previous level for next iteration
            previous_heading_level = current_level

        return violations

    def fix_violation(
        self, lines: list[str], violation: Violation, strategy: FixStrategy = FixStrategy.CONSERVATIVE
    ) -> list[str]:
        """Fix heading level skip with cascade detection and TODO insertion.

        CONSERVATIVE: Inserts TODO heading if fix would create cascade.
        AGGRESSIVE: Removes existing TODOs and applies cascade fixes.

        Args:
            lines: All lines in file (0-indexed)
            violation: Violation to fix
            strategy: Fix strategy (CONSERVATIVE or AGGRESSIVE)

        Returns:
            Modified lines with violation fixed
        """
        line_idx = violation.line_number - 1  # Convert to 0-indexed
        if line_idx < 0 or line_idx >= len(lines):
            return lines

        line = lines[line_idx]

        # If this is a TODO violation, just remove it
        if "TODO: check-md" in line:
            return self._remove_todo_at_line(lines, line_idx)

        # Parse current heading
        heading_match = self.HEADING_PATTERN.match(line)
        if not heading_match:
            return lines

        current_level = len(heading_match.group(1))

        # Find previous heading level
        previous_level = self._find_previous_heading_level(lines, line_idx)
        if previous_level is None:
            return lines  # No previous heading found

        # Detect cascade: would fixing this create a new violation?
        would_cascade = self._would_create_cascade(lines, line_idx, previous_level)

        if would_cascade and strategy == FixStrategy.CONSERVATIVE:
            # Insert TODO heading instead of downgrading
            return self._insert_todo_heading(lines, line_idx, previous_level, current_level)

        # Apply heading downgrade (aggressive mode or no cascade)
        return self._apply_heading_downgrade(lines, line_idx, line, previous_level, strategy)

    def _find_previous_heading_level(self, lines: list[str], from_idx: int) -> Optional[int]:
        """Find the level of the previous heading by scanning backwards.

        Args:
            lines: All file lines
            from_idx: Index to start scanning backwards from (exclusive)

        Returns:
            Previous heading level, or None if no previous heading found
        """
        for j in range(from_idx - 1, -1, -1):
            prev_heading_match = self.HEADING_PATTERN.match(lines[j])
            if prev_heading_match:
                return len(prev_heading_match.group(1))
        return None

    def _apply_heading_downgrade(
        self, lines: list[str], line_idx: int, line: str, previous_level: int, strategy: FixStrategy
    ) -> list[str]:
        """Apply heading level downgrade, handling aggressive mode cleanup.

        Args:
            lines: All file lines
            line_idx: Index of heading to downgrade
            line: The heading line content
            previous_level: Previous heading level
            strategy: Fix strategy

        Returns:
            Modified lines with heading downgraded
        """
        current_line_idx = line_idx
        current_hashes = self.HEADING_PATTERN.match(line).group(1)

        # In aggressive mode, remove any existing TODO heading before this violation
        if strategy == FixStrategy.AGGRESSIVE:
            lines = self._remove_todo_heading_before(lines, line_idx)
            # Recalculate line_idx in case TODO was removed
            current_line_idx = self._find_line_index(lines, line)
            if current_line_idx is None:
                return lines  # Heading disappeared somehow
            current_hashes = self.HEADING_PATTERN.match(lines[current_line_idx]).group(1)

        # Apply downgrade
        target_level = previous_level + 1
        target_hashes = "#" * target_level
        lines[current_line_idx] = lines[current_line_idx].replace(current_hashes, target_hashes, 1)
        return lines

    def _find_line_index(self, lines: list[str], target_line: str) -> Optional[int]:
        """Find the index of a specific line in the file.

        Args:
            lines: All file lines
            target_line: Line content to find

        Returns:
            Index of line, or None if not found
        """
        for i in range(len(lines)):
            if lines[i] == target_line and self.HEADING_PATTERN.match(lines[i]):
                return i
        return None

    def _would_create_cascade(
        self, lines: list[str], current_idx: int, prev_level: int
    ) -> bool:
        """Check if fixing current heading would create a new violation.

        Args:
            lines: All file lines
            current_idx: Index of current heading being fixed
            prev_level: Previous heading level

        Returns:
            True if next heading would become a violation after fix
        """
        # After fix, current heading would be at prev_level + 1
        fixed_level = prev_level + 1

        # Look for next heading after current
        for i in range(current_idx + 1, len(lines)):
            next_match = self.HEADING_PATTERN.match(lines[i])
            if next_match:
                next_level = len(next_match.group(1))
                # Would next heading skip a level after our fix?
                if next_level > fixed_level + 1:
                    return True
                # Stop at first heading (no cascade if decrement or same level)
                return False

        return False  # No next heading found

    def _remove_todo_at_line(self, lines: list[str], line_idx: int) -> list[str]:
        """Remove TODO heading at specified line with surrounding blank lines.

        Args:
            lines: All file lines
            line_idx: Index of TODO heading line

        Returns:
            Modified lines with TODO removed
        """
        start_idx = line_idx
        if line_idx > 0 and lines[line_idx - 1].strip() == "":
            start_idx = line_idx - 1

        end_idx = line_idx + 1
        if line_idx + 1 < len(lines) and lines[line_idx + 1].strip() == "":
            end_idx = line_idx + 2

        del lines[start_idx:end_idx]
        return lines

    def _insert_todo_heading(
        self, lines: list[str], violation_idx: int, prev_level: int, current_level: int
    ) -> list[str]:
        """Insert TODO heading before violation to signal missing structure.

        Args:
            lines: All file lines
            violation_idx: Index of violation line
            prev_level: Previous heading level
            current_level: Current (violating) heading level

        Returns:
            Modified lines with TODO inserted
        """
        target_level = prev_level + 1
        skip_amount = current_level - prev_level

        # Construct placeholder heading text for insertion
        if skip_amount == 2:
            todo_text = f"{'#' * target_level} TODO: check-md - add missing level {target_level} heading\n"
        else:
            # Multi-level skip: ## → ##### (skipped 3 and 4)
            missing_levels = ", ".join(str(l) for l in range(target_level, current_level))
            todo_text = f"{'#' * target_level} TODO: check-md - add missing level {missing_levels} headings\n"

        # Insert placeholder before the violation
        # Add blank line before placeholder if previous line isn't blank
        insert_lines = []
        if violation_idx > 0 and lines[violation_idx - 1].strip() != "":
            insert_lines.append("\n")
        insert_lines.append(todo_text)
        insert_lines.append("\n")

        # Insert at violation position
        lines[violation_idx:violation_idx] = insert_lines

        return lines

    def _remove_todo_heading_before(self, lines: list[str], violation_idx: int) -> list[str]:
        """Remove check-md TODO heading immediately before the violation.

        Searches backwards from violation for a TODO heading inserted by check-md.

        Args:
            lines: All file lines
            violation_idx: Index of violation heading

        Returns:
            Modified lines with TODO heading removed (if found)
        """
        # Look backwards for TODO heading (should be within a few lines)
        for i in range(violation_idx - 1, max(0, violation_idx - 5), -1):
            line = lines[i]
            if "TODO: check-md" in line and self.HEADING_PATTERN.match(line):
                # Found TODO heading - remove it and surrounding blank lines
                # Remove blank line before TODO if present
                start_idx = i
                if i > 0 and lines[i - 1].strip() == "":
                    start_idx = i - 1

                # Remove blank line after TODO if present
                end_idx = i + 1
                if i + 1 < len(lines) and lines[i + 1].strip() == "":
                    end_idx = i + 2

                # Remove the TODO and its surrounding blank lines
                del lines[start_idx:end_idx]
                break

        return lines


class Rule4NestedCodeBlocks(Rule):
    """
    ADR 008 Rule 4: Proper escaping for nested code blocks.

    Detects:
    - Code blocks (```) inside other code blocks with insufficient fence length
    - Recommends using N+1 backticks for outer block when N backticks appear inside

    This requires full file analysis to track nesting depth.
    """

    CODE_FENCE_PATTERN = re.compile(r"^(`{3,})(\w*)\s*$")

    def __init__(self) -> None:
        super().__init__(
            rule_id="ADR-002-R4",
            description="Nested code blocks must use longer fence for outer block",
        )

    def check_file(self, lines: list[str]) -> list[Violation]:
        """
        Check entire file for nested code block violations.

        Per ADR 008 Rule 4 and CommonMark spec:
        - A fence with a language tag always opens a new block
        - A fence without a language tag closes the current block if length >= opening fence
        - A fence without a language tag opens a nested block if length < opening fence
        - Problem: An inner opening fence with length >= outer fence will cause premature closing
        - Solution: Outer fence must be longer than any inner opening fence

        Algorithm:
        1. Classify each fence as OPENING or CLOSING:
           - Has language tag → OPENING
           - No language tag, not in block → OPENING
           - No language tag, fence_len < current_block → OPENING (nested)
           - No language tag, fence_len >= current_block → CLOSING
        2. OPENING fence: Check if fence_len >= containing block → VIOLATION
        3. CLOSING fence: Pop from stack
        """
        violations: list[Violation] = []
        block_stack: list[tuple[int, int]] = []  # Stack of (line_num, fence_len)

        for i, line in enumerate(lines):
            match = self.CODE_FENCE_PATTERN.match(line)
            line_num = i + 1

            if not match:
                continue  # Not a fence

            fence = match.group(1)
            fence_len = len(fence)
            language_tag = match.group(2) if match.group(2) else ""

            # STEP 1: Classify fence as OPENING or CLOSING
            if language_tag:
                # Has language tag → OPENING
                fence_type = "OPENING"
            elif not block_stack:
                # No language tag, not in a block → OPENING
                fence_type = "OPENING"
            else:
                # No language tag, we're inside a block
                current_block_line, current_block_len = block_stack[-1]
                if fence_len < current_block_len:
                    # Shorter than current block → OPENING
                    fence_type = "OPENING"
                else:
                    # Same or longer than current block → CLOSING
                    fence_type = "CLOSING"

            # STEP 2: Process based on classification
            if fence_type == "OPENING":
                # Check for violation: opening must be nested in larger block
                if block_stack:
                    current_block_line, current_block_len = block_stack[-1]
                    if fence_len >= current_block_len:
                        # VIOLATION: Opening fence >= containing block size
                        violations.append(
                            Violation(
                                rule_id=self.rule_id,
                                line_number=current_block_line,
                                severity=Severity.ERROR,
                                message=(
                                    f"Nested code block detected: outer block uses {current_block_len} "
                                    f"backticks but inner block at line {line_num} uses {fence_len}"
                                ),
                                context=lines[current_block_line - 1].strip(),
                                fix_hint=(
                                    f"Change outer fence to {fence_len + 1} backticks "
                                    f"(and matching closing fence)"
                                ),
                            )
                        )

                # Push this opening onto stack
                block_stack.append((line_num, fence_len))

            else:  # fence_type == "CLOSING"
                # Pop the most recent opening from stack
                if block_stack:
                    block_stack.pop()
                # If stack is empty, this is a closing fence with no open block
                # We don't flag this as a violation (not part of Rule 4)

        return violations

    def check_line(self, context: LineContext) -> list[Violation]:
        """Not used - this rule requires full file analysis."""
        return []

    def fix_violation(
        self, lines: list[str], violation: Violation, strategy: FixStrategy = FixStrategy.CONSERVATIVE
    ) -> list[str]:
        """Fix nested code block by increasing outer fence length.

        When an inner fence is >= outer fence length, increase the outer
        fence to be longer than any inner fence.

        Args:
            lines: All lines in file (0-indexed)
            violation: Violation indicating outer fence that needs to be lengthened
            strategy: Fix strategy (not used by this rule)

        Returns:
            Modified lines with outer fence increased
        """
        # Violation line_number points to the outer fence that needs to be fixed
        outer_fence_idx = violation.line_number - 1  # Convert to 0-indexed
        if outer_fence_idx < 0 or outer_fence_idx >= len(lines):
            return lines

        # Get the outer fence length
        outer_match = self.CODE_FENCE_PATTERN.match(lines[outer_fence_idx])
        if not outer_match:
            return lines

        outer_fence_len = len(outer_match.group(1))

        # Extract the inner fence length from the violation message
        # Message format: "...inner block at line X uses Y"
        import re
        match = re.search(r'line \d+ uses (\d+)', violation.message)
        if not match:
            return lines

        inner_fence_len = int(match.group(1))

        # Increase outer fence to be 1 longer than inner fence
        new_outer_len = inner_fence_len + 1

        # Update opening fence
        old_fence = outer_match.group(1)
        new_fence = '`' * new_outer_len
        lines[outer_fence_idx] = lines[outer_fence_idx].replace(old_fence, new_fence, 1)

        # Find and update corresponding closing fence
        # Scan forward from outer_fence_idx to find its closing fence
        block_depth = 1
        for i in range(outer_fence_idx + 1, len(lines)):
            match = self.CODE_FENCE_PATTERN.match(lines[i])
            if match:
                fence_len = len(match.group(1))
                lang_tag = match.group(2)

                if lang_tag:
                    # Opening fence
                    block_depth += 1
                elif fence_len >= outer_fence_len:
                    # Potential closing fence
                    block_depth -= 1
                    if block_depth == 0:
                        # This is the closing fence for our outer block
                        old_fence = match.group(1)
                        new_fence = '`' * new_outer_len
                        lines[i] = lines[i].replace(old_fence, new_fence, 1)
                        break

        return lines


class Rule5LabelValueSequences(Rule):
    """
    ADR 008 Rule 5: Label-value sequences require line breaks.

    Detects consecutive label-value lines that are missing <br> tags.
    Label-value pattern: **Label:** value or **Label**: value

    When label-value lines appear consecutively, they should end with <br>
    (except the last line in the sequence) to prevent markdown from wrapping
    them into a single paragraph.
    """

    # Pattern: **Label:** value or **Label**: value
    # Matches: optional leading spaces, **text**, optional colon inside/outside bold, content
    LABEL_VALUE_PATTERN = re.compile(
        r'^\s*\*\*([^*]+)\*\*\s*:?\s*(.+)$'
    )

    # Pattern to detect <br> tag at end of line (various formats)
    BR_TAG_PATTERN = re.compile(r'<br\s*/?>[\s\n]*$', re.IGNORECASE)

    def __init__(self) -> None:
        super().__init__(
            rule_id="ADR-002-R5",
            description="Label-value sequences require <br> tags between lines",
        )

    def check_line(self, context: LineContext) -> list[Violation]:
        """Not used - Rule5 requires full file analysis to detect sequences."""
        return []

    def check_file(self, lines: list[str]) -> list[Violation]:
        """Check entire file for label-value sequences missing <br> tags.

        Detects consecutive label-value lines and flags missing <br> tags.
        The last line in a sequence doesn't need <br>.

        Args:
            lines: All lines in the file

        Returns:
            List of all violations found
        """
        violations: list[Violation] = []
        in_code_block = False
        code_block_fence: Optional[str] = None

        for i, line in enumerate(lines):
            line_num = i + 1

            # Track code block state
            fence_match = re.match(r"^(`{3,})", line)
            if fence_match:
                fence = fence_match.group(1)
                if not in_code_block:
                    in_code_block = True
                    code_block_fence = fence
                elif fence == code_block_fence:
                    in_code_block = False
                    code_block_fence = None
                continue

            # Skip lines inside code blocks
            if in_code_block:
                continue

            # Check if current line matches label-value pattern
            current_match = self.LABEL_VALUE_PATTERN.match(line)
            if not current_match:
                continue

            # Check if next line also matches label-value pattern
            next_line_idx = i + 1
            if next_line_idx >= len(lines):
                # Last line in file - no violation
                continue

            next_line = lines[next_line_idx]

            # Skip if next line is blank (breaks sequence)
            if next_line.strip() == "":
                continue

            # Check if next line matches label-value pattern
            next_match = self.LABEL_VALUE_PATTERN.match(next_line)
            if not next_match:
                # Next line doesn't match - current line is last in sequence
                continue

            # Both current and next line match pattern - current line should have <br>
            if not self.BR_TAG_PATTERN.search(line):
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        line_number=line_num,
                        severity=Severity.ERROR,
                        message="Label-value line missing <br> tag (next line is also a label-value)",
                        context=line.strip(),
                        fix_hint="Add <br> at end of line to prevent wrapping with next line",
                    )
                )

        return violations

    def fix_violation(
        self, lines: list[str], violation: Violation, strategy: FixStrategy = FixStrategy.CONSERVATIVE
    ) -> list[str]:
        """Fix label-value line by adding <br> tag.

        Adds <br> at the end of the line (before newline if present).
        Strips trailing whitespace before adding <br>.

        Args:
            lines: All lines in file (0-indexed)
            violation: Violation to fix
            strategy: Fix strategy (not used by this rule)

        Returns:
            Modified lines with <br> added
        """
        line_idx = violation.line_number - 1  # Convert to 1-indexed
        if line_idx < 0 or line_idx >= len(lines):
            return lines

        line = lines[line_idx]

        # Strip trailing whitespace and newline
        stripped = line.rstrip()

        # Add <br> and restore newline if original had one
        if line.endswith('\n'):
            lines[line_idx] = stripped + "<br>\n"
        else:
            lines[line_idx] = stripped + "<br>"

        return lines


def get_all_rules() -> list[Rule]:
    """Get all enabled rules.

    Returns list of all currently enabled rule instances.
    Rules can be disabled by commenting them out in the return statement.

    Returns:
        List of instantiated rule objects
    """
    return [
        Rule1SemanticHeadings(),
        Rule2BlockSeparation(),
        Rule3HeadingIncrement(),
        Rule4NestedCodeBlocks(),
        Rule5LabelValueSequences(),
    ]
