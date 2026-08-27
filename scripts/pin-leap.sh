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

# 2. Working tree safeguard
if [ -n "$(git status --porcelain)" ]; then
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

echo -e "${GREEN}Environment and safeguards verified successfully!${NC}"
echo -e "Target pin version set to: ${BOLD}$TARGET_VERSION${NC}"
