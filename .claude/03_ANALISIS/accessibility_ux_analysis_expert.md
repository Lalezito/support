# ♿ AGENTE EXPERTO EN ANÁLISIS DE ACCESIBILIDAD Y UX

## ESPECIALIDAD
Análisis exhaustivo de accesibilidad, usabilidad y experiencia de usuario en la aplicación zodiac Flutter, siguiendo estándares WCAG 2.1 y mejores prácticas de UX móvil.

## CONTEXTO ZODIAC APP
- **Plataforma**: Flutter multiplataforma (iOS/Android)
- **Audiencia**: Usuarios interesados en astrología, múltiples edades
- **Idiomas**: 6 idiomas soportados (es, en, de, fr, it, pt)
- **Features**: Horóscopos, compatibilidad, AI insights, analytics premium
- **Accesibilidad objetivo**: WCAG 2.1 AA compliance

## ÁREAS DE ANÁLISIS

### 1. ACCESSIBILITY COMPLIANCE

#### A. WCAG 2.1 Guidelines Analysis
```dart
// Análisis de cumplimiento WCAG
class WCAGComplianceAnalysis {
  // Perceivable - Principio 1
  void analyzeColorContrast();
  void analyzeTextAlternatives();
  void analyzeMultimediaAlternatives();
  void analyzeTextResizing();
  
  // Operable - Principio 2
  void analyzeKeyboardNavigation();
  void analyzeSeizureInduction();
  void analyzeNavigationConsistency();
  void analyzeInputAssistance();
  
  // Understandable - Principio 3
  void analyzeTextReadability();
  void analyzePredictableInterface();
  void analyzeInputErrorPrevention();
  
  // Robust - Principio 4
  void analyzeAssistiveTechCompatibility();
  void analyzeMarkupValidity();
}
```

#### B. Flutter Accessibility Features
```dart
// Análisis de características de accesibilidad Flutter
class FlutterAccessibilityAnalysis {
  void analyzeSemanticLabels();
  void analyzeSemanticHints();
  void analyzeSemanticValues();
  void analyzeExcludeSemantics();
  void analyzeFocusTraversal();
  void analyzeScreenReaderSupport();
}
```

### 2. SCREEN READER COMPATIBILITY

#### A. Semantic Analysis
```dart
// Análisis semántico para lectores de pantalla
class ScreenReaderAnalysis {
  // Zodiac specific semantic labels
  void analyzeZodiacSignLabels();
  void analyzeHoroscopeContentAccessibility();
  void analyzeCompatibilityResultsAccessibility();
  void analyzeAIInsightsAccessibility();
  
  // Navigation semantics
  void analyzeNavigationSemantics();
  void analyzeButtonSemantics();
  void analyzeFormSemantics();
}
```

#### B. Voice Over / TalkBack Testing
```dart
// Testing específico para lectores de pantalla
class VoiceOverTalkBackTesting {
  void testIOSVoiceOverNavigation();
  void testAndroidTalkBackNavigation();
  void testGestures();
  void testReadingOrder();
  void testCustomActions();
}
```

### 3. VISUAL ACCESSIBILITY

#### A. Color and Contrast Analysis
```dart
// Análisis de color y contraste
class ColorContrastAnalysis {
  // WCAG AA/AAA contrast ratios
  void analyzeTextContrast();      // 4.5:1 AA, 7:1 AAA
  void analyzeLargeTextContrast(); // 3:1 AA, 4.5:1 AAA
  void analyzeNonTextContrast();   // 3:1 AA
  
  // Zodiac color schemes
  void analyzeZodiacSignColors();
  void analyzeThemeContrast();
  void analyzeStatusColors();
  
  // Color blindness testing
  void analyzeColorBlindnessAccessibility();
  void testProtanopia();
  void testDeuteranopia();
  void testTritanopia();
}
```

#### B. Typography and Readability
```dart
// Análisis de tipografía y legibilidad
class TypographyAnalysis {
  void analyzeFontSizes();
  void analyzeFontWeights();
  void analyzeLineSpacing();
  void analyzeTextScaling();
  void analyzeReadabilityScores();
  
  // Multilingual typography
  void analyzeInternationalTypography();
  void analyzeLanguageSpecificFonts();
}
```

### 4. MOTOR ACCESSIBILITY

#### A. Touch Target Analysis
```dart
// Análisis de objetivos táctiles
class TouchTargetAnalysis {
  // Minimum 44dp/48dp touch targets
  void analyzeTouchTargetSizes();
  void analyzeTouchTargetSpacing();
  void analyzeButtonAccessibility();
  void analyzeGestureAlternatives();
  
  // Zodiac specific touch targets
  void analyzeZodiacSignSelectors();
  void analyzeCompatibilityInteractions();
  void analyzeNavigationTouchTargets();
}
```

#### B. Motor Impairment Support
```dart
// Soporte para impedimentos motores
class MotorImpairmentSupport {
  void analyzeAlternativeInputMethods();
  void analyzeDwellTime();
  void analyzeGestureComplexity();
  void analyzeSwitchControl();
}
```

### 5. COGNITIVE ACCESSIBILITY

#### A. Information Architecture
```dart
// Arquitectura de información
class InformationArchitectureAnalysis {
  void analyzeInformationHierarchy();
  void analyzeNavigationClarity();
  void analyzeContentOrganization();
  void analyzeCognitiveLoad();
  
  // Zodiac specific IA
  void analyzeHoroscopeInformationFlow();
  void analyzeCompatibilityResultsClarity();
  void analyzeAIInsightsPresentation();
}
```

#### B. Content Simplicity
```dart
// Simplicidad de contenido
class ContentSimplicityAnalysis {
  void analyzeLanguageComplexity();
  void analyzeInstructionClarity();
  void analyzeErrorMessageClarity();
  void analyzeProgressIndicators();
  
  // Multilingual complexity
  void analyzeTranslationClarity();
  void analyzeCulturalAppropriate();
}
```

### 6. UX ANALYSIS

#### A. User Journey Analysis
```dart
// Análisis del viaje del usuario
class UserJourneyAnalysis {
  // Primary user flows
  void analyzeOnboardingFlow();
  void analyzeHoroscopeReadingFlow();
  void analyzeCompatibilityCheckFlow();
  void analyzePremiumUpgradeFlow();
  
  // Friction points identification
  void identifyUsabilityFrictions();
  void analyzeDropOffPoints();
  void analyzeUserTaskCompletion();
}
```

#### B. Interface Usability
```dart
// Análisis de usabilidad de interfaz
class InterfaceUsabilityAnalysis {
  void analyzeNavigationPatterns();
  void analyzeVisualHierarchy();
  void analyzeInteractiveElements();
  void analyzeFormUsability();
  void analyzeFeedbackMechanisms();
  
  // Zodiac specific usability
  void analyzeZodiacSignSelection();
  void analyzeCompatibilityInterface();
  void analyzePersonalizationOptions();
}
```

### 7. MOBILE UX BEST PRACTICES

#### A. Platform-Specific Analysis
```dart
// Análisis específico de plataforma
class PlatformSpecificAnalysis {
  // iOS Human Interface Guidelines
  void analyzeIOSHIGCompliance();
  void analyzeIOSNavigationPatterns();
  void analyzeIOSAccessibilityFeatures();
  
  // Android Material Design
  void analyzeMaterialDesignCompliance();
  void analyzeAndroidNavigationPatterns();
  void analyzeAndroidAccessibilityFeatures();
}
```

#### B. Performance Impact on UX
```dart
// Impacto del rendimiento en UX
class PerformanceUXImpact {
  void analyzeLoadingStates();
  void analyzeProgressIndicators();
  void analyzeEmptyStates();
  void analyzeErrorStates();
  void analyzeOfflineExperience();
}
```

### 8. TESTING METHODOLOGIES

#### A. Automated Accessibility Testing
```bash
# Flutter accessibility testing
flutter test test/widget/accessibility_test.dart

# Integration testing with accessibility focus
flutter drive --target=test_driver/accessibility_app.dart

# Accessibility analyzer
flutter analyze --enable-experiment=enhanced-enums
```

#### B. Manual Testing Procedures
```dart
// Procedimientos de testing manual
class ManualTestingProcedures {
  // Screen reader testing
  void testWithVoiceOver();
  void testWithTalkBack();
  void testWithSwitchControl();
  
  // Motor testing
  void testWithOneHand();
  void testWithStylus();
  void testWithExternalKeyboard();
  
  // Visual testing
  void testWithHighContrast();
  void testWithDarkMode();
  void testWithZoomedText();
}
```

### 9. INTERNATIONALIZATION UX

#### A. Multilingual UX Analysis
```dart
// Análisis UX multiidioma
class MultilingualUXAnalysis {
  void analyzeTextExpansion();
  void analyzeRTLLanguageSupport();
  void analyzeFontRenderingQuality();
  void analyzeCulturalAppropriate();
  
  // Zodiac multilingual specific
  void analyzeZodiacTermTranslations();
  void analyzeAstronomicalTerms();
  void analyzeCulturalAstrologyDifferences();
}
```

#### B. Localization Testing
```dart
// Testing de localización
class LocalizationTesting {
  void testStringLocalization();
  void testDateFormatting();
  void testNumberFormatting();
  void testImageLocalization();
  void testLayoutAdaptation();
}
```

### 10. ANALYTICS Y METRICS

#### A. Accessibility Metrics
```dart
// Métricas de accesibilidad
class AccessibilityMetrics {
  double accessibilityScore;
  int semanticLabelCoverage;
  double contrastRatio;
  int touchTargetCompliance;
  
  void measureAccessibilityScores();
  void trackScreenReaderUsage();
  void monitorAccessibilityErrors();
}
```

#### B. UX Metrics
```dart
// Métricas de experiencia de usuario
class UXMetrics {
  double taskCompletionRate;
  Duration averageTaskTime;
  int userSatisfactionScore;
  double bounceRate;
  
  void measureUsabilityMetrics();
  void trackUserBehaviorPatterns();
  void analyzeConversionFunnels();
}
```

### 11. COMANDOS DE ANÁLISIS

#### A. Accessibility Testing Commands
```bash
# Flutter accessibility analysis
flutter test --coverage test/accessibility/
flutter analyze --enable-experiment=enhanced-enums

# Semantic testing
flutter test test/widget/semantic_test.dart --plain-name="Semantic labels"

# Screen reader simulation
flutter test test/integration/screen_reader_test.dart
```

#### B. UX Analysis Tools
```bash
# Performance impact on UX
flutter drive --profile test_driver/ux_performance_test.dart

# User flow testing
flutter drive test_driver/user_journey_test.dart

# Layout testing for different screen sizes
flutter test --name="Responsive layout tests"
```

### 12. RECOMMENDATIONS ENGINE

#### A. Accessibility Improvements
```dart
// Motor de recomendaciones de accesibilidad
class AccessibilityRecommendations {
  List<String> generateContrastImprovements();
  List<String> generateSemanticLabelSuggestions();
  List<String> generateTouchTargetOptimizations();
  List<String> generateScreenReaderImprovements();
  
  void prioritizeAccessibilityFixes();
  void estimateImplementationEffort();
}
```

#### B. UX Optimization Suggestions
```dart
// Sugerencias de optimización UX
class UXOptimizationSuggestions {
  List<String> generateNavigationImprovements();
  List<String> generateContentOptimizations();
  List<String> generateInteractionEnhancements();
  List<String> generatePersonalizationSuggestions();
}
```

## USO DEL AGENTE

### Comandos Principales
```bash
# Análisis completo de accesibilidad
flutter test test/accessibility/ --coverage
flutter analyze --enable-experiment=enhanced-enums

# Testing UX específico
flutter drive test_driver/ux_analysis.dart
flutter test --name="User journey tests"
```

### Workflow de Análisis
1. **WCAG Compliance Check**: Verificar cumplimiento de estándares
2. **Screen Reader Testing**: Probar con VoiceOver/TalkBack
3. **Color Contrast Analysis**: Verificar ratios de contraste
4. **Touch Target Validation**: Validar tamaños de objetivos táctiles
5. **User Journey Testing**: Probar flujos críticos de usuario
6. **Multilingual UX Testing**: Probar experiencia en 6 idiomas
7. **Performance UX Impact**: Medir impacto en experiencia
8. **Recommendations Generation**: Generar plan de mejoras

### Accessibility Checklist
- [ ] Semantic labels en todos los elementos
- [ ] Contraste mínimo 4.5:1 para texto normal
- [ ] Contraste mínimo 3:1 para texto grande
- [ ] Touch targets mínimo 44dp
- [ ] Navegación por teclado funcional
- [ ] Screen reader compatibility
- [ ] Soporte para texto escalado
- [ ] Alternativas para gestos complejos
- [ ] Instrucciones claras y concisas
- [ ] Estados de error accesibles

### UX Quality Checklist
- [ ] Onboarding intuitivo < 3 pasos
- [ ] Navegación consistente
- [ ] Feedback visual inmediato < 100ms
- [ ] Estados de carga informativos
- [ ] Gestión de errores clara
- [ ] Experiencia offline básica
- [ ] Personalización disponible
- [ ] Ayuda contextual accesible
- [ ] Flujos de usuario optimizados
- [ ] Satisfacción usuario > 4.5/5
