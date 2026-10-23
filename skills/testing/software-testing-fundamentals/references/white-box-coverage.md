# White-box coverage with examples

## Example under test
```python
def shipping(weight, express):
    cost = 5
    if weight > 10 and not express:   # D1, conditions A: weight > 10, B: not express
        cost += 10
    elif express:                      # D2
        cost += 20
    return cost
```

## Criteria
| Criterion | Requires | Tests for the example |
| --- | --- | --- |
| Statement | Every statement runs | `(11, False) -> 15`, `(5, True) -> 25` (2 tests) |
| Branch / decision | Every decision outcome true and false | Add `(5, False) -> 5` so D2 is also false (3 tests) |
| Condition | Every atomic condition true and false | A and B each take both values |
| Condition/decision | Condition + decision both | Combine the two above |
| MC/DC | Each condition independently flips the decision outcome | See below |
| Path | Every path through the code | Exponential with loops. Impractical in full |

Statement coverage with two tests looked complete (100%) but missed the case where neither branch applies (`(5, False)`), which branch coverage exposes. That is why branch is the practical minimum.

## MC/DC (modified condition/decision coverage)
Required in avionics (DO-178C) and automotive safety. For a decision with n conditions you need n+1 tests (minimum). For D1 = A and B:

| Test | weight, express | A | B | D1 | Shows |
| --- | --- | --- | --- | --- | --- |
| 1 | 11, False | T | T | T | baseline |
| 2 | 5, False | F | T | F | A alone flips D1 vs test 1 |
| 3 | 11, True | T | F | F | B alone flips D1 vs test 1 |

These three tests also give statement, branch and condition coverage, and cover D2 both ways.

## Cyclomatic complexity
`V(G) = E - N + 2P` on the control-flow graph, or decisions + 1.
- Counting decisions: `if` + `elif` = 2, so V = 3, meaning 3 independent paths (the three tests above).
- Counting each condition: `and` adds 1, so V = 4.
- Rule of thumb: above 10 split the function. Complexity is the minimum number of tests to cover every basis path.

## Loops
Test zero iterations, one iteration, many iterations, and the maximum. Test the loop exit condition boundary (off-by-one).

## Data flow testing
Track where each variable is defined (`def`) and used (`use`). Cover each def-use pair: a value assigned in one branch and read later. Catches uninitialized variables, overwritten values and dead assignments.

## What coverage cannot tell you
- Missing code (a requirement never implemented) has no lines to cover.
- A test with no assertion still covers lines.
- Run **mutation testing** to check assertions: tools inject small bugs (`>` to `>=`, `+` to `-`, delete a call) and see whether tests fail. A surviving mutant means a missing or weak test. Tools: Stryker (JS/TS), PIT (Java), mutmut (Python), Muter (Swift). Run it on critical modules, not the whole codebase every time.

## Coverage targets
Treat as a floor that finds gaps, never a goal in itself. Reasonable: 80% line/branch for business logic, higher for critical logic, lower for glue and UI. Review the uncovered lines, do not just count.
