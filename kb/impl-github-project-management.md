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

All issue types are styled using color `#0E8A16` <span style="background-color: #0E8A16; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span> (dark green).

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
gh label create "type: documentation" --color "0E8A16" --description "Updates to guides, knowledge base articles, templates, or ADRs"
gh label create "type: chore" --color "0E8A16" --description "Routine maintenance, dependency updates, and workflow configuration"
```

#### Priority Levels

Priority levels use color-coded severity:

* **`priority: critical`** (`#D93F0B` <span style="background-color: #D93F0B; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`priority: normal`** (`#FBCA04` <span style="background-color: #FBCA04; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`priority: low`** (`#006B75` <span style="background-color: #006B75; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)

```bash
# Create priority labels
gh label create "priority: critical" --color "D93F0B" --description "Blockers, vulnerabilities, or major regressions needing immediate fix"
gh label create "priority: normal" --color "FBCA04" --description "Standard planned improvements or non-blocking bug fixes"
gh label create "priority: low" --color "006B75" --description "Minor items, speculative ideas, or non-disruptive feedback"
```

#### Community & Status Labels

Status labels help external contributors and maintainers coordinate triage:

* **`good first issue`** (`#7057FF` <span style="background-color: #7057FF; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`help wanted`** (`#008672` <span style="background-color: #008672; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`needs repro`** (`#D93F0B` <span style="background-color: #D93F0B; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)
* **`needs info`** (`#FBCA04` <span style="background-color: #FBCA04; display: inline-block; width: 14px; height: 14px; border: 1px solid #777; vertical-align: middle;"></span>)

```bash
# Create or update standard community labels
gh label create "good first issue" --color "7057FF" --description "Simple tasks well-suited for first-time contributors"
gh label create "help wanted" --color "008672" --description "Tasks seeking community assistance"
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

We leverage GitHub Projects' native workflows to automate card transitions. In the Project Board, navigate to **Workflows** (the lighting bolt icon on the top right) and configure the following rules:

### 1. Auto-Add to Project

*   **Trigger**: Item added to repository (`blunderstone/leap`).
*   **Condition**: When a new **Issue** or **Pull request** is created.
*   **Action**: Add to project and set Status to **Triage / Inbox**.

### 2. Item Closed

*   **Trigger**: Item closed in repository.
*   **Condition**: When an **Issue** is closed.
*   **Action**: Set Status to **Done**.

### 3. Pull Request Merged

*   **Trigger**: Pull Request merged in repository.
*   **Condition**: When a **Pull request** merges.
*   **Action**: Set Status to **Done**.

### 4. Pull Request Opened / Linked

*   **Trigger**: Pull request opened as draft or branch linked.
*   **Condition**: When a linked pull request is opened or a draft PR is created.
*   **Action**: Set Status to **In Progress**.

### 5. Pull Request Ready for Review

*   **Trigger**: Pull request marked "Ready for review".
*   **Condition**: When a pull request transitions from draft to ready for review.
*   **Action**: Set Status to **In Review**.
