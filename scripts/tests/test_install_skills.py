#!/usr/bin/env python3
"""
test_install_skills.py — Unit tests for install-skills.py script.

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

import os
import sys
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

# Adjust path to import install-skills module
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(SCRIPTS_DIR))

# Import target functions and configs from install-skills
import importlib
install_skills_mod = importlib.import_module("install-skills")


class TestInstallSkills(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name)
        self.skills_dir = self.project_root / ".skills"
        self.skills_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_skill_name_with_yaml(self):
        """Should parse name from YAML frontmatter correctly."""
        skill_dir = self.skills_dir / "test-skill-frontmatter"
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: parsed-skill-name\n"
            "version: 1.0.0\n"
            "---\n\n"
            "# Test Skill",
            encoding="utf-8"
        )
        
        name = install_skills_mod.get_skill_name(skill_dir)
        self.assertEqual(name, "parsed-skill-name")

    def test_get_skill_name_with_quoted_yaml(self):
        """Should strip quotes from YAML name if present."""
        skill_dir = self.skills_dir / "test-skill-quoted"
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: \"quoted-skill-name\"\n"
            "---\n",
            encoding="utf-8"
        )
        
        name = install_skills_mod.get_skill_name(skill_dir)
        self.assertEqual(name, "quoted-skill-name")

    def test_get_skill_name_fallback(self):
        """Should fall back to directory name if YAML frontmatter is absent."""
        skill_dir = self.skills_dir / "my-fallback-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("# Bare Skill with No Frontmatter", encoding="utf-8")
        
        name = install_skills_mod.get_skill_name(skill_dir)
        self.assertEqual(name, "my-fallback-skill")

    def test_install_skills_symlink(self):
        """Should create relative symlinks for all target agents."""
        # Create a test skill
        skill_dir = self.skills_dir / "leap-test"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: leap-test\n---\n# Content", encoding="utf-8")

        # Run installation
        install_skills_mod.install_skills(
            target_agent="all", 
            use_symlinks=True, 
            repo_root=self.project_root, 
            skills_dir=self.skills_dir
        )

        # Check projections for each agent
        agent_configs = {
            "gemini": self.project_root / ".gemini" / "skills" / "leap-test" / "SKILL.md",
            "cursor": self.project_root / ".cursor" / "rules" / "leap-test.mdc",
            "windsurf": self.project_root / ".windsurf" / "rules" / "leap-test.md",
            "claude": self.project_root / ".claude" / "commands" / "leap-test.md",
            "aider": self.project_root / ".aider" / "prompts" / "leap-test.md"
        }

        for agent, target_file in agent_configs.items():
            self.assertTrue(target_file.is_symlink(), f"Target {target_file} should be a symlink")
            
            # Verify relative symlink resolves correctly
            resolved_path = Path(os.readlink(target_file))
            self.assertFalse(resolved_path.is_absolute(), f"Symlink target {resolved_path} should be relative")
            
            full_resolved = (target_file.parent / resolved_path).resolve()
            self.assertEqual(full_resolved, skill_md.resolve())

    def test_install_skills_copy(self):
        """Should copy file contents directly when use_symlinks is False."""
        # Create a test skill
        skill_dir = self.skills_dir / "leap-test"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: leap-test\n---\n# Content", encoding="utf-8")

        # Run installation in copy mode
        install_skills_mod.install_skills(
            target_agent="all", 
            use_symlinks=False, 
            repo_root=self.project_root, 
            skills_dir=self.skills_dir
        )

        # Check physical file projections
        agent_configs = {
            "gemini": self.project_root / ".gemini" / "skills" / "leap-test" / "SKILL.md",
            "cursor": self.project_root / ".cursor" / "rules" / "leap-test.mdc",
            "windsurf": self.project_root / ".windsurf" / "rules" / "leap-test.md",
            "claude": self.project_root / ".claude" / "commands" / "leap-test.md",
            "aider": self.project_root / ".aider" / "prompts" / "leap-test.md"
        }

        for agent, target_file in agent_configs.items():
            self.assertTrue(target_file.exists())
            self.assertFalse(target_file.is_symlink())
            self.assertEqual(target_file.read_text(encoding="utf-8"), skill_md.read_text(encoding="utf-8"))

    def test_install_selective_agent(self):
        """Should install only for the requested selective agent."""
        # Create a test skill
        skill_dir = self.skills_dir / "leap-test"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: leap-test\n---\n# Content", encoding="utf-8")

        # Install for gemini only
        install_skills_mod.install_skills(
            target_agent="gemini", 
            use_symlinks=True, 
            repo_root=self.project_root, 
            skills_dir=self.skills_dir
        )

        # Gemini should exist
        gemini_target = self.project_root / ".gemini" / "skills" / "leap-test" / "SKILL.md"
        self.assertTrue(gemini_target.is_symlink())

        # Cursor should NOT exist
        cursor_target = self.project_root / ".cursor" / "rules" / "leap-test.mdc"
        self.assertFalse(cursor_target.exists())

    def test_install_skills_overwrite(self):
        """Should safely overwrite existing symlinks/files on subsequent runs."""
        skill_dir = self.skills_dir / "leap-test"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("---\nname: leap-test\n---\n# Original", encoding="utf-8")

        # Install first time
        install_skills_mod.install_skills(
            target_agent="gemini", 
            use_symlinks=True, 
            repo_root=self.project_root, 
            skills_dir=self.skills_dir
        )
        gemini_target = self.project_root / ".gemini" / "skills" / "leap-test" / "SKILL.md"
        self.assertTrue(gemini_target.is_symlink())

        # Modify source
        skill_md.write_text("---\nname: leap-test\n---\n# Updated", encoding="utf-8")

        # Install second time in copy mode to overwrite
        install_skills_mod.install_skills(
            target_agent="gemini", 
            use_symlinks=False, 
            repo_root=self.project_root, 
            skills_dir=self.skills_dir
        )
        self.assertTrue(gemini_target.exists())
        self.assertFalse(gemini_target.is_symlink())
        self.assertEqual(gemini_target.read_text(encoding="utf-8"), skill_md.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
