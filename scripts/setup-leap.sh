#!/usr/bin/env bash
# setup-leap.sh — LEAP Bootstrapper / Workspace Configurator
#
# Helps consumers initialize their project's LEAP environment.
#
# Author: F. Andy Seidl (https://www.linkedin.com/in/faseidl/)
#
# Copyright 2026 Blunderstone LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -euo pipefail

# Duplicate stdin (FD 0) to FD 3 so prompts can read from keyboard/pipe even when stdin is redirected
exec 3<&0

# Configuration Overrides (defaults to empty meaning "not set/ask")
# If NON_INTERACTIVE is "true", any unset override will fall back to DEFAULT_ANSWER (e.g., 'n' or 'y')
NON_INTERACTIVE="false"
DEFAULT_ANSWER=""

OVERRIDE_SUBMODULE_RECURSE=""
OVERRIDE_CHECK_MD=""
OVERRIDE_CLAUDE=""
OVERRIDE_GEMINI=""
OVERRIDE_COPILOT=""
OVERRIDE_CURSOR=""
OVERRIDE_SKILLS=""
OVERRIDE_GITIGNORE=""
OVERRIDE_HOOKS=""
OVERRIDE_QMD=""

show_help() {
  cat << 'EOF'
Usage: setup-leap.sh [options]

Bootstraps a repository's agent-friendly Literate Programming (LEAP) environment.

Options:
  -y, --yes                 Run non-interactively and answer YES to all prompts not explicitly set
  -n, --no                  Run non-interactively and answer NO to all prompts not explicitly set
  --submodule-recurse       Enable automatic Git Submodule updates
  --check-md                Install check-md (Markdown Linter)
  --claude                  Configure Claude Guide (CLAUDE.md)
  --gemini                  Configure Gemini & Antigravity Guide (GEMINI.md)
  --copilot                 Configure GitHub Copilot Instructions (.github/copilot-instructions.md)
  --cursor                  Configure Cursor Rules (.cursorrules)
  --skills                  Install LEAP custom skills for your AI agents
  --gitignore               Configure project's .gitignore for LEAP
  --hooks                   Install LEAP git pre-commit hook (only for LEAP repository maintainers)
  --qmd                     Run QMD semantic search configurator
  -h, --help                Show this help message and exit
EOF
}

# Parse command line options
while [[ $# -gt 0 ]]; do
  case "$1" in
    -y|--yes)
      NON_INTERACTIVE="true"
      DEFAULT_ANSWER="y"
      shift
      ;;
    -n|--no)
      NON_INTERACTIVE="true"
      DEFAULT_ANSWER="n"
      shift
      ;;
    --submodule-recurse)
      OVERRIDE_SUBMODULE_RECURSE="y"
      shift
      ;;
    --check-md)
      OVERRIDE_CHECK_MD="y"
      shift
      ;;
    --claude)
      OVERRIDE_CLAUDE="y"
      shift
      ;;
    --gemini)
      OVERRIDE_GEMINI="y"
      shift
      ;;
    --copilot)
      OVERRIDE_COPILOT="y"
      shift
      ;;
    --cursor)
      OVERRIDE_CURSOR="y"
      shift
      ;;
    --skills)
      OVERRIDE_SKILLS="y"
      shift
      ;;
    --gitignore)
      OVERRIDE_GITIGNORE="y"
      shift
      ;;
    --hooks)
      OVERRIDE_HOOKS="y"
      shift
      ;;
    --qmd)
      OVERRIDE_QMD="y"
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      show_help >&2
      exit 1
      ;;
  esac
done

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Check if TTY
if [ ! -t 1 ]; then
  RED=''
  GREEN=''
  YELLOW=''
  BLUE=''
  BOLD=''
  NC=''
fi

print_step() {
  echo -e "\n${BLUE}${BOLD}==>${NC} ${BOLD}$1${NC}"
}

print_success() {
  echo -e "  ${GREEN}✓${NC} $1"
}

print_warning() {
  echo -e "  ${YELLOW}⚠${NC} $1"
}

# Helper variable to keep track of questions
PROMPT_RESULT=""

# Helper function to ask a Yes/No question with a default value and descriptive help text
ask_yes_no() {
  local prompt="$1"
  local default="$2"
  local explanation="$3"
  local override="${4:-}"
  
  # Normalize default to lowercase
  default=$(echo "$default" | tr '[:upper:]' '[:lower:]')
  
  # Check if we have an explicit override set
  if [ -n "$override" ]; then
    PROMPT_RESULT="$override"
    echo -e "\n${BOLD}${prompt}${NC} (Override: ${override})"
    return 0
  fi
  
  # If non-interactive mode is enabled, use default answer override or the prompt's default
  if [ "$NON_INTERACTIVE" = "true" ]; then
    PROMPT_RESULT="${DEFAULT_ANSWER:-$default}"
    # Ensure it's lowercase 'y' or 'n'
    PROMPT_RESULT=$(echo "$PROMPT_RESULT" | tr '[:upper:]' '[:lower:]')
    echo -e "\n${BOLD}${prompt}${NC} (Non-interactive: ${PROMPT_RESULT})"
    return 0
  fi
  
  echo -e "\n${BOLD}${prompt}${NC}"
  echo -e "  ${explanation}"
  
  local options="[y/n]"
  if [ "$default" = "y" ]; then
    options="[Y/n]"
  else
    options="[y/N]"
  fi
  
  while true; do
    echo -n "  Answer ${options}: "
    read -r response <&3
    response="${response:-$default}"
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
      PROMPT_RESULT="y"
      return 0
    elif [[ "$response" =~ ^[Nn]$ ]]; then
      PROMPT_RESULT="n"
      return 0
    else
      echo -e "  ${RED}Please enter 'y' for Yes or 'n' for No.${NC}"
    fi
  done
}

# Helper function to ask a choice with options and descriptive help text
ask_choice() {
  local prompt="$1"
  local default="$2"
  local explanation="$3"
  local allowed_regex="$4"
  local options_display="$5"
  
  if [ "$NON_INTERACTIVE" = "true" ]; then
    if [ "$DEFAULT_ANSWER" = "y" ]; then
      PROMPT_RESULT="o" # Overwrite by default in non-interactive YES mode
    else
      PROMPT_RESULT="s" # Skip by default in non-interactive NO mode
    fi
    echo -e "\n${BOLD}${prompt}${NC} (Non-interactive: ${PROMPT_RESULT})"
    return 0
  fi
  
  echo -e "\n${BOLD}${prompt}${NC}"
  echo -e "  ${explanation}"
  
  while true; do
    echo -n "  Answer ${options_display}: "
    read -r response <&3
    response="${response:-$default}"
    
    # Normalize to lowercase
    response=$(echo "$response" | tr '[:upper:]' '[:lower:]')
    
    if [[ "$response" =~ ^[$allowed_regex]$ ]]; then
      PROMPT_RESULT="$response"
      return 0
    else
      echo -e "  ${RED}Please enter one of the allowed options: ${allowed_regex}${NC}"
    fi
  done
}

# Helper function to write content to a file safely, prompting if it already exists
write_file_safe() {
  local file_path="$1"
  local description="$2"
  
  if [ -f "$file_path" ]; then
    echo -e "\n  ${YELLOW}File already exists:${NC} $file_path"
    echo "  This file may contain custom, user-written instructions."
    echo "  Note: Choosing to Overwrite or Append will automatically save a backup (e.g. $file_path.bak), making it easy to revert at any time."
    
    ask_choice "How would you like to handle the existing $file_path?" "s" "Select 'o' to overwrite with the LEAP template, 'a' to append LEAP guidelines to the end of the file, or 's' to safely skip and preserve it." "oas" "[o/a/S]"
    
    local choice="$PROMPT_RESULT"
    
    if [ "$choice" = "s" ]; then
      print_warning "Preserved existing $file_path without modification."
      # Consume/discard stdin from the heredoc redirect
      cat > /dev/null
      return 0
    elif [ "$choice" = "o" ]; then
      # Double confirmation
      ask_yes_no "Are you SURE you want to completely overwrite $file_path?" "n" "This will erase and replace all existing custom content in this file!"
      if [ "$PROMPT_RESULT" != "y" ]; then
        print_warning "Overwriting cancelled. Preserved existing $file_path without modification."
        # Consume/discard stdin from the heredoc redirect
        cat > /dev/null
        return 0
      fi
      
      # Save backup before overwriting
      cp "$file_path" "$file_path.bak"
      print_success "Saved backup copy of original to $file_path.bak"
      
    elif [ "$choice" = "a" ]; then
      # Save backup before appending
      local parent_dir
      parent_dir=$(dirname "$file_path")
      mkdir -p "$parent_dir"
      
      cp "$file_path" "$file_path.bak"
      print_success "Saved backup copy of original to $file_path.bak"
      
      # Append a divider and the new content to the file
      echo -e "\n\n# --- LEAP METHODOLOGY SECTION ---" >> "$file_path"
      cat >> "$file_path"
      print_success "Appended LEAP guidelines to $file_path."
      return 0
    fi
  fi
  
  # Ensure parent directory exists
  local parent_dir
  parent_dir=$(dirname "$file_path")
  mkdir -p "$parent_dir"
  
  cat > "$file_path"
  print_success "$description"
}

# 1. Verify working directory
REPO_ROOT=$(pwd)
LEAP_DIR="leap"
IS_SUBMODULE=false
if [ ! -d "leap" ]; then
  if [ -f "scripts/setup-leap.sh" ]; then
    LEAP_DIR="."
    print_warning "Running setup directly within the LEAP repository itself."
  else
    echo -e "${RED}Error: 'leap' directory not found in the current directory.${NC}"
    echo "Please run this script from the root of your consuming repository:"
    echo "  bash leap/scripts/setup-leap.sh"
    exit 1
  fi
fi

if [ -f ".gitmodules" ] && grep -q "path = leap" ".gitmodules"; then
  IS_SUBMODULE=true
fi

echo -e "${GREEN}${BOLD}Welcome to the LEAP Workspace Configurator!${NC}"
echo "This helper will bootstrap your project's agent-friendly Literate Programming environment."

# 2. Create kb/ directory
print_step "Setting up Knowledge Base"
if [ -d "kb" ]; then
  print_success "Found existing 'kb/' directory."
else
  mkdir -p kb
  print_success "Created empty 'kb/' directory in project root."
fi

# 2b. Configure Submodule Recurse (if submodule)
if [ "$IS_SUBMODULE" = true ]; then
  ask_yes_no "Enable automatic Git Submodule updates?" "y" "Configures Git to automatically update the 'leap' folder during checkout or pull commands so you do not need to sync submodules manually." "$OVERRIDE_SUBMODULE_RECURSE"
  if [ "$PROMPT_RESULT" = "y" ]; then
    git config submodule.recurse true
    print_success "Enabled automatic submodule recursion (submodule.recurse = true)."
  else
    print_warning "Skipped submodule auto-recurse. Remember to run 'git submodule update --init --recursive' manually."
  fi
fi

# 3. Help install check-md
print_step "Installing check-md (Markdown Linter)"
if command -v check-md &> /dev/null; then
  print_success "check-md is already installed and available on PATH."
else
  if command -v uv &> /dev/null; then
    echo "  Modern 'uv' package manager detected!"
    ask_yes_no "Install check-md globally using 'uv tool'?" "y" "Installs the markdown linter globally on your system PATH using the extremely fast 'uv' tool manager." "$OVERRIDE_CHECK_MD"
    if [ "$PROMPT_RESULT" = "y" ]; then
      uv tool install --editable "$LEAP_DIR/check-md"
      print_success "check-md installed successfully via uv tool."
    else
      print_warning "Skipped check-md global install. You can install it manually from '$LEAP_DIR/check-md'."
    fi
  elif command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
    command -v pip3 &> /dev/null && PIP_CMD="pip3"
    echo "  Python pip detected."
    ask_yes_no "Install check-md in your active Python environment?" "y" "Installs the markdown linter in your current Python terminal environment using pip." "$OVERRIDE_CHECK_MD"
    if [ "$PROMPT_RESULT" = "y" ]; then
      $PIP_CMD install -e "$LEAP_DIR/check-md[dev]"
      print_success "check-md installed successfully via pip."
    else
      print_warning "Skipped check-md install. You can install it manually from '$LEAP_DIR/check-md'."
    fi
  else
    print_warning "Python / pip not detected on PATH. Please install Python 3.10+ and install check-md from '$LEAP_DIR/check-md'."
  fi
fi

# 4. Agent Configuration files
print_step "Configuring AI Agent Instructions"
echo "LEAP works best when your AI assistant is explicitly instructed to follow LEAP principles."

# Function to write CLAUDE.md
write_claude() {
  write_file_safe "CLAUDE.md" "Created CLAUDE.md (Claude Code / Cline / Roo Code / Cursor)" << 'EOF'
# Claude Developer Guide (LEAP Compliant)

This project adopts the **Literate (Extended-by-Agent) Programming (LEAP)** methodology.

## Workspace Skills (Preferred)

If specialized workspace skills are available (e.g., `leap-start`, `leap-dev`, `leap-pr`, `leap-handoff`, `leap-finish`), you **MUST** activate and follow them for managing feature lifecycles, TDD, and phase reviews.

## Fallback LEAP Guidelines (If Skills Are Not Used)

1. **Documentation First**: Always review the requirements in `kb/feature/<username>/<feature-name>/goals.md` and the incremental phases in `plan.md` before editing code.
2. **Sequential Phase Gating**: Work on only **one phase at a time**. After completing a phase, stop, present your completed work (code and test coverage), and **wait for explicit human review and approval** before proceeding to any subsequent phase.
3. **Testing & Coverage**: Write tests progressively during each phase (TDD). Maintain a target of 90%+ coverage.
4. **Markdown Standards**: All Markdown documentation in `kb/` must conform to LEAP formatting rules.

## Global Markdown Validation (check-md)

The `check-md` Markdown linter is globally installed and available on your system PATH. You can execute it directly from any workspace directory:

- **Check files**: `check-md kb/`
- **Auto-fix violations**: `check-md kb/ --fix`

Always run `check-md` to verify formatting compliance. Do not bypass Markdown linter errors.

## Build and Test Commands

List your project-specific build and test commands here.

For example:

- **Build**: `npm run build` or `cargo build`
- **Test**: `npm run test` or `cargo test`
EOF
}

# Function to write GEMINI.md
write_gemini() {
  write_file_safe "GEMINI.md" "Created GEMINI.md (Gemini CLI / Antigravity CLI / AGENTS.md)" << 'EOF'
# Gemini & Antigravity Developer Guide (LEAP Compliant)

This project adopts the **Literate (Extended-by-Agent) Programming (LEAP)** paradigm.

## Workspace Skills (Preferred)

If specialized workspace skills are available (e.g., `leap-start`, `leap-dev`, `leap-pr`, `leap-handoff`, `leap-finish`), you **MUST** activate and follow them for managing feature lifecycles, TDD, and phase reviews.

## Fallback LEAP Guidelines (If Skills Are Not Used)

1. **Documentation First**: Scan the project's `kb/` directory and review the active feature folder `kb/feature/<username>/<feature-name>/`. Read `goals.md` and `plan.md` before coding.
2. **Sequential Phase Gating**: Work on only **one phase at a time**. After completing a phase, stop, present your completed work (code and test coverage), and **wait for explicit human review and approval** before proceeding to any subsequent phase.
3. **Testing Rigor**: All code edits must be backed by progressive automated test coverage. Target 90%+ coverage.
4. **Markdown Standards**: Ensure Markdown files comply with `check-md` Rules 1-5.

## Tooling Commands

The `check-md` Markdown linter is globally installed and available on your system PATH. You can execute it directly from any workspace directory:

- **Check MD Compliance**: `check-md kb/`
- **Auto-Fix MD Errors**: `check-md kb/ --fix`
- **Build Project**: [Insert project build command]
- **Run Tests**: [Insert project test command]
EOF
}

# Function to write copilot-instructions.md
write_copilot() {
  write_file_safe ".github/copilot-instructions.md" "Created .github/copilot-instructions.md (GitHub Copilot)" << 'EOF'
# GitHub Copilot Custom Instructions (LEAP Compliant)

This project adopts the **Literate (Extended-by-Agent) Programming (LEAP)** methodology.

- **LEAP Workspace Skills**: If specialized workspace skills are available (`leap-start`, `leap-dev`, etc.), prioritize using them.
- **Documentation First**: Always review the requirements in `kb/feature/<username>/<feature-name>/goals.md` and the incremental phases in `plan.md` before editing code.
- **Sequential Phase Gating**: Implement only one phase at a time. Pause and ask the developer for explicit review and approval before proceeding to the next phase.
- **Markdown Standards**: The `check-md` Markdown linter is globally installed on the PATH and can be run directly from any directory. Ensure all Markdown changes comply with `check-md` Rules 1-5.
- **Testing**: Maintain high test coverage (90%+). Proactively verify code behaves correctly.
EOF
}

# Function to write .cursorrules
write_cursor() {
  write_file_safe ".cursorrules" "Created .cursorrules (Cursor / Windsurf)" << 'EOF'
# Cursor Rules (LEAP Compliant)

This project adopts the **Literate (Extended-by-Agent) Programming (LEAP)** methodology.

- **LEAP Workspace Skills**: If specialized workspace skills are available (`leap-start`, `leap-dev`, etc.), prioritize activating and following them.
- **Documentation First**: Always check `kb/feature/<username>/<feature-name>/goals.md` and `plan.md` before modifying or creating code.
- **Sequential Phase Gating**: Implement only one phase at a time. Stop and ask the developer for explicit review and approval before proceeding to any subsequent phase.
- **Markdown Standards**: The `check-md` Markdown linter is globally installed on your system PATH and can be run directly from any directory. Ensure Markdown files comply with `check-md` Rules 1-5 (run `check-md kb/ --fix` to verify).
- **Testing**: Proactively write unit and integration tests (target 90%+ coverage).
EOF
}

# Function to configure .gitignore in the target repository
configure_gitignore() {
  local gitignore_path="$REPO_ROOT/.gitignore"
  local backup_gitignore="${gitignore_path}.bak"
  
  # Ensure the file exists
  touch "$gitignore_path"
  
  # Patterns to add
  local patterns=(
    "*.bak"
    "dev-note-*"
    "/.gemini/"
    "/.cursor/"
    "/.windsurf/"
    "/.claude/"
    "/.aider/"
  )
  
  local added_any=false
  for pattern in "${patterns[@]}"; do
    if ! grep -Fqx "$pattern" "$gitignore_path" &>/dev/null; then
      if [ "$added_any" = false ]; then
        # Save backup copy
        cp "$gitignore_path" "$backup_gitignore"
        print_success "Saved backup copy of original to $backup_gitignore"
        # Add a header before the first added pattern
        echo -e "\n# LEAP Environment & AI Agent Ignore Patterns" >> "$gitignore_path"
        added_any=true
      fi
      echo "$pattern" >> "$gitignore_path"
    fi
  done
  
  if [ "$added_any" = true ]; then
    print_success "Configured .gitignore to ignore agent rule folders, backup files, and dev notes."
  else
    print_success ".gitignore is already fully configured for LEAP rules."
  fi
}

INSTALLED_AGENTS=""

# Ask Claude
ask_yes_no "Configure Claude Guide (CLAUDE.md)?" "y" "Creates CLAUDE.md in your repository root, informing Claude-based coding agents (like Claude Code, Cline, Roo Code, and Cursor) to follow your LEAP rules." "$OVERRIDE_CLAUDE"
if [ "$PROMPT_RESULT" = "y" ]; then
  write_claude
  INSTALLED_AGENTS="${INSTALLED_AGENTS:+$INSTALLED_AGENTS,}claude"
fi

# Ask Gemini
ask_yes_no "Configure Gemini & Antigravity Guide (GEMINI.md)?" "y" "Creates GEMINI.md in your repository root, which the Gemini CLI and the next-generation Antigravity CLI (agy) natively parse on startup." "$OVERRIDE_GEMINI"
if [ "$PROMPT_RESULT" = "y" ]; then
  write_gemini
  INSTALLED_AGENTS="${INSTALLED_AGENTS:+$INSTALLED_AGENTS,}gemini"
fi

# Ask Copilot
ask_yes_no "Configure GitHub Copilot Instructions?" "y" "Creates .github/copilot-instructions.md to automatically instruct GitHub Copilot Chat to align with your LEAP guidelines." "$OVERRIDE_COPILOT"
if [ "$PROMPT_RESULT" = "y" ]; then
  write_copilot
fi

# Ask Cursor
ask_yes_no "Configure Cursor Rules (.cursorrules)?" "y" "Creates .cursorrules to automatically feed guidelines into Cursor's inline and chat-assistant contexts." "$OVERRIDE_CURSOR"
if [ "$PROMPT_RESULT" = "y" ]; then
  write_cursor
  INSTALLED_AGENTS="${INSTALLED_AGENTS:+$INSTALLED_AGENTS,}cursor,windsurf"
fi

# 4b. Configure Staged Agent Skills
print_step "Configuring Custom Agent Skills"
echo "LEAP provides pre-built, staged AI agent skills under '.skills/' (e.g. leap-start, leap-dev, leap-resume, leap-handoff, leap-finish, leap-pr)."

ask_yes_no "Install LEAP custom skills for your AI agents?" "y" "Creates relative symlinks projecting .skills/ custom instructions into your configured agent directories." "$OVERRIDE_SKILLS"
if [ "$PROMPT_RESULT" = "y" ]; then
  if [ -z "$INSTALLED_AGENTS" ]; then
    print_warning "No agents were configured (Claude, Gemini, or Cursor). Skipping custom skills installation."
  else
    if python3 "$LEAP_DIR/scripts/install-skills.py" "$INSTALLED_AGENTS" --repo-root "$REPO_ROOT" --skills-dir "$REPO_ROOT/$LEAP_DIR/.skills"; then
      print_success "LEAP custom agent skills installed successfully for: $INSTALLED_AGENTS."
    else
      print_warning "Failed to install agent skills."
    fi
  fi
else
  print_warning "Skipped custom agent skills installation."
fi

# 4c. Configure .gitignore for Local Rule Projections
print_step "Configuring .gitignore for LEAP Rule Projections"
echo "To prevent cluttering your repository's git status, local agent folders (.cursor/, .gemini/, etc.), .bak files, and dev notes should be ignored."

ask_yes_no "Configure your project's .gitignore for LEAP?" "y" "Appends standard LEAP and AI agent directories to your repository's .gitignore file." "$OVERRIDE_GITIGNORE"
if [ "$PROMPT_RESULT" = "y" ]; then
  configure_gitignore
else
  print_warning "Skipped .gitignore configuration."
fi

# 4d. Configure Git Pre-Commit Hook (Only for LEAP Repository Maintainers)
if [ "$LEAP_DIR" = "." ]; then
  print_step "Configuring Git Pre-Commit Hook"
  echo "The LEAP pre-commit hook automatically runs 'run-all-checks.sh' before any git commit, preventing broken code or linter failures from being committed."

  ask_yes_no "Install LEAP git pre-commit hook?" "y" "Installs the pre-commit hook into your active git repository to physically block broken commits." "$OVERRIDE_HOOKS"
  if [ "$PROMPT_RESULT" = "y" ]; then
    HOOK_DIR=""
    if [ -f ".git" ]; then
      # Submodule pointer file
      GIT_DIR_POINTER=$(cat .git)
      if [[ "$GIT_DIR_POINTER" =~ ^gitdir:\ (.*) ]]; then
        HOOK_DIR="${BASH_REMATCH[1]}/hooks"
      fi
    elif [ -d ".git" ]; then
      HOOK_DIR=".git/hooks"
    fi

    if [ -n "$HOOK_DIR" ]; then
      mkdir -p "$HOOK_DIR"
      HOOK_DEST="$HOOK_DIR/pre-commit"
      
      # Backup existing hook if present
      if [ -f "$HOOK_DEST" ]; then
        cp "$HOOK_DEST" "$HOOK_DEST.bak"
        print_success "Saved backup of existing pre-commit hook to $HOOK_DEST.bak"
      fi
      
      # Copy canonical pre-commit hook
      if [ -f "scripts/git-pre-commit" ]; then
        cp "scripts/git-pre-commit" "$HOOK_DEST"
        chmod +x "$HOOK_DEST"
        print_success "Installed pre-commit hook to $HOOK_DEST and marked as executable."
      else
        print_warning "Source pre-commit hook script not found at scripts/git-pre-commit."
      fi
    else
      print_warning "Could not determine git hooks directory. Skipped pre-commit hook installation."
    fi
  else
    print_warning "Skipped pre-commit hook installation."
  fi
fi

# 5. Configure QMD Semantic Search
print_step "Configuring QMD Semantic Search"
echo "QMD is an on-device semantic search engine that lets AI agents find your documentation."

ask_yes_no "Run QMD semantic search configurator?" "y" "Registers your document collections, registers your local project with the local AI agent, and installs pre-commit hooks to keep the index updated automatically." "$OVERRIDE_QMD"
QMD_FAILED=false
if [ "$PROMPT_RESULT" = "y" ]; then
  if bash "$LEAP_DIR/scripts/qmd/qmd-config" --repo-root "$REPO_ROOT" --remove-legacy; then
    print_success "QMD semantic search configured successfully."
  else
    print_warning "QMD configuration failed or was cancelled. You can retry via 'bash $LEAP_DIR/scripts/qmd/qmd-config --repo-root $REPO_ROOT --remove-legacy'."
    QMD_FAILED=true
  fi
else
  print_warning "Skipped QMD configuration."
fi

print_step "LEAP Initialization Complete!"
if [ "$QMD_FAILED" = true ]; then
  echo -e "${RED}${BOLD}LEAP Setup Incomplete (Warnings Detected)${NC}"
  echo "  - Please fix the QMD path errors or clean up any broken pre-commit hooks before committing!"
  echo "  - You can retry QMD setup via: bash $LEAP_DIR/scripts/qmd/qmd-config --repo-root $REPO_ROOT --remove-legacy"
  exit 1
else
  echo -e "${GREEN}${BOLD}Congratulations! Your project is now fully LEAP-ready.${NC}"
fi

echo -e "\nNext steps to start a new task:"
echo "1. Activate your AI agent in this repository."
echo "2. Guide your agent to execute the task using modern LEAP workspace skills!"
echo "   For example, tell your agent to start the next feature branch:"
echo -e "     ${BLUE}\"Activate the skill 'leap-start' (or run /leap-start) to initialize our new feature for [description].\"${NC}"
