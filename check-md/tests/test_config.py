"""
test_config.py — Tests for configuration file support.

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
from pathlib import Path

import pytest

from check_md.config import CheckMdConfig, RuleConfig, ScoringConfig


class TestCheckMdConfig:
    """Tests for CheckMdConfig loading and parsing."""

    def test_load_empty_config(self) -> None:
        """Should handle empty config file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write("")
            temp_path = Path(f.name)

        try:
            config = CheckMdConfig.load(temp_path)
            assert config.rules == {}
            assert config.scoring.minimum_project_score == 80
            assert config.exclude == []
        finally:
            temp_path.unlink()

    def test_load_rules_config(self) -> None:
        """Should parse rules configuration."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write(
                """
rules:
  rule_1:
    enabled: true
    severity: error
  rule_2:
    enabled: false
    severity: warning
  rule_4:
    enabled: true
    severity: info
"""
            )
            temp_path = Path(f.name)

        try:
            config = CheckMdConfig.load(temp_path)
            assert config.rules["rule_1"].enabled is True
            assert config.rules["rule_1"].severity == "error"
            assert config.rules["rule_2"].enabled is False
            assert config.rules["rule_2"].severity == "warning"
            assert config.rules["rule_4"].enabled is True
            assert config.rules["rule_4"].severity == "info"
        finally:
            temp_path.unlink()

    def test_load_simple_boolean_rules(self) -> None:
        """Should parse simple boolean rule config."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write(
                """
rules:
  rule_1: true
  rule_2: false
"""
            )
            temp_path = Path(f.name)

        try:
            config = CheckMdConfig.load(temp_path)
            assert config.rules["rule_1"].enabled is True
            assert config.rules["rule_2"].enabled is False
        finally:
            temp_path.unlink()

    def test_load_scoring_config(self) -> None:
        """Should parse scoring configuration."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write(
                """
scoring:
  minimum_project_score: 85
  minimum_module_score: 75
"""
            )
            temp_path = Path(f.name)

        try:
            config = CheckMdConfig.load(temp_path)
            assert config.scoring.minimum_project_score == 85
            assert config.scoring.minimum_module_score == 75
        finally:
            temp_path.unlink()

    def test_load_exclude_patterns(self) -> None:
        """Should parse exclusion patterns."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write(
                """
exclude:
  - "node_modules/**"
  - "build/**"
  - "*.generated.md"
"""
            )
            temp_path = Path(f.name)

        try:
            config = CheckMdConfig.load(temp_path)
            assert config.exclude == ["node_modules/**", "build/**", "*.generated.md"]
        finally:
            temp_path.unlink()

    def test_load_complete_config(self) -> None:
        """Should parse complete configuration file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write(
                """
rules:
  rule_1:
    enabled: true
    severity: error
  rule_2:
    enabled: true
    severity: error
  rule_4:
    enabled: false
    severity: warning

scoring:
  minimum_project_score: 90
  minimum_module_score: 85

exclude:
  - "node_modules/**"
  - "build/**"
"""
            )
            temp_path = Path(f.name)

        try:
            config = CheckMdConfig.load(temp_path)
            assert len(config.rules) == 3
            assert config.rules["rule_4"].enabled is False
            assert config.scoring.minimum_project_score == 90
            assert len(config.exclude) == 2
        finally:
            temp_path.unlink()

    def test_is_rule_enabled_default(self) -> None:
        """Should return True for unconfigured rules."""
        config = CheckMdConfig()
        assert config.is_rule_enabled("ADR-002-R1") is True
        assert config.is_rule_enabled("ADR-002-R2") is True
        assert config.is_rule_enabled("ADR-002-R4") is True

    def test_is_rule_enabled_configured(self) -> None:
        """Should respect configured rule state."""
        config = CheckMdConfig(
            rules={
                "rule_1": RuleConfig(enabled=True),
                "rule_2": RuleConfig(enabled=False),
            }
        )
        assert config.is_rule_enabled("ADR-002-R1") is True
        assert config.is_rule_enabled("ADR-002-R2") is False
        assert config.is_rule_enabled("ADR-002-R4") is True  # default

    def test_get_rule_severity_default(self) -> None:
        """Should return 'error' for unconfigured rules."""
        config = CheckMdConfig()
        assert config.get_rule_severity("ADR-002-R1") == "error"
        assert config.get_rule_severity("ADR-002-R2") == "error"

    def test_get_rule_severity_configured(self) -> None:
        """Should return configured severity."""
        config = CheckMdConfig(
            rules={
                "rule_1": RuleConfig(enabled=True, severity="warning"),
                "rule_2": RuleConfig(enabled=True, severity="info"),
            }
        )
        assert config.get_rule_severity("ADR-002-R1") == "warning"
        assert config.get_rule_severity("ADR-002-R2") == "info"
        assert config.get_rule_severity("ADR-002-R4") == "error"  # default

    def test_find_config_in_current_directory(self) -> None:
        """Should find config in current directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir).resolve()
            config_path = temp_path / ".check-md.yml"
            config_path.write_text("rules: {}")

            found = CheckMdConfig.find_config(temp_path)
            assert found is not None
            assert found.resolve() == config_path.resolve()

    def test_find_config_in_parent_directory(self) -> None:
        """Should find config in parent directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir).resolve()
            config_path = temp_path / ".check-md.yml"
            config_path.write_text("rules: {}")

            # Search from subdirectory
            subdir = temp_path / "subdir"
            subdir.mkdir()

            found = CheckMdConfig.find_config(subdir)
            assert found is not None
            assert found.resolve() == config_path.resolve()

    def test_find_config_not_found(self) -> None:
        """Should return None if config not found."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir)
            found = CheckMdConfig.find_config(temp_path)
            assert found is None

    def test_load_raises_on_missing_file(self) -> None:
        """Should raise FileNotFoundError for missing config."""
        with pytest.raises(FileNotFoundError):
            CheckMdConfig.load(Path("/nonexistent/.check-md.yml"))

    def test_load_exclude_non_list_value(self) -> None:
        """Should handle non-list exclude value gracefully."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
            f.write(
                """
exclude: "single_string_not_list"
"""
            )
            temp_path = Path(f.name)

        try:
            config = CheckMdConfig.load(temp_path)
            # Should default to empty list when exclude is not a list
            assert config.exclude == []
        finally:
            temp_path.unlink()
