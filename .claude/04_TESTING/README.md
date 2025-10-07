# Subagentes Expertos en Testing - Zodiac App

Este directorio contiene subagentes especializados en diferentes tipos de testing para la aplicación zodiac (Flutter + Node.js backend).

## 🎯 Subagentes Disponibles

### 1. **Unit Testing Expert** (`unit_testing_expert.md`)
**Especialidad**: Pruebas unitarias para Flutter y Node.js
- ✅ Business Logic Testing (modelos, validators, utils)
- ✅ State Management Testing (Providers, BLoCs, Controllers)
- ✅ Service Testing (API clients, storage, auth)
- ✅ Zodiac Logic Testing (compatibilidad, horóscopos)
- ✅ Backend Testing (Express routes, PostgreSQL, OpenAI)

**Casos de Uso**:
- Probar cálculos de compatibilidad zodiacal
- Validar lógica de negocio sin dependencias
- Testing de servicios con mocks
- Verificar transformación de datos

### 2. **Integration Testing Expert** (`integration_testing_expert.md`)
**Especialidad**: Pruebas de integración entre componentes y servicios
- ✅ API Integration (Flutter ↔ Node.js Backend)
- ✅ Database Integration (PostgreSQL queries reales)
- ✅ OpenAI Integration (comunicación GPT-4)
- ✅ Cron Jobs Integration (horóscopos automáticos)
- ✅ External Services (N8N, notifications)

**Casos de Uso**:
- Probar flujo completo API → DB → Response
- Verificar integración con OpenAI GPT-4
- Testing de cron jobs programados
- Validar sincronización de datos

### 3. **Widget Testing Expert** (`widget_testing_expert.md`)
**Especialidad**: Pruebas de UI widgets Flutter
- ✅ UI Component Testing (cards, selectors, displays)
- ✅ User Interaction Testing (taps, scrolls, forms)
- ✅ State Management Testing (Provider/BLoC + UI)
- ✅ Responsive Design Testing (mobile/tablet/desktop)
- ✅ Accessibility Testing (semantics, navegación)
- ✅ Multilingual UI Testing (6 idiomas)

**Casos de Uso**:
- Probar componentes zodiacales personalizados
- Verificar interacciones de usuario
- Testing de responsive design
- Validar accesibilidad y localización

### 4. **E2E Testing Expert** (`e2e_testing_expert.md`)
**Especialidad**: Pruebas End-to-End completas
- ✅ User Journey Testing (flujos completos)
- ✅ Cross-Platform Testing (iOS/Android/Web)
- ✅ Performance Testing (memoria, batería, velocidad)
- ✅ Network Testing (offline, sync, conectividad)
- ✅ Real Device Testing (dispositivos físicos)

**Casos de Uso**:
- Probar onboarding completo de usuario
- Verificar experiencia diaria de horóscopo
- Testing de análisis de compatibilidad
- Validar funcionamiento offline/online

### 5. **Backend API Testing Expert** (`backend_api_testing_expert.md`)
**Especialidad**: Pruebas de APIs Node.js
- ✅ REST API Testing (endpoints HTTP)
- ✅ Authentication Testing (JWT, API keys, admin)
- ✅ Data Validation Testing (schemas, validaciones)
- ✅ Performance Testing (response times, load)
- ✅ Multilingual API Testing (6 idiomas)
- ✅ Error Handling Testing (4xx, 5xx responses)

**Casos de Uso**:
- Probar endpoints de horóscopos
- Verificar autenticación y autorización
- Testing de APIs administrativas
- Validar performance bajo carga

## 🏗️ Estructura de Testing Recomendada

```
zodiac_app/
├── test/
│   ├── unit/
│   │   ├── models/
│   │   ├── services/
│   │   ├── utils/
│   │   └── controllers/
│   ├── widget/
│   │   ├── screens/
│   │   ├── widgets/
│   │   ├── common/
│   │   └── responsive/
│   └── mocks/
└── integration_test/
    ├── api_integration/
    ├── database_integration/
    ├── external_services/
    └── e2e/

backend/flutter-horoscope-backend/
├── tests/
│   ├── unit/
│   │   ├── controllers/
│   │   ├── services/
│   │   └── utils/
│   ├── integration/
│   │   ├── database/
│   │   ├── external_apis/
│   │   └── cron_jobs/
│   └── api/
│       ├── endpoints/
│       ├── authentication/
│       ├── validation/
│       └── performance/
```

## 🚀 Comandos de Ejecución Rápida

### Flutter Testing
```bash
# Unit tests
flutter test test/unit/

# Widget tests
flutter test test/widget/

# Integration tests
flutter test integration_test/

# E2E tests
flutter test integration_test/e2e/

# Coverage completo
flutter test --coverage
```

### Backend Testing
```bash
# Unit tests
npm test -- tests/unit/

# Integration tests
npm run test:integration

# API tests
npm run test:api

# E2E backend tests
npm run test:e2e

# Load testing
npm run test:load
```

## 🎯 Características Específicas de Zodiac

### Testing de Lógica Zodiacal
- **12 signos del zodíaco**: Aries → Piscis
- **Cálculos de compatibilidad**: Elementos (fuego, tierra, aire, agua)
- **Fechas y rangos**: Validación de fechas de nacimiento
- **Personalización**: Contenido específico por signo

### Testing Multilingual
- **6 idiomas soportados**: Español, Inglés, Alemán, Francés, Italiano, Portugués
- **Localización**: Contenido traducido y formatos locales
- **Fallbacks**: Idioma por defecto cuando no hay traducción
- **UI Adaptation**: RTL languages, formatting

### Testing de Backend Enhanced v2.0
- **PostgreSQL**: Base de datos con migraciones
- **OpenAI GPT-4**: Generación automática de horóscopos
- **Railway Deployment**: Testing en ambiente real
- **Cron Jobs**: Horóscopos diarios (24h) y semanales (lunes 6 AM)
- **Security**: Rate limiting, authentication, validation

### Testing de Integración N8N
- **Webhooks**: Comunicación con workflows externos
- **Automation**: Triggers automáticos de generación
- **Data Flow**: Backend → N8N → External Services
- **Error Handling**: Fallos en integraciones externas

## 📊 Métricas de Testing Objetivo

### Coverage Targets
- **Unit Tests**: >90% coverage
- **Widget Tests**: >85% coverage
- **Integration Tests**: >80% coverage
- **API Tests**: >90% coverage

### Performance Targets
- **API Response**: <2 segundos
- **App Startup**: <3 segundos
- **Widget Render**: <100ms
- **Database Queries**: <500ms

### Quality Gates
- **All Tests Passing**: 100%
- **No Critical Bugs**: 0 blocker/critical
- **Security**: No vulnerabilities HIGH+
- **Accessibility**: WCAG 2.1 AA compliance

## 🔧 Herramientas y Dependencias

### Flutter Testing Stack
```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
  mockito: ^5.4.2
  mocktail: ^0.3.0
  patrol: ^2.0.0
  test: ^1.24.3
```

### Node.js Testing Stack
```json
{
  "devDependencies": {
    "jest": "^29.5.0",
    "supertest": "^6.3.3",
    "@types/jest": "^29.5.2",
    "artillery": "^2.0.0",
    "k6": "^0.45.0"
  }
}
```

## 🎓 Cómo Usar los Subagentes

1. **Identifica el tipo de testing**: Unit, Widget, Integration, E2E, API
2. **Consulta el subagente correspondiente**: Lee el archivo .md específico
3. **Adapta los ejemplos**: Usa los patrones para tu caso específico
4. **Ejecuta los tests**: Sigue los comandos de ejecución
5. **Itera y mejora**: Refina tests basado en resultados

## 📈 Roadmap de Testing

### Fase 1: Foundation (Actual)
- ✅ Unit tests básicos
- ✅ Widget tests core
- ✅ API tests principales
- ✅ Integration tests críticos

### Fase 2: Advanced (Siguiente)
- 🔄 Performance benchmarking
- 🔄 Visual regression testing
- 🔄 Accessibility automation
- 🔄 Load testing completo

### Fase 3: CI/CD Integration
- ⏳ Pipeline automation
- ⏳ Quality gates
- ⏳ Deployment testing
- ⏳ Monitoring integration

---

## 💡 Tips de Uso

- **Combina subagentes**: Usa múltiples expertos para testing completo
- **Prioriza por riesgo**: Testing crítico primero (auth, payments, data)  
- **Automatiza en CI**: Integra tests en pipeline de deployment
- **Mide y mejora**: Usa métricas para identificar gaps de testing

**¿Necesitas ayuda específica?** Consulta el subagente experto correspondiente para ejemplos detallados y mejores prácticas específicas de tu caso de uso.
