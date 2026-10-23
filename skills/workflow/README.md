# Workflow
Skills that shape how the agent works: phases, gates, pull requests and comprehension checks. Planned additions welcome.

## Our skills
- [dev-workflow](dev-workflow): phases and gates (analysis, grill, design, implementation, testing, validation, done), scaled to task size.
- [create-pull-request](create-pull-request): preflight, description template, draft PR via `gh`.
- [living-specs](living-specs): spec-driven development with specs in `docs/specs/`, an auto-generated index and a lint script, so future agents find them.
- [understanding-exam](understanding-exam): exam on the issue and solution for the engineer, graded with feedback.

## Curated external skills (category `workflow`)
Read before using. The defaults are marked.

| Skill | Author | Phase | Default | Notes |
| --- | --- | --- | --- | --- |
| [grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) | Matt Pocock | Grill | yes | Relentless interview in rounds, with a recommended answer for each question. Installs `grilling` with it |
| [verification-before-completion](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) | Jesse Vincent (obra) | Testing | yes | Evidence before any "done" claim |
| grill-with-docs, domain-modeling | Matt Pocock | Grill, design | optional | Same interview, also writes ADRs and a glossary |
| to-spec, to-tickets | Matt Pocock | Planning | optional | Need an issue tracker set up with his setup skill |
| pr, code-review, diagnosing-bugs, retro, handoff | Matt Pocock | various | optional | PR body template, review against spec, debugging loop |
| brainstorming, writing-plans, executing-plans | obra/superpowers | Design, implementation | optional | Heavier, opinionated planning flow |
| systematic-debugging, requesting/receiving-code-review, finishing-a-development-branch | obra/superpowers | various | optional | |
| spec-driven-development, planning-and-task-breakdown, interview-me, incremental-implementation, shipping-and-launch | Addy Osmani | various | optional | `interview-me` is an alternative to `grill-me` |

The skills collections these come from also ship their own full workflows ([mattpocock/skills](https://github.com/mattpocock/skills), [obra/superpowers](https://github.com/obra/superpowers), [github/spec-kit](https://github.com/github/spec-kit)). Installing a whole workflow framework next to `dev-workflow` gives the agent two competing processes, so pick one.

```bash
python3 scripts/install.py --category workflow,testing --project
```
