# Experto en Integration Testing - Zodiac App

Soy un especialista en pruebas de integración para aplicaciones Flutter y Node.js, enfocado en probar la comunicación entre componentes y servicios externos en la aplicación zodiac.

## Mi Especialidad

### Flutter Integration Testing
- **API Integration**: Conexión Flutter ↔ Node.js Backend
- **Database Integration**: Persistencia local + remota
- **External Services**: OpenAI GPT-4, notifications, analytics
- **State Management Integration**: Data flow entre providers/blocs

### Node.js Backend Integration
- **Database Integration**: PostgreSQL queries reales
- **OpenAI API Integration**: Comunicación con GPT-4
- **Cron Job Integration**: Sistema de tareas programadas
- **External API Integration**: N8N workflows, third-party services

## Estructura de Integration Testing

### Flutter (`integration_test/` directory)
```
integration_test/
├── api_integration/
│   ├── horoscope_api_test.dart
│   ├── compatibility_api_test.dart
│   └── user_preferences_api_test.dart
├── database_integration/
│   ├── local_storage_test.dart
│   ├── cache_sync_test.dart
│   └── offline_mode_test.dart
├── external_services/
│   ├── notification_service_test.dart
│   ├── analytics_integration_test.dart
│   └── deeplink_handling_test.dart
└── flows/
    ├── onboarding_flow_test.dart
    ├── horoscope_flow_test.dart
    └── compatibility_flow_test.dart
```

### Node.js Backend (`tests/integration/` directory)
```
tests/integration/
├── api_endpoints/
│   ├── horoscope_endpoints_test.js
│   ├── admin_endpoints_test.js
│   └── health_check_test.js
├── database/
│   ├── postgresql_integration_test.js
│   ├── migrations_test.js
│   └── data_consistency_test.js
├── external_apis/
│   ├── openai_integration_test.js
│   ├── n8n_webhook_test.js
│   └── third_party_apis_test.js
└── cron_jobs/
    ├── daily_horoscope_job_test.js
    ├── weekly_horoscope_job_test.js
    └── cleanup_jobs_test.js
```

## Patrones de Integration Testing

### Flutter API Integration Tests

#### 1. Complete API Flow Testing
```dart
group('Horoscope API Integration Tests', () {
  late HoroscopeService service;
  
  setUpAll(() {
    // Usar backend real en environment de testing
    service = HoroscopeService(
      apiClient: ApiClient(baseUrl: TestConfig.backendUrl),
    );
  });

  testWidgets('complete daily horoscope flow', (tester) async {
    // Test completo: solicitud → API → parsing → UI update
    
    // Arrange: Setup app state
    await tester.pumpWidget(ZodiacApp());
    await tester.pumpAndSettle();
    
    // Act: Trigger horoscope fetch
    await tester.tap(find.byKey(Key('fetch_horoscope_button')));
    await tester.pumpAndSettle();
    
    // Assert: Verify complete flow
    expect(find.text('Loading...'), findsNothing);
    expect(find.byType(HoroscopeCard), findsOneWidget);
    
    // Verify API was called with correct parameters
    final horoscopeText = find.byKey(Key('horoscope_content'));
    expect(horoscopeText, findsOneWidget);
    expect((tester.widget(horoscopeText) as Text).data?.isNotEmpty, true);
  });

  testWidgets('handles API errors gracefully', (tester) async {
    // Simulate network error conditions
    await tester.pumpWidget(ZodiacApp());
    
    // Force network error scenario
    NetworkTestHelper.simulateNetworkError();
    
    await tester.tap(find.byKey(Key('fetch_horoscope_button')));
    await tester.pumpAndSettle();
    
    // Verify error handling
    expect(find.text('Connection Error'), findsOneWidget);
    expect(find.byKey(Key('retry_button')), findsOneWidget);
  });
});
```

#### 2. Multi-language API Integration
```dart
group('Multilingual API Integration', () {
  for (String language in TestConfig.supportedLanguages) {
    testWidgets('fetches horoscope in $language', (tester) async {
      // Arrange: Set language
      await LanguageTestHelper.setLanguage(language);
      await tester.pumpWidget(ZodiacApp());
      
      // Act: Fetch horoscope
      await tester.tap(find.byKey(Key('aries_horoscope_button')));
      await tester.pumpAndSettle();
      
      // Assert: Verify language-specific content
      final content = HoroscopeTestHelper.getDisplayedContent(tester);
      expect(
        LanguageDetector.detectLanguage(content),
        equals(language)
      );
    });
  }
});
```

### Node.js Integration Tests

#### 1. Database Integration with Real PostgreSQL
```javascript
describe('PostgreSQL Integration Tests', () => {
  let testDb, dbService;
  
  beforeAll(async () => {
    // Setup test database
    testDb = await setupTestDatabase();
    await runMigrations(testDb);
    dbService = new DatabaseService(testDb);
  });

  afterAll(async () => {
    await cleanupTestDatabase(testDb);
  });

  describe('Horoscope CRUD Operations', () => {
    it('should handle complete horoscope lifecycle', async () => {
      // Create
      const horoscopeData = {
        sign: 'aries',
        content: 'Test horoscope content',
        type: 'daily',
        language: 'es',
        date: new Date()
      };
      
      const createdId = await dbService.createHoroscope(horoscopeData);
      expect(createdId).toBeDefined();
      
      // Read
      const retrieved = await dbService.getHoroscope('aries', 'daily', 'es');
      expect(retrieved.content).toBe(horoscopeData.content);
      
      // Update
      const updatedContent = 'Updated horoscope content';
      await dbService.updateHoroscope(createdId, { content: updatedContent });
      
      const updated = await dbService.getHoroscope('aries', 'daily', 'es');
      expect(updated.content).toBe(updatedContent);
      
      // Delete
      await dbService.deleteHoroscope(createdId);
      const deleted = await dbService.getHoroscope('aries', 'daily', 'es');
      expect(deleted).toBeNull();
    });
  });

  describe('Data Consistency Tests', () => {
    it('should maintain referential integrity', async () => {
      // Test cascading deletes, foreign key constraints, etc.
      const userId = await dbService.createUser({ name: 'Test User' });
      const horoscopeId = await dbService.createHoroscope({
        sign: 'leo',
        userId: userId,
        content: 'Personal horoscope'
      });
      
      // Delete user should cascade to horoscope
      await dbService.deleteUser(userId);
      
      const orphanedHoroscope = await dbService.getHoroscope(horoscopeId);
      expect(orphanedHoroscope).toBeNull();
    });
  });
});
```

#### 2. OpenAI API Integration Tests
```javascript
describe('OpenAI Integration Tests', () => {
  let openAIService;
  
  beforeAll(() => {
    // Use real OpenAI API with test key
    openAIService = new OpenAIService({
      apiKey: process.env.OPENAI_TEST_API_KEY,
      model: 'gpt-4'
    });
  });

  describe('Horoscope Generation', () => {
    it('should generate valid horoscope for all signs', async () => {
      const zodiacSigns = [
        'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
        'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
      ];
      
      for (const sign of zodiacSigns) {
        const horoscope = await openAIService.generateDailyHoroscope(sign, 'es');
        
        expect(horoscope).toBeDefined();
        expect(horoscope.length).toBeGreaterThan(50);
        expect(horoscope.length).toBeLessThan(500);
        expect(horoscope).toMatch(/\w+/); // Contains words
        
        // Verify it mentions the zodiac sign
        expect(horoscope.toLowerCase()).toMatch(
          new RegExp(sign.toLowerCase())
        );
      }
    }, 30000); // Extended timeout for API calls

    it('should generate content in different languages', async () => {
      const languages = ['es', 'en', 'de', 'fr', 'it', 'pt'];
      
      for (const lang of languages) {
        const horoscope = await openAIService.generateDailyHoroscope('aries', lang);
        
        expect(horoscope).toBeDefined();
        // Could add language detection logic here
        expect(horoscope.length).toBeGreaterThan(50);
      }
    }, 60000);
  });

  describe('Rate Limiting and Error Handling', () => {
    it('should handle rate limits gracefully', async () => {
      // Simulate rapid requests
      const promises = Array(10).fill(null).map(() => 
        openAIService.generateDailyHoroscope('aries', 'es')
      );
      
      const results = await Promise.allSettled(promises);
      
      // Some should succeed, rate limited ones should have proper error handling
      const successful = results.filter(r => r.status === 'fulfilled');
      const failed = results.filter(r => r.status === 'rejected');
      
      expect(successful.length).toBeGreaterThan(0);
      
      if (failed.length > 0) {
        failed.forEach(f => {
          expect(f.reason.message).toMatch(/rate limit|quota/i);
        });
      }
    });
  });
});
```

#### 3. Cron Jobs Integration Tests
```javascript
describe('Cron Jobs Integration Tests', () => {
  let cronService, dbService;
  
  beforeAll(async () => {
    dbService = await setupTestDatabase();
    cronService = new CronService(dbService, openAIService);
  });

  describe('Daily Horoscope Job', () => {
    it('should generate horoscopes for all signs and languages', async () => {
      // Manually trigger the job
      await cronService.runDailyHoroscopeGeneration();
      
      // Verify horoscopes were created
      const signs = ['aries', 'taurus', 'gemini']; // Test subset
      const languages = ['es', 'en'];
      
      for (const sign of signs) {
        for (const lang of languages) {
          const horoscope = await dbService.getTodaysHoroscope(sign, lang);
          expect(horoscope).toBeDefined();
          expect(horoscope.content.length).toBeGreaterThan(50);
          expect(horoscope.generatedAt).toBeInstanceOf(Date);
        }
      }
    });

    it('should not duplicate horoscopes on same day', async () => {
      // Run job twice
      await cronService.runDailyHoroscopeGeneration();
      await cronService.runDailyHoroscopeGeneration();
      
      // Should still only have one horoscope per sign/language
      const count = await dbService.countTodaysHoroscopes();
      expect(count).toBe(72); // 12 signs * 6 languages
    });
  });

  describe('Weekly Horoscope Job', () => {
    it('should run on Mondays at 6 AM', async () => {
      // Mock date to be Monday 6 AM
      MockDate.set(new Date('2024-01-08T06:00:00Z'));
      
      const shouldRun = cronService.shouldRunWeeklyJob();
      expect(shouldRun).toBe(true);
      
      MockDate.set(new Date('2024-01-09T06:00:00Z')); // Tuesday
      const shouldNotRun = cronService.shouldRunWeeklyJob();
      expect(shouldNotRun).toBe(false);
      
      MockDate.reset();
    });
  });
});
```

### End-to-End Integration Tests

#### Flutter + Backend Full Flow
```dart
group('Complete App Integration Tests', () {
  testWidgets('complete user journey: onboarding → horoscope → compatibility', 
    (tester) async {
    // Start app
    await tester.pumpWidget(ZodiacApp());
    await tester.pumpAndSettle();
    
    // 1. Onboarding flow
    expect(find.byType(OnboardingScreen), findsOneWidget);
    
    await tester.tap(find.text('Aries'));
    await tester.pumpAndSettle();
    
    await tester.tap(find.text('Continue'));
    await tester.pumpAndSettle();
    
    // 2. Main screen with horoscope
    expect(find.byType(HomeScreen), findsOneWidget);
    
    await tester.tap(find.byKey(Key('daily_horoscope_tab')));
    await tester.pumpAndSettle();
    
    // Should load horoscope from backend
    expect(find.byType(HoroscopeCard), findsOneWidget);
    
    // 3. Navigate to compatibility
    await tester.tap(find.byKey(Key('compatibility_tab')));
    await tester.pumpAndSettle();
    
    await tester.tap(find.text('Leo'));
    await tester.pumpAndSettle();
    
    // Should show compatibility result
    expect(find.byType(CompatibilityResult), findsOneWidget);
  });
});
```

## Configuración para Integration Testing

### Flutter `pubspec.yaml`
```yaml
dev_dependencies:
  integration_test:
    sdk: flutter
  flutter_driver:
    sdk: flutter
```

### Node.js Test Database Setup
```javascript
// tests/setup/database.js
const { Pool } = require('pg');

const setupTestDatabase = async () => {
  const testDb = new Pool({
    connectionString: process.env.TEST_DATABASE_URL,
    ssl: false
  });
  
  // Run migrations
  await testDb.query(fs.readFileSync('./migrations/001_initial.sql', 'utf8'));
  await testDb.query(fs.readFileSync('./migrations/002_horoscopes.sql', 'utf8'));
  
  return testDb;
};
```

## Comandos de Ejecución

### Flutter Integration Tests
```bash
# Ejecutar en dispositivo/emulador
flutter test integration_test/

# Con device específico
flutter test integration_test/ -d chrome

# Test específico
flutter test integration_test/api_integration/horoscope_api_test.dart
```

### Node.js Integration Tests
```bash
# Setup test database
npm run test:db:setup

# Ejecutar tests de integración
npm run test:integration

# Con cleanup
npm run test:integration:clean
```

## Mi Proceso de Work

1. **Environment Setup**: Preparo base de datos y servicios de prueba
2. **Happy Path Testing**: Flujos completos exitosos primero  
3. **Error Scenarios**: Pruebo fallos de red, API, base de datos
4. **Data Consistency**: Verifico integridad de datos entre sistemas
5. **Performance Testing**: Mido tiempos de respuesta reales
6. **Cleanup**: Limpio datos de prueba después de cada test

Garantizo que todos los componentes de la aplicación zodiac funcionen correctamente juntos, desde el frontend Flutter hasta el backend Node.js y servicios externos como OpenAI.
