#!/usr/bin/env bash
# pin-leap.sh — LEAP Submodule Pinning Utility
#
# Automates updating/pinning a LEAP submodule to a specific release tag, commit, or branch.
#
# Usage:
#   bash leap/scripts/pin-leap.sh [version/tag/commit/branch]
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

print_error() {
  echo -e "  ${RED}✗${NC} ${RED}Error: $1${NC}"
}

# 1. Environment and Git workspace checks
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  print_error "Not a git repository."
  exit 1
fi

CURRENT_DIR="$(pwd)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBMODULE_FULL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Check if running directly inside the LEAP repo itself
if [ "$CURRENT_DIR" = "$SUBMODULE_FULL_DIR" ]; then
  print_error "This script cannot be run directly within the LEAP repository itself."
  echo "It is designed to pin the LEAP submodule inside a consuming parent repository."
  exit 1
fi

# Ensure the parent directory doesn't fully encompass the submodule (meaning we are running inside the submodule folder)
if [[ "$CURRENT_DIR" == "$SUBMODULE_FULL_DIR"* ]]; then
  print_error "This script must be run from the root of the consuming repository."
  echo "Example: bash leap/scripts/pin-leap.sh"
  exit 1
fi

# Determine submodule relative path from parent repo root
SUBMODULE_REL_PATH="${SUBMODULE_FULL_DIR#$CURRENT_DIR/}"

# Verify .gitmodules exists in parent repo root
if [ ! -f ".gitmodules" ]; then
  print_error "No .gitmodules file found in current directory."
  echo "This script must be run from the root of a consuming repository containing a LEAP submodule."
  exit 1
fi

# Verify the submodule directory is registered in .gitmodules
if ! grep -q "path = $SUBMODULE_REL_PATH" ".gitmodules"; then
  print_error "Submodule directory '$SUBMODULE_REL_PATH' is not registered in .gitmodules."
  echo "Please ensure the LEAP submodule is properly initialized and configured."
  exit 1
fi

# 2. Working tree safeguard (ignoring dirty files inside submodules)
if [ -n "$(git status --porcelain --ignore-submodules=dirty)" ]; then
  print_error "Working tree has uncommitted/unstaged changes."
  echo "Please commit, stash, or discard your changes before running this script."
  exit 1
fi

# 3. Input validation & prompt
TARGET_VERSION="${1:-}"

if [ -z "$TARGET_VERSION" ]; then
  echo -n "Enter target LEAP release tag, commit, or branch (e.g. v1.0.0, main, or 'latest'): "
  read -r TARGET_VERSION <&3
fi

if [ -z "$TARGET_VERSION" ]; then
  print_error "Target version/tag cannot be empty."
  exit 1
fi

print_step "Verifying input and resolving version..."

# 4. Resolve 'latest' tag keyword if specified
if [ "$TARGET_VERSION" = "latest" ]; then
  echo "Resolving 'latest' stable tag..."
  
  # Fetch latest tags inside submodule (gracefully ignoring remote failures)
  (cd "$SUBMODULE_REL_PATH" && git fetch --tags &>/dev/null || true)
  
  # Find latest stable semantic version tag in the submodule
  TAGS=$(cd "$SUBMODULE_REL_PATH" && git tag -l "v*" --sort=-v:refname 2>/dev/null || true)
  RESOLVED_TAG=""
  
  for t in $TAGS; do
    # Filter out pre-releases containing a hyphen (-)
    if [[ "$t" != *-* ]]; then
      RESOLVED_TAG="$t"
      break
    fi
  done
  
  # Fallback to the absolute newest tag if no stable tags were found
  if [ -z "$RESOLVED_TAG" ]; then
    RESOLVED_TAG=$(echo "$TAGS" | head -n 1)
  fi
  
  if [ -z "$RESOLVED_TAG" ]; then
    print_error "Could not resolve 'latest' stable tag. No tags matching 'v*' found in submodule."
    exit 1
  fi
  
  TARGET_VERSION="$RESOLVED_TAG"
  print_success "Resolved 'latest' to tag: ${BOLD}$TARGET_VERSION${NC}"
else
  print_success "Target version set to: ${BOLD}$TARGET_VERSION${NC}"
fi

# 5. Create and switch to standard LEAP feature/chore branch
BRANCH_NAME="chore/pin-leap-$TARGET_VERSION"
print_step "Creating branch: $BRANCH_NAME"

if git rev-parse --verify "$BRANCH_NAME" &>/dev/null; then
  print_warning "Branch '$BRANCH_NAME' already exists. Switching to it."
  git checkout "$BRANCH_NAME"
else
  git checkout -b "$BRANCH_NAME"
  print_success "Successfully created and switched to branch: $BRANCH_NAME"
fi

# 6. Checkout specified version inside submodule
print_step "Updating LEAP submodule to: $TARGET_VERSION"

# Fetch latest tags from origin inside the submodule
(cd "$SUBMODULE_REL_PATH" && git fetch --tags &>/dev/null || true)

# Checkout target
if ! (cd "$SUBMODULE_REL_PATH" && git checkout -q "$TARGET_VERSION"); then
  print_error "Failed to checkout '$TARGET_VERSION' in submodule '$SUBMODULE_REL_PATH'."
  echo "Please verify that the tag, commit, or branch exists in the remote repository."
  # Rollback branch creation if possible
  git checkout -
  git branch -d "$BRANCH_NAME" || true
  exit 1
fi
print_success "Checked out '$TARGET_VERSION' in submodule '$SUBMODULE_REL_PATH'."

# 7. Generate LEAP Level 1 Compliance Directory structure
# Dynamically determine clean username for nested compliance directory per LEAP standards
# Prioritized hierarchy: 1. LEAP_USER env var, 2. git config, 3. OS fallback.
RESOLVED_USER="${LEAP_USER:-}"
if [ -z "$RESOLVED_USER" ]; then
  RESOLVED_USER=$(git config --get leap.user || echo "")
fi
if [ -z "$RESOLVED_USER" ]; then
  RESOLVED_USER="${USER:-$(id -un 2>/dev/null || whoami 2>/dev/null || echo "")}"
fi

# Normalize and sanitize the resolved username to match directory naming safety
LEAP_USER=$(echo "$RESOLVED_USER" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9._-]//g')

# Fallback to developer if resolved name is empty after sanitization
if [ -z "$LEAP_USER" ]; then
  LEAP_USER="developer"
fi

COMPLIANCE_DIR="kb/feature/$LEAP_USER/pin-leap-$TARGET_VERSION"
print_step "Generating LEAP Compliance Level 1 documents"

# Dynamically query default base branch of the parent repository (defaulting to main)
BASE_BRANCH=$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@' || echo "")
BASE_BRANCH="${BASE_BRANCH:-main}"

if ! mkdir -p "$COMPLIANCE_DIR"; then
  print_error "Failed to create compliance directory: $COMPLIANCE_DIR"
  exit 1
fi
CURRENT_DATE=$(date "+%Y-%m-%d")

# Define functions to generate the compliance documents.
# This keeps the quoted heredocs safe from command substitution, ensures correct heredoc placement,
# and allows for clean exit status checking.

generate_goals() {
  cat <<'EOF' | sed \
    -e "s|@TARGET_VERSION@|${TARGET_VERSION}|g" \
    -e "s|@CURRENT_DATE@|${CURRENT_DATE}|g" \
    -e "s|@LEAP_USER@|${LEAP_USER}|g" \
    > "$COMPLIANCE_DIR/goals.md"
# Pin LEAP to @TARGET_VERSION@ Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** @CURRENT_DATE@

---

## Quick Summary

Pin the LEAP submodule reference to version @TARGET_VERSION@ to align the repository with the latest standards.

## Executive Summary

To leverage the latest enhancements, bug fixes, and development skills provided by the LEAP repository, this change pins the local LEAP submodule to @TARGET_VERSION@.

## Objectives

1. Update the git submodule reference for LEAP to version @TARGET_VERSION@.
2. Initialize LEAP Compliance Level 1 feature structure to document the pinning procedure.

## Requirements

### Functional Requirements

- REQ-1: Verify that the parent repository's LEAP submodule points to tag or commit @TARGET_VERSION@.
- REQ-2: Ensure the feature directory is created under `kb/feature/@LEAP_USER@/pin-leap-@TARGET_VERSION@`.

### Non-Functional Requirements

- Compatibility: The updated submodule must be fully compatible with local build and validation scripts.

### Testing Requirements

- Run all local validation checks and test suites to confirm that the submodule update does not introduce any regressions.

## Success Criteria

- [x] LEAP submodule is checked out at @TARGET_VERSION@.
- [x] Level 1 Compliance directory `kb/feature/@LEAP_USER@/pin-leap-@TARGET_VERSION@` is created and staged.
EOF
}

generate_completion_summary() {
  cat <<'EOF' | sed \
    -e "s|@TARGET_VERSION@|${TARGET_VERSION}|g" \
    -e "s|@CURRENT_DATE@|${CURRENT_DATE}|g" \
    -e "s|@BASE_BRANCH@|${BASE_BRANCH}|g" \
    -e "s|@SUBMODULE_REL_PATH@|${SUBMODULE_REL_PATH}|g" \
    -e "s|@LEAP_USER@|${LEAP_USER}|g" \
    > "$COMPLIANCE_DIR/completion-summary.md"
# Pin LEAP to @TARGET_VERSION@ Completion Summary

**Branch:** `chore/pin-leap-@TARGET_VERSION@`<br>
**Base Branch:** `@BASE_BRANCH@`<br>
**Date:** @CURRENT_DATE@<br>
**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)

---

## Overview

The LEAP submodule was successfully updated and pinned to version @TARGET_VERSION@. This update aligns our local development skills, linters, and guides with the latest upstream standards.

## What Changed

### High-Level Summary

- Switched the LEAP submodule to the target version @TARGET_VERSION@.
- Auto-generated LEAP Compliance Level 1 documentation for this pinning event.
- Staged all changes for review.

### New Files

- `kb/feature/@LEAP_USER@/pin-leap-@TARGET_VERSION@/goals.md` - Compliance documentation goals.
- `kb/feature/@LEAP_USER@/pin-leap-@TARGET_VERSION@/completion-summary.md` - This completion summary.

### Modified Files

- `@SUBMODULE_REL_PATH@` - Submodule pointer updated to @TARGET_VERSION@.
EOF
}

# Run generation with error checking
if ! generate_goals; then
  print_error "Failed to generate goals.md"
  exit 1
fi

if ! generate_completion_summary; then
  print_error "Failed to generate completion-summary.md"
  exit 1
fi

print_success "Generated goals.md and completion-summary.md under $COMPLIANCE_DIR/"

# 8. Stage submodule pointer change and Level 1 folders
print_step "Staging modifications in parent repository"
git add "$SUBMODULE_REL_PATH"
git add "$COMPLIANCE_DIR"
print_success "Staged submodule reference and compliance folder."

# Output completion message and instructions
echo -e "\n${GREEN}${BOLD}Pinning operation complete!${NC}"
echo "Your LEAP submodule is now pinned to: ${BOLD}$TARGET_VERSION${NC}"
echo "Changes have been successfully staged in your new branch: ${BOLD}$BRANCH_NAME${NC}"
echo ""
echo "To review and commit these changes, run:"
echo "  git commit -m \"chore(deps): pin LEAP submodule to $TARGET_VERSION\""
echo "  git push origin $BRANCH_NAME"
echo ""
