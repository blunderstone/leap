"""
test_version.py — Test suite for release version configuration and alignment.

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

import json
from pathlib import Path
import re
import yaml
import check_md

def test_version_alignment():
    # 1. Check version in check_md package
    pkg_version = check_md.__version__
    assert pkg_version == "1.0.0-beta.0", f"Package version in check_md.__init__ is {pkg_version}, expected 1.0.0-beta.0"

    # Find pyproject.toml
    test_dir = Path(__file__).parent
    pyproject_path = test_dir / "../pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml does not exist"

    # Read and parse pyproject.toml version
    pyproject_content = pyproject_path.read_text()
    version_match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject_content, re.MULTILINE)
    assert version_match, "Could not find version in pyproject.toml"
    toml_version = version_match.group(1)
    assert toml_version == "1.0.0-beta.0", f"pyproject.toml version is {toml_version}, expected 1.0.0-beta.0"

    # 2. Check uv.lock version for check-md package
    uv_lock_path = test_dir / "../uv.lock"
    assert uv_lock_path.exists(), "uv.lock does not exist"
    uv_content = uv_lock_path.read_text()
    # Search for package check-md and grab its version
    # Since uv.lock is TOML, we can do a simple block-based search
    blocks = uv_content.split("[[package]]")
    check_md_lock_version = None
    for block in blocks:
        if 'name = "check-md"' in block:
            v_match = re.search(r'version\s*=\s*"([^"]+)"', block)
            if v_match:
                check_md_lock_version = v_match.group(1)
                break
    
    assert check_md_lock_version == "1.0.0-beta.0", f"uv.lock package version for check-md is {check_md_lock_version}, expected 1.0.0-beta.0"

    # 3. Check .release-please-manifest.json
    manifest_path = test_dir / "../../.release-please-manifest.json"
    assert manifest_path.exists(), ".release-please-manifest.json does not exist"
    with open(manifest_path, "r") as f:
        manifest_data = json.load(f)
    assert "." in manifest_data, "Manifest does not contain root package '.' entry"
    assert manifest_data["."] == "1.0.0-beta.0", f"Manifest version is {manifest_data['.']}, expected 1.0.0-beta.0"

    # 4. Check release-please-config.json
    config_path = test_dir / "../../release-please-config.json"
    assert config_path.exists(), "release-please-config.json does not exist"
    with open(config_path, "r") as f:
        config_data = json.load(f)
    assert "$schema" in config_data, "Config does not have a $schema"
    assert "packages" in config_data, "Config does not define 'packages'"

def test_github_action_workflow():
    test_dir = Path(__file__).parent
    workflow_path = test_dir / "../../.github/workflows/release-please.yml"
    assert workflow_path.exists(), "release-please.yml workflow does not exist"
    
    with open(workflow_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Assert trigger is push to main
    assert "on" in config, "workflow must have 'on' trigger"
    on_trigger = config["on"]
    assert "push" in on_trigger, "workflow must trigger on push"
    assert "branches" in on_trigger["push"], "push trigger must restrict branches"
    assert "main" in on_trigger["push"]["branches"], "push trigger must include 'main'"

    # Assert permissions
    assert "permissions" in config, "workflow must declare explicit permissions"
    perms = config["permissions"]
    assert perms.get("contents") == "write", "contents permission must be write"
    assert perms.get("pull-requests") == "write", "pull-requests permission must be write"

