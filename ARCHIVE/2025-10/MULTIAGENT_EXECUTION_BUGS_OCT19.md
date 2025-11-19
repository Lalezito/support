# Ejecución Multiagente - Arreglo de Bugs
**Fecha:** 19 de Octubre 2025
**Modo:** MULTIAGENTE PARALELO
**Objetivo:** Arreglar todos los bugs críticos de premium y UX

---

## 🎯 Estrategia de Ejecución

Vamos a lanzar **5 agentes en paralelo** para maximizar velocidad:
- **Agentes 1-3:** Bugs críticos de premium (prioridad máxima)
- **Agente 4:** Bug de UX/traducciones
- **Agente 5:** Investigación de funcionalidad

---

## 👥 AGENT 1: Premium State Refresh Fix

**Responsabilidad:** Bug #2 - Premium se vuelve a bloquear al salir de settings

**Contexto:**
- Después de comprar premium, al salir de PremiumScreen las features vuelven a aparecer bloqueadas
- Usuario tiene que volver a Home y luego a Settings para que se actualice
- **Causa raíz:** Providers no se invalidan después de la compra

**Archivos a modificar:**
```
lib/screens/premium_screen.dart
lib/providers/unified_premium_integration_provider.dart
```

**Tareas específicas:**

1. **Localizar método de compra en premium_screen.dart**
   - Buscar método `purchasePackage()` o similar
   - Identificar callback de éxito

2. **Agregar invalidación de providers**
   ```dart
   // Después de compra exitosa
   if (mounted) {
     // Invalidar provider de premium
     ref.invalidate(unifiedPremiumIntegrationProvider);

     // Invalidar provider de RevenueCat
     ref.invalidate(revenueCatProvider);

     // Esperar actualización
     await Future.delayed(Duration(milliseconds: 300));

     // Mostrar confirmación
     if (context.mounted) {
       ScaffoldMessenger.of(context).showSnackBar(
         SnackBar(content: Text('Premium activated! ✨'))
       );
     }
   }
   ```

3. **Verificar que Settings escucha cambios**
   - En `settings_screen.dart`, verificar que usa `ref.watch()` no `ref.read()`

4. **Testing:**
   - Comprar premium
   - Verificar que Settings se actualiza SIN volver a Home
   - Verificar que íconos premium aparecen inmediatamente

**Criterio de éxito:**
✅ Compra premium → Settings se actualiza inmediatamente sin volver a Home

---

## 👥 AGENT 2: Feature Gates Refresh Fix

**Responsabilidad:** Bug #3 - Funciones de análisis siguen bloqueadas después de comprar

**Contexto:**
- Después de comprar premium, algunas features (análisis, compatibilidad) siguen bloqueadas
- `PremiumFeatureGate` cachea el estado viejo
- Relacionado con Bug #2

**Archivos a modificar:**
```
lib/services/feature_gate_service.dart
lib/widgets/monetization/premium_feature_gate.dart
lib/screens/compatibility_screen.dart
lib/screens/analytics_dashboard_screen.dart
```

**Tareas específicas:**

1. **Agregar método de invalidación de cache en FeatureGateService**
   ```dart
   class FeatureGateService {
     DateTime? _cacheTimestamp;
     bool? _cachedIsPremium;

     // AGREGAR ESTE MÉTODO
     void invalidateCache() {
       _cacheTimestamp = null;
       _cachedIsPremium = null;
       AppLogger.info('FeatureGateService cache invalidated');
     }

     // Modificar checkAccess para respetar invalidación
     Future<bool> checkAccess(String featureId) async {
       // Si no hay cache o es muy viejo, refrescar
       if (_cacheTimestamp == null ||
           DateTime.now().difference(_cacheTimestamp!) > Duration(seconds: 5)) {
         _cachedIsPremium = await _checkPremiumStatus();
         _cacheTimestamp = DateTime.now();
       }
       return _cachedIsPremium ?? false;
     }
   }
   ```

2. **Crear provider para FeatureGateService**
   ```dart
   // En lib/providers/consolidated_providers.dart
   final featureGateServiceProvider = Provider<FeatureGateService>((ref) {
     return FeatureGateService();
   });
   ```

3. **Modificar PremiumFeatureGate para usar ref.watch**
   ```dart
   class PremiumFeatureGate extends ConsumerWidget {
     @override
     Widget build(BuildContext context, WidgetRef ref) {
       // USAR WATCH para que se reconstruya automáticamente
       final isPremium = ref.watch(unifiedPremiumIntegrationProvider)
         .select((state) => state.isPremium);

       if (isPremium) {
         return unlockedChild;
       } else {
         return lockedChild ?? _buildDefaultLocked();
       }
     }
   }
   ```

4. **Conectar invalidación con premium_screen**
   - Cuando se compra premium, invalidar FeatureGateService
   ```dart
   // En premium_screen después de compra
   final featureGateService = ref.read(featureGateServiceProvider);
   featureGateService.invalidateCache();
   ```

5. **Testing:**
   - Comprar premium
   - Acceder inmediatamente a Análisis → debe estar desbloqueado
   - Acceder a Compatibilidad avanzada → debe estar desbloqueado
   - Verificar todas las features premium

**Criterio de éxito:**
✅ Todas las features premium se desbloquean inmediatamente después de comprar

---

## 👥 AGENT 3: Birth Data Synchronization Fix

**Responsabilidad:** Bug #1 - Fecha de nacimiento no se guarda en AscendantScreen

**Contexto:**
- Usuario ingresa fecha de nacimiento en BirthDataCollectionScreen
- Se guarda en `BirthDataService`
- Pero `AscendantProfileScreen` lee de `PreferencesService`
- Los servicios no están sincronizados

**Archivos a modificar:**
```
lib/services/birth_data_service.dart
lib/services/preferences_service.dart
lib/screens/birth_data_collection_screen.dart
lib/screens/ascendant_profile_screen.dart
```

**Tareas específicas:**

1. **OPCIÓN ELEGIDA: Sincronizar ambos servicios**

   En `birth_data_service.dart`, método `saveBirthData()`:
   ```dart
   Future<bool> saveBirthData(BirthData birthData) async {
     try {
       // Validar
       final validation = BirthDataValidator.validate(birthData);
       if (!validation.isValid) {
         logError('Birth data validation failed');
         return false;
       }

       // 1. Guardar en BirthDataService (existente)
       final birthDataJson = birthData.toJson();
       await _prefs?.setString(_storageKey, jsonEncode(birthDataJson));
       _cachedBirthData = birthData;

       // 2. AGREGAR: Sincronizar con PreferencesService
       final prefsService = PreferencesService.instance;
       await prefsService.setBirthDate(birthData.birthDate);

       if (birthData.birthTime != null) {
         final timeString = '${birthData.birthTime!.hour.toString().padLeft(2, '0')}:${birthData.birthTime!.minute.toString().padLeft(2, '0')}';
         await prefsService.setBirthTime(timeString);
       }

       if (birthData.birthLocation != null) {
         await prefsService.setBirthLocation(
           birthData.birthLocation!.latitude,
           birthData.birthLocation!.longitude,
           birthData.birthLocation!.name ?? 'Unknown',
         );
       }

       AppLogger.info('✅ Birth data saved and synchronized');
       return true;
     } catch (e) {
       logError('Failed to save birth data: $e');
       return false;
     }
   }
   ```

2. **Verificar que AscendantProfileScreen usa PreferencesService correctamente**
   - El código actual ya lee de `PreferencesService.instance.birthDate` (línea 76)
   - Esto está bien, solo necesitamos que BirthDataService sincronice

3. **Agregar logging para debugging**
   ```dart
   // En BirthDataCollectionScreen después de guardar
   AppLogger.info('Birth data saved:');
   AppLogger.info('  Date: ${birthData.birthDate}');
   AppLogger.info('  Time: ${birthData.birthTime?.hour}:${birthData.birthTime?.minute}');
   AppLogger.info('  Location: ${birthData.birthLocation?.name}');
   ```

4. **Testing:**
   - Ingresar nueva fecha de nacimiento
   - Verificar logs que se guarda en ambos servicios
   - Abrir AscendantScreen
   - Verificar que muestra la fecha correcta
   - Verificar que calcula ascendant correctamente

**Criterio de éxito:**
✅ Fecha de nacimiento se guarda y AscendantScreen la muestra correctamente

---

## 👥 AGENT 4: Cosmic Coach Translations Fix

**Responsabilidad:** Bug #4 - Cosmic Coach aparece en inglés cuando app está en español

**Contexto:**
- App está configurada en español
- Cosmic Coach responde en inglés
- Servicio de AI no usa `AppLocalizations` ni sistema de traducciones

**Archivos a modificar:**
```
lib/services/cosmic_chat_service.dart
lib/services/consolidated_ai/coaching_ai_service.dart
lib/screens/cosmic_coach_screen.dart
lib/screens/cosmic_coach_chat_screen.dart
```

**Tareas específicas:**

1. **Detectar idioma del usuario en CoachingAIService**
   ```dart
   // En coaching_ai_service.dart

   Future<String> generateCoachingResponse(
     String userMessage,
     CoachingContext context,
     BuildContext uiContext, // Agregar este parámetro
   ) async {
     // Detectar idioma
     final locale = Localizations.localeOf(uiContext);
     final languageCode = locale.languageCode; // 'es', 'en', 'pt', etc.

     // Obtener nombre del idioma para el prompt
     final languageName = _getLanguageNameForAI(languageCode);

     // Modificar system prompt para incluir idioma
     final systemPrompt = '''
     You are a cosmic life coach and spiritual guide.

     IMPORTANT: You MUST respond in $languageName language.
     The user's interface language is: $languageCode
     All your responses must be in $languageName.

     Your role is to provide:
     - Astrological insights
     - Life guidance based on cosmic energies
     - Empathetic and supportive coaching

     Always respond in a warm, mystical, and empowering tone.
     Remember: ALWAYS use $languageName language in your response.
     ''';

     // Resto del código de generación...
   }

   String _getLanguageNameForAI(String code) {
     switch (code) {
       case 'es': return 'Spanish (Español)';
       case 'en': return 'English';
       case 'pt': return 'Portuguese (Português)';
       case 'fr': return 'French (Français)';
       case 'de': return 'German (Deutsch)';
       case 'it': return 'Italian (Italiano)';
       default: return 'English';
     }
   }
   ```

2. **Actualizar llamadas al servicio para pasar BuildContext**
   ```dart
   // En cosmic_coach_screen.dart o cosmic_coach_chat_screen.dart

   Future<void> _sendMessage(String message) async {
     final response = await coachingAIService.generateCoachingResponse(
       message,
       coachingContext,
       context, // Pasar el BuildContext
     );

     setState(() {
       messages.add(response);
     });
   }
   ```

3. **Agregar traducciones estáticas de UI**
   - Verificar que botones, placeholders, etc. usen `AppLocalizations`
   ```dart
   // Ejemplo en cosmic_coach_screen.dart
   TextField(
     decoration: InputDecoration(
       hintText: AppLocalizations.of(context).cosmicCoachInputHint,
       // En vez de hintText: 'Ask your cosmic coach...'
     ),
   )
   ```

4. **Testing:**
   - Configurar app en español
   - Abrir Cosmic Coach
   - Enviar mensaje → Verificar respuesta en español
   - Cambiar idioma a inglés
   - Enviar mensaje → Verificar respuesta en inglés
   - Probar con portugués, francés

**Criterio de éxito:**
✅ Cosmic Coach responde en el idioma configurado de la app

---

## 👥 AGENT 5: Ritual Functionality Investigation

**Responsabilidad:** Bug #5 - Investigar y documentar "realizar ritual"

**Contexto:**
- En Goals aparece opción "Realizar ritual"
- No está claro qué hace
- Sale en inglés
- Necesita documentación y posiblemente traducción

**Archivos a investigar:**
```
lib/screens/goal_planner/goal_planner_home_screen.dart
lib/models/cosmic_goal_unified.dart
lib/services/cosmic_coach_goal_generator.dart
lib/widgets/goals/ (si existen widgets específicos)
```

**Tareas específicas:**

1. **Investigar código de "realizar ritual"**
   - Buscar método `performRitual()` o similar
   - Documentar qué hace exactamente
   - Identificar si es animación, modal, o acción de backend

2. **Documentar funcionalidad**
   - Crear documento explicando:
     * ¿Qué es "realizar ritual"?
     * ¿Cuándo se puede usar?
     * ¿Es premium o free?
     * ¿Qué efecto tiene en el goal?
     * ¿Hay alguna animación o feedback visual?

3. **Identificar strings sin traducir**
   - Buscar textos hardcodeados en inglés
   - Listar qué keys faltan en `app_localizations_es.dart`

4. **Crear plan de fix si es necesario**
   - Si solo necesita traducción → agregar keys
   - Si tiene bugs → documentar para fix posterior

5. **Agregar traducciones**
   ```dart
   // En app_localizations_en.dart
   String get performRitual => 'Perform Ritual';
   String get ritualDescription => 'Complete this goal with a cosmic ritual';

   // En app_localizations_es.dart
   String get performRitual => 'Realizar Ritual';
   String get ritualDescription => 'Completa esta meta con un ritual cósmico';
   ```

**Criterio de éxito:**
✅ Funcionalidad documentada + traducciones agregadas

---

## 🔗 INTEGRATION PHASE

**Después de que todos los agentes terminen:**

1. **Verificar que fixes no se pisan entre sí**
   - Revisar cambios en `premium_screen.dart` (Agentes 1 y 2)
   - Asegurar que invalidaciones se ejecutan en orden correcto

2. **Testing de integración:**
   - Flujo completo: Onboarding → Birth data → Premium purchase → Use features
   - Verificar que todo funciona junto

3. **Resolver conflictos si existen**

---

## 🧪 REGRESSION TESTING PHASE

**Tests críticos a ejecutar:**

1. **Flujo de compra premium completo**
   ```
   [ ] Abrir app
   [ ] Ir a premium screen
   [ ] Comprar premium
   [ ] Verificar UI se actualiza inmediatamente
   [ ] NO volver a home
   [ ] Ir a Settings → verificar premium activo
   [ ] Ir a Análisis → verificar desbloqueado
   [ ] Ir a Cosmic Coach → verificar premium
   ```

2. **Flujo de birth data**
   ```
   [ ] Ingresar fecha de nacimiento
   [ ] Ingresar hora de nacimiento
   [ ] Ingresar ubicación
   [ ] Guardar
   [ ] Abrir Ascendant screen
   [ ] Verificar fecha correcta
   [ ] Verificar ascendant calculado
   ```

3. **Flujo de traducciones**
   ```
   [ ] App en español
   [ ] Cosmic Coach responde en español
   [ ] Cambiar a inglés
   [ ] Cosmic Coach responde en inglés
   [ ] UI de ritual en idioma correcto
   ```

---

## 📊 Tracking de Progreso

### Agent 1: Premium State Refresh
- [ ] Localizar método de compra
- [ ] Agregar ref.invalidate()
- [ ] Agregar delay
- [ ] Testing básico
- [ ] ✅ COMPLETADO

### Agent 2: Feature Gates Refresh
- [ ] Agregar invalidateCache()
- [ ] Modificar PremiumFeatureGate
- [ ] Conectar con premium_screen
- [ ] Testing básico
- [ ] ✅ COMPLETADO

### Agent 3: Birth Data Sync
- [ ] Modificar saveBirthData()
- [ ] Agregar sincronización
- [ ] Agregar logging
- [ ] Testing básico
- [ ] ✅ COMPLETADO

### Agent 4: Cosmic Coach i18n
- [ ] Detectar idioma
- [ ] Modificar prompts AI
- [ ] Actualizar UI strings
- [ ] Testing básico
- [ ] ✅ COMPLETADO

### Agent 5: Ritual Investigation
- [ ] Investigar código
- [ ] Documentar funcionalidad
- [ ] Agregar traducciones
- [ ] ✅ COMPLETADO

### Integration
- [ ] Merge de cambios
- [ ] Resolver conflictos
- [ ] Testing integración
- [ ] ✅ COMPLETADO

### Regression
- [ ] Premium flow
- [ ] Birth data flow
- [ ] Translations flow
- [ ] ✅ COMPLETADO

---

## 🎯 Criterios de Éxito General

✅ **Bug #1:** Fecha nacimiento se guarda y muestra correctamente
✅ **Bug #2:** Premium se actualiza inmediatamente sin volver a Home
✅ **Bug #3:** Todas las features se desbloquean inmediatamente
✅ **Bug #4:** Cosmic Coach responde en idioma correcto
✅ **Bug #5:** Ritual documentado y traducido

---

## 🚀 Siguiente Paso

**LANZAR AGENTES EN PARALELO:**
- Agent 1, 2, 3: Ejecutar simultáneamente (bugs críticos)
- Agent 4, 5: Ejecutar simultáneamente (UX)
- Luego Integration + Regression

**Comando para ejecutar:**
```
¡EMPEZAR EJECUCIÓN MULTIAGENTE AHORA!
```
