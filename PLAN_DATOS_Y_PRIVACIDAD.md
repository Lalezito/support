# Plan de Implementación: Datos y Privacidad

## 📊 Estado Actual de las 4 Funcionalidades

| Funcionalidad | Estado | Calificación |
|---------------|--------|--------------|
| **1. Backup de Datos** | Parcial | 🟡 60% |
| **2. Política de Privacidad** | Funcional | 🟢 90% |
| **3. Términos y Condiciones** | Funcional | 🟢 90% |
| **4. Limpieza de Datos** | Funcional | 🟢 95% |

---

## 1. 📦 BACKUP DE DATOS

### Estado Actual
- **Ubicación**: `settings_screen.dart` líneas 1391-1477
- **Funcionalidad**: Muestra un diálogo informativo + botón "Exportar"
- **Exportación**: Solo muestra los datos en un diálogo, NO genera archivo

### Problemas Detectados
1. ❌ **No hay backup real a la nube** - El texto dice "guardar en la nube" pero no lo hace
2. ❌ **No hay exportación a archivo** - Solo muestra datos en pantalla
3. ❌ **No hay función de restauración/importación**
4. ❌ **El botón "Exportar" solo muestra otro diálogo informativo**

### Mejoras a Implementar

#### A. Exportación Real a Archivo
```dart
// Agregar funcionalidad para exportar a JSON
- Crear archivo JSON con todos los datos del usuario
- Compartir via Share Sheet de iOS
- Incluir: zodiac sign, birth date, ascendant, preferences, goals, journal
```

#### B. Importación/Restauración
```dart
// Agregar funcionalidad para importar backup
- Leer archivo JSON de backup
- Restaurar preferencias y datos
- Validar formato antes de importar
```

#### C. Actualizar Textos
- Cambiar "Save to cloud" por "Export to file" (más preciso)
- O implementar backup real a la nube (más complejo)

### Archivos a Modificar
- [settings_screen.dart](zodiac_app/lib/screens/settings_screen.dart) - Líneas 1391-1478, 1716-1810
- [preferences_service.dart](zodiac_app/lib/services/preferences_service.dart) - Agregar métodos import/export
- Traducciones en `app_*.arb`

---

## 2. 🔒 POLÍTICA DE PRIVACIDAD

### Estado Actual
- **Ubicación Settings**: `settings_screen.dart` líneas 1480-1605
- **Pantalla Completa**: `terms_and_privacy_screen.dart` - `PrivacyPolicyDetailScreen`
- **Funcionalidad**: ✅ Muestra diálogo con información + pantalla detallada

### Lo que Funciona Bien
- ✅ Diálogo informativo con datos que se recopilan
- ✅ Sección "Cómo protegemos tus datos"
- ✅ Pantalla detallada completa (5 secciones)
- ✅ Información de contacto

### Mejoras Menores Sugeridas
1. 🔧 **Agregar botón para ver política completa** en el diálogo
2. 🔧 **Actualizar fecha** de "August 26, 2025" a fecha actual si es necesario
3. 🔧 **Traducir textos hardcodeados** en `PrivacyPolicyDetailScreen`

### Archivos a Modificar
- [terms_and_privacy_screen.dart](zodiac_app/lib/screens/terms_and_privacy_screen.dart) - Líneas 462-536

---

## 3. 📋 TÉRMINOS Y CONDICIONES

### Estado Actual
- **Ubicación Settings**: Navega a `/terms-and-privacy`
- **Pantalla Principal**: `terms_and_privacy_screen.dart` - `TermsAndPrivacyScreen`
- **EULA Completo**: `EULADetailScreen` con 14 secciones

### Lo que Funciona Bien
- ✅ Pantalla completa con info de suscripciones
- ✅ EULA detallado (14 secciones legales)
- ✅ Links a soporte y gestión de suscripciones
- ✅ Cumple con App Store Guidelines 3.1.2

### Mejoras Menores Sugeridas
1. 🔧 **Traducir textos hardcodeados** - Los diálogos de soporte están en español hardcodeado
2. 🔧 **Precio inconsistente** - EULA dice $7.99/mes pero subscriptionInfo dice $4.99/mes
3. 🔧 **Agregar link para copiar URL** de suscripciones de Apple

### Archivos a Modificar
- [terms_and_privacy_screen.dart](zodiac_app/lib/screens/terms_and_privacy_screen.dart) - Líneas 272-332

---

## 4. 🗑️ LIMPIEZA DE DATOS

### Estado Actual
- **Ubicación**: `settings_screen.dart` líneas 1607-1639
- **Funcionalidad**: Elimina todos los datos locales

### Lo que Funciona Bien
- ✅ Diálogo de confirmación antes de borrar
- ✅ Llama a `userPrefs.clear()` que borra todo
- ✅ Redirige a selección de idioma después
- ✅ Limpia el stack de navegación

### Mejoras Sugeridas
1. 🔧 **Agregar más información** sobre qué se borrará
2. 🔧 **Doble confirmación** para acción destructiva
3. 🔧 **Mostrar spinner** durante el proceso de limpieza
4. 🔧 **Ofrecer backup** antes de borrar

### Archivos a Modificar
- [settings_screen.dart](zodiac_app/lib/screens/settings_screen.dart) - Líneas 1607-1639

---

## 📋 PLAN DE ACCIÓN DETALLADO

### FASE 1: Correcciones Críticas (Prioridad Alta)

#### 1.1 Backup - Implementar Exportación Real
```
Tarea: Crear exportación funcional a archivo JSON
Archivos: settings_screen.dart, preferences_service.dart
Tiempo estimado: 30-45 min
```

#### 1.2 Términos - Corregir Precios
```
Tarea: Unificar precio $4.99 vs $7.99
Archivos: terms_and_privacy_screen.dart (línea 425)
Tiempo estimado: 5 min
```

### FASE 2: Traducciones (Prioridad Media)

#### 2.1 Diálogos Hardcodeados
```
Tarea: Traducir diálogos de soporte y suscripciones
Archivos: terms_and_privacy_screen.dart (líneas 272-332)
Traducciones: app_*.arb (6 idiomas)
Tiempo estimado: 20 min
```

### FASE 3: Mejoras UX (Prioridad Baja)

#### 3.1 Clear Data - Mejorar Diálogo
```
Tarea: Agregar lista de datos a borrar + ofrecer backup
Archivos: settings_screen.dart
Tiempo estimado: 15 min
```

#### 3.2 Privacy Policy - Botón Ver Más
```
Tarea: Agregar botón para ver política completa desde diálogo
Archivos: settings_screen.dart
Tiempo estimado: 10 min
```

---

## 🎯 RESUMEN EJECUTIVO

### Acciones Inmediatas (HOY)
1. **Backup**: Implementar exportación real a archivo JSON/compartible
2. **Términos**: Corregir inconsistencia de precios ($4.99 vs $7.99)
3. **Traducir**: Diálogos hardcodeados en español

### Acciones Opcionales (DESPUÉS)
4. **Backup**: Agregar funcionalidad de importación/restauración
5. **Clear Data**: Mejorar UX con lista de datos + ofrecer backup
6. **Privacy**: Agregar navegación a pantalla completa desde diálogo

---

## 📁 Archivos Principales Involucrados

| Archivo | Líneas Clave | Funcionalidad |
|---------|--------------|---------------|
| `settings_screen.dart` | 549-615 | Cards de la sección |
| `settings_screen.dart` | 1391-1478 | Diálogo Backup |
| `settings_screen.dart` | 1480-1605 | Diálogo Privacy |
| `settings_screen.dart` | 1607-1639 | Diálogo Clear Data |
| `settings_screen.dart` | 1716-1810 | Export User Data |
| `terms_and_privacy_screen.dart` | 1-53 | Pantalla principal |
| `terms_and_privacy_screen.dart` | 272-332 | Diálogos soporte (hardcoded) |
| `terms_and_privacy_screen.dart` | 336-459 | EULA completo |
| `terms_and_privacy_screen.dart` | 462-536 | Privacy Policy completa |
| `preferences_service.dart` | 243-261 | Método clear() |

---

## ✅ Criterio de Éxito

Cuando termines, las 4 funcionalidades deben:

1. **Backup**: Exportar datos reales a archivo compartible
2. **Privacy Policy**: Mostrar información completa + navegación a detalle
3. **Terms**: Precios consistentes + textos traducidos
4. **Clear Data**: Funcionar perfectamente (ya lo hace) + mejor UX

**Meta Final**: 100% funcional en los 6 idiomas soportados