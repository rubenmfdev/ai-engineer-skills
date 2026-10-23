---
name: software-testing-fundamentals
description: Classic software testing theory applied to real code. Covers black-box techniques (equivalence partitioning, boundary values, decision tables, state transitions, pairwise), white-box coverage (statement, branch, condition, MC/DC, cyclomatic complexity), gray-box, test levels and types, mutation testing and test doubles. Use when designing test cases, reviewing test quality or coverage, deciding what to test, or explaining testing concepts.
---

# Software Testing Fundamentals

## Workflow for designing tests
1. **Test basis:** what defines correct behavior? Requirements, spec, acceptance criteria, API contract, or only the code.
2. **Level:** unit, integration, system or acceptance (see below). Use the lowest level that can catch the defect.
3. **Technique:** choose from the table. Use more than one.
4. **Derive cases:** write input, expected result and why this case exists.
5. **Oracle:** know the expected result without running the code. If you cannot say what correct is, you do not have a test, you have a demo.
6. **Prioritize by risk:** likelihood times impact. Money, data, security and frequently used paths first.
7. **Review gaps:** check coverage, run mutation testing on critical code, do a short exploratory session.

## Which technique when
| Situation | Technique | Family |
| --- | --- | --- |
| Input has ranges or categories | Equivalence partitioning + boundary value analysis | Black-box |
| Output depends on combinations of conditions | Decision table / cause-effect | Black-box |
| Behavior depends on history or state | State transition testing | Black-box |
| Many parameters with interactions | Pairwise (combinatorial) | Black-box |
| User flows end to end | Use case / scenario testing | Black-box |
| Complex branching in code | Branch, condition, MC/DC coverage | White-box |
| Variables passed between statements | Data flow (def-use) testing | White-box |
| Unknown unknowns | Exploratory testing, error guessing, fuzzing, property-based | Experience-based |
| Are my tests any good? | Mutation testing | Test-quality |

Details and worked examples: [black-box techniques](references/black-box-techniques.md), [white-box coverage](references/white-box-coverage.md).

## Black-box, white-box, gray-box
- **Black-box (specification-based):** tests derive from requirements, ignoring code. Finds missing features and wrong behavior. Cannot see untested code paths.
- **White-box (structure-based):** tests derive from code structure. Finds untested paths and dead code. Cannot find a requirement that was never implemented.
- **Gray-box:** spec-driven tests that use some knowledge of internals (data layout, known risky modules, DB state checks).
Use black-box to decide **what** to test and white-box coverage to see **what you missed**.

## Quick reference
**Equivalence partitioning:** split inputs into classes that the system should treat alike. Test one value per class, valid and invalid.
**Boundary values:** bugs cluster at edges. For a valid range `[a, b]` test `a-1, a, b, b+1` (two-value) or also `a+1, b-1` (three-value).
**Coverage hierarchy:** statement < branch (decision) < condition < MC/DC < path. Branch coverage guarantees statement coverage, not the reverse. 100% coverage proves the code ran, not that it is right: assertions are what test behavior.
**Cyclomatic complexity:** `V(G) = decisions + 1` (counting each `if`, loop, `case`; count `&&`/`||` too if you count conditions). It equals the number of independent paths and the minimum tests for basis-path coverage.

## Levels
| Level | Scope | Speed | Typical tools |
| --- | --- | --- | --- |
| Unit | One function or class, collaborators faked | ms | XCTest / Swift Testing, Vitest, Jest |
| Integration | Modules together, real DB or network stub | seconds | Testcontainers, supertest |
| System / E2E | Whole app through its UI or API | slow | Playwright, XCUITest |
| Acceptance | Does it meet the business need | varies | BDD scenarios, manual UAT |

Prefer many fast unit tests, fewer integration tests, few E2E (the test pyramid). For UI-heavy apps a "trophy" shape with more integration tests is also common. Pick on cost versus confidence.

## Types of testing (what is checked, orthogonal to level)
Functional, regression (did old behavior break), smoke (does it start), sanity (quick check after a change), performance and load, security, usability and accessibility, compatibility, localization, recovery. Static testing (code review, linting, type checking) finds defects without running code.

## Seven testing principles
1. Testing shows the presence of defects, not their absence.
2. Exhaustive testing is impossible. Use risk and techniques.
3. Test early. Defects are cheaper the sooner they are found.
4. Defects cluster. A few modules hold most bugs.
5. Pesticide paradox. The same tests stop finding new bugs. Refresh them.
6. Testing is context dependent. A pacemaker is not a blog.
7. "No defects found" does not mean the right product was built.

## Test doubles
| Double | Purpose |
| --- | --- |
| Dummy | Fills a parameter, never used |
| Stub | Returns canned answers |
| Spy | Stub that records calls |
| Mock | Pre-programmed with expectations, fails if not met |
| Fake | Working lightweight implementation (in-memory DB) |
Prefer fakes and stubs. Over-mocking couples tests to implementation.

## Qualities of a good test
- One reason to fail. Name states the behavior: `rejects_expired_token`.
- Arrange, Act, Assert. No logic (loops, ifs) in tests.
- Deterministic: no real time, randomness, network or shared state without control.
- Fast and independent: any order, in parallel.
- Fails for the right reason. Watch it fail once before trusting it.
- Tests behavior through the public interface, not private details.

## Deliverable when asked to design tests
Give a table:

| ID | Technique | Input | Expected | Why |
| --- | --- | --- | --- | --- |
| T1 | BVA | age = 17 | rejected | lower boundary - 1 |

Then list what is deliberately not covered and the risk of that.

## Common mistakes
- Chasing a coverage number instead of risk.
- Testing only the happy path.
- Asserting nothing meaningful (calls code, checks it did not throw).
- Copying the implementation into the test as the expected value.
- Flaky tests left in the suite. Fix or delete.
- Testing the framework or trivial getters.
- Writing tests only after the code, from the code, so they confirm bugs.
