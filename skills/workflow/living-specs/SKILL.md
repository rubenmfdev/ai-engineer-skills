---
name: living-specs
description: Spec-driven development with specs stored in the repository where every future agent and engineer can find them. Sets up docs/specs with an auto-generated index, a spec template with testable acceptance criteria, a status lifecycle, and rules to keep specs updated in the same PR as the code. Use when starting a feature, when asked to write a spec, PRD or requirements, before implementing from a spec, or when setting up specs for a project.
---

# Living Specs

A spec says **what the system should do and why**, in terms a test can check. Stored in the repo and versioned with the code, it is the memory that future agents lack: they read the index, load only the specs they need, and change behavior knowingly.

## What goes where
| Artifact | Answers | Lives in | Lifetime |
| --- | --- | --- | --- |
| **Spec** | What behavior, for whom, how we know it works | `docs/specs/` | As long as the behavior exists. Updated with the code |
| **ADR** | Why we chose this design over others | `docs/adr/` (see `adr-writing`) | Permanent, superseded not edited |
| **Plan / tasks** | How and in what order | PR, issue, or a section in the spec | Throwaway |
| **Code and tests** | The actual behavior | source | Truth of what runs |

## Layout
```
docs/specs/
  README.md                  # generated index, one line per spec
  <area>/<NNNN>-<slug>.md    # e.g. auth/0003-login-rate-limit.md
```
First check whether the project already has a convention (`specs/`, `.specify/`, `openspec/`, `.kiro/specs/`). If it does, follow it and do not add a second place. Otherwise use `docs/specs/`. Bootstrap with:
```bash
python3 <skill-dir>/scripts/specs_index.py --init
```
This creates `docs/specs/README.md` and `docs/specs/_template.md`. The spec template is also at [assets/spec-template.md](assets/spec-template.md).

## Spec anatomy
Front matter: `id`, `title`, `status`, `area`, `summary` (one line, this is what agents scan), `updated`, optional `supersedes`, `superseded_by`, `related` (ADRs, issues, PRs).

Sections: Context, Goals, Non-goals, Requirements (`R1`, `R2`... use "shall"), Acceptance criteria (`AC1`... in Given/When/Then), Open questions, Design notes (link ADRs), Test mapping (AC to test), Rollout and risks, Change log.

Write requirements and criteria so a test can pass or fail on them:
- Bad: "Login should be fast and secure."
- Good: `R2` The system shall lock an account for 15 minutes after 5 failed logins within 10 minutes. `AC2` Given 5 failed logins in 10 minutes, when a 6th login with the correct password is attempted, then it is rejected with 429 and a `Retry-After` header.

## Status lifecycle
`draft` -> `approved` -> `implemented` -> `deprecated` or `superseded`
- Only the engineer moves a spec to `approved`. The agent proposes.
- `implemented` means merged, with every acceptance criterion mapped to a test.
- Never delete a spec. Mark it `deprecated`, or `superseded` with a link to the new one.

## Workflow
1. **Discover.** Read `docs/specs/README.md`. Search for related specs (`rg -il "<keyword>" docs/specs`). If one exists, update it. Do not write a duplicate. Load only the relevant specs, not the whole folder.
2. **Draft.** After the grill (`grill-me`, or phase 2 of `dev-workflow`), write the spec from the decisions made. Put unknowns under **Open questions**, never guesses. Keep it to about two pages. One spec per capability, not per ticket.
3. **Approve.** The engineer reviews and sets `status: approved`. For big features, commit the spec on its own first.
4. **Implement.** Write tests from the acceptance criteria and put the AC id in the test name. Cite the spec id in commits and the PR. If reality forces a deviation, stop, say so, and update the spec with the engineer's agreement. Never drift silently.
5. **Close.** Set `status: implemented`, fill the test mapping and note deviations, then regenerate the index and run the check.
6. **Maintain.** A bug that reveals a spec gap updates the spec in the fix PR. A PR that changes behavior without touching the spec is incomplete.

## Index and lint
```bash
python3 <skill-dir>/scripts/specs_index.py            # regenerate the index in docs/specs/README.md
python3 <skill-dir>/scripts/specs_index.py --check    # lint only, exit 1 on problems (use in CI)
python3 <skill-dir>/scripts/specs_index.py --next auth  # print the next free id for an area
```
`--check` reports: missing required fields, unknown status, duplicate ids, `supersedes` or `related` ids that do not exist, approved or implemented specs with no acceptance criteria, and an index that is out of date. `--root DIR` points at another specs folder.

## Make agents find the specs
Offer to add this to the project's `AGENTS.md` (or `CLAUDE.md`) and add it only with the engineer's yes:
```markdown
## Specs
Specs live in `docs/specs/` (index: `docs/specs/README.md`). Before changing behavior, find the relevant spec and read it. Specs with status approved or implemented are binding. Update the spec in the same PR as the code, and cite its id in commits and the PR.
```
Optionally run `--check` in CI and add "spec updated or not needed" to the PR template.

## Anti-patterns
- A spec per ticket. It piles up as noise. Use one per capability and update it.
- Specs that describe implementation (classes, tables). Put that in design notes or ADRs.
- Untestable criteria ("user-friendly", "fast").
- Writing the spec after the code to describe what happened. That is documentation, not a spec.
- A huge up-front spec for everything. Spec the next increment.
- Letting specs rot. Old and wrong is worse than missing, so deprecate what no longer holds.

## Works with
`dev-workflow` (the spec is the output of the grill and design phases), `grill-me`, `adr-writing`, `create-pull-request` (link the spec), `understanding-exam` (questions come from the spec and the diff). If the project already uses a spec tool such as [GitHub Spec Kit](https://github.com/github/spec-kit) or [OpenSpec](https://github.com/Fission-AI/OpenSpec), use its layout and commands instead of this one.
