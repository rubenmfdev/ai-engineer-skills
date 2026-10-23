# Compatibility

| Thing | Scope | Portable? |
| --- | --- | --- |
| `SKILL.md` folder (Agent Skills format) | On-demand skill, loaded by `description` | Yes, across agents that implement the format |
| `AGENTS.md` | Always-on project instructions | Yes, widely read across agents |
| Claude `CLAUDE.md` | Always-on project instructions for Claude Code | Claude only |
| Cursor rules (`.cursor/rules/*.mdc`) | Rules with globs or manual triggers | Cursor only |
| Copilot `.github/copilot-instructions.md` | Always-on repo instructions | Copilot only |
| Gemini `GEMINI.md` and TOML commands | Instructions and commands | Gemini CLI only |

Support changes quickly, so verify against each tool's current docs.

## Policy

- `SKILL.md` is the source of truth.
- Keep vendor-specific frontmatter (such as `allowed-tools`) out of skills unless it is harmless when ignored.
- Non-portable outputs are produced by scripts in `adapters/`, never edited by hand.
