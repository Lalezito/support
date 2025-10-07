# 🛡️ PROTOCOLO DE CUMPLIMIENTO OBLIGATORIO - ZODIAC 2025
## Sistema Manual de Enforcement para Refactoring Seguro

### 🚨 ADVERTENCIA CRÍTICA
**ESTE PROTOCOLO ES DE CUMPLIMIENTO OBLIGATORIO PARA TODOS LOS AGENTES**
**ENFORCEMENT MANUAL - CADA AGENTE ES RESPONSABLE DE SU CUMPLIMIENTO**

---

## 📋 CHECKLIST MANUAL OBLIGATORIO

### ✅ ANTES DE CUALQUIER MODIFICACIÓN:
- [ ] **BACKUP MANUAL**: Crear copia de seguridad: `cp -r zodiac_app zodiac_app_backup_$(date +%Y%m%d_%H%M%S)`
- [ ] **BRANCH MANUAL**: `git checkout -b refactor/[nombre-tarea]`
- [ ] **VERIFICACIÓN VISUAL**: Revisar lista de archivos prohibidos antes de editar
- [ ] **TESTS BASELINE MANUAL**: `flutter test` y documentar resultados
- [ ] **COMPILACIÓN BASELINE**: `flutter build apk --debug` y confirmar éxito

### ✅ DURANTE LA MODIFICACIÓN:
- [ ] **CAMBIOS INCREMENTALES**: Máximo 5 archivos por sesión
- [ ] **TEST MANUAL INMEDIATO**: Ejecutar `flutter test` después de cada cambio
- [ ] **COMPILACIÓN MANUAL**: Ejecutar `flutter analyze` después de cada modificación
- [ ] **VERIFICACIÓN FUNCIONAL**: Probar manualmente funciones modificadas
- [ ] **ROLLBACK MANUAL**: Si algo falla: `git checkout -- [archivo]` inmediatamente

### ✅ DESPUÉS DE CADA MODIFICACIÓN:
- [ ] **TESTS COMPLETOS MANUALES**: `flutter test --coverage`
- [ ] **ANÁLISIS MANUAL**: `flutter analyze` y verificar 0 errores nuevos
- [ ] **SMOKE TEST MANUAL**: `flutter run` y verificar que la app inicia
- [ ] **NAVEGACIÓN MANUAL**: Probar navegación básica entre pantallas
- [ ] **DOCUMENTACIÓN MANUAL**: Actualizar ADR con cambios realizados

---

## 🚫 ARCHIVOS ABSOLUTAMENTE PROHIBIDOS - VERIFICACIÓN MANUAL

### 🔴 ANTES DE EDITAR CUALQUIER ARCHIVO - VERIFICAR QUE NO ESTÉ EN ESTA LISTA:

#### NÚCLEO CRÍTICO (NUNCA TOCAR):
```
❌ lib/main.dart
❌ lib/firebase_options.dart  
❌ pubspec.yaml
❌ android/app/build.gradle
❌ ios/Runner/Info.plist
```

#### SERVICIOS DE PRODUCCIÓN (NUNCA TOCAR):
```
❌ lib/services/firebase_service.dart
❌ lib/services/revenue_cat_service.dart
❌ lib/services/preferences_service.dart
❌ lib/services/secure_storage_service.dart
❌ lib/services/production_analytics_service.dart
```

#### LOCALIZACIÓN (NUNCA TOCAR):
```
❌ lib/l10n/app_localizations.dart
❌ lib/l10n/app_localizations_es.dart
❌ lib/l10n/app_localizations_en.dart
❌ lib/l10n/app_localizations_de.dart
❌ lib/l10n/app_localizations_fr.dart
❌ lib/l10n/app_localizations_it.dart
❌ lib/l10n/app_localizations_pt.dart
```

#### PANTALLAS CORE DE USUARIO (NUNCA TOCAR):
```
❌ lib/screens/home_screen.dart
❌ lib/screens/language_selection_screen.dart
❌ lib/screens/sign_selection_screen.dart
❌ lib/screens/settings_screen.dart
❌ lib/screens/premium_screen.dart
```

---

## ⚡ COMANDOS MANUALES DE VERIFICACIÓN

### 🔍 EJECUTAR MANUALMENTE ANTES DE CADA COMMIT:

#### 1. Verificación de Análisis:
```bash
flutter analyze
# RESULTADO ESPERADO: "No issues found!"
# SI HAY ERRORES: NO CONTINUAR
```

#### 2. Verificación de Compilación:
```bash
flutter build apk --debug
# RESULTADO ESPERADO: "Built build/app/outputs/flutter-apk/app-debug.apk"
# SI FALLA: ROLLBACK INMEDIATO
```

#### 3. Verificación de Tests:
```bash
flutter test test/services/
flutter test test/widgets/
# RESULTADO ESPERADO: "All tests passed!"
# SI FALLAN: INVESTIGAR Y CORREGIR
```

#### 4. Verificación de Funcionalidad:
```bash
flutter run
# RESULTADO ESPERADO: App inicia sin crashes
# VERIFICAR: Navegación básica funciona
```

---

## 🚨 CONSECUENCIAS POR VIOLACIONES - AUTOAPLICADAS

### 🟡 VIOLACIÓN MENOR (Auto-Advertencia):
**Síntomas**: No seguir checklist, modificar sin tests
**Auto-Consecuencia**: 
- Detener trabajo inmediatamente
- Ejecutar rollback: `git checkout -- .`
- Reiniciar desde checklist

### 🔴 VIOLACIÓN GRAVE (Auto-Suspensión):
**Síntomas**: Modificar archivos prohibidos, causar errores de compilación
**Auto-Consecuencia**:
- Suspender trabajo por 24 horas
- Rollback completo: `git reset --hard HEAD~1`
- Restaurar desde backup: `cp -r ../zodiac_app_backup_* ./`

### ⚫ VIOLACIÓN CRÍTICA (Auto-Expulsión):
**Síntomas**: Tocar main.dart, firebase_options.dart, romper pagos
**Auto-Consecuencia**:
- Expulsión permanente del proyecto
- Rollback completo: `git reset --hard origin/main`
- Notificar al administrador del proyecto

---

## 🔄 PROTOCOLO MANUAL DE ROLLBACK

### 🆘 CUÁNDO EJECUTAR ROLLBACK MANUAL:
- ❌ Error de compilación: `flutter analyze` muestra errores
- ❌ Tests fallan: `flutter test` no pasa
- ❌ App no inicia: `flutter run` crashea
- ❌ Funcionalidad rota: Navegación no funciona

### 🔄 COMANDOS MANUALES DE ROLLBACK:

#### Rollback Suave (último cambio):
```bash
git checkout -- [archivo_problemático]
```

#### Rollback Medio (último commit):
```bash
git reset --hard HEAD~1
```

#### Rollback Completo (estado seguro):
```bash
git reset --hard origin/main
```

#### Rollback de Emergencia (desde backup):
```bash
rm -rf zodiac_app
cp -r zodiac_app_backup_[timestamp] zodiac_app
```

---

## 📊 AUTO-EVALUACIÓN DE CUMPLIMIENTO

### 🎯 VERIFICAR MANUALMENTE DESPUÉS DE CADA SESIÓN:

#### Métricas Obligatorias:
- [ ] **0 errores nuevos** en `flutter analyze`
- [ ] **0 tests rotos** en `flutter test`
- [ ] **App inicia correctamente** con `flutter run`
- [ ] **0 archivos prohibidos** modificados

#### Auto-Reporte Obligatorio:
```
AGENTE: [tu nombre]
FECHA: [fecha actual]
ARCHIVOS MODIFICADOS: [lista exacta]
FLUTTER ANALYZE: [sin errores/con errores]
FLUTTER TEST: [todos pasan/algunos fallan]
FLUTTER RUN: [inicia correctamente/crashea]
ARCHIVOS PROHIBIDOS TOCADOS: [sí/no]
ROLLBACKS EJECUTADOS: [número]
CUMPLIMIENTO: [100%/parcial/violación]
```

---

## 🤝 COMPROMISO DE HONOR MANUAL

### 📝 DECLARACIÓN PERSONAL (Confirmar antes de empezar):

**YO, [NOMBRE DEL AGENTE], DECLARO QUE:**

1. ✅ He leído completamente este protocolo
2. ✅ Entiendo que debo verificar manualmente cada paso
3. ✅ Me comprometo a ejecutar todos los comandos de verificación
4. ✅ Acepto las auto-consecuencias por violaciones
5. ✅ Priorizaré la estabilidad sobre la velocidad

**CONFIRMACIÓN**: "Acepto el protocolo manual de seguridad"

---

## 🔍 VERIFICACIÓN MANUAL DE ARCHIVOS PROHIBIDOS

### 📋 ANTES DE EDITAR - USAR ESTA CHECKLIST:

```bash
# 1. Ver qué archivo vas a editar
echo "Voy a editar: [NOMBRE_ARCHIVO]"

# 2. Verificar si está prohibido
grep -q "[NOMBRE_ARCHIVO]" PROTOCOLO_CUMPLIMIENTO_OBLIGATORIO.md
# Si encuentra coincidencia = ARCHIVO PROHIBIDO - NO EDITAR

# 3. Verificar cambios actuales
git status
# Revisar que no aparezcan archivos prohibidos

# 4. Antes de commit - verificar diferencias
git diff --name-only
# Asegurar que no hay archivos prohibidos en la lista
```

---

## 🚀 FLUJO DE TRABAJO MANUAL SEGURO

### 📋 PROCESO PASO A PASO:

#### INICIO DE SESIÓN:
1. `cd zodiac_app`
2. `cp -r . ../backup_$(date +%Y%m%d_%H%M%S)`
3. `git checkout -b refactor/mi-tarea`
4. `flutter analyze` (guardar resultado)
5. `flutter test` (guardar resultado)

#### DURANTE EL TRABAJO:
1. Verificar archivo no está prohibido
2. Hacer cambio pequeño (1-2 archivos)
3. `flutter analyze` inmediatamente
4. `flutter test` inmediatamente
5. Si falla algo: `git checkout -- .`

#### FINAL DE SESIÓN:
1. `flutter analyze` (debe ser limpio)
2. `flutter test` (todos deben pasar)
3. `flutter run` (debe iniciar)
4. Probar navegación básica
5. `git add . && git commit -m "..."`

---

## 🔐 CÓDIGO DE HONOR MANUAL

> **"Verificaré manualmente cada cambio antes de continuar"**
> **"La estabilidad es mi responsabilidad personal"**
> **"Prefiero ir lento pero seguro"**

**ENFORCEMENT MANUAL = DISCIPLINA PERSONAL**
**TU RESPONSABILIDAD = ÉXITO DEL PROYECTO**

## 🎯 PROTOCOLO DE EJECUCIÓN POR AGENTE

### 📱 FLUTTER MOBILE EXPERT:
✅ PERMITIDO:
- Crear servicios NUEVOS (sin eliminar existentes)
- Modificar servicios NO críticos
- Agregar providers en /lib/providers/
- Crear widgets nuevos

❌ PROHIBIDO:
- Modificar main.dart
- Eliminar servicios existentes sin migración 100%
- Cambiar dependency injection actual
- Tocar servicios de producción

### 🎨 UI DESIGN SYSTEM EXPERT:
✅ PERMITIDO:
- Crear archivos nuevos en /lib/design_system/
- Consolidar colores en design_system.dart EXISTENTE
- Crear componentes nuevos

❌ PROHIBIDO:
- Eliminar archivos de colores existentes hasta migración completa
- Modificar tema actual sin testing exhaustivo
- Cambiar localización existente

### 🏗️ ARCHITECTURE ANALYSIS EXPERT:
✅ PERMITIDO:
- Análisis read-only
- Generar reportes en archivos NUEVOS
- Documentar problemas sin tocar código

❌ PROHIBIDO:
- Modificar CUALQUIER archivo de código
- Cambiar estructura de directorios
- Mover archivos existentes

### ⚡ PERFORMANCE EXPERT:
✅ PERMITIDO:
- Crear performance_service.dart NUEVO
- Análisis de performance sin modificar código
- Optimizaciones en servicios NO críticos

❌ PROHIBIDO:
- Eliminar servicios de performance existentes
- Modificar sistema de caché actual
- Cambiar configuración de memoria
```

### 🌐 BACKEND API EXPERT:
```
✅ PERMITIDO:
- Crear API clients nuevos
- Trabajar en /lib/services/api/ (nuevo directorio)
- Integración MCP en backend

❌ PROHIBIDO:
- Modificar servicios Firebase existentes
- Cambiar configuración de autenticación
- Tocar revenue_cat_service.dart
```

### 🧪 TESTING EXPERT:
```
✅ PERMITIDO:
- Crear tests nuevos
- Ejecutar tests existentes
- Generar reportes de coverage

❌ PROHIBIDO:
- Eliminar tests existentes
- Modificar configuración de testing
- Cambiar estructura de /test/ sin aprobación
```

---

## 🚨 CONSECUENCIAS POR INCUMPLIMIENTO

### 🔴 NIVEL 1: Violación Menor
**Ejemplo**: No ejecutar tests antes de commit
**Consecuencia**: 
- ⚠️ Advertencia formal
- 🔄 Rollback obligatorio
- 📝 Documentación del incidente

### 🔴 NIVEL 2: Violación Grave  
**Ejemplo**: Modificar archivo en lista negra
**Consecuencia**:
- 🚫 Suspensión temporal del agente
- 🔄 Rollback completo a backup
- 📋 Re-training obligatorio del protocolo

### 🔴 NIVEL 3: Violación Crítica
**Ejemplo**: Romper funcionalidad de producción
**Consecuencia**:
- ❌ **EXPULSIÓN PERMANENTE** del proyecto
- 🔄 Restauración completa desde backup
- 📊 Reporte de incidente crítico

---

## 📋 REGISTRO DE CUMPLIMIENTO

### 📊 Tracking Obligatorio por Agente:

#### **Flutter Mobile Expert**:
- [ ] Backup verificado antes de iniciar
- [ ] Solo archivos permitidos modificados
- [ ] Tests ejecutados después de cada cambio
- [ ] Compilación verificada
- [ ] Funcionalidad crítica intacta

#### **UI Design System Expert**:
- [ ] Backup verificado antes de iniciar
- [ ] Solo creación de archivos nuevos
- [ ] No eliminación de archivos existentes
- [ ] Testing visual completado
- [ ] Compatibilidad con tema actual

#### **Architecture Analysis Expert**:
- [ ] Solo análisis read-only ejecutado
- [ ] Cero modificaciones de código
- [ ] Reportes generados en archivos separados
- [ ] Documentación completa sin tocar implementación

#### **Performance Expert**:
- [ ] Backup verificado antes de iniciar
- [ ] Solo servicios nuevos creados
- [ ] Métricas baseline respetadas
- [ ] No degradación de performance
- [ ] Testing de performance completado

#### **Backend API Expert**:
- [ ] Backup verificado antes de iniciar
- [ ] Solo nuevos API clients creados
- [ ] Servicios críticos intactos
- [ ] Integración sin disrupciones
- [ ] Testing de conectividad completado

#### **Testing Expert**:
- [ ] Tests baseline ejecutados
- [ ] Solo tests nuevos agregados
- [ ] Cobertura no reducida
- [ ] Todos los tests pasando
- [ ] Reportes de regresión generados

---

## 🔒 SISTEMA DE MONITOREO CONTINUO

### 📊 Métricas de Cumplimiento (Tracking Automático):

#### **Métricas de Seguridad**:
- ✅ **Archivos prohibidos tocados**: 0 (OBLIGATORIO)
- ✅ **Tests fallando**: 0 (OBLIGATORIO)  
- ✅ **Errores de compilación**: 0 (OBLIGATORIO)
- ✅ **Degradación de performance**: <5% (MÁXIMO)

#### **Métricas de Proceso**:
- ✅ **Backups realizados**: 100% (OBLIGATORIO)
- ✅ **Tests ejecutados pre-commit**: 100% (OBLIGATORIO)
- ✅ **Verificaciones de seguridad**: 100% (OBLIGATORIO)
- ✅ **Rollbacks exitosos**: 100% cuando necesario

---

## 🎯 ENFORCEMENT AUTOMÁTICO

### 🤖 Git Hooks Obligatorios:

#### **Pre-Commit Hook**:
```bash
#!/bin/bash
# Este hook DEBE estar activo en todos los repositorios
./.git/hooks/security-check.sh || {
    echo "🚨 COMMIT BLOQUEADO POR VIOLACIÓN DE SEGURIDAD"
    exit 1
}
```

#### **Pre-Push Hook**:
```bash
#!/bin/bash
# Verificación final antes de push
flutter test || {
    echo "🚨 PUSH BLOQUEADO - TESTS FALLANDO"
    exit 1
}
```

---

## 📞 ESCALACIÓN DE INCIDENTES

### 🚨 Proceso de Reporte Inmediato:

#### **Si Detectas Violación**:
1. **DETENER** inmediatamente toda actividad
2. **DOCUMENTAR** la violación específica
3. **EJECUTAR** rollback si es necesario
4. **REPORTAR** al coordinador del proyecto
5. **ESPERAR** instrucciones antes de continuar

#### **Contactos de Emergencia**:
- 🔴 **Violación Crítica**: Escalación inmediata
- 🟡 **Violación Menor**: Reporte dentro de 1 hora
- 📊 **Métricas Anómalas**: Reporte diario

---

## ✅ CONFIRMACIÓN DE CUMPLIMIENTO

### 📝 Declaración Obligatoria por Agente:

**"Yo, [NOMBRE_AGENTE], confirmo que:**
- ✅ He leído y entendido completamente este protocolo
- ✅ Me comprometo a seguir todas las reglas sin excepción
- ✅ Entiendo las consecuencias por incumplimiento
- ✅ Ejecutaré backup y testing antes de cualquier cambio
- ✅ NO tocaré archivos en la lista prohibida
- ✅ Reportaré inmediatamente cualquier problema"

**Fecha de Confirmación**: ___________
**Firma Digital**: ___________

---

*Protocolo de Cumplimiento Obligatorio*  
*Generado por Cascade AI - Enforcement Automático*  
*Fecha: 2025-09-14*  
*Versión: 1.0 - NO MODIFICAR SIN AUTORIZACIÓN*