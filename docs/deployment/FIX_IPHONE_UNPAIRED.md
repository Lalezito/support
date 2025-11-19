# 🔧 FIX: iPhone Unpaired - Cómo Emparejar

## ❌ PROBLEMA DETECTADO

```
Error: Alejandro Caceres's iPhone is not available because it is unpaired.
Pair with the device in the Xcode Devices Window, and respond to any pairing prompts on the device. (code -29)
```

**Tu iPhone está conectado por USB pero NO está emparejado (paired) con la Mac.**

---

## ✅ SOLUCIÓN: Emparejar el iPhone con Xcode

### Opción 1: Usando Xcode (MÁS FÁCIL)

#### Paso 1: Abrir Xcode Devices Window
```bash
# Abre Xcode y luego:
# Window → Devices and Simulators
# O usa el atajo: Shift + Cmd + 2
open -a Xcode
```

#### Paso 2: Emparejar el Dispositivo
1. En Xcode, ve a **Window → Devices and Simulators** (o `Shift + Cmd + 2`)
2. Verás tu iPhone en la lista de la izquierda
3. Si tiene un **⚠️ warning** o está en **gris**, haz clic en él
4. Verás un botón **"Connect via Network"** o **"Use for Development"**
5. Haz clic en ese botón

#### Paso 3: Trust en el iPhone
En tu **iPhone** aparecerá:
```
"Trust This Computer?"
[Don't Trust] [Trust]
```
1. Toca **"Trust"**
2. Ingresa tu **passcode** del iPhone
3. Espera 10-15 segundos

#### Paso 4: Verificar
En Xcode Devices, deberías ver:
- **Estado**: Connected (punto verde ●)
- **Información del dispositivo** visible

---

### Opción 2: Usando Terminal (ALTERNATIVA)

Si no quieres abrir Xcode, puedes intentar re-pair con estos comandos:

```bash
# 1. Verificar que idevicepair esté instalado
brew list libimobiledevice || brew install libimobiledevice

# 2. Listar dispositivos USB
idevice_id -l

# 3. Verificar estado de pairing
idevicepair validate

# 4. Si dice "not paired", hacer pairing
idevicepair pair
```

**Importante**: En el paso 4, cuando ejecutes `idevicepair pair`, debes:
1. Mantener el iPhone **desbloqueado**
2. Responder **"Trust"** cuando aparezca el prompt
3. Ingresar tu **passcode**

---

### Opción 3: Reset Completo del Pairing

Si las opciones anteriores no funcionan:

```bash
# 1. Unpair completamente
idevicepair unpair

# 2. Eliminar lockdown folder (requiere contraseña)
sudo rm -rf /var/db/lockdown/*

# 3. Desconectar y reconectar el cable USB

# 4. Volver a hacer pair
idevicepair pair
```

---

## 🔍 VERIFICAR QUE FUNCIONÓ

Después de hacer el pairing:

```bash
# Ver dispositivos conectados
flutter devices

# Deberías ver:
✅ Alejandro Caceres's iPhone (mobile) • 00008150-0015244A2288401C • ios • iOS 26.0.1
```

Si ya NO ves el error "unpaired", ¡funcionó!

---

## 🚀 PROBAR DEPLOYMENT

Una vez emparejado:

```bash
cd /Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app

# Probar deployment
flutter run -d 00008150-0015244A2288401C --debug
```

**Durante el deployment**:
- ✅ Mantén el iPhone **desbloqueado**
- ✅ Mantén la pantalla **activa** (no dejes que entre en sleep)
- ⏱️ Toma ~2-3 minutos la primera vez

---

## 💡 POR QUÉ PASÓ ESTO

El iPhone se "unpair" cuando:
1. Tocaste "Don't Trust" por accidente
2. El iPhone se reinició
3. Actualizaste iOS
4. Restauraste el iPhone
5. Cambiaste de cable USB (a veces)

---

## ⚠️ NOTAS IMPORTANTES

### Para Evitar Este Error en el Futuro:
- Siempre responde **"Trust"** cuando conectes el iPhone
- No cambies de cable USB durante el desarrollo
- Si actualizas iOS, espera que tengas que re-trust

### Si Sigue sin Funcionar:
1. Reinicia el iPhone (Power + Volume Down)
2. Reinicia la Mac
3. Usa un cable Apple original (algunos genéricos causan problemas)
4. Verifica que el puerto USB de la Mac esté limpio

---

## 📱 COMANDO RÁPIDO - TODO EN UNO

Ejecuta esto para intentar arreglar automáticamente:

```bash
# Fix completo
pkill Xcode && \
idevicepair unpair ; \
idevicepair pair && \
sleep 3 && \
flutter devices
```

Luego:
1. **Desbloquea** el iPhone
2. Toca **"Trust This Computer?"**
3. Ingresa tu **passcode**
4. Espera que aparezca en `flutter devices`

---

## ✅ RESUMEN

**Problema**: iPhone unpaired (código -29)

**Solución rápida**:
1. Abre **Xcode** → Window → Devices and Simulators
2. Haz clic en tu iPhone
3. Click **"Use for Development"**
4. En el iPhone: toca **"Trust"** e ingresa passcode
5. Espera 10 segundos
6. Verifica con `flutter devices`

**Tiempo**: 1-2 minutos

---

**Generado**: Octubre 15, 2025
**Error Code**: -29 (unpaired)
**Dispositivo**: Alejandro Caceres's iPhone (00008150-0015244A2288401C)
