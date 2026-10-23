---
name: github-actions-ci
description: Design fast and secure GitHub Actions workflows covering triggers, caching, matrices, permissions, pinned actions, secrets and releases. Use when creating or reviewing .github/workflows files, speeding up CI, or hardening a pipeline.
---

# GitHub Actions CI

## Security first
- Set least-privilege token permissions at the top, then raise per job:
  ```yaml
  permissions:
    contents: read
  ```
- Pin third-party actions to a full commit SHA (add a version comment). Tags can be moved.
- Never interpolate untrusted input (`github.event.pull_request.title`, branch names, issue bodies) directly into `run:`. Pass it through `env:` and quote the variable.
- Use `pull_request`, not `pull_request_target`, for untrusted code. If you need `pull_request_target`, never check out or run the PR's code with secrets present.
- Prefer OIDC to cloud providers over long-lived secrets.
- Scope secrets to environments with required reviewers for deploys.

## Speed
- Cache dependencies with the built-in setup action option (`cache: npm`, `cache: pip`, Gradle/Swift package caches) keyed on lockfiles.
- Cancel superseded runs:
  ```yaml
  concurrency:
    group: ${{ github.workflow }}-${{ github.ref }}
    cancel-in-progress: true
  ```
- Run lint, typecheck and unit tests as parallel jobs. Gate slower jobs with `needs:`.
- Use `paths:` filters or a changed-files step so docs-only changes skip heavy jobs.
- Use matrices for OS/language versions, with `fail-fast: false` when you want the full picture.
- Set `timeout-minutes` on every job.

## Structure
- Reusable logic goes in reusable workflows (`workflow_call`) or composite actions, not copy-paste.
- One workflow per concern: `ci.yml` (tests), `release.yml` (tags), `deploy.yml` (environments).
- Make required checks stable: a single aggregate job that `needs` the rest is easier to mark required.

## Release
- Trigger on tags (`v*`), build once, upload artifacts, and publish from that artifact.
- Generate changelogs from conventional commits or PR labels.
- Sign and attach provenance (`actions/attest-build-provenance`) for distributed binaries.

## Example
```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version-file: .nvmrc
          cache: npm
      - run: npm ci
      - run: npm run lint && npm test
```
(Replace tags with pinned SHAs in real repos.)

## Debug tips
- Re-run with debug logging (`ACTIONS_STEP_DEBUG`).
- Use `act` for quick local checks, then confirm on GitHub.
- Print context with `toJSON(github)` in a throwaway step when a condition misbehaves.
