# Best Practices: Managing AI Agent Sessions with LEAP

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2026-01-13<br>
**Last Updated:** August 23, 2026

---

## Overview

This document provides best practices for managing AI agent session boundaries when working with LEAP (Literate Extended-by-Agent Programming) feature branches. Effective session management reduces token overhead, maintains focus, and leverages LEAP's self-documenting nature.

## Key Insight

**LEAP documentation is self-documenting state.** The combination of `goals.md`, `plan.md`, phase artifacts, and up-to-date success criteria should be sufficient to resume work without preserving implementation details from completed phases.

## Session Compaction vs Clean Sessions

### What is Session Compaction?

When a conversation with an AI assistant (such as Gemini CLI, Claude Code, Cursor, Windsurf, or Aider) approaches its token limit, the system automatically **compacts** (summarizes) the conversation:

- Preserves full conversation history in a condensed summary.
- Resets the token budget to zero (re-allocating fresh tokens).
- Allows seamless continuation without manual intervention.
- The summary, however, includes outdated implementation details, discussions, and iterations from all completed phases.

### Why Clean Sessions Are Better

Starting a **new, clean session** at logical breakpoints is far preferable because:

1. **LEAP docs already capture state**: `goals.md` + `plan.md` + success criteria + phase artifacts = complete picture.
2. **Compaction preserves noise**: Implementation details from completed phases are not needed going forward.
3. **Lower token overhead**: Reading 3-4 LEAP docs (~5-10k tokens) vs processing a long compacted summary (~15k+ tokens of irrelevant details) keeps conversation speeds high.
4. **Focused context**: Only load what's relevant to the next phase.
5. **Clear mental model**: Each session maps to logical, bite-sized work units.

### Example: Why Details Become Noise

#### Phase 1 Complete (ADR creation)

- Compaction preserves: Draft iterations, formatting discussions, and ADR structure debates.
- Clean session needs: Just read the final ADR (`adr-015__cli-output-streams-architecture.md`).

#### Phase 3 Complete (Framework changes)

- Compaction preserves: Function signature discussions, inline comment iterations, and commit message crafting.
- Clean session needs: Read `goals.md` showing Phase 3 [x] complete, and understand that changes were successfully committed.

---

## Best Practices

### 1. Session Boundary = Phase Boundary (Generally)

#### Recommended pattern

- Complete a phase.
- Commit all changes.
- Update success criteria in `goals.md` and `plan.md`.
- **Start a new session for the next phase.**

**Exception:** Multiple simple phases that won't trigger compaction can easily share a single session.

### 2. Starting a New Session

When starting a new session to continue LEAP work:

#### Step 1: Orient yourself

Read the essential LEAP documents to understand the current state:

```bash
# Read these files to understand where we are:
kb/feature/<user>/<feature>/goals.md          # What are we doing?
kb/feature/<user>/<feature>/plan.md           # What's the approach?
kb/feature/<user>/<feature>/<phase-artifact>  # Phase-specific details
```

#### Step 2: Identify next work

- Check success criteria: What's `[x]` complete vs `[ ]` pending?
- Read plan: What's the next phase?
- Read phase-specific artifacts if needed (audit findings, ADRs, etc.).

#### Step 3: Proceed

State your understanding and proceed:

> "I can see from goals.md that Phase 3 is complete (framework changes committed).
> According to plan.md, Phase 4 is correcting CLI tool misuses. The audit findings
> show cobol-tools needs ~15 corrections. Should I start with those?"

### 3. When to Use Compaction (Let It Happen Naturally)

#### Compaction is acceptable when:

- Working through multiple small, related tasks in a single phase.
- In exploratory/research mode where context accumulates.
- Making many small iterations that build on each other.
- You haven't reached a natural breakpoint yet.

**Don't artificially trigger compaction** - if you're approaching the limit, assess whether it's a good time for a clean session break.

### 4. Document Decision Points in LEAP Files

When you make important decisions during a phase, **capture them in LEAP docs**:

- Update `plan.md` with a "Decision Points" section if approaches change.
- Add notes to phase artifacts explaining why specific choices were made.
- Update success criteria as work progresses.

This ensures clean sessions have access to decision context without needing the full conversation history.

---

## Practical Examples

### Example 1: Multi-Phase Feature (Ideal)

#### Session 1: Phases 1-2 (Documentation and Audit)

- Create ADR 015.
- Perform audit of CLI tools.
- Commit ADR + audit findings + updated success criteria.
- **Start new session.**

#### Session 2: Phase 3 (Framework Changes)

- Read `goals.md`, `plan.md`, and audit findings.
- Implement framework changes (rename function, add err=true).
- Commit changes + updated success criteria.
- **Start new session.**

#### Session 3: Phase 4 (Tool Corrections)

- Read `goals.md`, `plan.md`, and audit findings.
- Correct cobol-tools and fileset-manager misuses.
- Commit changes + updated success criteria.
- **Start new session.**

### Example 2: When Compaction Is Fine

#### Session 1: Phase 3 (Multiple small related tasks)

- Rename echoDefault → echoStatus (IDE refactor).
- Add err=true to three functions.
- Update documentation for all functions.
- Run tests and fix any issues.
- Total work: ~2 hours, multiple small commits, natural flow.
- Token usage: ~60k (well under limit).
- **Compaction not triggered, continuation natural.**

### Example 3: When to Force a Clean Break

#### Session 1: Approaching 150k tokens

- Completed Phase 1 (ADR) and Phase 2 (Audit).
- Starting Phase 3, still adding token overhead.
- **Decision point**: Even though Phase 3 could fit, start a new session to avoid compaction mid-phase.

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Continuing Through Compaction

```
Session 1: Phases 1-2 → compacts → Phase 3 → compacts → Phase 4
Result: Multiple compaction summaries, lots of noise
```

#### Better

```
Session 1: Phases 1-2 (commit)
Session 2: Phase 3 (commit)
Session 3: Phase 4 (commit)
```

### ❌ Anti-Pattern 2: Starting New Session Too Frequently

```
Session 1: Create goals.md (commit)
Session 2: Create plan.md (commit)
Session 3: Create ADR (commit)
```

#### Better

```
Session 1: Create goals.md + plan.md + ADR (commit all)
```

### ❌ Anti-Pattern 3: Not Updating Success Criteria

```
Complete Phase 3 → commit code changes → start new session
Result: New session doesn't know Phase 3 is complete
```

#### Better

```
Complete Phase 3 → update success criteria → commit everything → start new session
Result: New session reads [x] complete criteria and knows state
```

---

## Quick Reference

### When to Start a New Session

✅ **Good reasons:**

- Completed a phase (major milestone).
- Approaching token limit (>150k used).
- Switching between unrelated work.
- Taking a break and want clean resumption.

❌ **Poor reasons:**

- Every single commit.
- In the middle of a complex task.
- Before finishing current phase.
- When context is still actively building.

### Pre-Session Checklist

Before starting a new session for LEAP work:

- [ ] All work from previous session committed.
- [ ] Success criteria updated in `goals.md` and `plan.md`.
- [ ] Phase artifacts committed (ADRs, audit findings, etc.).
- [ ] Git status clean (no uncommitted changes).

### Session Start Checklist

When starting a new session:

- [ ] Read `goals.md` (understand objectives and current progress).
- [ ] Read `plan.md` (understand approach and next phase).
- [ ] Read relevant phase artifacts (ADRs, audit findings, etc.).
- [ ] Check git log recent commits (what was just completed).
- [ ] State understanding before proceeding.

---

## Benefits

Following these practices provides:

1. **Lower cognitive load**: Each session starts fresh with minimal context.
2. **Faster startup**: Reading 3-4 LEAP docs vs processing long compaction summary.
3. **Better focus**: Only load context relevant to the current phase.
4. **Natural pacing**: Session boundaries align with logical work units.
5. **Self-documenting progress**: LEAP docs + git history = complete picture.

---

## See Also

- [LEAP Methodology](guide-methodology.md) - Full LEAP methodology documentation
- [Document Taxonomy Guide](guide-document-taxonomy.md) - Document naming and organization
