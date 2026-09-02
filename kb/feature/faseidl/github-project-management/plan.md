# LEAP GitHub Project Management Implementation Plan

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-09-01

---

## Overview

The goal of this implementation is to establish a lightweight, highly automated, and standardized GitHub-native project management structure for the LEAP repository. We will author a permanent, LEAP-compliant guide in the project knowledge base first, then modernize our issue intake forms based on that guide, and finally use the GitHub CLI to verify live repository settings.

Since this change focuses on documentation, repository settings, and configuration forms rather than backend application code, the "TDD" aspect will center on **rigorous automated markdown linting** via our native `check-md` tool, **syntactic and schema validation of YAML files**, and **automated CLI inspection of live repository configurations**.

### Overall Assessment

- **Complexity:** LOW - The tasks involve straightforward document creation, YAML form authoring, template deletion, and CLI verification.
- **Risk:** LOW - No application logic is modified. Standard Git version control allows for immediate rollback of any configuration changes.

---

## Phase 1: Author Permanent Project Management Guide & Implementation Specifications

### Goals

- Write a comprehensive, LEAP-compliant guide document (`kb/guide-github-project-management.md`) for everyday contributors and agents.
- Write a separate, LEAP-compliant implementation setup document (`kb/impl-github-project-management.md`) specifically for repository administrators, outlining the one-time project board and label setup details.

### Approach

- Create `kb/guide-github-project-management.md` conforming to the LEAP prefix-first naming pattern for everyday usage.
- Create `kb/impl-github-project-management.md` conforming to the LEAP prefix-first naming pattern for technical admin setup.
- In `guide-github-project-management.md`, document the project board columns, standardized labels, and daily branch/PR naming workflows.
- In `impl-github-project-management.md`, document the exact steps for creating the `LEAP Development` project board, setting up column rules, configuring custom labels with exact hex values, and enabling GitHub Projects auto-add workflows.

### Testing

- Run the `check-md` linter over all newly created and modified Markdown files (including `plan.md`, the guide, and the implementation setup document) to guarantee zero linter warnings.
- Confirm all dates are in ISO 8601 (`YYYY-MM-DD`) format.

### Success Criteria

- [x] Permanent contributor guide `kb/guide-github-project-management.md` is successfully written.
- [x] Administrator-facing setup document `kb/impl-github-project-management.md` is successfully written.
- [x] Project board statuses, including the **Ice Box**, are fully defined.
- [x] Complete label taxonomy is documented with precise hexadecimal colors and descriptions.
- [x] All markdown files in the repository pass the `check-md` linter with high scores and no violations.

### Explicitly Deferred

- Programmatic execution/creation of the repository boards and labels (which requires specific live GitHub API credentials; detailed manual and CLI instructions are captured in the admin implementation document instead).

**Rationale:** Separating daily contributor workflows from one-time administrative setup instructions ensures high clarity for contributors while giving administrators a clean, focused technical reference guide without cluttering the main guide.

---

## Phase 2: Modernize Issue Intake Forms

### Goals

- Transition the existing static Markdown bug and proposal templates to modern, interactive GitHub Issue Forms (`.yml`).
- Integrate IDE-level schema validation into the YAML files to enable autocompletion and structural checks in IntelliJ and VS Code.
- Clean up the repository by removing the old Markdown issue templates.

### Approach

- Author `.github/ISSUE_TEMPLATE/bug-report.yml` based on the guide's specifications, detailing required text fields, checkboxes, dropdowns, and environment configurations.
- Author `.github/ISSUE_TEMPLATE/leap-improvement-proposal.yml` with structured prompts for context, current state, proposed change, benefits, and drawbacks.
- Include the SchemaStore directive at the top of each YAML file: `# yaml-language-server: $schema=https://json.schemastore.org/github-issue-forms.json`.
- Perform a `git rm` on the obsolete `.github/ISSUE_TEMPLATE/bug-report.md` and `leap-improvement-proposal.md` files.

### Testing

- Verify that both YAML files are syntactically valid and successfully compile.
- Verify that they reference the correct JSON SchemaStore URL.
- Verify that the old templates are completely removed from git.

### Success Criteria

- [x] `.github/ISSUE_TEMPLATE/bug-report.yml` created and verified.
- [x] `.github/ISSUE_TEMPLATE/leap-improvement-proposal.yml` created and verified.
- [x] Obsolete markdown issue templates removed from the workspace.
- [x] Both YAML files start with the correct `# yaml-language-server` schema directive.

### Explicitly Deferred

- None.

**Rationale:** Modernizing issue intake forms ensures that incoming reports from both humans and agents are standardized and contain all the required information to minimize triage overhead.

---

## Phase 3: Live Verification of Repository Settings

### Goals

- Inspect and verify that the live repository settings (labels, boards, issue selection forms) have been successfully configured by the repository administrator according to our documented implementation specifications.

### Approach

- Use the GitHub CLI (`gh`) locally in our shell execution loop to verify that the active label list matches the colors, names, and descriptions defined in `kb/impl-github-project-management.md`.
- Inspect the active project board configuration via CLI queries if available, or confirm that manual configuration is completed and matches.

### Testing

- Execute `gh label list --repo blunderstone/leap` (or the equivalent CLI command) to retrieve active repository labels and programmatically/visually compare them against our label specification.

### Success Criteria

- [ ] Live GitHub repository label configurations fetched and verified via the `gh` CLI.
- [ ] Label names, colors, and descriptions conform 100% to the taxonomy defined in `kb/impl-github-project-management.md`.

### Explicitly Deferred

- Full automation of GitHub Projects custom workflow verification (some automation features are only visible within the GitHub Web UI or require Enterprise token access).

**Rationale:** Adding a dedicated verification phase ensures that the transition from documented specs to live, functioning GitHub configurations is seamless, correct, and completely validated before concluding the feature branch.

---

## Risk Mitigation

### Risk 1: YAML Syntax and Schema Errors

Syntactically invalid YAML issue forms will cause GitHub to reject the files and hide the issue selection forms on the repository.

#### Mitigation

We will utilize local validation/compilation parsing checks and reference the SchemaStore URL directly in the files to let IDEs instantly identify and flag any deviation from GitHub's expected schema.

---

## Decision Points

### After Phase 1

- Proceed to Phase 2 once the permanent guide and implementation specifications are fully documented, all success criteria are met, and the `check-md` linter confirms 100% compliance.

### After Phase 2

- Proceed to Phase 3 once the modern issue forms are verified, old templates are removed, and the repository administrator has completed the initial live settings setup.

### After Phase 3

- Conclude the feature branch once the live settings are fetched and verified to be correct and matching the specs.
