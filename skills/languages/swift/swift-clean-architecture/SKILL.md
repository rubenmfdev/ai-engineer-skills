---
name: swift-clean-architecture
description: Structure Swift and SwiftUI apps with Clean Architecture covering views, view models, use cases, repositories, data sources, entities, DTOs and mappers, plus dependency rules, folder layout and testing. Use when designing app architecture, deciding where code belongs, splitting a massive view model, or reviewing layer boundaries in an iOS or macOS project.
---

# Clean Architecture for Swift

Three layers with one rule: **dependencies point inward**. Presentation and Data depend on Domain. Domain depends on nothing (no SwiftUI, no networking, no persistence frameworks).

```
Presentation  ->  Domain  <-  Data
(View, ViewModel)  (Entity, UseCase,    (RepositoryImpl, DataSource,
                    Repository protocol)  DTO, Mapper)
```

## Where does each thing go?
| Piece | Layer | Responsibility | Must not |
| --- | --- | --- | --- |
| **View** | Presentation | Render state, forward user actions | Contain business logic or call repositories |
| **ViewModel** | Presentation | Hold UI state, call use cases, map results to display models | Import networking or persistence, know DTOs |
| **Entity** | Domain | Plain business model and rules (`struct`) | Conform to `Codable` for an API, import UIKit/SwiftUI |
| **UseCase** | Domain | One business action (`GetOrdersUseCase`) | Know about UI or storage |
| **Repository protocol** | Domain | Describes the data the domain needs, in entities | Expose DTOs or framework types |
| **RepositoryImpl** | Data | Implements the protocol, picks and combines data sources, maps DTO to Entity | Be referenced by Presentation or Domain directly |
| **DataSource** | Data | One source of truth access (remote API, local DB, cache, Keychain) | Contain business rules |
| **DTO** | Data | Shape of the wire or DB format (`Codable`) | Leak outside Data |
| **Mapper** | Data (DTO to Entity), Presentation (Entity to display model) | Translate between models | Contain side effects |

## Rules
1. **Domain is pure Swift.** It should compile in a package that imports only `Foundation`.
2. **Repository protocols live in Domain, implementations in Data.** This is dependency inversion, and what makes everything testable.
3. **One use case, one job**, exposed as `func execute(...) async throws -> Entity` (or `callAsFunction`). Skip a use case when it would only forward a call and has no logic. Letting the view model call the repository for trivial reads is acceptable if the team agrees and is consistent.
4. **ViewModels talk to use cases**, never to DTOs, `URLSession`, or Core Data/SwiftData types.
5. **DTOs never cross the Data boundary.** Map to entities inside the repository implementation.
6. **Errors:** DataSources throw technical errors. Repository implementations translate them to domain errors (`enum OrderError`). ViewModels translate domain errors to user messages.
7. **Dependency injection at the composition root** (app entry or a `DIContainer`). No singletons or `Type.shared` reached from inside layers. Inject protocols through initializers.
8. **Concurrency:** ViewModels are `@MainActor`. Use cases, repositories and data sources are `Sendable` and nonisolated `async`. Entities and DTOs are `Sendable` value types.
9. **Models per layer.** Resist reusing one model everywhere. The mapping cost is the price of decoupling. If DTO equals Entity today, keep two types anyway when the API is outside your control.

## ViewModel shape
```swift
@MainActor @Observable
final class OrdersViewModel {
    enum State { case idle, loading, loaded([OrderRow]), failed(String) }
    private(set) var state: State = .idle
    private let getOrders: GetOrdersUseCase

    init(getOrders: GetOrdersUseCase) { self.getOrders = getOrders }

    func load() async {
        state = .loading
        do { state = .loaded(try await getOrders().map(OrderRow.init)) }
        catch { state = .failed(Self.message(for: error)) }
    }
}
```
Model screen state as one enum or struct, not many booleans. Views switch over it.

## Folder layout
Group by **feature first**, layer second, so a feature can be lifted out:
```
App/                 composition root, DI container
Core/                shared utilities, networking client, design system
Features/
  Orders/
    Presentation/    OrdersView, OrdersViewModel, OrderRow
    Domain/          Order, GetOrdersUseCase, OrderRepository (protocol)
    Data/            OrderRepositoryImpl, OrderRemoteDataSource, OrderDTO, OrderMapper
```
For larger apps enforce the dependency rule with the compiler: one Swift Package target per layer (or per feature and layer), with `Domain` having no dependencies. See [references/example.md](references/example.md) for a full vertical slice and a Package.swift sketch.

## Testing by layer
| Layer | Test with |
| --- | --- |
| Domain (use cases, entities) | Fast unit tests with fake repositories |
| Data | RepositoryImpl with stub data sources; mappers with fixtures; data sources against a mocked `URLProtocol` or in-memory store |
| Presentation | ViewModel tests with fake use cases, assert state transitions |
| Views | Previews and a few UI/snapshot tests |

Use Swift Testing (`@Test`, `#expect`) for new tests.

## Review checklist
- Does any `import` in Domain bring in SwiftUI, UIKit, CoreData, SwiftData, or networking?
- Does any view or view model reference a DTO or `RepositoryImpl`?
- Is any `Codable` DTO used as a UI model?
- Are dependencies injected through initializers as protocols?
- Is business logic hiding in a view, a view model, or a data source?
- Is every use case doing real work, or is it ceremony?

## When not to go this far
Small apps and prototypes: a View, a `@Observable` model, and one service is enough. Introduce use cases and separate DTOs when logic is reused across screens, the backend is unstable, or several people work in parallel.

## See also
- Broader architecture pattern catalog (MVVM, MVI, TCA, VIPER): https://github.com/efremidze/swift-architecture-skill
- SwiftUI and Swift Concurrency specifics: see [skills/languages/swift](../../README.md) for curated skills.
