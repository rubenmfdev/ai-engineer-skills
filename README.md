# AI Engineer Skills

A curated collection of agent skills for software engineers, covering languages, platforms, system design, DevOps and more. Built on the open **Agent Skills** format (`SKILL.md`), so they work with Claude Code and with other agents that read the same format.

> Status: early. v1 focuses on **Swift**, **JavaScript/TypeScript** and **Chrome extensions**.

## Use it with your agent

Open your project in Claude Code (or another agent) and say:

> Get all the necessary skills for our project from https://github.com/rubenmfdev/ai-engineer-skills. Follow its AGENTS.md.

The agent clones this repo, looks at your project (Swift, JavaScript, Chrome extension, ...), picks the matching skills and installs them into `./.claude/skills`. See [AGENTS.md](AGENTS.md) for what it does.

The catalog covers skills written here plus a curated set of external ones (Swift, React/TypeScript, Chrome extensions, general engineering practices and more). External skills are fetched from their authors' repos, not copied here. They are listed in [external-skills.json](external-skills.json).

## Catalog

Skills written in this repo:

| Skill | Category | What it does |
| --- | --- | --- |
| [swift-clean-architecture](skills/languages/swift/swift-clean-architecture) | Swift | Views, view models, use cases, repositories, data sources, entities, DTOs |
| [typescript-conventions](skills/languages/javascript/typescript-conventions) | JavaScript | Strict TypeScript, modules, error handling and tooling |
| [mv3-extension-development](skills/platforms/chrome-extensions/mv3-extension-development) | Chrome extensions | Manifest V3 architecture, service workers, messaging, storage |
| [extension-security-and-publishing](skills/platforms/chrome-extensions/extension-security-and-publishing) | Chrome extensions | Least-privilege permissions, CSP and Chrome Web Store review |
| [dev-workflow](skills/workflow/dev-workflow) | Workflow | Phases with gates, grill-me before building, PR and exam before done |
| [create-pull-request](skills/workflow/create-pull-request) | Workflow | Preflight, PR description template, draft PR via gh |
| [understanding-exam](skills/workflow/understanding-exam) | Workflow | Exam for the engineer on the issue and solution |
| [software-testing-fundamentals](skills/testing/software-testing-fundamentals) | Testing | Black-box, white-box, coverage, test levels, mutation testing |
| [adr-writing](skills/system-design/adr-writing) | System design | Write and review architecture decision records |
| [github-actions-ci](skills/devops/github-actions-ci) | DevOps | Fast, secure GitHub Actions pipelines |

Curated external skills: [Workflow](skills/workflow/README.md), [Swift](skills/languages/swift/README.md), [JavaScript](skills/languages/javascript/README.md), [Chrome extensions](skills/platforms/chrome-extensions/README.md). Those skills are maintained by others, so they are linked rather than copied.

Planned categories: mobile, testing, security, design, AI engineering, git workflow. See [skills/](skills).

## Install by hand

```bash
git clone https://github.com/rubenmfdev/ai-engineer-skills.git
cd ai-engineer-skills

python3 scripts/install.py --list                              # browse everything
python3 scripts/install.py --category swift                    # default Swift skills -> ~/.claude/skills
python3 scripts/install.py --category swift --topic security,accessibility --project
python3 scripts/install.py --only swift-clean-architecture,adr-writing --copy
python3 scripts/install.py --category swift --all              # also optional and alternative skills
python3 scripts/install.py --category swift --dry-run          # preview only
```

`--project` installs into `./.claude/skills` of the current directory (or use `--project-dir DIR`). `--dest <dir>` targets other agents that read `SKILL.md` folders.

## Repository layout

```
skills/<category>/[<group>/]<skill>/SKILL.md   # one folder per skill (our own)
external-skills.json                            # curated third-party skills
AGENTS.md                                       # instructions for agents using this repo
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
