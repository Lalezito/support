# 📱 INSTRUCCIONES: Crear Unidades de Anuncios en AdMob

## 🔴 PROBLEMA ACTUAL

Tu cuenta de AdMob muestra:
- **Banner**: 0 activos, 0 habilitados
- **Intersticial**: 0 activos, 0 habilitados

**Esto significa que NO tienes unidades de anuncios creadas.**

---

## ✅ SOLUCIÓN: Crear 3 Unidades de Anuncios

### Paso 1: Ir a AdMob Console

1. Abre [AdMob Console](https://apps.admob.com/)
2. Inicia sesión con la cuenta: Tu cuenta de Google asociada
3. Selecciona tu app "Zodiac Life Coach" (o como se llame)

---

### Paso 2: Crear Unidad de Anuncios BANNER

1. Click en **"Unidades de anuncios"** en el menú lateral
2. Click en **"Agregar unidad de anuncios"**
3. Selecciona **"Banner"**
4. Configura:
   - **Nombre:** `Zodiac App - Banner Principal`
   - **Formato:** Banner (320x50)
   - **Plataforma:** iOS y Android
5. Click **"Crear unidad de anuncios"**
6. **COPIA el ID que te da** (ej: `ca-app-pub-XXXXX/YYYYY`)

---

### Paso 3: Crear Unidad de Anuncios INTERSTICIAL

1. Click **"Agregar unidad de anuncios"** nuevamente
2. Selecciona **"Intersticial"**
3. Configura:
   - **Nombre:** `Zodiac App - Intersticial`
   - **Formato:** Intersticial
   - **Plataforma:** iOS y Android
4. Click **"Crear unidad de anuncios"**
5. **COPIA el ID que te da**

---

### Paso 4: Crear Unidad de Anuncios CON RECOMPENSA

1. Click **"Agregar unidad de anuncios"** nuevamente
2. Selecciona **"Con recompensa"** (Rewarded)
3. Configura:
   - **Nombre:** `Zodiac App - Con Recompensa`
   - **Formato:** Con recompensa
   - **Plataforma:** iOS y Android
4. Click **"Crear unidad de anuncios"**
5. **COPIA el ID que te da**

---

## 📋 DESPUÉS DE CREAR LAS UNIDADES

Tendrás 3 IDs nuevos, algo así:

```
Banner ID:       ca-app-pub-4441524618400998/XXXXXXXXXX
Intersticial ID: ca-app-pub-4441524618400998/YYYYYYYYYY
Recompensa ID:   ca-app-pub-4441524618400998/ZZZZZZZZZZ
```

---

## 🔧 ACTUALIZAR IDs EN EL CÓDIGO

### Archivo 1: `lib/services/ad_service.dart`

```dart
// Líneas 15-28 - REEMPLAZAR con tus nuevos IDs
static final String _bannerAdUnitId =
    Platform.isIOS
        ? 'ca-app-pub-4441524618400998/XXXXXXXXXX' // ← TU NUEVO BANNER ID iOS
        : 'ca-app-pub-4441524618400998/XXXXXXXXXX'; // ← TU NUEVO BANNER ID Android

static final String _interstitialAdUnitId =
    Platform.isIOS
        ? 'ca-app-pub-4441524618400998/YYYYYYYYYY' // ← TU NUEVO INTERSTICIAL ID iOS
        : 'ca-app-pub-4441524618400998/YYYYYYYYYY'; // ← TU NUEVO INTERSTICIAL ID Android

static final String _rewardedAdUnitId =
    Platform.isIOS
        ? 'ca-app-pub-4441524618400998/ZZZZZZZZZZ' // ← TU NUEVO RECOMPENSA ID iOS
        : 'ca-app-pub-4441524618400998/ZZZZZZZZZZ'; // ← TU NUEVO RECOMPENSA ID Android
```

### Archivo 2: `lib/widgets/monetization/ad_banner_widget_real.dart`

```dart
// Líneas 55-58 - USAR EL MISMO ID DE BANNER
final String adUnitId =
    Platform.isIOS
        ? 'ca-app-pub-4441524618400998/XXXXXXXXXX' // ← MISMO BANNER ID que arriba
        : 'ca-app-pub-4441524618400998/XXXXXXXXXX'; // ← MISMO BANNER ID que arriba
```

---

## 🎯 IDs SEPARADOS PARA iOS Y ANDROID (Opcional)

Si quieres trackear iOS y Android por separado, puedes crear **6 unidades** (3 para iOS, 3 para Android):

### iOS:
- Banner iOS: `ca-app-pub-XXX/111111`
- Intersticial iOS: `ca-app-pub-XXX/222222`
- Recompensa iOS: `ca-app-pub-XXX/333333`

### Android:
- Banner Android: `ca-app-pub-XXX/444444`
- Intersticial Android: `ca-app-pub-XXX/555555`
- Recompensa Android: `ca-app-pub-XXX/666666`

Y actualizar el código:
```dart
static final String _bannerAdUnitId =
    Platform.isIOS
        ? 'ca-app-pub-XXX/111111' // iOS específico
        : 'ca-app-pub-XXX/444444'; // Android específico
```

---

## ⚠️ IMPORTANTE: IDs de PRUEBA vs PRODUCCIÓN

### Para DESARROLLO (usar IDs de prueba de Google):

```dart
// IDs de PRUEBA - NO cobran, siempre muestran ads
static final String _bannerAdUnitId =
    Platform.isIOS
        ? 'ca-app-pub-3940256099942544/2934735716' // Test Banner iOS
        : 'ca-app-pub-3940256099942544/6300978111'; // Test Banner Android

static final String _interstitialAdUnitId =
    Platform.isIOS
        ? 'ca-app-pub-3940256099942544/4411468910' // Test Intersticial iOS
        : 'ca-app-pub-3940256099942544/1033173712'; // Test Intersticial Android

static final String _rewardedAdUnitId =
    Platform.isIOS
        ? 'ca-app-pub-3940256099942544/1712485313' // Test Rewarded iOS
        : 'ca-app-pub-3940256099942544/5224354917'; // Test Rewarded Android
```

### Para PRODUCCIÓN (tus IDs reales):

Usar los IDs que copiaste de AdMob Console.

---

## 🧪 TESTING PASO A PASO

### 1. Probar con IDs de Prueba Primero

```bash
# Actualizar código con IDs de prueba
# Correr en release mode
flutter clean
flutter pub get
flutter run --release

# Deberías ver ads de prueba inmediatamente
```

### 2. Probar con IDs Reales

```bash
# Actualizar código con tus IDs reales de AdMob
# Correr en release mode
flutter clean
flutter pub get
flutter run --release

# Los ads pueden tardar:
# - 30-60 segundos en aparecer
# - 24-48 horas si la app aún no está aprobada en AdMob
```

---

## 📊 VERIFICAR QUE FUNCIONA

### Logs Esperados:

```
✅ Ad services initialized
✅ Ads precargados: Banner, Interstitial, Rewarded
AdService: Attempting to load banner ad (attempt 1/3)
AdService: Banner ad REAL cargado exitosamente
```

### En la App:

1. Abre HomeScreen
2. Espera 30-60 segundos
3. Deberías ver un banner en la parte inferior
4. El banner debe decir "Anuncio" o "Ad" en la esquina

---

## ❓ TROUBLESHOOTING

### No aparecen ads después de 1 minuto:

1. **Verificar logs:**
   ```bash
   flutter logs | grep -i "ad"
   ```

2. **Errores comunes:**
   - `NO_FILL` = No hay ads disponibles en tu región
   - `NETWORK_ERROR` = Problemas de internet
   - `INVALID_REQUEST` = ID de unidad incorrecto

3. **Soluciones:**
   - Usar IDs de prueba primero para verificar que funciona
   - Esperar 24-48h para aprobación de AdMob
   - Probar con VPN a US/UK si estás en región con pocos ads

---

## ✅ CHECKLIST FINAL

- [ ] Crear 3 unidades de anuncios en AdMob Console
- [ ] Copiar los 3 IDs nuevos
- [ ] Actualizar `ad_service.dart` con los nuevos IDs
- [ ] Actualizar `ad_banner_widget_real.dart` con el mismo Banner ID
- [ ] Probar primero con IDs de prueba de Google
- [ ] Probar con tus IDs reales después
- [ ] Verificar logs con `flutter logs | grep -i "ad"`
- [ ] Esperar 30-60 segundos para ver el primer ad

---

**Tiempo Estimado:** 10-15 minutos para crear unidades
**Aprobación AdMob:** 24-48 horas para app nueva
**Testing inmediato:** Usar IDs de prueba de Google
