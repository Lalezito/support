# 🔴 FASE 1: iOS BLOQUEANTES - GUÍA COMPLETA
## Resolución de Bloqueadores Críticos para App Store

**Creado**: 13 de Octubre 2025
**Prioridad**: MÁXIMA - BLOQUEA deployment
**Tiempo estimado**: 45 minutos (MANUAL)
**Requiere**: Apple Developer Account Holder

---

## ⚠️ IMPORTANTE

Estos pasos **DEBEN** completarse antes de:
- TestFlight público
- App Store submission
- Producción builds

**NO SON AUTOMATIZABLES** - Requieren acceso manual al portal de Apple

---

## 📋 TAREA 0.1: iOS CODE SIGNING (30 minutos)

### Problema Identificado
```yaml
error: "Provisioning profile doesn't include entitlements"
archivo: ios/Runner/Runner.entitlements
capabilities_faltantes:
  - App Groups
  - Associated Domains

causa: El perfil de provisioning fue creado ANTES de agregar entitlements
impacto: BLOQUEA builds de producción para App Store
```

### Entitlements Actuales
**Archivo**: `ios/Runner/Runner.entitlements`
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<!-- App Groups para compartir datos entre widgets -->
	<key>com.apple.security.application-groups</key>
	<array>
		<string>group.com.zodiaclifecoach.app</string>
	</array>

	<!-- Associated Domains para deep links -->
	<key>com.apple.developer.associated-domains</key>
	<array>
		<string>applinks:zodiaclifecoach.app</string>
		<string>applinks:www.zodiaclifecoach.app</string>
	</array>

	<!-- Push Notifications -->
	<key>aps-environment</key>
	<string>production</string>
</dict>
</plist>
```

### Solución: Paso a Paso

#### PASO 1: Acceder al Portal de Apple Developer
1. Ir a https://developer.apple.com/account/
2. Iniciar sesión con Account Holder credentials
3. Ir a **Certificates, Identifiers & Profiles**

#### PASO 2: Editar App ID
1. Click en **Identifiers** (menú izquierdo)
2. Seleccionar tu App ID: `com.zodiaclifecoach.app`
   - Si no existe, crear uno nuevo con ese Bundle ID
3. Click en **Edit** o **Configure**

#### PASO 3: Activar Capabilities
Marcar las siguientes capabilities:

**✅ App Groups**
```
Nombre del grupo: group.com.zodiaclifecoach.app

Nota: Si el grupo no existe:
1. Ir a "App Groups" en el sidebar
2. Click en "+" para crear nuevo
3. Usar el ID: group.com.zodiaclifecoach.app
4. Description: "Zodiac Life Coach Data Sharing"
5. Save
6. Volver a Identifiers y seleccionarlo
```

**✅ Associated Domains**
```
Simplemente marcar el checkbox
No requiere configuración adicional aquí
(Los dominios se definen en el entitlements file)
```

**✅ Push Notifications** (probablemente ya está)
```
Verificar que está marcado
```

**✅ In-App Purchase** (probablemente ya está)
```
Verificar que está marcado
```

#### PASO 4: Guardar Cambios
1. Click en **Save** o **Continue**
2. Confirmar los cambios

#### PASO 5: Regenerar Provisioning Profile
1. Ir a **Profiles** (menú izquierdo)
2. Buscar tu perfil de distribución: `Zodiac App Store Distribution`
   - Tipo: "App Store"
   - App ID: com.zodiaclifecoach.app
3. Si existe:
   - Seleccionarlo
   - Click en **Edit**
   - Verificar que todas las capabilities están incluidas
   - Click en **Generate** o **Save**
4. Si NO existe:
   - Click en "+" para crear nuevo
   - Tipo: **App Store**
   - App ID: Seleccionar `com.zodiaclifecoach.app`
   - Certificado: Seleccionar tu Distribution Certificate
   - Nombre: `Zodiac App Store Distribution`
   - Click en **Generate**

#### PASO 6: Descargar Nuevo Perfil
1. Click en **Download**
2. Guardar el archivo `.mobileprovision`

#### PASO 7: Instalar Perfil en Xcode
Opción A - Automática (recomendada):
```bash
# Doble click en el archivo descargado
open ~/Downloads/Zodiac_App_Store_Distribution.mobileprovision
```

Opción B - Manual:
```bash
# Copiar a directorio de perfiles
cp ~/Downloads/Zodiac_App_Store_Distribution.mobileprovision \
   ~/Library/MobileDevice/Provisioning\ Profiles/
```

#### PASO 8: Verificar en Xcode
1. Abrir `ios/Runner.xcworkspace` en Xcode
2. Seleccionar target **Runner**
3. Ir a **Signing & Capabilities**
4. Verificar:
   - ✅ "Automatically manage signing" está DESACTIVADO (para App Store)
   - ✅ Provisioning Profile seleccionado: `Zodiac App Store Distribution`
   - ✅ No hay warnings de "Capabilities not included"

#### PASO 9: Limpiar y Rebuild
```bash
# En terminal
cd ios
rm -rf Pods Podfile.lock
pod install
cd ..

# Limpiar Xcode
rm -rf ~/Library/Developer/Xcode/DerivedData/*
```

### Verificación Final

#### Comando 1: Verificar Entitlements en Perfil
```bash
# Extraer entitlements del perfil instalado
security cms -D -i ~/Library/MobileDevice/Provisioning\ Profiles/*.mobileprovision \
  | grep -A 30 Entitlements
```

**Output esperado**:
```xml
<key>Entitlements</key>
<dict>
  <key>com.apple.security.application-groups</key>
  <array>
    <string>group.com.zodiaclifecoach.app</string>
  </array>
  <key>com.apple.developer.associated-domains</key>
  <array>
    <string>applinks:zodiaclifecoach.app</string>
  </array>
  <key>aps-environment</key>
  <string>production</string>
</dict>
```

#### Comando 2: Verificar Capabilities en App ID
```bash
# Listar capabilities del App ID (requiere fastlane o spaceship)
# O verificar manualmente en developer.apple.com
```

#### Comando 3: Test Build
```bash
# Desde Xcode, intentar Archive para App Store
# Product → Archive
# No debería haber errores de code signing
```

### Checklist de Completitud
```yaml
✅ App ID editado en developer.apple.com
✅ App Groups capability activada
✅ Associated Domains capability activada
✅ Provisioning profile regenerado
✅ Provisioning profile descargado
✅ Provisioning profile instalado en Mac
✅ Xcode usa el perfil correcto
✅ Xcode no muestra warnings de capabilities
✅ Build Archive exitoso
```

---

## 📋 TAREA 0.2: APP STORE CONTRACT (15 minutos)

### Problema Identificado
```yaml
error: "Paid Applications Schedule not accepted"
impacto: BLOQUEA submission y TestFlight público
causa: Contrato requerido para apps con In-App Purchases
requiere: Account Holder (no Admin ni Developer)
```

### ¿Por Qué es Necesario?
- **Zodiac App tiene In-App Purchases** (RevenueCat)
- Apple requiere que **Account Holder** acepte términos legales
- Sin esto:
  - ❌ No puedes publicar en App Store
  - ❌ No puedes usar TestFlight público
  - ❌ No puedes procesar pagos

### Solución: Paso a Paso

#### PASO 1: Verificar Rol
```yaml
requisito: SOLO Account Holder puede hacer esto
no_funciona_con:
  - Admin
  - App Manager
  - Developer

verificar_rol:
  1. Ir a App Store Connect
  2. Click en tu nombre (arriba derecha)
  3. Ver "Role" en la página de perfil
  4. Debe decir "Account Holder"
```

#### PASO 2: Acceder a App Store Connect
1. Ir a https://appstoreconnect.apple.com/
2. Iniciar sesión con Account Holder credentials

#### PASO 3: Navegar a Agreements
1. En el home de App Store Connect
2. Click en **Agreements, Tax, and Banking** (menú principal)
   - Puede estar en la página inicial
   - O en el menú de tres puntos (⋯)

#### PASO 4: Aceptar Paid Applications Schedule
1. Buscar sección **Agreements**
2. Encontrar **"Paid Applications Schedule"**
   - Estado actual: "Action Required" o "Not Accepted"
3. Click en **Review Agreement**
4. Leer términos y condiciones
5. Click en **Agree** o **Accept**

#### PASO 5: Completar Información Requerida

**Si pide información bancaria**:
```yaml
sección: "Banking Information"
requerido:
  - Nombre del banco
  - Número de cuenta (para recibir pagos de Apple)
  - Routing number (si USA) o SWIFT/IBAN (internacional)
  - Nombre del titular

nota: Esta info es para que Apple te pague las ventas
```

**Si pide información fiscal**:
```yaml
sección: "Tax Information"
requerido:
  - Tax ID (RFC en México, EIN/SSN en USA, etc.)
  - Dirección fiscal
  - Nombre legal de la entidad
  - Formularios W-8/W-9 (si aplica)

nota: Apple requiere esto para cumplir con leyes fiscales
```

#### PASO 6: Verificar Contactos
```yaml
sección: "Contact Information"
verificar:
  - Senior Management contact
  - Finance contact
  - Technical contact
  - Marketing contact

acción: Actualizar si es necesario
```

#### PASO 7: Confirmar Aceptación
1. Después de completar todo
2. Verificar que el estado cambió a **"Active"** o **"Accepted"**
3. Puede tomar 5-10 minutos en actualizarse

### Verificación Final

#### Check 1: Estado del Contrato
```yaml
ir_a: App Store Connect > Agreements, Tax, and Banking
verificar:
  - Paid Applications Schedule: ✅ Active
  - Banking: ✅ Completed
  - Tax: ✅ Completed
  - Contact Info: ✅ Updated
```

#### Check 2: App Capabilities
```yaml
ir_a: App Store Connect > My Apps > Zodiac Life Coach
verificar:
  - In-App Purchases: ✅ Enabled
  - TestFlight: ✅ Available
  - Submit for Review: ✅ Unlocked (ya no bloqueado)
```

### Checklist de Completitud
```yaml
✅ Account Holder identificado
✅ Acceso a App Store Connect verificado
✅ Paid Applications Schedule aceptado
✅ Información bancaria completada
✅ Información fiscal completada
✅ Contactos actualizados
✅ Estado "Active" verificado
✅ TestFlight desbloqueado
✅ Submit for Review desbloqueado
```

---

## 🔄 PRÓXIMOS PASOS

Una vez completadas ambas tareas:

### Inmediato
1. ✅ Intentar Archive desde Xcode
2. ✅ Subir build a App Store Connect
3. ✅ Configurar TestFlight
4. ✅ Invitar beta testers

### Validación Técnica
```bash
# Test build de producción
cd ios
xcodebuild -workspace Runner.xcworkspace \
           -scheme Runner \
           -configuration Release \
           -archivePath build/Runner.xcarchive \
           archive

# Verificar que no hay errores de code signing
```

### Documentación
- Tomar screenshots de:
  - App ID con capabilities activadas
  - Provisioning profile regenerado
  - Paid Applications Schedule aceptado
- Guardar en: `.claude/06_DEPLOYMENT/iOS_SETUP_SCREENSHOTS/`

---

## 📝 NOTAS IMPORTANTES

### Errores Comunes

#### Error 1: "Profile doesn't match entitlements"
```yaml
causa: Perfil viejo sin capabilities
solución: Regenerar perfil (PASO 5 arriba)
```

#### Error 2: "No profile found"
```yaml
causa: Perfil no instalado en Mac
solución: Descargar e instalar perfil (PASO 6-7 arriba)
```

#### Error 3: "Contract not accepted"
```yaml
causa: Account Holder no ha aceptado términos
solución: Solo Account Holder puede aceptar (TAREA 0.2)
```

#### Error 4: "Banking information required"
```yaml
causa: Apple necesita info bancaria para pagos
solución: Completar en App Store Connect (PASO 5)
```

### Si Algo Falla

#### Rollback de Entitlements
```bash
# Si los entitlements causan problemas
cd ios/Runner
git checkout Runner.entitlements
```

#### Rollback de Provisioning Profile
```bash
# Eliminar perfil problemático
rm ~/Library/MobileDevice/Provisioning\ Profiles/*.mobileprovision

# Xcode descargará uno nuevo automáticamente
```

#### Contacto de Soporte
```yaml
apple_developer_support:
  web: https://developer.apple.com/contact/
  telefono: Disponible en portal
  temas:
    - Certificate/Profile issues
    - Account Holder changes
    - Contract acceptance problems
```

---

## 🎯 CRITERIO DE ÉXITO

### Tarea 0.1 Completada Cuando:
- ✅ App ID tiene App Groups y Associated Domains
- ✅ Provisioning profile regenerado e instalado
- ✅ Xcode build Archive exitoso
- ✅ No hay warnings de capabilities

### Tarea 0.2 Completada Cuando:
- ✅ Paid Applications Schedule: Active
- ✅ Banking information: Completed
- ✅ Tax information: Completed
- ✅ TestFlight disponible
- ✅ Submit for Review desbloqueado

### Ambas Tareas Completas:
```yaml
resultado: App lista para TestFlight y App Store
siguiente_fase: FASE 2 - Ejecución paralela de mejoras
desbloquea:
  - TestFlight público
  - App Store submission
  - Production builds
  - In-App Purchases en producción
```

---

## 📊 TIEMPO INVERTIDO

```yaml
tarea_0.1_code_signing:
  estimado: 30 minutos
  real: [PENDIENTE]

tarea_0.2_app_store_contract:
  estimado: 15 minutos
  real: [PENDIENTE]

total_fase_1:
  estimado: 45 minutos
  real: [PENDIENTE]
```

---

## ✅ CHECKLIST FINAL

Antes de marcar FASE 1 como completada:

```yaml
✅ TAREA 0.1: iOS Code Signing
  ✅ App ID editado con capabilities
  ✅ Provisioning profile regenerado
  ✅ Provisioning profile instalado
  ✅ Xcode build Archive exitoso

✅ TAREA 0.2: App Store Contract
  ✅ Paid Applications Schedule aceptado
  ✅ Banking information completada
  ✅ Tax information completada
  ✅ TestFlight desbloqueado

✅ VALIDACIÓN FINAL
  ✅ Screenshot de App ID guardado
  ✅ Screenshot de Contract guardado
  ✅ Build de prueba exitoso
  ✅ Documentación actualizada
```

---

**Creado por**: iOS Deployment Specialist (Master Orchestrator)
**Fecha**: 13 de Octubre, 2025
**Versión**: 1.0
**Estado**: 📋 LISTO PARA EJECUCIÓN MANUAL

⚠️ **REQUIERE ACCIÓN HUMANA - NO AUTOMATIZABLE** ⚠️

🎯 **Una vez completado, continuar con FASE 2** 🚀