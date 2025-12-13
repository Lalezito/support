# 🧪 Guía de Prueba - Nuevo Diseño de Tarjetas

**Fecha**: 2 de noviembre de 2025
**Versión**: 1.0 - Diseño Galaxia Elegante

---

## 📱 Pasos para Probar el Nuevo Diseño

### 1. Abrir la App
- ✅ La app debería lanzarse normalmente en tu iPhone
- ✅ Verificar que no haya errores de compilación

### 2. Navegar a un Horóscopo
```
1. En la pantalla principal
2. Seleccionar cualquier signo zodiacal (ej: Aries, Leo, Géminis)
3. Ver el horóscopo diario
```

### 3. Abrir el Botón de Compartir
```
1. En la pantalla del horóscopo
2. Buscar el botón de compartir (ícono de "share" ↗️)
3. Tocar el botón
```

### 4. Ver el Modal de Compartir
```
Debería aparecer un modal con opciones:
- Instagram
- Facebook
- WhatsApp
- Twitter
- Telegram
- Compartir general
```

### 5. Generar la Tarjeta
```
1. Seleccionar cualquier opción (ej: Instagram)
2. La app generará la tarjeta de horóscopo
3. Debería aparecer el share sheet de iOS
```

---

## ✅ Qué Verificar en la Tarjeta Generada

### Diseño General
- [ ] Fondo oscuro con degradado vino/marrón/púrpura
- [ ] No se ve pixelado o borroso
- [ ] Tamaño correcto (landscape 16:9)

### Tipografía
- [ ] **"HORÓSCOPO"** aparece en mayúsculas serif elegante (Playfair Display)
- [ ] **"ARIES"** (o tu signo) aparece en fuente manuscrita elegante (Dancing Script)
- [ ] **Texto del horóscopo** aparece en fuente serif clásica (Cormorant Garamond)
- [ ] **Fecha** aparece en cursiva: "del [día] de [mes] al [día] de [mes]"

### Caja de Texto
- [ ] Hay una caja semitransparente oscura alrededor del texto
- [ ] El texto se lee claramente (buen contraste)
- [ ] Los bordes están redondeados
- [ ] Hay un borde sutil blanco

### Decoraciones
- [ ] Líneas curvas blancas sutiles en las esquinas (órbitas)
- [ ] Pequeños círculos de colores pastel (planetas)
- [ ] Estrellas muy sutiles en el fondo
- [ ] Indicador de carrusel (3 puntos) en la parte inferior

### Branding
- [ ] "Zodiac Life Coach" aparece en la parte inferior
- [ ] "zodiaclifecoach.app" aparece debajo

---

## 🎨 Comparación Visual

### ANTES (Diseño Anterior)
```
- Fondo púrpura genérico
- Fuente sans-serif simple
- Muchas decoraciones brillantes
- Texto difícil de leer
```

### DESPUÉS (Nuevo Diseño)
```
✅ Fondo galaxia vino/marrón/púrpura
✅ Fuentes elegantes serif + manuscrita
✅ Decoraciones sutiles y sofisticadas
✅ Caja semitransparente para legibilidad
✅ Fecha formateada elegantemente
✅ Indicador de carrusel
```

---

## 🐛 Posibles Problemas y Soluciones

### Problema 1: Fuentes no se ven elegantes
**Causa**: Google Fonts no cargó
**Solución**:
- Verificar conexión a internet
- Las fuentes deberían cargar automáticamente
- Si no, el sistema usará fuentes serif del sistema

### Problema 2: Texto muy largo se sale de la caja
**Solución**: La caja tiene scroll interno, deslizar hacia abajo

### Problema 3: No se ve la tarjeta
**Causa**: Error en generación de imagen
**Solución**: Revisar logs de consola

### Problema 4: Decoraciones muy visibles
**Solución**: Es normal, están diseñadas para ser sutiles pero visibles

---

## 📸 Screenshots Recomendados

Toma screenshots de:
1. Tarjeta generada completa
2. Detalle de la tipografía del título
3. Detalle de la caja de texto
4. Decoraciones en las esquinas
5. Share sheet mostrando la imagen

---

## 🚀 Próximos Pasos Después de Probar

### Si el diseño se ve BIEN ✅
1. Compartir en redes sociales reales
2. Ver cómo se ve en Instagram/Facebook
3. Ajustar tamaños de fuente si es necesario

### Si hay problemas ❌
1. Reportar qué no se ve bien
2. Tomar screenshots
3. Ajustar colores/tamaños según feedback

---

## 💡 Tips de Uso

- **Para mejor resultado**: Usa horóscopos con texto mediano (no muy largo)
- **Compartir en Instagram**: Selecciona "Instagram" del modal
- **Compartir en Stories**: Usa la opción de Instagram Stories
- **Guardar imagen**: Usa "Guardar imagen" del share sheet

---

## 🎯 Checklist Final

- [ ] App se ejecuta sin errores
- [ ] Botón de compartir funciona
- [ ] Tarjeta se genera correctamente
- [ ] Fuentes elegantes se ven bien
- [ ] Caja semitransparente tiene buen contraste
- [ ] Decoraciones son sutiles pero visibles
- [ ] Fecha formateada correctamente en español
- [ ] Share sheet muestra la imagen
- [ ] Imagen se puede compartir en redes sociales

---

¡Listo para probar! 🚀

**Recuerda**: Este es el diseño "galaxia elegante" inspirado en diseños de revista.
Debería verse profesional y sofisticado. ✨
