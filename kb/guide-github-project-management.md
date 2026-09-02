# LEAP GitHub Project Management Guide

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-09-01

---

## Overview

Efficient and transparent project management is critical for the open-source LEAP repository. To maintain developer velocity while offering complete visibility to both human contributors and AI coding agents, LEAP adopts a lightweight, highly automated, GitHub-native issue and project management workflow.

This guide outlines the everyday contributor and agent workflows, detailing branch naming conventions, PR processes, the standard label taxonomy, and how items progress through our automated project boards.

---

## The Label Taxonomy

Labels in the LEAP repository are categorized into three orthogonal groups: types, priorities, and community/status. This categorization prevents label bloat and makes it easy to filter and sort issues.

### 1. Issue Types

Issue type labels are colored based on whether they trigger automated releases and version bumps (via `release-please` conventional commit rules). This instantly signals the engineering impact of resolving an issue:

* **Release-Triggering Types** (`#0E8A16` <span style="background-color: #0E8A16; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>): Resolving these issues drives the product forward and triggers a new package version release:
  * **`type: bug`**: An unexpected failure, error, or incorrect behavior in the toolchain or codebase.
  * **`type: feature`**: A significant new capability or system architecture change.
  * **`type: enhancement`**: Minor improvements, optimizations, or performance tuning to existing capabilities.
* **Non-Release-Triggering Types** (`#5F6368` <span style="background-color: #5F6368; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>): Resolving these issues maintains project hygiene and documentation but does not trigger a release:
  * **`type: documentation`**: Updates to guides, knowledge base articles, templates, or ADRs.
  * **`type: chore`**: Routine maintenance tasks, dependency updates, and CI/CD workflow configuration.

### 2. Priority Levels

Priority levels are color-coded based on their severity to let developers instantly identify where to focus their attention.

* **`priority: critical`** (`#D93F0B` <span style="background-color: #D93F0B; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>): Blockers, security vulnerabilities, or major regressions that completely halt work and must be addressed immediately.
* **`priority: high`** (`#FBCA04` <span style="background-color: #FBCA04; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>): Severe bugs, major regressions, or critical feature milestones with high urgency.
* **`priority: normal`** (`#1D4ED8` <span style="background-color: #1D4ED8; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>): Standard planned features, improvements, or non-blocking bug fixes for the current cycle.
* **`priority: low`** (`#8A949E` <span style="background-color: #8A949E; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>): Minor items, speculative enhancements, or non-disruptive feedback.

### 3. Community & Status Labels

Status labels help external contributors find appropriate work and coordinate triage.

* **`good first issue`** (`#7057FF` <span style="background-color: #7057FF; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>): Simple tasks well-suited for first-time contributors.
* **`help wanted`** (`#008672` <span style="background-color: #008672; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>): Tasks seeking community assistance.
* **`needs repro`** (`#D93F0B` <span style="background-color: #D93F0B; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>): Bug reports that lack sufficient steps or details to reproduce locally.
* **`needs info`** (`#FBCA04` <span style="background-color: #FBCA04; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>): Issues awaiting clarification from the original poster.

---

## The Project Board Workflow

The **LEAP Development** project board organizes issues, tasks, and pull requests. Built using native GitHub Project boards, items automatically progress through columns based on standard repository events.

```
┌──────────────┐      ┌───────────┐      ┌───────────────┐      ┌────────────────┐
│ Triage/Inbox ├─────>│  Backlog  ├─────>│ Ready/Up Next ├─────>│  In Progress   │
└──────┬───────┘      └───────────┘      └───────────────┘      └───────┬────────┘
       │                                                                │
       ▼                                                                ▼
┌──────────────┐                                                ┌────────────────┐
│   Ice Box    │                                                │   In Review    │
└──────────────┘                                                └───────┬────────┘
                                                                        │
                                                                        ▼
                                                                ┌────────────────┐
                                                                │      Done      │
                                                                └────────────────┘
```

The board contains the following columns:

1. **Triage / Inbox**: All newly opened issues and discussions are automatically added here. Maintainers review items here to assign correct labels and priorities.
2. **Ice Box**: Valid ideas and feedback that we want to preserve but have no immediate plans to implement.
3. **Backlog**: Accepted issues awaiting scheduling.
4. **Ready / Up Next**: Fully scoped, prioritized issues for the current iteration. These are ready for any contributor or agent to pick up.
5. **In Progress**: Active development. An item automatically moves here when a branch is created or a draft PR is linked.
6. **In Review**: Pull request open and awaiting code review or CI feedback. An item automatically moves here when a linked PR is marked "Ready for review".
7. **Done**: Fully completed work. Merged PRs and resolved issues automatically move here.

---

## Everyday Contributor & Agent Workflows

Both human developers and AI coding agents must align with these standards to ensure frictionless project management.

### 1. Issue Selection

Before writing any code, always ensure there is an active GitHub Issue detailing the task. Checking the project board and coordinating assignments ensures that your contribution aligns with the repository's active goals and prevents duplicate or overlapping effort from other contributors.

*   **Forks & External Contributors**: While anyone can fork the repository and work on any task independently in their own fork (per the general [Contributing Guidelines](CONTRIBUTING.md)), coordinate with the core team to avoid competing pull requests. If you want to tackle an issue (such as a `good first issue` or `help wanted` item), please **comment on the issue** requesting assignment (e.g., *"I'd like to work on this!"*). A maintainer will then assign the issue to you, which automatically moves it on our project board to indicate it is claimed.
*   **Maintainers & Collaborators**: If you have write access to the repository, you can directly **self-assign** any unassigned issue in the **Ready / Up Next** column to claim it before starting work.
*   **Active Work**: Only begin development on items that are actively assigned to you. This keeps the board accurate and helps the community see what is currently being worked on.

### 2. Branch Naming & Directory Conventions

Always adhere to the standard branch naming format:

```
<username>/<feature-name>
```

* **Example**: `faseidl/github-project-management`

All ephemeral feature files (goals, plans, completion summaries, phase documents) must be nested under the correct feature directory:

```
kb/feature/<username>/<feature-name>/
```

### 3. Commit Guidelines

Commits in the LEAP repository trigger automated releases via `release-please`. Therefore, commit prefixes must follow strict rules:

* **Release-Triggering Prefixes**: Only `feat(...)` and `fix(...)` trigger automated releases. Use these *only* for permanent codebase changes (e.g., framework modifications, new CLI rules) or primary deliverables in the `kb/` folder (e.g., templates, guides).
* **Non-Release-Triggering Prefixes**: Use `chore(...)`, `docs(...)`, `refactor(...)`, or `test(...)` for routine tasks.
* **Feature Branch Commits**: Commits editing goals, plans, and completion summaries in the ephemeral `kb/feature/` directory **must never** use `feat` or `fix`. Always use `chore(workflow)` or `docs(workflow)`.

### 4. Pull Requests & Issue Linking

To ensure native GitHub Project automations work perfectly, always link your Pull Requests to their corresponding Issues.

* **Closing Keywords**: In the PR description, use GitHub's supported closing keywords in the format:
  ```
  Closes #<issue_number>
  ```

  * **Example**: `Closes #42`
* **Automated Transit**: Linking the issue ensures that opening a PR automatically transitions the issue to **In Progress** / **In Review**, and merging the PR transitions both the PR and issue to **Done**.
