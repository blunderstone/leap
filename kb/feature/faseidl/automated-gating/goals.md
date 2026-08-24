# Multi-Tiered Automated Gating Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-08-24

---

## Quick Summary

Implement a multi-tiered automated gating system—comprising a unified checker script, a git pre-commit hook, and cognitive agent constraints—to programmatically prevent AI agents and human developers from committing broken code or bypassing active test/linter failures.

## Executive Summary

While human-in-the-loop gating is the ultimate line of defense in the LEAP methodology, AI agents and developers can still suffer from "explanation/rationalization bias," leading them to propose finalization or commit changes even when active tests or linting suites are failing. This was recently demonstrated when a test failure caused by environmental conditions was rationalized away by an agent, which then pre-emptively offered to transition to feature finalization.

To solve this vulnerability, we propose a multi-tiered automated gating system:

1. **Unified Test Runner:** A single workspace script (`scripts/run-all-checks.sh`) to execute all formatters, linters, unit tests, and script tests, exiting with a non-zero exit code on the first failure.
2. **Git Pre-Commit Hook:** A pre-commit hook automatically installed during workspace setup that executes the unified runner, physically blocking local commits on failures.
3. **Cognitive Zero-Failure Rule:** A strict negative constraint in the `leap-dev` skill that programmatically forbids agents from declaring milestones complete or proposing skill transitions if there are failing checks.

## Risk and Complexity Assessment

**Overall Risk:** LOW

The tools utilized (Git hooks and Bash/Python scripts) are industry-standard, lightweight, and local. They do not introduce external dependencies or remote pipeline risks.

**Overall Complexity:** MEDIUM

The complexity lies in ensuring the setup scripts reliably configure the pre-commit hooks across different shells/environments, and verifying that the hooks block local commits under various failure scenarios without disrupting standard git behavior (such as `--no-verify` or fast non-functional changes).

## Objectives

1. Consolidate all workspace quality and testing checks into a single, authoritative command (`scripts/run-all-checks.sh`).
2. Programmatically enforce project compliance prior to any git commit via a pre-commit git hook.
3. Eliminate explanation/rationalization loopholes for AI agents by implementing a strict negative cognitive constraint.
4. Auto-install and configure the pre-commit hook seamlessly within existing setup scripts.

## Requirements

### Functional Requirements

- **REQ-1 (Unified Runner):** Create `scripts/run-all-checks.sh` which executes `check-md`, pytest suite, python unittest suite, and shell script tests. The runner must abort and exit with a non-zero code on the first failure.
- **REQ-2 (Pre-Commit Hook):** Implement a git pre-commit hook script that triggers the unified runner before any commit is processed, rejecting the commit if the runner exits with a non-zero code.
- **REQ-3 (Setup Automation):** Update `scripts/setup-leap.sh` to automatically install/register the pre-commit hook during environment initialization.
- **REQ-4 (Cognitive Rule):** Update `.skills/leap-dev/SKILL.md` to introduce a strict "Zero-Failure Rule" negative constraint, explicitly prohibiting agents from declaring phases complete, updating checklists, or recommending transitions when any checks are failing.
- **REQ-5 (CI Pipeline Gate):** Create a GitHub Actions workflow (e.g., `.github/workflows/ci.yml`) that automatically executes the unified runner (`scripts/run-all-checks.sh`) on every push to `main` and on all pull requests, ensuring remote enforcement.

### Non-Functional Requirements

- **Execution Speed:** The unified runner must execute within < 3 seconds on a clean workspace to avoid introducing developer friction.
- **Robustness:** The setup logic and hooks must handle paths correctly and work seamlessly on macOS (Darwin) and standard Linux environments.
- **Clear Diagnostics:** The runner and hook must print clean, unambiguous diagnostic messages showing exactly which suite failed.

### Testing Requirements

- **Automated Verification:** Write tests to verify that `run-all-checks.sh` returns exit code 0 when all tests pass, and a non-zero exit code when any check fails.
- **Manual Hook Validation:** Empirically verify that introducing a deliberate failure in a test or markdown file causes a local `git commit` command to be blocked, and that resolving the failure allows the commit to succeed.
- **Linter Self-Check:** Ensure that `check-md` runs clean and successfully passes over all new and modified markdown files.

### Documentation Requirements

- **Usage Documentation:** Document the new unified test runner and the automated pre-commit hook in the repository `README.md` and `GEMINI.md`.
- **Inline Explanations:** Add structured comments inside `run-all-checks.sh` explaining its stages, exits, and output formatting.

## Success Criteria

- [x] Unified check script (`scripts/run-all-checks.sh`) successfully executes check-md, python pytest, python unittest, and shell script tests.
- [ ] Git pre-commit hook is automatically copied or symlinked during `scripts/setup-leap.sh`.
- [ ] Git pre-commit hook successfully blocks local commits when any check fails.
- [ ] Git pre-commit hook permits commits when all checks pass.
- [ ] Strict "Zero-Failure Rule" cognitive constraint is integrated into `.skills/leap-dev/SKILL.md`.
- [ ] GitHub Actions CI workflow is configured and successfully executes the unified runner on every push and PR.
- [ ] Codebase test and linter suites pass completely after all modifications.

## Constraints

- **Compatibility:** Solutions must be compatible with bash, sh, and zsh environments on macOS and Linux.
- **Git Native:** The hook must rely on standard git hook functionality without introducing bulky, third-party pre-commit frameworks.

## Assumptions

- **Environment:** Developers and agents have standard developer tools (Python, Git, Bash) locally installed.
- **Pre-existing Suites:** The existing test directories (`check-md/tests/` and others) contain active tests that the runner can discover and execute.

## Out of Scope

- **Hard Restriction Bypass:** Completely blocking `--no-verify` or other standard git override flags is out of scope; standard git escape hatches remain accessible to human developers.
