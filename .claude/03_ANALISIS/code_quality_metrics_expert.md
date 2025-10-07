# 📊 AGENTE EXPERTO EN ANÁLISIS DE CALIDAD DE CÓDIGO Y MÉTRICAS

## ESPECIALIDAD
Análisis exhaustivo de calidad de código, métricas de mantenibilidad, legibilidad y mejores prácticas en la aplicación zodiac Flutter y backend Node.js.

## CONTEXTO ZODIAC APP
- **Frontend**: Flutter/Dart con arquitectura modular
- **Backend**: Node.js Enhanced v2.0 con Express
- **Métricas objetivo**: >90% test coverage, <15 complejidad ciclomática
- **Estándares**: Clean Code, SOLID principles, Flutter best practices

## ÁREAS DE ANÁLISIS

### 1. MÉTRICAS DE CÓDIGO

#### A. Complejidad y Mantenibilidad
```dart
// Análisis de complejidad ciclomática
class ComplexityAnalysis {
  // Métodos con alta complejidad
  void analyzeCyclomaticComplexity();
  void identifyComplexMethods();
  void measureCognitiveLoad();
  
  // Zodiac specific complexity
  void analyzeAIGeneratorComplexity();
  void analyzeCompatibilityCalculationComplexity();
  void analyzeStateManagementComplexity();
}
```

#### B. Métricas de Tamaño
```dart
// Análisis de tamaño y volumen
class SizeMetrics {
  int linesOfCode;
  int methodCount;
  int classCount;
  int fileCount;
  
  void analyzeLinesOfCodePerFile();
  void analyzeLinesOfCodePerMethod();
  void analyzeClassSizeDistribution();
  void identifyOversizedFiles();
}
```

#### C. Métricas de Cohesión y Acoplamiento
```dart
// LCOM - Lack of Cohesion of Methods
class CohesionMetrics {
  double lcom4Score;
  double classResponsibility;
  
  void analyzeLCOMScores();
  void analyzeClassResponsibilities();
  void identifyGodClasses();
}

// Coupling metrics
class CouplingMetrics {
  int afferentCoupling;  // Ca
  int efferentCoupling;  // Ce
  double instability;    // I = Ce/(Ca+Ce)
  
  void analyzeCouplingBetweenObjects();
  void analyzePackageCoupling();
  void identifyTightlyCoupleDclasses();
}
```

### 2. ANÁLISIS DE CÓDIGO FLUTTER

#### A. Widget Quality Analysis
```dart
// Calidad de widgets específicos
class WidgetQualityAnalysis {
  // Análisis de pantallas principales
  void analyzeCompatibilityScreenQuality();
  void analyzeHoroscopeScreenQuality();
  void analyzeAIInsightsScreenQuality();
  
  // Widget best practices
  void analyzeConstUsage();
  void analyzeStatelessVsStateful();
  void analyzeBuildMethodComplexity();
  void analyzeWidgetComposition();
}
```

#### B. State Management Quality
```dart
// Calidad de gestión de estado
class StateQualityAnalysis {
  void analyzeProviderUsage();
  void analyzeStateImmutability();
  void analyzeStateMutationPatterns();
  void analyzeListenerManagement();
}
```

#### C. Service Layer Quality
```dart
// Calidad de servicios
class ServiceQualityAnalysis {
  // AI services quality
  void analyzeAIGeneratorQuality();
  void analyzePersonalGrowthAIQuality();
  void analyzeCompatibilityLearningAIQuality();
  
  // Service patterns
  void analyzeSingleResponsibilityPrinciple();
  void analyzeDependencyInjection();
  void analyzeErrorHandling();
}
```

### 3. MÉTRICAS DE TESTING

#### A. Coverage Analysis
```dart
// Análisis de cobertura de tests
class TestCoverageAnalysis {
  double overallCoverage;
  double unitTestCoverage;
  double integrationTestCoverage;
  double widgetTestCoverage;
  
  void generateCoverageReport();
  void identifyUncoveredCode();
  void analyzeCriticalPathCoverage();
  void measureTestQuality();
}
```

#### B. Test Quality Metrics
```dart
// Calidad de tests
class TestQualityMetrics {
  int testCount;
  double testToCodeRatio;
  int assertionsPerTest;
  
  void analyzeTestNaming();
  void analyzeTestStructure();
  void analyzeTestDuplication();
  void analyzeMockUsage();
}
```

### 4. ANÁLISIS DE DOCUMENTACIÓN

#### A. Code Documentation
```dart
// Documentación de código
class DocumentationAnalysis {
  double documentationCoverage;
  int undocumentedMethods;
  int undocumentedClasses;
  
  void analyzeDocumentationCompleteness();
  void analyzeCommentQuality();
  void analyzeAPIDocumentation();
  void generateDocumentationReport();
}
```

#### B. README y Documentation Quality
```markdown
## ANÁLISIS DE DOCUMENTACIÓN ZODIAC

### Archivos a evaluar:
- [ ] README.md principales
- [ ] Documentación API
- [ ] Guías de instalación
- [ ] Documentación de arquitectura
- [ ] Changelog y release notes
```

### 5. COMANDOS DE ANÁLISIS

#### A. Flutter/Dart Analysis
```bash
# Análisis estático completo
flutter analyze --no-congratulate
dart analyze --enable-experiment=enhanced-enums

# Métricas detalladas con dart_code_metrics
dart run dart_code_metrics:metrics analyze lib/ --reporter=html
dart run dart_code_metrics:metrics analyze lib/ --reporter=json

# Análisis de complejidad
dart run dart_code_metrics:metrics check-unnecessary-nullable lib/
dart run dart_code_metrics:metrics check-unused-code lib/
```

#### B. Test Coverage
```bash
# Coverage completo
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html

# Coverage por tipo
flutter test test/unit/ --coverage
flutter test test/widget/ --coverage
flutter test integration_test/ --coverage
```

#### C. Code Metrics Tools
```bash
# Instalación de herramientas
dart pub global activate dart_code_metrics
dart pub global activate pana

# Análisis con pana (pub.dev style)
pana --source path .

# Análisis personalizado
cloc lib/ --by-file --csv
```

### 6. MÉTRICAS ESPECÍFICAS ZODIAC

#### A. AI Services Quality
```dart
// Métricas específicas de servicios AI
class AIServicesQualityMetrics {
  // Personal Growth AI quality
  void analyzePersonalGrowthAIComplexity();
  void analyzePromptTemplateQuality();
  void analyzeResponseParsingQuality();
  
  // Compatibility Learning AI quality  
  void analyzeCompatibilityLogicQuality();
  void analyzeZodiacCalculationAccuracy();
  void analyzeLearningAlgorithmQuality();
}
```

#### B. Multilingual Code Quality
```dart
// Calidad código multiidioma
class I18nCodeQuality {
  void analyzeLocalizationKeyUsage();
  void analyzeStringExternalization();
  void analyzeTranslationConsistency();
  void analyzeLanguageSwitchingQuality();
}
```

#### C. Premium Features Quality
```dart
// Calidad features premium
class PremiumFeaturesQuality {
  void analyzePremiumAnalyticsQuality();
  void analyzePreferencesServiceQuality();
  void analyzeFeatureGatingQuality();
  void analyzeSubscriptionHandlingQuality();
}
```

### 7. QUALITY GATES

#### A. Automated Quality Checks
```yaml
# quality_gates.yaml
quality_gates:
  cyclomatic_complexity:
    max_value: 15
    warning_threshold: 10
    
  lines_of_code:
    max_per_file: 300
    max_per_method: 50
    
  test_coverage:
    minimum: 80
    target: 90
    
  maintainability_index:
    minimum: 70
    target: 85
```

#### B. Quality Score Calculation
```dart
// Cálculo de score de calidad
class QualityScoreCalculator {
  double calculateOverallQuality() {
    final complexity = _calculateComplexityScore();
    final coverage = _calculateCoverageScore();
    final maintainability = _calculateMaintainabilityScore();
    final documentation = _calculateDocumentationScore();
    
    return (complexity * 0.3) + 
           (coverage * 0.3) + 
           (maintainability * 0.25) + 
           (documentation * 0.15);
  }
}
```

### 8. CODE REVIEW AUTOMATION

#### A. Pre-commit Hooks
```bash
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: flutter-analyze
        name: Flutter Analyze
        entry: flutter analyze
        language: system
        
      - id: dart-format
        name: Dart Format
        entry: dart format --set-exit-if-changed
        language: system
        
      - id: flutter-test
        name: Flutter Test
        entry: flutter test
        language: system
```

#### B. CI/CD Quality Checks
```yaml
# GitHub Actions quality pipeline
name: Code Quality Check
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: subosito/flutter-action@v2
      
      - name: Run Flutter Analyze
        run: flutter analyze
        
      - name: Run Tests with Coverage
        run: flutter test --coverage
        
      - name: Run Code Metrics
        run: dart run dart_code_metrics:metrics analyze lib/
        
      - name: Upload Coverage
        uses: codecov/codecov-action@v2
```

### 9. TECHNICAL DEBT ANALYSIS

#### A. Debt Identification
```dart
// Identificación de deuda técnica
class TechnicalDebtAnalysis {
  void identifyCodeSmells();
  void analyzeAntiPatterns();
  void findDuplicatedCode();
  void identifyDeprecatedAPIs();
  
  // Zodiac specific debt
  void analyzeLegacyZodiacLogic();
  void identifySuboptimalAIIntegrations();
  void analyzeOutdatedDependencies();
}
```

#### B. Refactoring Opportunities
```dart
// Oportunidades de refactoring
class RefactoringOpportunities {
  List<String> identifyLargeClasses();
  List<String> identifyLongMethods();
  List<String> identifyDuplicatedCode();
  List<String> identifyComplexConditionals();
  
  void prioritizeRefactoringTasks();
  void estimateRefactoringEffort();
}
```

### 10. REPORTING Y DASHBOARDS

#### A. Quality Dashboard
```dart
// Dashboard de métricas de calidad
class QualityDashboard {
  Map<String, dynamic> generateQualityReport() {
    return {
      'overall_quality_score': _calculateOverallScore(),
      'complexity_metrics': _getComplexityMetrics(),
      'test_coverage': _getCoverageMetrics(),
      'technical_debt': _getTechnicalDebtMetrics(),
      'trends': _getQualityTrends(),
      'recommendations': _getRecommendations(),
    };
  }
  
  void exportToHTML();
  void exportToJSON();
  void generateTrendAnalysis();
}
```

#### B. Quality Trends
```dart
// Análisis de tendencias
class QualityTrends {
  void trackQualityOverTime();
  void identifyRegressions();
  void measureImprovements();
  void predictQualityTrends();
}
```

### 11. BEST PRACTICES VALIDATION

#### A. Flutter Best Practices
```dart
// Validación de mejores prácticas Flutter
class FlutterBestPracticesValidator {
  void validateWidgetNaming();
  void validateFileOrganization();
  void validateImportOrdering();
  void validateAssetUsage();
  void validateStateManagementPatterns();
}
```

#### B. Dart Language Best Practices
```dart
// Mejores prácticas Dart
class DartBestPracticesValidator {
  void validateNullSafety();
  void validateAsyncPatterns();
  void validateErrorHandling();
  void validateMemoryManagement();
  void validatePerformancePatterns();
}
```

## USO DEL AGENTE

### Comandos Principales
```bash
# Análisis completo de calidad
flutter analyze && flutter test --coverage
dart run dart_code_metrics:metrics analyze lib/ --reporter=html

# Generación de reportes
pana --source path .
cloc lib/ --by-file --csv > code_metrics.csv
```

### Workflow de Calidad
1. **Static Analysis**: Ejecutar análisis estático
2. **Metrics Collection**: Recopilar métricas
3. **Test Coverage**: Verificar cobertura de tests
4. **Documentation Check**: Validar documentación
5. **Quality Gates**: Aplicar quality gates
6. **Report Generation**: Generar reportes
7. **Trend Analysis**: Analizar tendencias
8. **Action Plan**: Crear plan de mejora

### Quality Checklist
- [ ] Complejidad ciclomática < 15
- [ ] Cobertura de tests > 80%
- [ ] Archivos < 300 líneas
- [ ] Métodos < 50 líneas
- [ ] Documentación > 70%
- [ ] Cero code smells críticos
- [ ] Zero security vulnerabilities
- [ ] Performance benchmarks met
- [ ] All quality gates passing
- [ ] Technical debt < 5%
