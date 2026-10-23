---
name: run-linter
description: Find, run and act on a project's linters, formatters and type checkers correctly. Uses the project's own commands, scopes to changed files, fixes root causes instead of disabling rules, never edits lint config without asking, and reports results with evidence. Use when finishing code, before a commit or PR, when lint, format or type errors appear, when the user says "run the linter", or when setting up linting in a project.
---

# Run the Linter

Linters encode the project's standards. The goal is clean code under the project's rules, not a quiet terminal.

## 1. Find the project's commands
Look in this order and use the first that exists. Prefer the exact command CI runs, so local results match CI.
1. `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README`
2. CI workflows (`.github/workflows/*.yml`), `Makefile`, `justfile`
3. `package.json` scripts (`lint`, `format`, `typecheck`), `pyproject.toml`, `Package.swift` plugins, build scripts
4. `.pre-commit-config.yaml` (run with `pre-commit run --files <files>`)
5. Tool config files (table below)

| Config file | Tool |
| --- | --- |
| `.swiftlint.yml` | SwiftLint |
| `.swiftformat`, `.swift-format` | SwiftFormat, swift-format |
| `eslint.config.*`, `.eslintrc*` | ESLint |
| `.prettierrc*`, `prettier` in `package.json` | Prettier |
| `biome.json` | Biome |
| `tsconfig.json` | TypeScript (`tsc --noEmit`) |
| `ruff.toml`, `[tool.ruff]` in `pyproject.toml` | Ruff |
| `.golangci.yml` | golangci-lint |
| `rustfmt.toml`, `clippy.toml` | rustfmt, clippy |
| `.editorconfig` | formatting rules most editors and tools respect |

Exact flags per tool: [references/commands.md](references/commands.md). If no tool is configured, go to [Setting up linting](#setting-up-linting).

## 2. Run it
1. List what you touched: `git diff --name-only HEAD` plus untracked files.
2. Run the linter on those files first (fast feedback). Before a PR, run the full command CI runs.
3. Read the whole output. Note error and warning counts and which rules fire.
4. Many violations in files you did not touch are **pre-existing**. Do not fix them in this change. Mention them.

## 3. Fix, in this order
1. **Formatter first**, on touched files only (Prettier, `swift format`, `ruff format`, `gofmt`). Formatting noise is then out of the way.
2. **Safe autofix** on touched files (`eslint --fix`, `ruff check --fix`, `swiftlint --fix`, `biome check --write`). Read the diff afterwards. Autofix can change behavior.
3. **Manual fixes.** Understand the rule (`ruff rule <code>`, `swiftlint rules <id>`, `biome explain <rule>`, the ESLint rule page) and fix the cause. A rule usually points at a real smell: unused value, force unwrap, missing await, shadowed variable.
4. Unsafe fixes (`--unsafe-fixes`, `--unsafe`) only when you can say why they are safe, and then run the tests.
5. Re-run until clean on the touched files.

## 4. Never do these
- Disable a rule to make an error go away: `// swiftlint:disable all`, `/* eslint-disable */` at file top, `# noqa` with no code, `@ts-ignore`, `# type: ignore` with no reason.
- Edit lint config, thresholds, ignore lists or CI lint steps to make code pass.
- Run an auto-fixer or formatter over the whole repo unprompted. It buries the real change in a huge diff.
- Mix unrelated reformatting into the change.
- Skip hooks (`--no-verify`).

Allowed exception: a **targeted suppression** when the rule is wrong for that one line. It must name the rule, sit on that line or block only, carry a short reason, and be listed in your report: `// swiftlint:disable:next force_cast - bridged Objective-C API returns Any`. If a rule is wrong for the project, propose a config change to the engineer as a separate change.

## 5. Verify and report
Re-run the same command and show the result. Report:
- Command(s) run
- Before and after counts (errors, warnings)
- Auto-fixes applied (and that you reviewed them)
- Suppressions added (should be none, or listed with reasons)
- Pre-existing issues left alone
- Tests re-run if a fix touched logic

Do not claim "lint passes" without having run it in this session.

## Setting up linting
Only when asked, or after asking. Propose the smallest sensible setup and match the ecosystem:

| Ecosystem | Reasonable start |
| --- | --- |
| TypeScript / JavaScript | Biome, or ESLint with `typescript-eslint` plus Prettier, and `tsc --noEmit` |
| Swift | SwiftLint plus swift-format or SwiftFormat |
| Python | Ruff (lint and format) plus mypy or pyright |
| Go | `gofmt`, `go vet`, golangci-lint |
| Rust | `cargo fmt`, `cargo clippy -- -D warnings` |
| Shell, Docker, CI files | shellcheck, hadolint, actionlint |

Steps: add the config with recommended rules, fix or baseline existing violations in a separate change, add the command to CI and (optionally) a pre-commit hook, document the command in `AGENTS.md`.

## Legacy code with thousands of violations
Do not fix everything. Use the tool's baseline or bulk-suppression feature (SwiftLint baseline, ESLint bulk suppressions in recent versions, `ruff --add-noqa`; check your tool version) in a dedicated commit, so new code is held to the standard and old code is cleaned up gradually.

## Compiler and type warnings
Treat compiler warnings (Xcode, `tsc`, `cargo`) like lint. New warnings are not acceptable. CI should fail on them (`--strict`, `--max-warnings 0`, `-D warnings`).

## Works with
`dev-workflow` (implementation and testing gates), `create-pull-request` (preflight), `verification-before-completion`. For tool-specific depth see the curated linter skills in `external-skills.json` (topic `linting`).
