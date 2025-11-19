# Architecture Documentation

**Version**: 1.0.0
**Last Updated**: 2025-10-05
**Status**: ✅ Production Ready

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Data Flow Diagrams](#data-flow-diagrams)
3. [Service Dependency Graph](#service-dependency-graph)
4. [Module Structure](#module-structure)
5. [External Integrations](#external-integrations)

---

## System Architecture

### High-Level Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[Screens & Widgets]
        Providers[State Providers]
    end

    subgraph "Business Logic Layer"
        Services[Core Services]
        Managers[Feature Managers]
    end

    subgraph "Data Layer"
        Models[Data Models]
        Cache[Cache Service]
        Storage[Local Storage]
    end

    subgraph "External Services"
        Firebase[Firebase<br/>Analytics & Crashlytics]
        RevenueCat[RevenueCat<br/>Subscriptions]
        Railway[Railway Backend<br/>Horoscope API]
    end

    UI --> Providers
    Providers --> Services
    Services --> Managers
    Managers --> Models
    Services --> Cache
    Services --> Storage

    Services --> Firebase
    Services --> RevenueCat
    Services --> Railway

    style UI fill:#e1f5ff
    style Services fill:#fff4e6
    style Models fill:#f3e5f5
    style Firebase fill:#ffe0b2
    style RevenueCat fill:#c8e6c9
    style Railway fill:#ffccbc
```

---

### Three-Layer Architecture

```mermaid
graph LR
    subgraph "Layer 1: Presentation"
        A1[Screens]
        A2[Widgets]
        A3[Providers]
    end

    subgraph "Layer 2: Business Logic"
        B1[Services]
        B2[Managers]
        B3[Helpers]
    end

    subgraph "Layer 3: Data"
        C1[Models]
        C2[Storage]
        C3[API Clients]
    end

    A1 --> A3
    A2 --> A3
    A3 --> B1
    B1 --> B2
    B2 --> B3
    B1 --> C1
    B1 --> C2
    B1 --> C3

    style A1 fill:#bbdefb
    style A2 fill:#bbdefb
    style A3 fill:#90caf9
    style B1 fill:#fff9c4
    style B2 fill:#fff59d
    style B3 fill:#fff59d
    style C1 fill:#e1bee7
    style C2 fill:#ce93d8
    style C3 fill:#ce93d8
```

---

## Data Flow Diagrams

### 1. User Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant UI as Login Screen
    participant Identity as UserIdentityService
    participant Storage as Secure Storage
    participant Analytics as CoreAnalyticsService

    User->>UI: Enters credentials
    UI->>Identity: authenticate(email, password)
    Identity->>Storage: Store auth token
    Storage-->>Identity: Token stored
    Identity->>Analytics: setUserId(userId)
    Analytics-->>Identity: User tracked
    Identity-->>UI: Authentication successful
    UI-->>User: Navigate to home

    Note over User,Analytics: Secure authentication with<br/>analytics tracking
```

---

### 2. Premium Purchase Flow

```mermaid
sequenceDiagram
    participant User
    participant Paywall as PaywallScreen
    participant Subscription as SubscriptionService
    participant RevenueCat
    participant Premium as PremiumProvider
    participant Features as FeatureGating
    participant Analytics as CoreAnalyticsService

    User->>Paywall: Taps "Purchase"
    Paywall->>Analytics: logEvent('purchase_initiated')
    Paywall->>Subscription: purchaseTier(tier)
    Subscription->>RevenueCat: purchasePackage(package)

    alt Purchase Successful
        RevenueCat-->>Subscription: PurchaserInfo
        Subscription->>Premium: activatePremium(tier)
        Premium->>Features: updateFeatureAccess()
        Features-->>Premium: Features unlocked
        Subscription->>Analytics: logEvent('purchase_completed')
        Subscription-->>Paywall: Success
        Paywall-->>User: Welcome to Premium!
    else Purchase Failed
        RevenueCat-->>Subscription: Error
        Subscription->>Analytics: logEvent('purchase_failed')
        Subscription-->>Paywall: Failure
        Paywall-->>User: Purchase failed
    end
```

---

### 3. Offline Sync Flow

```mermaid
sequenceDiagram
    participant User
    participant App
    participant Offline as OfflineModeService
    participant Cache as CacheService
    participant Backend as BackendService
    participant Sync as SyncManager

    User->>App: Opens app (offline)
    App->>Offline: checkConnectivity()
    Offline-->>App: isOnline = false

    App->>Cache: getHoroscope(sign)
    Cache-->>App: Cached horoscope (stale)
    App-->>User: Shows cached data + stale indicator

    Note over User,Sync: User goes online

    Offline->>Sync: Connectivity restored
    Sync->>Backend: fetchLatestData()
    Backend-->>Sync: Fresh data
    Sync->>Cache: updateCache(data)
    Cache-->>Sync: Cache updated
    Sync-->>App: Sync complete
    App-->>User: Shows fresh data
```

---

### 4. Notification Scheduling Flow

```mermaid
sequenceDiagram
    participant User
    participant Settings as SettingsScreen
    participant NotifService as UnifiedNotificationService
    participant Platform as Flutter Local Notifications
    participant Prefs as SharedPreferences
    participant OS as Operating System

    User->>Settings: Enables daily horoscope
    Settings->>NotifService: requestPermission()
    NotifService->>OS: Request notification permission
    OS-->>User: Permission dialog
    User->>OS: Grants permission
    OS-->>NotifService: Permission granted

    Settings->>NotifService: scheduleDailyNotification(9, 0)
    NotifService->>Platform: schedule(time, payload)
    Platform-->>NotifService: Scheduled
    NotifService->>Prefs: savePreference('enabled', true)
    Prefs-->>NotifService: Saved
    NotifService-->>Settings: Success
    Settings-->>User: Notifications enabled!

    Note over OS,User: Next day at 9:00 AM
    OS->>User: Shows notification
    User->>OS: Taps notification
    OS->>NotifService: onNotificationTap(payload)
    NotifService->>Settings: Navigate to horoscope
```

---

### 5. Horoscope Fetch with Cache Flow

```mermaid
flowchart TD
    Start([User requests horoscope]) --> CheckOnline{Is online?}

    CheckOnline -->|Yes| CheckCache{Cache valid?}
    CheckOnline -->|No| UseCached[Use cached data]

    CheckCache -->|Yes, fresh| ReturnCached[Return cached]
    CheckCache -->|No, stale| FetchAPI[Fetch from API]

    FetchAPI --> APISuccess{API success?}
    APISuccess -->|Yes| UpdateCache[Update cache]
    APISuccess -->|No| ErrorHandle{Cache available?}

    UpdateCache --> ReturnFresh[Return fresh data]
    ErrorHandle -->|Yes| UseCached
    ErrorHandle -->|No| ShowError[Show error]

    UseCached --> AddStaleFlag[Add stale indicator]
    AddStaleFlag --> ReturnStale[Return stale data]

    ReturnCached --> End([Display to user])
    ReturnFresh --> End
    ReturnStale --> End
    ShowError --> End

    style Start fill:#e8f5e9
    style End fill:#e8f5e9
    style FetchAPI fill:#fff9c4
    style UpdateCache fill:#fff9c4
    style CheckOnline fill:#e1f5fe
    style CheckCache fill:#e1f5fe
    style APISuccess fill:#e1f5fe
    style ErrorHandle fill:#ffebee
    style ShowError fill:#ffcdd2
```

---

## Service Dependency Graph

### Core Services Dependencies

```mermaid
graph TD
    %% UI Layer
    Screens[Screens & Widgets]

    %% Service Layer
    Horoscope[HoroscopeService]
    Compatibility[CoreCompatibilityService]
    Premium[PremiumSubscriptionManager]
    Offline[OfflineModeService]
    Notifications[UnifiedNotificationService]
    Journal[SmartJournalingService]
    Coach[CoachingAIService]

    %% Support Services
    Analytics[CoreAnalyticsService]
    Logging[SecureLoggingService]
    Performance[PerformanceMonitoring]
    Cache[CacheService]
    UserIdentity[UserIdentityService]
    Backend[BackendService]

    %% External
    Firebase[Firebase]
    RevenueCat[RevenueCat]
    Railway[Railway API]

    %% Dependencies
    Screens --> Horoscope
    Screens --> Compatibility
    Screens --> Premium
    Screens --> Journal
    Screens --> Coach

    Horoscope --> Backend
    Horoscope --> Cache
    Horoscope --> Offline
    Horoscope --> Analytics
    Horoscope --> Logging

    Compatibility --> UserIdentity
    Compatibility --> Analytics
    Compatibility --> Cache

    Premium --> RevenueCat
    Premium --> Analytics
    Premium --> Logging

    Offline --> Cache
    Offline --> Backend
    Offline --> Analytics

    Notifications --> Analytics
    Notifications --> Logging

    Journal --> Analytics
    Journal --> Cache

    Coach --> Backend
    Coach --> Analytics
    Coach --> UserIdentity

    Backend --> Railway
    Analytics --> Firebase
    Logging --> Firebase

    UserIdentity --> Cache

    style Screens fill:#e1f5ff
    style Horoscope fill:#fff4e6
    style Compatibility fill:#fff4e6
    style Premium fill:#c8e6c9
    style Analytics fill:#f3e5f5
    style Firebase fill:#ffe0b2
    style RevenueCat fill:#c8e6c9
```

---

### Circular Dependencies Check

**Status**: ✅ No circular dependencies detected

**Key Design Decisions**:
1. Services never depend on UI components
2. Core services use dependency injection
3. Shared services (Analytics, Logging) are leaf nodes
4. External integrations are isolated

---

## Module Structure

### Directory Organization

```
lib/
├── main.dart                          # App entry point
├── screens/                           # UI Layer
│   ├── home_screen.dart
│   ├── horoscope_screen.dart
│   ├── compatibility_screen.dart
│   ├── premium_screen.dart
│   └── settings_screen.dart
├── services/                          # Business Logic Layer
│   ├── consolidated_ai/               # AI Services
│   │   ├── coaching_ai_service.dart
│   │   └── conversation_ai_service.dart
│   ├── consolidated_compatibility/    # Compatibility Services
│   │   ├── core_compatibility_service.dart
│   │   └── compatibility_provider.dart
│   ├── consolidated_payments/         # Payment Services
│   │   ├── quantum_payment_engine.dart
│   │   └── payment_provider.dart
│   ├── core_analytics_service.dart    # Analytics
│   ├── secure_logging_service.dart    # Logging
│   ├── performance_monitoring_service.dart  # Performance
│   ├── offline_mode_service.dart      # Offline Support
│   ├── unified_notification_service.dart    # Notifications
│   ├── user_identity_service.dart     # User Identity
│   ├── subscription_service.dart      # Subscriptions
│   └── backend_service.dart           # API Client
├── models/                            # Data Models
│   ├── horoscope.dart
│   ├── compatibility_result.dart
│   ├── subscription_tier.dart
│   └── user_profile.dart
├── providers/                         # State Management
│   ├── premium_provider.dart
│   ├── theme_provider.dart
│   └── user_provider.dart
├── utils/                             # Utilities
│   ├── constants.dart
│   ├── helpers.dart
│   └── app_logger.dart
└── widgets/                           # Reusable Widgets
    ├── cosmic_button.dart
    ├── zodiac_card.dart
    └── premium_badge.dart
```

---

### Service Categories

```mermaid
graph TD
    subgraph "Core Services"
        CS1[HoroscopeService]
        CS2[CompatibilityService]
        CS3[PremiumService]
        CS4[UserIdentityService]
    end

    subgraph "Support Services"
        SS1[AnalyticsService]
        SS2[LoggingService]
        SS3[PerformanceService]
        SS4[CacheService]
    end

    subgraph "Feature Services"
        FS1[AICoachService]
        FS2[JournalingService]
        FS3[NotificationService]
        FS4[OfflineService]
    end

    subgraph "Integration Services"
        IS1[BackendService]
        IS2[RevenueCatService]
        IS3[FirebaseService]
    end

    CS1 --> SS1
    CS1 --> SS2
    CS2 --> SS1
    CS3 --> IS2
    FS1 --> IS1
    FS2 --> SS4
    FS3 --> SS1
    FS4 --> SS4
    IS1 --> IS3

    style CS1 fill:#bbdefb
    style SS1 fill:#f3e5f5
    style FS1 fill:#fff9c4
    style IS1 fill:#c8e6c9
```

---

## External Integrations

### Integration Points

```mermaid
graph LR
    subgraph "Zodiac App"
        App[Flutter App]
        Services[Services Layer]
    end

    subgraph "Firebase"
        FA[Analytics]
        FC[Crashlytics]
        FM[Cloud Messaging]
    end

    subgraph "RevenueCat"
        RC[Subscription Management]
        RR[Receipt Validation]
    end

    subgraph "Railway Backend"
        RB[Horoscope API]
        RA[AI Endpoints]
    end

    App --> Services
    Services --> FA
    Services --> FC
    Services --> FM
    Services --> RC
    Services --> RR
    Services --> RB
    Services --> RA

    style App fill:#e1f5ff
    style FA fill:#ffe0b2
    style FC fill:#ffe0b2
    style FM fill:#ffe0b2
    style RC fill:#c8e6c9
    style RR fill:#c8e6c9
    style RB fill:#ffccbc
    style RA fill:#ffccbc
```

---

### API Communication

```mermaid
sequenceDiagram
    participant App
    participant BackendService
    participant Railway as Railway API
    participant Firebase

    App->>BackendService: fetchHoroscope(sign)
    BackendService->>Railway: GET /horoscope/daily/:sign

    alt API Success
        Railway-->>BackendService: { horoscope data }
        BackendService->>Firebase: logEvent('api_success')
        BackendService-->>App: Horoscope
    else API Failure
        Railway-->>BackendService: Error 500
        BackendService->>Firebase: logEvent('api_failure')
        BackendService->>BackendService: Retry logic
        BackendService->>Railway: GET /horoscope/daily/:sign
        Railway-->>BackendService: { horoscope data }
        BackendService-->>App: Horoscope
    else Network Error
        Railway-->>BackendService: Network timeout
        BackendService->>Firebase: logError('network_timeout')
        BackendService-->>App: Use cached data
    end
```

---

## Design Patterns

### 1. Singleton Pattern
**Used in**: All services
```dart
class CoreAnalyticsService {
  static final CoreAnalyticsService _instance = CoreAnalyticsService._internal();
  factory CoreAnalyticsService() => _instance;
  CoreAnalyticsService._internal();
}
```

### 2. Provider Pattern
**Used in**: State management
```dart
ChangeNotifierProvider(
  create: (_) => PremiumProvider(),
  child: MyApp(),
);
```

### 3. Repository Pattern
**Used in**: Data access
```dart
class HoroscopeRepository {
  Future<Horoscope> getHoroscope(String sign) async {
    // Try cache first
    final cached = await cache.get(sign);
    if (cached != null) return cached;

    // Fetch from API
    final fresh = await api.fetchHoroscope(sign);
    await cache.set(sign, fresh);
    return fresh;
  }
}
```

### 4. Observer Pattern
**Used in**: Analytics, logging
```dart
class AnalyticsObserver extends RouteObserver<PageRoute> {
  @override
  void didPush(Route route, Route? previousRoute) {
    analytics.logEvent('screen_view', {'screen': route.settings.name});
  }
}
```

---

## Scalability Considerations

### Horizontal Scaling
- **Backend**: Railway auto-scaling
- **Cache**: Distributed caching ready
- **Analytics**: Firebase auto-scales

### Performance Optimization
- **Lazy loading**: Services initialized on demand
- **Code splitting**: Feature modules isolated
- **Cache strategy**: Multi-layer caching
- **Offline first**: Reduce API calls

### Monitoring
- **Performance**: Real-time metrics
- **Errors**: Crashlytics integration
- **Revenue**: RevenueCat dashboard
- **Usage**: Firebase Analytics

---

## Future Enhancements

### Planned Improvements
1. **GraphQL API**: Replace REST with GraphQL
2. **WebSocket**: Real-time cosmic updates
3. **CDN**: Static content delivery
4. **Push Notifications**: Backend-triggered notifications
5. **Multi-language**: i18n support expansion

### Architecture Evolution
```mermaid
graph LR
    Current[Current Architecture<br/>Monolithic Services] --> Future[Future Architecture<br/>Microservices]

    subgraph "Current"
        C1[All services in app]
    end

    subgraph "Future"
        F1[Horoscope Service]
        F2[AI Service]
        F3[Payment Service]
        F4[Analytics Service]
    end

    Current --> F1
    Current --> F2
    Current --> F3
    Current --> F4

    style Current fill:#ffccbc
    style Future fill:#c8e6c9
```

---

**For questions**: Contact architecture team
**For updates**: See CHANGELOG.md
**For implementation**: See service documentation
