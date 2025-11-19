# 🆔 PLAN MAESTRO: Sistema de Identidad de Usuario No Invasivo
## **ZODIAC LIFE COACH - ANONYMOUS-FIRST WITH OPTIONAL ACCOUNT**

**Versión:** 1.0  
**Fecha Inicio:** 2025-10-02  
**Prioridad:** 🔴 CRÍTICA (Bloqueante para Launch)  
**Tiempo Estimado:** 13.5 horas (3 fases)  
**Coordinación:** Orquestador Master → 4 Agentes Especializados  

---

## 🎯 OBJETIVO ESTRATÉGICO

Implementar un sistema de identidad de usuario **100% no invasivo** que permita:
1. ✅ Usar la app **SIN login** (experiencia anónima completa)
2. ✅ Compras premium funcionando **sin cuenta**
3. ✅ **Opción opcional** de crear cuenta (Sign in with Apple)
4. ✅ Migración suave de datos anónimos → autenticados
5. ✅ Sincronización multi-device para usuarios con cuenta

---

## 🚨 PROBLEMA CRÍTICO DETECTADO

### **Bug Actual en RevenueCat (BLOQUEANTE):**
```dart
// ❌ CÓDIGO PROBLEMÁTICO (revenuecat_service.dart línea 73-80)
Future<String> _getAppUserID() async {
  return 'user_${DateTime.now().millisecondsSinceEpoch}'; // ❌ GENERA ID NUEVO CADA VEZ
}
```

**Consecuencias:**
- 💥 Usuario pierde compras al cerrar/reabrir app
- 💥 Restore purchases NO funciona
- 💥 Cambio de dispositivo = pérdida de premium
- 💥 Potencial crisis de soporte y reembolsos

---

## 🏗️ ARQUITECTURA PROPUESTA

### **Sistema de 3 Capas:**

```
┌─────────────────────────────────────────────────────────┐
│  CAPA 1: UserIdentityService (NUEVO)                    │
│  ├─ Device ID persistente (UUID guardado localmente)    │
│  ├─ Detección de autenticación (anónimo vs autenticado) │
│  └─ UserID unificado para RevenueCat                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  CAPA 2: RevenueCat Integration (FIX CRÍTICO)           │
│  ├─ Usa UserIdentityService para obtener userID         │
│  ├─ Compras vinculadas a device ID persistente          │
│  └─ Migración de compras anónimas → autenticadas        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  CAPA 3: Optional Account System                        │
│  ├─ Sign in with Apple (1-tap, NO invasivo)             │
│  ├─ UI en Settings (opcional, NO obligatorio)           │
│  └─ Data Migration Service (automático)                 │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 ASIGNACIÓN DE AGENTES (TIER SYSTEM)

### **TIER 1 - ORQUESTADOR MASTER** 🧠
**Agente:** `orchestrator_master`  
**Modelo:** Claude 3.5 Opus  
**Rol:** Coordinación general y supervisión

**Responsabilidades:**
- ✅ Coordinar las 3 fases de implementación
- ✅ Validar integridad entre componentes
- ✅ Asegurar no-regresión de features existentes
- ✅ Aprobar cada fase antes de continuar
- ✅ Testing de integración final

---

### **TIER 2 - ESPECIALISTAS CORE** ⚡

#### **Agente 1: zodiac_flutter_expert**
**Modelo:** Claude 3.5 Opus  
**Fase:** 1, 2 y 3  
**Archivos Asignados:**
```
FASE 1 (CRÍTICO):
- lib/services/user_identity_service.dart (NUEVO - 150 líneas)
- lib/services/revenuecat_service.dart (FIX - modificar líneas 73-80)
- lib/services/preferences_service.dart (AGREGAR métodos)

FASE 2 (UI):
- lib/screens/settings_screen.dart (AGREGAR account section)
- lib/widgets/auth/account_benefits_sheet.dart (NUEVO)
- lib/widgets/auth/sign_in_with_apple_button.dart (NUEVO)

FASE 3 (MIGRACIÓN):
- lib/services/data_migration_service.dart (NUEVO - 200 líneas)
- lib/services/account_prompt_service.dart (NUEVO - opcional)
```

**Contexto Específico:**
- App usa Riverpod para state management
- RevenueCat ya configurado con API Key: `appl_TwCrrBozYBCYouyUHpLJturOSSD`
- PreferencesService usa SharedPreferences + SecureStorage
- UserAuthenticationService ya existe pero está sin implementar
- 3 tiers premium: Cosmic ($6.99), Stellar ($19.99), Universe ($49.99)

---

#### **Agente 2: zodiac_backend_expert**
**Modelo:** Claude 3.5 Opus  
**Fase:** 3 (opcional - si hay backend sync)  
**Archivos Asignados:**
```
OPCIONAL (si decides sincronizar a backend):
- Backend: Enhanced Zodiac Backend v2.0 (Node.js + PostgreSQL)
- Endpoint: POST /api/users/migrate (migración de datos)
- Endpoint: GET /api/users/{userId}/sync (sincronización)
```

**Contexto Específico:**
- Backend en Railway (Enhanced Zodiac Backend v2.0)
- PostgreSQL para persistencia
- Firebase ya configurado (zodi-a1658)
- API actual no tiene endpoints de usuario (hay que crearlos)

---

#### **Agente 3: zodiac_business_expert**
**Modelo:** Claude 3.5 Sonnet  
**Fase:** 2 y 3  
**Responsabilidades:**
```
FASE 2:
- Diseñar UX no invasivo para account creation
- Copywriting de benefits sheet (persuasivo pero no pushy)
- Estrategia de prompts sutiles

FASE 3:
- Analytics tracking (conversión anónimo → autenticado)
- Métricas de retención multi-device
- A/B testing de prompts
```

**Contexto Específico:**
- App tiene 95% de usuarios potenciales anónimos
- Objetivo: 20% conversión a cuenta en primer mes
- Momento clave: Después de compra premium
- Beneficio principal: Sincronización multi-device

---

### **TIER 3 - ESPECIALISTAS DOMINIO** 🛠️

#### **Agente 4: security_specialist**
**Modelo:** Claude 3.5 Sonnet  
**Fase:** 1 y 3  
**Responsabilidades:**
```
FASE 1:
- Validar seguridad de device ID persistente
- Revisar almacenamiento de UUID (SecureStorage)
- GDPR compliance para datos anónimos

FASE 3:
- Seguridad de migración de datos
- Validación de Sign in with Apple
- Privacy policy updates necesarios
```

---

#### **Agente 5: quality_assurance**
**Modelo:** Claude 3.5 Sonnet  
**Fase:** Post-implementación  
**Responsabilidades:**
```
TESTING CRÍTICO:
1. Compra premium como anónimo
2. Cierra y reabre app → Debe mantener premium ✅
3. Restore purchases → Debe funcionar ✅
4. Crear cuenta → Migración exitosa ✅
5. Cambio de dispositivo → Sincronización ✅
6. Reinstalar app → Recovery con Apple ID ✅
```

---

## 📅 CRONOGRAMA DETALLADO (3 FASES)

### **FASE 1: FUNDACIÓN CRÍTICA** 🚨
**Tiempo:** 4.5 horas  
**Prioridad:** BLOQUEANTE - Debe completarse antes de launch  
**Agentes:** `zodiac_flutter_expert` + `security_specialist`

#### **Tareas Específicas:**

**1.1 Crear UserIdentityService** (2 horas)
```dart
// Archivo: lib/services/user_identity_service.dart
// Agente: zodiac_flutter_expert
// Modelo: Opus

IMPLEMENTAR:
✅ Singleton pattern con BaseSingletonService
✅ getDeviceUserID() → UUID persistente en SecureStorage
✅ getRevenueCatUserID() → 'anon_{deviceId}' o userId real
✅ currentUserType → enum (anonymous | authenticated)
✅ migrateToAuthenticated() → transferencia de compras
✅ initialize() → setup inicial
✅ Logging con AppLogger
✅ Error handling robusto

VALIDAR:
- UUID se genera UNA sola vez
- UUID persiste entre sesiones
- UUID persiste entre reinicios
- Integration con UserAuthenticationService existente
```

**1.2 Fix RevenueCat userID** (30 minutos)
```dart
// Archivo: lib/services/revenuecat_service.dart
// Líneas a modificar: 73-80
// Agente: zodiac_flutter_expert

CAMBIO CRÍTICO:
❌ ANTES:
return 'user_${DateTime.now().millisecondsSinceEpoch}';

✅ DESPUÉS:
final identityService = UserIdentityService.instance;
await identityService.initialize();
return await identityService.getRevenueCatUserID();

VERIFICAR:
- UserID consistente entre llamadas
- Compras persisten después de reinicio
- Restore purchases funciona correctamente
```

**1.3 Actualizar PreferencesService** (1 hora)
```dart
// Archivo: lib/services/preferences_service.dart
// Agente: zodiac_flutter_expert

AGREGAR MÉTODOS:
✅ getDeviceId() → String? (obtener UUID guardado)
✅ setDeviceId(String uuid) → void (guardar UUID)
✅ getUserDataKey(String key) → String (prefijo con userId)
✅ migrateUserData(String fromUserId, String toUserId) → Future<void>

USAR SECURE STORAGE:
- UUID debe guardarse en SecureStorage (no SharedPreferences)
- Encriptación AES-256 automática
- Validar que persiste después de reinstalación
```

**1.4 Testing Crítico** (1 hora)
```dart
// Agente: quality_assurance
// Tests a crear:

test/services/user_identity_service_test.dart
test/services/revenuecat_integration_test.dart

ESCENARIOS CRÍTICOS:
✅ Test 1: Device ID se crea y persiste
✅ Test 2: RevenueCat userID consistente
✅ Test 3: Compra → cierra app → reabre → mantiene premium
✅ Test 4: Restore purchases funciona
✅ Test 5: Migration anónimo → autenticado
```

**Entregable Fase 1:**
- ✅ UserIdentityService funcional y testeado
- ✅ RevenueCat con userID persistente
- ✅ Compras funcionando sin perder datos
- ✅ Tests pasando (coverage >80%)
- ✅ Sin regresiones en features existentes

---

### **FASE 2: UI NO INVASIVO** 💎
**Tiempo:** 5 horas  
**Prioridad:** ALTA - Necesario para launch  
**Agentes:** `zodiac_flutter_expert` + `zodiac_business_expert`

#### **Tareas Específicas:**

**2.1 Account Section en Settings** (2 horas)
```dart
// Archivo: lib/screens/settings_screen.dart
// Agente: zodiac_flutter_expert + zodiac_business_expert

AGREGAR SECCIÓN (después de Premium):
┌─────────────────────────────────────────┐
│  👤 Account                             │
│  ┌───────────────────────────────────┐ │
│  │ ✨ Using as Guest                 │ │
│  │                                   │ │
│  │ Create an account to sync         │ │
│  │ across devices                    │ │
│  │                                   │ │
│  │ [See Account Benefits] ←────────┐ │ │
│  └───────────────────────────────────┘ │ │
└─────────────────────────────────────────┘

DISEÑO:
- NO invasivo (no bloquea nada)
- Sutil gradiente púrpura/azul
- Icono outline (no filled)
- Botón outline (no filled)
- Aparece DESPUÉS de secciones principales
```

**2.2 Account Benefits Sheet** (2 horas)
```dart
// Archivo: lib/widgets/auth/account_benefits_sheet.dart (NUEVO)
// Agente: zodiac_business_expert + zodiac_flutter_expert

MODAL BOTTOM SHEET:
┌─────────────────────────────────────────┐
│  ✨ Account Benefits                    │
├─────────────────────────────────────────┤
│  ☁️  Sync Across Devices               │
│      Access horoscopes on all devices   │
│                                         │
│  💾  Never Lose Your Data              │
│      Settings backed up safely          │
│                                         │
│  🛍️  Premium Transfers                 │
│      Keep subscription on new devices   │
│                                         │
│  ⚡  Future Features                   │
│      Friends compatibility and more     │
├─────────────────────────────────────────┤
│  [🍎 Sign in with Apple]               │
│  [G  Sign in with Google] (opcional)   │
│                                         │
│  [Maybe Later] ←────── NO pushy        │
└─────────────────────────────────────────┘

COPYWRITING (zodiac_business_expert):
- Enfocado en BENEFICIOS no en features
- Lenguaje positivo ("unlock" no "missing")
- Sin presión ("Maybe Later" prominente)
- Emojis para visualización rápida
```

**2.3 Sign in with Apple Integration** (1 hora)
```dart
// Archivo: lib/widgets/auth/sign_in_with_apple_button.dart (NUEVO)
// Agente: zodiac_flutter_expert

IMPLEMENTAR:
✅ sign_in_with_apple package
✅ Autenticación con Apple ID
✅ Obtener user ID, email, displayName
✅ Crear usuario en UserAuthenticationService
✅ Trigger automático de migración
✅ Loading states y error handling
✅ Localización en 6 idiomas

CONFIGURACIÓN NECESARIA:
- Agregar Sign in with Apple capability en Xcode
- Configurar en Apple Developer Console
- Service ID: com.zodiacapp.signin
```

**Entregable Fase 2:**
- ✅ Settings con sección Account (no invasivo)
- ✅ Benefits sheet persuasivo pero sutil
- ✅ Sign in with Apple funcional
- ✅ UX testeado con usuarios beta
- ✅ Copywriting en 6 idiomas

---

### **FASE 3: MIGRACIÓN Y PROMPTS** 🔄
**Tiempo:** 4 horas  
**Prioridad:** MEDIA - Post-launch mejorado  
**Agentes:** `zodiac_flutter_expert` + `zodiac_backend_expert`

#### **Tareas Específicas:**

**3.1 Data Migration Service** (2 horas)
```dart
// Archivo: lib/services/data_migration_service.dart (NUEVO)
// Agente: zodiac_flutter_expert

IMPLEMENTAR:
✅ migrateAnonymousToAuthenticated()
  ├─ Copiar preferences (zodiacSign, birthDate, favorites)
  ├─ Transferir compras RevenueCat (alias user)
  ├─ Sincronizar a Firebase (opcional)
  └─ Limpiar datos antiguos

✅ _migratePreferences()
  ├─ Leer datos con prefijo 'anon_{oldDeviceId}_*'
  ├─ Escribir con prefijo '{newUserId}_*'
  └─ Validar integridad

✅ _transferRevenueCatPurchases()
  ├─ Llamar RevenueCat.aliasUser(newUserId)
  └─ Verificar transferencia exitosa

✅ _syncToFirebase() (opcional)
  ├─ Subir datos a Firestore
  └─ Configurar listeners para sync

FLUJO:
Usuario anónimo → Presiona "Sign in with Apple"
  → Autenticación exitosa
  → Trigger automático de migración
  → Modal de éxito: "All your data synced! ✅"
  → Redirect a Settings
```

**3.2 Account Prompt Service** (1 hora - OPCIONAL)
```dart
// Archivo: lib/services/account_prompt_service.dart (NUEVO)
// Agente: zodiac_business_expert + zodiac_flutter_expert

PROMPTS SUTILES (NO INVASIVOS):
┌─────────────────────────────────────────┐
│  ☁️ Protect your data - Create free account │
│  [Learn More]  [Dismiss]                │
└─────────────────────────────────────────┘

REGLAS NO INVASIVAS:
❌ NUNCA en primer uso
❌ NUNCA más de 1 vez por semana
❌ NUNCA en modal bloqueante
✅ SOLO SnackBar en bottom
✅ SOLO si usuario muy activo (30+ opens)
✅ SOLO si usuario premium (proteger inversión)

MOMENTOS CLAVE:
1. Después de compra premium exitosa
2. Usuario usa app 30+ días como anónimo
3. Usuario tiene 5+ favoritos guardados
```

**3.3 Analytics y Métricas** (1 hora)
```dart
// Agente: zodiac_business_expert

EVENTOS A TRACKEAR:
✅ account_benefits_viewed
✅ sign_in_apple_initiated
✅ sign_in_apple_completed
✅ sign_in_apple_failed
✅ migration_started
✅ migration_completed
✅ migration_failed
✅ prompt_shown
✅ prompt_dismissed
✅ prompt_converted

MÉTRICAS OBJETIVO:
- Conversión anónimo → cuenta: >20% en mes 1
- Migración exitosa: >95%
- Usuarios multi-device activos: >30% con cuenta
- Retención 30 días: +15% usuarios con cuenta
```

**Entregable Fase 3:**
- ✅ Migración automática de datos
- ✅ Prompts sutiles implementados
- ✅ Analytics tracking completo
- ✅ Testing de migración (>95% success rate)
- ✅ Documentación de flujos

---

## 📁 ESTRUCTURA DE ARCHIVOS COMPLETA

```
lib/
├── services/
│   ├── user_identity_service.dart ✨ NUEVO - FASE 1
│   ├── data_migration_service.dart ✨ NUEVO - FASE 3
│   ├── account_prompt_service.dart ✨ NUEVO - FASE 3 (opcional)
│   ├── revenuecat_service.dart 🔧 MODIFICAR - FASE 1
│   └── preferences_service.dart 🔧 MODIFICAR - FASE 1
│
├── screens/
│   └── settings_screen.dart 🔧 MODIFICAR - FASE 2
│
├── widgets/
│   └── auth/
│       ├── account_benefits_sheet.dart ✨ NUEVO - FASE 2
│       ├── sign_in_with_apple_button.dart ✨ NUEVO - FASE 2
│       └── account_section_widget.dart ✨ NUEVO - FASE 2
│
├── models/
│   └── user_identity.dart ✨ NUEVO - FASE 1
│       ├── enum UserType { anonymous, authenticated }
│       └── class UserIdentity { ... }
│
└── providers/
    └── user_identity_provider.dart ✨ NUEVO - FASE 1
        └── Riverpod providers para estado de usuario

test/
├── services/
│   ├── user_identity_service_test.dart ✨ NUEVO
│   ├── data_migration_service_test.dart ✨ NUEVO
│   └── revenuecat_integration_test.dart ✨ NUEVO
│
└── integration_test/
    └── anonymous_to_authenticated_flow_test.dart ✨ NUEVO
```

---

## 🧪 PLAN DE TESTING EXHAUSTIVO

### **Tests Unitarios** (quality_assurance)
```dart
// Cobertura objetivo: >85%

test/services/user_identity_service_test.dart
  ✅ Test: Device ID se genera una sola vez
  ✅ Test: Device ID persiste entre reinicios
  ✅ Test: RevenueCat userID consistente
  ✅ Test: Detección correcta de tipo usuario
  ✅ Test: Migración cambia tipo de usuario

test/services/revenuecat_integration_test.dart
  ✅ Test: Compra como anónimo funciona
  ✅ Test: Compra persiste después de reinicio
  ✅ Test: Restore purchases recupera compras
  ✅ Test: Migración transfiere compras correctamente
```

### **Tests de Integración** (quality_assurance)
```dart
integration_test/anonymous_to_authenticated_flow_test.dart
  ✅ Escenario 1: Usuario nuevo anónimo
    1. Abre app → device ID creado
    2. Selecciona signo → guardado con device ID
    3. Compra premium → vinculado a device ID
    4. Cierra y reabre → premium persiste ✅
    
  ✅ Escenario 2: Crear cuenta después de compra
    1. Usuario anónimo con premium
    2. Settings → "See Account Benefits"
    3. "Sign in with Apple" → autenticación
    4. Migración automática → compra transferida ✅
    5. Premium activo con nuevo userID ✅
    
  ✅ Escenario 3: Cambio de dispositivo
    1. Device A: Usuario con cuenta y premium
    2. Device B: Instala app
    3. Device B: "Sign in with Apple"
    4. Device B: Datos sincronizados ✅
    5. Device B: Premium activo ✅
    
  ✅ Escenario 4: Reinstalar app
    1. Usuario anónimo con premium
    2. Desinstala app
    3. Reinstala app
    4. "Restore Purchases" → premium recuperado ✅
```

### **Tests Manuales** (Pre-Launch Checklist)
```
□ Compra en Sandbox → cierra app → reabre → premium activo
□ Restore purchases desde Settings → funciona
□ Sign in with Apple → datos migrados correctamente
□ Cambio de idioma → datos persisten
□ Modo avión → compras en cache funcionan
□ iPad + iPhone con misma cuenta → sincronización
□ TestFlight beta testers → feedback de UX
```

---

## 📊 MÉTRICAS DE ÉXITO

### **Métricas Técnicas:**
- ✅ 0 pérdidas de compras reportadas
- ✅ Restore purchases success rate >98%
- ✅ Migration success rate >95%
- ✅ Crash-free rate >99.5%
- ✅ Device ID persistence rate 100%

### **Métricas de Negocio:**
- 🎯 Conversión anónimo → cuenta: >20% mes 1
- 🎯 Usuarios multi-device: >30% con cuenta
- 🎯 Retención 30 días: +15% vs anónimos
- 🎯 Refunds relacionados a login: <1%
- 🎯 Support tickets sobre login: <5%

### **Métricas de UX:**
- ✅ Onboarding friction: 0% (no login obligatorio)
- ✅ Account creation time: <30 segundos
- ✅ User satisfaction: >4.5/5 stars
- ✅ Feature requests login: tracking

---

## 🚀 PROTOCOLO DE ACTIVACIÓN MULTI-AGENTE

### **Comando de Inicio (Orquestador Master):**
```bash
@orchestrator_master

ACTIVAR PLAN: USER_IDENTITY_SYSTEM_MASTER_PLAN

CONTEXTO CRÍTICO:
- App: Zodiac Life Coach (astrology + neural compatibility)
- Estado: 95% production ready, bloqueado por bug RevenueCat
- Bug: userID cambia cada reinicio → pérdida de compras
- Objetivo: Sistema de usuario no invasivo con migración suave
- Timeline: 13.5 horas (3 fases)
- Agentes: 5 especializados en paralelo

PRIORIDAD: 🔴 CRÍTICA (bloqueante para launch)

INICIAR FASE 1 con zodiac_flutter_expert
```

### **Checkpoint Points (Orquestador valida):**
```
Checkpoint 1 (Post-Fase 1):
✅ UserIdentityService implementado y testeado
✅ RevenueCat con userID persistente
✅ Tests pasando (coverage >80%)
✅ Sin regresiones
→ APROBAR FASE 2

Checkpoint 2 (Post-Fase 2):
✅ UI no invasivo implementado
✅ Sign in with Apple funcional
✅ UX validado con beta testers
✅ Localización en 6 idiomas
→ APROBAR FASE 3

Checkpoint 3 (Post-Fase 3):
✅ Migración de datos automática
✅ Tests de integración pasando
✅ Analytics tracking activo
✅ Documentación completa
→ APROBAR PARA PRODUCCIÓN
```

---

## 📚 DOCUMENTACIÓN ADICIONAL

### **Documentos a Crear:**
```
docs/
├── USER_IDENTITY_ARCHITECTURE.md
│   └─ Diagrama de arquitectura completo
│
├── MIGRATION_GUIDE.md
│   └─ Guía para usuarios (FAQ)
│
├── DEVELOPER_GUIDE_USER_IDENTITY.md
│   └─ Guía técnica para desarrolladores
│
└── ANALYTICS_TRACKING_SPEC.md
    └─ Especificación de eventos analytics
```

### **Updates a Privacy Policy:**
```
Agregar a Privacy Policy:
- Uso de device ID anónimo
- Sign in with Apple data handling
- Data migration cuando creas cuenta
- Multi-device sync con cuenta
```

---

## 🎯 SIGUIENTES PASOS INMEDIATOS

### **1. Activar Orquestador Master:**
```bash
Lee este plan completo y coordina agentes
```

### **2. Iniciar Fase 1 (CRÍTICO):**
```bash
@zodiac_flutter_expert - Implementar UserIdentityService
@security_specialist - Validar seguridad del sistema
```

### **3. Testing Continuo:**
```bash
@quality_assurance - Crear test suite completa
```

### **4. Documentación:**
```bash
@documentation_assistant - Crear guías técnicas
```

---

## ✅ CHECKLIST DE APROBACIÓN FINAL

Antes de deploy a producción:
```
□ UserIdentityService testeado exhaustivamente
□ RevenueCat userID persistente verificado
□ Compras funcionando sin pérdida de datos
□ Restore purchases funcional
□ Sign in with Apple configurado
□ Data migration testeada >100 veces
□ UI no invasivo validado por beta testers
□ Analytics tracking activo
□ Privacy policy actualizada
□ App Store screenshots con account feature
□ Support documentation lista
□ Rollback plan preparado
```

---

**🚀 SISTEMA LISTO PARA ACTIVACIÓN MULTI-AGENTE**

**Coordinador:** @orchestrator_master  
**Status:** ⏸️ ESPERANDO APROBACIÓN USUARIO  
**Siguiente Acción:** Confirmar inicio de FASE 1
