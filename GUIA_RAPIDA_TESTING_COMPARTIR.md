# 🧪 Guía Rápida: Cómo Probar Botones de Compartir

**App**: Zodiac Life Coach
**Feature**: Compartir en Redes Sociales
**Tiempo estimado**: 5 minutos

---

## 📍 Paso 1: Navegar a un Horóscopo

1. Abre la app
2. Selecciona tu signo zodiacal (si no lo has hecho)
3. Ve a la pantalla de horóscopo diario
4. Busca el **botón de compartir** (ícono de compartir)

---

## 🧪 Paso 2: Probar Cada Botón

### 📸 Instagram

**¿Qué probar?**:
- [ ] Toca el botón de Instagram
- [ ] ¿Se abre el share sheet de iOS?
- [ ] ¿Ves la imagen del horóscopo en la preview?
- [ ] ¿Instagram aparece en las opciones?

**✅ ÉXITO si**: Share sheet se abre con imagen
**⚠️ OK si**: Necesitas seleccionar Instagram manualmente
**❌ PROBLEMA si**: No pasa nada al tocar el botón

---

### 💬 WhatsApp

**¿Qué probar?**:
- [ ] Toca el botón de WhatsApp
- [ ] Si tienes WhatsApp: ¿Se abre el share sheet?
- [ ] Si NO tienes WhatsApp: ¿Mensaje de error en español?

**✅ ÉXITO si**: Share sheet se abre O mensaje claro de error
**❌ PROBLEMA si**: No pasa nada al tocar el botón

---

### 📘 Facebook

**¿Qué probar?**:
- [ ] Toca el botón de Facebook
- [ ] ¿Se abre el share sheet?
- [ ] ¿Ves Facebook en las opciones?

**✅ ÉXITO si**: Share sheet se abre con imagen
**❌ PROBLEMA si**: No pasa nada

---

### 🐦 Twitter/X

**¿Qué probar?**:
- [ ] Toca el botón de Twitter
- [ ] Si tienes Twitter: ¿Se abre share sheet?
- [ ] Si NO tienes Twitter: ¿Se abre navegador web?

**✅ ÉXITO si**: Share sheet O navegador web se abre
**❌ PROBLEMA si**: No pasa nada

---

### ✈️ Telegram

**¿Qué probar?**:
- [ ] Toca el botón de Telegram
- [ ] Si tienes Telegram: ¿Se abre share sheet?
- [ ] Si NO tienes Telegram: ¿Mensaje de error?

**✅ ÉXITO si**: Share sheet se abre O error claro
**❌ PROBLEMA si**: No pasa nada

---

## 🧪 Paso 3: Probar Cancelar

**¿Qué probar?**:
- [ ] Abre share sheet (cualquier botón)
- [ ] Toca "Cancelar" o cierra el sheet
- [ ] ¿Ves algún mensaje de error?

**✅ ÉXITO si**: NO ves ningún error (cancelar es normal)
**❌ PROBLEMA si**: Aparece mensaje de error al cancelar

---

## 📊 Cómo Reportar Resultados

### Si TODO Funciona ✅

Simplemente di:
> "✅ Todo funciona - share sheet se abre en todos"

### Si Algo NO Funciona ❌

Dime **específicamente**:
1. **Qué botón** (Instagram, WhatsApp, etc.)
2. **Qué pasó** (nada, error, crash, etc.)
3. **Qué esperabas** que pasara

**Ejemplo**:
> "❌ WhatsApp - Toco el botón y no pasa nada"
> "⚠️ Instagram - Share sheet se abre pero no veo la imagen"

---

## 🎯 Resultados Esperados

### ✅ Comportamiento CORRECTO

- Share sheet se abre en todos los botones
- Imagen del horóscopo aparece en preview
- Puedes seleccionar app de la lista
- Si app no instalada: mensaje en español
- Si cancelas: NO aparece error

### ⚠️ Limitaciones Conocidas (NORMALES)

- Instagram/WhatsApp pueden no aceptar imagen+texto perfectamente (limitación de Meta)
- Puede que tengas que seleccionar app manualmente del sheet (esto es normal en iOS)
- Share sheet puede mostrar muchas opciones (comportamiento estándar)

### ❌ Comportamiento INCORRECTO

- No pasa nada al tocar botón
- App se crashea
- Error aparece al cancelar
- Share sheet no muestra imagen

---

## ⏱️ Tiempo de Testing

- **Testing básico**: 2-3 minutos (probar cada botón una vez)
- **Testing completo**: 5 minutos (probar todos los escenarios)

---

## 📝 Plantilla de Reporte Rápido

```
Instagram: ✅ / ⚠️ / ❌ - [comentario]
WhatsApp: ✅ / ⚠️ / ❌ - [comentario]
Facebook: ✅ / ⚠️ / ❌ - [comentario]
Twitter: ✅ / ⚠️ / ❌ - [comentario]
Telegram: ✅ / ⚠️ / ❌ - [comentario]
Cancelar: ✅ / ❌ - [comentario]
```

**Ejemplo de reporte**:
```
Instagram: ✅ - Share sheet funciona perfecto
WhatsApp: ✅ - Se abre correctamente
Facebook: ⚠️ - Sheet se abre pero no veo imagen clara
Twitter: ✅ - Abre web (no tengo app)
Telegram: ❌ - No pasa nada al tocar botón
Cancelar: ✅ - No muestra error
```

---

🎯 **¡Prueba y me cuentas qué tal!**
