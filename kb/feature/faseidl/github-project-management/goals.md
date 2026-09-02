# LEAP GitHub Project Management Goals

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-09-01

---

## Quick Summary

Establish a lightweight, highly automated GitHub-native project and issue management structure for the LEAP repository, enhancing maintainer efficiency and community transparency.

## Executive Summary

As a focused open-source repository with small maintainer loops, LEAP requires project management processes that maximize developer efficiency and minimize manual bookkeeping. This feature introduces a cohesive project management structure that relies on native GitHub automations, structured issue templates, and a clean label taxonomy.

Currently, the repository contains basic, older-style Markdown issue templates (`.github/ISSUE_TEMPLATE/bug-report.md` and `leap-improvement-proposal.md`). We will replace these with modern, interactive GitHub Issue Forms (`.yml`) to standardize user feedback, define a clear label taxonomy, outline the `LEAP Development` project board workflow, and produce a LEAP-compliant usage guide (`kb/guide-github-project-management.md`) documenting these standards.

## Objectives

1. Modernize issue intake by transitioning from Markdown-based issue templates to interactive, structured GitHub Issue Forms (`.yml`).
2. Define a clean, orthogonal label taxonomy (types, priority, and community labels) to categorize work efficiently.
3. Formulate a lightweight workflow and Kanban board strategy using native GitHub Project automations to manage items from triage to release.
4. Author a LEAP-compliant guide (`kb/guide-github-project-management.md`) as part of the permanent knowledge base.

## Requirements

### Functional Requirements

- **REQ-1:** Transition the Bug Report template to a structured GitHub Issue Form (`.github/ISSUE_TEMPLATE/bug-report.yml`) with required fields for environment details (OS, Python version, check-md version), steps to reproduce, and actual/expected behaviors.
- **REQ-2:** Transition the LEAP Improvement Proposal (LIP) to a structured GitHub Issue Form (`.github/ISSUE_TEMPLATE/leap-improvement-proposal.yml`) with fields for context, current state, proposed change, benefits, and drawbacks.
- **REQ-3:** Define a clean label taxonomy including:
  - Issue types (`type: bug`, `type: feature`, `type: enhancement`, `type: documentation`, `type: chore`) with a single consistent color (`#0E8A16`).
  - Priority levels (`priority: critical`, `priority: normal`, `priority: low`) with color-coded severity.
  - Community / status labels (`good first issue`, `help wanted`, `needs repro`, `needs info`).
- **REQ-4:** Align branch naming and pull request conventions strictly with existing LEAP standards:
  - Branch naming must follow the format `<username>/<feature-name>` (e.g., `faseidl/github-project-management`).
  - Ephemeral directories must be nested under `kb/feature/<username>/<feature-name>/`.
  - PR title/descriptions must align with conventional commit standards, and leverage GitHub closing keywords (e.g. `Closes #12`) to automatically move issues upon PR merge.
- **REQ-5:** Establish standard GitHub Project Board Statuses/Columns to manage issues/PRs:
  - **Triage / Inbox:** New issues/discussions submitted by users or maintainers (Auto-add when a new Issue is opened).
  - **Ice Box:** Issues/ideas we want to remember but for which we have no current intention to address.
  - **Backlog:** Accepted issues awaiting prioritization or scheduling.
  - **Ready / Up Next:** Scoped, ready-to-work issues for the current focus cycle.
  - **In Progress:** Actively being developed (Auto-move when branch or draft PR is linked).
  - **In Review:** Pull request open and awaiting review / CI checks (Auto-move when PR is marked 'Ready for review').
  - **Done:** Merged or resolved (Auto-move when PR merges or issue is closed).
- **REQ-6:** Produce a comprehensive, LEAP-compliant guide document (`kb/guide-github-project-management.md`) detailing the project management structure, project board statuses, label configurations, and workflows for everyday contributors and agents.
- **REQ-7:** Produce a separate, LEAP-compliant implementation document (`kb/impl-github-project-management.md`) detailing the one-time manual/CLI setup instructions for repository administrators (such as creating the project board, setting up labels, and enabling automated workflows).

### Non-Functional Requirements

- **LEAP Taxonomy Compliance:** The new documentation must reside in the correct `kb/` directory and follow the prefix-first pattern (`guide-github-project-management.md` and `impl-github-project-management.md`).
- **Date Formatting:** All dates in the goals, plan, and guide documents must strictly use the ISO 8601 standard (`YYYY-MM-DD`).
- **Markdown Consistency:** All written documentation must be fully compatible with LEAP guidelines and parse perfectly through the workspace's linter (`check-md`).
- **YAML Schema Integration:** All YAML files (specifically GitHub Issue Forms) must reference their respective schema (e.g., using `# yaml-language-server: $schema=https://json.schemastore.org/github-issue-forms.json`) so that IDEs like IntelliJ or VS Code can perform automated verification checks.

### Testing Requirements

- **Syntax & Schema Validation:** Verify that all YAML-based issue templates are syntactically valid, reference their SchemaStore schemas correctly, and conform to the GitHub Issue Forms schema.
- **Linter Validation:** Run the `check-md` linter on all written documents (goals, plans, guides) to guarantee zero linter warnings and a high linting score.
- **Manual Verification:** Verify that old templates are removed and the file layout is clean.

### Documentation Requirements

- A permanent, LEAP-compliant guide under `kb/guide-github-project-management.md` explaining the everyday contributor/agent workflow.
- A permanent, LEAP-compliant implementation spec under `kb/impl-github-project-management.md` explaining the administrator-facing setup and automation commands.

## Success Criteria

- [ ] Interactive GitHub Issue Forms for bug reports and proposals created and verified.
- [ ] Old Markdown-based issue templates successfully removed.
- [x] Standardized label taxonomy clearly defined and documented in the guide.
- [x] The permanent guide `kb/guide-github-project-management.md` is authored and integrated into the knowledge base.
- [x] The administrator-facing setup document `kb/impl-github-project-management.md` is authored and integrated into the knowledge base.
- [ ] All new and modified markdown files pass `check-md` checks with no style or semantic violations.

## Constraints

- No changes to the core LEAP framework or `check-md` linter.
- Must be fully compatible with existing release pipelines (`release-please`) and CI configurations.

## Assumptions

- Maintainers have appropriate permissions on the GitHub repository to create labels and configure GitHub Projects.
- GitHub CLI or manual configuration will be used to establish the labels and project boards following the guide.

## Out of Scope

- Implementing automated external syncs to third-party issue trackers (e.g., Jira, Linear).
- Custom repository-specific automation scripts (unless lightweight and helper-only).
