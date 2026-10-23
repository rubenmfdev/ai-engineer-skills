# Black-box techniques with examples

## Equivalence partitioning + boundary value analysis
Spec: ticket price by age. 0 to 12 child ($5), 13 to 64 adult ($10), 65 to 120 senior ($7). Anything else is invalid.

| Partition | Class | Representative |
| --- | --- | --- |
| Invalid low | age < 0 | -5 |
| Child | 0 to 12 | 6 |
| Adult | 13 to 64 | 30 |
| Senior | 65 to 120 | 80 |
| Invalid high | age > 120 | 150 |
| Invalid type | not an integer | "abc", 12.5, null |

Boundary values (two-value): `-1, 0, 12, 13, 64, 65, 120, 121`.
That is 8 boundary tests plus 3 type tests, instead of 120+ inputs. Check each boundary against the spec: "up to 12" is `<= 12`, not `< 12`. Ambiguous specs are themselves a finding.

## Decision table
Spec: members get 10% off orders of $100 or more, 5% below $100. Non-members get 2% off orders of $100 or more, nothing below.

| Rule | R1 | R2 | R3 | R4 |
| --- | --- | --- | --- | --- |
| Member? | Y | Y | N | N |
| Order >= $100? | Y | N | Y | N |
| **Discount** | 10% | 5% | 2% | 0% |

One test per rule (4 tests). With n binary conditions there are up to 2^n rules. Merge rules where a condition does not matter ("-"). Add boundary tests at 99.99, 100.00.

## State transition testing
Order lifecycle: Created -> Paid -> Shipped -> Delivered. Created or Paid -> Cancelled. Shipped and Delivered cannot be cancelled.

| From \ Event | pay | ship | deliver | cancel |
| --- | --- | --- | --- | --- |
| Created | Paid | invalid | invalid | Cancelled |
| Paid | invalid | Shipped | invalid | Cancelled |
| Shipped | invalid | invalid | Delivered | **invalid** |
| Delivered | invalid | invalid | invalid | invalid |
| Cancelled | invalid | invalid | invalid | invalid |

Coverage levels: all states, all valid transitions (each arrow once), all invalid transitions (every "invalid" cell must be rejected without corrupting state), and sequences of length n for riskier flows. The invalid cells are where bugs hide.

## Pairwise (combinatorial)
Parameters: Browser {Chrome, Firefox, Safari}, OS {Windows, macOS, Linux}, Language {EN, ES}. Full combination is 18. Pairwise covers every pair of values from any two parameters in 9 tests:

| # | Browser | OS | Language |
| --- | --- | --- | --- |
| 1 | Chrome | Windows | EN |
| 2 | Chrome | macOS | ES |
| 3 | Chrome | Linux | EN |
| 4 | Firefox | Windows | ES |
| 5 | Firefox | macOS | EN |
| 6 | Firefox | Linux | ES |
| 7 | Safari | Windows | EN |
| 8 | Safari | macOS | ES |
| 9 | Safari | Linux | EN |

Based on the observation that most defects come from one or two parameters interacting. Tools: PICT, AllPairs. Add known-risky full combinations by hand. Wrong when a bug needs three parameters together.

## Use case / scenario testing
Take a user goal, e.g. "Reset password". Main flow: request link, open email, set new password, log in. Alternate flows: expired link, reused link, unknown email, weak password, link opened twice. One test per flow. Good for acceptance tests.

## Error guessing and exploratory testing
Use experience: empty strings, very long input, Unicode and emoji, leading and trailing spaces, negative numbers, zero, null, duplicates, concurrent requests, clock changes, timezones, offline, interrupted uploads. In exploratory sessions timebox (30 to 60 min), set a charter ("explore checkout with invalid addresses"), take notes, turn findings into automated tests.

## Property-based testing
Instead of examples, state properties that hold for all inputs and let a tool generate cases: `decode(encode(x)) == x`, sorting is idempotent, `len(result) == len(input)`. Tools: fast-check (JS), Hypothesis (Python), swift-testing parameterized tests or SwiftCheck.
