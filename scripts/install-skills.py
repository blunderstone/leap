#!/usr/bin/env python3
"""
install-skills.py — Installs skills from canonical .skills/ into agent directories.

Installs skills from canonical .skills/<skill-name>/SKILL.md into agent directories.
Supports: gemini, cursor, windsurf, claude, aider, all
Supports submodule consumption via --repo-root and --skills-dir.

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
from pathlib import Path

# Base default paths relative to this script
SCRIPT_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_skill_name(skill_dir: Path) -> str:
    """Extract name from YAML frontmatter if present; fallback to directory name."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return skill_dir.name
    
    try:
        lines = skill_file.read_text(encoding="utf-8").splitlines()
        if lines and lines[0].strip() == "---":
            for line in lines[1:]:
                if line.strip() == "---":
                    break
                if line.startswith("name:"):
                    return line.split(":", 1)[1].strip().strip('"\'')
    except Exception:
        pass

    return skill_dir.name


def install_skills(target_agent: str = "all", use_symlinks: bool = True, repo_root: Path = None, skills_dir: Path = None):
    # Resolve roots with fallbacks
    repo_root = repo_root or SCRIPT_PROJECT_ROOT
    skills_dir = skills_dir or (repo_root / ".skills")

    if not skills_dir.exists():
        print(f"Error: Canonical skills directory '{skills_dir}' not found.")
        sys.exit(1)

    # Dynamic target agent configuration mapping based on repo_root
    agent_configs = {
        "gemini": {
            "dir": repo_root / ".gemini" / "skills",
            "nested": True,
        },
        "cursor": {
            "dir": repo_root / ".cursor" / "rules",
            "ext": ".mdc",
        },
        "windsurf": {
            "dir": repo_root / ".windsurf" / "rules",
            "ext": ".md",
        },
        "claude": {
            "dir": repo_root / ".claude" / "commands",
            "ext": ".md",
        },
        "aider": {
            "dir": repo_root / ".aider" / "prompts",
            "ext": ".md",
        }
    }

    # Normalize target_agent input
    target_agent = target_agent.lower().strip()
    
    targets = list(agent_configs.keys()) if target_agent == "all" else [target_agent]

    # Validate target agent selection
    for agent in targets:
        if agent not in agent_configs:
            print(f"Error: Unknown agent '{agent}'. Supported: {', '.join(agent_configs.keys())}, all")
            sys.exit(1)

    # Clean up old legacy paths if present
    if "gemini" in targets:
        legacy_dir = repo_root / ".gemini" / "instructions"
        if legacy_dir.exists():
            print(f"Cleaning up legacy Gemini instructions directory: {legacy_dir.relative_to(repo_root)}")
            shutil.rmtree(legacy_dir)

    installed_count = 0

    for skill_path in skills_dir.iterdir():
        if not skill_path.is_dir():
            continue

        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue

        skill_name = get_skill_name(skill_path)

        for agent in targets:
            cfg = agent_configs.get(agent)
            if cfg.get("nested"):
                target_dir = cfg["dir"] / skill_name
                target_file = target_dir / "SKILL.md"
            else:
                target_dir = cfg["dir"]
                target_file = target_dir / f"{skill_name}{cfg['ext']}"

            target_dir.mkdir(parents=True, exist_ok=True)

            # Remove existing link/file if present
            if target_file.exists() or target_file.is_symlink():
                target_file.unlink()

            if use_symlinks:
                # Relative symlink keeps the repository portable across environments
                rel_source = Path(os.path.relpath(skill_md, start=target_dir))
                target_file.symlink_to(rel_source)
                display_target = f"{skill_name}/{target_file.name}" if cfg.get("nested") else target_file.name
                print(f"[{agent}] Linked {display_target} -> {skill_md.relative_to(repo_root)}")
            else:
                shutil.copy2(skill_md, target_file)
                display_target = f"{skill_name}/{target_file.name}" if cfg.get("nested") else target_file.name
                print(f"[{agent}] Copied {skill_md.relative_to(repo_root)} -> {display_target}")
            
            installed_count += 1

    print(f"\nDone: successfully installed {installed_count} skill projections.")


if __name__ == "__main__":
    # Filter arguments
    use_copy = "--copy" in sys.argv
    
    # Custom --repo-root parsing
    repo_root_path = None
    if "--repo-root" in sys.argv:
        try:
            idx = sys.argv.index("--repo-root")
            repo_root_path = Path(sys.argv[idx + 1]).resolve()
        except IndexError:
            print("Error: --repo-root expects a directory path.")
            sys.exit(1)

    # Custom --skills-dir parsing
    skills_dir_path = None
    if "--skills-dir" in sys.argv:
        try:
            idx = sys.argv.index("--skills-dir")
            skills_dir_path = Path(sys.argv[idx + 1]).resolve()
        except IndexError:
            print("Error: --skills-dir expects a directory path.")
            sys.exit(1)

    # Clean out parsed arguments to isolate the positional target_agent
    clean_args = [
        arg for arg in sys.argv[1:] 
        if arg not in ("--copy", "--repo-root", "--skills-dir")
        and (len(sys.argv) <= sys.argv.index(arg) or sys.argv[sys.argv.index(arg) - 1] not in ("--repo-root", "--skills-dir"))
    ]
    
    agent_arg = clean_args[0] if clean_args else "all"
    install_skills(
        target_agent=agent_arg, 
        use_symlinks=not use_copy, 
        repo_root=repo_root_path, 
        skills_dir=skills_dir_path
    )
