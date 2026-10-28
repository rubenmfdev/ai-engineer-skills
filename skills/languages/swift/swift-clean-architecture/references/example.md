# Example vertical slice: Orders

## Domain
```swift
// Entity (every Domain data object ends in Entity; one type per file)
struct OrderEntity: Identifiable, Equatable, Sendable {
    let id: String
    let total: Decimal
    let placedAt: Date
    let status: Status
    enum Status: Sendable { case pending, shipped, delivered, cancelled }
}

enum OrderError: Error, Sendable { case offline, notFound, unknown }

// Repository protocol (owned by Domain)
protocol OrderRepository: Sendable {
    func orders() async throws -> [OrderEntity]
}

// Use case type: what view models depend on (and tests fake)
protocol GetOrdersUseCaseType: Sendable {
    func execute() async throws -> [OrderEntity]
}

// Use case: one public method, `execute`; depends only on repositories or other use cases
struct GetOrdersUseCase: GetOrdersUseCaseType {
    let repository: OrderRepository
    func execute() async throws -> [OrderEntity] {
        try await repository.orders().sorted { $0.placedAt > $1.placedAt }
    }
}

// With more than 2 parameters, take a single input struct
struct PlaceOrderUseCaseInput: Sendable {
    let productID: String
    let quantity: Int
    let couponCode: String?
}

protocol PlaceOrderUseCaseType: Sendable {
    func execute(_ input: PlaceOrderUseCaseInput) async throws -> OrderEntity
}
```

## Data
```swift
// DTO (every Data layer data object ends in DTO): matches the API, stays inside Data
struct OrderDTO: Decodable, Sendable {
    let id: String
    let total_cents: Int
    let placed_at: Date
    let status: String
}

// Mapper
enum OrderMapper {
    static func map(_ dto: OrderDTO) -> OrderEntity {
        OrderEntity(
            id: dto.id,
            total: Decimal(dto.total_cents) / 100,
            placedAt: dto.placed_at,
            status: OrderEntity.Status(rawValue: dto.status) ?? .pending
        )
    }
}
private extension OrderEntity.Status {
    init?(rawValue: String) {
        switch rawValue {
        case "shipped": self = .shipped
        case "delivered": self = .delivered
        case "cancelled": self = .cancelled
        case "pending": self = .pending
        default: return nil
        }
    }
}

// Data source
protocol OrderRemoteDataSource: Sendable {
    func fetchOrders() async throws -> [OrderDTO]
}

struct URLSessionOrderRemoteDataSource: OrderRemoteDataSource {
    let client: HTTPClient
    func fetchOrders() async throws -> [OrderDTO] {
        try await client.get("/orders")
    }
}

// A second data source for the same repository: local storage with SwiftData.
// Only data sources import SwiftData; they hand out plain DTOs, never `@Model` classes.
protocol OrderLocalDataSource: Sendable {
    func cachedOrders() async throws -> [OrderDTO]
}

@ModelActor
actor SwiftDataOrderLocalDataSource: OrderLocalDataSource {
    func cachedOrders() throws -> [OrderDTO] {
        try modelContext.fetch(FetchDescriptor<OrderRecord>()).map(OrderDTO.init)
    }
}

// Repository implementation: the one DataRepository for OrderRepository.
// It imports only Foundation; framework code lives in the data sources.
struct OrderDataRepository: OrderRepository {
    let remote: OrderRemoteDataSource
    let local: OrderLocalDataSource?   // optional cache; the repository decides when to use it

    func orders() async throws -> [OrderEntity] {
        do {
            return try await remote.fetchOrders().map(OrderMapper.map)
        } catch let error as URLError where error.code == .notConnectedToInternet {
            throw OrderError.offline
        } catch {
            throw OrderError.unknown
        }
    }
}
```

## Presentation
```swift
struct OrderRow: Identifiable {
    let id: String
    let title: String
    let subtitle: String
    init(_ order: OrderEntity) {
        id = order.id
        title = order.total.formatted(.currency(code: "EUR"))
        subtitle = order.placedAt.formatted(date: .abbreviated, time: .omitted)
    }
}

struct OrdersView: View {
    @State var viewModel: OrdersViewModel
    var body: some View {
        Group {
            switch viewModel.state {
            case .idle, .loading: ProgressView()
            case .loaded(let rows): List(rows) { Text($0.title) }
            case .failed(let message): ContentUnavailableView(message, systemImage: "wifi.slash")
            }
        }
        .task { await viewModel.load() }
    }
}
```

## Composition root
```swift
@main struct MyApp: App {
    private let container = DIContainer()
    var body: some Scene {
        WindowGroup { OrdersView(viewModel: container.makeOrdersViewModel()) }
    }
}

final class DIContainer {
    private let client = HTTPClient(baseURL: URL(string: "https://api.example.com")!)
    func makeOrdersViewModel() -> OrdersViewModel {
        let repo = OrderDataRepository(remote: URLSessionOrderRemoteDataSource(client: client))
        return OrdersViewModel(getOrders: GetOrdersUseCase(repository: repo))
    }
}
```

## Test sketch
```swift
struct OrderRepositoryMock: OrderRepository {
    var result: Result<[OrderEntity], OrderError>
    func orders() async throws -> [OrderEntity] { try result.get() }
}

@Test @MainActor func showsFailureWhenOffline() async {
    let vm = OrdersViewModel(getOrders: GetOrdersUseCase(repository: OrderRepositoryMock(result: .failure(.offline))))
    await vm.load()
    guard case .failed = vm.state else { return Issue.record("expected failed") }
}
```

## Package layout (optional, enforces the rule)
```swift
// Package.swift (sketch)
targets: [
    .target(name: "OrdersDomain"),                                   // no dependencies
    .target(name: "OrdersData", dependencies: ["OrdersDomain"]),
    .target(name: "OrdersPresentation", dependencies: ["OrdersDomain"]),
    .testTarget(name: "OrdersDomainTests", dependencies: ["OrdersDomain"]),
]
```
Presentation never depends on Data. Only the app target imports all three and wires them together.
