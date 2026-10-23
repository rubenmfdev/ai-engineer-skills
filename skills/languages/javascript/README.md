# JavaScript / TypeScript

Original skill here: [typescript-conventions](typescript-conventions).

Curated external skills (all in [external-skills.json](../../../external-skills.json), category `javascript`). Read a skill before using it.

| Skill | Author | Topic | Default | Notes |
| --- | --- | --- | --- | --- |
| [vercel-react-best-practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices) | Vercel | react | yes | React/Next.js performance rules. Repo has no license file |
| [vercel-composition-patterns](https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns) | Vercel | react | yes | Compound components, avoiding boolean-prop sprawl |
| [web-design-guidelines](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines) | Vercel | design | yes | Reviews UI against Web Interface Guidelines |
| [typescript-pro](https://github.com/Jeffallan/claude-skills/tree/main/skills/typescript-pro) | Jeffallan | language | yes | Advanced types, generics, tRPC |
| [javascript-pro](https://github.com/Jeffallan/claude-skills/tree/main/skills/javascript-pro) | Jeffallan | language | yes | Modern ES, async, ESM, Node |
| [frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | Anthropic | design | yes | Distinctive visual design, avoids templated UI. Apache-2.0 |
| [webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | Anthropic | testing | yes | Playwright against local apps. Apache-2.0 |
| [frontend-ui-engineering](https://github.com/addyosmani/agent-skills/tree/main/skills/frontend-ui-engineering) | Addy Osmani | ui | yes | Accessible, responsive production UI |
| react-expert, nextjs-developer, playwright-expert, test-master | Jeffallan | various | optional | Alternatives or extras |
| [mcp-builder](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) | Anthropic | ai | optional | Build MCP servers |
| vercel-react-native-skills | Vercel | react-native | optional | React Native and Expo |
| [browser-testing-with-devtools](https://github.com/addyosmani/agent-skills/tree/main/skills/browser-testing-with-devtools) | Addy Osmani | testing | optional | Needs Chrome DevTools MCP |

Cross-language engineering skills (TDD, security, code review, git, docs, CI/CD) are in category `general`, from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills).

```bash
python3 scripts/install.py --category javascript,general --project
```
