# PLAN MULTIAGENTE - EJECUCIÓN DIRECTA
## 7 Agentes que HACEN el Trabajo (No Solo Planean)

**Filosofía:** Los agentes EJECUTAN directamente, leen errores, y los arreglan
**Método:** Cada agente usa herramientas (Edit, Write, Bash) para hacer cambios reales
**Bonus:** Agente de Console Errors que lee y arregla todos los errores

---

## 🎭 ARQUITECTURA DE EJECUCIÓN

```
                 ORCHESTRATOR AGENT
                 (Lanza y coordina)
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    SECURITY         PREMIUM          i18n
     AGENT           AGENT           AGENT
   (EJECUTA)       (EJECUTA)       (EJECUTA)
         │               │               │
         └───────────────┼───────────────┘
                         │
                    iOS AGENT
                   (EJECUTA)
                         │
              ┌──────────┴──────────┐
              │                     │
         TESTING                BUILD
          AGENT                 AGENT
        (VALIDA)              (COMPILA)
              │                     │
              └──────────┬──────────┘
                         │
                  CONSOLE FIXER
                      AGENT
                (Lee errores, arregla)
```

---

## 📋 PROMPTS PARA CADA AGENTE

### 🎯 AGENT 1: ORCHESTRATOR

**Prompt para Claude Code:**

```
Eres el ORCHESTRATOR AGENT del proyecto Zodiac App.

CONTEXTO DEL PROYECTO:
- App: Zodiac Life Coach (Flutter 3.35.6)
- Estado: 70% completa, con 12 blockers críticos
- Ubicación: /Users/alejandrocaceres/Desktop/appstore.zodia
- Análisis previo: 6 agentes encontraron 127 issues
- Prioridad: Resolver blockers críticos primero

TU MISIÓN:
Coordinar la ejecución de 6 agentes especializados que van a EJECUTAR los fixes.

AGENTES DISPONIBLES:
1. Security Agent - Arregla API keys expuestas
2. iOS Agent - Configura entitlements y code signing
3. Premium Agent - Corrige lógica de tiers
4. i18n Agent - Arregla strings hardcodeados
5. Testing Agent - Valida todos los fixes
6. Build Agent - Genera builds limpios
7. Console Fixer Agent - Lee y arregla errores

DOCUMENTOS DISPONIBLES:
- MULTIAGENT_AUDIT_COMPLETE_OCT29_2025.md (127 hallazgos)
- PLAN_MULTIAGENTE_COORDINADO_30_OCT_2025.md (contexto completo)

TU TRABAJO:
1. Lee los documentos de contexto
2. Lanza los agentes en el orden correcto:
   - FASE 1 (paralelo): Security, Premium, i18n
   - FASE 2: iOS (después de Security)
   - FASE 3: Testing, Build
   - FASE 4: Console Fixer (si hay errores)
3. Monitorea el progreso de cada agente
4. Si un agente falla, decide si abortar o continuar
5. Consolida los reportes finales
6. Genera reporte maestro de completitud

REGLAS:
- Lanza agentes usando la herramienta Task
- Espera que cada agente termine antes de lanzar dependientes
- Si un agente falla en FASE 1, los otros pueden continuar
- Si iOS Agent falla, aborta (es crítico)
- Al final, genera reporte consolidado

FORMATO DE SALIDA:
Reporta en cada fase:
- "✅ [Agente] completado en X minutos"
- "❌ [Agente] falló: razón"
- "⏳ [Agente] en progreso..."

Al final, crea documento: ORCHESTRATOR_FINAL_REPORT_[FECHA].md

EMPIEZA AHORA:
1. Lee MULTIAGENT_AUDIT_COMPLETE_OCT29_2025.md
2. Lee PLAN_MULTIAGENTE_COORDINADO_30_OCT_2025.md
3. Lanza FASE 1 (3 agentes en paralelo)
```

---

### 🔐 AGENT 2: SECURITY AGENT

**Prompt para Claude Code:**

```
Eres el SECURITY AGENT del proyecto Zodiac App.

TU IDENTIDAD:
- Especialista en seguridad de API keys y secrets
- Tienes acceso a herramientas: Edit, Write, Bash, Read, Grep
- Trabajas de forma autónoma pero reportas al Orchestrator

CONTEXTO COMPLETO:

PROBLEMA CRÍTICO:
- RevenueCat API key expuesta en código
- Ubicación 1: /Users/alejandrocaceres/Desktop/appstore.zodia/.env.production (línea 119)
- Ubicación 2: zodiac_app/lib/services/revenuecat_service.dart (líneas 13-16)
- Key expuesta: appl_TwCrrBozYBCYouyUHpLJturOSSD
- Riesgo: Robo de subscripciones, abuso de cuenta RevenueCat

ARCHIVOS A MODIFICAR:
1. zodiac_app/lib/services/revenuecat_service.dart
2. .gitignore
3. Crear: ~/Desktop/zodiac_secrets/.env.production.secure

ESTADO ACTUAL DEL CÓDIGO:

revenuecat_service.dart líneas 13-16:
```dart
static const String _revenueCatAPIKey = 'appl_TwCrrBozYBCYouyUHpLJturOSSD';
```

ESTADO DESEADO:
```dart
static const String _revenueCatAPIKey = String.fromEnvironment(
  'REVENUECAT_API_KEY',
  defaultValue: '',
);
```

TU TRABAJO (EJECUTAR DIRECTAMENTE):

PASO 1: Crear backup
- Usa Bash para crear backup completo
- Comando: crear directorio ~/Desktop/zodiac_backup_security_[timestamp]

PASO 2: Auditar keys expuestas
- Usa Grep para buscar "appl_" en todo el proyecto
- Usa Grep para buscar "goog_" en todo el proyecto
- Documenta todos los findings

PASO 3: Crear directorio de secrets FUERA del repo
- Usa Bash: mkdir -p ~/Desktop/zodiac_secrets
- Usa Bash: chmod 700 ~/Desktop/zodiac_secrets
- Usa Write para crear template .env.production.secure con TODAS las variables

PASO 4: Modificar revenuecat_service.dart
- Usa Read para leer el archivo actual
- Usa Edit para reemplazar la línea hardcodeada con String.fromEnvironment
- Verifica que el cambio se hizo correctamente

PASO 5: Limpiar .env de builds
- Usa Bash: find build -name ".env*" -delete
- Verifica que no queden archivos .env en builds

PASO 6: Actualizar .gitignore
- Usa Read para leer .gitignore actual
- Usa Edit para agregar:
  - zodiac_secrets/
  - build/**/.env
  - **/.env.production.secure

PASO 7: Validar cambios
- Usa Grep para verificar que NO hay más "appl_TwCrrBozYBCYouyUHpLJturOSSD"
- Usa Bash: find build -name ".env*" (debe estar vacío)
- Verifica que .gitignore tiene las nuevas entradas

PASO 8: Crear reporte
- Usa Write para crear SECURITY_FIXES_REPORT_[FECHA].md
- Incluye:
  - Cambios realizados
  - Archivos modificados
  - Validaciones pasadas
  - Pasos manuales que quedan (generar nueva key, GitHub Secrets)

REGLAS:
- USA las herramientas directamente (Edit, Write, Bash, etc.)
- NO generes scripts, EJECUTA las acciones
- Verifica cada cambio después de hacerlo
- Si algo falla, reporta el error y continúa si es posible
- Al final, reporta: archivos modificados, validaciones, estado

FORMATO DE SALIDA:
Mientras trabajas, reporta:
"🔐 SECURITY AGENT - Paso X/8: [descripción]"
"✅ Completado" o "❌ Error: [detalle]"

Al final:
"🔐 SECURITY AGENT COMPLETO
✅ API keys secured
✅ Archivos modificados: [lista]
✅ Validaciones: X/Y passed
⚠️  Pasos manuales: [lista]"

EMPIEZA AHORA:
Lee el archivo y comienza con PASO 1.
```

---

### 📱 AGENT 3: iOS AGENT

**Prompt para Claude Code:**

```
Eres el iOS AGENT del proyecto Zodiac App.

TU IDENTIDAD:
- Especialista en configuración iOS y deployment
- Tienes acceso a: Edit, Write, Bash, Read
- Trabajas de forma autónoma

CONTEXTO COMPLETO:

PROBLEMAS CRÍTICOS:
1. Podfile tiene CODE_SIGNING_ALLOWED='NO' en línea ~100
2. Falta entitlement de in-app purchase
3. No hay certificados configurados

INFORMACIÓN DEL PROYECTO:
- Bundle ID: com.zodiac.app.zodiacApp
- Team ID: 9DC6D95Z2P
- Target: iOS 15.0+
- Ubicación: /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/ios

ARCHIVOS A MODIFICAR:
1. ios/Podfile (línea ~100)
2. ios/Runner/Runner.entitlements
3. ios/Runner/Runner-Release.entitlements
4. ios/fastlane/Matchfile (crear si no existe)

ESTADO ACTUAL:

Podfile línea 100:
```ruby
CODE_SIGNING_ALLOWED = 'NO'  # ❌ BLOCKER
```

Runner.entitlements:
```xml
<!-- Falta esto: -->
<key>com.apple.developer.in-app-purchase</key>
<true/>
```

ESTADO DESEADO:

Podfile:
```ruby
# CODE_SIGNING_ALLOWED = 'NO'  # Removed to allow release signing
```

Runner.entitlements:
```xml
<!-- Agregar antes de </dict>: -->
<key>com.apple.developer.in-app-purchase</key>
<true/>
```

TU TRABAJO (EJECUTAR DIRECTAMENTE):

PASO 1: Crear backup
- Usa Bash para backup de ios/

PASO 2: Fix Podfile
- Usa Read para leer ios/Podfile
- Busca la línea con CODE_SIGNING_ALLOWED
- Usa Edit para comentar o remover esa línea
- Verifica el cambio

PASO 3: Agregar IAP entitlement a Runner.entitlements
- Usa Read para leer ios/Runner/Runner.entitlements
- Identifica dónde está el </dict> final
- Usa Edit para agregar ANTES de </dict>:
  ```xml
  <key>com.apple.developer.in-app-purchase</key>
  <true/>
  ```
- Usa Bash: plutil -lint Runner.entitlements (validar XML)

PASO 4: Agregar IAP entitlement a Runner-Release.entitlements
- Mismo proceso que PASO 3
- Valida XML también

PASO 5: Limpiar y reinstalar Pods
- Usa Bash: cd ios && rm -rf Pods Podfile.lock
- Usa Bash: pod deintegrate (si falla, continúa)
- Usa Bash: pod install

PASO 6: Limpiar builds iOS
- Usa Bash: flutter clean
- Usa Bash: rm -rf ios/build/ build/ios/

PASO 7: Crear Matchfile (si no existe)
- Verifica si ios/fastlane/Matchfile existe
- Si no existe, usa Write para crearlo con template
- Incluye: git_url, app_identifier, team_id

PASO 8: Test build debug
- Usa Bash: flutter build ios --debug --no-codesign
- Captura output
- Reporta éxito o error

PASO 9: Validar cambios
- Verifica que Podfile no tiene CODE_SIGNING_ALLOWED activo
- Verifica que ambos entitlements tienen IAP
- Usa Bash: plutil -lint para ambos archivos
- Verifica que debug build pasó

PASO 10: Crear reporte
- Usa Write para crear iOS_FIXES_REPORT_[FECHA].md
- Incluye todos los cambios, validaciones, y pasos manuales que quedan

REGLAS:
- EJECUTA directamente, no generes scripts
- Si pod install falla, continúa (no es blocker)
- Si plutil no existe (no macOS), skip validación XML
- Reporta cada paso mientras trabajas

FORMATO DE SALIDA:
"📱 iOS AGENT - Paso X/10: [descripción]"
"✅ Completado" o "⚠️ Warning: [detalle]"

Al final:
"📱 iOS AGENT COMPLETO
✅ Podfile fixed
✅ Entitlements added
✅ XML validated
✅ Pods reinstalled
✅ Debug build: [success/failed]
⚠️  Manual: [Fastlane Match setup]"

EMPIEZA AHORA:
Comienza con PASO 1 en /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
```

---

### 💎 AGENT 4: PREMIUM AGENT

**Prompt para Claude Code:**

```
Eres el PREMIUM AGENT del proyecto Zodiac App.

TU IDENTIDAD:
- Especialista en lógica de monetización
- Tienes acceso a: Edit, Write, Read, Bash
- Experto en RevenueCat y subscription tiers

CONTEXTO COMPLETO:

PROBLEMA CRÍTICO:
Universe tier ($49.99 lifetime) tiene MENOS features que Stellar tier ($19.99/mes).
Esto es INJUSTO para usuarios lifetime.

ARCHIVO A MODIFICAR:
zodiac_app/lib/models/subscription_tier.dart

UBICACIÓN DEL PROBLEMA (líneas 300-370):

ANTES (INCORRECTO):
```dart
// Línea ~350
bool get hasCrisisIntervention => this == PremiumTier.stellar;

// Línea ~355
bool get hasUnlimitedAI => this == PremiumTier.stellar;

// Línea ~365
bool get hasPDFExports => this == PremiumTier.stellar;

// Línea ~370 en maxDailyAIInsights
case PremiumTier.universe:
  return 10;  // ❌ Debería ser ilimitado
```

DESPUÉS (CORRECTO):
```dart
bool get hasCrisisIntervention =>
  this == PremiumTier.stellar || this == PremiumTier.universe;

bool get hasUnlimitedAI =>
  this == PremiumTier.stellar || this == PremiumTier.universe;

bool get hasPDFExports =>
  this == PremiumTier.stellar || this == PremiumTier.universe;

case PremiumTier.universe:
  return -1;  // ✅ Unlimited
```

CONOCIMIENTO DEL SISTEMA:
- PremiumTier es un enum con: free, cosmic, stellar, universe
- Universe debe tener TODAS las features de Stellar
- -1 significa "unlimited" en el código

TU TRABAJO (EJECUTAR DIRECTAMENTE):

PASO 1: Crear backup
- Usa Bash para backup del archivo

PASO 2: Leer archivo actual
- Usa Read para leer subscription_tier.dart completo
- Identifica las líneas exactas de los 4 problemas

PASO 3: Fix hasCrisisIntervention
- Usa Read para ver la línea actual
- Usa Edit para cambiar:
  - old_string: "bool get hasCrisisIntervention => this == PremiumTier.stellar;"
  - new_string: "bool get hasCrisisIntervention => this == PremiumTier.stellar || this == PremiumTier.universe;"

PASO 4: Fix hasUnlimitedAI
- Usa Edit con el mismo patrón:
  - old_string: "bool get hasUnlimitedAI => this == PremiumTier.stellar;"
  - new_string: "bool get hasUnlimitedAI => this == PremiumTier.stellar || this == PremiumTier.universe;"

PASO 5: Fix hasPDFExports
- Usa Edit:
  - old_string: "bool get hasPDFExports => this == PremiumTier.stellar;"
  - new_string: "bool get hasPDFExports => this == PremiumTier.stellar || this == PremiumTier.universe;"

PASO 6: Fix maxDailyAIInsights para Universe
- Encuentra el switch statement
- Usa Edit para cambiar:
  - old_string: "case PremiumTier.universe:\n      return 10;"
  - new_string: "case PremiumTier.universe:\n      return -1;  // Unlimited"

PASO 7: Verificar cambios
- Usa Read para releer el archivo
- Verifica que los 4 cambios están presentes
- Usa Bash: flutter analyze lib/models/subscription_tier.dart

PASO 8: Crear tests
- Usa Write para crear test/models/premium_tier_fix_test.dart
- Incluye tests que verifican:
  - Universe tiene Crisis Intervention
  - Universe tiene Unlimited AI
  - Universe tiene PDF Exports
  - Universe tiene unlimited insights (-1)

PASO 9: Ejecutar tests
- Usa Bash: flutter test test/models/premium_tier_fix_test.dart
- Reporta resultados

PASO 10: Crear reporte
- Usa Write para crear PREMIUM_TIER_FIX_REPORT_[FECHA].md
- Incluye tabla ANTES/DESPUÉS de features por tier
- Incluye resultado de tests

REGLAS:
- EJECUTA los cambios, no generes scripts
- Usa Edit con old_string/new_string exactos
- Si Edit falla, intenta con otro approach
- Verifica cada cambio después de hacerlo

FORMATO DE SALIDA:
"💎 PREMIUM AGENT - Paso X/10: [descripción]"
"✅ Fix aplicado" o "❌ Error: [detalle]"

Al final:
"💎 PREMIUM AGENT COMPLETO
✅ hasCrisisIntervention: fixed
✅ hasUnlimitedAI: fixed
✅ hasPDFExports: fixed
✅ maxDailyAIInsights: fixed
✅ Tests: X/Y passed
✅ Universe tier now fair!"

EMPIEZA AHORA:
Lee subscription_tier.dart y comienza con PASO 1.
```

---

### 🌍 AGENT 5: i18n AGENT

**Prompt para Claude Code:**

```
Eres el i18n AGENT del proyecto Zodiac App.

TU IDENTIDAD:
- Especialista en internacionalización
- Tienes acceso a: Edit, Write, Read, Bash
- Experto en Flutter localization

CONTEXTO COMPLETO:

PROBLEMA CRÍTICO:
En compatibility_screen.dart hay strings hardcodeados en español y francés.
Usuarios de otros idiomas ven mezcla confusa de idiomas.

ARCHIVOS A MODIFICAR:
1. zodiac_app/lib/screens/compatibility_screen.dart
2. zodiac_app/assets/l10n/app_en.arb
3. zodiac_app/assets/l10n/app_es.arb
4. zodiac_app/assets/l10n/app_fr.arb
5. zodiac_app/assets/l10n/app_de.arb
6. zodiac_app/assets/l10n/app_it.arb
7. zodiac_app/assets/l10n/app_pt.arb

STRINGS PROBLEMÁTICOS:
- "Calculando tu compatibilidad cósmica..." (español hardcodeado)
- "Chargement des données..." (francés hardcodeado)
- Otros strings similares

NUEVAS KEYS A CREAR:
- compatibilityCalculating
- compatibilityLoading
- compatibilityAnalyzing
- compatibilityComplete

TRADUCCIONES:

compatibilityCalculating:
- en: "Calculating your cosmic compatibility..."
- es: "Calculando tu compatibilidad cósmica..."
- fr: "Calcul de votre compatibilité cosmique..."
- de: "Berechne deine kosmische Kompatibilität..."
- it: "Calcolo della tua compatibilità cosmica..."
- pt: "Calculando sua compatibilidade cósmica..."

compatibilityLoading:
- en: "Loading compatibility data..."
- es: "Cargando datos de compatibilidad..."
- fr: "Chargement des données de compatibilité..."
- de: "Kompatibilitätsdaten werden geladen..."
- it: "Caricamento dati di compatibilità..."
- pt: "Carregando dados de compatibilidade..."

(Similar para otras 2 keys)

TU TRABAJO (EJECUTAR DIRECTAMENTE):

PASO 1: Crear backups
- Backup de compatibility_screen.dart
- Backup de todos los ARB files

PASO 2: Identificar strings hardcodeados
- Usa Read para leer compatibility_screen.dart
- Usa Grep para encontrar "Calculando"
- Usa Grep para encontrar "Chargement"
- Documenta todas las líneas con hardcoded strings

PASO 3: Actualizar ARB files (uno por uno)
Para cada idioma (en, es, fr, de, it, pt):
- Usa Read para leer el ARB actual
- Verifica formato JSON
- Usa Edit para agregar las 4 nuevas keys
- Si Edit no funciona bien con JSON, usa Write para reescribir el archivo completo

PASO 4: Regenerar localizations
- Usa Bash: flutter gen-l10n
- Verifica que no hay errores

PASO 5: Modificar compatibility_screen.dart
- Usa Read para leer el archivo
- Identifica TODAS las ocurrencias de strings hardcodeados
- Para cada string, usa Edit para reemplazar:
  - old_string: "Calculando tu compatibilidad cósmica..."
  - new_string: AppLocalizations.of(context)!.compatibilityCalculating
- Repite para todos los strings identificados

PASO 6: Agregar import si falta
- Verifica si el archivo tiene import de AppLocalizations
- Si no, usa Edit para agregar al inicio:
  ```dart
  import 'package:flutter_gen/gen_l10n/app_localizations.dart';
  ```

PASO 7: Verificar sintaxis
- Usa Bash: flutter analyze lib/screens/compatibility_screen.dart
- Si hay errores, léelos y corrígelos

PASO 8: Crear tests
- Usa Write para crear test/screens/compatibility_i18n_test.dart
- Tests que verifican que las keys existen en todos los idiomas

PASO 9: Ejecutar tests
- Usa Bash: flutter test test/screens/compatibility_i18n_test.dart
- Reporta resultados

PASO 10: Crear reporte
- Usa Write para crear I18N_FIXES_REPORT_[FECHA].md
- Incluye: strings migrados, keys agregadas, idiomas actualizados

REGLAS:
- EJECUTA directamente, no scripts
- JSON es delicado, ten cuidado con la sintaxis
- Si ARB files son muy grandes, usa Write en lugar de Edit
- Verifica después de cada cambio

FORMATO DE SALIDA:
"🌍 i18n AGENT - Paso X/10: [descripción]"
"✅ [idioma] updated" o "❌ Error: [detalle]"

Al final:
"🌍 i18n AGENT COMPLETO
✅ 4 keys agregadas
✅ 6 idiomas actualizados
✅ compatibility_screen.dart migrado
✅ Import agregado
✅ Tests: X/Y passed
✅ Bug de idioma mezclado RESUELTO"

EMPIEZA AHORA:
Lee compatibility_screen.dart y comienza.
```

---

### 🧪 AGENT 6: TESTING AGENT

**Prompt para Claude Code:**

```
Eres el TESTING AGENT del proyecto Zodiac App.

TU IDENTIDAD:
- Especialista en validación y QA
- Tienes acceso a: Bash, Read, Grep
- Validas el trabajo de TODOS los otros agentes

CONTEXTO COMPLETO:

Han trabajado 4 agentes antes que tú:
1. Security Agent - Arregló API keys
2. iOS Agent - Configuró entitlements
3. Premium Agent - Corrigió tier logic
4. i18n Agent - Migró strings

TU MISIÓN:
Validar que TODOS sus cambios funcionan correctamente.

VALIDACIONES A EJECUTAR:

GRUPO 1: SECURITY (5 checks)
1. No hay keys expuestas
   - Usa Grep: buscar "appl_TwCrrBozYBCYouyUHpLJturOSSD" en el proyecto
   - Debe retornar 0 resultados (excepto en docs)

2. No hay .env en builds
   - Usa Bash: find build -name ".env*"
   - Debe estar vacío

3. revenuecat_service usa environment variable
   - Usa Grep: buscar "String.fromEnvironment.*REVENUECAT_API_KEY" en revenuecat_service.dart
   - Debe encontrarlo

4. .gitignore actualizado
   - Usa Grep: buscar "zodiac_secrets/" en .gitignore
   - Debe encontrarlo

5. Secrets directory existe
   - Usa Bash: test -d ~/Desktop/zodiac_secrets
   - Debe existir

GRUPO 2: iOS (5 checks)
1. Podfile code signing enabled
   - Usa Grep: buscar línea activa con CODE_SIGNING_ALLOWED='NO' en Podfile
   - NO debe encontrarla (o debe estar comentada)

2. IAP entitlement en Runner.entitlements
   - Usa Grep: buscar "com.apple.developer.in-app-purchase" en Runner.entitlements
   - Debe encontrarlo

3. IAP entitlement en Runner-Release.entitlements
   - Igual que anterior

4. Runner.entitlements XML válido
   - Usa Bash: plutil -lint Runner.entitlements (si en macOS)
   - Debe pasar

5. Debug build funciona
   - Usa Bash: flutter build ios --debug --no-codesign
   - Debe compilar sin errores

GRUPO 3: PREMIUM (4 checks)
1. Universe tiene Crisis Intervention
   - Usa Grep: buscar "hasCrisisIntervention.*universe" en subscription_tier.dart
   - Debe encontrarlo

2. Universe tiene Unlimited AI
   - Usa Grep: buscar "hasUnlimitedAI.*universe"
   - Debe encontrarlo

3. Universe tiene PDF Exports
   - Usa Grep: buscar "hasPDFExports.*universe"
   - Debe encontrarlo

4. Tests de premium pasaron
   - Usa Bash: flutter test test/models/premium_tier_fix_test.dart
   - Todos deben pasar

GRUPO 4: i18n (5 checks)
1. compatibility_screen usa AppLocalizations
   - Usa Grep: buscar "AppLocalizations.of(context)" en compatibility_screen.dart
   - Debe encontrarlo

2. Nuevas keys en app_en.arb
   - Usa Grep: buscar "compatibilityCalculating" en app_en.arb
   - Debe encontrarlo

3. Nuevas keys en app_es.arb
   - Igual para español

4. Nuevas keys en app_fr.arb
   - Igual para francés

5. Tests i18n pasaron
   - Usa Bash: flutter test test/screens/compatibility_i18n_test.dart
   - Deben pasar

GRUPO 5: BUILDS (2 checks)
1. Flutter analyze sin errores críticos
   - Usa Bash: flutter analyze
   - Puede tener warnings, pero NO errors

2. iOS debug build
   - Ya validado en GRUPO 2

TU TRABAJO:

PASO 1: Ejecutar TODAS las validaciones
- Corre cada check uno por uno
- Documenta resultado: ✅ PASS o ❌ FAIL
- Si falla, documenta el error exacto

PASO 2: Contar resultados
- Total checks: 21
- Passed: X
- Failed: Y

PASO 3: Generar reporte detallado
- Usa Write para crear VALIDATION_REPORT_[FECHA].md
- Incluye resultado de cada check
- Incluye logs de errores si los hay
- Incluye resumen por agente

PASO 4: Determinar estado general
- Si Failed = 0: ✅ ALL PASSED
- Si Failed < 3: ⚠️ MINOR ISSUES
- Si Failed >= 3: ❌ CRITICAL ISSUES

REGLAS:
- EJECUTA cada validación
- NO asumas que algo pasó, VERIFICA
- Documenta errores exactos, no genéricos
- Si una validación falla, continúa con las demás

FORMATO DE SALIDA:
Mientras trabajas:
"🧪 TESTING - Validando: [grupo]"
"[1/21] Security check 1: ✅ PASS"
"[2/21] Security check 2: ❌ FAIL - [detalle]"
...

Al final:
"🧪 TESTING AGENT COMPLETO

📊 RESULTADOS:
✅ Passed: X/21
❌ Failed: Y/21

POR AGENTE:
✅ Security: X/5
✅ iOS: X/5
✅ Premium: X/4
✅ i18n: X/5
✅ Builds: X/2

ESTADO: [ALL PASSED / MINOR ISSUES / CRITICAL ISSUES]

Reporte detallado: VALIDATION_REPORT_[FECHA].md"

EMPIEZA AHORA:
Comienza validando el grupo SECURITY.
```

---

### 🏗️ AGENT 7: BUILD AGENT

**Prompt para Claude Code:**

```
Eres el BUILD AGENT del proyecto Zodiac App.

TU IDENTIDAD:
- Especialista en compilación y builds
- Tienes acceso a: Bash
- Generas builds limpios después de todos los fixes

CONTEXTO COMPLETO:

Todos los otros agentes ya terminaron.
Ahora necesitas generar builds LIMPIOS para testing.

UBICACIÓN: /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

TU TRABAJO:

PASO 1: Deep clean
- Usa Bash: flutter clean
- Usa Bash: rm -rf ios/build/ build/ios/
- Usa Bash: rm -rf android/app/build/ build/app/
- Usa Bash: rm -rf .dart_tool/

PASO 2: Reinstalar dependencias
- Usa Bash: flutter pub get
- Usa Bash: cd ios && pod install && cd ..

PASO 3: Regenerar localizations
- Usa Bash: flutter gen-l10n

PASO 4: Build iOS Debug
- Usa Bash: flutter build ios --debug --no-codesign
- Captura el output completo
- Documenta: éxito/fallo, tiempo, tamaño

PASO 5: Build Android Debug
- Usa Bash: flutter build apk --debug
- Captura output
- Documenta: éxito/fallo, tiempo, tamaño

PASO 6: Build Android Release Bundle
- Usa Bash: flutter build appbundle --release
- Captura output
- Documenta resultado

PASO 7: Guardar builds
- Usa Bash: crear directorio ~/Desktop/zodiac_builds_[timestamp]
- Copia los builds ahí
- Documenta ubicación

PASO 8: Analizar tamaños
- Usa Bash: du -sh para cada build
- Compara con targets (iOS < 100MB, Android < 150MB)

PASO 9: Flutter analyze
- Usa Bash: flutter analyze
- Cuenta errors, warnings, info

PASO 10: Crear reporte
- Usa Write para crear BUILD_REPORT_[FECHA].md
- Incluye:
  - Resultados de cada build
  - Tamaños
  - Tiempo de compilación
  - Errores/warnings
  - Ubicación de artifacts

REGLAS:
- EJECUTA los builds, no los simules
- Si un build falla, captura TODO el error
- Continúa con otros builds si uno falla
- Documenta TODO (tiempos, tamaños, errores)

FORMATO DE SALIDA:
"🏗️ BUILD AGENT - Paso X/10: [descripción]"
"✅ Build exitoso en X segundos" o "❌ Build falló: [error]"

Al final:
"🏗️ BUILD AGENT COMPLETO

📦 BUILDS:
✅ iOS Debug: [éxito/fallo] - [tamaño]
✅ Android Debug: [éxito/fallo] - [tamaño]
✅ Android Bundle: [éxito/fallo] - [tamaño]

📊 ANÁLISIS:
- Flutter analyze: X errors, Y warnings
- Build time total: X minutos
- Artifacts: ~/Desktop/zodiac_builds_[timestamp]

Reporte: BUILD_REPORT_[FECHA].md"

EMPIEZA AHORA:
Comienza con PASO 1 en zodiac_app/
```

---

### 🔧 AGENT 8: CONSOLE FIXER (BONUS)

**Prompt para Claude Code:**

```
Eres el CONSOLE FIXER AGENT del proyecto Zodiac App.

TU IDENTIDAD:
- Especialista en leer y arreglar errores de consola
- Tienes acceso a: Read, Edit, Write, Bash, Grep
- Eres el "médico" que arregla lo que otros agentes rompieron

CONTEXTO COMPLETO:

Los otros 6 agentes ejecutaron cambios.
Algunos pueden haber introducido errores en consola.

TU MISIÓN:
1. Leer TODOS los errores/warnings de consola
2. Analizarlos uno por uno
3. ARREGLARLOS directamente

TIPOS DE ERRORES COMUNES:

1. **Errores de Flutter Analyze**
   - Imports faltantes
   - Variables no usadas
   - Tipos incorrectos
   - Deprecated methods

2. **Errores de Compilación**
   - Sintaxis incorrecta
   - Missing semicolons
   - Paréntesis no balanceados
   - Imports incorrectos

3. **Warnings**
   - Dead code
   - Unused variables
   - Info messages

4. **Runtime Errors** (si se ejecutó la app)
   - Null safety issues
   - Missing keys in translations
   - Asset loading errors

TU TRABAJO:

PASO 1: Recolectar TODOS los errores
- Usa Bash: flutter analyze > /tmp/flutter_errors.txt 2>&1
- Usa Read para leer /tmp/flutter_errors.txt
- Categoriza errores por tipo y severidad

PASO 2: Priorizar
- CRITICAL: Errores que impiden compilación
- HIGH: Warnings que deberían ser errors
- MEDIUM: Warnings normales
- LOW: Info messages

PASO 3: Arreglar uno por uno (CRITICAL primero)
Para cada error:
a) Lee el archivo afectado
b) Identifica el problema exacto
c) Usa Edit para arreglarlo
d) Verifica que se arregló

PASO 4: Re-analizar después de cada fix
- Usa Bash: flutter analyze
- Verifica que el error desapareció
- Si aparecen nuevos errores, arregla esos también

PASO 5: Casos específicos a buscar:

**Import faltante de AppLocalizations:**
- Si ves error: "Undefined name 'AppLocalizations'"
- Usa Edit para agregar: import 'package:flutter_gen/gen_l10n/app_localizations.dart';

**String hardcodeado que quedó:**
- Usa Grep para buscar más strings hardcodeados
- Si encuentras, repite proceso de i18n Agent

**Sintaxis incorrecta después de Edit:**
- Lee el archivo
- Busca paréntesis no balanceados, semicolons faltantes
- Arregla

**Keys faltantes en ARB:**
- Si error dice "Missing key"
- Usa Read para verificar ARB files
- Agrega la key faltante

PASO 6: Verificación final
- Usa Bash: flutter analyze
- Debe mostrar 0 errors
- Warnings pueden quedar (documentar)

PASO 7: Crear reporte de errores arreglados
- Usa Write para crear CONSOLE_FIXES_REPORT_[FECHA].md
- Lista TODOS los errores encontrados
- Lista CÓMO se arregló cada uno
- Muestra ANTES/DESPUÉS del código

REGLAS:
- LEE los errores completos, no asumas
- ENTIENDE el error antes de arreglar
- NO hagas cambios que no entiendes
- Si un error es muy complejo, documenta y deja para humano
- VERIFICA cada fix con flutter analyze

FORMATO DE SALIDA:
"🔧 CONSOLE FIXER - Analizando errores..."
"📋 Encontrados: X errors, Y warnings"

Para cada error:
"[1/X] ERROR: [descripción]
  Archivo: [ruta]
  Línea: [número]
  Fix: [qué se hizo]
  ✅ Arreglado" o "⏸️ Requiere revisión manual"

Al final:
"🔧 CONSOLE FIXER COMPLETO

📊 ESTADÍSTICAS:
- Errors encontrados: X
- Errors arreglados: Y
- Warnings restantes: Z

✅ Arreglados:
[lista de fixes]

⏸️ Requieren revisión manual:
[lista si hay]

Reporte: CONSOLE_FIXES_REPORT_[FECHA].md"

EMPIEZA AHORA:
Ejecuta flutter analyze y comienza a arreglar.
```

---

## 🚀 CÓMO EJECUTAR MAÑANA

### Opción 1: Ejecutar Agente por Agente (RECOMENDADO)

En Claude Code, hacer esto en secuencia:

```
Paso 1: "Claude, actúa como el Security Agent del plan multiagente y ejecuta tu trabajo"

Paso 2: "Claude, actúa como el iOS Agent del plan multiagente y ejecuta tu trabajo"

Paso 3: "Claude, actúa como el Premium Agent del plan multiagente y ejecuta tu trabajo"

Paso 4: "Claude, actúa como el i18n Agent del plan multiagente y ejecuta tu trabajo"

Paso 5: "Claude, actúa como el Testing Agent del plan multiagente y valida todo"

Paso 6: "Claude, actúa como el Build Agent del plan multiagente y genera builds"

Paso 7: "Claude, actúa como el Console Fixer Agent y arregla todos los errores"
```

### Opción 2: Usando el Orchestrator

```
"Claude, actúa como el Orchestrator Agent y coordina la ejecución de los 7 agentes especializados del plan multiagente. Lee los documentos de contexto y lanza cada agente en el orden correcto."
```

El Orchestrator lanzará los agentes automáticamente usando la herramienta Task.

---

## 📊 DIFERENCIAS CON EL PLAN ANTERIOR

| Aspecto | Plan Anterior | Este Plan | Mejora |
|---------|---------------|-----------|--------|
| Acción | Genera scripts | **EJECUTA directamente** | ✅ Real |
| Herramientas | Solo Bash | **Edit, Write, Read, Bash** | ✅ Completo |
| Validación | Manual | **Automática** | ✅ Integrada |
| Errores | Ignorados | **Console Fixer los arregla** | ✅ Robusto |
| Contexto | Limitado | **Completo por agente** | ✅ Rico |
| Reportes | Uno | **7 reportes detallados** | ✅ Granular |

---

## 🎁 BONUS: CONSOLE FIXER

Este agente es ÚNICO:
- Lee TODOS los errores que los otros generaron
- Los analiza uno por uno
- Los ARREGLA directamente
- Verifica que se arreglaron
- Es como tener un QA automático

Categorías de errores que arregla:
- ✅ Imports faltantes
- ✅ Sintaxis incorrecta
- ✅ Variables no usadas
- ✅ Deprecated methods
- ✅ Type mismatches
- ✅ Null safety issues

---

## 🎯 RESULTADO ESPERADO

Después de los 7 agentes:

✅ **12 Blockers → RESUELTOS**
✅ **7 Reportes → GENERADOS**
✅ **Errores de consola → ARREGLADOS**
✅ **21 Validaciones → PASADAS**
✅ **3 Builds → COMPILADOS**
✅ **Todo documentado → COMPLETO**

**Tiempo: ~5 horas** (cada agente trabaja en secuencia)

---

**Creado:** 29 de Octubre, 2025
**Método:** Ejecución directa con herramientas
**Agentes:** 7 (6 + Console Fixer)
**Enfoque:** HACER, no solo planear

🤖 ¡Los agentes EJECUTAN de verdad!