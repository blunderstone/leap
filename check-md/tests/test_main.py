"""
test_main.py — Tests for __main__.py module entry point.

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

import subprocess
import sys


def test_main_module_execution() -> None:
    """Should execute as module with python -m check_md."""
    # Run check-md as module with --help flag
    result = subprocess.run(
        [sys.executable, "-m", "check_md", "--help"],
        capture_output=True,
        text=True,
        timeout=5
    )

    # Should exit successfully
    assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}\nStderr: {result.stderr}"

    # Should show help text - strip leading whitespace for assertion
    stripped_output = result.stdout.strip()
    assert stripped_output.startswith("Usage:"), \
        f"Expected help to start with 'Usage:', got:\n{stripped_output[:100]}"

    # Should contain key CLI options
    assert "--fix" in result.stdout, "Help should mention --fix option"
    assert "--format" in result.stdout, "Help should mention --format option"
