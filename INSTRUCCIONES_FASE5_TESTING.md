# 🧪 INSTRUCCIONES PARA FASE 5: TESTING MULTIIDIOMA

**Para:** AGENTE 9 - QA Tester
**De:** AGENTE 8 - Integrador
**Fecha:** Noviembre 16, 2025
**Estado Actual:** FASE 4 completada al 100%

---

## 📍 Contexto Rápido

El archivo `context_aware_goal_generator.dart` ha sido **completamente refactorizado** para usar traducciones multiidioma. Ahora necesitamos **verificar que todo funciona correctamente en los 6 idiomas**.

---

## 🎯 Tu Misión

Crear una suite de tests que verifique:
1. ✅ Todos los goals se generan en los 6 idiomas
2. ✅ La estructura de datos es consistente
3. ✅ Las variables zodiacales se interpolan correctamente
4. ✅ No hay errores de runtime

---

## 📁 Archivos Clave

### Para Leer (Contexto)
1. `/lib/services/cosmic_coach/context_aware_goal_generator.dart` (224 líneas)
2. `/lib/services/cosmic_coach/context_aware_goal_translations.dart` (3,036 líneas)
3. `FASE_4_INTEGRACION_COMPLETE_NOV16.md` (este reporte)

### Para Crear (Testing)
1. `/test/services/cosmic_coach/context_aware_goal_generator_test.dart`
2. `/test/services/cosmic_coach/context_aware_goal_translations_test.dart`

---

## 🧪 Tests a Implementar

### 1. Sleep Goals Testing (7 tests × 6 idiomas = 42 tests)

```dart
group('Sleep Goals - Excellent (7-9h)', () {
  test('generates excellent sleep goals in English', () {
    final goals = ContextAwareGoalGenerator.generateSleepGoals(
      'aries',
      8.0,
      'en',
    );

    expect(goals.length, 2); // 2 goals
    expect(goals[0]['title'], contains('Peak Energy'));
    expect(goals[1]['title'], contains('Sleep Wins'));
  });

  test('generates excellent sleep goals in Spanish', () {
    final goals = ContextAwareGoalGenerator.generateSleepGoals(
      'aries',
      8.0,
      'es',
    );

    expect(goals.length, 2);
    expect(goals[0]['title'], contains('Energía'));
    expect(goals[1]['title'], contains('Victorias'));
  });

  // Repetir para: pt, fr, de, it
});

group('Sleep Goals - Deprived (<6h)', () {
  // Similar tests para sleepDeprivedGoals
});

group('Sleep Goals - Too Much (>9h)', () {
  // Similar tests para tooMuchSleepGoals
});

group('Sleep Goals - Decent (6-7h)', () {
  // Similar tests para decentSleepGoals
});
```

### 2. Emotional Goals Testing (9 tests × 6 idiomas = 54 tests)

```dart
group('Emotional Goals - Stressed', () {
  test('generates stressed goal in all languages', () {
    for (final lang in ['en', 'es', 'pt', 'fr', 'de', 'it']) {
      final goals = ContextAwareGoalGenerator.generateEmotionalGoals(
        'leo',
        'stressed',
        lang,
      );

      expect(goals.length, 1);
      expect(goals[0]['category'], 'wellness');
      expect(goals[0]['microHabits'], isNotEmpty);
    }
  });
});

// Repetir para: anxious, calm, energized, tired, motivated,
// unmotivated, confident, uncertain
```

### 3. Zodiac Sign Testing (12 signos × 2 funciones × 6 idiomas = 144 tests)

```dart
group('Zodiac Sign Interpolation', () {
  final signs = [
    'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
  ];

  test('all zodiac signs work in sleep goals', () {
    for (final sign in signs) {
      for (final lang in ['en', 'es', 'pt', 'fr', 'de', 'it']) {
        final goals = ContextAwareGoalGenerator.generateSleepGoals(
          sign,
          8.0,
          lang,
        );

        expect(goals, isNotEmpty);
        expect(goals[0], containsPair('title', isNotNull));
      }
    }
  });
});
```

### 4. Data Structure Validation

```dart
group('Data Structure Validation', () {
  test('all goals have required fields', () {
    final goals = ContextAwareGoalGenerator.generateSleepGoals(
      'aries',
      8.0,
      'en',
    );

    for (final goal in goals) {
      // Required fields
      expect(goal['title'], isNotNull);
      expect(goal['description'], isNotNull);
      expect(goal['category'], isNotNull);
      expect(goal['microHabits'], isNotNull);
      expect(goal['successIndicators'], isNotNull);

      // microHabits structure
      final microHabits = goal['microHabits'] as List;
      for (final habit in microHabits) {
        expect(habit['habit'], isNotNull);
        expect(habit['when'], isNotNull);
        expect(habit['why'], isNotNull);
      }
    }
  });
});
```

### 5. Edge Cases

```dart
group('Edge Cases', () {
  test('handles unknown zodiac sign gracefully', () {
    final goals = ContextAwareGoalGenerator.generateSleepGoals(
      'unknown_sign',
      8.0,
      'en',
    );

    expect(goals, isNotEmpty); // Should fallback
  });

  test('handles unknown emotional state gracefully', () {
    final goals = ContextAwareGoalGenerator.generateEmotionalGoals(
      'aries',
      'unknown_state',
      'en',
    );

    expect(goals, isNotEmpty); // Should fallback to calm
  });

  test('handles unknown language code', () {
    final goals = ContextAwareGoalGenerator.generateSleepGoals(
      'aries',
      8.0,
      'xx', // Unknown lang
    );

    expect(goals, isNotEmpty); // Should fallback to English
  });
});
```

---

## 📊 Coverage Esperado

```
Total Tests: ~240
├── Sleep Goals: 42 tests
├── Emotional Goals: 54 tests
├── Zodiac Signs: 144 tests
├── Data Structure: 10 tests
├── Edge Cases: 5 tests
└── Integration: 15 tests
```

**Target Coverage:** 95%+

---

## 🚀 Comandos para Ejecutar

### Run All Tests
```bash
flutter test test/services/cosmic_coach/
```

### Run Specific Test File
```bash
flutter test test/services/cosmic_coach/context_aware_goal_generator_test.dart
```

### Run with Coverage
```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

---

## ✅ Criterios de Éxito

Para considerar FASE 5 completa:

- [ ] **240+ tests creados** (sleep + emotional + zodiac + edge cases)
- [ ] **Todos los tests pasan** (0 failing tests)
- [ ] **Coverage >95%** en generator y translations
- [ ] **Todos los idiomas verificados** (en, es, pt, fr, de, it)
- [ ] **Estructura de datos validada** (campos requeridos)
- [ ] **Edge cases cubiertos** (fallbacks funcionan)
- [ ] **Documentación de tests** (comentarios claros)

---

## 📝 Checklist de Testing

### Sleep Goals
- [ ] Excellent sleep (7-9h) en 6 idiomas
- [ ] Sleep deprived (<6h) en 6 idiomas
- [ ] Too much sleep (>9h) en 6 idiomas
- [ ] Decent sleep (6-7h) en 6 idiomas

### Emotional Goals
- [ ] Stressed en 6 idiomas
- [ ] Anxious en 6 idiomas
- [ ] Calm en 6 idiomas
- [ ] Energized en 6 idiomas
- [ ] Tired en 6 idiomas
- [ ] Motivated en 6 idiomas
- [ ] Unmotivated en 6 idiomas
- [ ] Confident en 6 idiomas
- [ ] Uncertain en 6 idiomas

### Zodiac Signs
- [ ] Todos los 12 signos funcionan
- [ ] Sleep quality phrases por signo
- [ ] Motivational messages por signo

### Validación
- [ ] Estructura de datos consistente
- [ ] microHabits tienen campos requeridos
- [ ] successIndicators no vacíos
- [ ] Variables interpoladas correctamente

### Edge Cases
- [ ] Signo desconocido → fallback
- [ ] Estado desconocido → fallback to calm
- [ ] Idioma desconocido → fallback to English
- [ ] Horas negativas → manejo
- [ ] Horas > 24 → manejo

---

## 🎯 Ejemplo de Test Completo

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:zodiac_app/services/cosmic_coach/context_aware_goal_generator.dart';

void main() {
  group('ContextAwareGoalGenerator', () {
    group('Sleep Goals - Excellent (7-9h)', () {
      test('generates 2 goals for excellent sleep in English', () {
        final goals = ContextAwareGoalGenerator.generateSleepGoals(
          'aries',
          8.0,
          'en',
        );

        expect(goals.length, 2);
        expect(goals[0]['title'], contains('Peak Energy'));
        expect(goals[0]['description'], contains('warrior-quality'));
        expect(goals[0]['microHabits'], hasLength(2));
        expect(goals[1]['title'], contains('Sleep Wins'));
      });

      test('generates goals with correct structure', () {
        final goals = ContextAwareGoalGenerator.generateSleepGoals(
          'leo',
          8.5,
          'es',
        );

        for (final goal in goals) {
          expect(goal, containsPair('title', isA<String>()));
          expect(goal, containsPair('description', isA<String>()));
          expect(goal, containsPair('category', 'sleep'));
          expect(goal, containsPair('microHabits', isA<List>()));
          expect(goal, containsPair('successIndicators', isA<List>()));

          final microHabits = goal['microHabits'] as List;
          for (final habit in microHabits) {
            expect(habit, containsPair('habit', isA<String>()));
            expect(habit, containsPair('when', isA<String>()));
            expect(habit, containsPair('why', isA<String>()));
          }
        }
      });
    });
  });
}
```

---

## 🛠️ Herramientas Recomendadas

### Testing
```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  mockito: ^5.4.0
  test: ^1.24.0
```

### Coverage
```bash
# Instalar lcov
brew install lcov  # macOS
apt-get install lcov  # Linux

# Generar coverage
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
```

---

## 📚 Referencias Útiles

1. **Flutter Testing Docs:** https://docs.flutter.dev/testing
2. **Mockito:** https://pub.dev/packages/mockito
3. **Test Coverage:** https://docs.flutter.dev/testing/code-coverage
4. **FASE 4 Report:** `FASE_4_INTEGRACION_COMPLETE_NOV16.md`

---

## ⏱️ Tiempo Estimado

- **Setup tests:** 30 min
- **Sleep goals tests:** 45 min
- **Emotional goals tests:** 45 min
- **Zodiac + edge cases:** 30 min
- **Documentation:** 30 min
- **TOTAL:** ~3 horas

---

## 🎁 Entregables Esperados

1. ✅ `context_aware_goal_generator_test.dart` (240+ tests)
2. ✅ `context_aware_goal_translations_test.dart` (helper functions)
3. ✅ `FASE_5_TESTING_COMPLETE_NOV16.md` (reporte de testing)
4. ✅ Coverage report (>95%)
5. ✅ Test execution screenshot

---

## 🚨 Posibles Problemas y Soluciones

### Problema 1: Tests fallan por estructura de datos
**Solución:** Verificar que translations devuelven Map<String, dynamic>

### Problema 2: Interpolación de variables falla
**Solución:** Verificar que zodiac sign se pasa correctamente a translations

### Problema 3: Coverage bajo
**Solución:** Agregar tests para edge cases y todas las combinaciones

### Problema 4: Tests lentos
**Solución:** Usar setUp() para datos comunes, evitar repetición

---

## ✨ Consejos Finales

1. **Empieza con un test simple** que compile y pase
2. **Usa data-driven tests** para evitar repetición
3. **Verifica TODOS los idiomas** en cada test importante
4. **Documenta edge cases** encontrados
5. **Reporta inconsistencias** en traducciones si las encuentras

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa `FASE_4_INTEGRACION_COMPLETE_NOV16.md` para contexto
2. Verifica que backup existe: `.backup_nov16`
3. Consulta estructura en `VISUAL_COMPARISON_FASE4.md`

---

**¡Adelante, AGENTE 9! El código está listo para ser testeado. 🧪**

---

_Preparado por: AGENTE 8 - Integrador_
_Fecha: Noviembre 16, 2025_
_Next: FASE 5 - Testing Multiidioma_
