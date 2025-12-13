# 🌍 PLAN MAESTRO: Mejoras Premium con i18n-First Approach

**Fecha de creación**: Octubre 31, 2025
**Estrategia**: i18n-First Development (Internacionalización desde el inicio)
**Idiomas soportados**: 6 (EN, ES, DE, FR, IT, PT)
**Objetivo**: Implementar todas las mejoras premium con soporte multilenguaje completo desde día 1

---

## 📖 ¿QUÉ ES i18n-FIRST APPROACH?

**Internacionalización (i18n)** significa desarrollar software pensando en múltiples idiomas desde el inicio, no como un "agregado posterior".

### Principios i18n-First:
1. ✅ **Cero textos hardcodeados** → Todo a través de AppLocalizations
2. ✅ **6 idiomas simultáneos** → EN, ES, DE, FR, IT, PT desde commit 1
3. ✅ **Contexto cultural** → Considerar formatos de fecha, moneda, expresiones
4. ✅ **Testing multilenguaje** → QA en todos los idiomas antes de release
5. ✅ **Validación automática** → Scripts que detectan textos sin traducir

### Estructura actual de tu app:
```
assets/l10n/
├── app_en.arb (112 KB) ✅ Inglés - Base
├── app_es.arb (102 KB) ✅ Español
├── app_de.arb (97 KB)  ✅ Alemán
├── app_fr.arb (95 KB)  ✅ Francés
├── app_it.arb (113 KB) ✅ Italiano
└── app_pt.arb (113 KB) ✅ Portugués

614 usos de AppLocalizations en 40 archivos ✅
```

---

## 🎯 RESUMEN EJECUTIVO

### Scope del Plan:
- **9 mejoras premium** principales
- **54 nuevas claves i18n** (9 features × 6 idiomas = 54 traducciones)
- **8 pantallas modificadas**
- **4 sprints de implementación**
- **Tiempo estimado**: 6-8 semanas

### ROI Estimado:
- **+30% conversión internacional** (traducciones completas)
- **+200% upgrade Cosmic→Stellar** (features exclusivas claras)
- **+$35K/año en revenue** (basado en 10K usuarios activos)

---

## 📋 WORKFLOW i18n-FIRST

### Proceso para CADA feature:

```
┌─────────────────────────────────────────────────────────┐
│ FASE 1: DISEÑO & PLANIFICACIÓN                         │
├─────────────────────────────────────────────────────────┤
│ 1. Identificar todos los textos de la feature          │
│ 2. Crear claves i18n descriptivas                      │
│ 3. Considerar contexto cultural (fechas, moneda, etc)  │
│ 4. Revisar sensibilidad cultural (emojis, expresiones) │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ FASE 2: TRADUCCIÓN (6 IDIOMAS)                         │
├─────────────────────────────────────────────────────────┤
│ 1. Escribir texto EN (inglés base)                     │
│ 2. Traducir a ES, DE, FR, IT, PT                       │
│ 3. Validar traducciones con hablantes nativos          │
│ 4. Ajustar por longitud de texto (algunos idiomas +30%)│
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ FASE 3: IMPLEMENTACIÓN                                 │
├─────────────────────────────────────────────────────────┤
│ 1. Agregar claves a app_en.arb (base)                  │
│ 2. Agregar traducciones a app_es/de/fr/it/pt.arb       │
│ 3. Implementar UI usando AppLocalizations.of(context)  │
│ 4. NUNCA usar Text('hardcoded string')                 │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ FASE 4: QA & VALIDACIÓN                                │
├─────────────────────────────────────────────────────────┤
│ 1. Test en TODOS los 6 idiomas                         │
│ 2. Validar que no hay overflow de texto                │
│ 3. Verificar que contexto cultural es correcto         │
│ 4. Run validation script (detecta textos sin traducir) │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 SPRINT 1: FIXES CRÍTICOS (Semana 1-2)

### Objetivo: Arreglar problemas existentes con i18n completo

---

### ✅ MEJORA 1.1: Fix Traducciones Ascendant

**Problema**: Horóscopos de ascendente solo en inglés

**Archivos afectados**:
- `lib/screens/ascendant_screen.dart`
- `lib/services/ascendant_horoscope_service.dart`

**Claves i18n necesarias** (6 idiomas × 12 signos = 72 traducciones):

```json
// app_en.arb
{
  "ascendantHoroscopeTitle": "Your {sign} Ascendant Today",
  "@ascendantHoroscopeTitle": {
    "description": "Title for ascendant horoscope",
    "placeholders": {
      "sign": {
        "type": "String",
        "example": "Aries"
      }
    }
  },

  "ascendantLoadingHoroscope": "Consulting cosmic energies for your rising sign...",
  "ascendantNoDataYet": "Enter your birth data to discover your ascendant",
  "ascendantHoroscopeGeneratedToday": "Generated today at {time}",
  "@ascendantHoroscopeGeneratedToday": {
    "placeholders": {
      "time": {
        "type": "String",
        "example": "3:45 PM"
      }
    }
  }
}
```

**Traducciones ES**:
```json
{
  "ascendantHoroscopeTitle": "Tu Ascendente {sign} Hoy",
  "ascendantLoadingHoroscope": "Consultando las energías cósmicas de tu signo ascendente...",
  "ascendantNoDataYet": "Ingresa tu fecha de nacimiento para descubrir tu ascendente",
  "ascendantHoroscopeGeneratedToday": "Generado hoy a las {time}"
}
```

**Implementación**:

```dart
// lib/screens/ascendant_screen.dart
Widget _buildHoroscopeContent(BuildContext context, String sign) {
  final l10n = AppLocalizations.of(context)!;

  return Column(
    children: [
      // ❌ MAL: Text('Your $sign Ascendant Today'),
      // ✅ BIEN:
      Text(l10n.ascendantHoroscopeTitle(sign)),

      // Horoscope content también traducido
      FutureBuilder<String>(
        future: _getTranslatedHoroscope(sign, l10n.localeName),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Text(l10n.ascendantLoadingHoroscope);
          }
          return Text(snapshot.data ?? l10n.ascendantNoDataYet);
        },
      ),
    ],
  );
}

Future<String> _getTranslatedHoroscope(String sign, String locale) async {
  // Call backend with locale parameter
  final response = await _horoscopeService.getAscendantHoroscope(
    sign: sign,
    language: locale, // 'en', 'es', 'de', etc.
  );
  return response.content;
}
```

**Checklist i18n**:
- [ ] ✅ Agregar 5 claves a app_en.arb
- [ ] ✅ Traducir a ES (5 claves)
- [ ] ✅ Traducir a DE (5 claves)
- [ ] ✅ Traducir a FR (5 claves)
- [ ] ✅ Traducir a IT (5 claves)
- [ ] ✅ Traducir a PT (5 claves)
- [ ] ✅ Modificar backend API para aceptar parámetro `language`
- [ ] ✅ Test en cada idioma
- [ ] ✅ Validar que no hay textos hardcodeados

**Tiempo estimado**: 2 días

---

### ✅ MEJORA 1.2: Fix Traducciones Cosmic Coach Goals

**Problema**: Metas del Cosmic Coach en inglés únicamente

**Archivos afectados**:
- `lib/screens/cosmic_coach_screen.dart`
- `lib/features/premium/screens/goal_planner/goal_planner_home_screen.dart`

**Claves i18n necesarias**:

```json
// app_en.arb
{
  "goalPlannerTitle": "Cosmic Goals",
  "goalPlannerSubtitle": "Set and track your cosmic intentions",
  "goalCategoryCareer": "Career & Purpose",
  "goalCategoryRelationships": "Relationships",
  "goalCategorySelfGrowth": "Self Growth",
  "goalCategoryHealth": "Health & Wellness",
  "goalCategoryFinances": "Finances",
  "goalStatusNotStarted": "Not Started",
  "goalStatusInProgress": "In Progress",
  "goalStatusCompleted": "Completed",
  "goalCreateNew": "Create New Goal",
  "goalEditTitle": "Edit Goal",
  "goalDeleteConfirm": "Are you sure you want to delete this goal?",
  "goalCompletedCelebration": "🎉 Goal completed! The universe celebrates with you!",
  "goalNoGoalsYet": "No cosmic goals yet. Create your first intention!",
  "goalDueDate": "Due date: {date}",
  "@goalDueDate": {
    "placeholders": {
      "date": {
        "type": "String",
        "example": "Dec 31, 2025"
      }
    }
  }
}
```

**Traducciones ES**:
```json
{
  "goalPlannerTitle": "Metas Cósmicas",
  "goalPlannerSubtitle": "Establece y rastrea tus intenciones cósmicas",
  "goalCategoryCareer": "Carrera y Propósito",
  "goalCategoryRelationships": "Relaciones",
  "goalCategorySelfGrowth": "Crecimiento Personal",
  "goalCategoryHealth": "Salud y Bienestar",
  "goalCategoryFinances": "Finanzas",
  "goalStatusNotStarted": "No Iniciada",
  "goalStatusInProgress": "En Progreso",
  "goalStatusCompleted": "Completada",
  "goalCreateNew": "Crear Nueva Meta",
  "goalEditTitle": "Editar Meta",
  "goalDeleteConfirm": "¿Estás seguro de que quieres eliminar esta meta?",
  "goalCompletedCelebration": "🎉 ¡Meta completada! ¡El universo celebra contigo!",
  "goalNoGoalsYet": "No tienes metas cósmicas aún. ¡Crea tu primera intención!",
  "goalDueDate": "Fecha límite: {date}"
}
```

**Implementación**:

```dart
// lib/screens/cosmic_coach_screen.dart
class GoalCard extends ConsumerWidget {
  final Goal goal;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;

    // ❌ MAL: Textos hardcodeados
    // String category = 'Career & Purpose';
    // String status = 'In Progress';

    // ✅ BIEN: Todo traducido
    String getCategoryText(GoalCategory category) {
      switch (category) {
        case GoalCategory.career:
          return l10n.goalCategoryCareer;
        case GoalCategory.relationships:
          return l10n.goalCategoryRelationships;
        case GoalCategory.selfGrowth:
          return l10n.goalCategorySelfGrowth;
        case GoalCategory.health:
          return l10n.goalCategoryHealth;
        case GoalCategory.finances:
          return l10n.goalCategoryFinances;
      }
    }

    String getStatusText(GoalStatus status) {
      switch (status) {
        case GoalStatus.notStarted:
          return l10n.goalStatusNotStarted;
        case GoalStatus.inProgress:
          return l10n.goalStatusInProgress;
        case GoalStatus.completed:
          return l10n.goalStatusCompleted;
      }
    }

    return Card(
      child: Column(
        children: [
          Text(getCategoryText(goal.category)),
          Text(getStatusText(goal.status)),
          if (goal.dueDate != null)
            Text(l10n.goalDueDate(_formatDate(goal.dueDate!, l10n.localeName))),
        ],
      ),
    );
  }

  String _formatDate(DateTime date, String locale) {
    // Formato de fecha según idioma
    final formatter = DateFormat.yMMMd(locale);
    return formatter.format(date);
  }
}
```

**Consideraciones culturales**:
- **Fechas**: Formato varía por idioma (MM/DD/YYYY en US, DD/MM/YYYY en Europa)
- **Emojis**: 🎉 es universal, pero verificar que sea apropiado en todas las culturas
- **Tone**: "The universe celebrates" puede sonar extraño en alemán → ajustar

**Checklist i18n**:
- [ ] ✅ Agregar 15 claves a app_en.arb
- [ ] ✅ Traducir a ES (15 claves)
- [ ] ✅ Traducir a DE (15 claves) - ajustar "universe celebrates"
- [ ] ✅ Traducir a FR (15 claves)
- [ ] ✅ Traducir a IT (15 claves)
- [ ] ✅ Traducir a PT (15 claves)
- [ ] ✅ Implementar formateo de fechas por locale
- [ ] ✅ Test en cada idioma
- [ ] ✅ Validar overflow de texto (alemán puede ser +30% más largo)

**Tiempo estimado**: 2 días

---

### ✅ MEJORA 1.3: Fix Compatibility Premium Features

**Problema**: Features premium en compatibility screen no funcionan

**Archivos afectados**:
- `lib/screens/compatibility_screen.dart:892, 1096`

**Claves i18n necesarias**:

```json
// app_en.arb
{
  "compatibilityPremiumLoading": "Analyzing cosmic connection...",
  "compatibilityDeepAnalysisTitle": "Deep Compatibility Analysis",
  "compatibilityRelationshipPatterns": "Relationship Patterns",
  "compatibilityLongTermPotential": "Long-term Potential",
  "compatibilityConflictResolution": "Conflict Resolution Strategies",
  "compatibilityGrowthOpportunities": "Growth Opportunities Together",
  "compatibilityUpgradePrompt": "Unlock deep analysis with Stellar",
  "compatibilityViewHistory": "View Compatibility History",
  "compatibilityNoHistoryYet": "No previous compatibility checks",
  "compatibilityPremiumBenefit": "Save and track all your compatibility analyses"
}
```

**Implementación con AsyncValue correcto**:

```dart
// lib/screens/compatibility_screen.dart
Widget _buildPremiumSection(BuildContext context, WidgetRef ref) {
  final l10n = AppLocalizations.of(context)!;
  final isPremiumAsync = ref.watch(isPremiumUserProvider);

  return isPremiumAsync.when(
    data: (isPremium) {
      if (!isPremium) {
        return _buildUpgradePrompt(l10n);
      }

      // Premium content
      return Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            l10n.compatibilityDeepAnalysisTitle,
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          SizedBox(height: 16),
          _buildRelationshipPatterns(l10n),
          _buildLongTermPotential(l10n),
          _buildConflictStrategies(l10n),
          _buildGrowthOpportunities(l10n),
          SizedBox(height: 24),
          _buildHistorySection(l10n),
        ],
      );
    },
    loading: () => Center(
      child: Column(
        children: [
          CircularProgressIndicator(),
          SizedBox(height: 16),
          Text(l10n.compatibilityPremiumLoading),
        ],
      ),
    ),
    error: (_, __) => _buildUpgradePrompt(l10n),
  );
}

Widget _buildUpgradePrompt(AppLocalizations l10n) {
  return Card(
    child: Padding(
      padding: EdgeInsets.all(16),
      child: Column(
        children: [
          Icon(Icons.lock_outline, size: 48),
          SizedBox(height: 16),
          Text(
            l10n.compatibilityUpgradePrompt,
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          SizedBox(height: 8),
          Text(l10n.compatibilityPremiumBenefit),
          SizedBox(height: 16),
          ElevatedButton(
            onPressed: () => _navigateToPremiumScreen(),
            child: Text(l10n.unlockPremium),
          ),
        ],
      ),
    ),
  );
}
```

**Checklist i18n**:
- [ ] ✅ Agregar 10 claves a app_en.arb
- [ ] ✅ Traducir a todos los idiomas (10 × 6 = 60 traducciones)
- [ ] ✅ Fix AsyncValue handling
- [ ] ✅ Test premium/free flows en cada idioma
- [ ] ✅ Validar que upgrade prompts se ven bien

**Tiempo estimado**: 2 días

---

## 🚀 SPRINT 2: AI INSIGHTS COUNTER (Semana 3-4)

### ✅ MEJORA 2.1: Implementar Contador de AI Insights

**Objetivo**: Mostrar límite de 10 insights/día para Cosmic, ilimitado para Stellar

**Archivos a crear/modificar**:
- `lib/widgets/premium/ai_insights_counter_widget.dart` (NUEVO)
- `lib/services/ai_insights_usage_tracker.dart` (NUEVO)
- `lib/screens/cosmic_coach_screen.dart` (MODIFICAR)

**Claves i18n necesarias**:

```json
// app_en.arb
{
  "aiInsightsRemainingToday": "{count} AI insights remaining today",
  "@aiInsightsRemainingToday": {
    "description": "Shows how many AI insights user has left",
    "placeholders": {
      "count": {
        "type": "int",
        "example": "7"
      }
    }
  },

  "aiInsightsUnlimited": "∞ Unlimited AI insights",
  "aiInsightsLimitReached": "Daily limit reached",
  "aiInsightsResetsAt": "Resets at midnight ({timezone})",
  "@aiInsightsResetsAt": {
    "placeholders": {
      "timezone": {
        "type": "String",
        "example": "PST"
      }
    }
  },

  "aiInsightsUpgradePrompt": "Want unlimited insights?",
  "aiInsightsUpgradeButton": "Upgrade to Stellar",
  "aiInsightsLowWarning": "Only {count} insights left today!",
  "@aiInsightsLowWarning": {
    "placeholders": {
      "count": {
        "type": "int",
        "example": "2"
      }
    }
  },

  "aiInsightsWhatCounts": "What counts as an AI insight?",
  "aiInsightsExplanation": "Each question to Cosmic Coach or Crisis AI uses one insight. Birth charts and compatibility don't count.",

  "aiInsightsUsageHistory": "Today's Usage",
  "aiInsightsUsedAt": "Used at {time}",
  "@aiInsightsUsedAt": {
    "placeholders": {
      "time": {
        "type": "String",
        "example": "3:45 PM"
      }
    }
  }
}
```

**Traducciones ES**:
```json
{
  "aiInsightsRemainingToday": "{count} insights de IA restantes hoy",
  "aiInsightsUnlimited": "∞ Insights de IA ilimitados",
  "aiInsightsLimitReached": "Límite diario alcanzado",
  "aiInsightsResetsAt": "Se reinicia a medianoche ({timezone})",
  "aiInsightsUpgradePrompt": "¿Quieres insights ilimitados?",
  "aiInsightsUpgradeButton": "Mejora a Stellar",
  "aiInsightsLowWarning": "¡Solo te quedan {count} insights hoy!",
  "aiInsightsWhatCounts": "¿Qué cuenta como insight de IA?",
  "aiInsightsExplanation": "Cada pregunta al Coach Cósmico o Crisis AI usa un insight. Las cartas natales y compatibilidad no cuentan.",
  "aiInsightsUsageHistory": "Uso de Hoy",
  "aiInsightsUsedAt": "Usado a las {time}"
}
```

**Implementación**:

```dart
// lib/widgets/premium/ai_insights_counter_widget.dart
class AIInsightsCounter extends ConsumerWidget {
  const AIInsightsCounter({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final tier = ref.watch(currentTierProvider);
    final usageTracker = ref.watch(aiInsightsUsageProvider);

    // Stellar y Universe tienen ilimitado
    if (tier == PremiumTier.stellar || tier == PremiumTier.universe) {
      return _buildUnlimitedBadge(l10n);
    }

    // Cosmic tiene límite de 10
    return usageTracker.when(
      data: (usage) {
        final remaining = 10 - usage.usedToday;
        final color = remaining < 3 ? Colors.red : Colors.orange;

        return Container(
          padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: color),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.psychology, color: color, size: 20),
              SizedBox(width: 8),
              Text(
                l10n.aiInsightsRemainingToday(remaining),
                style: TextStyle(
                  color: color,
                  fontWeight: FontWeight.bold,
                ),
              ),
              if (remaining < 3) ...[
                SizedBox(width: 8),
                GestureDetector(
                  onTap: () => _showUpgradeDialog(context, l10n),
                  child: Icon(Icons.arrow_upward, color: color, size: 16),
                ),
              ],
            ],
          ),
        );
      },
      loading: () => SizedBox.shrink(),
      error: (_, __) => SizedBox.shrink(),
    );
  }

  Widget _buildUnlimitedBadge(AppLocalizations l10n) {
    return Container(
      padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.purple, Colors.pink],
        ),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(Icons.all_inclusive, color: Colors.white, size: 20),
          SizedBox(width: 8),
          Text(
            l10n.aiInsightsUnlimited,
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  void _showUpgradeDialog(BuildContext context, AppLocalizations l10n) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(l10n.aiInsightsLowWarning(2)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(l10n.aiInsightsUpgradePrompt),
            SizedBox(height: 16),
            Text(
              l10n.aiInsightsExplanation,
              style: TextStyle(fontSize: 12, color: Colors.grey),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text(l10n.cancel),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.pop(context);
              Navigator.pushNamed(context, '/premium');
            },
            child: Text(l10n.aiInsightsUpgradeButton),
          ),
        ],
      ),
    );
  }
}

// lib/services/ai_insights_usage_tracker.dart
class AIInsightsUsage {
  final int usedToday;
  final DateTime lastResetDate;
  final List<DateTime> usageTimestamps;

  AIInsightsUsage({
    required this.usedToday,
    required this.lastResetDate,
    required this.usageTimestamps,
  });

  bool get hasReachedLimit => usedToday >= 10;
  int get remaining => 10 - usedToday;
}

final aiInsightsUsageProvider = StreamProvider<AIInsightsUsage>((ref) async* {
  final prefs = await SharedPreferences.getInstance();

  while (true) {
    final usage = _loadUsageFromPrefs(prefs);
    yield usage;
    await Future.delayed(Duration(seconds: 30)); // Update every 30s
  }
});
```

**Consideraciones culturales**:
- **Timezone**: Mostrar timezone del usuario (PST, CET, JST, etc.)
- **Formato 12h vs 24h**: US usa AM/PM, Europa usa 24h
- **Términos**: "Midnight" = "Medianoche" (ES), "Mitternacht" (DE), "Minuit" (FR)

**Checklist i18n**:
- [ ] ✅ Agregar 11 claves a app_en.arb
- [ ] ✅ Traducir a ES (11 claves)
- [ ] ✅ Traducir a DE (11 claves)
- [ ] ✅ Traducir a FR (11 claves)
- [ ] ✅ Traducir a IT (11 claves)
- [ ] ✅ Traducir a PT (11 claves)
- [ ] ✅ Implementar formato de hora por locale (12h vs 24h)
- [ ] ✅ Test en cada idioma
- [ ] ✅ Validar que contador se ve bien en todos los idiomas
- [ ] ✅ Test upgrade flow en cada idioma

**Tiempo estimado**: 4 días

---

## 🚀 SPRINT 3: STELLAR EXCLUSIVE FEATURES (Semana 5-7)

### ✅ MEJORA 3.1: PDF Export de Birth Chart (Stellar Only)

**Objetivo**: Feature exclusiva de Stellar - Exportar carta natal a PDF profesional

**Archivos a crear**:
- `lib/services/premium/pdf_export_service.dart` (NUEVO)
- `lib/widgets/premium/pdf_export_button.dart` (NUEVO)

**Claves i18n necesarias**:

```json
// app_en.arb
{
  "pdfExportTitle": "Export Birth Chart",
  "pdfExportDescription": "Generate a professional PDF of your complete natal chart",
  "pdfExportButton": "Export to PDF",
  "pdfExportGenerating": "Generating your cosmic blueprint...",
  "pdfExportSuccess": "PDF exported successfully!",
  "pdfExportError": "Failed to generate PDF. Please try again.",
  "pdfExportShareTitle": "Share your birth chart",
  "pdfExportSaveTitle": "Save to Files",
  "pdfExportPrintTitle": "Print",

  "pdfExportStellarOnly": "PDF Export is a Stellar feature",
  "pdfExportUpgradeMessage": "Upgrade to Stellar to export professional PDFs of your charts",
  "pdfExportUpgradeButton": "Unlock PDF Export",

  "pdfContentTitle": "{name}'s Birth Chart",
  "@pdfContentTitle": {
    "placeholders": {
      "name": {
        "type": "String",
        "example": "Maria"
      }
    }
  },

  "pdfContentSubtitle": "Born {date} at {time} in {location}",
  "@pdfContentSubtitle": {
    "placeholders": {
      "date": {
        "type": "String",
        "example": "March 15, 1990"
      },
      "time": {
        "type": "String",
        "example": "3:45 PM"
      },
      "location": {
        "type": "String",
        "example": "New York, USA"
      }
    }
  },

  "pdfSectionPlanets": "Planetary Positions",
  "pdfSectionHouses": "House Placements",
  "pdfSectionAspects": "Major Aspects",
  "pdfSectionInterpretation": "Chart Interpretation",
  "pdfFooter": "Generated with Zodiac App • Premium Stellar",
  "pdfDisclaimer": "For entertainment purposes only"
}
```

**Traducciones ES**:
```json
{
  "pdfExportTitle": "Exportar Carta Natal",
  "pdfExportDescription": "Genera un PDF profesional de tu carta natal completa",
  "pdfExportButton": "Exportar a PDF",
  "pdfExportGenerating": "Generando tu mapa cósmico...",
  "pdfExportSuccess": "¡PDF exportado exitosamente!",
  "pdfExportError": "Error al generar PDF. Por favor intenta de nuevo.",
  "pdfExportShareTitle": "Compartir tu carta natal",
  "pdfExportSaveTitle": "Guardar en Archivos",
  "pdfExportPrintTitle": "Imprimir",

  "pdfExportStellarOnly": "Exportar PDF es una función Stellar",
  "pdfExportUpgradeMessage": "Mejora a Stellar para exportar PDFs profesionales de tus cartas",
  "pdfExportUpgradeButton": "Desbloquear Exportación PDF",

  "pdfContentTitle": "Carta Natal de {name}",
  "pdfContentSubtitle": "Nacido el {date} a las {time} en {location}",

  "pdfSectionPlanets": "Posiciones Planetarias",
  "pdfSectionHouses": "Casas Astrológicas",
  "pdfSectionAspects": "Aspectos Principales",
  "pdfSectionInterpretation": "Interpretación de la Carta",
  "pdfFooter": "Generado con Zodiac App • Premium Stellar",
  "pdfDisclaimer": "Solo para fines de entretenimiento"
}
```

**Implementación**:

```dart
// lib/widgets/premium/pdf_export_button.dart
class PDFExportButton extends ConsumerWidget {
  final BirthChartData chartData;

  const PDFExportButton({required this.chartData, Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppLocalizations.of(context)!;
    final tier = ref.watch(currentTierProvider);

    // Feature gate - Solo Stellar y Universe
    if (tier != PremiumTier.stellar && tier != PremiumTier.universe) {
      return _buildLockedButton(context, l10n);
    }

    return ElevatedButton.icon(
      icon: Icon(Icons.picture_as_pdf),
      label: Text(l10n.pdfExportButton),
      onPressed: () => _exportToPDF(context, l10n),
    );
  }

  Widget _buildLockedButton(BuildContext context, AppLocalizations l10n) {
    return OutlinedButton.icon(
      icon: Icon(Icons.lock_outline),
      label: Text(l10n.pdfExportButton),
      onPressed: () => _showUpgradeDialog(context, l10n),
    );
  }

  Future<void> _exportToPDF(BuildContext context, AppLocalizations l10n) async {
    // Mostrar loading
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => Center(
        child: Card(
          child: Padding(
            padding: EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                CircularProgressIndicator(),
                SizedBox(height: 16),
                Text(l10n.pdfExportGenerating),
              ],
            ),
          ),
        ),
      ),
    );

    try {
      final pdfService = PDFExportService();
      final pdfBytes = await pdfService.generateBirthChartPDF(
        chartData: chartData,
        locale: l10n.localeName, // ¡IMPORTANTE! PDF en idioma del usuario
      );

      Navigator.pop(context); // Cerrar loading

      // Mostrar opciones de compartir
      await _showShareOptions(context, pdfBytes, l10n);

      // Success snackbar
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(l10n.pdfExportSuccess),
          backgroundColor: Colors.green,
        ),
      );

    } catch (e) {
      Navigator.pop(context); // Cerrar loading

      // Error snackbar
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(l10n.pdfExportError),
          backgroundColor: Colors.red,
        ),
      );
    }
  }

  Future<void> _showShareOptions(
    BuildContext context,
    Uint8List pdfBytes,
    AppLocalizations l10n,
  ) async {
    return showModalBottomSheet(
      context: context,
      builder: (context) => Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          ListTile(
            leading: Icon(Icons.share),
            title: Text(l10n.pdfExportShareTitle),
            onTap: () => _sharePDF(pdfBytes, l10n),
          ),
          ListTile(
            leading: Icon(Icons.save_alt),
            title: Text(l10n.pdfExportSaveTitle),
            onTap: () => _savePDF(pdfBytes, l10n),
          ),
          ListTile(
            leading: Icon(Icons.print),
            title: Text(l10n.pdfExportPrintTitle),
            onTap: () => _printPDF(pdfBytes, l10n),
          ),
        ],
      ),
    );
  }
}

// lib/services/premium/pdf_export_service.dart
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;

class PDFExportService {
  Future<Uint8List> generateBirthChartPDF({
    required BirthChartData chartData,
    required String locale, // 'en', 'es', 'de', etc.
  }) async {
    final pdf = pw.Document();

    // Cargar traducciones según locale
    final translations = await _loadTranslations(locale);

    pdf.addPage(
      pw.Page(
        build: (context) => pw.Column(
          crossAxisAlignment: pw.CrossAxisAlignment.start,
          children: [
            // Título traducido
            pw.Text(
              translations['pdfContentTitle']!.replaceAll(
                '{name}',
                chartData.name,
              ),
              style: pw.TextStyle(fontSize: 24, fontWeight: pw.FontWeight.bold),
            ),

            pw.SizedBox(height: 8),

            // Subtítulo con fecha/hora formateada según locale
            pw.Text(
              _formatSubtitle(chartData, translations, locale),
              style: pw.TextStyle(fontSize: 14, color: PdfColors.grey),
            ),

            pw.SizedBox(height: 24),

            // Secciones traducidas
            _buildSection(translations['pdfSectionPlanets']!, chartData.planets, locale),
            _buildSection(translations['pdfSectionHouses']!, chartData.houses, locale),
            _buildSection(translations['pdfSectionAspects']!, chartData.aspects, locale),

            pw.Spacer(),

            // Footer traducido
            pw.Text(
              translations['pdfFooter']!,
              style: pw.TextStyle(fontSize: 10, color: PdfColors.grey),
            ),
            pw.Text(
              translations['pdfDisclaimer']!,
              style: pw.TextStyle(fontSize: 8, color: PdfColors.grey),
            ),
          ],
        ),
      ),
    );

    return pdf.save();
  }

  Future<Map<String, String>> _loadTranslations(String locale) async {
    // Cargar traducciones desde app_${locale}.arb
    final String arbContent = await rootBundle.loadString(
      'assets/l10n/app_$locale.arb',
    );
    final Map<String, dynamic> json = jsonDecode(arbContent);

    // Extraer solo las claves de PDF
    return {
      'pdfContentTitle': json['pdfContentTitle'] ?? '',
      'pdfContentSubtitle': json['pdfContentSubtitle'] ?? '',
      'pdfSectionPlanets': json['pdfSectionPlanets'] ?? '',
      'pdfSectionHouses': json['pdfSectionHouses'] ?? '',
      'pdfSectionAspects': json['pdfSectionAspects'] ?? '',
      'pdfSectionInterpretation': json['pdfSectionInterpretation'] ?? '',
      'pdfFooter': json['pdfFooter'] ?? '',
      'pdfDisclaimer': json['pdfDisclaimer'] ?? '',
    };
  }

  String _formatSubtitle(
    BirthChartData chartData,
    Map<String, String> translations,
    String locale,
  ) {
    // Formatear fecha según locale
    final dateFormatter = DateFormat.yMMMMd(locale);
    final timeFormatter = DateFormat.jm(locale); // 12h o 24h según locale

    return translations['pdfContentSubtitle']!
      .replaceAll('{date}', dateFormatter.format(chartData.birthDate))
      .replaceAll('{time}', timeFormatter.format(chartData.birthTime))
      .replaceAll('{location}', chartData.birthLocation);
  }
}
```

**Consideraciones culturales para PDF**:
- **Formato de página**: A4 (Europa) vs Letter (US) - detectar por locale
- **Formato de fecha**: Varía por país
- **Dirección de texto**: LTR para todos tus idiomas (pero considerar RTL futuro)
- **Nombres de planetas**: Traducir Mercury→Mercurio, Venus→Venus, etc.

**Checklist i18n**:
- [ ] ✅ Agregar 19 claves a app_en.arb
- [ ] ✅ Traducir a ES (19 claves)
- [ ] ✅ Traducir a DE (19 claves)
- [ ] ✅ Traducir a FR (19 claves)
- [ ] ✅ Traducir a IT (19 claves)
- [ ] ✅ Traducir a PT (19 claves)
- [ ] ✅ Traducir nombres de planetas (12 × 6 = 72 traducciones)
- [ ] ✅ Traducir nombres de signos (12 × 6 = 72 traducciones)
- [ ] ✅ Implementar formato de fecha/hora por locale en PDF
- [ ] ✅ Test PDF en cada idioma
- [ ] ✅ Validar que PDF se ve profesional en todos los idiomas
- [ ] ✅ Test upgrade flow cuando usuario es Cosmic

**Tiempo estimado**: 5 días

---

### ✅ MEJORA 3.2: Relationship Pattern Analysis (Stellar Only)

*(Continuaría con todas las demás mejoras siguiendo el mismo patrón...)*

**Tiempo estimado para Sprint 3 completo**: 3 semanas

---

## 📊 HERRAMIENTAS Y VALIDACIÓN i18n

### Script de Validación Automática

Crear script que detecte problemas i18n:

```bash
# scripts/validate_i18n.sh
#!/bin/bash

echo "🌍 Validando internacionalización..."

# 1. Detectar textos hardcodeados en Dart
echo "1️⃣ Buscando Text('hardcoded')..."
grep -r "Text('" lib/ --include="*.dart" | grep -v "AppLocalizations" | grep -v "// OK:" > hardcoded.txt

if [ -s hardcoded.txt ]; then
  echo "❌ Encontrados textos hardcodeados:"
  cat hardcoded.txt
  exit 1
fi

# 2. Verificar que todas las claves existen en todos los idiomas
echo "2️⃣ Verificando paridad de claves..."
python3 scripts/check_translation_parity.py

# 3. Detectar traducciones faltantes (valores vacíos)
echo "3️⃣ Buscando traducciones vacías..."
for lang in en es de fr it pt; do
  empty=$(jq -r 'to_entries[] | select(.value == "") | .key' assets/l10n/app_$lang.arb)
  if [ ! -z "$empty" ]; then
    echo "❌ Traducciones vacías en app_$lang.arb:"
    echo "$empty"
    exit 1
  fi
done

echo "✅ Validación i18n exitosa!"
```

```python
# scripts/check_translation_parity.py
import json
import sys

languages = ['en', 'es', 'de', 'fr', 'it', 'pt']
base_lang = 'en'

# Cargar claves de inglés (base)
with open(f'assets/l10n/app_{base_lang}.arb', 'r') as f:
    base_keys = set(json.load(f).keys())
    # Filtrar claves que empiezan con @ (metadata)
    base_keys = {k for k in base_keys if not k.startswith('@')}

errors = []

# Verificar cada idioma
for lang in languages:
    if lang == base_lang:
        continue

    with open(f'assets/l10n/app_{lang}.arb', 'r') as f:
        lang_keys = set(json.load(f).keys())
        lang_keys = {k for k in lang_keys if not k.startswith('@')}

    # Claves faltantes
    missing = base_keys - lang_keys
    if missing:
        errors.append(f"❌ {lang.upper()}: Faltan {len(missing)} claves:")
        for key in sorted(missing)[:5]:  # Mostrar primeras 5
            errors.append(f"   - {key}")
        if len(missing) > 5:
            errors.append(f"   ... y {len(missing) - 5} más")

    # Claves extras (no en base)
    extra = lang_keys - base_keys
    if extra:
        errors.append(f"⚠️  {lang.upper()}: {len(extra)} claves extras (no en EN)")

if errors:
    print("\n".join(errors))
    sys.exit(1)
else:
    print("✅ Todas las traducciones están sincronizadas")
```

### Integración en CI/CD

Agregar a tu pipeline:

```yaml
# .github/workflows/i18n_validation.yml
name: i18n Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Validate i18n
        run: |
          chmod +x scripts/validate_i18n.sh
          ./scripts/validate_i18n.sh
```

---

## 📈 MÉTRICAS DE ÉXITO

### KPIs por Sprint:

**Sprint 1 (Fixes)**:
- [ ] 0 textos hardcodeados en Ascendant/Goals (validation script pasa)
- [ ] Engagement +20% en usuarios ES/DE/FR/IT/PT
- [ ] Compatibility premium features funcionan 100%

**Sprint 2 (AI Counter)**:
- [ ] 80%+ usuarios Cosmic ven el contador
- [ ] 15%+ usuarios Cosmic llegan a límite (muestra necesidad)
- [ ] 5%+ conversión Cosmic→Stellar (counter como trigger)

**Sprint 3 (Stellar Features)**:
- [ ] 30%+ usuarios Stellar usan PDF export en primer mes
- [ ] 10%+ conversión Cosmic→Stellar (features exclusivas claras)

---

## 🎯 CHECKLIST GENERAL i18n-FIRST

Para TODA nueva feature:

### Antes de Escribir Código:
- [ ] ✅ Listar todos los textos visibles de la feature
- [ ] ✅ Crear claves i18n descriptivas (snake_case)
- [ ] ✅ Considerar plurales (1 item vs 5 items)
- [ ] ✅ Considerar placeholders dinámicos ({count}, {name}, etc.)
- [ ] ✅ Revisar sensibilidad cultural (emojis, metáforas)

### Durante Implementación:
- [ ] ✅ Agregar claves a app_en.arb (base)
- [ ] ✅ Traducir a ES, DE, FR, IT, PT
- [ ] ✅ Usar AppLocalizations.of(context)! en código
- [ ] ✅ NUNCA Text('hardcoded string')
- [ ] ✅ Formatear fechas/horas según locale
- [ ] ✅ Formatear números/moneda según locale

### Testing:
- [ ] ✅ Test visual en todos los 6 idiomas
- [ ] ✅ Verificar que no hay overflow de texto
- [ ] ✅ Run validation script (0 errores)
- [ ] ✅ Test con idiomas largos (alemán +30%)
- [ ] ✅ Verificar que metadata (@placeholders) es correcto

### Antes de Commit:
- [ ] ✅ Run `flutter gen-l10n` (genera código)
- [ ] ✅ Run `scripts/validate_i18n.sh` (pasa)
- [ ] ✅ Commit incluye todos los .arb files
- [ ] ✅ PR description menciona "✅ i18n completo"

---

## 🚀 CRONOGRAMA COMPLETO

```
SEMANA 1-2: Sprint 1 - Fixes Críticos
├─ Día 1-2: Fix Ascendant translations (i18n completo)
├─ Día 3-4: Fix Cosmic Coach goals (i18n completo)
├─ Día 5-6: Fix Compatibility premium features
└─ Día 7-8: QA en 6 idiomas + Buffer

SEMANA 3-4: Sprint 2 - AI Insights Counter
├─ Día 1-2: Crear AI insights counter widget (i18n completo)
├─ Día 3-4: Implementar usage tracker service
├─ Día 5-6: Integrar en Cosmic Coach screen
├─ Día 7-8: QA en 6 idiomas + Upgrade flows

SEMANA 5-7: Sprint 3 - Stellar Exclusive Features
├─ Día 1-5: PDF Export (i18n completo)
├─ Día 6-10: Relationship Pattern Analysis (i18n completo)
├─ Día 11-15: Priority AI Responses (i18n completo)
└─ Día 16-21: QA extensivo + Buffer

SEMANA 8: Sprint 4 - Polish & Launch
├─ Día 1-2: Crisis AI marketing improvements
├─ Día 3-4: Universe tier repositioning
├─ Día 5-6: Remove debug code
└─ Día 7: Final QA + Release
```

**Total**: 8 semanas (56 días)

---

## 💰 INVERSIÓN ESTIMADA

### Horas de Desarrollo:
- Sprint 1: 60 horas
- Sprint 2: 80 horas
- Sprint 3: 120 horas
- Sprint 4: 40 horas
- **Total**: 300 horas

### Traducción Professional (opcional):
- 150+ nuevas claves × 5 idiomas = 750 traducciones
- @ $0.10/palabra promedio = ~$3,000-5,000
- *Alternativa*: DeepL API + revisión manual = $500

### ROI Proyectado:
- Revenue adicional: **+$35K/año**
- Inversión: ~$5K (traducciones) + desarrollo
- **ROI**: 7x en primer año

---

## 🎬 PRÓXIMOS PASOS INMEDIATOS

1. **Revisar y aprobar este plan**
2. **Setup validation scripts** (1 día)
3. **Crear branch**: `feature/premium-improvements-i18n`
4. **Comenzar Sprint 1, Día 1**: Fix Ascendant translations

¿Quieres que comience con el Sprint 1 inmediatamente? 🚀
