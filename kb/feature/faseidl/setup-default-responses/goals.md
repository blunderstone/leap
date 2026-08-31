# setup-leap.sh Default Responses Goals

**Author:** [F. Andy Seidl](https://github.com/faseidl)<br>
**Date:** 2026-08-30

---

## Quick Summary

Rethink and update the interactive prompt default responses in `scripts/setup-leap.sh` from "n" to "y" for standard configurations, making first-time setup seamless and easy for users while keeping destructive operations safely defaulting to "n".

## Executive Summary

Currently, `setup-leap.sh` defaults every single prompt to "n" (No). While this is safe, it creates a high-friction user experience for first-time setup where users have to carefully type "y" for every setup step to configure the workspace properly. 

By updating standard setup prompts to default to "y" (Yes), users can seamlessly complete a first-time repository setup by simply pressing Enter through the prompt sequence, while still allowing advanced users to opt-out. Destructive or dangerous operations (such as overwriting existing customized files) will remain defaulting to "n" for safety.

## Objectives

1. Improve the "first-time setup" user experience of `setup-leap.sh` by changing reasonable non-destructive configuration defaults to "y".
2. Maintain strict safety for destructive actions (e.g., file overwrites) by keeping their default response as "n".
3. Ensure automated tests for `setup-leap.sh` are updated to match and verify the new default behaviors.

## Requirements

### Functional Requirements

- REQ-1: Update the default for "Enable automatic Git Submodule updates?" to "y".
- REQ-2: Update the default for check-md installation prompts ("Install check-md globally using 'uv tool'?" and "Install check-md in your active Python environment?") to "y".
- REQ-3: Update the default for AI assistant instructions configuration prompts (CLAUDE.md, GEMINI.md, copilot-instructions.md, .cursorrules) to "y".
- REQ-4: Update the default for "Install LEAP custom skills for your AI agents?" to "y".
- REQ-5: Update the default for "Configure your project's .gitignore for LEAP?" to "y".
- REQ-6: Update the default for "Install LEAP git pre-commit hook?" to "y".
- REQ-7: Update the default for "Run QMD semantic search configurator?" to "y".
- REQ-8: Ensure that "Are you SURE you want to completely overwrite $file_path?" explicitly remains defaulting to "n" for safety.

### Non-Functional Requirements

- Maintainability: Code changes should be clean, readable, and consistent with the shell script's established styling.
- Compatibility: Maintain full compatibility with interactive and non-interactive setup modes (`-y` / `--yes` and `-n` / `--no` flags).

### Testing Requirements

- Verify that all modified prompts behave correctly when pressing Enter (i.e. resolving to their new default values).
- Update and verify that existing test suites (specifically `scripts/tests/test_setup_flags.sh` or similar) do not break, or are updated to align with the new defaults.

### Documentation Requirements

- Document the new setup experience in the pull request description or relevant files if needed.
- Review existing repo documentation (e.g., `README.md`, `kb/`) for mentions of setup prompts or default answers, and update them to reflect the new behavior.

## Success Criteria

- [ ] Interactive prompts for all standard non-destructive workspace configurations in `setup-leap.sh` default to "y".
- [ ] Overwrite prompts explicitly continue to default to "n".
- [ ] Non-interactive modes continue to work correctly under the new default paradigm.
- [ ] Setup script automated tests run and pass cleanly.
- [ ] Documentation audit completed and any affected references updated.

## Constraints

- Bash 3.2+ compatibility (standard for macOS and Linux environments).

## Assumptions

- Users running `setup-leap.sh` generally want to configure LEAP features and AI instructions, so defaulting to Yes for non-destructive actions matches the user's primary intent.

## Out of Scope

- Adding new configuration prompts or features to the setup script.
