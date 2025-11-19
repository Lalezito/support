# 🛠️ CONFIGURAR STOREKIT EN XCODE (PASO A PASO)

## ❌ PROBLEMA ACTUAL

```
PlatformException(23, None of the products could be fetched from App Store Connect)
```

**Causa:** RevenueCat no puede cargar productos porque:
1. Los productos aún no están **aprobados** en App Store Connect, O
2. No hay StoreKit Configuration File activo en Xcode

## ✅ SOLUCIÓN: CONFIGURAR STOREKIT CONFIGURATION

### 📋 PASOS DETALLADOS

#### 1️⃣ Abrir el Proyecto en Xcode

```bash
open /Users/alejandrocaceres/Desktop/appstore\ -\ zodia/zodiac_app/ios/Runner.xcworkspace
```

**Espera a que Xcode abra completamente** (puede tardar 10-20 segundos)

---

#### 2️⃣ Seleccionar el Scheme

1. En la barra superior de Xcode, encuentra el botón que dice **"Runner"** (junto al botón de Play ▶️)
2. Click en **"Runner"**
3. Selecciona **"Edit Scheme..."** del menú dropdown

---

#### 3️⃣ Configurar StoreKit

1. En el panel que se abre, selecciona **"Run"** en el sidebar izquierdo
2. Click en la pestaña **"Options"** (arriba)
3. Scroll down hasta encontrar **"StoreKit Configuration"**
4. En el dropdown, selecciona: **`ZodiacStoreKitConfig.storekit`**
   - Si no aparece, click en "+" y navega a: `ios/ZodiacStoreKitConfig.storekit`
5. Click **"Close"**

---

#### 4️⃣ Verificar que Está Activo

En la barra superior de Xcode:
- Debería aparecer un nuevo ícono ✓ junto al simulador
- O el texto "StoreKit: ZodiacStoreKitConfig.storekit"

---

#### 5️⃣ Ejecutar desde Xcode

**IMPORTANTE:** Debes correr la app **desde Xcode**, no desde terminal.

1. Selecciona el simulador: **iPhone 16 Pro iOS 18.3**
2. Click en el botón **Play ▶️** (arriba a la izquierda)
3. Espera a que compile y se abra el simulador

---

## 🧪 QUÉ DEBERÍAS VER

### ✅ **Si funciona correctamente:**

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

### ❌ **Si sigue sin funcionar:**

```
flutter: 📱 TEST: ❌ Error: PlatformException(23, None of the products...
```

Entonces el problema es que el archivo StoreKit **no está siendo usado**.

---

## 🎯 ALTERNATIVA: EDITAR DIRECTAMENTE EL SCHEME

Si el método anterior no funciona:

1. Cierra Xcode completamente
2. Abre el archivo del scheme:
   ```bash
   open /Users/alejandrocaceres/Desktop/appstore\ -\ zodia/zodiac_app/ios/Runner.xcodeproj/xcshareddata/xcschemes/Runner.xcscheme
   ```
3. Busca la sección `<LaunchAction>`
4. Agrega dentro de ella:
   ```xml
   <StoreKitConfigurationFileReference
      identifier = "../ZodiacStoreKitConfig.storekit">
   </StoreKitConfigurationFileReference>
   ```
5. Guarda y vuelve a abrir Xcode

---

## 📊 VERIFICAR PRODUCTOS EN EL SIMULADOR

Una vez que la app esté corriendo:

1. Deberías ver **3 botones** en la pantalla:
   - Test Cosmic ($6.99/month)
   - Test Stellar ($19.99/month)
   - Test Universe ($49.99 lifetime)

2. Click en cualquier botón

3. Debería aparecer la **StoreKit Payment Sheet**:
   - Mostrará el nombre del producto
   - Precio simulado
   - Botones: "Subscribe" y "Cancel"

4. Click en "Subscribe"

5. La compra se procesará **localmente** (sin cargos reales)

6. En los logs deberías ver:
   ```
   flutter: 📱 TEST: 🛒 Testing purchase for: tier1_subscription
   flutter: 📱 TEST: 📦 Found package: Cosmic Monthly
   flutter: 📱 TEST: 💰 Price: $6.99
   flutter: 📱 TEST: 🚀 Launching purchase flow...
   flutter: 📱 TEST: ✅ Purchase successful!
   ```

---

## ⚠️ TROUBLESHOOTING

### "Products not found" error persiste

**Solución 1:** Limpiar build
```bash
cd /Users/alejandrocaceres/Desktop/appstore\ -\ zodia/zodiac_app/ios
rm -rf build/
pod install
```

**Solución 2:** Reiniciar Xcode
1. Quit Xcode completamente (Cmd+Q)
2. Borrar DerivedData:
   ```bash
   rm -rf ~/Library/Developer/Xcode/DerivedData
   ```
3. Volver a abrir Xcode

**Solución 3:** Verificar Bundle ID
- En Xcode, ve a Runner → Signing & Capabilities
- Verifica que el Bundle ID sea: `com.zodiac.app.zodiacApp`

### StoreKit Configuration no aparece en el dropdown

1. Click derecho en la carpeta `ios/` en Xcode
2. Selecciona "Add Files to Runner..."
3. Navega a `ZodiacStoreKitConfig.storekit`
4. Asegúrate de marcar "Copy items if needed"
5. Click "Add"

---

## 🎉 ÉXITO CONFIRMADO

Sabrás que todo funciona cuando:

✅ Los 3 productos cargan correctamente
✅ Los precios se muestran ($6.99, $19.99, $49.99)
✅ Al hacer click aparece el StoreKit payment sheet
✅ Las compras simuladas se completan sin errores
✅ RevenueCat muestra "Active entitlements: [zodiac_premium_access]"

---

## 📱 SIGUIENTE PASO: PROBAR EN DISPOSITIVO REAL

Una vez que funcione en simulador:

1. Conecta tu iPhone
2. En Xcode, selecciona tu iPhone (en lugar del simulador)
3. Run desde Xcode
4. Las compras usarán **Sandbox mode** automáticamente
5. Podrás probar con usuarios sandbox de App Store Connect

---

**¿Listo para configurar?** Abre Xcode y sigue los pasos 1-5 ⬆️
