# Best Practices: Test-Driven Development (TDD)

**Author:** [F. Andy Seidl](https://www.linkedin.com/in/faseidl/)<br>
**Date:** 2025-12-15<br>
**Last Updated:** 2026-01-08

---

## Table of Contents

1. [Overview](#overview)
2. [Why TDD is Mandatory](#why-tdd-is-mandatory)
   - [TDD is More Efficient](#tdd-is-more-efficient)
   - [TDD Guides AI Assistants Effectively](#tdd-guides-ai-assistants-effectively)
   - [Tests Codify Requirements](#tests-codify-requirements)
   - [Tests Enable Confident Refactoring](#tests-enable-confident-refactoring)
3. [Test Quality is Critical to TDD Success](#test-quality-is-critical-to-tdd-success)
   - [TDD Effectiveness Depends on Test Quality](#tdd-effectiveness-depends-on-test-quality)
   - [Tests are Executable Specifications](#tests-are-executable-specifications)
   - [High-Quality Tests Have These Characteristics](#high-quality-tests-have-these-characteristics)
   - [Why This Matters for AI-Assisted Development](#why-this-matters-for-ai-assisted-development)
   - [Learn More About Test Quality](#learn-more-about-test-quality)
4. [The TDD Workflow](#the-tdd-workflow)
   - [1. Red: Write a Failing Test](#1-red-write-a-failing-test)
     - [RED Phase: Disciplined Workflow](#red-phase-disciplined-workflow)
     - [Quick Reference: RED Phase Checklist](#quick-reference-red-phase-checklist)
   - [2. Green: Write Minimal Implementation](#2-green-write-minimal-implementation)
   - [3. Refactor: Improve the Code](#3-refactor-improve-the-code)
   - [Repeat the Cycle](#repeat-the-cycle)
5. [Scope: When to Use TDD](#scope-when-to-use-tdd)
   - [Mandatory TDD](#mandatory-tdd)
   - [When TDD May Be Impractical](#when-tdd-may-be-impractical)
6. [TDD for Different Scenarios](#tdd-for-different-scenarios)
   - [New Features](#new-features)
   - [Bug Fixes](#bug-fixes)
   - [Refactoring](#refactoring)
7. [TDD Best Practices](#tdd-best-practices)
   - [Start with the Simplest Test](#start-with-the-simplest-test)
   - [One Assertion Per Test (Usually)](#one-assertion-per-test-usually)
   - [Test Names Describe Behavior](#test-names-describe-behavior)
   - [Keep Tests Fast](#keep-tests-fast)
   - [Tests Should Be Independent](#tests-should-be-independent)
8. [TDD with AI Assistants](#tdd-with-ai-assistants)
   - [Pattern 1: Test-First Dialogue](#pattern-1-test-first-dialogue)
   - [Pattern 2: Bug Fix with Reproduction](#pattern-2-bug-fix-with-reproduction)
   - [Pattern 3: Incremental Feature Building](#pattern-3-incremental-feature-building)
9. [Common TDD Mistakes](#common-tdd-mistakes)
   - [Guessing Instead of Asking](#guessing-instead-of-asking)
   - [Writing Tests After Implementation](#writing-tests-after-implementation)
   - [Writing Too Much Code at Once](#writing-too-much-code-at-once)
   - [Skipping Refactor Step](#skipping-refactor-step)
10. [Summary](#summary)
11. [Related Documents](#related-documents)

---

## Overview

### Standard Practice

Test-Driven Development (TDD) is the standard practice for all new feature development and defect repair in this project.

TDD is a software development approach where you write tests before writing the implementation code. This document explains why TDD is mandatory, how to practice it effectively, and why it's particularly valuable for AI-assisted development.

### Relationship to Other Documents

- See [best-practices-testing.md](best-practices-testing.md) for comprehensive testing standards and patterns
- See [best-practices-kotlin-code.md](best-practices-kotlin-code.md) for Kotlin coding standards
- See [leap-implementation-guide-ghee.md](leap-implementation-guide-ghee.md) for LEAP development workflow

---

## Why TDD is Mandatory

### TDD is More Efficient

**Empirical observation:** Writing tests first is **more efficient** than writing tests after implementation.

When you write tests after the fact:

- You must context-switch back to testing mode
- You must reverse-engineer requirements from implementation
- You're tempted to skip edge cases ("it works, why test more?")
- You write tests that pass trivially (confirming what already works)
- You waste time fixing bugs that TDD would have caught immediately

When you write tests first:

- Tests codify requirements before implementation
- You catch misunderstandings early
- You design better APIs (tests reveal awkward interfaces)
- Implementation is guided by clear success criteria
- Refactoring is safe (tests prevent regressions)

### TDD Guides AI Assistants Effectively

**TDD is especially valuable when working with AI assistants** (like Claude Code, GitHub Copilot, etc.).

AI assistants excel at TDD because:

1. **Tests provide explicit requirements** - No ambiguity about what "correct" means
2. **Immediate feedback** - AI can run tests to verify implementation
3. **Iterative refinement** - Failing tests guide AI toward correct solutions
4. **Edge case discovery** - Writing tests reveals scenarios AI might miss
5. **Prevents hallucination** - Tests catch when AI invents non-existent APIs

#### Example dialogue pattern

**Developer:** "Implement a function that validates email addresses"

**Problem:** Too vague. What's a valid email? What about edge cases?

#### Better with TDD

**Developer:** "Here are the test cases for email validation. Make them pass."

```kotlin
@Test
fun `valid email addresses should pass`() {
    assertTrue(
        validateEmail("user@example.com"),
        "Standard email 'user@example.com' should be valid"
    )
    assertTrue(
        validateEmail("first.last@example.co.uk"),
        "Email with dots and country-code TLD 'first.last@example.co.uk' should be valid"
    )
}

@Test
fun `invalid email addresses should fail`() {
    assertFalse(
        validateEmail("notanemail"),
        "'notanemail' should be invalid (no @ symbol)"
    )
    assertFalse(
        validateEmail("@example.com"),
        "'@example.com' should be invalid (no local part)"
    )
    assertFalse(
        validateEmail("user@"),
        "'user@' should be invalid (no domain)"
    )
}
```

Now AI knows exactly what "correct" means.

### Tests Codify Requirements

Tests are **executable requirements specification**:

- **For new features:** Tests define what "working" means
- **For bug fixes:** Tests reproduce the defect before fixing it
- **For refactoring:** Tests prove behavior hasn't changed
- **For documentation:** Tests show how code should be used

**Tests answer the question:** "How do I know when I'm done?"

### Tests Enable Confident Refactoring

Without tests, refactoring is terrifying:

- Change anything → might break something
- Can't prove behavior preserved
- Manual testing is incomplete and tedious

With TDD test suite:

- Refactor freely → tests catch regressions immediately
- Prove behavior preserved by passing tests
- Automated validation in seconds

**This enables continuous code improvement** without fear of breaking existing functionality.

---

## Test Quality is Critical to TDD Success

### TDD Effectiveness Depends on Test Quality

**TDD is only as effective as the quality of your tests.** Writing tests first doesn't automatically lead to better code—writing *high-quality* tests first does.

#### Poor tests lead to poor implementations

```kotlin
// ❌ BAD: Vague test provides vague requirements
@Test
fun `discount works`() {
    val result = calculateDiscount(customer, 100.0)
    assertTrue(result < 100.0)  // Passes for ANY discount!
}

// Implementation guided by vague test → unclear requirements → bugs
fun calculateDiscount(customer: Customer, price: Double): Double {
    return price * 0.5  // 50% discount? Is this right? Test passes...
}
```

#### High-quality tests lead to correct implementations

```kotlin
// ✅ GOOD: Precise test provides precise requirements
@Test
fun `regular customers get 10 percent discount`() {
    val customer = Customer(type = CustomerType.REGULAR)
    val result = calculateDiscount(customer, 100.0)

    assertEquals(
        90.0,
        result,
        0.01,
        "Regular customer should get 10% discount: expected $90.00 but got $${result}"
    )
}

// Implementation guided by precise test → clear requirements → correct code
fun calculateDiscount(customer: Customer, price: Double): Double {
    val discountRate = when (customer.type) {
        CustomerType.REGULAR -> 0.10  // Exactly 10% as specified
        else -> 0.0
    }
    return price * (1.0 - discountRate)
}
```

### Tests are Executable Specifications

When you write tests first, **tests become your specification**. They define:

- **What** the code should do (exact behavior)
- **How** to know it's correct (success criteria)
- **Why** edge cases matter (documented in test names and assertions)

**Poor specifications → Poor implementations.** Your tests must be as precise and clear as you want your code to be.

### High-Quality Tests Have These Characteristics

1. **Descriptive assertion messages** - Provide context that assertions don't show automatically
   ```kotlin
   // ❌ BAD: No context when assertion fails
   assertEquals(expected, actual)

   // ❌ BAD: Restates what assertEquals already shows
   assertEquals(
       expected,
       actual,
       "Expected: '$expected', Actual: '$actual'"
   )

   // ✅ GOOD: Provides context about which query and why
   assertEquals(
       expected,
       actual,
       "Match query for single variable should use simplified format (no commas)"
   )
   ```

2. **Exact verification** - Use `assertEquals()` with precise expected values, not vague `contains()` checks
   ```kotlin
   // ❌ BAD: Vague - could pass for wrong output
   assertTrue(result.contains("important_part"))

   // ✅ GOOD: Exact - only passes for correct output
   val expected = "complete exact expected output"
   assertEquals(expected, result)
   ```

3. **Self-documenting** - Test name and assertions clearly explain the requirement
   ```kotlin
   // ✅ GOOD: Anyone can understand what this tests
   @Test
   fun `expired coupons should be rejected with helpful error message`() {
       val expiredCoupon = Coupon(code = "SAVE10", expiryDate = yesterday())

       val result = applyCoupon(expiredCoupon)

       assertFalse(
           result.isSuccess,
           "Expired coupon should be rejected"
       )
       assertEquals(
           "Coupon 'SAVE10' expired on ${yesterday()}",
           result.errorMessage,
           "Error message should show coupon code and expiry date"
       )
   }
   ```

4. **Focused on one behavior** - Each test verifies one specific thing
5. **Independent** - Can run in any order without dependencies

### Why This Matters for AI-Assisted Development

**AI assistants implement to the specification you provide.** When using TDD with AI:

- **High-quality tests** → AI understands exactly what to build → correct implementation
- **Poor-quality tests** → AI guesses at requirements → incorrect or incomplete implementation

The tests are the AI's instructions. Make them clear, precise, and complete.

### Learn More About Test Quality

This document focuses on the TDD workflow. For comprehensive guidance on writing high-quality tests, see:

- **[best-practices-testing.md](best-practices-testing.md)** - Complete testing standards including assertion patterns, exact verification strategies, and common pitfalls to avoid

**Required reading:** Every developer practicing TDD must understand the test quality standards in best-practices-testing.md.

---

## The TDD Workflow

TDD follows a simple three-step cycle: **Red → Green → Refactor**

### 1. Red: Write a Failing Test

Start by writing a test for the next small piece of functionality. The test must fail because the functionality doesn't exist yet.

#### CRITICAL: Proper TDD RED Phase

**TDD RED means:** Tests COMPILE and RUN but FAIL on assertions.

**Not TDD RED:** Tests that fail with compilation errors.

#### RED Phase: Disciplined Workflow

The RED phase requires discipline and checkpoints to ensure tests are high-quality specifications. Follow these steps **before moving to implementation**:

##### Step 1: Ensure Tests Compile

Write the test and add stubs so it compiles:

```kotlin
// Write the test
@Test
fun `calculateDiscount should return 10 percent off for regular customers`() {
    val customer = Customer(type = CustomerType.REGULAR)
    val result = calculateDiscount(customer, 100.0)
    assertEquals(90.0, result, 0.01)
}

// Add stub so it compiles
fun calculateDiscount(customer: Customer, price: Double): Double {
    TODO("Not yet implemented")
}
```

**Checkpoint:** Tests must compile before proceeding.

##### Step 2: Ensure Tests Follow best-practices-testing.md

Review tests against [best-practices-testing.md](best-practices-testing.md):

- ✅ Descriptive assertion messages providing context
- ✅ Exact verification using `assertEquals()` with precise expected values
- ✅ Self-documenting test names
- ✅ One behavior per test
- ✅ Independent tests (no dependencies on other tests)
- ✅ Proper use of test framework features (`@TempDir`, base class cleanup, etc.)
- ✅ Following project-specific patterns (QueryBuilder DSL, etc.)

**Checkpoint:** Tests must meet quality standards before proceeding.

##### Step 3: Pause for Code Review and Refinement

**Do not rush past this step.** Review the tests critically:

- Do assertions clearly express requirements?
- Are expected values precise and complete?
- Do test names accurately describe behavior?
- **Are there any assumptions or guesses?**
- Does the test verify exactly what should happen?

Refine tests based on review. This is when you catch vague assertions, weak test names, and missing edge cases.

#### CRITICAL: Never Guess About Requirements

#### If you don't know something and can't easily find the answer, ASK.

- ❌ **Don't guess** what the output format should be
- ❌ **Don't assume** edge case behavior
- ❌ **Don't infer** requirements from incomplete information
- ❌ **Don't write defensive code** for unknown scenarios

✅ **Do ask specific questions:**

- "What should the output format be for select queries?"
- "How should the system handle null values?"
- "What's the expected behavior when the list is empty?"

**For AI Assistants:** This is especially critical. When you find yourself writing code like:

- `// I think this might need...`
- `// Probably should handle...`
- `// Guessing that the format is...`

**STOP.** Ask the question instead. Guessing wastes time and creates incorrect tests.

**Checkpoint:** Tests must be reviewed and refined before running. No guesses or assumptions allowed.

##### Step 4: Run Tests and Review Results

Run the tests and verify they fail **appropriately** for TDD RED:

```bash
./gradlew test --tests "MyFeatureTest"
```

#### Expected RED phase failures

- ✅ `NotImplementedError` from `TODO()` stubs
- ✅ Assertion failures from wrong/missing behavior
- ✅ Clear failure messages showing what's expected vs actual

#### Not acceptable RED phase failures

- ❌ Compilation errors
- ❌ Null pointer exceptions from missing setup
- ❌ Unclear failure messages

Review test output:

- Do failures clearly show what's missing?
- Are failure messages helpful for implementation?
- Do failures validate that tests are checking the right things?

**Checkpoint:** Tests must fail appropriately before committing.

##### Step 5: Commit the Tests (Baseline)

Once tests compile, meet quality standards, and fail appropriately:

```bash
git add <test files>
git commit -m "test: add TDD RED tests for feature X

Tests define requirements for:
- Behavior 1
- Behavior 2
- Edge case handling

All tests currently fail appropriately (TODO/NotImplementedError).
Ready for implementation phase."
```

#### Why commit tests before implementation

- **Baseline:** Clear record of tests before implementation
- **Stability:** Ideally, tests won't need changes during implementation
- **Audit trail:** Shows how tests evolve (should be minimal)
- **Clarity:** Separates "define requirements" from "implement requirements"

**If tests need changes during implementation**, it usually means:

- Requirements weren't fully understood (refine tests)
- Tests had bugs (fix and commit separately)
- Requirements changed (document why)

**Checkpoint:** Tests committed as baseline before implementation.

##### Step 6: Proceed to Implementation (GREEN Phase)

Now implement code to make tests pass. Tests are the specification—implement exactly what they require, no more, no less.

If you find yourself thinking "I need to change the test," stop and ask:

- Did I misunderstand the requirements? (Discuss with team)
- Is there a bug in the test? (Fix test, commit separately)
- Are requirements changing? (Document decision)

**Goal:** Tests from RED phase should rarely need changes during GREEN phase.

#### Quick Reference: RED Phase Checklist

- ✅ **Step 1:** Tests compile (with `TODO()` stubs)
- ✅ **Step 2:** Tests follow best-practices-testing.md
- ✅ **Step 3:** Tests reviewed and refined
- ✅ **Step 4:** Tests run and fail appropriately
- ✅ **Step 5:** Tests committed as baseline
- ✅ **Step 6:** Ready for implementation

**Remember:** ❌ **Not TDD RED:** Compilation errors | ✓ **Proper TDD RED:** Compiles, runs, fails on assertions

### 2. Green: Write Minimal Implementation

Write just enough code to make the test pass. Don't worry about elegance yet.

```kotlin
fun calculateDiscount(customer: Customer, price: Double): Double {
    return when (customer.type) {
        CustomerType.REGULAR -> price * 0.9
        else -> price
    }
}
```

**Run the test.** It should pass.

#### Why minimal implementation

- Proves you're not over-engineering
- Keeps focus on current requirement
- Makes next test guide you toward better design

### 3. Refactor: Improve the Code

Now that tests pass, improve the code without changing behavior.

```kotlin
fun calculateDiscount(customer: Customer, price: Double): Double {
    val discountRate = when (customer.type) {
        CustomerType.REGULAR -> 0.10
        CustomerType.PREMIUM -> 0.20
        CustomerType.VIP -> 0.30
        else -> 0.0
    }
    return price * (1.0 - discountRate)
}
```

**Run tests again.** They should still pass.

#### Why refactor

- Eliminate duplication
- Improve names and structure
- Extract reusable code
- Tests protect against breaking changes

### Repeat the Cycle

Continue Red → Green → Refactor for each new requirement:

1. Add test for next small feature
2. Make it pass with minimal code
3. Refactor to improve design
4. Repeat

**Key principle:** Take **small steps**. Don't try to implement everything at once.

---

## Scope: When to Use TDD

### Mandatory TDD

You **must** use TDD for:

#### 1. All New Feature Development

When implementing new functionality:

- Start with tests defining expected behavior
- Implement features to make tests pass
- Refactor with confidence

#### 2. All Defect Repair

When fixing bugs:

- **First:** Write test that reproduces the bug (test fails)
- **Then:** Fix the bug (test passes)
- **Finally:** Refactor if needed

#### This ensures

- Bug is truly fixed (test proves it)
- Bug stays fixed (regression test prevents recurrence)
- Root cause is understood (reproducing bug requires understanding it)

### When TDD May Be Impractical

TDD may be challenging for:

- **Exploratory prototypes** - When you don't know what you're building yet
- **Legacy code** - Hard to test until refactored (see Michael Feathers' "Working Effectively with Legacy Code")
- **External dependencies** - Requires test doubles or integration test infrastructure

**Even in these cases**, write tests as soon as practical. The longer you wait, the harder testing becomes.

---

## TDD for Different Scenarios

### New Features

```kotlin
// 1. RED: Write failing test
@Test
fun `user can search products by name`() {
    val products = listOf(
        Product("Laptop", 999.99),
        Product("Mouse", 29.99)
    )
    val repository = ProductRepository(products)

    val results = repository.searchByName("Laptop")

    assertEquals(
        1,
        results.size,
        "Search for 'Laptop' should return exactly 1 result but got ${results.size}"
    )
    assertEquals(
        "Laptop",
        results[0].name,
        "First result should be 'Laptop' but was '${results[0].name}'"
    )
}

// 2. GREEN: Implement minimal solution
class ProductRepository(private val products: List<Product>) {
    fun searchByName(query: String): List<Product> {
        return products.filter { it.name.contains(query, ignoreCase = true) }
    }
}

// 3. REFACTOR: Add more cases, improve implementation
```

### Bug Fixes

```kotlin
// Bug report: "Discount calculation fails for zero-price items"

// 1. RED: Write test that reproduces bug
@Test
fun `calculateDiscount should handle zero price without error`() {
    val customer = Customer(type = CustomerType.REGULAR)

    val result = calculateDiscount(customer, 0.0)

    assertEquals(
        0.0,
        result,
        0.01,
        "Zero-price item should return 0.0 without error but got $result"
    )
}

// Test fails with: ArithmeticException: Division by zero

// 2. GREEN: Fix the bug
fun calculateDiscount(customer: Customer, price: Double): Double {
    if (price <= 0.0) return 0.0  // Handle edge case
    val discountRate = getDiscountRate(customer)
    return price * (1.0 - discountRate)
}

// Test now passes

// 3. REFACTOR: Extract edge case handling if needed
```

### Refactoring

```kotlin
// Before refactoring: Ensure comprehensive test coverage
@Test
fun `calculateTotal includes all line items`() { /* ... */ }

@Test
fun `calculateTotal applies discount correctly`() { /* ... */ }

@Test
fun `calculateTotal handles empty cart`() { /* ... */ }

// Refactor with confidence
// Tests will catch if behavior changes
```

---

## TDD Best Practices

### Start with the Simplest Test

Don't try to test everything at once. Start with the most basic case:

```kotlin
// ✅ Good: Simplest case first
@Test
fun `empty list returns empty result`() {
    val result = processItems(emptyList())
    assertTrue(
        result.isEmpty(),
        "Processing empty list should return empty result but got ${result.size} items"
    )
}

// ❌ Too complex to start
@Test
fun `handles complex nested structures with error conditions`() {
    // Save this for later
}
```

### One Assertion Per Test (Usually)

Tests are clearer when focused on one thing:

```kotlin
// ✅ Good: Single concern
@Test
fun `valid user can login`() {
    val result = authenticate("user", "password")
    assertTrue(
        result.isSuccess,
        "Valid credentials should authenticate successfully but got: ${result.errorMessage}"
    )
}

@Test
fun `authenticated user has correct role`() {
    val result = authenticate("admin", "password")
    assertEquals(
        Role.ADMIN,
        result.user?.role,
        "Admin user should have ADMIN role but got: ${result.user?.role}"
    )
}

// ❌ Testing multiple things
@Test
fun `authentication works correctly`() {
    val result = authenticate("user", "password")
    assertTrue(result.isSuccess)
    assertEquals("user", result.user?.username)
    assertNotNull(result.token, "Authentication should return a token")
    // What failed if this test breaks? Multiple things tested = unclear failures
}
```

### Test Names Describe Behavior

Use descriptive test names that explain what should happen:

```kotlin
// ✅ Good: Describes behavior
@Test
fun `discount applies only to items marked as eligible`() { }

@Test
fun `expired coupons are rejected`() { }

// ❌ Bad: Unclear what's being tested
@Test
fun `testDiscount()`() { }

@Test
fun `test2()`() { }
```

### Keep Tests Fast

Slow tests discourage running them frequently:

- Use test doubles (mocks, stubs) for external dependencies
- Avoid actual database/network calls in unit tests
- Save integration tests for separate test suite

**Goal:** Unit tests should run in seconds, not minutes.

### Tests Should Be Independent

Each test should:

- Set up its own data
- Not depend on other tests
- Clean up after itself (or use framework support like `@TempDir`)

```kotlin
// ✅ Good: Self-contained
@Test
fun `user can create account`() {
    val service = UserService()  // Fresh instance
    val user = service.createUser("newuser")
    assertNotNull(
        user.id,
        "Created user should have an ID assigned but was null"
    )
}

// ❌ Bad: Depends on previous test
@Test
fun `user can login`() {
    // Assumes account was created in previous test
    authenticate("newuser", "password")  // Might fail if run independently
}
```

---

## TDD with AI Assistants

**Important:** When working with AI assistants, follow the [RED Phase: Disciplined Workflow](#red-phase-disciplined-workflow) rigorously. AI assistants benefit from explicit checkpoints and clear specifications.

### AI Assistant Golden Rule: Never Guess

**AI assistants must ask questions when requirements are unclear.** Do not:

- Guess at output formats
- Assume edge case behavior
- Infer requirements from partial information
- Write defensive code for unknown scenarios
- Make assumptions about what "probably" should happen

#### Instead, ask specific questions

```
❌ Bad AI behavior:
"I'll implement this with defensive checks for various formats..."
[Writes complex code handling multiple assumed scenarios]

✅ Good AI behavior:
"I don't know the expected output format for select queries.
Should I:
A) Use the existing ResultFormatter output?
B) Return raw JSON?
C) Something else?

Can you show me an example of the expected output?"
```

#### Why this matters

- Wrong assumptions → wrong tests → wrong implementation → wasted time
- Asking takes 30 seconds, fixing wrong assumptions takes 30 minutes
- Tests are specifications - they must be precise, not guesses

### Pattern 1: Test-First Dialogue

```
You: I need a function that parses CSV files. Here's my first test:

[paste test code]

Make this test pass.

AI: [implements minimal solution]

You: Good. Now add support for quoted fields containing commas.
Here's the test:

[paste test code]

AI: [extends implementation]
```

### Pattern 2: Bug Fix with Reproduction

```
You: There's a bug - the calculator crashes on negative numbers.
Write a test that reproduces this bug.

AI: [writes failing test]

You: Good. Now fix it.

AI: [fixes implementation, test passes]
```

### Pattern 3: Incremental Feature Building

```
You: I'm building a shopping cart. Let's start TDD-style.

Write a test for adding a single item to an empty cart.

AI: [writes test]

You: Now implement it.

AI: [minimal implementation]

You: Great. Now write a test for adding multiple items.

AI: [writes test]

You: Implement that.

[Continue iterating...]
```

---

## Common TDD Mistakes

### Guessing Instead of Asking

❌ **Don't do this:**

```kotlin
// AI writes test with guessed output format
@Test
fun `query execution produces output`() {
    val output = executeQuery(query)

    // Guessing it's JSON... or maybe plain text... adding defensive checks
    assertTrue(output.contains("result") || output.contains("{"))
    // This passes for many wrong outputs!
}
```

✅ **Do this:**

````
Human: "I need tests for query execution. What should the output format be?"

AI: "I don't know the output format. Let me ask:
- Should the output be JSON, plain text, or something else?
- Can you show me an example of expected output?
- Are there different formats for different query types?"
````

### Writing Tests After Implementation

❌ **Don't do this:**

```kotlin
// Oops, already wrote the whole implementation
fun calculateShipping(order: Order): Double {
    // 50 lines of complex logic
}

// Now trying to test it...
@Test
fun `shipping calculation works`() {
    // Hard to know what to test
    // Tempted to just call it and check it doesn't crash
}

```

✅ **Do this:**

```kotlin
// 1. Write test first
@Test
fun `free shipping for orders over 50 dollars`() {
    val order = Order(items = listOf(Item(price = 60.0)))
    assertEquals(
        0.0,
        calculateShipping(order),
        0.01,
        "Orders over $50 should have free shipping but got $${calculateShipping(order)}"
    )
}

// 2. Now implement
fun calculateShipping(order: Order): Double {
    if (order.total() >= 50.0) return 0.0
    return 5.99
}

```

### Writing Too Much Code at Once

❌ **Don't do this:**

```kotlin
@Test
fun `complete order processing workflow`() {
    // Testing everything at once
}

fun processOrder(order: Order) {
    // Implementing entire workflow before any tests pass
    validateOrder(order)
    calculateTotals(order)
    applyDiscounts(order)
    processPayment(order)
    sendConfirmation(order)
    updateInventory(order)
}

```

✅ **Do this:**

```kotlin
// Test 1: Just validation
@Test
fun `order with items is valid`() { }

// Test 2: Add calculation
@Test
fun `calculates subtotal correctly`() { }

// Test 3: Add discounts
@Test
fun `applies discount code`() { }

// Build up incrementally...

```

### Skipping Refactor Step

❌ **Don't do this:**

```kotlin
// Test passes, move on! (Don't refactor)
fun calculate(x: Double, y: Double, z: Double): Double {
    if (x > 0) {
        if (y > 0) {
            if (z > 0) {
                return x * y * z * 0.9  // Copy-pasted magic numbers everywhere
            }
        }
    }
    return x * y * z
}

```

✅ **Do this:**

```kotlin
// Test passes, now refactor
fun calculate(values: List<Double>): Double {
    val product = values.reduce { acc, value -> acc * value }
    return if (allPositive(values)) {
        applyDiscount(product, STANDARD_DISCOUNT_RATE)
    } else {
        product
    }
}

```

---

## Summary

### Key Takeaways

1. **TDD is mandatory** for all new development and bug fixes
2. **Write tests first** - It's more efficient than testing after
3. **Follow the disciplined RED phase workflow** - Compile, review, refine, run, commit before implementing
4. **AI assistants work best with TDD** - Tests provide explicit requirements
5. **Follow Red-Green-Refactor** - Small steps, continuous improvement
6. **Tests codify requirements** - They define what "working" means
7. **Tests enable refactoring** - Change code confidently

### The TDD Cycle

1. **Red:** Write failing test (defines requirement)
2. **Green:** Make it pass (minimal implementation)
3. **Refactor:** Improve design (tests protect against breakage)
4. **Repeat:** Next requirement

### Remember

- Start with the simplest test
- Take small steps
- Run tests frequently
- Keep tests fast and independent
- Refactor when tests are green
- Let tests guide your design

---

## Related Documents

- [best-practices-testing.md](best-practices-testing.md) - Comprehensive testing standards and patterns
- [best-practices-kotlin-code.md](best-practices-kotlin-code.md) - Kotlin coding standards
- [leap-implementation-guide-ghee.md](leap-implementation-guide-ghee.md) - LEAP development workflow
- [best-practices-logging.md](best-practices-logging.md) - Logging best practices for test diagnostics
