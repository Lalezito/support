# 🔍 PROBLEMA ACTUAL - COSMIC COACH (Noviembre 12, 2025 - 21:17)

## Reporte del Usuario

"Vamos por partes. ¿Podemos hacer que donde dice 'acción hacia tus metas' haya otra cosa?"

"Y después, volver para atrás donde estaban las metas ya anteriores. Estaban completas las estadísticas. Dejarla como estaban antes, porque ahora se borran cada vez que entramos ahí. Se mantienen. A ver, a ver bien la racha, no se está manteniendo igual. Pero se mantienen las estadísticas. Pero hay que hacer que se mantenga la racha también. Y el tema de las metas, cambiamelo ahí que me diga otra nueva meta acción hacia tus metas, igual que sea algo distinto a eso."

---

## Problemas Identificados

### 1. ❌ "Acciones hacia tus metas" (Texto Genérico)
**Status**: BLOQUEANTE

**Qué está pasando**:
- Los goals muestran texto genérico "acciones hacia tus metas"
- NO muestran biorhythm goals específicos como:
  - "⚡ Rendimiento Físico Máximo"
  - "💤 Fase de Recuperación Física"
  - "🧠 Pico Intelectual"

**Por qué sucede**:
- El provider tiene goals VIEJOS cargados del storage (SharedPreferences)
- Aunque `_loadCoachData()` genera goals nuevos con Enhanced Adapter, el UI muestra los viejos
- El provider lee goals del disco ANTES de que se generen los nuevos

**Intentos de Fix**:
1. ✅ Comenté `await loadGoals()` en `_initialize()` del provider
2. ❌ PERO ahora los goals están VACÍOS en lugar de mostrar los nuevos

**Root Cause REAL**:
El provider NO está inicializando `_currentGoals` con los goals del Enhanced Adapter. La lista está vacía porque:
- `_initialize()` ya NO carga goals viejos (comentado)
- Pero `_currentGoals` se queda como lista vacía `[]`
- Cuando la UI lee `provider.currentGoals`, obtiene lista vacía
- La UI renderiza goals vacíos con texto placeholder "acciones hacia tus metas"

---

### 2. ❌ Estadísticas se Borran
**Status**: RESUELTO PARCIALMENTE

**Qué reporta el usuario**:
- "Se mantienen las estadísticas" ✅
- "La racha no se está manteniendo igual" ❌

**Fix aplicado**:
- Removí `await goalsProvider.clearAllData()` de `_loadCoachData()`
- Ahora solo llama a `setGoals()` sin borrar estadísticas

**Problema restante**: La racha (streak) no se mantiene

---

## Solución Correcta

### Cambio en Provider (`cosmic_goals_provider.dart`)

El provider debe:
1. ✅ NO cargar goals viejos en `_initialize()` - Ya hecho
2. ✅ Cargar estadísticas en `_initialize()` - Ya hecho
3. ✅ Esperar que `_loadCoachData()` llame `setGoals()` con goals nuevos - Ya hecho
4. ❌ **PERO**: Asegurar que los goals se generen INMEDIATAMENTE al abrir la pantalla

### Cambio en Screen (`cosmic_coach_screen.dart`)

El problema es el TIMING:
```dart
// Actual:
initState() {
  _initializeService();  // Async - no esperamos
}

Future<void> _initializeService() async {
  await _loadCoachData();  // Genera goals
}
```

El problema es que `initState()` NO espera a que `_initializeService()` termine.

**Solución**: Usar `FutureBuilder` o cargar goals en `build()` si están vacíos.

---

## Próximos Pasos

### 1. Verificar que goals se generen al abrir pantalla
- Agregar logging para ver CUÁNDO se llama `_loadCoachData()`
- Verificar que `setGoals()` se ejecute ANTES de que la UI renderice

### 2. Implementar fallback si goals vacíos
```dart
if (goalsProvider.currentGoals.isEmpty) {
  // Mostrar loader o generar goals ahora
}
```

### 3. Fix de racha (streak)
- Investigar por qué la racha no se mantiene
- Verificar que `loadStatistics()` cargue correctamente el streak

---

## Estado de la Compilación

**Actualmente**: Instalando app en iPhone con fixes de provider
**Esperando**: Ver si ahora los goals se generan correctamente

**Archivos Modificados**:
1. `lib/providers/cosmic_goals_provider.dart` - Comentado `await loadGoals()` en `_initialize()`
2. `lib/screens/cosmic_coach_screen.dart` - Removido `clearAllData()`

---

**Fecha**: Noviembre 12, 2025 - 21:17 hrs
**Status**: Debugging en progreso
**Bloqueante**: Goals no muestran texto específico
