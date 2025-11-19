# 🎯 TODO MASTER PLAN - 21 Octubre 2025

**Fecha creación:** 2025-10-21 02:50 AM
**Última actualización:** 2025-10-21 02:50 AM
**Branch actual:** `feature/mega-multiagent-execution`
**Estado:** 🔴 EN PROGRESO - 6 problemas críticos detectados

---

## 📋 CONTEXTO DEL PROYECTO

### Problema Principal:
Usuario tiene plan "Essential" ($6.99) que **NO existe en RevenueCat**. Esto causa:
- Analytics bloqueado
- Cosmic Coach parcialmente funcional
- Birth data no persiste
- Contenido en inglés en lugar de español

### Configuración Actual de RevenueCat:
- ✅ `cosmic` ($6.99) - tier1_subscription
- ✅ `stellar` ($19.99) - tier2_subscription
- ✅ `universe` ($49.99) - lifetime_tier1_purchase
- ❌ `essential` - **NO EXISTE** (tier deprecado en código pero activo en app del usuario)

### Repositorios:
- **Frontend:** `/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app`
- **Backend:** `/Users/alejandrocaceres/Desktop/appstore.zodia/backend`
- **Docs:** `/Users/alejandrocaceres/Desktop/appstore.zodia/`

---

## 🎯 TODOS - PRIORIDAD CRÍTICA

### 🔴 P0 - BLOQUEADORES (Hacer HOY)

#### ☐ TODO-001: Fix Birth Data Persistence
**Prioridad:** 🔴 CRÍTICO
**Estimación:** 2 horas
**Asignado a:** `@agent:flutter-expert` o `@agent:general-purpose`

**Problema:**
- Usuario guarda fecha de nacimiento
- Cierra la app
- Vuelve a abrir → La fecha no aparece
- Ascendant screen pide fecha otra vez

**Root Cause:**
- `BirthDataService` guarda en `SharedPreferences`
- `AscendantProfileScreen` lee de `SecureStorage`
- Sincronización (`_syncToPreferencesService`) puede fallar silenciosamente

**Archivos a modificar:**
1. `zodiac_app/lib/services/birth_data_service.dart`
2. `zodiac_app/lib/screens/ascendant_profile_screen.dart` (verificar fix actual)

**Solución propuesta:**
```dart
// Opción A: Unificar en SecureStorage (RECOMENDADO)
// - Eliminar guardado en SharedPreferences
// - Guardar SOLO vía PreferencesService → SecureStorage
// - Mantener cache en memoria para performance

// Opción B: Implementar fallback robusto
// - Intentar leer de SecureStorage primero
// - Si falla, leer de SharedPreferences
// - Migrar automáticamente de SharedPrefs → SecureStorage
```

**Testing:**
- [ ] Guardar fecha de nacimiento
- [ ] Cerrar app completamente (kill process)
- [ ] Reabrir app
- [ ] Verificar que fecha persiste
- [ ] Ir a Ascendant screen → NO debe pedir fecha otra vez
- [ ] Verificar que ascendant se calcula correctamente

**Multi-agent notes:**
- Puede ejecutarse en paralelo con TODO-003, TODO-004
- NO depende de RevenueCat
- Requiere rebuild + deploy para testing

---

#### ☐ TODO-002: Investigar "Essential" Entitlement Mystery
**Prioridad:** 🔴 CRÍTICO
**Estimación:** 1 hora
**Asignado a:** `@agent:devops-expert` o manual investigation

**Problema:**
- Usuario tiene plan "Essential" activo en la app
- "Essential" NO existe en RevenueCat Dashboard
- "Essential" es un tier DEPRECADO en el código

**Investigación necesaria:**
1. **RevenueCat Dashboard:**
   - [ ] Buscar usuario por email/ID
   - [ ] Ver qué entitlements tiene activos
   - [ ] Ver historial de compras
   - [ ] Verificar si "essential" aparece en algún lado

2. **App Store Connect:**
   - [ ] Verificar productos in-app configurados
   - [ ] Ver si existe producto llamado "essential"
   - [ ] Revisar historial de productos

3. **Usuario iOS:**
   - [ ] iPhone Settings → App Store → Subscriptions
   - [ ] Buscar suscripción de Zodiac
   - [ ] Capturar screenshot del plan activo

**Posibles escenarios:**
- A) Usuario tiene suscripción de prueba/testing
- B) Producto legacy de versión anterior de la app
- C) Error de configuración en RevenueCat
- D) Usuario NO tiene suscripción activa (FREE tier)

**Acción según resultado:**
- Si NO hay suscripción → Usuario debe comprar plan real
- Si hay "essential" → Mapear a "cosmic" en RevenueCat
- Si hay otro nombre → Actualizar código para reconocerlo

**Multi-agent notes:**
- Requiere acceso manual a RevenueCat Dashboard
- Bloqueante para TODO-006 (Analytics fix)

---

#### ☐ TODO-003: Fix Cosmic Coach Language (Backend)
**Prioridad:** 🔴 CRÍTICO
**Estimación:** 3 horas
**Asignado a:** `@agent:backend-expert` o `@agent:general-purpose`

**Problema:**
- App está en español
- Cosmic Coach muestra contenido en inglés
- Goal Planner genera metas con nombres raros ("Rally's Ritual", "Golems")

**Root Cause:**
- UI usa `AppLocalizations` correctamente (títulos en español) ✅
- Contenido AI se genera en inglés porque backend no sabe el idioma del usuario

**Archivos a investigar:**
1. `backend/` - Buscar servicios de AI/Goal generation
2. `zodiac_app/lib/services/cosmic_coach_goal_generator.dart`
3. `zodiac_app/lib/screens/cosmic_coach_screen.dart` (ya usa AppLocalizations)

**Solución propuesta:**

**Backend API:**
```python
# backend/services/ai_service.py (ejemplo)

def generate_goal(user_id, focus_area, language='en'):
    """Generate astrological goal in user's language"""

    # Get user language from profile or header
    user_language = request.headers.get('Accept-Language', 'en')

    prompt = f"""
    Generate a personalized astrological goal in {user_language}.

    Focus area: {focus_area}
    Language: {user_language}

    The goal should:
    - Be specific and actionable
    - Relate to astrological guidance
    - Use cosmic/spiritual terminology appropriate for {user_language}
    - Avoid generic business jargon

    Examples for Spanish:
    - "Conectar con tu energía lunar mediante meditación diaria"
    - "Fortalecer relaciones bajo la influencia de Venus"

    Generate goal in {user_language}:
    """

    return ai_model.generate(prompt)
```

**Frontend (pasar idioma al backend):**
```dart
// zodiac_app/lib/services/cosmic_coach_goal_generator.dart

Future<Goal> generateGoal(FocusArea focusArea) async {
  final locale = Localizations.localeOf(context);

  final response = await http.post(
    Uri.parse('$backendUrl/api/goals/generate'),
    headers: {
      'Accept-Language': locale.languageCode, // 'es', 'en', etc.
    },
    body: jsonEncode({
      'focus_area': focusArea.apiValue,
      'language': locale.languageCode,
    }),
  );

  return Goal.fromJson(jsonDecode(response.body));
}
```

**Testing:**
- [ ] Cambiar idioma de la app a español
- [ ] Generar nueva meta en Cosmic Coach
- [ ] Verificar que meta está en español
- [ ] Verificar que contenido tiene sentido astrológico
- [ ] Probar con inglés también

**Multi-agent notes:**
- Requiere cambios en backend Y frontend
- Puede ejecutarse en paralelo con TODO-001
- Requiere deploy de backend + app

---

### 🟡 P1 - IMPORTANTE (Esta semana)

#### ☐ TODO-004: Mejorar Goal Planner AI Prompts
**Prioridad:** 🟡 IMPORTANTE
**Estimación:** 2 horas
**Asignado a:** `@agent:backend-expert`

**Problema:**
- AI genera metas con nombres sin sentido ("Rally's Ritual", "Golems")
- Contenido no es astrológicamente relevante

**Root Cause:**
- Prompt al AI es muy genérico
- No incluye ejemplos de metas astrológicas
- No valida que el contenido sea apropiado

**Solución:**

**Mejorar prompt con contexto astrológico:**
```python
# backend/services/goal_ai_service.py

ASTROLOGICAL_GOAL_PROMPT = """
You are an expert astrologer creating personalized goals.

User zodiac sign: {zodiac_sign}
Current moon phase: {moon_phase}
Focus area: {focus_area}
Language: {language}

Create a goal that:
1. Relates to astrological energies and cosmic timing
2. Uses spiritual/cosmic terminology (NOT business jargon)
3. Is specific and actionable
4. Culturally appropriate for {language} speakers

BAD examples (avoid):
- "Rally's Ritual" (meaningless)
- "Golems" (not astrological)
- "Synergize team dynamics" (business jargon)

GOOD examples for Spanish:
- "Ritual de Luna Llena para Manifestación"
- "Conexión Diaria con tu Elemento {element}"
- "Meditación Planetaria bajo la influencia de {planet}"

GOOD examples for English:
- "Full Moon Manifestation Ritual"
- "Daily Connection with your {element} Element"
- "Planetary Meditation under {planet}'s influence"

Generate goal in {language}:
"""

def generate_astrological_goal(user_profile, focus_area, language):
    prompt = ASTROLOGICAL_GOAL_PROMPT.format(
        zodiac_sign=user_profile.zodiac_sign,
        moon_phase=get_current_moon_phase(),
        focus_area=focus_area,
        language=language,
        element=user_profile.element,
        planet=user_profile.ruling_planet,
    )

    goal = ai_model.generate(prompt)

    # Validate output
    if not validate_astrological_content(goal):
        # Regenerate or use fallback
        return get_fallback_goal(focus_area, language)

    return goal
```

**Agregar validación:**
```python
def validate_astrological_content(goal_text):
    """Validate that goal contains astrological terminology"""

    astrological_keywords = [
        'luna', 'moon', 'planeta', 'planet',
        'signo', 'sign', 'elemento', 'element',
        'energía', 'energy', 'cósmic', 'cosmic',
        'ritual', 'meditación', 'meditation',
    ]

    # Check if goal contains at least one astrological keyword
    has_astro_keyword = any(
        keyword.lower() in goal_text.lower()
        for keyword in astrological_keywords
    )

    # Check for business jargon (reject if found)
    business_jargon = ['synergy', 'leverage', 'kpi', 'roi']
    has_business_jargon = any(
        jargon.lower() in goal_text.lower()
        for jargon in business_jargon
    )

    return has_astro_keyword and not has_business_jargon
```

**Testing:**
- [ ] Generar 10 metas diferentes
- [ ] Verificar que TODAS tienen terminología astrológica
- [ ] Verificar que NINGUNA tiene business jargon
- [ ] Verificar que están en el idioma correcto
- [ ] User testing: ¿Las metas tienen sentido?

**Multi-agent notes:**
- Depende de TODO-003 (idioma)
- Puede ejecutarse en paralelo con TODO-001

---

#### ☐ TODO-005: Fix "Realiza Ritual" Copywriting
**Prioridad:** 🟢 MENOR
**Estimación:** 30 min
**Asignado a:** `@agent:general-purpose`

**Problema:**
- Texto "Realiza ritual" es confuso
- Usuario no entiende qué significa

**Solución:**
Cambiar copywriting en localization files.

**Archivos a modificar:**
1. `zodiac_app/assets/l10n/app_es.arb`
2. `zodiac_app/assets/l10n/app_en.arb`

**Cambios propuestos:**
```json
// app_es.arb
{
  "goalTypeRitual": "Ritual de Conexión Cósmica",
  "goalTypeRitualDescription": "Práctica espiritual diaria para conectar con tu energía cósmica",
  "goalTypeRitualShort": "Ritual Cósmico",
  "goalActionPerformRitual": "Completar ritual diario"
}

// app_en.arb
{
  "goalTypeRitual": "Cosmic Connection Ritual",
  "goalTypeRitualDescription": "Daily spiritual practice to connect with your cosmic energy",
  "goalTypeRitualShort": "Cosmic Ritual",
  "goalActionPerformRitual": "Complete daily ritual"
}
```

**Testing:**
- [ ] Run `flutter gen-l10n`
- [ ] Verificar que textos nuevos aparecen en Goal Planner
- [ ] Probar en español e inglés

**Multi-agent notes:**
- Independiente, puede hacerse en cualquier momento
- Requiere rebuild

---

#### ☐ TODO-006: Debug Analytics Premium Gate Issue
**Prioridad:** 🔴 CRÍTICO
**Estimación:** 2 horas
**Asignado a:** `@agent:flutter-expert`

**Problema:**
- Analytics muestra premium gate a pesar del fix de "essential"
- Usuario reporta que sigue bloqueado

**Dependencias:**
- ⚠️ Bloqueado por TODO-002 (necesitamos saber qué entitlement tiene el usuario)

**Investigación:**

**Paso 1: Verificar que el fix está instalado**
```bash
# Ver logs de la app corriendo
flutter logs -d 00008150-0015244A2288401C | grep -E "(essential|tier|premium|PREMIUM)"
```

**Esperado:**
```
✨ Essential entitlement recognized (alias of cosmic)
🔄 Subscription tier updated to: Essential
📢 Tier change broadcast to listeners
🔍 [PREMIUM] Has premium entitlement: true
```

**Si NO aparece:**
- Build instalada NO tiene el fix
- Necesita rebuild + redeploy

**Paso 2: Verificar el provider**
```dart
// zodiac_app/lib/screens/analytics_dashboard_screen.dart:72

final isPremiumAsync = ref.watch(isPremiumUserProvider);

return isPremiumAsync.when(
  data: (isPremium) {
    print('🔍 Analytics: isPremium = $isPremium');
    // Si isPremium = false → Muestra gate
    // Si isPremium = true → Muestra dashboard
  },
  loading: () {
    print('⏳ Analytics: Loading premium status...');
    // Stuck aquí = Provider nunca resuelve
  },
  error: (error, stack) {
    print('❌ Analytics: Error loading premium status: $error');
    // Error state → Muestra error screen (puede parecer un gate)
  },
);
```

**Paso 3: Verificar isPremiumUserProvider**
```dart
// zodiac_app/lib/providers/unified_premium_integration_provider.dart

// ¿Qué retorna userTierProvider?
final tierAsync = ref.watch(userTierProvider);
print('🔍 Current tier: ${tierAsync.valueOrNull}');

// ¿Qué retorna isPremiumUserProvider?
final isPremiumAsync = ref.watch(isPremiumUserProvider);
print('🔍 Is premium: ${isPremiumAsync.valueOrNull}');
```

**Posibles causas:**

**A) Usuario NO tiene entitlement activo en RevenueCat**
- RevenueCat retorna entitlements vacíos
- `currentTier = PremiumTier.free`
- `isPremium = false`
- **Solución:** Usuario debe comprar suscripción real

**B) Provider en estado error**
- RevenueCat initialization falló
- Provider lanza exception
- Analytics muestra error screen (parece premium gate)
- **Solución:** Fix RevenueCat initialization

**C) Provider stuck en loading**
- RevenueCat nunca retorna
- Provider queda en loading infinito
- Analytics muestra loading infinito (parece gate)
- **Solución:** Add timeout to provider

**D) Build NO tiene el fix**
- Código viejo instalado
- "essential" NO reconocido
- **Solución:** Rebuild + redeploy

**Fix según diagnóstico:**

**Si es (A) - No hay entitlement:**
```dart
// No hay fix de código, usuario debe comprar
// Mostrar mensaje claro: "No tienes suscripción activa"
```

**Si es (B) - Error state:**
```dart
// zodiac_app/lib/providers/unified_premium_integration_provider.dart

final userTierProvider = StreamProvider<PremiumTier>((ref) async* {
  try {
    final revenueCatService = rc.RevenueCatService.instance;

    // Add timeout
    final initialized = await revenueCatService
        .initialize()
        .timeout(Duration(seconds: 10));

    if (!initialized) {
      throw Exception('RevenueCat initialization timeout');
    }

    final subscriptionService = ref.watch(subscriptionServiceProvider);
    yield subscriptionService.currentTier;
  } catch (e) {
    AppLogger.error('Error in userTierProvider', e);
    // Yield FREE instead of throwing (graceful degradation)
    yield PremiumTier.free;
  }
});
```

**Si es (C) - Loading infinito:**
```dart
// Add timeout to provider
final isPremiumUserProvider = StreamProvider<bool>((ref) async* {
  try {
    await for (final tierAsync in ref.watch(userTierProvider.stream)) {
      yield tierAsync != PremiumTier.free;
    }
  } on TimeoutException {
    // Default to false after timeout
    yield false;
  }
}).timeout(Duration(seconds: 15));
```

**Si es (D) - Build viejo:**
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
flutter clean
/Users/alejandrocaceres/flutter/bin/flutter build ios --release
/Users/alejandrocaceres/flutter/bin/flutter run -d 00008150-0015244A2288401C --release
```

**Testing:**
- [ ] Verificar logs muestran "essential" reconocido
- [ ] Abrir Analytics
- [ ] Verificar que NO muestra premium gate
- [ ] Verificar que muestra dashboard con gráficos

**Multi-agent notes:**
- Bloqueado por TODO-002
- Requiere logs/debugging manual

---

### 🟢 P2 - NICE TO HAVE (Próxima semana)

#### ☐ TODO-007: Add Dynamic Pricing from RevenueCat
**Prioridad:** 🟢 MENOR
**Estimación:** 1 hora
**Asignado a:** `@agent:flutter-expert`

**Problema:**
- Precios hardcoded en código ($6.99, $19.99, $49.99)
- Si cambias precios en RevenueCat/App Store, no se reflejan en la app

**Solución:**
Obtener precios dinámicamente de RevenueCat SDK.

**Archivos a modificar:**
1. `zodiac_app/lib/screens/premium_screen.dart`
2. `zodiac_app/lib/models/subscription_tier.dart`

**Implementación:**
```dart
// zodiac_app/lib/screens/premium_screen.dart

class PremiumScreen extends ConsumerStatefulWidget {
  // ...
}

class _PremiumScreenState extends ConsumerState<PremiumScreen> {
  Map<String, Package>? _packages;
  bool _loadingPrices = true;

  @override
  void initState() {
    super.initState();
    _loadPrices();
  }

  Future<void> _loadPrices() async {
    try {
      final offerings = await Purchases.getOfferings();

      if (offerings.current != null) {
        final packages = offerings.current!.availablePackages;

        setState(() {
          _packages = {
            for (var package in packages)
              package.identifier: package
          };
          _loadingPrices = false;
        });
      }
    } catch (e) {
      AppLogger.error('Error loading prices', e);
      setState(() => _loadingPrices = false);
    }
  }

  String _getPrice(String packageId) {
    if (_loadingPrices) return '...';

    final package = _packages?[packageId];
    if (package == null) {
      // Fallback to hardcoded price
      switch (packageId) {
        case 'tier1_monthly': return '\$6.99';
        case 'tier2_monthly': return '\$19.99';
        case 'lifetime_tier1': return '\$49.99';
        default: return '???';
      }
    }

    return package.storeProduct.priceString;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column([
        // Cosmic tier
        PremiumTierCard(
          tier: PremiumTier.cosmic,
          price: _getPrice('tier1_monthly'), // Dynamic price
          onTap: () => _purchase('tier1_monthly'),
        ),

        // Stellar tier
        PremiumTierCard(
          tier: PremiumTier.stellar,
          price: _getPrice('tier2_monthly'), // Dynamic price
          onTap: () => _purchase('tier2_monthly'),
        ),

        // Universe tier
        PremiumTierCard(
          tier: PremiumTier.universe,
          price: _getPrice('lifetime_tier1'), // Dynamic price
          badge: 'BEST VALUE',
          onTap: () => _purchase('lifetime_tier1'),
        ),
      ]),
    );
  }
}
```

**Testing:**
- [ ] Abrir Premium screen
- [ ] Verificar que precios coinciden con RevenueCat/App Store
- [ ] Cambiar precio en RevenueCat
- [ ] Reinstalar app
- [ ] Verificar que precio nuevo aparece

**Multi-agent notes:**
- Independiente
- Low priority

---

## 🤖 MULTI-AGENT EXECUTION STRATEGY

### Agentes Disponibles:

```json
{
  "agents": [
    {
      "id": "flutter-expert",
      "type": "general-purpose",
      "specialization": "Flutter/Dart development",
      "can_handle": ["TODO-001", "TODO-005", "TODO-006", "TODO-007"]
    },
    {
      "id": "backend-expert",
      "type": "general-purpose",
      "specialization": "Python/Node.js backend, AI prompts",
      "can_handle": ["TODO-003", "TODO-004"]
    },
    {
      "id": "devops-expert",
      "type": "general-purpose",
      "specialization": "RevenueCat, App Store, deployment",
      "can_handle": ["TODO-002"]
    }
  ]
}
```

### Ejecución Paralela:

**Fase 1 (Paralelo):**
```
Agent 1: TODO-001 (Birth Data Fix)
Agent 2: TODO-003 (Cosmic Coach Language - Backend)
Agent 3: TODO-002 (Investigar Essential) - Manual
```

**Fase 2 (Después de Fase 1):**
```
Agent 1: TODO-004 (Goal Planner Prompts) - Depende de TODO-003
Agent 2: TODO-006 (Analytics Debug) - Depende de TODO-002
Agent 3: TODO-005 (Copywriting) - Independiente
```

**Fase 3 (Opcional):**
```
Agent 1: TODO-007 (Dynamic Pricing)
```

### Comandos para Multi-Agent:

```bash
# Lanzar múltiples agentes en paralelo
claude-code task --parallel \
  "TODO-001: Fix Birth Data Persistence" \
  "TODO-003: Fix Cosmic Coach Language Backend" \
  "TODO-005: Fix Realiza Ritual Copywriting"

# Lanzar secuencialmente (con dependencias)
claude-code task --sequential \
  "TODO-002: Investigate Essential Entitlement" \
  "TODO-006: Debug Analytics Premium Gate"
```

---

## 📊 PROGRESS TRACKING

### Overall Progress:
```
┌─────────────────────────────────────┐
│ ████░░░░░░░░░░░░░░░░░░░░░░░░░ 14%  │
│ 1 de 7 TODOs completados            │
└─────────────────────────────────────┘
```

### By Priority:
```
🔴 P0 (Crítico):    0 / 4 completados  (  0%)
🟡 P1 (Importante): 0 / 2 completados  (  0%)
🟢 P2 (Menor):      0 / 1 completados  (  0%)
```

### Timeline:
```
Hoy (21 Oct):
  - [ ] TODO-001 (2h)
  - [ ] TODO-002 (1h) - Manual
  - [ ] TODO-006 (2h) - Depende de TODO-002

Esta semana:
  - [ ] TODO-003 (3h)
  - [ ] TODO-004 (2h)
  - [ ] TODO-005 (30min)

Próxima semana:
  - [ ] TODO-007 (1h)
```

---

## 🔗 DOCUMENTACIÓN RELACIONADA

- `CRITICAL_FIXES_OCT21.md` - Problema inicial reportado
- `CRITICAL_FIXES_ANALYSIS_OCT21.md` - Análisis completo con root causes
- `TIER_SYSTEM_FIX_OCT21.md` - Multi-tier system implementation
- `ESSENTIAL_FIX_FINAL_OCT21.md` - Fix del entitlement "essential"

---

## 📝 NOTAS DE IMPLEMENTACIÓN

### Commits recomendados:

```bash
# TODO-001
git commit -m "fix(birth-data): unify storage to prevent data loss

- Remove dual storage system (SharedPrefs + SecureStorage)
- Save birth data only via PreferencesService (SecureStorage)
- Add fallback to migrate existing SharedPrefs data
- Add robust error handling with logging

Closes #TODO-001"

# TODO-003
git commit -m "feat(i18n): add language support to AI content generation

Backend:
- Accept Accept-Language header in goal generation API
- Pass user language to AI prompts
- Add language-specific examples to prompts

Frontend:
- Send locale.languageCode in API requests
- Update CosmicCoachGoalGenerator to pass language

Closes #TODO-003"

# TODO-004
git commit -m "improve(ai): enhance goal prompts with astrological context

- Add astrological keywords to prompts
- Add validation for astrological content
- Add fallback goals for validation failures
- Remove business jargon from generated content

Closes #TODO-004"
```

---

## 🚨 AVISOS IMPORTANTES

### ⚠️ Breaking Changes:
- TODO-001: Puede perder datos existentes en SharedPreferences si no se migran correctamente
- TODO-003: Requiere deploy de backend + app sincronizados

### ⚠️ Dependencias Externas:
- TODO-002: Requiere acceso a RevenueCat Dashboard (manual)
- TODO-003: Requiere acceso al backend + permisos para deploy

### ⚠️ Testing en Producción:
- Todos los TODOs requieren testing en device real (iPhone 00008150-0015244A2288401C)
- TODO-006: Requiere usuario con suscripción real para testing completo

---

**✅ READY TO EXECUTE**

Este plan está listo para ejecución multi-agente. Cada TODO tiene:
- ✅ Descripción clara del problema
- ✅ Root cause analysis
- ✅ Solución propuesta con código
- ✅ Testing checklist
- ✅ Estimación de tiempo
- ✅ Dependencias mapeadas
- ✅ Multi-agent assignment

Para empezar, ejecuta:
```bash
# Opción 1: Un TODO a la vez
claude-code task "TODO-001: Fix Birth Data Persistence"

# Opción 2: Múltiples TODOs en paralelo
claude-code task --parallel "TODO-001" "TODO-003" "TODO-005"
```

---

**Última actualización:** 2025-10-21 02:50 AM
**Next review:** 2025-10-21 PM (después de completar TODO-001, TODO-002)
