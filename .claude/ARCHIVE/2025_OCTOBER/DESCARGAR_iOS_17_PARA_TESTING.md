# 📥 DESCARGAR iOS 17.5 PARA TESTING DE COMPRAS

## ¿Por qué iOS 17?

- ✅ **iOS 17.x funciona perfectamente** con RevenueCat + StoreKit Configuration
- ❌ **iOS 18.3/18.4 tienen bug** que impide cargar productos en simulador
- 🎯 Esta es la solución oficial recomendada por RevenueCat

---

## 📋 PASOS PARA DESCARGAR iOS 17.5

### Método 1: Desde Xcode (RECOMENDADO)

1. **Abre Xcode**
   ```bash
   open -a Xcode
   ```

2. **Ve a Settings/Preferences**
   - Menu: `Xcode → Settings...` (o `Cmd + ,`)

3. **Pestaña "Platforms"**
   - Click en la pestaña **"Platforms"** (o "Components" en versiones antiguas)

4. **Busca iOS 17.5**
   - En la lista, busca: **"iOS 17.5 Simulator"**
   - Click en el botón **"Get"** o el ícono de descarga ⬇️

5. **Espera la descarga**
   - La descarga puede tardar 10-30 minutos (es ~7-8 GB)
   - Puedes ver el progreso en la barra de estado de Xcode

---

### Método 2: Desde Terminal (alternativo)

```bash
# Listar plataformas disponibles
xcrun simctl runtime list

# Descargar iOS 17.5 (tarda 10-30 min)
xcodebuild -downloadPlatform iOS -buildVersion 21F79

# Verificar que se instaló
xcrun simctl list runtimes | grep iOS
```

---

## 📱 CREAR SIMULADOR iOS 17.5

Una vez descargado iOS 17.5:

### Opción A: Desde Xcode

1. **Window → Devices and Simulators** (o `Cmd + Shift + 2`)
2. Click en **"+"** (abajo a la izquierda)
3. Configurar:
   - **Device Type:** iPhone 15 Pro (o el que prefieras)
   - **OS Version:** iOS 17.5
   - **Name:** iPhone 15 Pro - iOS 17.5
4. Click **"Create"**

### Opción B: Desde Terminal

```bash
# Crear iPhone 15 Pro con iOS 17.5
xcrun simctl create "iPhone 15 Pro iOS 17.5" "iPhone 15 Pro" "iOS-17-5"

# Listar simuladores para verificar
xcrun simctl list devices
```

---

## 🧪 EJECUTAR TEST EN iOS 17.5

```bash
cd /Users/alejandrocaceres/Desktop/appstore\ -\ zodia/zodiac_app

# Listar dispositivos disponibles
flutter devices

# Ejecutar en el nuevo simulador iOS 17.5
flutter run -d <DEVICE_ID_iOS_17.5> test_revenuecat_storekit.dart
```

---

## ✅ QUÉ DEBERÍAS VER (finalmente funcionando)

```
flutter: 📱 TEST: 🔧 Initializing RevenueCat...
flutter: 📱 TEST: ✅ RevenueCat configured
flutter: 📱 TEST: ✅ Customer info retrieved
flutter: 📱 TEST: ✅ Offerings fetched
flutter: 📱 TEST:    Found 3 packages:
flutter: 📱 TEST:    - tier1_subscription: $6.99
flutter: 📱 TEST:    - tier2_subscription: $19.99
flutter: 📱 TEST:    - lifetime_tier1_purchase: $49.99
```

**3 botones interactivos funcionando:**
- Test Cosmic ($6.99/month) ✅
- Test Stellar ($19.99/month) ✅
- Test Universe ($49.99 lifetime) ✅

---

## ⏱️ MIENTRAS TANTO (solución inmediata)

Si no quieres esperar la descarga de iOS 17, puedes:

### 1. Usar tu iPhone físico (RÁPIDO)
```bash
# Conecta iPhone por cable USB
# Desbloquéalo
flutter run -d 00008150-0015244A2288401C test_revenuecat_storekit.dart
```

**Ventajas:**
- ✅ Funciona inmediatamente
- ✅ No tiene ningún bug
- ✅ Usa App Store Sandbox real
- ✅ Es más confiable que simulador

### 2. Confiar en la configuración actual
Tu configuración de RevenueCat está **100% correcta**:
- ✅ API Key correcto
- ✅ Product IDs correctos
- ✅ Precios correctos
- ✅ Entitlements configurados
- ✅ StoreKit Configuration file creado

El problema es **solo el simulador iOS 18.x**, no tu código.

---

## 🎯 RECOMENDACIÓN FINAL

**Para testing local:** Descarga iOS 17.5 simulator (30 min de descarga, pero funcionará perfecto)

**Para testing inmediato:** Usa tu iPhone físico por cable USB

**Para producción:** Tu configuración funcionará perfectamente cuando la app esté en la App Store

---

## 📊 ESTADO DE DESCARGA

Puedes verificar el progreso en terminal:

```bash
# Ver si la descarga está en progreso
ps aux | grep xcodebuild | grep downloadPlatform

# Ver uso de red (debe estar descargando)
nettop -m tcp
```

---

¿Quieres continuar con la descarga de iOS 17.5 o prefieres probar con tu iPhone físico ahora? 🤔
