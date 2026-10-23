---
name: swift-concurrency
description: Guidance for Swift concurrency with async/await, actors, structured concurrency, Sendable and migrating to Swift 6 strict concurrency. Use when writing async Swift code, fixing data-race or Sendable warnings, choosing between actors and @MainActor, or adopting Swift 6 language mode.
---

# Swift Concurrency

## Mental model
- `async` marks a suspension point, not a thread. Code after `await` may resume on a different thread unless isolated to an actor.
- Isolation is the unit of safety. Data is safe when it is either immutable, `Sendable`, or isolated to one actor.

## Defaults
1. Mark UI-facing types `@MainActor`. Do not sprinkle `DispatchQueue.main.async`.
2. Prefer structured concurrency (`async let`, `TaskGroup`) over unstructured `Task { }`. Children are cancelled and awaited automatically.
3. Use an `actor` for shared mutable state accessed from many contexts. Use a class with `@MainActor` when that state is UI state.
4. Prefer value types (`struct`, `enum`) for data crossing isolation boundaries. They are implicitly `Sendable` when their members are.

## Tasks
- `Task { }` inherits the current actor and priority. `Task.detached` does not, so use it rarely and say why.
- Always handle cancellation in long work: check `try Task.checkCancellation()` or `Task.isCancelled` between steps.
- Store a `Task` handle only when you must cancel it. Cancel in `deinit` or on state change.
- In SwiftUI prefer `.task { }` which cancels with the view.

## Parallel work
```swift
async let a = fetchA()
async let b = fetchB()
let (x, y) = try await (a, b)
```
Use `withThrowingTaskGroup` for dynamic counts. Bound concurrency for large fans-out (add tasks in batches) to avoid flooding the network or CPU.

## Sendable
- Fix Sendable errors by making the type a value type, making it an actor, or isolating it to `@MainActor`, in that order.
- `final class` with only `let` constants of Sendable types can be `Sendable`.
- `@unchecked Sendable` is a promise you must back with a lock. Leave a comment naming the lock. Never use it just to silence warnings.
- Closures that cross isolation must be `@Sendable`. Capture values, not mutable `self`.

## Bridging old APIs
- Completion handlers: wrap with `withCheckedThrowingContinuation` and resume **exactly once** on every path.
- Delegates and notifications: expose as `AsyncStream`; call `continuation.finish()` and set `onTermination` for cleanup.

## Swift 6 migration path
1. Turn on `-strict-concurrency=targeted`, fix warnings.
2. Move to `complete`, fix module by module starting with leaf modules.
3. Switch the language mode to 6 per target once warning-free.
4. Re-check global and static mutable variables: make them `let`, isolate them, or wrap in an actor.

## Pitfalls
- Actor reentrancy: state can change across an `await` inside an actor method. Re-validate assumptions after suspending.
- Blocking the main actor with synchronous work. Move heavy computation to a nonisolated `async` function.
- Using `Task.sleep` for synchronization. Use proper signals instead.
