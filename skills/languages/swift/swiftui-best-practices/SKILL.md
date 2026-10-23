---
name: swiftui-best-practices
description: Guidance for writing and reviewing SwiftUI code covering state management, view composition, navigation, lists and performance. Use when building SwiftUI views, choosing between @State, @Binding, @Observable and @Environment, or fixing slow or over-redrawing views.
---

# SwiftUI Best Practices

Targets iOS 17+ / Swift 5.9+ (Observation framework). For older deployment targets, see the fallback notes in each section.

## State: pick the narrowest tool
| Need | Use |
| --- | --- |
| Local value owned by one view | `@State` |
| Child edits parent's value | `@Binding` |
| Reference-type model owned by a view | `@State` holding an `@Observable` class |
| Shared model injected from above | `@Environment(Model.self)` |
| Child reads a model but does not own it | plain `let` or `@Bindable` when it needs bindings |

- Prefer `@Observable` over `ObservableObject`. It tracks per-property reads, so fewer redraws. Pre-iOS 17 fall back to `ObservableObject` with `@StateObject` (owner) and `@ObservedObject` (non-owner).
- Mark `@State` properties `private`. If a parent must set them, it should be a parameter instead.
- Never create a model in `body` or in an initializer of a non-owning view. Ownership belongs in `@State` or the app root.

## View composition
- Keep `body` small and declarative. Extract subviews as separate `View` structs, not computed properties, so SwiftUI can skip them when inputs are unchanged.
- Pass only the data a subview needs, not the whole model. Narrow inputs mean fewer invalidations.
- Move logic out of `body`: formatting, filtering and sorting belong in the model or a computed property on it, not recomputed per render.
- Use `ViewModifier` or `View` extensions for repeated styling instead of copy-pasting modifier chains.

## Lists and identity
- Give `ForEach` and `List` stable identity: `Identifiable` models with a persistent `id`, never `\.self` on mutable values or array indices.
- Use `LazyVStack` inside `ScrollView` for long content. A plain `VStack` builds everything up front.
- Avoid `AnyView`. It erases type information and defeats diffing. Prefer `@ViewBuilder`, `Group` or generics.

## Navigation
- Use `NavigationStack` with a typed path and `navigationDestination(for:)`. `NavigationView` is deprecated.
- Keep the path in a model (`@Observable` router) when navigation must be driven from outside views or restored.
- Present sheets with `.sheet(item:)` over `.sheet(isPresented:)` when the content depends on data.

## Side effects and async
- Use `.task { }` (auto-cancelled with the view) instead of `onAppear` plus a manual `Task`.
- Use `.task(id: value)` to re-run when an input changes.
- Do not mutate state from `body`. Do it in actions, `.task`, or `.onChange`.

## Performance checklist
1. Is the view's input narrower than the model it receives?
2. Are identities stable?
3. Is heavy work (parsing, sorting, image decoding) off `body` and off the main actor?
4. Check redraws with `Self._printChanges()` temporarily, or Instruments' SwiftUI template.

## Previews
Give every non-trivial view a `#Preview` with realistic sample data and at least one edge case (empty, long text, error).
