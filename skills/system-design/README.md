# System design

Our skill: [adr-writing](adr-writing). For specs, see [living-specs](../workflow/living-specs).

Curated external skills (category `system-design` in [external-skills.json](../../external-skills.json)). Read before using.

| Topic | Skills | Default |
| --- | --- | --- |
| architecture | `architecture-patterns` (wshobson: Clean, Hexagonal, DDD) | yes |
| | `architecture-designer` (Jeffallan), `codebase-design`, `improve-codebase-architecture` (Matt Pocock) | optional |
| api | `api-design-principles` (wshobson: REST and GraphQL) | yes |
| | `api-designer` (Jeffallan), `api-and-interface-design` (Addy Osmani) | optional |
| distributed | `microservices-patterns`, `saga-orchestration`, `microservices-architect` | optional |
| database | `postgresql-table-design`, `sql-optimization-patterns`, `database-optimizer` | optional |
| adr | `architecture-decision-records` (wshobson) | optional, alternative to ours |
| migration, performance | `deprecation-and-migration`, `performance-optimization` (Addy Osmani) | optional |

```bash
python3 scripts/install.py --category system-design --project
python3 scripts/install.py --category system-design --topic database --all --project
```
Gap: a step-by-step "design a system from requirements" skill (requirements, capacity estimates, API, data model, scaling, trade-offs) was not found. Candidate to write here.
