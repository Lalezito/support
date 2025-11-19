# 🌌 PLAN MAESTRO: REDISEÑO CÓSMICO - BIRTH & ASCENDANT SCREENS
## **PARTE 3: COMPONENTES RESTANTES + PLAN DE EJECUCIÓN**

---

## 🕐 2. CosmicTimePicker Widget (Resumen)

```dart
// lib/widgets/cosmic_pickers/cosmic_time_picker.dart

class CosmicTimePicker extends StatefulWidget {
  final TimeOfDay initialTime;
  final Function(TimeOfDay) onTimeSelected;
  
  // DISEÑO:
  // - Circular clock face con glassmorphism
  // - Hour markers con glow effects
  // - Animated hands (hora y minutos)
  // - AM/PM selector cosmic
  // - Microanimaciones en cada cambio
}
```

---

## 📍 3. CosmicPlacePicker Widget (Resumen)

```dart
// lib/widgets/cosmic_pickers/cosmic_place_picker.dart

import 'package:geocoding/geocoding.dart';
import 'package:geolocator/geolocator.dart';

class CosmicPlacePicker extends StatefulWidget {
  final String? initialPlace;
  final Function(PlaceData) onPlaceSelected;
  
  // FEATURES:
  // - Search bar con autocomplete
  // - Current location detection (GPS)
  // - Popular cities preset
  // - Timezone auto-detection
  // - Map preview (opcional)
  // - Country flags
}

class PlaceData {
  final String cityName;
  final String countryName;
  final String countryCode;
  final double latitude;
  final double longitude;
  final String timezone;
  
  PlaceData({
    required this.cityName,
    required this.countryName,
    required this.countryCode,
    required this.latitude,
    required this.longitude,
    required this.timezone,
  });
}
```

---

## 🎴 4. CosmicBirthDataCard Widget

```dart
// lib/widgets/cosmic_pickers/cosmic_birth_data_card.dart

class CosmicBirthDataCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? value;
  final String? subtitle;
  final VoidCallback onTap;
  final bool isRequired;
  final bool isCompleted;
  
  @override
  Widget build(BuildContext context) {
    return CosmicCard(
      style: isCompleted ? CosmicCardStyle.accent : CosmicCardStyle.primary,
      showGlow: isCompleted,
      glowColor: CosmicColors.cosmicGold,
      onTap: onTap,
      child: Row(
        children: [
          // Icon container con glow
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              gradient: isCompleted 
                ? LinearGradient([
                    CosmicColors.cosmicPurple,
                    CosmicColors.cosmicGold,
                  ])
                : null,
              color: !isCompleted 
                ? Colors.white.withOpacity(0.1)
                : null,
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(
              icon,
              color: Colors.white,
              size: 28,
            ),
          ),
          
          const SizedBox(width: 16),
          
          // Content
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w600,
                        color: Colors.white,
                      ),
                    ),
                    if (isRequired) ...[
                      const SizedBox(width: 6),
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 2,
                        ),
                        decoration: BoxDecoration(
                          color: CosmicColors.cosmicPurple.withOpacity(0.3),
                          borderRadius: BorderRadius.circular(4),
                          border: Border.all(
                            color: CosmicColors.cosmicPurple,
                          ),
                        ),
                        child: const Text(
                          'Required',
                          style: TextStyle(
                            fontSize: 10,
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ],
                ),
                const SizedBox(height: 4),
                Text(
                  value ?? 'Not selected',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: isCompleted 
                      ? CosmicColors.cosmicGold
                      : Colors.white.withOpacity(0.5),
                  ),
                ),
                if (subtitle != null) ...[
                  const SizedBox(height: 2),
                  Text(
                    subtitle!,
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.white.withOpacity(0.6),
                    ),
                  ),
                ],
              ],
            ),
          ),
          
          // Arrow indicator
          Icon(
            Icons.chevron_right,
            color: Colors.white.withOpacity(0.5),
            size: 24,
          ),
        ],
      ),
    ).animate().fadeIn().slideX(begin: -0.1, end: 0);
  }
}
```

---

## ⭐ 5. ZodiacConstellationBackground Widget

```dart
// lib/widgets/backgrounds/zodiac_constellation_background.dart

import 'dart:math' as math;

class ZodiacConstellationBackground extends StatefulWidget {
  final String? zodiacSign;
  final int particleCount;
  final bool enableParallax;
  
  const ZodiacConstellationBackground({
    super.key,
    this.zodiacSign,
    this.particleCount = 50,
    this.enableParallax = true,
  });

  @override
  State<ZodiacConstellationBackground> createState() => 
    _ZodiacConstellationBackgroundState();
}

class _ZodiacConstellationBackgroundState 
    extends State<ZodiacConstellationBackground>
    with TickerProviderStateMixin {
  
  late AnimationController _twinkleController;
  late List<StarParticle> _stars;
  
  @override
  void initState() {
    super.initState();
    
    _twinkleController = AnimationController(
      duration: const Duration(seconds: 3),
      vsync: this,
    )..repeat();
    
    _generateStars();
  }

  void _generateStars() {
    _stars = List.generate(widget.particleCount, (index) {
      return StarParticle(
        x: math.Random().nextDouble(),
        y: math.Random().nextDouble(),
        size: math.Random().nextDouble() * 3 + 1,
        brightness: math.Random().nextDouble(),
        twinkleSpeed: math.Random().nextDouble() * 2 + 1,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    
    return AnimatedBuilder(
      animation: _twinkleController,
      builder: (context, child) {
        return CustomPaint(
          size: size,
          painter: ConstellationPainter(
            stars: _stars,
            animationValue: _twinkleController.value,
            zodiacSign: widget.zodiacSign,
          ),
        );
      },
    );
  }

  @override
  void dispose() {
    _twinkleController.dispose();
    super.dispose();
  }
}

class StarParticle {
  final double x;
  final double y;
  final double size;
  final double brightness;
  final double twinkleSpeed;
  
  StarParticle({
    required this.x,
    required this.y,
    required this.size,
    required this.brightness,
    required this.twinkleSpeed,
  });
}

class ConstellationPainter extends CustomPainter {
  final List<StarParticle> stars;
  final double animationValue;
  final String? zodiacSign;
  
  ConstellationPainter({
    required this.stars,
    required this.animationValue,
    this.zodiacSign,
  });

  @override
  void paint(Canvas canvas, Size size) {
    // Dibujar estrellas con efecto de parpadeo
    for (final star in stars) {
      final opacity = (math.sin(animationValue * math.pi * 2 * star.twinkleSpeed) + 1) / 2;
      final paint = Paint()
        ..color = Colors.white.withOpacity(opacity * star.brightness)
        ..style = PaintingStyle.fill;
      
      canvas.drawCircle(
        Offset(star.x * size.width, star.y * size.height),
        star.size,
        paint,
      );
      
      // Glow effect
      if (star.size > 2) {
        final glowPaint = Paint()
          ..color = CosmicColors.cosmicGold.withOpacity(opacity * 0.2)
          ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 4);
        
        canvas.drawCircle(
          Offset(star.x * size.width, star.y * size.height),
          star.size * 2,
          glowPaint,
        );
      }
    }
    
    // Dibujar líneas de constelación si hay signo zodiacal
    if (zodiacSign != null) {
      _drawConstellationLines(canvas, size);
    }
  }

  void _drawConstellationLines(Canvas canvas, Size size) {
    // TODO: Implementar patrones específicos por signo zodiacal
    final paint = Paint()
      ..color = CosmicColors.cosmicPurple.withOpacity(0.3)
      ..strokeWidth = 1
      ..style = PaintingStyle.stroke;
    
    // Ejemplo: conectar algunas estrellas
    for (int i = 0; i < stars.length - 1; i += 5) {
      final start = Offset(
        stars[i].x * size.width,
        stars[i].y * size.height,
      );
      final end = Offset(
        stars[i + 1].x * size.width,
        stars[i + 1].y * size.height,
      );
      
      if ((start - end).distance < size.width * 0.2) {
        canvas.drawLine(start, end, paint);
      }
    }
  }

  @override
  bool shouldRepaint(ConstellationPainter oldDelegate) => true;
}
```

---

## 📋 PLAN DE EJECUCIÓN - 5 FASES

### **FASE 1: Setup & Componentes Base (2h)**
```
✅ Agregar dependencias a pubspec.yaml
   - flutter_animate: ^4.3.0
   - geocoding: ^3.0.0  
   - geolocator: ^11.0.0

✅ Crear estructura de carpetas:
   lib/widgets/cosmic_pickers/
   ├─ cosmic_date_picker.dart
   ├─ cosmic_time_picker.dart
   ├─ cosmic_place_picker.dart
   └─ cosmic_birth_data_card.dart

✅ Crear ZodiacConstellationBackground
   lib/widgets/backgrounds/zodiac_constellation_background.dart

✅ Tests iniciales de componentes
```

### **FASE 2: CosmicDatePicker (2.5h)**
```
✅ Implementar estructura base
✅ Agregar glassmorphism effects
✅ Implementar calendar grid con animaciones
✅ Agregar month/year navigation
✅ Integrar zodiac sign detection
✅ Implementar glow animations
✅ Testing en Birth Date Screen
```

### **FASE 3: CosmicTimePicker (1.5h)**
```
✅ Diseño de clock face circular
✅ Implementar hour/minute selection
✅ AM/PM toggle cosmic
✅ Animaciones de transición
✅ Integration con Birth Date Screen
```

### **FASE 4: CosmicPlacePicker (2h)**
```
✅ Setup geocoding services
✅ Implementar search bar
✅ Current location detection
✅ Popular cities preset
✅ Timezone calculation
✅ Integration con Ascendant Screen
```

### **FASE 5: Integración & Refinamiento (2h)**
```
✅ Rediseñar Birth Date Screen completamente
✅ Rediseñar Ascendant Screen completamente
✅ Agregar ZodiacConstellationBackground
✅ Implementar CosmicBirthDataCard
✅ Testing exhaustivo
✅ Optimización de animaciones
✅ Localización (6 idiomas)
✅ Polish final
```

---

## 🎨 NUEVAS SCREENS - CÓDIGO COMPLETO

### **birth_date_screen.dart - REDISEÑADO:**

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../widgets/cosmic_pickers/cosmic_date_picker.dart';
import '../widgets/cosmic_pickers/cosmic_time_picker.dart';
import '../widgets/cosmic_pickers/cosmic_birth_data_card.dart';
import '../widgets/backgrounds/zodiac_constellation_background.dart';
import '../widgets/ui/cosmic_button.dart';

class BirthDateScreen extends ConsumerStatefulWidget {
  const BirthDateScreen({super.key});

  @override
  ConsumerState<BirthDateScreen> createState() => _BirthDateScreenState();
}

class _BirthDateScreenState extends ConsumerState<BirthDateScreen> {
  DateTime? _selectedDate;
  TimeOfDay? _selectedTime;
  String? _detectedZodiacSign;

  void _showDatePicker() async {
    await showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => CosmicDatePicker(
        initialDate: _selectedDate ?? DateTime.now(),
        firstDate: DateTime(1900),
        lastDate: DateTime.now(),
        onDateSelected: (date) {
          setState(() {
            _selectedDate = date;
            _detectedZodiacSign = _getZodiacSign(date);
          });
          Navigator.pop(context);
        },
      ),
    );
  }

  void _showTimePicker() async {
    await showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => CosmicTimePicker(
        initialTime: _selectedTime ?? TimeOfDay.now(),
        onTimeSelected: (time) {
          setState(() => _selectedTime = time);
          Navigator.pop(context);
        },
      ),
    );
  }

  void _continue() {
    if (_selectedDate == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select your birth date')),
      );
      return;
    }
    
    // Save data and navigate
    // ... existing save logic ...
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text(
          'Birth Data',
          style: TextStyle(color: Colors.white),
        ),
      ),
      body: Stack(
        children: [
          // Animated background
          ZodiacConstellationBackground(
            zodiacSign: _detectedZodiacSign,
          ),
          
          // Content
          SafeArea(
            child: Column(
              children: [
                // Header
                Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.auto_awesome,
                            color: CosmicColors.cosmicGold,
                            size: 28,
                          ),
                          const SizedBox(width: 12),
                          const Text(
                            'Your Cosmic Blueprint',
                            style: TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                          ),
                          const SizedBox(width: 12),
                          Icon(
                            Icons.auto_awesome,
                            color: CosmicColors.cosmicGold,
                            size: 28,
                          ),
                        ],
                      ).animate().fadeIn().slideY(begin: -0.2, end: 0),
                      
                      const SizedBox(height: 12),
                      
                      Text(
                        'Every star alignment tells a unique story',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.white.withOpacity(0.7),
                        ),
                        textAlign: TextAlign.center,
                      ).animate().fadeIn(delay: 200.ms),
                    ],
                  ),
                ),
                
                // Data cards
                Expanded(
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.symmetric(horizontal: 20),
                    child: Column(
                      children: [
                        // Birth Date Card
                        CosmicBirthDataCard(
                          icon: Icons.calendar_today,
                          title: 'Birth Date',
                          value: _selectedDate != null
                              ? _formatDate(_selectedDate!)
                              : null,
                          subtitle: _detectedZodiacSign != null
                              ? 'Your Sun Sign: $_detectedZodiacSign ${_getZodiacEmoji(_detectedZodiacSign!)}'
                              : null,
                          onTap: _showDatePicker,
                          isRequired: true,
                          isCompleted: _selectedDate != null,
                        ).animate().fadeIn(delay: 100.ms),
                        
                        const SizedBox(height: 16),
                        
                        // Birth Time Card
                        CosmicBirthDataCard(
                          icon: Icons.access_time,
                          title: 'Birth Time',
                          value: _selectedTime != null
                              ? _formatTime(_selectedTime!)
                              : null,
                          subtitle: 'For precise ascendant calculation',
                          onTap: _showTimePicker,
                          isRequired: false,
                          isCompleted: _selectedTime != null,
                        ).animate().fadeIn(delay: 200.ms),
                        
                        const SizedBox(height: 32),
                      ],
                    ),
                  ),
                ),
                
                // Continue button
                Padding(
                  padding: const EdgeInsets.all(20),
                  child: CosmicButton(
                    text: 'Continue Journey',
                    icon: Icons.auto_awesome,
                    onPressed: _continue,
                    style: CosmicButtonStyle.primary,
                    fullWidth: true,
                  ).animate().fadeIn(delay: 300.ms).slideY(begin: 0.2, end: 0),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String _formatDate(DateTime date) {
    // Format: "March 21, 1995"
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return '${months[date.month - 1]} ${date.day}, ${date.year}';
  }

  String _formatTime(TimeOfDay time) {
    final hour = time.hourOfPeriod == 0 ? 12 : time.hourOfPeriod;
    final minute = time.minute.toString().padLeft(2, '0');
    final period = time.period == DayPeriod.am ? 'AM' : 'PM';
    return '$hour:$minute $period';
  }

  String _getZodiacSign(DateTime date) {
    // ... existing zodiac logic ...
    return 'Aries';
  }

  String _getZodiacEmoji(String sign) {
    const zodiacEmojis = {
      'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊',
      'Cancer': '♋', 'Leo': '♌', 'Virgo': '♍',
      'Libra': '♎', 'Scorpio': '♏', 'Sagittarius': '♐',
      'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓',
    };
    return zodiacEmojis[sign] ?? '⭐';
  }
}
```

---

## ✅ CHECKLIST FINAL

```
□ flutter pub add flutter_animate geocoding geolocator
□ Crear carpeta lib/widgets/cosmic_pickers/
□ Crear carpeta lib/widgets/backgrounds/
□ Implementar CosmicDatePicker
□ Implementar CosmicTimePicker
□ Implementar CosmicPlacePicker
□ Implementar CosmicBirthDataCard
□ Implementar ZodiacConstellationBackground
□ Rediseñar birth_date_screen.dart
□ Rediseñar ascendant_screen.dart
□ Testing en iOS
□ Testing en Android
□ Localización (6 idiomas)
□ Performance optimization
□ Git commit
```

---

**🚀 LISTO PARA IMPLEMENTACIÓN CON CLAUDE CODE**

**Próximo paso:** Ejecutar FASE 1 del plan
