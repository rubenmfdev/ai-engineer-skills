# Structure

## Category tree vs. skill contents

The tree above a skill is for humans browsing the repo. The tools only care about the skill folder (the one containing `SKILL.md`).

```
skills/
  languages/swift/swift-concurrency/        <- skill folder
    SKILL.md
    references/actors.md
  languages/javascript/typescript-conventions/
    SKILL.md
    scripts/check-tsconfig.mjs
  platforms/chrome-extensions/mv3-extension-development/
    SKILL.md
    assets/manifest.example.json
```

## Rules

- `scripts/validate.py` finds every folder with a `SKILL.md`, whatever its depth.
- The only checks are on `SKILL.md` frontmatter and size, and that relative links resolve.
- Inside a skill, use whatever fits: Swift skills might ship `references/` only, a JS skill might ship runnable `scripts/`, a Chrome extension skill might ship `assets/` templates.
- Suggested (not required) names: `references/` for docs loaded on demand, `scripts/` for executables, `assets/` for files copied into output.

## Adding a category

Create `skills/<category>/` and add a short `README.md` saying what belongs there. Nested groups (such as `languages/swift/`) are optional.
