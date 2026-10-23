# Commands by tool

Prefer `npx`/`bunx`/`pnpm exec` or the project's script runner so the project's pinned version is used. Check `--help` for your version, flags change.

## Changed files
```bash
git diff --name-only --diff-filter=ACMR HEAD            # modified, uncommitted
git diff --name-only --diff-filter=ACMR <base>...HEAD   # whole branch
git ls-files --others --exclude-standard                # untracked
```

## Swift
```bash
swiftlint lint --strict <paths>        # warnings fail
swiftlint lint --fix <paths>           # safe autocorrect (older versions: swiftlint autocorrect)
swiftlint rules <rule_id>              # explain a rule
swift format lint -r Sources Tests     # swift-format (Swift 6 toolchain)
swift format -i -r Sources Tests
swiftformat . --lint                   # SwiftFormat (Nick Lockwood)
swiftformat <paths>
```
Xcode build warnings: `xcodebuild ... 2>&1 | grep -E "warning:|error:"`.

## JavaScript / TypeScript
```bash
npx eslint <files>                     # add --max-warnings 0 to fail on warnings
npx eslint --fix <files>
npx eslint --print-config <file>       # which rules apply
npx prettier --check <files>
npx prettier --write <files>
npx biome check <paths>                # lint + format + import order
npx biome check --write <paths>        # safe fixes (--unsafe for unsafe ones)
npx biome explain <rule>
npx biome ci .                         # CI mode, no writes
npx tsc --noEmit                       # type check
```

## Python
```bash
ruff check <paths>
ruff check --fix <paths>
ruff format --check <paths>
ruff format <paths>
ruff rule <CODE>                       # explain a rule
mypy <paths>      # or: pyright
```

## Go
```bash
gofmt -l .            # lists unformatted files
gofmt -w <files>
go vet ./...
golangci-lint run ./...
```

## Rust
```bash
cargo fmt --check
cargo fmt
cargo clippy --all-targets -- -D warnings
```

## Kotlin / JVM
```bash
./gradlew ktlintCheck detekt
./gradlew ktlintFormat
```

## Other files
```bash
shellcheck script.sh
hadolint Dockerfile
actionlint                             # GitHub Actions workflows
markdownlint "**/*.md"
yamllint .
```

## pre-commit
```bash
pre-commit run --files $(git diff --name-only HEAD)
pre-commit run --all-files
```
