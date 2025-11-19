# ⚠️ CRITICAL: DO NOT CHANGE - Enhanced Coach Adapter

**Fecha**: 13 de Noviembre, 2025
**Archivo**: `/lib/services/cosmic_coach/enhanced_coach_adapter.dart`

---

## 🚨 NUNCA CAMBIAR ESTE CÓDIGO

En el archivo `enhanced_coach_adapter.dart`, línea 50, hay una llamada a:

```dart
final rawGoals = _service.generateCompleteGoalSet(
  sign: sign,
  context: context,
  birthDate: birthDate,
  languageCode: languageCode,
);
```

### ⚠️ REGLA ABSOLUTA:

**NUNCA cambiar `generateCompleteGoalSet` por `generateBiorhythmGoals`**

---

## ❌ LO QUE NO SE DEBE HACER

```dart
// ❌ INCORRECTO - NO HACER ESTO:
final rawGoals = _service.generateBiorhythmGoals(
  sign: sign,
  birthDate: birthDate,
  languageCode: languageCode,
);
```

**Problema**: Esto genera SOLO 1-2 goals de biorritmos (físico/emocional/intelectual).

---

## ✅ LO CORRECTO

```dart
// ✅ CORRECTO - SIEMPRE USAR ESTO:
final rawGoals = _service.generateCompleteGoalSet(
  sign: sign,
  context: context,
  birthDate: birthDate,
  languageCode: languageCode,
);
```

**Por qué**: Esto genera 5+ goals completos que incluyen:
1. Context-aware goals (basados en sueño, emociones, energía)
2. Zodiac-specific goals (shadow work, superpowers)
3. Micro-habits (2 por signo)
4. Biorhythm goals (ciclos físicos, emocionales, intelectuales)

---

## 🎯 QUÉ HACE CADA MÉTODO

### `generateCompleteGoalSet` (✅ USAR ESTE)

Genera set COMPLETO de goals:
- **Sleep goals**: "Recupera tu energía física" (si duermes poco)
- **Emotion goals**: "Maneja tu estrés" (si estás estresado)
- **Zodiac goals**: "Desarrolla tu poder de liderazgo" (Aries)
- **Micro-habits**: "5 minutos de meditación"
- **Biorhythm goals**: "Día Físico Crítico" (basado en ciclo de 23 días)

**Resultado**: 5-7 goals variados y personalizados

### `generateBiorhythmGoals` (❌ NO USAR SOLO)

Genera SOLO goals de ciclos:
- **Physical cycle** (23 días)
- **Emotional cycle** (28 días)
- **Intellectual cycle** (33 días)

**Resultado**: 1-2 goals (muy poco)

---

## 📊 COMPARACIÓN

### Con `generateCompleteGoalSet` (✅ CORRECTO):

```
Usuario ve:
1. Recupera tu energía física (context: sleep)
2. Maneja tu estrés diario (context: emotion)
3. Desarrolla tu poder de liderazgo (zodiac: Aries)
4. 5 minutos de meditación (micro-habit)
5. Camina 10 minutos al día (micro-habit)
6. Día Físico Crítico - descansa (biorhythm)
7. Pico Emocional - conéctate (biorhythm)

Total: 7 goals ✅
```

### Con `generateBiorhythmGoals` (❌ INCORRECTO):

```
Usuario ve:
1. Día Físico Crítico - descansa (biorhythm)

Total: 1 goal ❌
```

---

## 🐛 HISTORIAL DEL BUG

### Noviembre 13, 2025 - 11:00 PM

**Reportado por usuario**:
> "Solo veo una meta genérica 'Acción hacia tus metas'"

**Investigación**:
El código estaba usando `generateCompleteGoalSet` correctamente, PERO los goals guardados en el iPhone eran de versión antigua (antes de biorritmos).

**Solución**:
Implementé sistema de versiones en `goal_persistence_service.dart` para detectar y limpiar goals viejos automáticamente.

**IMPORTANTE**:
El código del adapter está CORRECTO. Si el usuario reporta goals genéricos, el problema NO es el adapter, es que hay goals viejos guardados en storage.

---

## ✅ VERIFICACIÓN

Si necesitas verificar que el código está correcto:

```bash
# Buscar la llamada en enhanced_coach_adapter.dart
grep -n "generateCompleteGoalSet" lib/services/cosmic_coach/enhanced_coach_adapter.dart

# Debe retornar:
# 50:      final rawGoals = _service.generateCompleteGoalSet(
```

Si ves `generateBiorhythmGoals`, ESTÁ MAL y debe cambiarse a `generateCompleteGoalSet`.

---

## 📝 CHECKLIST PARA CAMBIOS FUTUROS

Antes de modificar `enhanced_coach_adapter.dart`:

- [ ] ¿El cambio mantiene `generateCompleteGoalSet`?
- [ ] ¿No estoy cambiando a `generateBiorhythmGoals`?
- [ ] ¿Los users seguirán viendo 5+ goals?
- [ ] ¿Leí este documento de advertencia?

Si alguna respuesta es NO, **NO HACER EL CAMBIO**.

---

## 🎯 RESUMEN

**Regla de Oro**:
> Siempre usar `generateCompleteGoalSet` en el EnhancedCoachAdapter.
> Nunca cambiar a `generateBiorhythmGoals` solo.

**Razón**:
> Users esperan ver múltiples goals variados (sueño, emoción, zodiac, hábitos, biorritmos).
> Si solo usas biorritmos, verán 1-2 goals y se quejarán.

**Si hay problema con goals genéricos**:
> El problema NO es el adapter.
> El problema es que hay goals viejos guardados en storage.
> Solución: Sistema de versiones en `goal_persistence_service.dart`.

---

**RECUERDA**: Este es uno de los bugs más confusos. El código está bien, pero goals viejos en storage causan el problema. No toques el adapter.
