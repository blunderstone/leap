# Tech Debt: [Topic]

**Author:** [Your Name](https://www.linkedin.com/in/your-profile/)<br>
**Date Created:** [YYYY-MM-DD]<br>
**Status:** [open | in-progress | done]<br>
**Tracking Issue:** [none | issue reference(s)]<br>
**Last Updated:** [YYYY-MM-DD]

[Status: the leading token must be one of `open`, `in-progress`, or `done`. A short qualifier may follow, separated by an em-dash, a hyphen, or a double hyphen — whichever is easiest to type; the enum token is what carries the meaning. For example `open — partially mitigated by the literal fast path; underlying cause unresolved` or `open - partially mitigated`. Location is authoritative: a document living in `kb/meta/` or `<module>/kb/` is unresolved, and a document that has been moved to the feature directory that resolved it is `done`. If the Status field is absent, infer status from location.]

[Tracking Issue: the issue that owns remediation of this debt, written in the canonical form used by your tracking system (for example a Linear issue ID or a GitHub issue number) and hyperlinked whenever possible; comma-separate the rare case of more than one. Use `none` when no issue has been filed — recording the debt matters more than filing an issue for it, and `none` keeps untracked debt findable for later triage. An issue that merely supplies provenance ("discovered during...", "found while tracing...") is not a tracking issue; list it in the "Related Issues" section of this document instead.]

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

[Context only, never tracking. The work that discovered this debt, adjacent bugs, superseded attempts. The issue that owns remediation belongs in the Tracking Issue header field, not here — an issue listed here carries no ownership, and closing it does not resolve the debt.]

- [Issue reference] - [How it relates]
- Related tech debt: `tech-debt-[topic].md`

### Related Decisions

- ADR [adr-NNN] - [Relevant decision]

---

## Notes

### When This Gets Resolved

Set Status to `done` and move this document to the feature branch directory that resolved it (e.g., `kb/feature/username/feature-name/tech-debt-[topic].md`). Location is authoritative: the move is what marks the debt resolved, and the Status value simply agrees with it. Close the tracking issue, if there is one, at the same time.

### Consider Converting to Idea

If resolution isn't straightforward and suggests new enhancement opportunities, consider creating an `idea-[topic].md` document.
