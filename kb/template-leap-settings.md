# LEAP Settings

**Purpose:** This file defines project-specific LEAP configuration and compliance requirements.

**Location:** `kb/leap-settings.md` (project root) or `<module>/kb/leap-settings.md` (module-specific)

---

## Test Coverage Requirements

**What this defines:** Minimum test coverage thresholds for LEAP Level 1 compliance. These values override the default 50% baseline when higher standards are required.

**How it's used:** Build systems (Gradle, Maven) should enforce these minimums in CI/CD. LEAP Level 1 compliance requires meeting whichever is higher: these thresholds or 50%.

### Configuration

```
Line Coverage:     87%
Instruction Coverage: 84%
Branch Coverage:   57%
```

#### Notes

- These values typically match your build tool configuration (e.g., `koverVerify` in Gradle)
- Update this file when project coverage standards change
- Module-specific settings can override project-wide settings

---

## LEAP Compliance Target

**What this defines:** The LEAP compliance level your project aims to achieve.

**Current Target:** Level 2 (Standard)

**Rationale:** [Explain why this level was chosen for your project]

---

## Project-Specific Conventions

**What this defines:** Project-specific extensions or modifications to LEAP practices.

### Documentation Conventions

[Document any project-specific documentation requirements beyond standard LEAP]

#### Example

- All TypeQL schema files must include schema documentation in `kb/`
- All CLI tools must document usage in `kb/guide-<tool-name>.md`

### Code Documentation Publishing

**What this defines:** Configuration for generated code documentation (Levels 2 & 3).

#### Local Generation (Level 2)

- **Tool:** [Dokka | Javadoc | JSDoc | other]
- **Command:** `./gradlew dokkaHtml` (or equivalent)
- **Output Location:** `build/dokka/html/` (or equivalent)
- **Instructions:** Documented in project README

#### CI Publishing (Level 3)

- **Publishing Trigger:** PRs merged to `[branch-name]`
- **Hosted Location:** `[URL or server path]`
- **Access:** Internal staff only
- **URL documented in:** Project README

#### Exemption

- [ ] This project has no code artifacts and is exempt from code documentation publishing requirements

#### Example for Kotlin project

```
Tool: Dokka
Command: ./gradlew dokkaHtml
Output: build/dokka/html/
CI Publishes to: https://docs.internal.company.com/ghee-app/
```

---

## Module-Specific Overrides

**What this defines:** Modules that have different LEAP requirements than the project default.

| Module | Coverage Requirement | LEAP Level | Rationale |
|--------|---------------------|------------|-----------|
| `<module-name>` | 95% / 92% / 70% | Level 3 | [Why this module has higher standards] |
| `<experimental-module>` | 50% / 50% / 50% | Level 1 | [Why this module has lower standards] |

---

## TEMPLATE GUIDANCE (DELETE THIS SECTION IN ACTUAL SETTINGS FILE)

### When to Create This File

Create `kb/leap-settings.md` when:

- Your project has test coverage requirements above 50%
- You want to document project-specific LEAP practices
- You have module-specific compliance requirements
- You want to formalize your LEAP compliance target

### When NOT to Create This File

Skip this file if:

- Your project uses default 50% coverage for Level 1
- You follow standard LEAP practices without project-specific extensions
- Your project is small and doesn't need formal compliance tracking

### Keeping This File Updated

Update this file when:

- Project coverage standards change
- You adopt a new LEAP compliance level
- New project-specific conventions are established
- Module requirements change

### Example: Minimal Settings File

For a project that just wants to document its coverage requirements:

```markdown
# LEAP Settings

## Test Coverage Requirements

Line Coverage:     87%
Instruction Coverage: 84%
Branch Coverage:   57%

These values match our Gradle `koverVerify` configuration.

## LEAP Compliance Target

Current Target: Level 2 (Standard)
```
