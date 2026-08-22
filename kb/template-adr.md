# ADR [Number]__[Short Descriptive Name]

**Status:** [proposed | accepted | rejected | deprecated | superseded]<br>
**Deciders:** [Name(s)]<br>
**Date:** [YYYY-MM-DD]

---

## Issue

[Describe the problem or decision that needs to be made. Include:]

### Current State

- [What exists today]
- [Current problems or limitations]
- [Why this decision is needed]

#### Problems with Current Approach

1. **[Problem Category]**: [Description]
2. **[Problem Category]**: [Description]

## Decision

[State the decision clearly and concisely. This is the "what we decided" section.]

### [Decision Title/Summary]

[Detailed description of the decision, including:]

- Key aspects of the approach
- Important conventions or patterns
- Examples demonstrating the decision

## Rationale

[Why this approach was chosen over alternatives. This section explains the reasoning behind the decision.]

- [Key benefit that drove the decision]
- [Important consideration or constraint]
- [Why this approach is better than alternatives]
- [Long-term implications]

## Options Considered

### Option A: [Name]

#### Approach
[Describe this option]

#### Pros

- [Benefit 1]
- [Benefit 2]

#### Cons

- [Drawback 1]
- [Drawback 2]

---

### Option B: [Name]

#### Approach
[Describe this option]

#### Pros

- [Benefit 1]
- [Benefit 2]

#### Cons

- [Drawback 1]
- [Drawback 2]

---

[Add more options as needed]

## Evaluation Criteria

1. **[Criterion 1]**: [What makes this important?]
2. **[Criterion 2]**: [What makes this important?]
3. **[Criterion 3]**: [What makes this important?]

## Comparison Matrix

[Optional: Use a table to compare options against criteria]

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| [Criterion 1] | ✓ |  | ✓ |
| [Criterion 2] |  | ✓ | ✓ |
| [Criterion 3] | ✓ | ✓ |  |

Use ✓ for meets criterion, leave empty for doesn't meet criterion.

---

## Consequences

### Positive

- **[Benefit Category]**: [Description]
- **[Benefit Category]**: [Description]

### Negative

- **[Cost/Tradeoff Category]**: [Description]
- **[Cost/Tradeoff Category]**: [Description]

### Neutral

[Optional: Include neutral consequences if significant]

- **[Observation]**: [Description]

### Migration Strategy

[Optional: If this decision requires migration of existing code/docs/practices. Note: Scope this section to describing the high-level migration strategy rather than tracking task-by-task execution. Active task tracking belongs in feature plans, issues, or pull requests, not inside the immutable ADR.]

#### Phase 1: [Phase Name]

[Description of migration phase]

#### Phase 2: [Phase Name]

[Description of migration phase]

---

## References

[Optional: Links to related ADRs, external resources, discussions]

- ADR [number]: [Brief description]
- [External resource title]: [URL]
- [Discussion/issue reference]

---

## TEMPLATE GUIDANCE (DELETE THIS SECTION IN ACTUAL ADRs)

**Note to ADR Authors:** This section contains guidance for using this template. Delete this entire section when creating an actual ADR.

### ADR Naming Convention

- **Top-level ADRs**: `adr-NNN__description.md` (in `kb/adr/`)
- **Module-specific ADRs**: `<module>-adr-NNN__description.md` (in `<module>/kb/adr/`)
- Use double underscore `__` to separate identifier from description
- See ADR leap-adr-001 for complete naming policy

### ADR Status Workflow

- **proposed**: Decision under consideration
- **accepted**: Decision approved and adopted as official policy. This status represents established architectural policy rather than pending development. Once accepted, the ADR is canonical policy going forward, and there is no need to edit the ADR or add custom tracking fields (such as `**Implemented:**`) to reflect completion state.
- **rejected**: Decision considered but not adopted
- **deprecated**: Decision no longer recommended (but not forbidden)
- **superseded**: Decision replaced by another ADR (reference the new ADR)

#### Approval Authority

- Anyone can create an ADR in **proposed** status
- Promotion to **accepted** status requires Chief Architect approval
- This ensures architectural decisions are reviewed before implementation

### Considering Testability

When architectural decisions affect testing, include testability considerations:

#### Include as Evaluation Criterion

```markdown
## Evaluation Criteria

1. **Testability**: Can this approach be easily tested? Does it enable or hinder test coverage?
```

#### Document in Consequences

```markdown
### Positive
- **Improved Testability**: Repository pattern enables isolated unit tests with mock TypeDB client

### Negative
- **Testing Complexity**: Requires integration tests with real TypeDB instance for full validation
```

#### Examples of decisions with testability implications

- Dependency injection patterns
- API design choices (public interfaces)
- Database access patterns
- Separation of concerns
- Framework and library selections

### Writing Tips

- **Pre-Write Gate**: Before writing, name the alternative you rejected and the reason it lost. If you cannot name a viable alternative, there is no policy decision to record; write an `impl-` or `guide-` document instead.
- **No Living/Implementation Content**: An accepted ADR is an immutable historical record and must not contain implementation details that change over time. The following sections **do not belong** in an ADR and should be placed in an implementation document (`impl-` or `guide-`) instead:
  - *Implementation Details*
  - *Usage*
  - *How to Run*
  - *Common Pitfalls*
  - *Best Practices*
  - *Future Enhancements*
- **Issue section**: Focus on the problem, not the solution
- **Decision section**: State what was decided and why (rationale)
- **Options section**: Show you considered alternatives
- **Consequences section**: Be honest about tradeoffs
- **Consider testability**: When decisions affect testing, make it explicit
- **Use examples**: Concrete examples help readers understand
- **Keep it concise**: ADRs should be scannable and focused
