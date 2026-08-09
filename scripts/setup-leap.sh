#!/usr/bin/env bash

# LEAP Bootstrapper / Workspace Configurator
# Helps consumers initialize their project's LEAP environment.

set -euo pipefail

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
  
  echo -e "\n${BOLD}${prompt}${NC}"
  echo -e "  ${explanation}"
  
  local options="[y/n]"
  if [ "$default" = "y" ] || [ "$default" = "Y" ]; then
    options="[Y/n]"
    default="y"
  else
    options="[y/N]"
    default="n"
  fi
  
  while true; do
    echo -n "  Answer ${options}: "
    read -r response
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

# Helper function to write content to a file safely, prompting if it already exists
write_file_safe() {
  local file_path="$1"
  local description="$2"
  
  if [ -f "$file_path" ]; then
    echo -e "\n  ${YELLOW}File already exists:${NC} $file_path"
    echo "  This file may contain custom, user-written instructions."
    ask_yes_no "Overwrite existing $file_path?" "n" "Select 'y' to replace the existing file with the standard LEAP configuration, or 'n' to safely preserve your custom file."
    if [ "$PROMPT_RESULT" != "y" ]; then
      print_warning "Preserved existing $file_path."
      # Consume/discard stdin
      cat > /dev/null
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
  ask_yes_no "Enable automatic Git Submodule updates?" "y" "Configures Git to automatically update the 'leap' folder during checkout or pull commands so you do not need to sync submodules manually."
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
    ask_yes_no "Install check-md globally using 'uv tool'?" "y" "Installs the markdown linter globally on your system PATH using the extremely fast 'uv' tool manager."
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
    ask_yes_no "Install check-md in your active Python environment?" "y" "Installs the markdown linter in your current Python terminal environment using pip."
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

This project follows the **Literate (Extended-by-Agent) Programming (LEAP)** methodology. Please respect the following guidelines for all code changes, architecture decisions, and feature implementations.

## LEAP Principles

1. **Documentation First**: Before modifying or creating code, check if there is an active feature branch folder in `kb/feature/<username>/<feature-name>/`.
   - Ensure a `goals.md` exists outlining the requirements.
   - For complex, multi-phase changes, verify there is an execution `plan.md`.
   - Update plans and document phase completions as you work.
2. **Test Throughout**: Write unit and integration tests for every implemented phase. Target 90%+ coverage.
3. **Completion Summary**: Create or update `completion-summary.md` in the feature folder before considering the implementation complete.
4. **Agent-Friendly Style**: All Markdown documents in `kb/` must conform to LEAP Markdown standards (semantic headings, blank line block separation, consecutive metadata `<br>` tags).

## Markdown Compliance (check-md)

Always lint and format markdown documents before finalizing them. This project uses the `check-md` utility.

- **Check files**: `check-md kb/`
- **Auto-fix violations**: `check-md kb/ --fix`

Run `check-md` to verify formatting compliance. Do not bypass markdown errors.

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

This project adopts the **Literate (Extended-by-Agent) Programming (LEAP)** paradigm. Every task must be carried out following our documentation-first and testing-first lifecycle.

## LEAP Paradigm Guidelines

1. **Knowledge Retrieval**: Always scan the project's root `kb/` directory first. Familiarize yourself with design constraints, guide documents (`leap/kb/guide-*.md`), and implementation blueprints (`leap/kb/impl-*.md`).
2. **Feature Branch Lifecycle**:
   - Locate your feature directory at `kb/feature/<username>/<feature-name>/`.
   - Read `goals.md` and `plan.md` before coding.
   - Author detailed phase journals (`phase-1.md`, etc.) for complex features.
   - Document a comprehensive summary in `completion-summary.md` on completion.
3. **Testing Rigor**: All code edits must be backed by automated test coverage. Proactively run the test commands.
4. **Markdown Standards**: Markdown files must strictly comply with `check-md` Rules 1-5.

## Tooling Commands

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

This project follows the **Literate (Extended-by-Agent) Programming (LEAP)** methodology. Please respect the following guidelines for all code changes, architecture decisions, and feature implementations.

- **Documentation First**: Always respect and follow requirements and plans inside the `kb/` directory, specifically `kb/feature/<username>/<feature-name>/goals.md` and `plan.md`.
- **Markdown Standards**: Ensure markdown changes comply with check-md standards:
  - Separate block elements with empty lines.
  - Use proper headings (# for title, ##, ###, etc.) instead of bold text.
  - Use <br> tags for consecutive metadata lists.
- **Testing**: Maintain high test coverage (90%+). Proactively verify code behaves correctly.
EOF
}

# Function to write .cursorrules
write_cursor() {
  write_file_safe ".cursorrules" "Created .cursorrules (Cursor / Windsurf)" << 'EOF'
# Cursor Rules (LEAP Compliant)

This project follows the **Literate (Extended-by-Agent) Programming (LEAP)** methodology. Please respect the following guidelines for all code changes, architecture decisions, and feature implementations.

- **Documentation First**: Always check `kb/feature/<username>/<feature-name>/goals.md` and `plan.md` before modifying or creating code.
- **Markdown Standards**: Ensure markdown files comply with check-md rules (proper headings, blank lines around code blocks/lists, <br> for metadata). Run `check-md kb/ --fix` to verify.
- **Testing**: Proactively write unit and integration tests. Target 90%+ coverage.
EOF
}

# Ask Claude
ask_yes_no "Configure Claude Guide (CLAUDE.md)?" "y" "Creates CLAUDE.md in your repository root, informing Claude-based coding agents (like Claude Code, Cline, Roo Code, and Cursor) to follow your LEAP rules."
if [ "$PROMPT_RESULT" = "y" ]; then
  write_claude
fi

# Ask Gemini
ask_yes_no "Configure Gemini & Antigravity Guide (GEMINI.md)?" "y" "Creates GEMINI.md in your repository root, which the Gemini CLI and the next-generation Antigravity CLI (agy) natively parse on startup."
if [ "$PROMPT_RESULT" = "y" ]; then
  write_gemini
fi

# Ask Copilot
ask_yes_no "Configure GitHub Copilot Instructions?" "n" "Creates .github/copilot-instructions.md to automatically instruct GitHub Copilot Chat to align with your LEAP guidelines."
if [ "$PROMPT_RESULT" = "y" ]; then
  write_copilot
fi

# Ask Cursor
ask_yes_no "Configure Cursor Rules (.cursorrules)?" "n" "Creates .cursorrules to automatically feed guidelines into Cursor's inline and chat-assistant contexts."
if [ "$PROMPT_RESULT" = "y" ]; then
  write_cursor
fi

# 5. Configure QMD Semantic Search
print_step "Configuring QMD Semantic Search"
echo "QMD is an on-device semantic search engine that lets AI agents find your documentation."

ask_yes_no "Run QMD semantic search configurator?" "y" "Registers your document collections, registers your local project with the local AI agent, and installs pre-commit hooks to keep the index updated automatically."
QMD_FAILED=false
if [ "$PROMPT_RESULT" = "y" ]; then
  if bash "$LEAP_DIR/scripts/qmd/qmd-config" --repo-root "$REPO_ROOT"; then
    print_success "QMD semantic search configured successfully."
  else
    print_warning "QMD configuration failed or was cancelled. You can retry via 'bash $LEAP_DIR/scripts/qmd/qmd-config --repo-root $REPO_ROOT'."
    QMD_FAILED=true
  fi
else
  print_warning "Skipped QMD configuration."
fi

print_step "LEAP Initialization Complete!"
if [ "$QMD_FAILED" = true ]; then
  echo -e "${RED}${BOLD}LEAP Setup Incomplete (Warnings Detected)${NC}"
  echo "  - Please fix the QMD path errors or clean up any broken pre-commit hooks before committing!"
  echo "  - You can retry QMD setup via: bash $LEAP_DIR/scripts/qmd/qmd-config --repo-root $REPO_ROOT"
  exit 1
else
  echo -e "${GREEN}${BOLD}Congratulations! Your project is now fully LEAP-ready.${NC}"
fi

echo "Next steps:"
echo "1. Create your first feature branch: 'git checkout -b <username>/<feature-name>'"
echo "2. Create your feature directory: 'mkdir -p kb/feature/<username>/<feature-name>'"
echo "3. Author your goals.md file in that folder."
echo "4. Activate your AI agent and start building!"
