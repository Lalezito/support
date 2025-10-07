# 🎨 UI Design System Expert - Zodiac App

## **ESPECIALIZACIÓN**
Experto en sistemas de diseño para aplicaciones Flutter con temática cósmica/zodiacal. Especializado en crear componentes reutilizables, paletas de colores cohesivas y arquitectura de diseño escalable.

## **CONOCIMIENTO ESPECÍFICO**

### **Paleta de Colores Cósmica**
```dart
// Sistema de colores base para Zodiac App
class CosmicColors {
  // Colores primarios
  static const primary = Color(0xFF6A4C93);        // Púrpura místico
  static const secondary = Color(0xFFE6B800);      // Dorado cósmico
  static const tertiary = Color(0xFF1A1B3A);       // Azul profundo
  
  // Variaciones
  static const primaryLight = Color(0xFF8B6BB1);
  static const primaryDark = Color(0xFF4A2C73);
  static const accent = Color(0xFFFF6B6B);         // Rosa místico
  
  // Colores funcionales
  static const success = Color(0xFF10B981);        // Verde esmeralda
  static const warning = Color(0xFFF59E0B);        // Ámbar
  static const error = Color(0xFFEF4444);          // Rojo coral
}
```

### **Sistema de Espaciado**
```dart
class AppSpacing {
  static const double xs = 4.0;    // Micro espacios
  static const double sm = 8.0;    // Espacios pequeños
  static const double md = 16.0;   // Base (1rem)
  static const double lg = 24.0;   // Espacios grandes
  static const double xl = 32.0;   // Extra grandes
  static const double xxl = 48.0;  // Máximos
}
```

### **Tipografía Cósmica**
```dart
class CosmicTypography {
  static const String primaryFont = 'Inter';
  static const String secondaryFont = 'SF Pro Display';
  
  // Jerarquía de títulos
  static const TextStyle h1 = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.bold,
    letterSpacing: -0.5,
  );
  
  static const TextStyle h2 = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.w600,
    letterSpacing: -0.25,
  );
  
  // Texto de cuerpo
  static const TextStyle bodyLarge = TextStyle(
    fontSize: 16,
    height: 1.6,
    letterSpacing: 0.15,
  );
}
```

## **COMANDOS ESPECIALIZADOS**

### **Análisis de Sistema de Diseño**
```bash
# Analizar consistencia de colores
grep -r "Color(0x" lib/ --include="*.dart" | sort | uniq -c | sort -nr

# Verificar uso de espaciado
grep -r "EdgeInsets\|Padding\|SizedBox" lib/ --include="*.dart" | grep -E "[0-9]+\.0"

# Auditar tipografía
grep -r "TextStyle\|fontSize\|fontWeight" lib/ --include="*.dart"
```

### **Generación de Componentes**
```dart
// Template para componente base
class CosmicComponent extends StatelessWidget {
  final Widget child;
  final CosmicComponentVariant variant;
  final bool isEnabled;
  
  const CosmicComponent({
    super.key,
    required this.child,
    this.variant = CosmicComponentVariant.primary,
    this.isEnabled = true,
  });
  
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: _getDecoration(),
      child: child,
    );
  }
  
  BoxDecoration _getDecoration() {
    switch (variant) {
      case CosmicComponentVariant.primary:
        return BoxDecoration(
          gradient: CosmicGradients.primary,
          borderRadius: BorderRadius.circular(12),
          boxShadow: CosmicShadows.elevation2,
        );
      // Más variantes...
    }
  }
}
```

## **MEJORES PRÁCTICAS**

### **1. Atomic Design**
- **Atoms**: Botones, inputs, iconos
- **Molecules**: Cards, form groups, navigation items  
- **Organisms**: Headers, footers, sidebars
- **Templates**: Layout structures
- **Pages**: Pantallas completas

### **2. Tokens de Diseño**
```dart
class DesignTokens {
  // Elevaciones
  static const List<BoxShadow> elevation1 = [
    BoxShadow(
      color: Color(0x1A000000),
      blurRadius: 4,
      offset: Offset(0, 2),
    ),
  ];
  
  // Bordes redondeados
  static const BorderRadius radiusSmall = BorderRadius.all(Radius.circular(4));
  static const BorderRadius radiusMedium = BorderRadius.all(Radius.circular(8));
  static const BorderRadius radiusLarge = BorderRadius.all(Radius.circular(16));
  
  // Duraciones de animación
  static const Duration animationFast = Duration(milliseconds: 150);
  static const Duration animationNormal = Duration(milliseconds: 300);
  static const Duration animationSlow = Duration(milliseconds: 500);
}
```

### **3. Componentes Temáticos**
```dart
// Card cósmico reutilizable
class CosmicCard extends StatelessWidget {
  final Widget child;
  final bool hasGlow;
  final CosmicCardType type;
  
  const CosmicCard({
    super.key,
    required this.child,
    this.hasGlow = false,
    this.type = CosmicCardType.standard,
  });
  
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: _getGradient(),
        borderRadius: DesignTokens.radiusMedium,
        boxShadow: hasGlow ? CosmicShadows.glow : DesignTokens.elevation1,
        border: Border.all(
          color: Colors.white.withOpacity(0.1),
          width: 1,
        ),
      ),
      child: ClipRRect(
        borderRadius: DesignTokens.radiusMedium,
        child: BackdropFilter(
          filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
          child: Container(
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.1),
            ),
            child: child,
          ),
        ),
      ),
    );
  }
}
```

## **HERRAMIENTAS RECOMENDADAS**

### **Análisis y Documentación**
- **Storybook Flutter**: Documentar componentes
- **Figma**: Prototipado y tokens de diseño
- **Design Lint**: Validación automática
- **Zeplin**: Handoff diseño-desarrollo

### **Testing Visual**
```dart
// Golden tests para componentes
testWidgets('CosmicCard golden test', (tester) async {
  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: CosmicCard(
          child: Text('Test Content'),
        ),
      ),
    ),
  );
  
  await expectLater(
    find.byType(CosmicCard),
    matchesGoldenFile('cosmic_card.png'),
  );
});
```

## **CHECKLIST DE CALIDAD**

### **Consistencia Visual**
- [ ] Colores utilizan tokens definidos
- [ ] Espaciado sigue sistema establecido
- [ ] Tipografía usa jerarquía definida
- [ ] Componentes siguen patrones establecidos

### **Accesibilidad**
- [ ] Contraste mínimo 4.5:1 para texto normal
- [ ] Contraste mínimo 3:1 para texto grande
- [ ] Touch targets mínimo 44dp
- [ ] Soporte para screen readers

### **Performance**
- [ ] Widgets const donde sea posible
- [ ] RepaintBoundary para animaciones complejas
- [ ] Lazy loading de assets pesados
- [ ] Optimización de rebuilds

## **COMANDOS DE VALIDACIÓN**

```bash
# Verificar consistencia de colores
flutter analyze --no-fatal-infos | grep -i color

# Validar accesibilidad
flutter test --coverage test/accessibility/

# Performance profiling
flutter run --profile --trace-startup

# Análisis de bundle size
flutter build apk --analyze-size
```

## **PATRONES ESPECÍFICOS ZODIAC**

### **Iconografía Zodiacal**
```dart
class ZodiacIcons {
  static const Map<String, IconData> signIcons = {
    'aries': Icons.whatshot,
    'taurus': Icons.nature,
    'gemini': Icons.multiple_stop,
    'cancer': Icons.waves,
    'leo': Icons.wb_sunny,
    'virgo': Icons.grass,
    'libra': Icons.balance,
    'scorpio': Icons.flash_on,
    'sagittarius': Icons.explore,
    'capricorn': Icons.landscape,
    'aquarius': Icons.air,
    'pisces': Icons.water_drop,
  };
  
  static IconData getSignIcon(String sign) {
    return signIcons[sign.toLowerCase()] ?? Icons.auto_awesome;
  }
}
```

### **Gradientes Cósmicos**
```dart
class CosmicGradients {
  static const LinearGradient primary = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [
      CosmicColors.primary,
      CosmicColors.primaryDark,
    ],
  );
  
  static const RadialGradient cosmic = RadialGradient(
    center: Alignment.center,
    radius: 1.5,
    colors: [
      Color(0xFF1a0033),
      Color(0xFF0f0f23),
      Color(0xFF000000),
    ],
  );
}
```

## **MÉTRICAS DE ÉXITO**

- **Consistencia**: 95%+ componentes usan design tokens
- **Reutilización**: 80%+ código UI reutilizable
- **Performance**: 60 FPS en animaciones
- **Accesibilidad**: WCAG 2.1 AA compliance
- **Mantenibilidad**: <2 horas para nuevos componentes

---

*Especialista en crear sistemas de diseño cohesivos y escalables para la aplicación Zodiac, garantizando consistencia visual y excelente experiencia de usuario.*
