# <Feature Name> Completion Summary

**Branch:** `<username>/<feature-branch-name>`<br>
**Base Branch:** `<base-branch>`<br>
**Date:** [Date]<br>
**Author:** [Your Name](https://www.linkedin.com/in/your-profile/)

---

## Overview

[What was built and why. Provide context about the feature and its purpose in 1-2 paragraphs.]

## What Changed

### High-Level Summary

[Bullet-point list of major changes:]

- Added feature X
- Modified component Y
- Refactored module Z
- Updated documentation for W

### Detailed Changes

#### Component 1

- Change detail 1
- Change detail 2

#### Component 2

- Change detail 1
- Change detail 2

### New Files

- `path/to/NewFile1.kt` - Description of purpose
- `path/to/NewFile2.kt` - Description of purpose

### Modified Files

- `path/to/ModifiedFile1.kt` - Description of changes
- `path/to/ModifiedFile2.kt` - Description of changes

### Deleted Files

- `path/to/OldFile.kt` - Reason for deletion

## Key Implementation Details

### Technical Decision 1

[Description of important technical decision and rationale]

### Technical Decision 2

[Description of important technical decision and rationale]

### Architecture Changes

[Description of any architectural changes or patterns introduced]

## Testing

### Test Coverage

- **Line Coverage:** X% (target: 90%+)
- **Statement Coverage:** Y% (target: 90%+)
- **Branch Coverage:** Z% (target: 90%+)

### Test Strategy

[Description of testing approach:]

- Unit tests for [components]
- Integration tests for [workflows]
- Performance tests for [critical paths]
- Edge case testing for [scenarios]

### Test Results

- Total tests: XXX
- Passing: XXX
- New tests added: XX

## Documentation

### Structured API Documentation

- [List key public APIs, interfaces, and primary classes documented with KDoc/JSDoc/etc.]
- Example: `QueryBuilder.kt` - Complete KDoc for all public methods and the primary class

### Implementation Documentation

- [List implementation docs created or updated]
- Example: `kb/query-builder-architecture.md` - Architecture and design patterns

### Source Comments

- All public APIs have structured documentation
- Complex algorithms have inline comments explaining approach
- Non-obvious design decisions are documented in code

### Usage Documentation

- [List usage docs created or updated]
- Example: `kb/cli-framework-usage-guide.md` - Complete usage guide for new framework

## Permanent Documentation Assessment

**REQUIRED:** Assess feature documentation for insights that should be preserved permanently before merging/closing this branch.

Feature directories (`kb/feature/<username>/<feature-name>/`) are ephemeral and may be removed as they age. Before completing this feature, evaluate what documentation should be migrated to permanent locations.

### Assessment Questions

Review your feature documentation and ask:

- **Did we learn something valuable** about the technology or domain?
  - If yes → Consider `kb/meta/lessons-<topic>.md`

- **Did we make an architectural decision** that should be recorded?
  - If yes → Create `kb/adr/adr-NNN__description.md` (requires Chief Architect review and approval)

- **Did we discover a best practice** worth sharing?
  - If yes → Update or create `kb/meta/best-practices-<topic>.md` (requires Chief Architect review and approval)

- **Is there technical debt** that needs tracking?
  - If yes → Update or create `kb/meta/tech-debt-<topic>.md`

- **Did we create implementation documentation** that applies beyond this feature?
  - If yes → Migrate to `kb/impl-<topic>.md` or module-specific `<module>/kb/impl-<topic>.md`

### Documentation Preserved

[List permanent documentation created or updated as result of this assessment, or state "None - no insights require permanent preservation"]

#### Example responses

- Created `kb/adr/adr-015__query-builder-architecture.md` documenting decision to use fluent DSL pattern
- Updated `kb/meta/best-practices-kotlin-code.md` with section on builder pattern conventions
- Created `kb/meta/lessons-typedb-performance.md` documenting bulk fetch optimization patterns
- None - feature implementation was straightforward with no novel insights

## Breaking Changes

[List any breaking changes, or state "None"]

### Breaking Change 1

**What changed:** [Description]

**Impact:** [Who/what is affected]

**Migration:** [How to adapt]

## Migration Guide

[Steps for users to adapt to changes. Can be "No action required" if backward compatible.]

### For Users

1. Step 1
2. Step 2

### For Developers

1. Step 1
2. Step 2

## Known Limitations

[Issues deferred or still outstanding]

- Limitation 1: Description and reasoning
- Limitation 2: Description and reasoning

## Future Work

[Features explicitly deferred to future phases]

- Future enhancement 1
- Future enhancement 2

## Performance Impact

[Description of performance characteristics:]

- Baseline performance: [metrics]
- After changes: [metrics]
- Impact: [positive/negative/neutral]

## Related Issues

[References to tickets, discussions, or related work]

- Closes #XXX: [Issue description]
- Addresses #YYY: [Issue description]
- Related to #ZZZ: [Issue description]

## Verification Steps

[Steps reviewers can take to verify the changes work correctly]

1. Checkout the branch: `git checkout <username>/<feature-branch-name>`
2. Build: `./gradlew build`
3. Run tests: `./gradlew test`
4. Verify coverage: `./gradlew koverHtmlReport`
5. Test manually: [specific commands or steps]

## Acknowledgments

[Optional: Thank team members who contributed feedback, reviews, or collaboration]
