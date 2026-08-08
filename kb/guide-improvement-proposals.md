# LEAP Improvement Proposals

**Purpose:** Capture ideas for improving the LEAP (Literate (Extended-by-Agent) Programming) methodology

**Status:** Living document - add proposals as ideas emerge during development

**Review Process:** Proposals collected here will be reviewed periodically as a separate initiative

---

## How to Use This Document

When working on features, if you identify potential improvements to LEAP methodology:

1. Add a new proposal section below
2. Include date, context, and rationale
3. Mark status as "Proposed"
4. Continue with current work - don't implement immediately
5. Proposals will be reviewed and discussed separately

---

## Proposal Template

```markdown
## [Proposal ID]: [Brief Title]

**Date Proposed:** YYYY-MM-DD

**Proposed By:** [Name]

**Status:** Proposed | Under Review | Accepted | Rejected | Implemented

**Context:** What situation prompted this idea?

**Current State:** How does LEAP work today?

**Proposed Change:** What improvement are you suggesting?

**Benefits:**
- Benefit 1
- Benefit 2

**Drawbacks:**
- Drawback 1
- Drawback 2

**Alternatives Considered:**
- Alternative 1
- Alternative 2

**Implementation Effort:** Low | Medium | High

**Priority:** Low | Medium | High | Critical
```

---

## Active Proposals

### PROP-001: Quick Summary Section in goals.md

**Date Proposed:** 2025-10-22

**Status:** Implemented

**Date Implemented:** 2025-11-07 (Phase 1 of faseidl/leap-1)

**Context:** During feature branch setup for `faseidl/core-ns-deps`, created a README.md to provide quick context when browsing feature directories. User requested deletion to stick strictly to LEAP (goals, plan, completion-summary only). This prompted discussion about LEAP potentially being too lean for quick orientation.

**Current State:** LEAP feature directories contain:

- `goals.md` - Full requirements document (often long and detailed)
- `plan.md` - Implementation plan
- `completion-summary.md` - Post-completion summary

When browsing feature directories, developers must open and read goals.md to understand what the feature does. The executive summary is helpful but comes after frontmatter.

**Proposed Change:** Add an optional "Quick Summary" section at the very top of `goals.md` (before or right after frontmatter):

```markdown
# Feature Name Goals

**Quick Summary:** [2-3 sentence summary of what this feature does and why]

**Author:** [Name]
**Date:** [Date]

---

## Executive Summary
[Full detailed summary...]
```

#### Benefits

- Provides immediate context when browsing feature directories
- Maintains LEAP's single-file principle (no separate README)
- Helps onboarding developers quickly understand feature scope
- Minimal overhead (2-3 sentences)
- Optional - use for complex features, skip for simple ones

#### Drawbacks

- Adds slight redundancy with executive summary
- Might be misused as a substitute for proper executive summary
- Increases template complexity slightly
- Could be seen as unnecessary if executive summary is already concise

#### Alternatives Considered

1. **Separate README.md file**
   - Pros: Clear separation of concerns, standard GitHub convention
   - Cons: Violates LEAP single-file principle, creates redundancy
   - Rejected: User prefers sticking to LEAP structure

2. **Reorganize goals.md frontmatter**
   - Pros: No new section needed
   - Cons: Frontmatter is for metadata, not content
   - Not recommended: Mixes concerns

3. **Use git commit message conventions**
   - Pros: Summary already exists in branch commit messages
   - Cons: Requires looking at git history, not visible in file browser
   - Not sufficient: Need summary visible in directory

4. **Directory naming convention**
   - Pros: No file changes needed
   - Cons: Directory names can't contain enough context
   - Not practical: Names would become too long

**Implementation Effort:** Low

#### Implemented Changes

- ✓ Updated `template-goals.md` with Quick Summary section (Phase 1, faseidl/leap-1)
- ✓ Quick Summary section appears before Executive Summary for quick orientation
- Guidance in best practices documentation (deferred to Phase 2)
- Update existing feature branches (optional, only if they would benefit)

**Priority:** Low

- Not blocking any work
- Quality-of-life improvement
- Can be evaluated alongside other LEAP refinements

---

## Proposal History

*No proposals reviewed yet*

---

## Guidelines for Proposals

### Good Proposal Characteristics

- Addresses real pain point encountered during development
- Includes concrete examples from actual features
- Considers implementation cost and impact
- Proposes lightweight solutions that fit LEAP philosophy
- Acknowledges trade-offs honestly

### When to Add a Proposal

- You notice repeated friction in the LEAP workflow
- You implement a workaround multiple times that should be standardized
- You receive feedback from other developers about LEAP confusion
- You identify missing guidance in LEAP documentation

### When NOT to Add a Proposal

- One-time edge case that isn't representative
- Personal preference without broader benefit
- Idea that conflicts with LEAP core principles
- Solution looking for a problem

---

**Last Updated:** 2025-10-22
