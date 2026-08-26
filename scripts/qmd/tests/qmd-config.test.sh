#!/usr/bin/env bash
# qmd-config.test.sh — Behavioral verification for the canonical qmd-config script.
#
# Builds throwaway git repositories with fake remotes and kb/ layouts, runs
# qmd-config --dry-run against each, and asserts the emitted plan. Requires no
# qmd installation and performs no machine-level side effects. Also verifies the
# per-repo wrapper template resolves and targets the outer repository.
#
# Run: bash scripts/qmd/tests/qmd-config.test.sh   (expects PASS=N FAIL=0)
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

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT="$HERE/../qmd-config"
WRAPPER="$HERE/../qmd-config.wrapper"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# Isolate HOME to prevent host-machine environment state (e.g., existing launch agents) from leaking into tests
export HOME="$WORK/fake-home"
mkdir -p "$HOME/Library/LaunchAgents"

PASS=0
FAIL=0

# ---- assertion helpers ------------------------------------------------------

assert_contains() { # label output needle
  if printf '%s\n' "$2" | grep -qF -- "$3"; then
    PASS=$((PASS+1)); printf "  ok   %s\n" "$1"
  else
    FAIL=$((FAIL+1)); printf "  FAIL %s\n       expected to find: %s\n" "$1" "$3"
    printf '       ---- output ----\n%s\n       ----------------\n' "$2"
  fi
}

assert_absent() { # label output needle
  if printf '%s\n' "$2" | grep -qF -- "$3"; then
    FAIL=$((FAIL+1)); printf "  FAIL %s\n       expected NOT to find: %s\n" "$1" "$3"
    printf '       ---- output ----\n%s\n       ----------------\n' "$2"
  else
    PASS=$((PASS+1)); printf "  ok   %s\n" "$1"
  fi
}

# ---- repo builders ----------------------------------------------------------

# make_repo <dirname> [remote-url]
make_repo() {
  local name="$1" remote="${2:-}"
  local repo="$WORK/$name"
  mkdir -p "$repo"
  git -C "$repo" init -q
  [ -n "$remote" ] && git -C "$repo" remote add origin "$remote"
  mkdir -p "$repo/kb/adr" "$repo/kb/feature/u/f" "$repo/kb/meta" "$repo/server/kb/adr"
  : > "$repo/kb/adr/adr-001__x.md"
  : > "$repo/kb/guide-x.md"
  : > "$repo/kb/meta/lessons-x.md"
  : > "$repo/server/kb/adr/adr-001__y.md"
  mkdir -p "$repo/utils/qmd"
  cp "$SCRIPT" "$repo/utils/qmd/qmd-config"
  chmod +x "$repo/utils/qmd/qmd-config"
  printf '%s' "$repo"
}

add_leap_dirs() { # repo
  local repo="$1"
  mkdir -p "$repo/leap/kb" "$repo/leap-extensions/kb"
  : > "$repo/leap/kb/guide-methodology.md"
  : > "$repo/leap-extensions/kb/guide-x.md"
}

# make_shared_repo <dirname> <remote-url>
# Simulates the shared-submodule model: the canonical script lives in a NESTED git
# repo at leap/scripts (reproducing a submodule's detached-HEAD toplevel), and the
# repo carries the thin wrapper template at utils/qmd/qmd-config.
make_shared_repo() {
  local name="$1" remote="$2"
  local repo="$WORK/$name"
  mkdir -p "$repo"
  git -C "$repo" init -q
  git -C "$repo" remote add origin "$remote"
  mkdir -p "$repo/kb/adr"
  : > "$repo/kb/adr/adr-001__x.md"
  : > "$repo/kb/guide-x.md"
  mkdir -p "$repo/leap/scripts/qmd" "$repo/leap/kb"
  git -C "$repo/leap" init -q
  : > "$repo/leap/kb/guide-methodology.md"
  cp "$SCRIPT" "$repo/leap/scripts/qmd/qmd-config"
  chmod +x "$repo/leap/scripts/qmd/qmd-config"
  mkdir -p "$repo/utils/qmd"
  cp "$WRAPPER" "$repo/utils/qmd/qmd-config"
  chmod +x "$repo/utils/qmd/qmd-config"
  printf '%s' "$repo"
}

run() { # repo [args...]
  local repo="$1"; shift
  "$repo/utils/qmd/qmd-config" --dry-run "$@"
}

# ---- Test 1: prefix from https remote --------------------------------------

echo "Test 1: prefix from https remote"
r=$(make_repo webapp-checkout "https://github.com/example-org/webapp.git")
out=$(run "$r")
assert_contains "prefix resolves to webapp" "$out" "PREFIX=webapp"
assert_contains "source is remote" "$out" "PREFIX_SOURCE=remote"
assert_contains "adrs collection prefixed" "$out" "COLLECTION webapp-adrs PATH"
assert_contains "readmes collection prefixed" "$out" "COLLECTION webapp-readmes PATH"
assert_contains "kb mask includes both kb dirs" "$out" "MASK {kb,server/kb}/adr/*.md"

# ---- Test 2: prefix from ssh remote, case-folded ---------------------------

echo "Test 2: prefix from ssh remote (case-folded)"
r=$(make_repo sample-checkout "git@github.com:example-org/Sample-Service.git")
out=$(run "$r")
assert_contains "ssh remote parsed and lowercased" "$out" "PREFIX=sample-service"
assert_contains "source is remote" "$out" "PREFIX_SOURCE=remote"

# ---- Test 3: directory fallback (no remote) --------------------------------

echo "Test 3: directory fallback when no remote"
r=$(make_repo myproject)
out=$(run "$r")
assert_contains "prefix from directory" "$out" "PREFIX=myproject"
assert_contains "source is directory" "$out" "PREFIX_SOURCE=directory"

# ---- Test 4: explicit override + slugify -----------------------------------

echo "Test 4: explicit --prefix override with slugify"
r=$(make_repo whatever "https://github.com/example-org/whatever.git")
out=$(run "$r" --prefix "Foo_Bar Baz")
assert_contains "override slugified" "$out" "PREFIX=foo-bar-baz"
assert_contains "source is override" "$out" "PREFIX_SOURCE=override"

# ---- Test 5: shared-collection ownership (auto) ----------------------------

echo "Test 5a: non-owner skips shared collections (auto)"
r=$(make_repo webapp-shared "https://github.com/example-org/webapp.git")
add_leap_dirs "$r"
out=$(run "$r")
assert_contains "index shared false for non-owner" "$out" "INDEX_SHARED=false"
assert_absent  "no leap collection registered" "$out" "COLLECTION leap PATH"
assert_absent  "leap kb excluded from project mask" "$out" "leap/kb"

echo "Test 5b: owner (commons) registers shared collections (auto)"
r=$(make_repo commons-checkout "https://github.com/example-org/commons.git")
add_leap_dirs "$r"
out=$(run "$r")
assert_contains "index shared true for owner" "$out" "INDEX_SHARED=true"
assert_contains "leap collection registered unprefixed" "$out" "COLLECTION leap PATH"
assert_contains "leap-extensions collection registered" "$out" "COLLECTION leap-extensions PATH"
assert_contains "shared context hint" "$out" "CONTEXT qmd://leap"

# ---- Test 6: shared-collection overrides -----------------------------------

echo "Test 6a: --with-shared forces on for non-owner"
r=$(make_repo webapp-force "https://github.com/example-org/webapp.git")
add_leap_dirs "$r"
out=$(run "$r" --with-shared)
assert_contains "forced index shared true" "$out" "INDEX_SHARED=true"
assert_contains "leap collection registered" "$out" "COLLECTION leap PATH"

echo "Test 6b: --no-shared forces off for owner"
r=$(make_repo commons-force "https://github.com/example-org/commons.git")
add_leap_dirs "$r"
out=$(run "$r" --no-shared)
assert_contains "forced index shared false" "$out" "INDEX_SHARED=false"
assert_absent  "no leap collection" "$out" "COLLECTION leap PATH"

# ---- Test 7: --clean emits removals ----------------------------------------

echo "Test 7: --clean removes project collections first"
r=$(make_repo webapp-clean "https://github.com/example-org/webapp.git")
out=$(run "$r" --clean)
assert_contains "removes prefixed adrs" "$out" "REMOVE webapp-adrs"
assert_contains "removes prefixed readmes" "$out" "REMOVE webapp-readmes"

# ---- Test 7b: --remove-legacy removes unprefixed collections ---------------

echo "Test 7b: --remove-legacy removes unprefixed project collections"
r=$(make_repo legacy-repo "https://github.com/example-org/sample-app.git")
add_leap_dirs "$r"
out=$(run "$r" --remove-legacy)
assert_contains "removes bare adrs" "$out" "REMOVE adrs"
assert_contains "removes bare features" "$out" "REMOVE features"
assert_contains "removes bare readmes" "$out" "REMOVE readmes"
assert_absent  "does NOT remove shared leap" "$out" "REMOVE leap"
assert_contains "still registers prefixed collections" "$out" "COLLECTION sample-app-adrs PATH"

echo "Test 7c: legacy removal is opt-in"
r=$(make_repo legacy-optin "https://github.com/example-org/sample-app.git")
out=$(run "$r")
assert_absent "no legacy removal without the flag" "$out" "REMOVE adrs"

echo "Test 7d: --remove-legacy combines with --clean"
r=$(make_repo legacy-both "https://github.com/example-org/sample-app.git")
out=$(run "$r" --remove-legacy --clean)
assert_contains "removes bare legacy name" "$out" "REMOVE adrs"
assert_contains "removes prefixed name too" "$out" "REMOVE sample-app-adrs"

# ---- Test 8: dry-run performs no side effects ------------------------------

echo "Test 8: dry-run marker present"
r=$(make_repo webapp-dry "https://github.com/example-org/webapp.git")
out=$(run "$r")
assert_contains "dry-run notice" "$out" "(dry-run: no install"

# ---- Test 8b: scheduled refresh decisions ----------------------------------

echo "Test 8b: scheduled refresh defaults on and is platform aware"
r=$(make_repo sched-repo "https://github.com/example-org/sample-app.git")

out=$(QMD_PLATFORM=Darwin run "$r")
assert_contains "macOS resolves to launchd" "$out" "SCHEDULE mechanism=launchd"
assert_contains "installed by default" "$out" "action=install"

out=$(QMD_PLATFORM=Darwin run "$r" --no-schedule)
assert_contains "--no-schedule opts out" "$out" "action=skip"

out=$(QMD_PLATFORM=Darwin run "$r" --remove-schedule)
assert_contains "--remove-schedule removes" "$out" "action=remove"

out=$(QMD_PLATFORM=Linux "$r/utils/qmd/qmd-config" --dry-run)
assert_contains "Linux resolves to cron" "$out" "SCHEDULE mechanism=cron"

out=$(QMD_PLATFORM=Plan9 "$r/utils/qmd/qmd-config" --dry-run)
assert_contains "unknown platform is unsupported" "$out" "mechanism=none action=unsupported"

assert_absent "dry-run installs no launch agent" "$(ls "$HOME/Library/LaunchAgents" 2>/dev/null)" "local.qmd.refresh"

# ---- Test 9: --repo-root targets the given repo ----------------------------

echo "Test 9: --repo-root targets the specified repository"
r=$(make_repo target-repo "https://github.com/example-org/target-repo.git")
out=$("$SCRIPT" --repo-root "$r" --dry-run)
assert_contains "prefix from --repo-root's remote" "$out" "PREFIX=target-repo"
assert_contains "source is remote" "$out" "PREFIX_SOURCE=remote"

# ---- Test 10: shared-model wrapper resolves and targets the outer repo -------

echo "Test 10: wrapper runs shared canonical script against the outer repo"
r=$(make_shared_repo myservice "https://github.com/example-org/myservice.git")
out=$("$r/utils/qmd/qmd-config" --dry-run)
rp="$(cd "$r" && pwd -P)"
assert_contains "wrapper yields outer repo prefix" "$out" "PREFIX=myservice"
assert_contains "source is remote (not submodule)" "$out" "PREFIX_SOURCE=remote"
assert_absent  "prefix is NOT the leap submodule" "$out" "PREFIX=leap"
assert_contains "collections target outer repo root" "$out" "COLLECTION myservice-adrs PATH $rp "

# ---- Test 11: wrapper is fail-safe when canonical is missing ----------------

echo "Test 11: wrapper errors clearly when shared script is absent"
r=$(make_repo no-leap "https://github.com/example-org/no-leap.git")
cp "$WRAPPER" "$r/utils/qmd/qmd-config"; chmod +x "$r/utils/qmd/qmd-config"
set +e
out=$("$r/utils/qmd/qmd-config" --dry-run 2>&1); rc=$?
set -e
assert_contains "nonzero exit when canonical missing" "rc=$rc" "rc=1"
assert_contains "clear not-found message" "$out" "shared qmd-config not found"

# ---- summary ----------------------------------------------------------------

echo ""
echo "PASS=$PASS FAIL=$FAIL"
[ "$FAIL" -eq 0 ]
