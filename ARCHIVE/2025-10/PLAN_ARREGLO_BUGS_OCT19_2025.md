# Plan de Arreglo de Bugs - Octubre 19, 2025

**Fecha de creación:** 19 de Octubre 2025
**Estado:** PLANIFICACIÓN
**Prioridad:** ALTA - Bugs críticos en funcionalidad premium

---

## 📋 TODO List General

- [ ] **FASE 1:** Análisis y Reproducción (Todos los bugs)
- [ ] **FASE 2:** Fixes Críticos (Bugs #1, #2, #3)
- [ ] **FASE 3:** Fixes UX (Bug #4)
- [ ] **FASE 4:** Clarificación y Fixes (Bug #5)
- [ ] **FASE 5:** Testing y Regresión
- [ ] **FASE 6:** Documentación y Deploy

---

## FASE 1: Análisis y Reproducción

### Objetivos
- Reproducir cada bug en entorno local
- Confirmar causa raíz
- Identificar archivos exactos a modificar

### TODO - Análisis

- [ ] **Bug #1: Fecha de nacimiento**
  - [ ] Reproducir: Ingresar fecha de nacimiento
  - [ ] Verificar: ¿Se guarda en BirthDataService?
  - [ ] Verificar: ¿Se guarda en PreferencesService?
  - [ ] Verificar: ¿AscendantProfileScreen lee correctamente?
  - [ ] Confirmar causa raíz: Desconexión entre servicios

- [ ] **Bug #2: Premium se bloquea**
  - [ ] Reproducir: Comprar premium desde PremiumScreen
  - [ ] Verificar: Estado en RevenueCatService
  - [ ] Verificar: Estado en Provider
  - [ ] Verificar: Actualización de UI en Settings
  - [ ] Confirmar causa raíz: Falta refresh del provider

- [ ] **Bug #3: Funciones de análisis bloqueadas**
  - [ ] Reproducir: Después de comprar, acceder a análisis
  - [ ] Verificar: PremiumFeatureGate checks
  - [ ] Verificar: FeatureGateService estado
  - [ ] Confirmar causa raíz: Cache del feature gate

- [ ] **Bug #4: Cosmic Coach en inglés**
  - [ ] Reproducir: Acceder a Cosmic Coach con app en español
  - [ ] Verificar: ¿Usa AppLocalizations?
  - [ ] Verificar: ¿Respuestas de AI en qué idioma?
  - [ ] Confirmar causa raíz: Falta integración i18n

- [ ] **Bug #5: Realizar ritual**
  - [ ] Reproducir: Ejecutar "realizar ritual"
  - [ ] Documentar: ¿Qué hace exactamente?
  - [ ] Definir: ¿Es el comportamiento esperado?

**Duración estimada:** 1-2 horas

---

## FASE 2: Fixes Críticos

### Bug #1: Sincronizar BirthDataService con PreferencesService

**Archivos a modificar:**
```
lib/services/birth_data_service.dart
lib/services/preferences_service.dart
lib/screens/birth_data_collection_screen.dart
```

**Plan de fix:**

1. **Opción A: Usar solo BirthDataService (RECOMENDADO)**
   - [ ] Modificar `AscendantProfileScreen` para leer de `BirthDataService`
   - [ ] Eliminar lectura de `PreferencesService.birthDate`
   - [ ] Usar `BirthDataService.instance.birthData?.birthDate`

2. **Opción B: Sincronizar ambos servicios**
   - [ ] En `BirthDataService.saveBirthData()`, también guardar en `PreferencesService`
   - [ ] Agregar:
   ```dart
   await PreferencesService.instance.setBirthDate(birthData.birthDate);
   if (birthData.birthTime != null) {
     await PreferencesService.instance.setBirthTime(
       '${birthData.birthTime!.hour}:${birthData.birthTime!.minute}'
     );
   }
   ```

**TODO - Implementación Bug #1:**
- [ ] Decidir entre Opción A o B
- [ ] Implementar cambios en archivos
- [ ] Agregar logs para debug
- [ ] Probar guardado de fecha
- [ ] Probar lectura en AscendantScreen

---

### Bug #2: Actualizar estado premium después de compra

**Archivos a modificar:**
```
lib/screens/premium_screen.dart
lib/providers/unified_premium_integration_provider.dart
lib/screens/settings_screen.dart
```

**Plan de fix:**

**En `premium_screen.dart` después de compra exitosa:**
```dart
// Después de purchasePackage() exitoso
if (mounted) {
  // Invalidar el provider para forzar refresh
  ref.invalidate(unifiedPremiumIntegrationProvider);

  // También invalidar feature gates
  ref.invalidate(featureGateServiceProvider);

  // Dar tiempo a que se actualice
  await Future.delayed(Duration(milliseconds: 500));

  // Navegar de vuelta
  Navigator.pop(context);
}
```

**TODO - Implementación Bug #2:**
- [ ] Localizar método de compra en `premium_screen.dart`
- [ ] Agregar `ref.invalidate()` después de compra
- [ ] Agregar delay para actualización
- [ ] Verificar que Settings se actualiza al volver
- [ ] Testing del flujo completo

---

### Bug #3: Refrescar Feature Gates

**Archivos a modificar:**
```
lib/services/feature_gate_service.dart
lib/widgets/monetization/premium_feature_gate.dart
```

**Plan de fix:**

**En `feature_gate_service.dart`:**
```dart
class FeatureGateService {
  // Agregar método para invalidar cache
  void invalidateCache() {
    _cacheTimestamp = null;
    _cachedIsPremium = null;
  }

  // Llamar desde RevenueCatService cuando cambia estado
}
```

**En `premium_feature_gate.dart`:**
```dart
@override
Widget build(BuildContext context, WidgetRef ref) {
  // Watch el provider para que se reconstruya automáticamente
  final isPremium = ref.watch(unifiedPremiumIntegrationProvider)
    .select((state) => state.isPremium);

  // Resto del código...
}
```

**TODO - Implementación Bug #3:**
- [ ] Agregar método `invalidateCache()` en FeatureGateService
- [ ] Modificar PremiumFeatureGate para usar `ref.watch()`
- [ ] Conectar invalidación con RevenueCatService
- [ ] Testing con múltiples feature gates

---

## FASE 3: Fixes UX

### Bug #4: Cosmic Coach en español

**Archivos a modificar:**
```
lib/services/cosmic_chat_service.dart
lib/services/consolidated_ai/coaching_ai_service.dart
lib/screens/cosmic_coach_screen.dart
lib/screens/cosmic_coach_chat_screen.dart
```

**Plan de fix:**

**En `coaching_ai_service.dart`:**
```dart
Future<String> generateCoachingResponse(
  String userMessage,
  BuildContext context,
) async {
  final locale = Localizations.localeOf(context);
  final language = locale.languageCode; // 'es', 'en', etc.

  // Agregar language al prompt de AI
  final systemPrompt = '''
  You are a cosmic life coach.
  Respond in ${_getLanguageName(language)} language.
  User's language: $language
  ''';

  // Resto del código...
}

String _getLanguageName(String code) {
  switch (code) {
    case 'es': return 'Spanish';
    case 'en': return 'English';
    case 'pt': return 'Portuguese';
    default: return 'English';
  }
}
```

**TODO - Implementación Bug #4:**
- [ ] Agregar detección de idioma en CoachingAIService
- [ ] Modificar prompts de AI para incluir idioma
- [ ] Agregar system message con idioma
- [ ] Testing con español, inglés, portugués
- [ ] Verificar respuestas consistentes en idioma correcto

---

## FASE 4: Clarificación y Fixes

### Bug #5: Funcionalidad "Realizar Ritual"

**TODO - Investigación:**
- [ ] Leer código de `goal_planner_home_screen.dart`
- [ ] Identificar qué hace el método `performRitual()`
- [ ] Documentar comportamiento esperado
- [ ] Verificar si es premium o free
- [ ] Decidir si necesita fix o solo traducción

**Posibles fixes:**
1. Si solo necesita traducción:
   - [ ] Agregar keys a `app_localizations_es.dart`
   - [ ] Traducir textos del ritual

2. Si tiene bugs funcionales:
   - [ ] Documentar bugs específicos
   - [ ] Crear plan de fix individual

---

## FASE 5: Testing y Regresión

### Testing Individual

**Bug #1: Fecha de nacimiento**
- [ ] Test: Ingresar fecha nueva
- [ ] Test: Verificar se guarda correctamente
- [ ] Test: Abrir AscendantScreen
- [ ] Test: Verificar muestra fecha correcta
- [ ] Test: Calcular ascendant correcto

**Bug #2: Estado premium**
- [ ] Test: Comprar premium desde PremiumScreen
- [ ] Test: Volver a Settings sin pasar por Home
- [ ] Test: Verificar features desbloqueadas
- [ ] Test: Verificar íconos premium visibles
- [ ] Test: Reiniciar app, verificar persiste

**Bug #3: Feature gates**
- [ ] Test: Acceder a Análisis después de compra
- [ ] Test: Acceder a Compatibilidad avanzada
- [ ] Test: Acceder a Cosmic Coach premium
- [ ] Test: Verificar todos desbloqueados
- [ ] Test: Verificar sin premium = bloqueado

**Bug #4: Traducciones Cosmic Coach**
- [ ] Test: App en español → Cosmic Coach en español
- [ ] Test: App en inglés → Cosmic Coach en inglés
- [ ] Test: App en portugués → Cosmic Coach en portugués
- [ ] Test: Cambiar idioma en runtime

### Testing de Regresión

**Flujo completo de onboarding + premium:**
- [ ] Onboarding nuevo usuario
- [ ] Ingresar fecha de nacimiento
- [ ] Ver horóscopo básico (free)
- [ ] Intentar feature premium (bloqueado)
- [ ] Comprar premium
- [ ] Verificar todo desbloqueado inmediatamente
- [ ] Cerrar y reabrir app
- [ ] Verificar premium persiste
- [ ] Usar Cosmic Coach en español
- [ ] Usar análisis avanzado
- [ ] Verificar ascendant correcto

**Flujo de edge cases:**
- [ ] Comprar premium sin fecha de nacimiento
- [ ] Comprar premium, cerrar app antes de confirmar
- [ ] Restaurar compras
- [ ] Cambiar idioma después de usar Cosmic Coach
- [ ] Borrar datos, volver a ingresar

---

## FASE 6: Documentación y Deploy

### Documentación

- [ ] Actualizar `BUGS_REPORTADOS_OCT19_2025.md` con fixes
- [ ] Documentar cambios en CHANGELOG.md
- [ ] Crear migration guide si cambian APIs
- [ ] Documentar nuevas pruebas agregadas

### Deploy

- [ ] Code review de todos los cambios
- [ ] Merge a branch de desarrollo
- [ ] Testing en TestFlight (iOS) / Internal Testing (Android)
- [ ] Verificar con usuarios beta
- [ ] Deploy a producción
- [ ] Monitorear errores en primeras 24h

---

## Estimación de Tiempo

| Fase | Duración Estimada |
|------|-------------------|
| FASE 1: Análisis | 1-2 horas |
| FASE 2: Fixes Críticos | 3-4 horas |
| FASE 3: Fixes UX | 2-3 horas |
| FASE 4: Clarificación | 1-2 horas |
| FASE 5: Testing | 2-3 horas |
| FASE 6: Documentación | 1 hora |
| **TOTAL** | **10-15 horas** |

---

## Orden de Ejecución Recomendado

### Día 1: Bugs Críticos
1. Bug #2: Premium se bloquea (MÁS CRÍTICO)
2. Bug #3: Feature gates bloqueados (depende de #2)
3. Bug #1: Fecha de nacimiento

### Día 2: UX y Testing
4. Bug #4: Cosmic Coach traducciones
5. Bug #5: Clarificar ritual
6. Testing completo
7. Documentación

---

## Notas de Implementación

### Consideraciones importantes:

1. **No romper compatibilidad hacia atrás**
   - Usuarios existentes con datos guardados deben seguir funcionando
   - Migración de datos si es necesario

2. **Testing en dispositivos reales**
   - iOS físico para probar compras
   - Android físico para probar compras
   - Diferentes versiones de OS

3. **Logging mejorado**
   - Agregar logs en puntos críticos
   - Ayudará a debuggear si aparecen nuevos bugs

4. **Rollback plan**
   - Mantener versión anterior funcional
   - Feature flags para activar/desactivar fixes

---

## Criterios de Éxito

✅ **Bug #1 resuelto cuando:**
- Fecha de nacimiento se guarda correctamente
- AscendantScreen muestra información correcta
- Ascendant se calcula automáticamente

✅ **Bug #2 resuelto cuando:**
- Compra de premium actualiza UI inmediatamente
- No se necesita volver a Home para ver cambios
- Estado persiste entre sesiones

✅ **Bug #3 resuelto cuando:**
- Todas las features premium se desbloquean inmediatamente
- No hay features que queden bloqueadas
- Feature gates funcionan correctamente

✅ **Bug #4 resuelto cuando:**
- Cosmic Coach responde en el idioma de la app
- Traducciones son consistentes
- Cambio de idioma afecta a Cosmic Coach

✅ **Bug #5 resuelto cuando:**
- Funcionalidad "realizar ritual" está documentada
- Textos están traducidos (si aplica)
- Comportamiento es consistente

---

## Contacto y Seguimiento

**Responsable:** Claude Code
**Reportado por:** Usuario
**Tracking:** Este documento + TODO list en Claude Code

**Actualizaciones:**
- Actualizar este documento al completar cada fase
- Marcar TODOs conforme se completen
- Documentar cualquier hallazgo nuevo
