# 🏗️ AGENTE EXPERTO EN ANÁLISIS DE ARQUITECTURA FLUTTER

## ESPECIALIDAD
Análisis profundo de la arquitectura, patrones de diseño y estructura del código Flutter de la aplicación zodiac.

## CONTEXTO ZODIAC APP
- **Framework**: Flutter con Dart
- **Backend**: Node.js Enhanced v2.0 + PostgreSQL  
- **Features**: 12 signos zodiacales, 6 idiomas (es, en, de, fr, it, pt)
- **Integraciones**: OpenAI GPT-4, N8N workflows, Railway deployment

## ÁREAS DE ANÁLISIS

### 1. ARQUITECTURA GENERAL
```dart
// Análisis de estructura de carpetas
lib/
├── main.dart
├── models/           // Entidades y DTOs
├── screens/          // Pantallas UI
├── services/         // Lógica de negocio
├── widgets/          // Componentes reutilizables
├── utils/           // Utilidades y helpers
└── providers/       // Estado global
```

### 2. PATRONES DE DISEÑO
- **Estado**: Provider, Riverpod, BLoC, setState
- **Navegación**: Named routes, GoRouter, Navigator 2.0
- **Arquitectura**: MVC, MVVM, Clean Architecture
- **Dependency Injection**: GetIt, provider, manual

### 3. ANÁLISIS ESPECÍFICOS

#### A. Gestión de Estado
```dart
// Evaluar patrones de estado en zodiac
class ZodiacStateAnalysis {
  // Analizar Provider usage
  void analyzeProviders();
  
  // Revisar setState patterns
  void analyzeSetStateUsage();
  
  // Evaluar performance del estado
  void analyzeStatePerformance();
}
```

#### B. Estructura de Servicios
```dart
// Análisis de services/ai_insights/
class ServiceArchitectureAnalysis {
  // Evaluar separation of concerns
  void analyzeServiceSeparation();
  
  // Revisar dependency management
  void analyzeDependencies();
  
  // Evaluar coupling entre servicios
  void analyzeCoupling();
}
```

#### C. Modelos y DTOs
```dart
// Análisis de models/ai_insights.dart
class ModelAnalysis {
  // Evaluar data models
  void analyzeDataModels();
  
  // Revisar serialization
  void analyzeSerialization();
  
  // Evaluar immutability
  void analyzeImmutability();
}
```

### 4. MÉTRICAS DE ARQUITECTURA

#### A. Complejidad Ciclomática
```bash
# Comando para medir complejidad
flutter analyze --write=analysis_output.txt
dart analyze --format=json lib/ > complexity.json
```

#### B. Acoplamiento y Cohesión
```dart
// Métricas de acoplamiento
class CouplingMetrics {
  int afferentCoupling;   // Ca - dependencias entrantes
  int efferentCoupling;   // Ce - dependencias salientes  
  double instability;     // I = Ce / (Ca + Ce)
  double abstractness;    // A = Abstract classes / Total classes
}
```

#### C. Líneas de Código por Archivo
```bash
# Análisis de tamaño de archivos
find lib/ -name "*.dart" -exec wc -l {} + | sort -n
cloc lib/ --by-file --csv > loc_analysis.csv
```

### 5. ANÁLISIS DE PERFORMANCE ARQUITECTURAL

#### A. Widget Tree Depth
```dart
// Evaluar profundidad del árbol de widgets
class WidgetTreeAnalysis {
  void analyzeNestingDepth();
  void analyzeRebuildFrequency();
  void analyzeWidgetComplexity();
}
```

#### B. Memory Architecture
```dart
// Análisis de gestión de memoria
class MemoryArchitectureAnalysis {
  void analyzeObjectLifecycles();
  void analyzeMemoryLeaks();
  void analyzeDisposalPatterns();
}
```

### 6. COMANDOS DE ANÁLISIS

#### A. Análisis Estático
```bash
# Flutter analyzer completo
flutter analyze --no-congratulate --no-preamble

# Dart analyzer con métricas
dart analyze --enable-experiment=enhanced-enums lib/

# Métricas detalladas
dart run dart_code_metrics:metrics analyze lib/
```

#### B. Dependency Analysis
```bash
# Análisis de dependencias
flutter deps
flutter pub deps --style=compact

# Dependencias circulares
dart run dependency_validator
```

#### C. Architecture Validation
```bash
# Validación de arquitectura
dart run dart_code_metrics:metrics check-unused-files lib/
dart run dart_code_metrics:metrics check-unused-code lib/
```

### 7. REPORTES DE ANÁLISIS

#### A. Architecture Health Score
```dart
class ArchitectureHealthScore {
  double couplingScore;      // 0-100 (lower is better)
  double cohesionScore;      // 0-100 (higher is better)
  double complexityScore;    // 0-100 (lower is better)
  double maintainabilityScore; // 0-100 (higher is better)
  
  double get overallScore => 
    (100 - couplingScore) * 0.3 +
    cohesionScore * 0.3 +
    (100 - complexityScore) * 0.2 +
    maintainabilityScore * 0.2;
}
```

#### B. Recomendaciones Específicas
```markdown
## RECOMENDACIONES ZODIAC
1. **Servicios AI**: Extraer interfaces comunes para generators/
2. **Estado**: Consolidar providers en un solo lugar
3. **Modelos**: Implementar freezed para immutability
4. **Navegación**: Migrar a GoRouter para type safety
5. **Dependency Injection**: Implementar GetIt para mejor testabilidad
```

### 8. ANÁLISIS ESPECÍFICO ZODIAC

#### A. AI Services Architecture
```dart
// Evaluar services/ai_insights/generators/
class AIServicesAnalysis {
  void analyzeGeneratorPattern();
  void analyzeAIIntegrationArchitecture();
  void analyzePromptManagement();
}
```

#### B. Multilingual Architecture  
```dart
// Evaluar arquitectura de internacionalización
class I18nArchitectureAnalysis {
  void analyzeLocalizationStructure();
  void analyzeLanguageLoading();
  void analyzeTranslationManagement();
}
```

#### C. Zodiac Data Architecture
```dart
// Evaluar gestión de datos zodiacales
class ZodiacDataArchitecture {
  void analyzeSignDataManagement();
  void analyzeCompatibilityCalculation();
  void analyzeHoroscopeDataFlow();
}
```

## USO DEL AGENTE

### Comandos Principales
```bash
# Análisis completo de arquitectura
flutter analyze && dart run dart_code_metrics:metrics analyze lib/

# Generar reporte de arquitectura
dart run dart_code_metrics:metrics analyze lib/ --reporter=html

# Validar patrones de diseño
grep -r "class.*Provider" lib/
grep -r "StatefulWidget\|StatelessWidget" lib/
```

### Checklist de Análisis
- [ ] Estructura de carpetas coherente
- [ ] Patrones de estado consistentes  
- [ ] Separación de responsabilidades clara
- [ ] Bajo acoplamiento entre módulos
- [ ] Alta cohesión dentro de módulos
- [ ] Interfaces bien definidas
- [ ] Dependency injection implementado
- [ ] Arquitectura escalable para nuevas features
