# Contributing

## Adding a skill

1. Copy `templates/SKILL.template.md` to `skills/<category>/[<group>/]<your-skill>/SKILL.md`.
2. The folder name must equal the `name` in the frontmatter (lowercase letters, digits, hyphens).
3. Write the `description` as a trigger. Say **what** the skill does and **when** to use it, including the words a user would type. It is the only part always loaded into context.
4. Keep `SKILL.md` under about 500 lines. Move detail into `references/` and link to it so it loads on demand.
5. Put runnable helpers in `scripts/` inside the skill, not in the body.
6. Run `python3 scripts/validate.py` and fix every error.
7. Add the skill to the catalog table in `README.md`.

## Quality bar

- Opinionated and specific beats generic advice an agent already knows.
- Include concrete do/don't examples and the reasoning behind rules.
- Say which tool or OS versions the guidance targets.
- No copied content without a compatible license; credit sources in the skill.
- Prefer skills that were tried on real tasks.

## Folder freedom

Skills may use any internal layout. Only `SKILL.md` is required, so do not add empty folders to match other skills.
