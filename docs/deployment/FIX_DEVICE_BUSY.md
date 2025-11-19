# 📱 FIX: "Device is busy" Error

## ❌ Problema
```
Error: Device is busy (Waiting to reconnect to Alejandro Caceres's iPhone)
```

## ✅ SOLUCIONES (En orden de más simple a más complejo)

### Solución 1: Desbloquear y Confiar en la Mac (MÁS COMÚN)
```bash
1. Desbloquea tu iPhone (Face ID / Touch ID / Passcode)
2. Verás popup: "Trust This Computer?"
3. Toca "Trust"
4. Ingresa tu passcode del iPhone
5. Espera 10 segundos
```

### Solución 2: Reconectar Cable
```bash
1. Desconecta el cable Lightning/USB-C del iPhone
2. Espera 5 segundos
3. Reconecta el cable
4. Desbloquea el iPhone
5. Verifica con: flutter devices
```

### Solución 3: Cerrar Apps que Usan el Dispositivo
```bash
# Cerrar Xcode si está abierto
pkill Xcode

# Cerrar cualquier simulador
killall Simulator

# Verificar dispositivo
flutter devices
```

### Solución 4: Reiniciar usbmuxd (Servicio de comunicación iOS)
```bash
# Reiniciar el daemon de comunicación iOS-Mac
sudo pkill usbmuxd

# Se reinicia automáticamente
sleep 3

# Verificar conexión
flutter devices
```

### Solución 5: Limpiar DerivedData de Xcode
```bash
# Eliminar cache de Xcode
rm -rf ~/Library/Developer/Xcode/DerivedData/*

# Limpiar proyecto Flutter
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app
flutter clean
```

### Solución 6: Reiniciar Dispositivos
```bash
1. Reinicia tu iPhone (mantén Power + Volume Down)
2. O reinicia la Mac (si todo lo demás falla)
```

## 🔍 VERIFICACIÓN

Después de aplicar cualquier solución, verifica:

```bash
# Ver dispositivos conectados
flutter devices

# Deberías ver:
✅ Alejandro Caceres's iPhone (mobile) • 00008150-0015244A2288401C • ios • iOS 26.0.1
```

## 🚀 REINTENTAR DEPLOYMENT

Una vez solucionado:

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Opción A: Test app de compras
flutter run -d 00008150-0015244A2288401C test_purchases_real_device.dart --release

# Opción B: App principal
flutter run -d 00008150-0015244A2288401C --release
```

## 💡 TIPS

### Para Evitar Este Error
1. **Siempre desbloquea** el iPhone antes de compilar
2. **Mantén el cable conectado** durante toda la compilación
3. **No uses Xcode y Flutter simultáneamente** en el mismo dispositivo
4. **Trust the computer** la primera vez que conectes

### Identificar si el Device Está Listo
```bash
# Si ves esto, está listo:
Found 3 connected devices:
  Alejandro Caceres's iPhone (mobile) ✅

# Si ves esto, NO está listo:
  Alejandro Caceres's iPhone (mobile) (busy)
  Alejandro Caceres's iPhone (mobile) (unavailable)
```

## 🐛 DEBUGGING ADICIONAL

Si nada funciona, corre diagnóstico completo:

```bash
# Ver logs detallados del dispositivo
idevicesyslog

# Ver información del dispositivo
ideviceinfo

# Ver pair record
idevicepair validate

# Re-pair si es necesario
idevicepair unpair
idevicepair pair
```

## ⚡ COMANDO RÁPIDO

Ejecuta esto para solucionar la mayoría de casos:

```bash
# Fix rápido (combina las soluciones más comunes)
sudo pkill usbmuxd && sleep 3 && flutter devices
```

Luego:
1. Desbloquea tu iPhone
2. Trust this computer si aparece el prompt
3. Espera 10 segundos
4. Reintenta el deployment

---

**Generado**: Octubre 15, 2025
**Error**: Device is busy
**Dispositivo**: Alejandro Caceres's iPhone (00008150-0015244A2288401C)
