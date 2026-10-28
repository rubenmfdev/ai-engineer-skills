---
name: swift-clean-architecture
description: Structure Swift and SwiftUI apps with Clean Architecture covering views, view models, use cases, repositories, data sources, entities, DTOs and mappers, plus dependency rules, folder layout and testing. Use when designing app architecture, deciding where code belongs, splitting a massive view model, or reviewing layer boundaries in an iOS or macOS project.
---

# Clean Architecture for Swift

Three layers with one rule: **dependencies point inward**. Presentation and Data depend on Domain. Domain depends on nothing (no SwiftUI, no networking, no persistence frameworks).

```
Presentation  ->  Domain  <-  Data
(View, ViewModel)  (Entity, UseCase,    (DataRepository, DataSource,
                    Repository protocol)  DTO, Mapper)
```

## Where does each thing go?
| Piece | Layer | Responsibility | Must not |
| --- | --- | --- | --- |
| **View** | Presentation | Render state, forward user actions | Contain business logic or call repositories |
| **ViewModel** | Presentation | Hold UI state, call use cases through their `UseCaseType` protocols, map results to display models | Import networking or persistence, know DTOs |
| **Entity** | Domain | Plain business model and rules (`struct`) | Conform to `Codable` for an API, import UIKit/SwiftUI |
| **UseCaseType** | Domain | Protocol of one use case (`GetOrdersUseCaseType`) with its single `execute` method. What view models depend on, so tests can fake it | Have more than one method |
| **UseCase** | Domain | One business action, named `<Verb><Noun>UseCase` (`GetOrdersUseCase`), conforming to its `UseCaseType`. Depends only on repository protocols and other use case types | Know about UI, data sources, SDK clients (analytics, clipboard, URL opening...) or storage |
| **Repository protocol** | Domain | Describes the data the domain needs, in entities | Expose DTOs or framework types |
| **DataRepository** | Data | The one implementation of the repository protocol (`OrderDataRepository`). Picks and combines data sources behind protocols, maps DTO to Entity, translates errors | Import a persistence or networking framework, touch `ModelContext`/`NSManagedObjectContext`/`URLSession`, or be referenced by Presentation or Domain directly |
| **DataSource** | Data | Access to one source of truth (remote API, SwiftData/Core Data, cache, Keychain) behind a `<Name>DataSource` protocol. The only place that imports the framework. Returns and accepts DTOs | Contain business rules or return framework types (`@Model`, `NSManagedObject`) |
| **DTO** | Data | Shape of the wire or DB format (`Codable`) | Leak outside Data |
| **Mapper** | Data (DTO to Entity), Presentation (Entity to display model) | Translate between models | Contain side effects |

## Rules
1. **Domain is pure Swift.** It should compile in a package that imports only `Foundation`.
2. **Repository protocols live in Domain, implementations in Data.** This is dependency inversion, and what makes everything testable.
   - There is **exactly one** `DataRepository` per repository protocol (test fakes aside). Never write `SwiftDataOrderRepository` next to `RemoteOrderRepository`.
   - Variation lives in **DataSources**: `SwiftDataOrderDataSource`, `URLSessionOrderRemoteDataSource`, `InMemoryOrderDataSource`... each conforming to a `<Name>DataSource` protocol. The `DataRepository` is given the data sources it needs (one, or remote plus local cache) and decides how to combine them.
   - The `DataRepository` file imports only `Foundation`. All framework code (`import SwiftData`, `ModelContext`, `FetchDescriptor`, `import CoreData`, `URLSession`) is inside a DataSource.
3. **Use cases follow strict conventions:**
   - **Naming:** every use case is `<Verb><Noun>UseCase` (`GetOrdersUseCase`, `PlaceOrderUseCase`) and conforms to a `<Verb><Noun>UseCaseType` protocol declared next to it. View models hold `any GetOrdersUseCaseType`, never the concrete type.
   - **One public method, always `execute`.** Not `callAsFunction`, not `run`, not several methods. Helpers are `private`. One use case, one job.
   - **Parameters:** `execute` takes at most 2 parameters. With more than 2, create a `<Verb><Noun>UseCaseInput` struct (`PlaceOrderUseCaseInput`) and take that single value.
   - **Dependencies:** a use case holds only **repository protocols** and **other use case types**. Anything else it needs (opening URLs, clipboard, analytics, SDKs) is wrapped behind a repository, or stays out of the use case.
   - Do not create a use case that would only forward a call and has no logic; agree as a team how view models read trivial data and stay consistent.
4. **ViewModels talk to use cases** (through their `UseCaseType` protocols), never to DTOs, `URLSession`, or Core Data/SwiftData types.
5. **DTOs never cross the Data boundary.** Map to entities inside the `DataRepository`. Persistence models (`@Model` classes, `NSManagedObject`) are DTO-like and not `Sendable`: the DataSource maps them to plain `Sendable` DTO structs, so even the DataRepository never sees them.
6. **Errors:** DataSources throw technical errors. The `DataRepository` translates them to domain errors (`enum OrderError`). ViewModels translate domain errors to user messages.
7. **Dependency injection at the composition root** (app entry or a `DIContainer`). No singletons or `Type.shared` reached from inside layers. Inject protocols through initializers.
8. **Concurrency:** ViewModels are `@MainActor`. Use cases, repositories and data sources are `Sendable` and nonisolated `async`. Entities and DTOs are `Sendable` value types.
9. **Models per layer.** Resist reusing one model everywhere. The mapping cost is the price of decoupling. If DTO equals Entity today, keep two types anyway when the API is outside your control.

## ViewModel shape
```swift
@MainActor @Observable
final class OrdersViewModel {
    enum State { case idle, loading, loaded([OrderRow]), failed(String) }
    private(set) var state: State = .idle
    private let getOrders: any GetOrdersUseCaseType

    init(getOrders: any GetOrdersUseCaseType) { self.getOrders = getOrders }

    func load() async {
        state = .loading
        do { state = .loaded(try await getOrders.execute().map(OrderRow.init)) }
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
    Domain/          Order, GetOrdersUseCase, GetOrdersUseCaseType, OrderRepository (protocol)
    Data/            OrderDataRepository, OrderRemoteDataSource (protocol), URLSessionOrderRemoteDataSource, OrderDTO, OrderMapper
```
For larger apps enforce the dependency rule with the compiler: one Swift Package target per layer (or per feature and layer), with `Domain` having no dependencies. See [references/example.md](references/example.md) for a full vertical slice and a Package.swift sketch.

## Testing by layer
| Layer | Test with |
| --- | --- |
| Domain (use cases, entities) | Fast unit tests with fake repositories (and fake use case types for use cases that call other use cases) |
| Data | `DataRepository` with stub data sources; mappers with fixtures; data sources against a mocked `URLProtocol` or in-memory store |
| Presentation | ViewModel tests with fake `UseCaseType` conformers, assert state transitions |
| Views | Previews and a few UI/snapshot tests |

Use Swift Testing (`@Test`, `#expect`) for new tests.

## Review checklist
- Does any `import` in Domain bring in SwiftUI, UIKit, CoreData, SwiftData, or networking?
- Does any view or view model reference a DTO or the `DataRepository`?
- Does a `DataRepository` import SwiftData, Core Data or another framework, or is there more than one implementation of one repository protocol? Move the framework code into a DataSource.
- Is any `Codable` DTO used as a UI model?
- Are dependencies injected through initializers as protocols?
- Is business logic hiding in a view, a view model, or a data source?
- Is every use case doing real work, or is it ceremony?
- Does every use case have a `UseCaseType` protocol, one public `execute`, at most 2 parameters (else a `UseCaseInput` struct), and only repositories or other use cases as dependencies?

## When not to go this far
Small apps and prototypes: a View, a `@Observable` model, and one service is enough. Introduce use cases and separate DTOs when logic is reused across screens, the backend is unstable, or several people work in parallel.

## See also
- Broader architecture pattern catalog (MVVM, MVI, TCA, VIPER): https://github.com/efremidze/swift-architecture-skill
- SwiftUI and Swift Concurrency specifics: see [skills/languages/swift](../../README.md) for curated skills.
