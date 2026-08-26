"""
config.py — Configuration file support for check-md.

This module handles loading and parsing .check-md.yml configuration files.

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

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import yaml


@dataclass
class RuleConfig:
    """Configuration for a single rule.

    Attributes:
        enabled: Whether the rule is enabled
        severity: Severity level (error, warning, info)
    """

    enabled: bool = True
    severity: str = "error"


@dataclass
class ScoringConfig:
    """Configuration for compliance scoring.

    Attributes:
        minimum_project_score: Minimum acceptable project score (0-100)
        minimum_module_score: Minimum acceptable module score (0-100)
    """

    minimum_project_score: int = 80
    minimum_module_score: Optional[int] = None


@dataclass
class CheckMdConfig:
    """Complete configuration for check-md.

    Attributes:
        rules: Configuration for each rule (by rule_id)
        scoring: Scoring thresholds
        exclude: List of glob patterns to exclude from checking
    """

    rules: Dict[str, RuleConfig] = field(default_factory=dict)
    scoring: ScoringConfig = field(default_factory=ScoringConfig)
    exclude: List[str] = field(default_factory=list)

    @classmethod
    def load(cls, config_path: Path) -> "CheckMdConfig":
        """Load configuration from YAML file.

        Args:
            config_path: Path to .check-md.yml file

        Returns:
            Parsed configuration object

        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If config file is malformed
        """
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if data is None:
            data = {}

        # Parse rules
        rules = {}
        if "rules" in data:
            for rule_id, rule_data in data["rules"].items():
                if isinstance(rule_data, dict):
                    rules[rule_id] = RuleConfig(
                        enabled=rule_data.get("enabled", True),
                        severity=rule_data.get("severity", "error"),
                    )
                else:
                    # Simple boolean: rules: { rule_1: true }
                    rules[rule_id] = RuleConfig(enabled=bool(rule_data))

        # Parse scoring
        scoring = ScoringConfig()
        if "scoring" in data:
            scoring_data = data["scoring"]
            if isinstance(scoring_data, dict):
                scoring = ScoringConfig(
                    minimum_project_score=scoring_data.get("minimum_project_score", 80),
                    minimum_module_score=scoring_data.get("minimum_module_score"),
                )

        # Parse exclude patterns
        exclude = data.get("exclude", [])
        if not isinstance(exclude, list):
            exclude = []

        return cls(rules=rules, scoring=scoring, exclude=exclude)

    @classmethod
    def find_config(cls, start_path: Path) -> Optional[Path]:
        """Find .check-md.yml in current directory or parent directories.

        Searches upward from start_path until a .check-md.yml file is found
        or the filesystem root is reached.

        Args:
            start_path: Directory to start search from

        Returns:
            Path to config file, or None if not found
        """
        current = start_path.resolve()

        # Search upward through parent directories
        while True:
            config_path = current / ".check-md.yml"
            if config_path.exists():
                return config_path

            # Check if we've reached the root
            parent = current.parent
            if parent == current:
                return None

            current = parent

    def is_rule_enabled(self, rule_id: str) -> bool:
        """Check if a rule is enabled.

        Args:
            rule_id: Rule identifier (e.g., "ADR-002-R1")

        Returns:
            True if rule is enabled (default: True if not configured)
        """
        # Map full rule IDs to config keys
        rule_key_map = {
            "ADR-002-R1": "rule_1",
            "ADR-002-R2": "rule_2",
            "ADR-002-R4": "rule_4",
        }

        rule_key = rule_key_map.get(rule_id, rule_id)

        if rule_key in self.rules:
            return self.rules[rule_key].enabled

        # Default: enabled
        return True

    def get_rule_severity(self, rule_id: str) -> str:
        """Get severity level for a rule.

        Args:
            rule_id: Rule identifier (e.g., "ADR-002-R1")

        Returns:
            Severity level: "error", "warning", or "info" (default: "error")
        """
        # Map full rule IDs to config keys
        rule_key_map = {
            "ADR-002-R1": "rule_1",
            "ADR-002-R2": "rule_2",
            "ADR-002-R4": "rule_4",
        }

        rule_key = rule_key_map.get(rule_id, rule_id)

        if rule_key in self.rules:
            return self.rules[rule_key].severity

        # Default: error
        return "error"
