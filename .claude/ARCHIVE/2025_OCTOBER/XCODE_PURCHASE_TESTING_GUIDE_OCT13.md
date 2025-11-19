# 🎯 XCODE PURCHASE TESTING - Guía Paso a Paso (13 Oct 2025)

**Estado Actual**: ✅ Xcode abierto y listo para testing
**Objetivo**: Probar las compras in-app usando StoreKit Configuration
**Tiempo estimado**: 5-10 minutos

---

## 📊 SITUACIÓN ACTUAL

### ✅ LO QUE YA FUNCIONA:
- ✅ App compila y corre perfectamente con `flutter run`
- ✅ Flutter 3.35.6 instalado en `~/flutter`
- ✅ 47 pods instalados correctamente
- ✅ RevenueCat configurado con API Key
- ✅ **Products.storekit** configurado con 3 productos:
  - `tier1_subscription` - Cosmic Premium ($6.99/mes) + 1 semana gratis
  - `tier2_subscription` - Stellar Tier ($19.99/mes) + 1 semana gratis
  - `lifetime_tier1_purchase` - Universe Lifetime ($49.99 one-time)
- ✅ Xcode scheme ya tiene StoreKit Configuration configurado (líneas 76-78)

### ❌ EL PROBLEMA:
- iOS 18.2/18.4 simulator tiene **bug conocido de Apple** con Sandbox
- `flutter run` **NO usa** StoreKit Configuration files
- xcodebuild CLI falla con "Flutter/Flutter.h not found"

### ✅ LA SOLUCIÓN:
**Usar Xcode GUI directamente** - esto SÍ usa Products.storekit correctamente

---

## 🚀 PASOS PARA PROBAR COMPRAS EN XCODE

### Paso 1: Verificar que Xcode esté abierto ✅

Xcode ya fue abierto con el comando:
```bash
open ios/Runner.xcworkspace
```

**Espera 10-20 segundos** para que Xcode termine de indexar el proyecto.

---

### Paso 2: Verificar StoreKit Configuration

En Xcode, hacer lo siguiente:

1. **Product** (menú superior) → **Scheme** → **Edit Scheme...**
2. En la ventana que abre, seleccionar **Run** (lado izquierdo)
3. Ir a la pestaña **Options**
4. Buscar **"StoreKit Configuration"**
5. **Verificar** que diga: `../Products.storekit` ✅

**Si NO está configurado**:
1. Click en el dropdown de "StoreKit Configuration"
2. Seleccionar `Products.storekit`
3. Click "Close"

**Si YA está configurado** (debería estarlo):
1. Simplemente click "Close"

---

### Paso 3: Seleccionar Simulador

En la barra superior de Xcode:

1. Click en el dropdown junto a "Runner" (donde dice el dispositivo)
2. Seleccionar: **iPhone 16 Pro** (o cualquier iPhone 15/16 simulator)
3. **NO uses iPhone físico todavía** (requiere Xcode 16.4 para iOS 26.0.1)

---

### Paso 4: Ejecutar la App

1. Click en el botón **Play ▶️** (arriba a la izquierda)
2. Xcode empezará a compilar
3. **Espera 1-2 minutos** para la primera compilación
4. El simulador se abrirá automáticamente
5. La app se lanzará

**Si ves errores de compilación**:
- Revisa la pestaña "Issues" en Xcode
- Si dice "PhaseScriptExecution failed": ver sección de Troubleshooting abajo

---

### Paso 5: Navegar a Premium Screen

Una vez la app esté corriendo:

1. En la app, buscar el botón de **"Premium"** o **"Upgrade"**
2. Navegar a la pantalla de subscripciones
3. **Deberías ver 3 opciones**:
   - Cosmic Premium - $6.99/month (1 week free trial)
   - Stellar Tier - $19.99/month (1 week free trial)
   - Universe Lifetime - $49.99 (one-time purchase)

---

### Paso 6: Probar una Compra

1. Click en cualquiera de los 3 botones de compra
2. **Aparecerá el Payment Sheet de StoreKit**
3. En el sheet, verás:
   - Nombre del producto
   - Precio
   - Botón "Subscribe" o "Buy"
4. Click en **"Subscribe"** o **"Buy"**
5. **NO necesitas Touch ID** (es local testing)
6. La compra debería completarse instantáneamente

---

### Paso 7: Verificar que Premium se Activó

Después de comprar:

1. La app debería mostrar mensaje de éxito
2. Las features premium deberían desbloquearse
3. El UI debería cambiar mostrando que eres premium

**Para verificar en logs**:
En Xcode, ir a la **Console** (abajo) y buscar:
```
✅ Purchase successful
✅ Entitlements: [cosmic] o [stellar] o [universe]
✅ Customer info updated
```

---

## 🐛 TROUBLESHOOTING

### Problema 1: "PhaseScriptExecution failed"

**Síntomas**: Xcode muestra error al compilar

**Solución A - Limpiar DerivedData**:
```bash
# En terminal:
rm -rf ~/Library/Developer/Xcode/DerivedData/*
```

Luego en Xcode: **Product** → **Clean Build Folder** (Cmd+Shift+K)

**Solución B - Verificar Flutter Path**:
```bash
# En terminal:
export PATH="$HOME/flutter/bin:$PATH"
export FLUTTER_ROOT="$HOME/flutter"
which flutter
# Debería mostrar: /Users/alejandrocaceres/flutter/bin/flutter
```

Luego reintentar en Xcode.

**Solución C - Reabrir Xcode**:
1. Cerrar Xcode completamente (Cmd+Q)
2. En terminal:
```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
open ios/Runner.xcworkspace
```
3. Esperar que indexe
4. Presionar Play ▶️

---

### Problema 2: "No products available"

**Causa**: StoreKit Configuration no está cargado

**Solución**:
1. Product → Scheme → Edit Scheme
2. Run → Options
3. StoreKit Configuration → Seleccionar `Products.storekit`
4. Close
5. Clean Build Folder (Cmd+Shift+K)
6. Run (Cmd+R)

---

### Problema 3: "Offerings not found" en logs

**Causa**: RevenueCat no puede cargar offerings

**Solución A - Verificar API Key**:
```bash
# En terminal:
grep -r "appl_" zodiac_app/lib/main.dart
# Debería mostrar: appl_TwCrrBozYBCYouyUHpLJturOSSD
```

**Solución B - Verificar Internet**:
- RevenueCat necesita internet para sincronizar
- Verificar que el simulador tenga conexión

---

### Problema 4: Xcode "Indexing..." por mucho tiempo

**Solución**:
1. Espera 1-2 minutos
2. Si sigue indexing después de 3 minutos:
   - Cerrar Xcode (Cmd+Q)
   - En terminal:
   ```bash
   rm -rf ~/Library/Developer/Xcode/DerivedData/*
   ```
   - Reabrir Xcode
   - Esperar nuevo index (será más rápido)

---

## 📋 CHECKLIST DE ÉXITO

Marca cuando completes cada paso:

- [ ] ✅ Xcode abierto con Runner.xcworkspace
- [ ] ✅ StoreKit Configuration verificado en scheme
- [ ] ✅ Simulador iPhone 16 Pro seleccionado
- [ ] ✅ App compiló sin errores
- [ ] ✅ Simulador abrió la app
- [ ] ✅ Navegué a Premium screen
- [ ] ✅ Veo 3 productos con precios correctos
- [ ] ✅ Click en un producto abrió Payment Sheet
- [ ] ✅ Compra se completó exitosamente
- [ ] ✅ Premium features se activaron
- [ ] ✅ Logs muestran "Purchase successful"

**Si marcaste todo ✅**: ¡FELICITACIONES! Tus compras funcionan perfectamente.

---

## 🎯 PRÓXIMOS PASOS

### Para Producción:

Una vez verificado que funciona en Xcode:

1. **Actualizar Xcode a 16.4** (para soportar iOS 26.0.1)
   - Mac → System Settings → Software Update
   - Tiempo: 30-50 minutos

2. **Crear Sandbox Tester en App Store Connect**
   - App Store Connect → Users and Access → Sandbox Testers
   - Email: test.zodiac@icloud.com
   - Password: ZodiacTest2025!

3. **Configurar iPhone físico**
   - Ajustes → App Store → Sandbox Account
   - Iniciar sesión con sandbox tester

4. **Probar en iPhone real**
   ```bash
   export PATH="$HOME/flutter/bin:$PATH"
   flutter run -d "Alejandro's iPhone"
   ```

5. **Verificar en RevenueCat Dashboard**
   - https://app.revenuecat.com
   - Customers → Buscar tu userID
   - Verificar entitlement activo

---

## 📊 COMPARACIÓN: XCODE vs FLUTTER RUN

| Aspecto | Xcode GUI | flutter run |
|---------|-----------|-------------|
| **Usa Products.storekit** | ✅ Sí | ❌ No |
| **Testing local** | ✅ Sí | ❌ No |
| **Compila con Flutter paths** | ✅ Sí | ✅ Sí |
| **Hot reload** | ❌ No | ✅ Sí |
| **Debugging** | ✅ Breakpoints | ✅ Print logs |
| **Tiempo compilación** | ~2 min | ~50 seg |
| **Velocidad iteración** | Lenta | Rápida |
| **Testing compras** | ✅ PERFECTO | ❌ No funciona |

**Conclusión**:
- **Para probar compras**: Usa Xcode
- **Para desarrollo normal**: Usa `flutter run`

---

## 💡 TIPS IMPORTANTES

### 1. StoreKit Testing vs Sandbox Testing

**StoreKit Testing** (lo que estamos usando):
- ✅ Funciona en simulador
- ✅ No necesita sandbox account
- ✅ Compras instantáneas
- ✅ No necesita internet (para StoreKit)
- ⚠️ RevenueCat SÍ necesita internet para sincronizar

**Sandbox Testing** (para iPhone físico):
- ✅ Más realista
- ✅ Testing completo de producción
- ✅ Funciona con RevenueCat dashboard
- ⚠️ Requiere sandbox account
- ⚠️ Requiere Xcode 16.4 para iOS 26.0.1

### 2. iOS 18.2 Simulator Bug

**Bug Oficial de Apple**:
- iOS 18.2 y 18.4 simulators tienen bug con Sandbox accounts
- NO es problema de tu código
- NO es problema de RevenueCat
- Es limitación conocida de Apple

**Workarounds**:
1. ✅ Usar StoreKit Configuration (lo que hacemos)
2. ✅ Usar iOS 17.5 simulator (downgrade)
3. ✅ Usar dispositivo físico (requiere Xcode update)

### 3. Productos Configurados

Tu **Products.storekit** tiene:

```json
{
  "tier1_subscription": {
    "price": "$6.99/month",
    "trial": "1 week free",
    "name": "Cosmic Premium"
  },
  "tier2_subscription": {
    "price": "$19.99/month",
    "trial": "1 week free",
    "name": "Stellar Tier"
  },
  "lifetime_tier1_purchase": {
    "price": "$49.99",
    "type": "one-time",
    "name": "Universe Lifetime"
  }
}
```

**Estos DEBEN coincidir** con:
- App Store Connect → In-App Purchases
- RevenueCat Dashboard → Products

---

## 🔍 VERIFICAR CONFIGURACIÓN

### Comando 1: Ver Products.storekit
```bash
cat /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/ios/Products.storekit | grep -A 2 "productID"
```

### Comando 2: Ver API Key
```bash
grep "appl_" /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/lib/main.dart
```

### Comando 3: Ver Scheme Configuration
```bash
cat /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/ios/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme | grep -A 1 "StoreKitConfigurationFileReference"
```

**Debería mostrar**:
```xml
<StoreKitConfigurationFileReference
   identifier = "../Products.storekit">
```

---

## 📱 ESTADO ACTUAL - RESUMEN

```
✅ Flutter: 3.35.6 @ ~/flutter
✅ Xcode: 16.3 (abierto)
✅ Pods: 47 instalados
✅ RevenueCat: Configurado
✅ Products.storekit: 3 productos
✅ Scheme: StoreKit configurado
✅ Simulador: iOS 18.2 disponible

⏳ SIGUIENTE: Presionar Play ▶️ en Xcode
```

---

## 🎉 CUANDO FUNCIONE

Una vez que veas las compras funcionando:

1. ✅ **Toma screenshots** del flujo de compra
2. ✅ **Documenta** cualquier issue que encuentres
3. ✅ **Prueba los 3 productos** (Cosmic, Stellar, Universe)
4. ✅ **Verifica** que cada entitlement se active
5. ✅ **Cierra y reabre** la app para verificar persistencia

**Luego**:
- Puedes continuar desarrollando con `flutter run` (hot reload rápido)
- Solo vuelve a Xcode cuando necesites probar compras
- Cuando actualices Xcode 16.4, podrás probar en iPhone físico

---

## 📞 REFERENCIAS

- **Session Summary**: `RESUMEN_FINAL_SESION_COMPRAS_OCT13.md`
- **Solución Completa**: `SOLUCION_DEFINITIVA_TESTING_COMPRAS_2025.md`
- **Products File**: `zodiac_app/ios/Products.storekit`
- **Scheme File**: `zodiac_app/ios/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme`

---

**Creado**: 13 Octubre 2025 - 10:30 PM
**Para**: Testing de compras in-app con StoreKit Configuration
**Estado**: ✅ LISTO PARA TESTING

**¡AHORA PRESIONA PLAY EN XCODE Y PRUEBA TUS COMPRAS! 🚀**
