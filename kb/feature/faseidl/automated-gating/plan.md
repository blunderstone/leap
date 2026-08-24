# Multi-Tiered Automated Gating Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-24

---

## Overview

This implementation plan outlines the creation and verification of a multi-tiered automated gating system. The goal is to programmatically block broken code from being committed locally or merged remotely, and to prevent AI agents from ignoring test failures.

**Development Approach:** Use Test-Driven Development (TDD) throughout—write tests before implementation code, following the Red-Green-Refactor cycle.

### Overall Assessment

- **Complexity:** MEDIUM - Requires cross-environment compatibility for bash/python scripts, reliable git hook deployment via setup scripts, and GitHub Actions workflow configuration.
- **Risk:** LOW - Changes are localized, backward-compatible, and do not introduce bulky third-party dependencies.

---

## Phase 1: Unified Check Script (`scripts/run-all-checks.sh`)

### Goals

- Consolidate all codebase checkers and tests into a single script.
- Ensure the runner executes fast (<3 seconds when clean) and exits immediately with a non-zero code if any individual check fails.
- Provide clean, legible terminal summaries for the developer.

### Approach

- Implement `scripts/run-all-checks.sh` in standard POSIX-compliant Bash.
- Run the following checks sequentially:
  1. Markdown styling check: `check-md kb/`
  2. Python `check-md` pytest suite: `check-md/.venv/bin/pytest check-md/tests/` (or fallback to global `pytest` if `.venv` is missing)
  3. Skill install tests: `python3 scripts/tests/test_install_skills.py`
  4. QMD config shell tests: `bash scripts/qmd/tests/qmd-config.test.sh`
- Support a fast-fail mode (default) and exit immediately on any sub-step failure.
- Ensure it prints a clear execution report at the end.

### Testing

- Write automated test scenarios (as a unit or integration script) that mock or introduce temporary check failures (e.g., temporary failing tests, invalid markdown files) and assert that `run-all-checks.sh` exits with a non-zero code.
- Verify exit code behavior under a fully passing workspace (expects exit code `0`).

### Success Criteria

- [ ] `scripts/run-all-checks.sh` successfully exits with 0 on a clean workspace.
- [ ] `scripts/run-all-checks.sh` successfully exits with 1 on the first failure of any subcommand.
- [ ] Script is fully executable and documented internally with comments.
- [ ] Tests for the unified script are implemented and passing.

---

## Phase 2: Git Pre-Commit Hook Integration

### Goals

- Establish an automated local gate preventing any git commits when repository checks fail.
- Auto-install and configure the pre-commit hook seamlessly in existing setup scripts.

### Approach

- Create a canonical pre-commit hook template/script at `scripts/git-pre-commit` (or direct within `scripts/`).
- The hook will simply run `./scripts/run-all-checks.sh` and exit with the script's exit code, thus blocking the commit if checks fail.
- Update `scripts/setup-leap.sh` to automatically install this pre-commit hook into the active repository's `.git/hooks/pre-commit` directory and mark it as executable (`chmod +x`).
- Ensure the setup script cleanly handles pre-existing pre-commit hooks (making backups of any custom pre-existing user hooks if present).

### Testing

- Verify setup automation by running `scripts/setup-leap.sh` and ensuring `.git/hooks/pre-commit` is created and correctly linked/written.
- **Empirical Failure Test (RED):** Inject a deliberate linter violation (e.g., in a markdown file), attempt a local git commit, and confirm that the commit is successfully rejected with diagnostic feedback.
- **Empirical Success Test (GREEN):** Resolve the violation, attempt a local git commit, and confirm that the commit completes successfully.

### Success Criteria

- [ ] Pre-commit hook is automatically copied or symlinked during environment setup.
- [ ] Git commit attempt is blocked on check failure, giving immediate feedback.
- [ ] Git commit attempt is permitted to succeed on fully clean checks.
- [ ] Legacy or custom pre-commit hooks are safely preserved/backed up.

---

## Phase 3: Cognitive Zero-Failure Rule & CI Gating

### Goals

- Eliminate AI agent "explanation/rationalization bias" via direct cognitive skill negative constraints.
- Remote-enforce the unified checker utilizing GitHub Actions.

### Approach

- Update `.skills/leap-dev/SKILL.md` under its rules and negative constraints to establish the **"Zero-Failure Rule"**. This rule explicitly and strictly forbids agents from declaring development phases complete, updating progress checklists, or proposing/proceeding with skill transitions (such as `leap-finish` or `leap-handoff`) if there are any active linter or test failures.
- Create a GitHub Actions workflow `.github/workflows/ci.yml` that triggers on all pulls and pushes to `main`. The workflow will execute `scripts/run-all-checks.sh` to enforce remote gating.

### Testing

- Verify that `.skills/leap-dev/SKILL.md` has been updated and passes `check-md`.
- Run `check-md` over the entire `kb/` directory (including the goals, plan, and skills changes) to guarantee perfect linter compliance.
- Commit the changes and verify that the local pre-commit hook runs perfectly.

### Success Criteria

- [ ] Strict "Zero-Failure Rule" cognitive constraint is integrated into `.skills/leap-dev/SKILL.md`.
- [ ] GitHub Actions CI workflow `.github/workflows/ci.yml` is correctly defined and successfully executed.
- [ ] Codebase test and linter suites pass completely after all modifications.
- [ ] Comprehensive validation is performed and check-md is 100% clean across the entire repository.

---

## Risk Mitigation

### Risk 1: Hook Execution Delay / Developer Friction

If the check suite is slow, developers might bypass the hook using `--no-verify`.

#### Mitigation

By utilizing highly targeted and fast test suites (such as pytest for check-md, python unittests, and standard bash scripts), the total check-runner execution remains under 3 seconds, which minimizes development friction.

### Risk 2: Setup Path Portability Issues

Different environments might have varying paths or shell setups, potentially causing the pre-commit hook to fail to find Python or pytest.

#### Mitigation

Implement smart fallback logic in `scripts/run-all-checks.sh` to check for the `.venv` directory, Python versions, or globally available commands. Clearly output friendly setup diagnostic instructions if a dependency is missing.

---

## Decision Points

### After Phase 1

- Proceed if `run-all-checks.sh` successfully aggregates all tests and fails correctly on failures.
- Adjust Python virtual environment detection logic if the script struggles to run pytest cleanly.

### After Phase 2

- Proceed if the pre-commit hook successfully blocks commits on a mock failure.
- Ensure `setup-leap.sh` cleanly permissions the pre-commit file across target developer machines (macOS/Darwin and Linux).

---

## Notes

- All changes are designed to run locally, ensuring compliance is achieved before pushing to a remote repository.
