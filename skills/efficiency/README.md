# Efficiency (token usage)

Tools that cut how many tokens an agent spends exploring a codebase. These are **tools**, not skill folders: they are installed with their own commands, and they register a skill in your project. The installer prints the commands and never runs them for you.

## Recommended: Graphify
[Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) (Apache-2.0, 130k+ stars). Builds a knowledge graph of the project (code, docs, schemas, PDFs) that the agent queries instead of grepping through files.

```bash
uv tool install graphifyy        # note the two y's. Needs Python 3.10+ and uv (or pipx)
graphify install --project       # registers the skill in ./.claude/skills
```
Then in the agent: `/graphify .`, followed by `graphify query "how does login work?"`, `graphify path A B`, `graphify explain X`. Output goes to `graphify-out/` (`graph.json`, `GRAPH_REPORT.md`, `graph.html`). Decide whether to commit it or add it to `.gitignore`.

Why this one:
- Code is parsed locally with tree-sitter. No LLM calls, nothing leaves your machine for code.
- Every edge is tagged `EXTRACTED` or `INFERRED`, so you can tell fact from guess.
- Works across 20+ agents and many languages, and ships as a skill.

Caveats:
- Savings depend on the project and on how often the agent actually uses the graph instead of reading files. The headline numbers in the README (and in third-party posts) are the vendors' claims. Measure on your own project.
- The README promotes a paid Graphify Cloud. The local CLI is free.
- Rebuild the graph after big changes, or it goes stale.
- Use the official package `graphifyy`. Other `graphify*` packages on PyPI are not affiliated.

## Other tools worth knowing (not in the catalog)
| Tool | What it saves | Notes |
| --- | --- | --- |
| [rtk-ai/rtk](https://github.com/rtk-ai/rtk) | Output of shell commands (git, test runs) is compressed before the agent sees it | Hook-based, so it needs no agent changes. Two editions (one is Apache-2.0 plus BUSL-1.1, one is Apache-2.0 only). Complements a code graph |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | Output tokens, by making the agent terse | Trades readability for tokens. Conflicts with explanations and the `understanding-exam` |
| [tirth8205/code-review-graph](https://github.com/tirth8205/code-review-graph) | Similar to Graphify, aimed at code review | MIT |

Cheap habits that cost nothing: keep `AGENTS.md` short, point it at an index (like `docs/specs/README.md`) instead of pasting docs, and start fresh sessions for unrelated tasks.
