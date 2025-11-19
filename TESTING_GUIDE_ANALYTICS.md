# 🧪 Guía de Testing - Analytics Dashboard

**Fecha:** 13 de Noviembre 2025
**Propósito:** Verificar que el Analytics Dashboard refactorizado funciona correctamente

---

## ✅ Pre-requisitos

- ✅ Build compilado sin errores
- ✅ Traducciones generadas (`flutter gen-l10n`)
- ✅ Dependencias instaladas (`shimmer: ^3.0.0`)

---

## 🎯 Tests a Realizar

### **Test 1: Compilación y Navegación** ⏱️ 2 min

1. **Compilar la app**
   ```bash
   flutter run
   ```

2. **Navegar al Analytics Dashboard**
   - Ir a Home Screen
   - Tap en el botón de Analytics (si es premium)
   - O navegar desde el menú

3. **Verificar que carga sin crashes**
   - ✅ No debe haber errores en consola
   - ✅ La pantalla debe aparecer

---

### **Test 2: Loading State** ⏱️ 1 min

**Objetivo:** Verificar que el shimmer loading aparece mientras carga

**Pasos:**
1. Abrir Analytics Dashboard
2. Observar los primeros segundos

**Resultado esperado:**
- ✅ Debe mostrar 3 shimmer cards animadas
- ✅ Texto "Loading your cosmic insights..." (o traducido)
- ✅ Animación fluida

**Captura de pantalla:** `screenshots/analytics_loading_state.png`

---

### **Test 3: Success State con Datos** ⏱️ 3 min

**Objetivo:** Verificar que muestra datos correctamente

**Pasos:**
1. Esperar a que cargue completamente
2. Verificar cada sección

**Secciones a verificar:**

#### **Header Card**
- ✅ Ícono de gráfica
- ✅ "Your Cosmic Journey" (traducido)
- ✅ Número de lecturas totales
- ✅ Badge "Premium" si es usuario premium

#### **Reading Streak**
- ✅ Emoji 🔥
- ✅ "Reading Streak" (traducido)
- ✅ Subtítulo "All time" (traducido)
- ✅ Número de días
- ✅ Mensaje motivacional

#### **Weekly Activity Chart**
- ✅ Título "Weekly Activity" (traducido)
- ✅ Subtítulo "Last 7 days" (traducido)
- ✅ 7 barras del chart
- ✅ Etiquetas de días (Mon, Tue, etc. - traducidas)
- ✅ Gradiente azul/morado

#### **Quick Stats Grid (4 cards)**
- ✅ Compatibility checks (con número)
- ✅ Coach Sessions (con número)
- ✅ Favorite Feature (traducido - ej: "Daily Horoscope")
- ✅ Most Active Day (traducido - ej: "Monday")

#### **Goals Progress**
- ✅ Emoji 🎯
- ✅ Título traducido
- ✅ Porcentaje correcto
- ✅ Barra de progreso verde

#### **Premium Stats (solo si premium)**
- ✅ Emoji ⭐
- ✅ "Premium Features" traducido
- ✅ Cosmic Coach sessions
- ✅ Advanced Charts views
- ✅ Compatibility Pro checks

**Captura de pantalla:** `screenshots/analytics_success_state.png`

---

### **Test 4: Empty State** ⏱️ 2 min

**Objetivo:** Verificar empty state para usuarios nuevos

**Pasos:**
1. Crear usuario nuevo sin datos (o limpiar cache)
2. Abrir Analytics Dashboard

**Resultado esperado:**
- ✅ Ilustración cósmica (📊✨)
- ✅ Título: "No data yet" (traducido)
- ✅ Subtítulo motivacional
- ✅ 3 sugerencias:
  - 🌟 Read daily horoscope
  - 💑 Check compatibility
  - 💬 Chat with Cosmic Coach

**Captura de pantalla:** `screenshots/analytics_empty_state.png`

---

### **Test 5: Error State** ⏱️ 2 min

**Objetivo:** Verificar que el error state funciona

**Pasos:**
1. Simular error (desconectar internet o modificar provider temporalmente)
2. Abrir Analytics Dashboard

**Resultado esperado:**
- ✅ Ícono de error rojo
- ✅ Mensaje de error
- ✅ Botón "Retry" (traducido)
- ✅ Al hacer tap en Retry, intenta recargar

**Captura de pantalla:** `screenshots/analytics_error_state.png`

---

### **Test 6: Pull-to-Refresh** ⏱️ 1 min

**Objetivo:** Verificar que refresh funciona

**Pasos:**
1. En Success State, hacer pull-to-refresh
2. Observar comportamiento

**Resultado esperado:**
- ✅ Spinner de refresh aparece
- ✅ Datos se recargan
- ✅ No hay crashes

---

### **Test 7: Localización en 6 Idiomas** ⏱️ 10 min

**Objetivo:** Verificar traducciones completas

**Para cada idioma:**

#### **Inglés (EN)**
1. Cambiar idioma del dispositivo a English
2. Verificar:
   - ✅ "Daily Horoscope" (favorite feature)
   - ✅ "Monday" (most active day)
   - ✅ "Last 7 days" (subtitle)
   - ✅ "Mon, Tue, Wed..." (chart labels)

#### **Español (ES)**
1. Cambiar idioma a Español
2. Verificar:
   - ✅ "Horóscopo Diario"
   - ✅ "Lunes"
   - ✅ "Últimos 7 días"
   - ✅ "Lun, Mar, Mié..."

#### **Portugués (PT)**
1. Cambiar idioma a Português
2. Verificar:
   - ✅ "Horóscopo Diário"
   - ✅ "Segunda-feira"
   - ✅ "Últimos 7 dias"
   - ✅ "Seg, Ter, Qua..."

#### **Francés (FR)**
1. Cambiar idioma a Français
2. Verificar:
   - ✅ "Horoscope Quotidien"
   - ✅ "Lundi"
   - ✅ "7 derniers jours"
   - ✅ "Lun, Mar, Mer..."

#### **Alemán (DE)**
1. Cambiar idioma a Deutsch
2. Verificar:
   - ✅ "Tageshoroskop"
   - ✅ "Montag"
   - ✅ "Letzte 7 Tage"
   - ✅ "Mo, Di, Mi..."

#### **Italiano (IT)**
1. Cambiar idioma a Italiano
2. Verificar:
   - ✅ "Oroscopo Giornaliero"
   - ✅ "Lunedì"
   - ✅ "Ultimi 7 giorni"
   - ✅ "Lun, Mar, Mer..."

**Capturas:** Una por idioma en `screenshots/analytics_i18n_{locale}.png`

---

### **Test 8: Tema Claro/Oscuro** ⏱️ 2 min

**Objetivo:** Verificar contraste en ambos modos

#### **Modo Oscuro (Dark)**
1. Activar modo oscuro
2. Verificar Analytics Dashboard

**Resultado esperado:**
- ✅ Texto blanco visible
- ✅ Cards con gradientes semi-transparentes
- ✅ Bordes visibles
- ✅ Buen contraste

#### **Modo Claro (Light)**
1. Activar modo claro
2. Verificar Analytics Dashboard

**Resultado esperado:**
- ✅ Texto oscuro visible
- ✅ Cards distinguibles del fondo
- ✅ Bordes visibles
- ✅ Buen contraste

**Capturas:** `screenshots/analytics_dark_mode.png` y `analytics_light_mode.png`

---

### **Test 9: Premium vs Free** ⏱️ 3 min

**Objetivo:** Verificar comportamiento según tier

#### **Usuario Free**
1. Asegurarse de no tener premium
2. Abrir Analytics Dashboard

**Resultado esperado:**
- ✅ NO debe mostrar badge "Premium"
- ✅ NO debe mostrar sección "Premium Features"
- ✅ Resto de stats se muestran normalmente

#### **Usuario Premium**
1. Activar premium
2. Abrir Analytics Dashboard

**Resultado esperado:**
- ✅ Badge "Premium" en header
- ✅ Sección "Premium Features" visible
- ✅ Stats de premium features con números

**Capturas:** `screenshots/analytics_free.png` y `analytics_premium.png`

---

### **Test 10: Performance** ⏱️ 2 min

**Objetivo:** Verificar que no hay lag

**Pasos:**
1. Abrir Dashboard
2. Scroll arriba/abajo varias veces
3. Hacer pull-to-refresh
4. Navegar a otras pantallas y volver

**Resultado esperado:**
- ✅ Scroll fluido (60fps)
- ✅ Sin stuttering
- ✅ Animaciones suaves
- ✅ Transiciones rápidas

---

## 🐛 Issues Conocidos

### **Advertencias de Compilación**
```
info • Angle brackets in doc comment (2 warnings)
```
**Impacto:** Ninguno - solo warnings de documentación
**Fix:** Opcional - reemplazar `<` con `&lt;` en comentarios

---

## 📊 Checklist de Verificación

### **Funcionalidad Core**
- [ ] Compila sin errores
- [ ] Loading state funciona
- [ ] Success state muestra datos
- [ ] Empty state aparece cuando no hay datos
- [ ] Error state con retry funciona
- [ ] Pull-to-refresh recarga datos

### **Localización**
- [ ] Inglés (EN) - todos los textos
- [ ] Español (ES) - todos los textos
- [ ] Portugués (PT) - todos los textos
- [ ] Francés (FR) - todos los textos
- [ ] Alemán (DE) - todos los textos
- [ ] Italiano (IT) - todos los textos

### **Valores Dinámicos Localizados**
- [ ] Favorite feature traducida
- [ ] Most active day traducido
- [ ] Días de la semana traducidos
- [ ] Time periods traducidos

### **Visual/UX**
- [ ] Modo oscuro con buen contraste
- [ ] Modo claro con buen contraste
- [ ] Shimmer animation fluida
- [ ] Gradientes consistentes
- [ ] Spacing correcto
- [ ] Icons alineados

### **Premium/Free**
- [ ] Free: No badge, no premium section
- [ ] Premium: Badge visible, premium section visible
- [ ] Premium stats muestran números

### **Performance**
- [ ] Scroll fluido
- [ ] Sin memory leaks
- [ ] Transiciones suaves
- [ ] Refresh rápido

---

## 📝 Reportar Issues

Si encuentras algún problema, reporta con:

1. **Descripción:** Qué esperabas vs qué pasó
2. **Pasos:** Cómo reproducir
3. **Screenshot:** Captura del problema
4. **Dispositivo:** iPhone/iPad modelo
5. **iOS Version:** Versión de iOS
6. **Idioma:** En qué idioma ocurrió
7. **Premium:** Usuario premium o free

**Formato:**
```markdown
### Issue: [Título corto]

**Descripción:**
[Descripción detallada]

**Pasos para reproducir:**
1. Paso 1
2. Paso 2
3. Paso 3

**Resultado esperado:**
[Qué debería pasar]

**Resultado actual:**
[Qué pasó realmente]

**Screenshot:**
[Adjuntar imagen]

**Entorno:**
- Dispositivo: iPhone 15 Pro
- iOS: 17.2
- Idioma: Español
- Premium: Sí
```

---

## 🚀 Quick Test Script

Para testing rápido, usa este orden:

```bash
# 1. Compilar
flutter run

# 2. Test básico (5 min)
- Abrir Analytics
- Verificar que carga
- Verificar datos se muestran
- Pull-to-refresh

# 3. Test idiomas (3 idiomas - 5 min)
- EN: Verificar textos
- ES: Verificar textos
- PT: Verificar textos

# 4. Test premium/free (2 min)
- Desactivar premium → verificar
- Activar premium → verificar

# 5. Test modos (2 min)
- Dark mode → verificar contraste
- Light mode → verificar contraste

Total: ~15 min para test completo básico
```

---

## ✅ Testing Completado

**Fecha:** _______________
**Testeado por:** _______________
**Resultado:** [ ] Todos los tests pasaron  [ ] Issues encontrados

**Notas:**
_______________________________________________________
_______________________________________________________
_______________________________________________________

---

**Próximo paso:** Después de testing, documentar cualquier ajuste necesario
