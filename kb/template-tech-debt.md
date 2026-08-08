# Tech Debt: [Topic]

**Author:** [Your Name](https://www.linkedin.com/in/your-profile/)<br>
**Date Created:** [Date]<br>
**Status:** [open | in-progress]<br>
**Last Updated:** [Date]

---

## Summary

[One-sentence description of the technical debt]

## Context

### Why This Exists

[How did we get here? What decisions led to this debt?]

### When It Was Created

[Approximate timeframe, feature, or commit]

### Original Rationale

[If known, why was this approach chosen at the time?]

## The Problem

### What's Wrong

[Clear description of the issue]

### Impact

- **Code Quality**: [How it affects maintainability, readability, etc.]
- **Performance**: [Performance implications, if any]
- **Development Velocity**: [How it slows down development]
- **Risk**: [Potential for bugs, security issues, etc.]

### Affected Components

- `path/to/file1.kt` - [Description]
- `path/to/file2.kt` - [Description]

## Examples

### Current Implementation

```[language]
// Example of the current problematic code
[code]
```

### Issues with Current Approach

- Issue 1
- Issue 2

## Proposed Solution

### Approach

[High-level description of how to fix this]

### Benefits

- Benefit 1
- Benefit 2

### Estimated Effort

[Rough estimate: Small / Medium / Large / Very Large]

### Dependencies

[Any dependencies or prerequisites for fixing this]

## Workarounds

[Temporary solutions or ways to work around the issue while it exists]

## References

### Code Locations

- `path/to/file:line` - [Description]
- TODO comments referencing this doc

### Related Issues

- Issue #XXX
- Related tech debt: `tech-debt-[topic].md`

### Related Decisions

- ADR [adr-NNN] - [Relevant decision]

---

## Notes

### When This Gets Resolved

Move this document to the feature branch directory that resolved it (e.g., `kb/feature/username/feature-name/tech-debt-[topic].md`). The location change indicates resolved status.

### Consider Converting to Idea

If resolution isn't straightforward and suggests new enhancement opportunities, consider creating an `idea-[topic].md` document.
