---
name: adr-writing
description: Write and review Architecture Decision Records that capture context, options, the decision and consequences. Use when making a significant technical decision, documenting why a design was chosen, or reviewing a proposed architecture change.
---

# ADR Writing

An ADR records **one** significant decision and why, so future readers do not have to rediscover it.

## When to write one
- Hard to reverse or expensive to change (datastore, framework, auth model, API style).
- Affects multiple teams or modules.
- Someone will ask "why did we do it this way?" in six months.

Skip it for easily reversible or purely local choices.

## Workflow
1. Name the decision as a question: "How do we store user sessions?"
2. Gather constraints: scale, latency, team skills, budget, compliance, deadlines.
3. List at least two real options, including "do nothing" when plausible.
4. Compare options against the constraints, with evidence (benchmarks, prior incidents, docs).
5. Decide, and state the trade-offs honestly.
6. Save as `docs/adr/NNNN-short-title.md`, number sequentially, never renumber.
7. Link superseded ADRs. Do not edit an accepted ADR's decision, write a new one that supersedes it.

## Template
```markdown
# NNNN. Title in the form of a decision

- Status: proposed | accepted | superseded by NNNN | rejected
- Date: YYYY-MM-DD
- Deciders: names or roles

## Context
The forces at play: problem, constraints, requirements. Facts, not advocacy.

## Options considered
### Option A, name
Pros / cons / cost.
### Option B, name
Pros / cons / cost.

## Decision
We will ... because ...

## Consequences
Good: ...
Bad / risks: ...
Follow-ups: ...
```

## Review checklist
- Is the problem stated separately from the solution?
- Are the options genuine, with their costs, not strawmen?
- Does the decision follow from the context and name the main trade-off?
- Are consequences concrete, including the negative ones?
- Is there a trigger to revisit it (metric, date, scale threshold)?
- Is it short enough to be read (one to two pages)?
