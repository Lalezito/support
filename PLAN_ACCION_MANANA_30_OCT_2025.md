# PLAN DE ACCIÓN PARA MAÑANA - 30 OCTUBRE 2025
## Resolución de Blockers Críticos - Día 1

**Objetivo del Día:** Resolver los 12 blockers críticos identificados por los agentes
**Tiempo Estimado Total:** 8-10 horas de trabajo enfocado
**Prioridad:** MÁXIMA - Sin estos fixes no se puede lanzar

---

## 🌅 SESIÓN MATUTINA (8:00 AM - 12:00 PM) - 4 horas

### 🔴 BLOQUE 1: SEGURIDAD CRÍTICA (8:00 - 10:00 AM) - 2 horas

#### ✅ TAREA 1.1: Rotar y Asegurar API Keys (60 min)
**Prioridad:** CRÍTICA
**Archivos afectados:**
- `.env.production` (línea 119)
- `zodiac_app/lib/services/revenuecat_service.dart` (líneas 13-16)

**Pasos a ejecutar:**

```bash
# 1. Backup del estado actual (5 min)
cd /Users/alejandrocaceres/Desktop/appstore.zodia
git checkout -b hotfix/secure-api-keys
git add -A
git commit -m "Backup before API key rotation"

# 2. Generar nueva RevenueCat API key (10 min)
# MANUAL: Ir a https://app.revenuecat.com/
# - Login con tu cuenta
# - Projects > Zodiac App > API Keys
# - Generate new iOS API Key
# - Copiar la nueva key
# - GUARDAR EN LUGAR SEGURO (1Password/LastPass)
# - Invalidar la key antigua DESPUÉS de actualizar

# 3. Crear .env.production.secure FUERA del repositorio (15 min)
cd ~/Desktop
mkdir -p zodiac_secrets
cat > zodiac_secrets/.env.production.secure << 'EOF'
# Production Environment Variables - NUNCA COMMITEAR
REVENUECAT_IOS_API_KEY=appl_NUEVA_KEY_AQUI
REVENUECAT_ANDROID_API_KEY=goog_NUEVA_KEY_AQUI

# Firebase
FIREBASE_IOS_API_KEY=TU_KEY_AQUI
FIREBASE_ANDROID_API_KEY=TU_KEY_AQUI

# App Store Connect API
APPLE_ID=tu_email@example.com
APP_STORE_CONNECT_API_KEY_ID=TU_KEY_ID
APP_STORE_CONNECT_API_ISSUER_ID=TU_ISSUER_ID
APP_STORE_CONNECT_API_KEY_BASE64=TU_KEY_BASE64

# Backend
BACKEND_URL=https://zodiac-backend-api-production-8ded.up.railway.app
EOF

# 4. Remover keys hardcodeadas del código (20 min)
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Editar revenuecat_service.dart para usar dart-define
# El código actual tiene esto en línea 13-16:
# static const String _revenueCatAPIKey = 'appl_TwCrrBozYBCYouyUHpLJturOSSD';
#
# Necesitamos cambiarlo por:
# static const String _revenueCatAPIKey = String.fromEnvironment(
#   'REVENUECAT_API_KEY',
#   defaultValue: '', // Sin default en producción
# );

# 5. Configurar GitHub Secrets (10 min)
# MANUAL: Ir a GitHub repo > Settings > Secrets and variables > Actions
# Agregar estos secrets:
# - REVENUECAT_IOS_API_KEY
# - REVENUECAT_ANDROID_API_KEY
# - APP_STORE_CONNECT_API_KEY_ID
# - APP_STORE_CONNECT_API_ISSUER_ID
# - APP_STORE_CONNECT_API_KEY_BASE64
```

**Checklist:**
- [ ] Nueva RevenueCat key generada y guardada en secretos
- [ ] .env.production.secure creado FUERA del repo
- [ ] Keys removidas del código fuente
- [ ] GitHub Secrets configurados
- [ ] Key antigua invalidada en RevenueCat dashboard

**Verificación:**
```bash
# Verificar que no hay keys expuestas
cd /Users/alejandrocacares/Desktop/appstore.zodia
grep -r "appl_TwCrrBozYBCYouyUHpLJturOSSD" . --exclude-dir=.git --exclude-dir=build
# Resultado esperado: No matches (o solo en este documento de plan)

# Verificar que .env no está en builds
find build -name ".env" 2>/dev/null
# Resultado esperado: Vacío
```

---

#### ✅ TAREA 1.2: Limpiar .env de Build Artifacts (30 min)

```bash
# 1. Limpiar builds actuales (5 min)
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
flutter clean
find build -name ".env" -delete 2>/dev/null
find build -name "*.env*" -delete 2>/dev/null

# 2. Actualizar .gitignore (5 min)
cat >> .gitignore << 'EOF'

# Environment files in builds
build/**/.env
build/**/.env.*
**/.env.local
**/.env.*.local

# Secrets directory
zodiac_secrets/
EOF

# 3. Verificar archivos trackeados (5 min)
git status
# Asegurar que ningún .env está staged

# 4. Remover del historio si existe (15 min - OPCIONAL pero recomendado)
# PRECAUCIÓN: Esto reescribe el historial
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env.production' \
  --prune-empty --tag-name-filter cat -- --all

# 5. Forzar push (si hiciste filter-branch)
# git push origin --force --all
# git push origin --force --tags
```

**Checklist:**
- [ ] Builds limpios sin .env
- [ ] .gitignore actualizado
- [ ] Git status limpio
- [ ] Historial limpio (opcional)

---

#### ✅ TAREA 1.3: Fix Código de Firma iOS (30 min)

```bash
# 1. Editar Podfile (10 min)
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/ios

# Abrir Podfile y buscar línea ~100
# Comentar o remover esta línea:
# CODE_SIGNING_ALLOWED = 'NO'

# Debería quedar:
# # CODE_SIGNING_ALLOWED = 'NO'  # Removido para permitir release signing

# 2. Limpiar pods (5 min)
rm -rf Pods/
rm Podfile.lock
pod deintegrate
pod install

# 3. Limpiar build de iOS (5 min)
cd ..
flutter clean
rm -rf ios/build/
rm -rf build/ios/

# 4. Testear que compile (10 min)
flutter build ios --debug --no-codesign
# Debe compilar sin errores
```

**Checklist:**
- [ ] CODE_SIGNING_ALLOWED removido del Podfile
- [ ] Pods reinstalados
- [ ] Build debug exitoso

---

### 🟡 BLOQUE 2: PREMIUM FEATURES CRÍTICOS (10:00 AM - 12:00 PM) - 2 horas

#### ✅ TAREA 2.1: Agregar In-App Purchase Entitlements (30 min)

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/ios/Runner

# 1. Backup de entitlements actuales (5 min)
cp Runner.entitlements Runner.entitlements.backup
cp Runner-Release.entitlements Runner-Release.entitlements.backup

# 2. Agregar entitlement a Runner.entitlements (10 min)
# Editar Runner.entitlements
# Agregar antes del </dict> final:

# <key>com.apple.developer.in-app-purchase</key>
# <true/>

# 3. Agregar a Runner-Release.entitlements (10 min)
# Mismo contenido que arriba

# 4. Verificar formato XML (5 min)
plutil -lint Runner.entitlements
plutil -lint Runner-Release.entitlements
# Ambos deben decir: "OK"
```

**Archivos a editar:**

**`ios/Runner/Runner.entitlements`** - Agregar:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<!-- Contenido existente -->

	<!-- AGREGAR ESTO: -->
	<key>com.apple.developer.in-app-purchase</key>
	<true/>
</dict>
</plist>
```

**`ios/Runner/Runner-Release.entitlements`** - Agregar lo mismo

**Checklist:**
- [ ] Entitlement agregado a Runner.entitlements
- [ ] Entitlement agregado a Runner-Release.entitlements
- [ ] XML válido (plutil -lint OK)
- [ ] Backup guardado

---

#### ✅ TAREA 2.2: Fix Bug de Idioma Mezclado (60 min)

**Archivo:** `zodiac_app/lib/screens/compatibility_screen.dart`

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# 1. Identificar todos los hardcoded strings (15 min)
grep -n "Calculando\|Chargement\|Loading" lib/screens/compatibility_screen.dart

# 2. Crear backup (5 min)
cp lib/screens/compatibility_screen.dart lib/screens/compatibility_screen.dart.backup

# 3. Agregar keys faltantes a ARB files (20 min)
# Necesitaremos agregar algo como:

# En assets/l10n/app_en.arb:
# "compatibilityCalculating": "Calculating your cosmic compatibility...",
# "compatibilityLoading": "Loading compatibility data...",

# En assets/l10n/app_es.arb:
# "compatibilityCalculating": "Calculando tu compatibilidad cósmica...",
# "compatibilityLoading": "Cargando datos de compatibilidad...",

# En assets/l10n/app_fr.arb:
# "compatibilityCalculating": "Calcul de votre compatibilité cosmique...",
# "compatibilityLoading": "Chargement des données de compatibilité...",

# 4. Actualizar el código para usar AppLocalizations (15 min)
# Cambiar:
# "Calculando tu compatibilidad cósmica..."
# Por:
# AppLocalizations.of(context)!.compatibilityCalculating

# 5. Regenerar localization (5 min)
flutter gen-l10n

# 6. Testear (hot reload y verificar)
flutter run --debug
```

**Checklist:**
- [ ] Strings hardcodeados identificados
- [ ] Keys agregadas a los 6 ARB files (en, es, fr, de, it, pt)
- [ ] Código actualizado para usar AppLocalizations
- [ ] Localizations regeneradas
- [ ] Testeado en español, inglés y francés

---

#### ✅ TAREA 2.3: Decisión sobre Universe Tier (30 min)

**Decisión Requerida:** ¿Qué hacer con el tier Universe?

**Situación actual:**
- Universe tier: $49.99 lifetime
- Tiene MENOS features que Stellar ($19.99/mes)
- Crisis AI: NO incluido en Universe
- PDF exports: NO incluido en Universe
- AI insights: 10/día (Universe) vs ilimitado (Stellar)

**Opciones:**

**Opción A: Dar todas las features de Stellar a Universe** ✅ RECOMENDADO
- Tiempo: 30 min de código
- Beneficio: Usuarios lifetime felices
- Riesgo: Bajo

**Opción B: Subir precio de Universe a $99.99**
- Tiempo: 5 min de config
- Beneficio: Más ingresos potenciales
- Riesgo: Menos conversiones

**Opción C: Mantener como está pero documentar claramente**
- Tiempo: 15 min de docs
- Beneficio: Ninguno
- Riesgo: Alto (usuarios molestos)

**Plan si eliges Opción A (recomendado):**

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Archivo a editar: lib/models/subscription_tier.dart

# Cambios necesarios en líneas 300-370:

# ANTES:
# bool get hasCrisisIntervention => this == PremiumTier.stellar;
# bool get hasUnlimitedAI => this == PremiumTier.stellar;
# bool get hasPDFExports => this == PremiumTier.stellar;

# DESPUÉS:
# bool get hasCrisisIntervention =>
#   this == PremiumTier.stellar || this == PremiumTier.universe;
# bool get hasUnlimitedAI =>
#   this == PremiumTier.stellar || this == PremiumTier.universe;
# bool get hasPDFExports =>
#   this == PremiumTier.stellar || this == PremiumTier.universe;

# También en maxDailyAIInsights:
# ANTES:
# case PremiumTier.universe:
#   return 10;

# DESPUÉS:
# case PremiumTier.universe:
#   return -1; // Unlimited
```

**Checklist:**
- [ ] Decisión tomada sobre qué opción usar
- [ ] Si Opción A: Código actualizado
- [ ] Si Opción B: Precio actualizado en RevenueCat
- [ ] Si Opción C: Documentación clara creada
- [ ] Tests de premium features ejecutados
- [ ] Marketing materials actualizados (si aplica)

---

## 🌆 SESIÓN TARDE (2:00 PM - 6:00 PM) - 4 horas

### 🟢 BLOQUE 3: CERTIFICADOS Y ENVIRONMENT (2:00 - 4:00 PM) - 2 horas

#### ✅ TAREA 3.1: Configurar Fastlane Match (90 min)

**Prerequisitos:**
- Cuenta de Apple Developer activa
- Acceso a App Store Connect
- Git repository privado para certificates (o crear uno nuevo)

```bash
# 1. Instalar/actualizar Fastlane (10 min)
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/ios
gem install fastlane
fastlane update_fastlane

# 2. Inicializar Match (15 min)
fastlane match init

# Seleccionar: git (storage mode)
# Ingresar URL del repo privado para certs (crear uno si es necesario)
# Ejemplo: https://github.com/tu-usuario/zodiac-certificates.git (PRIVADO)

# 3. Configurar Matchfile (10 min)
# Se creará automáticamente, pero verificar que tenga:

cat > fastlane/Matchfile << 'EOF'
git_url("https://github.com/TU_USUARIO/zodiac-certificates.git")
storage_mode("git")
type("appstore")
app_identifier("com.zodiac.app.zodiacApp")
username("tu_email@example.com")
team_id("9DC6D95Z2P")
EOF

# 4. Generar certificados de desarrollo (20 min)
fastlane match development
# Ingresar passphrase cuando lo pida (GUARDAR EN SECRETOS)

# 5. Generar certificados de App Store (20 min)
fastlane match appstore
# Usar la misma passphrase

# 6. Configurar en GitHub Secrets (10 min)
# MANUAL: Agregar a GitHub Secrets:
# - MATCH_PASSWORD (la passphrase que usaste)
# - MATCH_GIT_URL (URL del repo de certificates)

# 7. Verificar que los certificados se instalaron (5 min)
security find-identity -v -p codesigning
# Deberías ver tus certificados listados

# 8. Testear build firmado (10 min)
fastlane build_release
# O manualmente:
# flutter build ios --release
```

**Checklist:**
- [ ] Fastlane actualizado
- [ ] Match inicializado
- [ ] Repo privado para certs creado
- [ ] Certificados de desarrollo generados
- [ ] Certificados de appstore generados
- [ ] MATCH_PASSWORD guardado en secretos
- [ ] GitHub Secrets configurados
- [ ] Build firmado exitoso

**Troubleshooting:**
Si tienes problemas con certificados existentes:
```bash
# Limpiar certificados viejos
fastlane match nuke development
fastlane match nuke distribution
# Luego regenerar
```

---

#### ✅ TAREA 3.2: Configurar App Store Connect API (30 min)

```bash
# 1. Generar API Key en App Store Connect (15 min)
# MANUAL:
# - Ir a https://appstoreconnect.apple.com/
# - Users and Access > Keys
# - Generate API Key
# - Nombre: "Zodiac CI/CD"
# - Access: App Manager
# - Download .p8 file (SOLO UNA VEZ)
# - Copiar Key ID (ej: ABC123DEF4)
# - Copiar Issuer ID (ej: 12345678-1234-1234-1234-123456789012)

# 2. Convertir .p8 a base64 (5 min)
cd ~/Downloads
base64 -i AuthKey_ABC123DEF4.p8 | pbcopy
# Ahora tienes el contenido en el clipboard

# 3. Guardar en secretos (5 min)
# Crear archivo temporal (NO commitear):
cd ~/Desktop/zodiac_secrets
cat > app_store_connect.txt << 'EOF'
KEY_ID=ABC123DEF4
ISSUER_ID=12345678-1234-1234-1234-123456789012
KEY_BASE64=<pegar aquí el contenido del clipboard>
EOF

# 4. Agregar a GitHub Secrets (5 min)
# MANUAL: GitHub > Settings > Secrets
# - APP_STORE_CONNECT_API_KEY_ID
# - APP_STORE_CONNECT_API_ISSUER_ID
# - APP_STORE_CONNECT_API_KEY_BASE64
```

**Checklist:**
- [ ] API Key generada en App Store Connect
- [ ] .p8 file descargado y guardado seguro
- [ ] Key convertida a base64
- [ ] Secrets guardados en archivo seguro
- [ ] GitHub Secrets configurados

---

### 🔵 BLOQUE 4: TESTING Y VALIDACIÓN (4:00 - 6:00 PM) - 2 horas

#### ✅ TAREA 4.1: Test de Compra en Dispositivo Físico (60 min)

**Prerequisitos:**
- iPhone físico conectado
- Sandbox test user configurado en App Store Connect

```bash
# 1. Configurar sandbox user (10 min)
# MANUAL:
# - App Store Connect > Users and Access > Sandbox Testers
# - Create new sandbox tester
# - Email: test+zodiac1@yourdomain.com
# - Password: GuardarEnSecretos123!
# - Región: tu país

# 2. Build para dispositivo físico (15 min)
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Desinstalar app actual del dispositivo
# iPhone: mantener app presionada > Remove App

# Build debug para testing
flutter clean
flutter build ios --debug
flutter install --debug

# O usando Xcode:
open ios/Runner.xcworkspace
# Seleccionar tu dispositivo > Run

# 3. Configurar sandbox en iPhone (5 min)
# En iPhone:
# - Settings > App Store > Sandbox Account
# - Sign in con el test user creado

# 4. Test de compra (20 min)
# En la app:
# 1. Ir a pantalla de premium
# 2. Seleccionar un tier (ej: Cosmic - $6.99)
# 3. Intentar comprar
# 4. Verificar que aparece el popup de Apple
# 5. Confirmar compra con sandbox account
# 6. Verificar que el tier se activa
# 7. Matar app y reabrir
# 8. Verificar que tier persiste

# 5. Test de restore purchases (10 min)
# En la app:
# 1. Desinstalar app
# 2. Reinstalar
# 3. Ir a premium
# 4. Tap "Restore Purchases"
# 5. Verificar que tier se restaura
```

**Checklist:**
- [ ] Sandbox user creado
- [ ] App instalada en dispositivo físico
- [ ] Sandbox account configurado en iPhone
- [ ] Compra de Cosmic tier exitosa
- [ ] Compra de Stellar tier exitosa
- [ ] Restore purchases funciona
- [ ] Tier persiste después de reiniciar app
- [ ] No hay crashes durante el flujo

**Log de pruebas a documentar:**
```
Test 1: Compra Cosmic tier
- Timestamp: [hora]
- Resultado: [éxito/fallo]
- Observaciones: [cualquier issue]

Test 2: Compra Stellar tier
- Timestamp: [hora]
- Resultado: [éxito/fallo]
- Observaciones: [cualquier issue]

Test 3: Restore purchases
- Timestamp: [hora]
- Resultado: [éxito/fallo]
- Observaciones: [cualquier issue]
```

---

#### ✅ TAREA 4.2: Validación de Environment Variables (30 min)

```bash
# 1. Crear script de validación (15 min)
cd /Users/alejandrocaceres/Desktop/appstore.zodia

cat > validate_env.sh << 'EOF'
#!/bin/bash

echo "🔍 Validando Environment Variables..."

# Función para verificar variable
check_var() {
  if [ -z "${!1}" ]; then
    echo "❌ Falta: $1"
    return 1
  else
    echo "✅ OK: $1"
    return 0
  fi
}

# Load .env si existe
if [ -f "~/Desktop/zodiac_secrets/.env.production.secure" ]; then
  source ~/Desktop/zodiac_secrets/.env.production.secure
fi

# Verificar variables críticas
errors=0

check_var "REVENUECAT_IOS_API_KEY" || ((errors++))
check_var "APPLE_ID" || ((errors++))
check_var "APP_STORE_CONNECT_API_KEY_ID" || ((errors++))
check_var "APP_STORE_CONNECT_API_ISSUER_ID" || ((errors++))
check_var "APP_STORE_CONNECT_API_KEY_BASE64" || ((errors++))
check_var "FIREBASE_IOS_API_KEY" || ((errors++))

echo ""
if [ $errors -eq 0 ]; then
  echo "✅ Todas las variables configuradas correctamente"
  exit 0
else
  echo "❌ Faltan $errors variables críticas"
  exit 1
fi
EOF

chmod +x validate_env.sh

# 2. Ejecutar validación (5 min)
./validate_env.sh

# 3. Verificar en GitHub Secrets (5 min)
# MANUAL: Verificar que todos los secrets estén en GitHub

# 4. Test build con dart-define (5 min)
cd zodiac_app
flutter build ios --release \
  --dart-define=REVENUECAT_API_KEY=$REVENUECAT_IOS_API_KEY \
  --dart-define=FIREBASE_API_KEY=$FIREBASE_IOS_API_KEY
```

**Checklist:**
- [ ] Script de validación creado
- [ ] Todas las variables verificadas
- [ ] GitHub Secrets completos
- [ ] Build con dart-define exitoso

---

#### ✅ TAREA 4.3: Build de Release Completo (30 min)

```bash
# 1. Build iOS Release (15 min)
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

flutter clean
flutter pub get

flutter build ios --release \
  --dart-define=REVENUECAT_API_KEY=$REVENUECAT_IOS_API_KEY

# Verificar que no hay errores

# 2. Build Android Release (15 min)
flutter build appbundle --release \
  --dart-define=REVENUECAT_API_KEY=$REVENUECAT_ANDROID_API_KEY

# Verificar que no hay errores

# 3. Verificar tamaños (5 min)
ls -lh build/ios/iphoneos/Runner.app
ls -lh build/app/outputs/bundle/release/app-release.aab

# 4. Guardar builds (5 min)
mkdir -p ~/Desktop/zodiac_builds_oct30
cp -r build/ios/iphoneos/Runner.app ~/Desktop/zodiac_builds_oct30/
cp build/app/outputs/bundle/release/app-release.aab ~/Desktop/zodiac_builds_oct30/
```

**Checklist:**
- [ ] iOS release build exitoso
- [ ] Android release bundle exitoso
- [ ] Tamaños razonables (iOS < 100MB, Android < 150MB)
- [ ] Builds guardados en carpeta segura
- [ ] No warnings críticos en console

---

## 📝 SESIÓN FINAL (6:00 - 7:00 PM) - 1 hora

### 🎯 BLOQUE 5: DOCUMENTACIÓN Y COMMIT (6:00 - 7:00 PM)

#### ✅ TAREA 5.1: Documentar Todo lo Realizado (30 min)

```bash
# 1. Crear reporte de progreso (20 min)
cd /Users/alejandrocaceres/Desktop/appstore.zodia

cat > PROGRESO_DIA1_30_OCT_2025.md << 'EOF'
# PROGRESO DÍA 1 - 30 OCTUBRE 2025
## Resolución de Blockers Críticos

### ✅ COMPLETADO

#### Seguridad
- [x] RevenueCat API keys rotadas
- [x] Keys removidas del código
- [x] .env.production.secure creado fuera del repo
- [x] GitHub Secrets configurados
- [x] Build artifacts limpiados
- [x] .gitignore actualizado

#### iOS
- [x] CODE_SIGNING_ALLOWED removido del Podfile
- [x] In-app purchase entitlements agregados
- [x] Fastlane Match configurado
- [x] Certificados generados
- [x] App Store Connect API configurada

#### Premium Features
- [x] Bug de idioma mezclado resuelto
- [x] Strings agregados a ARB files
- [x] Universe tier decisión tomada: [indicar opción elegida]
- [x] Código actualizado según decisión

#### Testing
- [x] Compra en dispositivo físico testeada
- [x] Sandbox user configurado
- [x] Restore purchases verificado
- [x] Environment variables validadas

#### Builds
- [x] iOS release build exitoso
- [x] Android release bundle exitoso
- [x] Builds guardados

### 📊 MÉTRICAS

- **Tiempo total invertido:** [X] horas
- **Blockers resueltos:** 12/12
- **Tests exitosos:** [X]/[Y]
- **Builds exitosos:** 2/2 (iOS + Android)

### 🐛 ISSUES ENCONTRADOS

[Documentar cualquier problema encontrado durante el día]

1. Issue 1: [descripción]
   - Solución aplicada: [solución]
   - Status: [resuelto/pendiente]

### 📋 PENDIENTE PARA MAÑANA

[Listar cualquier tarea que no se completó hoy]

1. [Tarea pendiente si existe]

### 🎯 PRÓXIMOS PASOS

- Mañana: Iniciar Fase 1 (Alta Prioridad)
  - Completar 163 keys de traducción faltantes
  - Comenzar testing de revenue features
  - Iniciar backend hardening

EOF

# 2. Actualizar el reporte con datos reales (10 min)
# Editar PROGRESO_DIA1_30_OCT_2025.md con los resultados reales
```

---

#### ✅ TAREA 5.2: Commit y Backup (20 min)

```bash
# 1. Verificar cambios (5 min)
cd /Users/alejandrocaceres/Desktop/appstore.zodia
git status
git diff

# 2. Commit de seguridad (5 min)
git add zodiac_app/ios/Runner/*.entitlements
git add zodiac_app/ios/Podfile
git add zodiac_app/lib/services/revenuecat_service.dart
git add zodiac_app/lib/models/subscription_tier.dart
git add zodiac_app/lib/screens/compatibility_screen.dart
git add zodiac_app/assets/l10n/*.arb
git add .gitignore
git add PROGRESO_DIA1_30_OCT_2025.md

git commit -m "fix: resolve critical blockers - day 1

- Secure API keys (moved to dart-define)
- Add in-app purchase entitlements
- Fix iOS code signing in Podfile
- Fix mixed language bug in compatibility screen
- Update Universe tier feature access
- Clean .env from build artifacts
- Configure Fastlane Match
- Setup App Store Connect API

Resolves: SEC-001, SEC-002, SEC-003, REV-001, REV-002, CODE-001, CODE-002

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 3. Push a rama de feature (5 min)
git push origin hotfix/secure-api-keys

# 4. Crear backup completo (5 min)
cd ~/Desktop
tar -czf zodiac_backup_oct30_$(date +%H%M).tar.gz \
  appstore.zodia/zodiac_app \
  zodiac_secrets \
  zodiac_builds_oct30

echo "✅ Backup creado: ~/Desktop/zodiac_backup_oct30_*.tar.gz"
```

**Checklist:**
- [ ] Reporte de progreso completado
- [ ] Todos los cambios commiteados
- [ ] Push exitoso
- [ ] Backup completo creado
- [ ] Secrets guardados en lugar seguro (no en repo)

---

#### ✅ TAREA 5.3: Preparar para Mañana (10 min)

```bash
# 1. Crear checklist para mañana (5 min)
cat > TODO_MANANA_31_OCT.md << 'EOF'
# TODO PARA MAÑANA - 31 OCTUBRE 2025
## Fase 1: Alta Prioridad - Día 2

### 🎯 Objetivos del Día
1. Completar traducciones faltantes
2. Iniciar testing de revenue features
3. Configurar Redis backend

### 📋 Tareas Priorizadas

#### Mañana (8:00 AM - 12:00 PM)
- [ ] Identificar las 163 keys faltantes exactas
- [ ] Traducir profesionalmente (o usar AI + review)
- [ ] Agregar a ARB files (de, fr, it, pt)
- [ ] Validar con script

#### Tarde (2:00 PM - 6:00 PM)
- [ ] Escribir tests para subscription_service.dart
- [ ] Escribir tests para notification_service.dart
- [ ] Configurar Redis en Railway
- [ ] Fix npm vulnerabilities backend

### 📦 Recursos Necesarios
- [ ] Acceso a traductor profesional o DeepL API
- [ ] Railway account para Redis
- [ ] Tiempo para testing

EOF

# 2. Verificar estado final (5 min)
flutter doctor -v
git status
echo "✅ Todo listo para mañana"
```

---

## 📊 RESUMEN EJECUTIVO DEL DÍA

### Tiempo Total Estimado: 10 horas

| Bloque | Tiempo | Tasks |
|--------|--------|-------|
| Seguridad Crítica | 2h | 3 tasks |
| Premium Features | 2h | 3 tasks |
| Certificados & Env | 2h | 2 tasks |
| Testing & Validación | 2h | 3 tasks |
| Documentación | 1h | 3 tasks |
| Buffer/Imprevistos | 1h | - |
| **TOTAL** | **10h** | **14 tasks** |

### 🎯 Objetivos del Día

**PRIMARIO (MUST):**
- ✅ Asegurar todas las API keys
- ✅ Configurar certificados iOS
- ✅ Agregar in-app purchase entitlements
- ✅ Fix bug crítico de idioma mezclado
- ✅ Resolver Universe tier logic

**SECUNDARIO (SHOULD):**
- ✅ Test de compra en dispositivo físico
- ✅ Builds de release exitosos
- ✅ Environment variables configuradas

**TERCIARIO (NICE TO HAVE):**
- ✅ Documentación completa
- ✅ Backup creado
- ✅ Plan para mañana

### 🚀 Resultado Esperado

Al final del día deberías tener:
1. ✅ 0 secrets expuestos en el repositorio
2. ✅ iOS capaz de hacer builds firmados
3. ✅ In-app purchases funcionando en sandbox
4. ✅ Bug crítico de UI resuelto
5. ✅ Lógica de premium tiers correcta
6. ✅ Environment de desarrollo seguro
7. ✅ Builds de release exitosos para iOS y Android

### 📈 Progreso Esperado en Blockers

- **Antes:** 12 blockers críticos
- **Después:** 0 blockers críticos ✅
- **Progreso:** 100% de blockers críticos resueltos

---

## ⚠️ NOTAS IMPORTANTES

### 🔐 Seguridad

1. **NUNCA commitear:**
   - .env.production.secure
   - Archivos .p8 de App Store Connect
   - Passphrases de Match
   - API keys en código

2. **SIEMPRE guardar en:**
   - 1Password / LastPass
   - GitHub Secrets (para CI/CD)
   - ~/Desktop/zodiac_secrets (local, fuera del repo)

3. **Verificar antes de push:**
   ```bash
   git diff --cached
   # Revisar que no hay secrets
   ```

### 🆘 Troubleshooting

**Si Fastlane Match falla:**
```bash
# Limpiar y reintentar
fastlane match nuke development
fastlane match nuke distribution
fastlane match development
fastlane match appstore
```

**Si la compra en sandbox falla:**
1. Verificar que sandbox user está signed in en iPhone
2. Verificar que el producto existe en App Store Connect
3. Verificar que el bundle ID coincide
4. Verificar logs en Xcode console
5. Revisar RevenueCat dashboard para ver el evento

**Si el build de iOS falla:**
```bash
# Limpiar todo y reintentar
cd ios
rm -rf Pods Podfile.lock
pod deintegrate
pod install
cd ..
flutter clean
flutter pub get
flutter build ios --debug
```

### 📞 Contactos de Emergencia

- **RevenueCat Support:** support@revenuecat.com
- **Apple Developer Support:** developer.apple.com/support
- **GitHub Support:** support.github.com

---

## ✅ CHECKLIST FINAL DEL DÍA

Al terminar el día, verificar:

### Seguridad
- [ ] Nueva RevenueCat key generada y guardada
- [ ] Keys antiguas invalidadas
- [ ] Código sin hardcoded secrets
- [ ] GitHub Secrets configurados
- [ ] .env files limpiados de builds
- [ ] Backup de secrets creado fuera del repo

### iOS
- [ ] Podfile sin CODE_SIGNING_ALLOWED
- [ ] Entitlements de IAP agregados
- [ ] Match configurado y funcionando
- [ ] Certificados generados
- [ ] App Store Connect API configurada
- [ ] Build de release exitoso

### Premium
- [ ] Bug de idioma mezclado resuelto
- [ ] Strings en ARB files
- [ ] Universe tier lógica corregida
- [ ] Compra testeada en dispositivo físico
- [ ] Restore purchases funciona

### Documentación
- [ ] Reporte de progreso completo
- [ ] Commit con mensaje detallado
- [ ] Push a feature branch
- [ ] Backup completo creado
- [ ] Plan para mañana preparado

### Builds
- [ ] iOS release build OK
- [ ] Android release bundle OK
- [ ] Builds guardados
- [ ] No warnings críticos

---

## 🎉 MOTIVACIÓN

¡Hoy es un día crucial! Vas a resolver TODOS los blockers críticos que impiden el lanzamiento.

**Después de hoy:**
- ✅ El código será seguro
- ✅ Las compras funcionarán
- ✅ Los builds estarán listos
- ✅ El camino a producción estará despejado

**Mantén el enfoque en:**
1. Seguridad primero
2. Revenue features segundo
3. Testing tercero

No te distraigas con issues menores. Hoy es solo blockers críticos.

---

## 📱 RECORDATORIOS DURANTE EL DÍA

### Cada 2 horas:
- [ ] Hacer commit de progreso
- [ ] Tomar break de 10 minutos
- [ ] Revisar que vas en tiempo

### Antes del almuerzo:
- [ ] Seguridad debe estar 100% completa
- [ ] Entitlements agregados
- [ ] Código sin secrets

### Antes de terminar:
- [ ] Todos los tests pasando
- [ ] Documentación completa
- [ ] Backup creado
- [ ] Git push exitoso

---

**Fecha de creación:** 29 de Octubre, 2025
**Para ejecutar:** 30 de Octubre, 2025
**Duración:** 1 día completo (10 horas)
**Resultado esperado:** 0 blockers críticos

---

¡Éxito! 🚀