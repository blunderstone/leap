# LEAP GitHub Project Management Implementation Specification

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-09-01

---

## Overview

This implementation specification outlines the one-time manual and GitHub CLI setup steps required for repository administrators to establish the standard project management structure and automated workflows for LEAP.

Administrators must set up:

1. Standard labels with precise colors and descriptions.
2. The `LEAP Development` GitHub Project board.
3. Native GitHub Project automations to transition cards between states.

---

## 1. Label Initialization

To standardize issues, administrators should delete non-standard default labels and create the standardized orthogonal groups of labels.

### Step-by-Step Creation

Run the following GitHub CLI commands to create/configure each label. If a label already exists, the `gh label edit` command can be used instead of `gh label create`.

#### Issue Types

Issue types are styled based on whether they trigger automated releases and version bumps:

* **Release-Triggering** (`#0E8A16` <span style="background-color: #0E8A16; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **Non-Release-Triggering** (`#5F6368` <span style="background-color: #5F6368; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)

```bash
# Delete default labels that do not fit the taxonomy
gh label delete "bug" --yes || true
gh label delete "documentation" --yes || true
gh label delete "enhancement" --yes || true
gh label delete "duplicate" --yes || true
gh label delete "invalid" --yes || true
gh label delete "question" --yes || true
gh label delete "wontfix" --yes || true

# Create the standard issue types
gh label create "type: bug" --color "0E8A16" --description "Unexpected failure, error, or incorrect behavior"
gh label create "type: feature" --color "0E8A16" --description "Significant new capability or system architecture change"
gh label create "type: enhancement" --color "0E8A16" --description "Minor improvement or performance tuning to existing capabilities"
gh label create "type: documentation" --color "5F6368" --description "Updates to guides, knowledge base articles, templates, or ADRs"
gh label create "type: chore" --color "5F6368" --description "Routine maintenance, dependency updates, and workflow configuration"
```

#### Priority Levels

Priority levels use color-coded severity:

* **`priority: critical`** (`#D93F0B` <span style="background-color: #D93F0B; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`priority: high`** (`#FBCA04` <span style="background-color: #FBCA04; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`priority: normal`** (`#1D4ED8` <span style="background-color: #1D4ED8; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`priority: low`** (`#8A949E` <span style="background-color: #8A949E; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)

```bash
# Create priority labels
gh label create "priority: critical" --color "D93F0B" --description "Blockers, vulnerabilities, or major regressions needing immediate fix"
gh label create "priority: high" --color "FBCA04" --description "Severe bugs, major regressions, or critical feature milestones"
gh label create "priority: normal" --color "1D4ED8" --description "Standard planned improvements or non-blocking bug fixes"
gh label create "priority: low" --color "8A949E" --description "Minor items, speculative ideas, or non-disruptive feedback"
```

#### Community & Status Labels

Status labels help external contributors and maintainers coordinate triage:

* **`good first issue`** (`#7057FF` <span style="background-color: #7057FF; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`help wanted`** (`#7057FF` <span style="background-color: #7057FF; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`needs repro`** (`#D93F0B` <span style="background-color: #D93F0B; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`needs info`** (`#FBCA04` <span style="background-color: #FBCA04; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)

```bash
# Create or update standard community labels
gh label create "good first issue" --color "7057FF" --description "Simple tasks well-suited for first-time contributors"
gh label create "help wanted" --color "7057FF" --description "Tasks seeking community assistance"
gh label create "needs repro" --color "D93F0B" --description "Bug reports lacking sufficient details to reproduce locally"
gh label create "needs info" --color "FBCA04" --description "Issues awaiting clarification from the poster"
```

---

## 2. GitHub Project Board Setup

The `LEAP Development` project board must be created at the organization or user level and linked to the repository.

### Step 1: Create the Project

1. Navigate to your GitHub profile or organization -> **Projects** -> **New project**.
2. Select the **Board** template (or a blank board) and name it **LEAP Development**.
3. Go to the project settings, and link it to the `blunderstone/leap` repository.

### Step 2: Configure Fields and Columns

Rename or add the default board columns to match the following taxonomy exactly:

*   **Triage / Inbox** (Status: `Todo`)
*   **Ice Box** (Status: `Ice Box`)
*   **Backlog** (Status: `Backlog`)
*   **Ready / Up Next** (Status: `Ready`)
*   **In Progress** (Status: `In Progress`)
*   **In Review** (Status: `In Review`)
*   **Done** (Status: `Done`)

To set up custom status options:

1. In the Project, click the arrow next to the **Status** field column heading, and click **Field settings**.
2. Add, remove, or rename statuses to align with the list above. Save changes.

---

## 3. Automation Workflows

We leverage GitHub Projects' native workflows to automate card transitions. In the Project Board, navigate to **Workflows** (the lightning bolt icon on the top right) and configure the following rules to align with our active board rules:

### 1. Auto-Add Workflows

*   **Auto-add to project (Active)**:
    *   **Trigger**: Item added to repository (`blunderstone/leap`).
    *   **Condition**: When a new **Issue** or **Pull request** is created.
    *   **Action**: Automatically adds the issue/PR to the project.
*   **Auto-add sub-issues to project (Active)**:
    *   **Trigger**: Checklist item sub-issues are created under a parent issue.
    *   **Action**: Automatically adds parent-linked sub-issues to the project board.

### 2. Status Assignment on Entry

*   **Item added to project (Active)**:
    *   **Trigger**: An issue or pull request is newly added to the project board.
    *   **Action**: Set Status to **Triage / Inbox** (or **Ready / Up Next** depending on project triage preferences).
    *   *Note*: Ensure that newly added PRs are either manually assigned or handled by linked-issue rules to prevent overriding active progress.

### 3. Review Workflows

*   **Pull Request Linked to Issue (Active)**:
    *   **Trigger**: A pull request is linked to an issue.
    *   **Action**: Set Status to **In Review**.
    *   **Rationale**: Configured to move linked items straight to **In Review**, this rule elegantly bypasses native GitHub Projects v2 gaps where directly opened non-draft PRs get stuck or pull cards backwards.
*   **Code review approved (Active)**:
    *   **Trigger**: A pull request gets approved during review.
    *   **Action**: Maintains status in **In Review** or transitions to a custom "Approved" milestone column if configured.
*   **Code changes requested (Active)**:
    *   **Trigger**: Code changes are requested on an open pull request.
    *   **Action**: Set Status back to **In Progress** to signal active work is needed.

### 4. Close & Done Workflows

*   **Pull Request Merged (Active)**:
    *   **Trigger**: Pull Request is merged into the default branch.
    *   **Action**: Set Status to **Done**.
*   **Item Closed (Active)** & **Auto-close issue (Active)**:
    *   **Trigger**: An issue is closed or marked completed in the repository.
    *   **Action**: Automatically sets Status to **Done** for both tracked issue cards and standalone project items.
