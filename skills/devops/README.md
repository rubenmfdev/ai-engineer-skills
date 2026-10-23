# DevOps

Our skill: [github-actions-ci](github-actions-ci).

Curated external skills (category `devops` in [external-skills.json](../../external-skills.json)). Defaults are the broadly useful ones. Install by topic so you only get what the project uses.

| Topic | Skills | Default |
| --- | --- | --- |
| docker | `docker-project-foundations`, `docker-build-strategies`, `docker-destructive-guardrails` ([docker/skills](https://github.com/docker/skills), official) | yes |
| | `docker-compose-patterns`, `dockerfile-validator` | optional |
| terraform | `terraform-style-guide` ([HashiCorp](https://github.com/hashicorp/agent-skills), official, MPL-2.0) | yes |
| | `terraform-test`, `refactor-module`, `terrashark`, `terraform-skill` | optional |
| kubernetes | `kubernetes-skill` (failure-mode workflow, MIT) | yes |
| | `k8s-debug`, `k8s-security-policies`, `gitops-workflow`, `helm-chart-scaffolding` | optional |
| ci | `secrets-management` | yes |
| | `deployment-pipeline-design`, `github-actions-templates`, `github-actions-validator` | optional |
| observability | `sre-engineer`, `monitoring-expert`, `slo-implementation`, `distributed-tracing`, `observability-and-instrumentation` | optional |
| incident | `postmortem-writing`, `incident-runbook-templates` | optional |
| cost | `cost-optimization` | optional |

Notes: `terraform-skill` (antonbabenko) has a license file the host does not recognize, so check it. The Docker, Terraform and Kubernetes skills are young, so test them on a non-production setup first.

```bash
python3 scripts/install.py --category devops --topic docker,ci --project
```
