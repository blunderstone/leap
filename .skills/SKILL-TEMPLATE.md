---
name: sample-skill-name
description: Clear, 1-2 sentence description of what the skill does and when the agent should trigger it.
version: 1.0.0
parameters:

  - name: target_file
    type: string
    description: Path to the file to inspect
    required: true

---

# Skill: Sample Skill Name

## Context & Purpose

Provide high-level framing of the problem domain and architectural intent.

## Trigger Conditions

- Explicit user invocation (e.g., `/sample-skill` or direct prompt).
- Implicit context: agent detects specific patterns in the workspace (e.g., refactoring a module, running migrations).

## Operational Workflow

1. **Analyze:** Inspect the inputs and check workspace prerequisites.
2. **Execute:** Perform the transformation, validation, or generation step.
3. **Verify:** Check results against defined constraints.

## Constraints & Rules

- Rule 1: Always maintain deterministic output.
- Rule 2: Do not modify files outside the explicit scope.

## Output Schema / Format

Specify the exact format, JSON payload structure, or Markdown template the agent should return.
