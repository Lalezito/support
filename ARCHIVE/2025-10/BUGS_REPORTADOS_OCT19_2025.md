# Bugs Reportados - 19 de Octubre 2025

**Reportados por:** Usuario
**Fecha:** 19 de Octubre 2025
**Prioridad:** ALTA - Afectan funcionalidad principal premium

---

## 1. ❌ Fecha de nacimiento no se guarda en AscendantScreen

**Síntoma:**
- Después de ingresar la fecha de nacimiento, cuando se toca la pantalla de AscendantScreen no cambia nada
- La fecha no parece quedar guardada

**Archivos involucrados:**
- `lib/screens/ascendant_profile_screen.dart` (líneas 66-127)
- `lib/screens/birth_data_collection_screen.dart` (líneas 368-443)
- `lib/services/birth_data_service.dart`

**Análisis preliminar:**
- `AscendantProfileScreen` carga datos de `PreferencesService.instance.birthDate` (línea 76)
- `BirthDataCollectionScreen` guarda en `BirthDataService` (línea 397)
- **POSIBLE CAUSA**: Los datos se guardan en `BirthDataService` pero `AscendantProfileScreen` lee de `PreferencesService`
- Hay desconexión entre servicios de almacenamiento

**Estado:** 🔴 EN INVESTIGACIÓN

---

## 2. ❌ Premium se vuelve a bloquear al salir de Settings

**Síntoma:**
- Después de comprar premium, al salir de la pantalla de premium vuelven a aparecer las funciones como bloqueadas
- Hay que volver hasta Home y luego regresar a Settings para que las cosas estén desbloqueadas

**Archivos involucrados:**
- `lib/screens/settings_screen.dart`
- `lib/screens/premium_screen.dart`
- `lib/services/revenuecat_service.dart`
- `lib/providers/unified_premium_integration_provider.dart`

**Análisis preliminar:**
- **POSIBLE CAUSA**: Estado de premium no se actualiza correctamente en el provider
- El widget no se está reconstruyendo cuando cambia el estado premium
- Falta un `ref.invalidate()` o `ref.refresh()` después de la compra

**Estado:** 🔴 EN INVESTIGACIÓN

---

## 3. ❌ Funciones de análisis siguen bloqueadas después de comprar

**Síntoma:**
- Con todo ya desbloqueado después de comprar premium
- Al intentar usar las funciones de análisis, siguen apareciendo como que hay que desbloquearlas

**Archivos involucrados:**
- `lib/screens/compatibility_screen.dart`
- `lib/screens/analytics_dashboard_screen.dart`
- `lib/widgets/monetization/premium_feature_gate.dart`
- `lib/services/feature_gate_service.dart`

**Análisis preliminar:**
- **POSIBLE CAUSA**: `PremiumFeatureGate` no se está actualizando con el nuevo estado
- El servicio de feature gates está cacheando el estado anterior
- Probablemente relacionado con el Bug #2

**Estado:** 🔴 EN INVESTIGACIÓN

---

## 4. ⚠️ Cosmic Coach aparece en inglés cuando app está en español

**Síntoma:**
- La aplicación está configurada en español
- Cosmic Coach muestra todo el contenido en inglés

**Archivos involucrados:**
- `lib/screens/cosmic_coach_screen.dart`
- `lib/screens/cosmic_coach_chat_screen.dart`
- `lib/services/cosmic_chat_service.dart`
- `lib/services/consolidated_ai/coaching_ai_service.dart`
- `lib/l10n/app_localizations_es.dart` (traducciones)

**Análisis preliminar:**
- **POSIBLE CAUSA**: El servicio de Cosmic Coach no está usando `AppLocalizations`
- Las respuestas de AI se generan en inglés sin pasar por el sistema de traducciones
- Falta integración con `SimpleTranslationsHelper`

**Estado:** 🟡 EN INVESTIGACIÓN

---

## 5. ❓ "Realizar ritual" en Goals - Funcionalidad desconocida

**Síntoma:**
- En la sección de Goals aparece una opción "Realizar ritual"
- Sale un "coso" (probablemente modal o animación)
- Sale en inglés
- No está claro qué hace esta funcionalidad

**Archivos involucrados:**
- `lib/screens/goal_planner/goal_planner_home_screen.dart`
- `lib/models/cosmic_goal_unified.dart`
- `lib/services/cosmic_coach_goal_generator.dart`

**Preguntas pendientes:**
- ¿Qué se supone que hace "realizar ritual"?
- ¿Es una animación ceremonial?
- ¿Marca un goal como completado de forma especial?
- ¿Es contenido premium o free?

**Estado:** 🟡 REQUIERE CLARIFICACIÓN

---

## Prioridad de Resolución

### 🔴 CRÍTICO (Afecta funcionalidad premium principal)
1. Bug #2: Premium se vuelve a bloquear
2. Bug #3: Funciones de análisis bloqueadas
3. Bug #1: Fecha de nacimiento no se guarda

### 🟡 IMPORTANTE (Afecta UX y calidad)
4. Bug #4: Cosmic Coach en inglés
5. Bug #5: Clarificar funcionalidad "realizar ritual"

---

## Patrón Común Identificado

**Los bugs #1, #2 y #3 parecen estar relacionados con:**
- Problemas de sincronización de estado entre servicios
- Falta de actualización de providers después de cambios
- Uso de múltiples fuentes de verdad (`PreferencesService` vs `BirthDataService` vs `RevenueCatService`)

**Solución probable:**
- Consolidar en un solo source of truth
- Usar Riverpod correctamente con `ref.invalidate()` o `ref.refresh()`
- Asegurar que los widgets se reconstruyan cuando cambia el estado

---

## Próximos Pasos

1. ✅ Documentar bugs
2. ⏳ Reproducir cada bug en entorno de desarrollo
3. ⏳ Identificar causa raíz de cada uno
4. ⏳ Implementar fixes
5. ⏳ Testing de regresión
6. ⏳ Deploy

---

**Notas adicionales:**
- Todos estos bugs fueron reportados después de la gran ejecución multiagente de Oct 13-14
- Sugiere que los cambios recientes pueden haber introducido regresiones
- Revisar commits recientes relacionados con premium y birth data
