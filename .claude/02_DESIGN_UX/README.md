# 🎨 AGENTES ESPECIALIZADOS EN DISEÑO UX/UI - ZODIAC APP

## 📋 **ÍNDICE DE AGENTES**

Este directorio contiene agentes especializados de Claude Code para el diseño y mejora de la experiencia de usuario de la aplicación Zodiac. Cada agente está optimizado para tareas específicas del proceso de diseño.

### **🎯 AGENTES PRINCIPALES**

| Agente | Especialización | Casos de Uso |
|--------|----------------|--------------|
| **[ui_design_system_expert.md](./ui_design_system_expert.md)** | Sistemas de diseño y componentes | Crear paletas de colores, espaciado, tipografía, tokens de diseño |
| **[flutter_animation_expert.md](./flutter_animation_expert.md)** | Animaciones y micro-interacciones | Transiciones fluidas, efectos visuales, optimización de performance |
| **[ux_research_expert.md](./ux_research_expert.md)** | Investigación y análisis UX | Testing de usabilidad, métricas, análisis de comportamiento |
| **[mobile_ui_specialist.md](./mobile_ui_specialist.md)** | Interfaces móviles nativas | Patrones iOS/Android, responsive design, touch optimization |
| **[visual_identity_expert.md](./visual_identity_expert.md)** | Identidad visual y branding | Iconografía, ilustraciones, consistencia de marca |

---

## 🚀 **GUÍA DE USO RÁPIDO**

### **Para Implementar el Plan UX 2025:**

1. **Fase 1 - Sistema de Diseño Base**
   ```bash
   # Usar: ui_design_system_expert.md
   # Crear: cosmic_colors.dart, app_spacing.dart, cosmic_typography.dart
   ```

2. **Fase 2 - Assets Gráficos**
   ```bash
   # Usar: visual_identity_expert.md
   # Crear: Iconografía zodiacal, ilustraciones, patrones cósmicos
   ```

3. **Fase 3 - Animaciones**
   ```bash
   # Usar: flutter_animation_expert.md
   # Implementar: Micro-interacciones, transiciones, loading states
   ```

4. **Fase 4 - Pantallas Principales**
   ```bash
   # Usar: mobile_ui_specialist.md
   # Rediseñar: Home, Compatibility, Sign Selection screens
   ```

5. **Fase 5 - Testing y Optimización**
   ```bash
   # Usar: ux_research_expert.md
   # Ejecutar: Usability testing, A/B testing, métricas
   ```

---

## 🛠️ **COMANDOS ÚTILES**

### **Análisis de Diseño Actual**
```bash
# Analizar consistencia de colores
grep -r "Color(0x" lib/ --include="*.dart" | sort | uniq -c

# Verificar espaciado
grep -r "EdgeInsets\|Padding\|SizedBox" lib/ --include="*.dart" | grep -E "[0-9]+\.0"

# Auditar tipografía
grep -r "TextStyle\|fontSize\|fontWeight" lib/ --include="*.dart"
```

### **Performance de Animaciones**
```bash
# Profiling de animaciones
flutter run --profile --trace-startup

# Detectar frame drops
flutter run --profile --verbose

# Análisis de memoria
flutter run --profile --trace-systrace
```

### **Testing UX**
```bash
# Screenshots para testing visual
flutter test --update-goldens test/golden/

# Testing de accesibilidad
flutter test test/accessibility/

# Performance benchmarks
flutter drive --target=test_driver/performance_test.dart
```

---

## 📊 **MÉTRICAS OBJETIVO**

### **Métricas Técnicas**
- **Performance**: 60 FPS consistente
- **Load Time**: <2s startup
- **Memory**: <150MB promedio
- **Bundle Size**: <50MB total

### **Métricas UX**
- **User Satisfaction**: 4.5+ estrellas
- **Task Completion**: >90%
- **Retention**: +25% día 7
- **Conversion**: +20% premium

---

## 🎯 **ESPECIALIZACIÓN POR AGENTE**

### **🎨 UI Design System Expert**
**Cuándo usar**: Necesitas crear o modificar componentes base, colores, espaciado, tipografía.

**Comandos clave**:
```dart
// Crear nuevo componente
class CosmicComponent extends StatelessWidget { ... }

// Validar consistencia
BrandValidator.validateColorUsage(color);
```

### **✨ Flutter Animation Expert**
**Cuándo usar**: Implementar animaciones, micro-interacciones, transiciones entre pantallas.

**Comandos clave**:
```dart
// Animación optimizada
class OptimizedCosmicWidget extends StatelessWidget { ... }

// Performance monitoring
AnimationPerformanceMonitor.trackAnimation(name, controller);
```

### **🔍 UX Research Expert**
**Cuándo usar**: Necesitas datos de usuario, testing de usabilidad, análisis de comportamiento.

**Comandos clave**:
```bash
# Analytics
firebase analytics:export --project=zodiac-app

# A/B testing
firebase analytics:funnel --events="app_open,sign_selected"
```

### **📱 Mobile UI Specialist**
**Cuándo usar**: Optimizar para móviles, implementar patrones nativos iOS/Android.

**Comandos clave**:
```dart
// Responsive design
ResponsiveLayout(mobileLayout: widget, tabletLayout: tablet)

// Touch optimization
TouchTargets.ensureMinTouchTarget(child: widget)
```

### **🎭 Visual Identity Expert**
**Cuándo usar**: Crear iconografía, ilustraciones, mantener consistencia de marca.

**Comandos clave**:
```dart
// Iconografía zodiacal
ZodiacIconSystem.getSignIcon(signName)

// Patrones cósmicos
CosmicPatterns.starField(starCount: 100)
```

---

## 📋 **CHECKLIST DE IMPLEMENTACIÓN**

### **Antes de Empezar**
- [ ] Leer el [PLAN_UX_MEJORAS_2025.md](../PLAN_UX_MEJORAS_2025.md)
- [ ] Identificar la fase actual del proyecto
- [ ] Seleccionar el agente apropiado
- [ ] Verificar dependencias técnicas

### **Durante la Implementación**
- [ ] Seguir las mejores prácticas del agente
- [ ] Usar comandos de validación
- [ ] Documentar cambios importantes
- [ ] Ejecutar tests de calidad

### **Después de Implementar**
- [ ] Verificar métricas de performance
- [ ] Validar consistencia de marca
- [ ] Actualizar documentación
- [ ] Marcar tareas como completadas

---

## 🔗 **RECURSOS ADICIONALES**

### **Documentación de Referencia**
- [Flutter Design Guidelines](https://docs.flutter.dev/ui)
- [Material Design 3](https://m3.material.io/)
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [WCAG 2.1 Accessibility](https://www.w3.org/WAI/WCAG21/quickref/)

### **Herramientas Recomendadas**
- **Figma**: Prototipado y sistema de diseño
- **Storybook Flutter**: Documentación de componentes
- **Firebase Analytics**: Métricas de usuario
- **Lighthouse**: Performance y accesibilidad

### **Comunidad y Soporte**
- [Flutter Community](https://flutter.dev/community)
- [Material Design Community](https://material.io/community)
- [UX Mastery](https://uxmastery.com/)

---

## 📞 **SOPORTE**

Para dudas específicas sobre cada agente, consulta la documentación individual de cada especialista. Cada archivo contiene ejemplos de código, comandos específicos y mejores prácticas para su área de especialización.

**¡Transforma la aplicación Zodiac en una experiencia visual premium!** 🌟
