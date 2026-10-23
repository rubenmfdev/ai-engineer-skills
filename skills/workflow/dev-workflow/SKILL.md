---
name: dev-workflow
description: Run software work through explicit phases with gates (analysis, grill, design, implementation, testing, validation, done), scaled to the size of the task. Includes a grill-me interview before implementation, then a pull request and an understanding exam for the engineer before done. Use when starting a non-trivial feature, bug fix or refactor, when asked to "follow the workflow", or when the engineer wants control over how the agent works.
---

# Dev Workflow

A process wrapper for agent work. The agent proposes, the engineer decides at each gate.

## Step 0: size the task and announce it
| Size | Examples | Phases to run |
| --- | --- | --- |
| Trivial | typo, rename, config tweak | Implement, Test |
| Small | single-file bug, small helper | Analysis (short), Implement, Test, Validate (PR) |
| Standard | feature, multi-file fix | All phases |
| Risky | auth, payments, migrations, data deletion, public API | All phases, plus an ADR and a second review |

Say the size and the phases in one line, e.g. `Standard task. Phases: analysis, grill, design, implement, test, validate.` The engineer can override ("skip the grill", "full workflow"). Show the phases as a task list and tick them off.

## Phases and gates
| # | Phase | What the agent does | Output | Gate to leave |
| --- | --- | --- | --- | --- |
| 1 | **Analysis** | Read the request and the code. Find facts yourself (do not ask what you can look up). List unknowns and non-goals. | Problem statement (3 to 6 lines), acceptance criteria, open questions | Engineer confirms the understanding |
| 2 | **Grill** | Interview the engineer until nothing important is assumed. Use the `grill-me` skill if installed, otherwise follow [the built-in grill](#the-built-in-grill). | Decisions list | Engineer says go |
| 3 | **Design** | Compare at least two options for non-trivial work. Pick one. List files and interfaces touched, test strategy, risks, rollback. Write an ADR (`adr-writing`) for hard-to-reverse choices. | Plan as small ordered steps, each verifiable | Engineer approves the plan |
| 4 | **Implementation** | Work in thin slices. Test first where it fits (`tdd`, `test-driven-development`). One logical change per commit. Note out-of-scope findings instead of fixing them. Run build and lint after each slice. | Working code | All plan steps done, build and lint pass |
| 5 | **Testing** | The agent checks it built the thing right. Run the relevant suites, add missing tests (use `software-testing-fundamentals` to find gaps), add a regression test for every bug. Evidence before claims (`verification-before-completion`). | Test results, list of what is not tested | Tests pass, gaps stated honestly |
| 6 | **Validation** | The engineer checks it is the right thing and that they own it. Check each acceptance criterion with evidence, self-review the diff, open the PR (`create-pull-request`), then run the `understanding-exam`. | PR link, exam result | Criteria met, exam passed or waived by the engineer |
| 7 | **Done** | Summarize what changed, what was decided, follow-ups. Optional short retro. | Final report | n/a |

Testing is the agent proving correctness. Validation is the human confirming it solves the right problem and that they understand it.

## The built-in grill
Use this when no `grill-me` skill is installed.
1. Build a tree of decisions: every choice branches into the choices that depend on it.
2. Ask in rounds. Each round holds every question whose prerequisites are settled. Number them and give your recommended answer so "yes" accepts it.
3. Never ask something you can find in the code, docs or tools. Look it up.
4. Recompute the tree after each answer. Stop when no open branch is left and nothing is silently assumed.
5. Summarize the decisions and ask for the go-ahead. Do not start building before it.

Always grill, even for small tasks, when the request is ambiguous, touches security or data, or has more than one reasonable design.

## Rules
- Never skip a gate silently. If skipping, say so and why.
- If new facts break an earlier phase, go back, say so, and redo it.
- Keep the plan small. Prefer 5 steps over 25.
- Pushing, opening PRs and anything visible to others needs the engineer's yes, unless they already asked for it.
- Do not claim done without evidence from this session: command and result.
- Keep scope. Park everything else in a "follow-ups" list.

## Skills used per phase
| Phase | Skill (if installed) | Fallback |
| --- | --- | --- |
| Grill | `grill-me` | built-in grill above |
| Design | `living-specs`, `adr-writing` | options table in chat |
| Implementation | `tdd` or `test-driven-development`, language skills | red-green-refactor by hand |
| Testing | `software-testing-fundamentals`, `verification-before-completion` | run the suite, read the output |
| Validation | `create-pull-request`, `understanding-exam`, `code-review` | PR template in `create-pull-request` |

## Status line
Keep one line current while working:
`Phase 4/7 Implementation | step 3 of 5 | tests: green | blocked: no`

## Customizing
If the repo has `docs/WORKFLOW.md`, read it first. It overrides this skill (phase names, required gates, PR rules, exam pass mark).
