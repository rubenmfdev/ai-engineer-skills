---
name: create-pull-request
description: Prepare and open a high-quality pull request with preflight checks, a clear description (problem, approach, testing evidence, risk, review guide) and a draft PR via the gh CLI. Use when work is ready for review, when the user says "open a PR" or "create a pull request", or in the validation phase of dev-workflow.
---

# Create Pull Request

## 1. Preflight
Run and read the output of each:
```bash
git status --short
git diff --stat <base>...HEAD
git log --oneline <base>..HEAD
```
- Find the base branch (`git symbolic-ref refs/remotes/origin/HEAD`). Do not assume `main`.
- Look for files that do not belong: debug code, `.env`, secrets, build output, unrelated formatting. Remove them.
- Run the project's build, lint (`run-linter`) and tests. Keep the exact commands and results for the description. If anything fails, stop and report. Do not open a PR over red checks unless the user says so.
- Read your own diff as a reviewer would. Fix what you would flag.
- If the diff is much more than about 400 changed lines or mixes concerns, propose splitting it.

## 2. Branch and commits
- Branch name: follow the repo's convention, else `<type>/<short-topic>` (`fix/login-timeout`).
- Commit messages: match the style in `git log` (conventional commits if the repo uses them). One logical change per commit.
- Follow any attribution rules from the user, `CLAUDE.md` or `AGENTS.md`.

## 3. Ask before publishing
Pushing and opening a PR are visible to others. If the user has not asked for it in this conversation, show the title and description and ask first.

## 4. Description
Write it for a reviewer who has not seen the conversation. Keep prose short. Use this template:

```markdown
## Summary
What changed and why, in 2 to 4 lines. Link the issue: Closes #123.

## Context
The problem or need. Root cause for bugs.

## Approach
What you did and the key decisions. Alternatives considered and why rejected.

## Changes
- Area A: ...
- Area B: ...

## Testing
- Commands run and results (`npm test`: 142 passed)
- New tests: what they cover
- Not tested / known gaps: ...

## Risk and rollout
- Blast radius: which users or systems are affected
- Reversible? (one-way or two-way door), migrations, flags, rollback steps

## Review guide
Start with `path/File.swift`. Skim: generated or mechanical files. Scrutinize: the retry logic in `Client.swift`.

## Evidence
Screenshots, before/after output, logs.
```
Drop sections that do not apply. Never invent test results.

## 5. Open it
Write the body to a file, then create a draft so the author can finish validation first:
```bash
git push -u origin HEAD
gh pr create --draft --base <base> --title "<title>" --body-file /tmp/pr-body.md
```
Titles are short and in the imperative, matching repo style. After creating, print the URL.

## 6. After
- Offer the `understanding-exam` so the author confirms they understand the change before marking it ready.
- Mark ready with `gh pr ready` only when the user says so.
- Add reviewers or labels only when asked.
