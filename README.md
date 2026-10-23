# AI Engineer Skills

A curated collection of agent skills for software engineers, covering languages, platforms, system design, DevOps and more. Built on the open **Agent Skills** format (`SKILL.md`), so they work with Claude Code and with other agents that read the same format.

> Status: early. v1 focuses on **Swift**, **JavaScript/TypeScript** and **Chrome extensions**.

## Catalog

| Skill | Category | What it does |
| --- | --- | --- |
| [swiftui-best-practices](skills/languages/swift/swiftui-best-practices) | Swift | State, view composition, navigation and performance in SwiftUI |
| [swift-concurrency](skills/languages/swift/swift-concurrency) | Swift | async/await, actors, Sendable and migrating to Swift 6 |
| [typescript-conventions](skills/languages/javascript/typescript-conventions) | JavaScript | Strict TypeScript, modules, error handling and tooling |
| [mv3-extension-development](skills/platforms/chrome-extensions/mv3-extension-development) | Chrome extensions | Manifest V3 architecture, service workers, messaging, storage |
| [extension-security-and-publishing](skills/platforms/chrome-extensions/extension-security-and-publishing) | Chrome extensions | Least-privilege permissions, CSP and Chrome Web Store review |
| [adr-writing](skills/system-design/adr-writing) | System design | Write and review architecture decision records |
| [github-actions-ci](skills/devops/github-actions-ci) | DevOps | Fast, secure GitHub Actions pipelines |

Planned categories: mobile, testing, security, design, AI engineering, git workflow. See [skills/](skills).

## Install

```bash
git clone https://github.com/rubenmfdev/ai-engineer-skills.git
cd ai-engineer-skills

# Install every skill for Claude Code (user level)
python3 scripts/install.py --target claude

# Only some skills, copied instead of symlinked
python3 scripts/install.py --target claude --only swift-concurrency,adr-writing --copy

# Other agents that read SKILL.md folders
python3 scripts/install.py --dest ~/.some-agent/skills
```

Add `--project` to install into the current project (`./.claude/skills`) instead of your home directory.

## Repository layout

```
skills/<category>/[<group>/]<skill>/SKILL.md   # one folder per skill
templates/                                      # skill and AGENTS.md templates
adapters/                                       # exporters for non-SKILL.md tools
commands/                                       # slash-command style prompts (later)
scripts/                                        # validate.py, install.py
docs/                                           # format notes and compatibility
```

**Each skill is self-contained.** The only required file is `SKILL.md`. Everything else (`references/`, `scripts/`, `assets/`, ...) is up to the skill, so a Swift skill and a Chrome extension skill can look completely different inside. See [docs/structure.md](docs/structure.md).

## Compatibility

See [docs/compatibility.md](docs/compatibility.md) for how `SKILL.md`, `AGENTS.md`, Cursor rules and Copilot instructions relate.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Short version: one focused skill per folder, a precise `description`, run `python3 scripts/validate.py`.

## Credits and curated links

Other great skill collections are listed in [docs/curated-links.md](docs/curated-links.md).

## License

MIT, see [LICENSE](LICENSE).
