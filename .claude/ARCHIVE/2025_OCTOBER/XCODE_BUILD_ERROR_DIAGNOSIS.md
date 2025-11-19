# 🔍 DIAGNÓSTICO: Error PhaseScriptExecution en Xcode

**Fecha**: October 10, 2025
**Proyecto**: Zodiac App (Flutter iOS)
**Error**: `Command PhaseScriptExecution failed with a nonzero exit code`

---

## 🚨 PROBLEMAS IDENTIFICADOS

### 1. ⚠️ CRÍTICO: Ruta con Espacios y Caracteres Especiales

**Problema Detectado**:
```
/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app
                                    ↑        ↑
                            Espacio antes    Espacio después
```

**Por qué es problemático**:
- Los scripts de shell en Xcode NO manejan bien rutas con espacios sin quoting
- El script de Flutter `xcode_backend.sh` puede fallar al interpretar la ruta
- Causa `ProcessException` y `PhaseScriptExecution failed`

**Evidencia en project.pbxproj**:
```bash
export FLUTTER_APPLICATION_PATH="/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app"
```

**Referencia**: Caso documentado en dev.to donde un espacio al final del directorio causaba exactamente este error ￼.

---

### 2. 🔧 Scripts de Build Detectados

**Scripts identificados en el proyecto**:

#### A. Flutter Build Script
```bash
shellScript = "export FLUTTER_ROOT=\"/opt/homebrew/Caskroom/flutter/3.29.2/flutter\"
export FLUTTER_APPLICATION_PATH=\"/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app\"
export FLUTTER_BUILD_DIR=build
/bin/sh \"$FLUTTER_ROOT/packages/flutter_tools/bin/xcode_backend.sh\" build
";
```
**Riesgo**: ALTO - Ruta con espacios puede causar fallo

#### B. Flutter Embed & Thin Script
```bash
shellScript = "/bin/sh \"$FLUTTER_ROOT/packages/flutter_tools/bin/xcode_backend.sh\" embed_and_thin";
```
**Riesgo**: MEDIO - Depende de variables de entorno

#### C. CocoaPods Check Manifest
```bash
shellScript = "diff \"${PODS_PODFILE_DIR_PATH}/Podfile.lock\" \"${PODS_ROOT}/Manifest.lock\" > /dev/null
if [ $? != 0 ] ; then
    echo \"error: The sandbox is not in sync with the Podfile.lock. Run 'pod install'\" >&2
    exit 1
fi
";
```
**Riesgo**: BAJO - Pero puede fallar si pods están desincronizados

---

### 3. 📱 Configuración de Entitlements

**Archivos encontrados**:
- `Runner.entitlements` (Development)
- `Runner-Release.entitlements` (Release)

**Contenido actual (Runner.entitlements)**:
```xml
✅ aps-environment: development (correcto para Debug)
✅ associated-domains: applinks configurado
✅ keychain-access-groups: configurado para flutter_secure_storage
✅ application-groups: configurado
```

**Estado**: ✅ CORRECTO - Entitlements están bien configurados

---

### 4. 🔐 Posibles Problemas de Firma

**Esquema actual**: Desconocido (necesita verificación)
**Configuración recomendada**:
- Debug → usar certificado de desarrollo
- Release → usar certificado de distribución

**Problema común**: Compilar en Release sin perfil de distribución causa fallo en firma

---

## 🎯 PLAN DE CORRECCIÓN

### OPCIÓN A: Solución Definitiva (Recomendada)

**1. Renombrar directorio del proyecto** (eliminar espacios)

```bash
# Desde Desktop
cd "/Users/alejandrocaceres/Desktop"

# Renombrar "appstore - zodia" → "appstore-zodia"
mv "appstore - zodia" "appstore-zodia"
```

**Nuevo path**:
```
/Users/alejandrocaceres/Desktop/appstore-zodia/zodiac_app
```

**2. Actualizar referencias en Xcode**

Después de renombrar, abrir Xcode y dejar que detecte automáticamente el nuevo path, o manualmente:
- Abrir `Runner.xcodeproj`
- File → Project Settings → Advanced
- Verificar que las rutas se actualizaron

**3. Limpiar y reconstruir**

```bash
cd "/Users/alejandrocaceres/Desktop/appstore-zodia/zodiac_app"

# Flutter clean
flutter clean
flutter pub get

# CocoaPods clean
cd ios
rm -rf Pods Podfile.lock
pod deintegrate
pod install

# Xcode clean
# En Xcode: Product → Clean Build Folder (⇧⌘K)
```

---

### OPCIÓN B: Solución Temporal (Si no puedes renombrar)

**1. Actualizar scripts con quoting correcto**

Editar manualmente `Runner.xcodeproj/project.pbxproj`:

**Antes**:
```bash
export FLUTTER_APPLICATION_PATH="/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app"
```

**Después** (con escaping):
```bash
export FLUTTER_APPLICATION_PATH='/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app'
```

⚠️ **Advertencia**: Esto puede ser sobrescrito por Flutter en futuras regeneraciones.

**2. Limpiar caché**

```bash
# Flutter clean
flutter clean
rm -rf build/
flutter pub get

# CocoaPods
cd ios
pod deintegrate
rm -rf Pods Podfile.lock .symlinks
pod install

# Xcode clean build folder
```

---

### OPCIÓN C: Diagnóstico Paso a Paso (Actual)

**Paso 1: Identificar el script que falla**

```bash
# Ejecutar build desde terminal para ver logs completos
cd "/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app/ios"

xcodebuild \
  -workspace Runner.xcworkspace \
  -scheme Runner \
  -configuration Debug \
  -destination 'generic/platform=iOS Simulator' \
  clean build 2>&1 | tee build_log.txt
```

**Buscar en el log**:
```bash
grep -i "error" build_log.txt
grep -i "failed" build_log.txt
grep -i "PhaseScriptExecution" build_log.txt
```

**Paso 2: Verificar configuración del esquema**

En Xcode:
1. Product → Scheme → Edit Scheme (⌘<)
2. Verificar que Run esté en **Debug** (no Release)
3. Verificar que Build Configuration sea **Debug**

**Paso 3: Revisar Run Script phases**

En Xcode:
1. Target Runner → Build Phases
2. Para cada Run Script:
   - ✅ Verificar que el script existe
   - ✅ Marcar "Run script only when installing" si no es crítico
   - ✅ Verificar que paths sean correctos

---

## 🔍 CHECKLIST DE VERIFICACIÓN

### Antes de Build
- [ ] Directorio NO contiene espacios en el path
- [ ] `flutter clean` ejecutado
- [ ] `pod deintegrate` y `pod install` ejecutados
- [ ] Xcode Build Folder limpiado (⇧⌘K)
- [ ] Esquema configurado en Debug (no Release)
- [ ] Certificado de desarrollo válido instalado
- [ ] Bundle ID correcto en Xcode
- [ ] Equipo correcto seleccionado

### Durante Build
- [ ] No hay errores de "No such file or directory"
- [ ] Scripts de Flutter se ejecutan correctamente
- [ ] CocoaPods manifest está sincronizado
- [ ] Firma de código exitosa

### Después de Build
- [ ] App compila sin errores
- [ ] No hay warnings de entitlements
- [ ] Puede ejecutarse en simulador/dispositivo

---

## 🚨 SÍNTOMAS POR CAUSA

### Si el error es por RUTA CON ESPACIOS:
```
Error: ProcessException
Error: Command PhaseScriptExecution failed
Log: No such file or directory
Log: /Users/.../Desktop/appstore (resto del path cortado)
```

**Solución**: Renombrar directorio

---

### Si el error es por PODS DESINCRONIZADOS:
```
Error: The sandbox is not in sync with the Podfile.lock
Exit code: 1
```

**Solución**:
```bash
cd ios
pod deintegrate
rm Podfile.lock
pod install
```

---

### Si el error es por FIRMA DE CÓDIGO:
```
Error: Code signing failed
Error: No matching provisioning profiles found
Exit code: 1 (en fase de firma)
```

**Solución**:
1. Xcode → Signing & Capabilities
2. Activar "Automatically manage signing"
3. Seleccionar equipo correcto
4. Cambiar a Debug si estás en Release

---

### Si el error es por FLUTTER_ROOT:
```
Error: FLUTTER_ROOT not found
Error: xcode_backend.sh: No such file or directory
```

**Solución**:
```bash
# Verificar que Flutter esté instalado
which flutter
# Debe mostrar: /opt/homebrew/Caskroom/flutter/3.29.2/flutter/bin/flutter

# Si no, reinstalar Flutter o actualizar path
```

---

## 📊 DIAGNÓSTICO ACTUAL

### Problema Identificado
✅ **CONFIRMADO**: Ruta del proyecto contiene espacios
```
/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app
                                    ↑     ↑
                                  Problema detectado
```

### Impacto
- 🔴 **CRÍTICO**: Los scripts de Flutter pueden fallar
- 🟡 **MEDIO**: CocoaPods puede tener problemas con paths
- 🟢 **BAJO**: Entitlements están correctos

### Recomendación
🎯 **ACCIÓN INMEDIATA**: Renombrar directorio "appstore - zodia" → "appstore-zodia"

---

## 🛠️ COMANDOS DE EJECUCIÓN

### Plan Completo de Limpieza y Rebuild

```bash
#!/bin/bash
# XCODE_BUILD_FIX.sh

set -e

echo "🧹 Paso 1: Limpieza de Flutter..."
cd "/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app"
flutter clean
rm -rf build/
flutter pub get

echo "🧹 Paso 2: Limpieza de CocoaPods..."
cd ios
pod deintegrate 2>/dev/null || true
rm -rf Pods Podfile.lock .symlinks
pod install

echo "✅ Limpieza completada. Ahora:"
echo "1. Abre Xcode"
echo "2. Product → Clean Build Folder (⇧⌘K)"
echo "3. Product → Build (⌘B)"
echo ""
echo "⚠️  IMPORTANTE: Considera renombrar el directorio para eliminar espacios"
echo "   mv '/Users/alejandrocaceres/Desktop/appstore - zodia' '/Users/alejandrocaceres/Desktop/appstore-zodia'"
```

**Ejecutar**:
```bash
chmod +x XCODE_BUILD_FIX.sh
./XCODE_BUILD_FIX.sh
```

---

## 📝 PRÓXIMOS PASOS

### Paso 1: Ejecutar Diagnóstico
```bash
cd "/Users/alejandrocaceres/Desktop/appstore - zodia/zodiac_app"
flutter doctor -v
```

### Paso 2: Limpiar Todo
```bash
# Ejecutar el script de limpieza completo (ver arriba)
```

### Paso 3: Build desde Terminal
```bash
cd ios
xcodebuild -workspace Runner.xcworkspace \
  -scheme Runner \
  -configuration Debug \
  -destination 'generic/platform=iOS Simulator' \
  clean build
```

### Paso 4: Si Falla, Renombrar Directorio
```bash
cd "/Users/alejandrocaceres/Desktop"
mv "appstore - zodia" "appstore-zodia"
# Luego repetir Paso 2 y 3
```

---

## ✅ CRITERIOS DE ÉXITO

El error estará resuelto cuando:
- [ ] Build completa sin errores
- [ ] No aparece "PhaseScriptExecution failed"
- [ ] App se ejecuta en simulador
- [ ] Logs muestran "BUILD SUCCEEDED"

---

**Fecha de Diagnóstico**: October 10, 2025
**Analista**: Master Coordinator
**Prioridad**: 🔴 ALTA
**Tiempo Estimado de Resolución**: 15-30 minutos
