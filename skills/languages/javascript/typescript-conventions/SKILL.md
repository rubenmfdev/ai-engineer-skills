---
name: typescript-conventions
description: Conventions for writing modern, strictly typed TypeScript and JavaScript covering tsconfig strictness, types, modules, error handling, async code and tooling. Use when starting a TS/JS project, reviewing TypeScript, tightening types, or removing any.
---

# TypeScript Conventions

## Baseline config
Enable in `tsconfig.json`:
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "verbatimModuleSyntax": true,
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "target": "ES2022",
    "skipLibCheck": true
  }
}
```
Use `moduleResolution: "NodeNext"` for Node libraries published to npm.

## Types
- No `any`. Use `unknown` at boundaries and narrow it. If `any` is unavoidable, scope it to one line with a comment.
- Model states with discriminated unions, not optional-field bags:
  ```ts
  type Result<T> = { ok: true; value: T } | { ok: false; error: Error };
  ```
- Prefer `type` for unions and `interface` for object shapes meant to be extended. Be consistent within a project.
- Use `satisfies` to check a literal against a type without widening it.
- Derive types from values (`typeof`, `as const`, `ReturnType`) instead of duplicating them.
- Validate external data (API responses, `JSON.parse`, env vars) at runtime with a schema library such as Zod or Valibot, and infer the TS type from the schema.

## Modules and structure
- ES modules only. Use named exports; avoid default exports so renames are tracked.
- Use `import type` for type-only imports.
- Avoid barrel files (`index.ts` re-exports) in large apps. They hurt tree-shaking and slow builds.
- Keep side effects out of module top level.

## Async and errors
- `async`/`await` over raw promise chains. Always `await` or explicitly `void` a promise; enable `@typescript-eslint/no-floating-promises`.
- Use `Promise.all` for independent work, `Promise.allSettled` when partial failure is acceptable.
- Throw `Error` subclasses with a `cause`: `throw new Error("load failed", { cause: err })`.
- Do not swallow errors in empty `catch`. Log with context or rethrow.
- Pass `AbortSignal` into cancellable work (`fetch`, timers).

## JavaScript habits
- `const` by default, `let` when reassigned, never `var`.
- `===` always. Use `??` and `?.` instead of `||` checks that misfire on `0` or `""`.
- Prefer array methods and `for...of` over index loops. Use `structuredClone` for deep copies.
- Do not mutate function arguments.

## Tooling
- Formatter: Prettier or Biome. Linter: ESLint with `typescript-eslint` (type-checked config) or Biome.
- Run `tsc --noEmit` in CI. Treat type errors as build failures.
- Tests: Vitest or the Node test runner. Keep unit tests next to source as `*.test.ts`.
- Pin the Node version with `.nvmrc` or `engines`, and commit the lockfile.
