# 📋 Registro Histórico de Errores - Zodiac App

Este archivo registra errores encontrados y sus soluciones para referencia futura.

---

## 2025-12-15 | Mezcla de Archivos Entre Ramas

### Descripción
Al ejecutar `git checkout main -- .` se mezclaron archivos de la rama `main` con la rama actual `agent-ux-production`, causando **14,617 errores**.

### Síntomas
- Miles de `undefined_identifier`
- `undefined_method` en múltiples archivos
- Imports rotos (`uri_does_not_exist`)
- Errores de tipo (`non_type_as_type_argument`)

### Archivos Más Afectados
- `lib/widgets/ui/empty_state_variants.dart` - AppLocalizations, EmptyState, EmptyStateIcon undefined
- `lib/widgets/zodiac_constellation_overlay.dart` - ZodiacSign undefined
- Múltiples servicios y widgets

### Causa Raíz
El comando `git checkout main -- .` reemplaza TODOS los archivos del directorio actual con la versión de otra rama, pero NO cambia de rama. Esto crea un estado híbrido inconsistente.

### Solución Aplicada
```bash
git stash  # Guardó cambios locales
# Esto restauró automáticamente los archivos al estado del último commit de agent-ux-production
```

### Estado Post-Solución
- Rama: `agent-ux-production`
- Errores: 67 (mayormente en `secret_manager_service.dart`)
- App funcional

### Lección Aprendida
- **NUNCA** usar `git checkout <rama> -- .` para "ver" otra rama
- Usar `git diff <rama>` para comparar
- Usar `git stash` + `git checkout <rama>` para cambiar de rama

---

## Plantilla para Nuevos Errores

```markdown
## YYYY-MM-DD | Título del Error

### Descripción
[Qué pasó]

### Síntomas
- [Lista de errores visibles]

### Causa Raíz
[Por qué ocurrió]

### Solución Aplicada
```bash
[Comandos ejecutados]
```

### Lección Aprendida
[Cómo evitarlo en el futuro]
```

---

## Índice de Errores por Categoría

### Git / Control de Versiones
- [2025-12-15] Mezcla de archivos entre ramas

### Dependencias
- (Pendiente)

### Imports / Localización
- (Pendiente)

### Build / Compilación
- (Pendiente)
