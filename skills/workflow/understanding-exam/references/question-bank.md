# Question templates

Fill the brackets from the real diff.

## Problem
- What was going wrong before this change, and for whom?
- What is the root cause? Why did [symptom] only happen when [condition]?
- What would a user notice after this change that they did not before?

## Rationale
- Why [approach] instead of [alternative]? What does the alternative cost?
- Why does [function] live in [module] and not [other module]?
- What assumption does [design choice] rely on? What if it stops holding?

## Code trace
- [Input X] arrives at [entry point]. List the functions that run, in order, and the final result.
- Which line decides [behavior], and what are its inputs?
- Where does [value] come from, and who can change it?

## What if
- What breaks if [guard/check/lock] is removed?
- What if [dependency] is slow, down or returns [odd value]?
- What if this runs twice, or two runs overlap?
- What changes at 100 times the data?

## Risk and edges
- What is the worst realistic failure of this change? How would you notice?
- How do we roll this back? What data cannot be rolled back?
- What input could abuse this (security)?

## Tests
- Which behavior is not covered by the tests? How would you test it?
- If [line] were changed to [mutation], which test fails? If none, why?

## Spot the flaw (give a short claim, ask if it is true)
- "The retry loop is safe because requests are idempotent." (Are they? Check [endpoint].)
- "The cache is invalidated on every write." (Is it, in [path]?)

## Multiple choice pattern
Stem with a concrete scenario, 4 options, one correct, distractors based on real misconceptions:
- the plausible but outdated behavior
- the behavior in a different branch
- the behavior that would be true if [guard] were missing
