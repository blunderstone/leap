# LEAP Improvement Proposals

**Purpose:** Guide contributors on how to propose improvements or changes to the LEAP methodology itself.

**Status:** Stable

---

## Proposing Methodology Changes

LEAP is an open-source methodology that evolves based on community experience. All proposals for improving or changing the methodology are tracked and discussed publicly as **GitHub Issues** on the main [blunderstone/leap](https://github.com/blunderstone/leap) repository.

Using GitHub Issues for proposals enables transparent community discussion, easy labeling, clear assignment of responsibility, and direct tracking of implementation progress.

### How to Submit a Proposal

1. Navigate to the [LEAP Issues page](https://github.com/blunderstone/leap/issues) on GitHub.
2. Click **New Issue**.
3. Choose the appropriate issue template:
   - For methodology changes, feature requests, or template enhancements, select the **LEAP Improvement Proposal** template.
   - For checker bugs, formatting defects, or tooling crashes, select the **Bug Report / Defect** template.
4. Fill out the pre-structured sections (such as Context, Current State, Proposed Change, or Reproduction Steps) with as much detail and concrete context as possible.
5. Submit the issue. Maintainers and community members will review, discuss, and track progress directly in the issue thread.

---

## Guidelines for Proposals

To maintain high technical quality and prevent methodology bloat, all proposals should adhere to the following standards before submission.

### Good Proposal Characteristics

- **Direct Pain Point:** Addresses a real friction point encountered during actual codebase development.
- **Concrete Evidence:** Includes specific examples and context from real features or files.
- **Cost-Benefit Conscious:** Considers the implementation cost, complexity, and mental overhead versus the actual gain.
- **Lightweight Design:** Proposes elegant, simple solutions that align with the core LEAP philosophies (such as minimality, explicit composition, and self-enforcing conventions).
- **Honest Trade-offs:** Clearly acknowledges drawbacks and alternatives considered.

### When to Submit a Proposal

- You notice recurring friction or a repeated pattern of confusion in the LEAP workflow.
- You find yourself implementing the exact same workaround across multiple features that should be standardized.
- You identify a critical gap or ambiguity in the existing LEAP guides.

### When NOT to Submit a Proposal

- A one-time, highly specific edge case that is unlikely to occur in other projects.
- A matter of personal, aesthetic coding-style preference without a functional or structural benefit to the workflow.
- A speculative idea that conflicts with LEAP's foundational tenets (e.g., introducing heavy bureaucracy or excessive file duplication).
- A complex solution that is looking for a problem.
