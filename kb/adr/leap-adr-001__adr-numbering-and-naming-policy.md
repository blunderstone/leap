# ADR Numbering and Naming Policy

**Status:** accepted<br>
**Deciders:** F. Andy Seidl<br>
**Date:** 2025-11-07

---

## Issue

How should ADRs be numbered and named to ensure clear referencing, discoverability, and avoid ambiguity across a multi-module project?

### Current State

- ADRs can exist in top-level `kb/adr/` or module-specific `<module>/kb/adr/`
- Numbers are scoped to containing directory (e.g., multiple "001" ADRs exist)
- Some ADRs use numbers, others use descriptive names without numbers
- Gaps exist in numbering sequences

#### Problems with Current Approach

1. **Ambiguity**: Referencing "ADR 001" is unclear - which one?
2. **Cross-reference complexity**: Must use full paths in references
3. **Discoverability**: Must search multiple directories to find ADRs
4. **Inconsistency**: Mixed numbering/naming approaches
5. **Merge conflicts**: Distributed numbering increases collision risk

## Decision

### Adopt Option B: Prefix-Based Numbering with "adr" Keyword and Double-Underscore Separator

#### Naming Convention

- Top-level/cross-cutting ADRs: `adr-NNN__description.md`
- Module-specific ADRs: `<module>-adr-NNN__description.md`
- Double underscore `__` separates identifier from description (following ontology conventions)
- Module prefix is exactly the module name (no ambiguity)

#### Examples

- `kb/adr/adr-010__adr-numbering-policy.md` (this ADR, top-level)
- `cobol-tools-cli/kb/adr/cobol-tools-cli-adr-001__single-cli-architecture.md`
- `meridian/kb/adr/meridian-adr-001__storage-abstraction.md`
- `my-hyphenated-module/kb/adr/my-hyphenated-module-adr-001__some-decision.md` (no ambiguity)

**Module Prefixes** (prefix = exact module directory name):

- Top-level uses `adr-` (no module prefix)
- `cobol-tools-cli-adr-` = cobol-tools-cli module
- `api-server-adr-` = api-server module
- `web-ui-adr-` = web-ui module
- `ontology-adr-` = ontology module
- `meridian-adr-` = meridian module

Prefixes automatically match module directory names. No registry needed. No collisions if module moved to different project.

#### Searchability

- `adr-*` → Finds ALL ADRs (top-level and all modules)
- `cobol-tools-cli-adr-*` → Finds only cobol-tools-cli module ADRs
- `meridian-adr-*` → Finds only Meridian module ADRs
- `*__*` → Alternative pattern to find all ADRs by separator

#### Rationale for Double-Underscore Separator

- Eliminates ambiguity: `my-module-003-adr-001__...` could be parsed multiple ways with `-` separator
- Double underscore `__` provides unambiguous boundary between identifier and description
- Consistent with ontology naming conventions already used in project
- Visually distinct: easy to identify the separation point

#### Referencing ADRs

- Reference format: Use only the identifier portion (before `__`)
  - Example: "See ADR adr-010" or "ADR cobol-tools-cli-adr-001"
  - Not necessary to include description in references
- The description portion serves keyword discovery, not identification
- Both humans and AI agents can find ADRs via keyword searches in filenames

## Options Considered

### Option A: Global Sequential Numbering

#### Approach

- Single number sequence across entire project (001, 002, 003, ...)
- All ADRs in top-level `kb/adr/` directory
- Format: `NNN-descriptive-name.md` (e.g., `010-database-choice.md`)

#### Pros

- Unambiguous references: "ADR 010" is unique
- Simple to understand and implement
- Natural chronological ordering
- Easy discoverability (one location)

#### Cons

- Module-specific decisions in top-level directory feels wrong
- Doesn't scale well if modules become separate repos
- High-level view mixes concerns (top-level architecture with module details)

---

### Option B: Prefix-Based Numbering with "adr" Keyword and Double-Underscore Separator

#### Approach

- Prefix indicates scope with "adr" keyword for discoverability
- Double underscore `__` separates identifier from description (ontology convention)
- Top-level/cross-cutting: `adr-NNN__description.md`
- Module-specific: `<module>-adr-NNN__description.md`
- Can be in top-level `kb/adr/` or module-specific `<module>/kb/adr/` directories
- Examples:
  - `kb/adr/adr-010__database-choice.md` (top-level)
  - `cobol-tools-cli/kb/adr/cobol-tools-cli-adr-001__naming-conventions.md` (module-specific)

#### Pros

- Clear scope in reference: "ADR cobol-tools-cli-adr-001" or "ADR adr-010"
- Excellent searchability: `adr-*` finds all ADRs, `cobol-tools-cli-adr-*` finds specific module ADRs
- Unique identifiers across project
- No ambiguity: `__` clearly separates identifier from description
- Module prefix matches module directory name exactly (no registry needed)
- No collisions if module moved to different project
- Allows module-specific organization
- Better for potential module extraction to separate repos
- Consistent with ontology naming conventions

#### Cons

- Slightly more verbose than pure numbers
- Requires migration of existing ADRs
- Must use `__` separator consistently

---

### Option C: Date-Based Naming

#### Approach

- Use date as primary identifier: `YYYY-MM-DD-descriptive-name.md`
- Can be in top-level or module-specific directories
- Format: `2025-11-07-database-choice.md`

#### Pros

- Natural uniqueness (one ADR per day typically)
- Chronological ordering built-in
- No number collision issues
- Context about when decision made

#### Cons

- Less concise for references: "ADR 2025-11-07-database-choice"
- Multiple ADRs on same day require disambiguation
- Date may not be meaningful for understanding decision
- Doesn't indicate scope

---

### Option D: Hierarchical Numbering with Ranges

#### Approach

- Top-level: 000-099
- Server module: 100-199
- CLI module: 200-299
- UI module: 300-399
- (etc., allocate ranges per module)

#### Pros

- Unique identifiers
- Scope encoded in number range
- Can still use short references: "ADR 105"
- Supports both top-level and module organization

#### Cons

- Need to manage range allocations
- Range exhaustion for active modules
- Not intuitive which range belongs to which module
- Breaks down if module boundaries change

---

### Option E: Hybrid - Location + Local Number

#### Approach

- Keep current directory-scoped numbering
- References must include location: `core:001`, `cli:001`
- Format: `NNN-descriptive-name.md` in respective `kb/adr/` directories

#### Pros

- Minimal change from current approach
- Module-specific ADRs stay with module
- Local numbers easier to manage

#### Cons

- References more complex: "ADR core:001"
- Still requires establishing location shortcuts
- Doesn't solve discoverability
- Ambiguity remains if location omitted

---

## Evaluation Criteria

1. **Unambiguous References**: Can we reference an ADR without confusion?
2. **Discoverability**: Can someone find all ADRs easily?
3. **Maintainability**: How easy to add new ADRs without conflicts?
4. **Scalability**: Works as project grows?
5. **Migration Effort**: How hard to adopt from current state?

## Comparison Matrix

| Criterion | Global | Prefix | Date | Hierarchical | Hybrid |
|-----------|--------|--------|------|--------------|--------|
| Unambiguous | ✓ | ✓ |  | ✓ |  |
| Discoverable | ✓ | ✓ | ✓ | ✓ |  |
| Maintainable | ✓ | ✓ | ✓ | ✓ | ✓ |
| Scalable |  | ✓ | ✓ |  | ✓ |
| Migration | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## Consequences

### Positive

- **Unambiguous References**: Every ADR has unique identifier across project
- **Excellent Discoverability**: `*adr*` pattern finds all ADRs regardless of location
- **Module Clarity**: Prefix immediately indicates scope of decision
- **Future-Proof**: Supports module extraction to separate repositories
- **Searchable by Module**: Can find all CLI decisions with `cli-adr*` pattern
- **Maintains Organization**: ADRs can stay in appropriate module directories
- **Clear Numbering**: Simple sequential numbers within each prefix scope

### Negative

- **Migration Required**: Existing ADRs need renaming
- **Slightly Verbose**: Longer filenames than simple numbers (especially for modules with long names)
- **Module Rename Impact**: Renaming a module requires renaming all its ADRs and updating all references across project
- **Mixed Numbering**: Will have gaps after migration (e.g., adr-001 through adr-009 already exist, next is adr-010)
- **Module-Specific References**: Module ADR references are more verbose (e.g., "cobol-tools-cli-adr-001" vs "ADR 001")

### Migration Strategy

#### Phase 1: High-Priority Migration (Part of leap-1)

Rename existing top-level ADRs to new format:

- `001-kg-repository-pattern.md` → `adr-001__kg-repository-pattern.md`
- `002-query-construction-method-isolation.md` → `adr-002__query-construction-method-isolation.md`
- Continue for all numbered ADRs in `kb/adr/`

Handle unnumbered top-level ADRs:

- Use git history to determine file creation order (maintain chronological numbering)
- Assign next available adr-NNN numbers with `__` separator
- Example: `cli-naming-conventions.md` → `adr-011__cli-naming-conventions.md`
- Preserves chronological order where possible

#### Phase 2: Module-Specific ADRs (Opportunistic)

As we work in each module, rename to new format using full module name:

- `cobol-tools-cli/kb/adr/001-*.md` → `cobol-tools-cli-adr-001__*.md`
- `meridian/kb/adr/002-*.md` → `meridian-adr-001__*.md` (restart numbering per module prefix)
- Update cross-references in documentation

#### Phase 3: Update Cross-References

- Search for references to each specific old ADR name
- Update to new naming format
- Example searches:
  - `git grep "001-kg-repository-pattern"` → update to `adr-001__kg-repository-pattern`
  - `git grep "ADR 001"` → check context and update appropriately

#### Grandfather Clause

Old ADR references remain valid during transition:

- Documentation can refer to "old ADR 001" if context clear
- New documentation must use new format
- Full migration not required immediately - can be incremental

#### Migration Checklist

- [ ] Rename top-level ADRs to use `__` separator (kb/adr/)
- [ ] Assign numbers to unnumbered ADRs using git history for chronological order
- [ ] Create ADR template with new naming guidance and examples
- [ ] Document naming convention in taxonomy guide (no prefix registry needed - use module names)
- [ ] Update cross-references to renamed ADRs in LEAP documents
- [ ] Module-specific ADRs (deferred to Phase 6 or later, use full module names as prefix)

---

## Note: Understanding ADRs vs Other Documentation

### ADRs are fundamentally different from other documentation types.

ADRs document **architectural policy decisions** - binding choices about patterns, technologies, and approaches that establish architectural principles across the project (or even across all projects). They are:

- **Prospective**: Made before significant implementation work begins
- **Prescriptive**: Establish "we will do X" not "we did X"
- **Policy-making**: Create architectural rules and standards
- **Review-driven**: Require architectural review and approval

**Other document types are descriptive**, documenting what exists:

- **Implementation guides** (`impl-`): How the system works internally
- **Usage guides** (`guide-`): How to use features
- **Best practices** (`best-practices-`): Established development patterns
- **Lessons learned** (`lessons-`): Insights from development experience

### Choosing and Remediation Guidance

For comprehensive guidance on distinguishing ADRs from implementation documents (including the four decision questions, the splitting rule, the maintenance rule, and remediation steps for existing documentation), refer directly to the **[Choosing Between an ADR and an Implementation Document](../guide-document-taxonomy.md#choosing-between-an-adr-and-an-implementation-document)** section of the LEAP Document Taxonomy and Naming Guide (`kb/guide-document-taxonomy.md`).

The canonical definition and testing criteria are managed in the taxonomy guide to avoid duplication and definition forking across documents.

### When Retrofitting LEAP Documentation

When documenting an existing codebase, you will commonly extract:

- Implementation guides explaining component architecture
- Usage guides showing how to use existing features
- Best practices documenting established patterns
- Lessons learned capturing development insights

**You will rarely extract ADRs** because existing code represents *implemented decisions*, not the formal architectural policy-making that ADRs document. The code already shows what was chosen; ADRs document *why* a choice was made *before* implementation and establish it as policy.

**Exception**: You may create an ADR to document and ratify an existing architectural pattern as official policy going forward (e.g., "ADR: Adopt Existing Repository Pattern as Standard").
