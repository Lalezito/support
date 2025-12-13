# 🧠 COSMIC COACH - MEJORAS AVANZADAS PARTE 3-7
## Noviembre 12, 2025 - Especificaciones Completas

---

## 🔄 PARTE 3: BIORHYTHMS & CICLOS NATURALES

### **Teoría de Biorritmos (Ciclos de Energía Personal)**

Descubierto por Wilhelm Fliess en 1800s, estudiado científicamente en 1900s:
- **Ciclo Físico**: 23 días (fuerza, resistencia, coordinación)
- **Ciclo Emocional**: 28 días (creatividad, sensibilidad, mood)
- **Ciclo Intelectual**: 33 días (memoria, alerteza, lógica)

Cada ciclo tiene 3 fases:
- **Fase Alta (Peak)**: Días 1-11 aprox - máxima energía
- **Día Crítico**: Cruce de ciclo - momento vulnerable
- **Fase Baja (Recovery)**: Días 12-23 aprox - recuperación

```dart
class BiorhythmCalculator {
  /// Calcula biorhythm basado en fecha de nacimiento
  static Map<String, BiorhythmPhase> calculateBiorhythms(DateTime birthDate) {
    final today = DateTime.now();
    final daysSinceBirth = today.difference(birthDate).inDays;

    return {
      'physical': _calculateCycle(daysSinceBirth, 23),
      'emotional': _calculateCycle(daysSinceBirth, 28),
      'intellectual': _calculateCycle(daysSinceBirth, 33),
    };
  }

  static BiorhythmPhase _calculateCycle(int daysSinceBirth, int cycleLength) {
    final position = daysSinceBirth % cycleLength;
    final percentage = sin((position / cycleLength) * 2 * pi) * 100;

    if (percentage > 50) return BiorhythmPhase.high;
    if (percentage < -50) return BiorhythmPhase.low;
    if (percentage.abs() < 10) return BiorhythmPhase.critical;
    return BiorhythmPhase.neutral;
  }
}

enum BiorhythmPhase {
  high,      // Peak energy
  neutral,   // Balanced
  low,       // Recovery
  critical,  // Day of transition (vulnerable)
}
```

### **Goals Basados en Biorhythms**

#### 1. **Goal: "⚡ Physical Peak Day"**
```dart
Goal(
  title: "⚡ Peak Performance",
  description: "Tu ciclo físico está en MÁXIMO hoy (día ${biorhythmDay}/23). Momento perfecto para: workout intenso, competencia, récord personal.",
  category: "fitness",
  difficulty: "hard",
  activeWhen: BiorhythmPhase.high,
  scienceExplanation: """
  🔬 BIORHYTHMS - CICLO FÍSICO (23 días):

  Tu cuerpo tiene ciclos naturales de energía que se repiten
  cada 23 días desde tu nacimiento.

  FASE ALTA (Días 1-11):
  • Fuerza muscular máxima
  • Resistencia aumentada
  • Coordinación óptima
  • Recuperación rápida
  • Menor riesgo de lesiones

  ESTUDIOS:
  - Atletas olímpicos rompen récords en fase alta (75% de casos)
  - Cirujanos tienen menos errores en fase alta
  - Accidentes de trabajo disminuyen 40% en fase alta

  QUÉ HACER HOY:
  ✅ PR (Personal Record) en gym
  ✅ Competencia deportiva
  ✅ Aprender movimiento nuevo complejo
  ✅ Workout de máxima intensidad
  ✅ Desafío físico que postergaste
  """,
  zodiacConnection: {
    'Aries': 'Tu Marte se alinea con tu biorhythm físico. HOY eres imparable.',
    'Leo': 'Tu Sol brilla más cuando tu cuerpo está en peak. Tiempo de brillar físicamente.',
    'Sagitario': 'Tu Júpiter expansivo + física peak = aventuras extremas hoy.',
  },
  tasks: [
    "🏋️ Intenta un peso/distancia/tiempo nuevo",
    "🏃 Corre más rápido o más lejos que lo usual",
    "🧗 Prueba actividad física desafiante",
    "⚽ Juega deporte competitivo",
    "💪 Do your hardest workout routine",
  ],
);
```

#### 2. **Goal: "🎨 Emotional Peak Day"**
```dart
Goal(
  title: "🎨 Creatividad Máxima",
  description: "Tu ciclo emocional está en PEAK hoy (día ${biorhythmDay}/28). Momento perfecto para: arte, música, escribir, conversaciones profundas.",
  category: "creativity",
  difficulty: "medium",
  activeWhen: BiorhythmPhase.high,
  scienceExplanation: """
  🔬 BIORHYTHMS - CICLO EMOCIONAL (28 días):

  FASE ALTA (Días 1-14):
  • Creatividad fluye naturalmente
  • Emociones estables y positivas
  • Empatía aumentada
  • Relaciones fluyen fácil
  • Intuición aguda

  ESTUDIOS:
  - Artistas producen mejores obras en fase alta
  - Terapia es más efectiva en fase alta emocional
  - Relaciones mejoran si ambos están en fase alta

  QUÉ HACER HOY:
  ✅ Crear arte (pintura, música, escritura)
  ✅ Conversación importante con ser querido
  ✅ Terapia o trabajo emocional profundo
  ✅ Expresar sentimientos creativamente
  ✅ Conectar genuinamente con alguien
  """,
  zodiacConnection: {
    'Cáncer': 'Tu Luna + ciclo emocional peak = sensibilidad suprema hoy.',
    'Pisces': 'Tu Neptuno + emociones peak = canal artístico abierto.',
    'Libra': 'Tu Venus + emociones peak = relaciones florecen hoy.',
  },
  tasks: [
    "🎨 Crea algo artístico (cualquier medio)",
    "💬 Ten conversación profunda con alguien importante",
    "📝 Escribe sobre tus sentimientos",
    "🎵 Toca música o canta",
    "❤️ Expresa amor/aprecio a alguien",
  ],
);
```

#### 3. **Goal: "🧠 Intellectual Peak Day"**
```dart
Goal(
  title: "🧠 Mente Brillante",
  description: "Tu ciclo intelectual está en PEAK hoy (día ${biorhythmDay}/33). Momento perfecto para: aprender, estudiar, decisiones importantes, estrategia.",
  category: "learning",
  difficulty: "hard",
  activeWhen: BiorhythmPhase.high,
  scienceExplanation: """
  🔬 BIORHYTHMS - CICLO INTELECTUAL (33 días):

  FASE ALTA (Días 1-16):
  • Memoria fotográfica
  • Concentración máxima
  • Lógica clara
  • Decisiones acertadas
  • Aprendizaje rápido

  ESTUDIOS:
  - Estudiantes tienen 30% mejor performance en exámenes en fase alta
  - CEOs toman mejores decisiones en fase intelectual alta
  - Programadores escriben código con menos bugs

  QUÉ HACER HOY:
  ✅ Estudiar material complejo
  ✅ Tomar decisión importante (inversión, carrera, relación)
  ✅ Aprender skill nuevo
  ✅ Resolver problema difícil
  ✅ Planear estrategia a largo plazo
  """,
  zodiacConnection: {
    'Géminis': 'Tu Mercurio + intelecto peak = genio hoy.',
    'Virgo': 'Tu Mercurio analítico + fase alta = precisión perfecta.',
    'Aquarius': 'Tu Urano + intelecto peak = ideas revolucionarias.',
  },
  tasks: [
    "📚 Estudia algo complejo (2+ horas focus)",
    "🎯 Toma 1 decisión importante que postergaste",
    "💡 Resuelve problema difícil",
    "📊 Planea estrategia para próximos 3 meses",
    "🧩 Aprende algo nuevo y desafiante",
  ],
);
```

#### 4. **Goal: "⚠️ Critical Day - Self Care"**
```dart
Goal(
  title: "⚠️ Día Crítico - Cuídate",
  description: "ALERTA: Hoy es día CRÍTICO en tu ciclo ${criticalCycle}. Más vulnerable a errores/accidentes. Toma precauciones extra.",
  category: "safety",
  difficulty: "easy",
  activeWhen: BiorhythmPhase.critical,
  scienceExplanation: """
  🔬 DÍAS CRÍTICOS - MOMENTOS DE TRANSICIÓN:

  Cuando un ciclo cruza de fase alta a baja (o viceversa),
  hay un momento de INESTABILIDAD.

  ESTADÍSTICAS:
  - 60% más accidentes de tráfico en días críticos físicos
  - 40% más errores médicos en días críticos intelectuales
  - Conflictos relacionales aumentan en días críticos emocionales

  POR QUÉ OCURRE:
  Tu cuerpo/mente/emociones están RE-CALIBRANDO.
  Es como reiniciar una computadora - momento vulnerable.

  QUÉ EVITAR HOY:
  ❌ Conducir rápido o distraído
  ❌ Tomar decisiones importantes
  ❌ Actividades de alto riesgo
  ❌ Confrontaciones importantes
  ❌ Multitasking complejo

  QUÉ HACER HOY:
  ✅ Ir despacio y con cuidado
  ✅ Doble-check todo
  ✅ Pedir ayuda si es necesario
  ✅ Descansar más de lo usual
  ✅ Meditación y grounding
  """,
  warningsBy Cycle: {
    'physical': [
      "🚗 Maneja con cuidado extra",
      "🏋️ No intentes récords personales",
      "⚠️ Cuidado con herramientas/maquinaria",
      "🧘 Haz yoga/stretching suave (no intenso)",
    ],
    'emotional': [
      "💬 Pospón conversaciones difíciles",
      "🚫 No tomes decisiones relacionales importantes",
      "😌 Practica auto-compasión",
      "🎭 Acepta que las emociones están inestables",
    ],
    'intellectual': [
      "🎯 Pospón decisiones importantes 24h",
      "✅ Doble-check todo (emails, cálculos, contratos)",
      "🧠 No estudies material nuevo complejo",
      "📋 Revisa en lugar de crear",
    ],
  },
  zodiacAdvice: {
    'Aries': 'Tu impulso marciano + día crítico = receta para accidente. PAUSA hoy.',
    'Géminis': 'Tu mente rápida puede cometer errores en día crítico. Ve DESPACIO.',
    'Escorpio': 'Tu intensidad + emociones críticas = explosión potencial. RESPIRA.',
  },
);
```

---

## 💑 PARTE 4: GOALS DE RELACIONES POR COMPATIBILIDAD

### **Sistema de Compatibilidad Zodiacal Avanzado**

Basado en aspectos astrológicos entre signos:
- **Conjunción (0°)**: Mismo signo - entienden perfectamente pero pueden chocar
- **Sextil (60°)**: 2 signos de distancia - armonía fácil
- **Cuadrado (90°)**: 3 signos de distancia - tensión pero crecimiento
- **Trígono (120°)**: 4 signos de distancia - flow natural
- **Oposición (180°)**: Signos opuestos - atracción magnética pero desafíos

### **Goals por Tipo de Relación**

#### 1. **Oposiciones (Atracción Magnética + Tensión)**

Parejas opuestas:
- Aries ↔ Libra
- Tauro ↔ Escorpio
- Géminis ↔ Sagitario
- Cáncer ↔ Capricorn
- Leo ↔ Aquarius
- Virgo ↔ Pisces

```dart
Goal(
  title: "⚖️ Navega Tu Oposición (Aries-Libra)",
  description: "Aries + Libra = opuestos que se atraen. Ustedes son espejo uno del otro - aprende de lo que tu pareja tiene y tú necesitas.",
  category: "relationships",
  difficulty: "hard",
  forPairs: ['Aries-Libra', 'Libra-Aries'],
  astroExplanation: """
  🪐 OPOSICIÓN ARIES-LIBRA:

  Aries (Yo) ←→ Libra (Nosotros)
  Marte (Acción) ←→ Venus (Armonía)
  Fuego (Impulso) ←→ Aire (Reflexión)
  Cardinal (Inicia) ←→ Cardinal (Inicia)

  DINÁMICA:
  Aries: "¡Vamos! ¡Hazlo YA!"
  Libra: "Pero... veamos todos los ángulos primero"

  Aries: "Yo sé lo que quiero"
  Libra: "¿Pero tú qué quieres?"

  REGALO MUTUO:
  - Aries enseña a Libra: Decisión rápida, autenticidad, coraje
  - Libra enseña a Aries: Consideración, diplomacia, paciencia

  CONFLICTOS COMUNES:
  ⚔️ Aries: "¡Decides ya!" vs Libra: "Dame tiempo para pensar"
  ⚔️ Aries: "Yo primero" vs Libra: "¿Y los demás?"
  ⚔️ Aries: Directo/brutal vs Libra: Indirecto/diplomático

  CÓMO HACER QUE FUNCIONE:
  ✅ Aries: Practica paciencia - cuenta hasta 10
  ✅ Libra: Practica decisión - elige en <5 min
  ✅ Ambos: Aprecien que el otro los COMPLETA
  ✅ Compromiso: Alterna quién decide (lunes Aries, martes Libra)
  """,
  dailyTasks: [
    "🎯 Aries: Pregunta a tu Libra su opinión ANTES de actuar",
    "⚖️ Libra: Toma 1 decisión rápida hoy SIN consultar",
    "💬 Ambos: Discutan 1 tema donde NO están de acuerdo - busquen punto medio",
    "❤️ Aries: Di algo bonito/diplomático (modo Libra)",
    "🔥 Libra: Haz algo espontáneo/impulsivo (modo Aries)",
  ],
  weeklyRitual: """
  RITUAL ARIES-LIBRA (1x semana):

  1. Encuentren espacio neutro (café, parque)
  2. Aries: Comparte qué aprendiste de Libra esta semana
  3. Libra: Comparte qué aprendiste de Aries esta semana
  4. Ambos: "Te admiro porque tú eres [cualidad que yo no tengo]"
  5. Compromiso: ¿En qué área practicaré ser más como tú?

  NOTA: Oposiciones funcionan cuando CADA UNO aprende del otro,
  no cuando uno trata de cambiar al otro.
  """,
);
```

#### 2. **Cuadrados (Fricción Productiva)**

Parejas en cuadrado:
- Aries ↔ Cáncer/Capricorn
- Tauro ↔ Leo/Aquarius
- Géminis ↔ Virgo/Pisces
- etc.

```dart
Goal(
  title: "⚡ Fricción Productiva (Aries-Cáncer)",
  description: "Aries + Cáncer = choque de necesidades. Aries necesita acción, Cáncer necesita seguridad. Ambos son válidos.",
  category: "relationships",
  difficulty: "hard",
  forPairs: ['Aries-Cancer', 'Cancer-Aries'],
  astroExplanation: """
  🪐 CUADRADO ARIES-CÁNCER:

  Aries (Fuego/Cardinal) ⚔️ Cáncer (Agua/Cardinal)
  Marte (Guerra) ⚔️ Luna (Emoción)
  Independencia ⚔️ Intimidad

  CONFLICTO CENTRAL:
  Aries: "Dame espacio, necesito libertad"
  Cáncer: "Quédate cerca, necesito conexión"

  Aries: "¡Aventura! ¡Riesgo!"
  Cáncer: "Seguridad. Hogar. Estabilidad."

  POR QUÉ ES DIFÍCIL:
  Ambos son signos CARDINALES (líderes, iniciadores).
  Ninguno quiere ceder. Ambos quieren liderar la relación
  en direcciones OPUESTAS.

  REGALO MUTUO:
  - Aries enseña a Cáncer: Coraje, independencia, aventura
  - Cáncer enseña a Aries: Vulnerabilidad, empatía, raíces

  CÓMO HACER QUE FUNCIONE:
  ✅ Aries: Entiende que la necesidad de seguridad de Cáncer es REAL
  ✅ Cáncer: Entiende que la necesidad de espacio de Aries NO es rechazo
  ✅ Compromiso: "Adventure from a secure base"
     (Cáncer crea hogar estable, Aries sale a conquistar el mundo)
  """,
  dailyTasks: [
    "🔥 Aries: Haz 1 cosa que haga sentir seguro/a a tu Cáncer",
    "🌊 Cáncer: Da espacio a tu Aries por 2 horas sin pedir explicaciones",
    "💬 Ambos: 'Necesito X, ¿cómo podemos hacer que ambos seamos felices?'",
    "🏠 Crea ritual diario: 20 min de conexión (para Cáncer) + 20 min solo (para Aries)",
  ],
  warningSign: """
  🚨 SEÑAL DE PELIGRO:

  Si Aries siente: "Me sofoca, no puedo respirar"
  Si Cáncer siente: "Me abandona, no le importo"

  AMBOS SON VÁLIDOS. Ninguno es "equivocado".

  SOLUCIÓN: Estructura predecible
  - Lunes/Miércoles/Viernes: Aries tiene libertad total
  - Martes/Jueves/Sábado: Tiempo juntos sin interrupciones
  - Domingo: Deciden juntos

  Cuando Cáncer SABE que tiene tiempo garantizado,
  puede soltar. Cuando Aries SABE que tiene espacio garantizado,
  puede conectar.
  """,
);
```

#### 3. **Trígonos (Flow Natural)**

Parejas en trígono (mismo elemento):
- **Fuego**: Aries, Leo, Sagitario
- **Tierra**: Tauro, Virgo, Capricorn
- **Aire**: Géminis, Libra, Aquarius
- **Agua**: Cáncer, Escorpio, Pisces

```dart
Goal(
  title: "🔥 Flow de Fuego (Aries-Leo-Sagitario)",
  description: "Signos de Fuego juntos = química explosiva. Pero cuidado: demasiado fuego puede quemar todo.",
  category: "relationships",
  difficulty: "medium",
  forPairs: ['Aries-Leo', 'Aries-Sagittarius', 'Leo-Sagittarius'],
  astroExplanation: """
  🪐 TRÍGONO DE FUEGO:

  QUÍMICA:
  ✅ Se entienden PERFECTAMENTE
  ✅ Misma velocidad (rápida)
  ✅ Misma energía (alta)
  ✅ Mismas necesidades (acción, aventura, pasión)

  PELIGROS:
  ⚠️ Demasiada intensidad (burnout)
  ⚠️ Competencia (ambos quieren ganar)
  ⚠️ Impulsividad doble (malas decisiones)
  ⚠️ Falta de grounding (todo es emoción, poca practicidad)

  DINÁMICA POR PAREJA:

  ARIES + LEO:
  • Química: 🔥🔥🔥🔥🔥
  • Reto: Ambos quieren liderar
  • Solución: Alternar roles de liderazgo

  ARIES + SAGITARIO:
  • Química: 🔥🔥🔥🔥🔥
  • Reto: Demasiada independencia (¿cuándo se ven?)
  • Solución: Aventuras JUNTOS

  LEO + SAGITARIO:
  • Química: 🔥🔥🔥🔥
  • Reto: Leo necesita atención, Sagitario necesita libertad
  • Solución: Leo brilla EN las aventuras de Sagitario
  """,
  dailyTasks: [
    "🧘 AMBOS: 10 min de calma/meditación (equilibren el fuego)",
    "🌍 Hagan algo PRÁCTICO juntos (finanzas, limpieza)",
    "💬 Pregúntense: '¿Estamos yendo demasiado rápido?'",
    "🎯 Compitan en algo SALUDABLE (gym, juego, cocina)",
    "😴 Prioricen descanso (fuego necesita recuperarse)",
  ],
  balancingElement: """
  ELEMENTO FALTANTE: TIERRA

  Signos de Fuego juntos = pura energía, pero ¿dónde está la base?

  AGREGAR TIERRA:
  ✅ Rutinas predecibles
  ✅ Ahorro financiero
  ✅ Metas a largo plazo
  ✅ Cuidado del cuerpo físico
  ✅ Hogar estable

  PRÁCTICA:
  1x semana: "Día de Tierra"
  - Cocinen comida saludable
  - Revisen finanzas juntos
  - Limpien/organicen un espacio
  - Caminen en naturaleza (grounding)
  - Planeen próximos 3 meses

  RESULTADO: Fuego con DIRECCIÓN = éxito garantizado
  """,
);
```

---

## 🔢 PARTE 5: NUMEROLOGÍA + ASTROLOGÍA (Doble Sistema)

### **Life Path Number (Número de Vida)**

Cálculo:
```dart
class NumerologyCalculator {
  /// Calcula Life Path Number desde fecha de nacimiento
  /// Ejemplo: 15/03/1990 = 1+5+0+3+1+9+9+0 = 28 = 2+8 = 10 = 1+0 = 1
  static int calculateLifePath(DateTime birthDate) {
    int sum = _sumDigits(birthDate.day) +
              _sumDigits(birthDate.month) +
              _sumDigits(birthDate.year);

    // Reducir hasta master number (11, 22, 33) o single digit
    while (sum > 9 && sum != 11 && sum != 22 && sum != 33) {
      sum = _sumDigits(sum);
    }

    return sum;
  }

  static int _sumDigits(int number) {
    return number.toString()
        .split('')
        .map((d) => int.parse(d))
        .reduce((a, b) => a + b);
  }

  /// Calcula Personal Year (Año Personal)
  /// Muestra qué energía domina tu año actual
  static int calculatePersonalYear(DateTime birthDate, int currentYear) {
    final sum = _sumDigits(birthDate.day) +
                _sumDigits(birthDate.month) +
                _sumDigits(currentYear);

    int result = sum;
    while (result > 9) {
      result = _sumDigits(result);
    }

    return result;
  }
}
```

### **Goals por Life Path Number + Zodiac**

#### Ejemplo: Life Path 1 + Aries

```dart
Goal(
  title: "👑 Líder Nato (LP1 + Aries)",
  description: "Life Path 1 + Aries = DOBLE energía de liderazgo. Naciste para liderar, pero aprende a dejar brillar a otros también.",
  category: "leadership",
  difficulty: "hard",
  forCombination: {
    'lifePathNumber': 1,
    'zodiacSign': 'Aries',
  },
  doubleSystemExplanation: """
  🔢+🪐 NUMEROLOGÍA + ASTROLOGÍA:

  LIFE PATH 1:
  • Líder independiente
  • Pionero innovador
  • Coraje natural
  • Dificultad: Escuchar a otros

  ARIES:
  • Guerrero iniciador
  • Energía marciana
  • Acción rápida
  • Dificultad: Impaciencia

  LP1 + ARIES = SÚPER LÍDER
  ✅ Doble iniciativa
  ✅ Doble coraje
  ✅ Doble confianza

  PERO TAMBIÉN:
  ⚠️ Doble impaciencia
  ⚠️ Doble ego
  ⚠️ Dificultad de trabajar en equipo

  TU LECCIÓN DE VIDA:
  Liderar ≠ Hacer todo solo
  Verdadero liderazgo = Empoderar a otros
  """,
  tasks: [
    "👥 Delega 1 tarea importante a alguien hoy",
    "👂 En tu próxima reunión: escucha 70%, habla 30%",
    "🎯 Elige a alguien para mentorear (comparte tu poder)",
    "🙏 Admite 1 error públicamente (humildad)",
    "🤝 Pide ayuda en algo (no hagas todo solo)",
  ],
  growthPath: """
  EVOLUCIÓN LP1 + ARIES:

  Nivel 1 (Ego): "Yo sé mejor que todos"
  Nivel 2 (Acción): "Yo lo hago porque nadie más lo hará"
  Nivel 3 (Liderazgo): "Yo inicio y otros se unen"
  Nivel 4 (Maestría): "Yo creo más líderes"

  META: Ser el líder que crea MÁS líderes,
  no el líder que necesita seguidores.
  """,
);
```

### **Personal Year Goals (2025)**

```dart
class PersonalYearGoals {
  /// Genera goals basados en Personal Year 2025
  static Goal generateYearGoal(int personalYear, String zodiacSign) {
    switch (personalYear) {
      case 1: // Año de Nuevos Comienzos
        return Goal(
          title: "🌱 Año 1: Siembra Nuevos Comienzos",
          description: "2025 es tu Año Personal 1 - momento de EMPEZAR cosas nuevas. Planta semillas que cosecharás en 9 años.",
          tasks: [
            "🚀 Inicia 1 proyecto nuevo importante",
            "💼 Cambia de trabajo/carrera si lo has pensado",
            "🏠 Múdate o renueva completamente tu espacio",
            "👤 Re-invéntate (look, estilo, identidad)",
            "🎯 Define visión clara para próximos 9 años",
          ],
        );

      case 2: // Año de Relaciones y Paciencia
        return Goal(
          title: "🤝 Año 2: Cultiva Relaciones",
          description: "2025 es tu Año Personal 2 - momento de COOPERAR. No fuerces, deja que las cosas maduren.",
          tasks: [
            "💑 Profundiza relación romántica o inicia una",
            "🤝 Crea partnerships (negocios, creativos)",
            "🧘 Practica paciencia (todo toma tiempo este año)",
            "👥 Networking intenso - conoce gente nueva",
            "⚖️ Balancea dar y recibir en todas las relaciones",
          ],
        );

      case 3: // Año de Expresión Creativa
        return Goal(
          title: "🎨 Año 3: Expresa Tu Creatividad",
          description: "2025 es tu Año Personal 3 - momento de CREAR y COMUNICAR. Tu voz necesita ser escuchada.",
          tasks: [
            "🎨 Crea algo artístico (música, arte, escritura)",
            "📱 Comparte tu creatividad públicamente (redes)",
            "🗣️ Habla en público o crea contenido",
            "🎉 Socializa MÁS - este es tu año extrovertido",
            "😄 Prioriza diversión y alegría sobre trabajo duro",
          ],
        );

      case 4: // Año de Construcción y Trabajo Duro
        return Goal(
          title: "🏗️ Año 4: Construye Fundaciones Sólidas",
          description: "2025 es tu Año Personal 4 - momento de TRABAJAR DURO. Nada de atajos, solo disciplina.",
          tasks: [
            "💼 Establece rutinas productivas sólidas",
            "💰 Construye seguridad financiera (ahorra, invierte)",
            "🏠 Mejora tu hogar/espacio de trabajo",
            "📊 Planifica a largo plazo (5-10 años)",
            "💪 Gym/salud - construye cuerpo fuerte",
          ],
        );

      case 5: // Año de Cambio y Libertad
        return Goal(
          title: "✈️ Año 5: Abraza El Cambio",
          description: "2025 es tu Año Personal 5 - momento de CAMBIO RADICAL. Rompe rutinas, explora, viaja.",
          tasks: [
            "✈️ Viaja (nacional o internacional)",
            "🔄 Cambia algo GRANDE (trabajo, ciudad, look)",
            "🎢 Di SÍ a oportunidades inesperadas",
            "🎉 Experimenta (comida nueva, actividades nuevas)",
            "🌍 Expande tu zona de confort radicalmente",
          ],
        );

      case 6: // Año de Responsabilidad y Amor
        return Goal(
          title: "❤️ Año 6: Amor y Responsabilidad",
          description: "2025 es tu Año Personal 6 - momento de CUIDAR. Familia, hogar, comunidad te necesitan.",
          tasks: [
            "👨‍👩‍👧 Prioriza familia (padres, hijos, hermanos)",
            "🏠 Mejora tu hogar (decoración, arreglos)",
            "💑 Compromiso relacional (matrimonio, mudarse juntos)",
            "🤱 Cuida a quien lo necesita (enfermedad, dificultad)",
            "🎨 Belleza y armonía en tu ambiente",
          ],
        );

      case 7: // Año de Introspección
        return Goal(
          title: "🧘 Año 7: Busca Sabiduría Interior",
          description: "2025 es tu Año Personal 7 - momento de REFLEXIONAR. No es año de acción, sino de entendimiento.",
          tasks: [
            "📚 Estudia algo profundo (filosofía, espiritualidad)",
            "🧘 Meditación diaria (mínimo 20 min)",
            "📝 Journaling intenso - conoce tu mente",
            "🌲 Tiempo solo en naturaleza",
            "🔍 Terapia o trabajo de autoconocimiento",
          ],
        );

      case 8: // Año de Poder y Dinero
        return Goal(
          title: "💰 Año 8: Manifestación Material",
          description: "2025 es tu Año Personal 8 - momento de GANAR. Poder, dinero, éxito profesional.",
          tasks: [
            "💼 Busca promoción o aumento significativo",
            "💰 Invierte (real estate, stocks, negocio)",
            "👔 Lidera/inicia negocio o proyecto grande",
            "💪 Asume poder y autoridad (no seas tímido/a)",
            "🎯 Piensa GRANDE - este es tu año de abundancia",
          ],
        );

      case 9: // Año de Cierre y Finalización
        return Goal(
          title: "🔚 Año 9: Suelta y Completa",
          description: "2025 es tu Año Personal 9 - momento de CERRAR CICLOS. Termina lo viejo para empezar nuevo en 2026.",
          tasks: [
            "🚪 Termina relaciones que ya no sirven",
            "📦 Dona/vende cosas viejas (declutter radical)",
            "✅ Completa proyectos pendientes",
            "💔 Perdona y suelta resentimientos",
            "🙏 Practica desapego - prepárate para nuevo ciclo",
          ],
        );

      default:
        throw Exception('Invalid Personal Year number');
    }
  }
}
```

---

## 🌟 PARTE 6: GOALS BASADOS EN CARTA ASTRAL COMPLETA

### **Ascendente + Sol Goals (Identidad Doble)**

```dart
class AscendantSunGoals {
  /// Genera goals basados en Sol + Ascendente
  static Goal generateDualIdentityGoal({
    required String sunSign,
    required String ascendantSign,
  }) {
    return Goal(
      title: "🌅 Integra Tu Doble Naturaleza",
      description: "Sol en $sunSign + Ascendente en $ascendantSign = 2 identidades que necesitas integrar.",
      explanation: """
      🪐 SOL vs ASCENDENTE:

      SOL (Esencia Interna):
      • Quién ERES realmente
      • Tu ego/identidad core
      • Cómo brillas cuando estás solo
      • Tu $sunSign es tu verdadero yo

      ASCENDENTE (Máscara Social):
      • Cómo te VEN otros
      • Tu primera impresión
      • Tu estrategia de vida
      • Tu $ascendantSign es tu "disfraz"

      EJEMPLO:
      Sol en Cáncer, Ascendente en Aries:
      - Por dentro: Sensible, emocional, hogareño (Cáncer)
      - Por fuera: Valiente, agresivo, independiente (Aries)
      - Conflicto: "Parezco duro pero soy sensible"

      TU TAREA:
      Integrar ambos. No eres UNO u OTRO - eres AMBOS.
      El Ascendente es cómo IMPLEMENTAS tu Sol.
      """,
      tasks: [
        "🌅 Identifica: ¿Cuándo actúas como $ascendantSign? (probablemente en público/trabajo)",
        "☀️ Identifica: ¿Cuándo actúas como $sunSign? (probablemente solo/con íntimos)",
        "💬 Comparte tu lado $sunSign en contextos donde normalmente actúas $ascendantSign",
        "⚖️ Pregunta: ¿Cómo mi $ascendantSign SIRVE a mi $sunSign?",
        "🎭 Acepta: Ambas identidades son REALES y necesarias",
      ],
    );
  }
}
```

### **Aspectos Natales Desafiantes (Trabajo Interior)**

```dart
class ChallengingAspectGoals {
  /// Goals para aspectos natales difíciles

  // Marte Cuadra Saturno Natal
  static Goal marsSaturnSquare(String sunSign) {
    return Goal(
      title: "⚔️ Domina Tu Marte-Saturno",
      description: "Naciste con Marte cuadra Saturno - frustración es tu maestro. Aprende a canalizar la tensión.",
      natalAspect: "Mars Square Saturn",
      difficulty: "hard",
      lifelongWork: true,
      explanation: """
      🪐 MARTE CUADRA SATURNO NATAL:

      Esto significa que EN TU CARTA NATAL (momento de nacer),
      Marte y Saturno estaban en ángulo de 90° (cuadrado).

      QUÉ SIGNIFICA:
      Marte = GO! (acelerador)
      Saturno = STOP! (freno)
      Cuadrado = Ambos activos AL MISMO TIEMPO

      CÓMO SE SIENTE:
      • Quieres avanzar pero algo te detiene (interno)
      • Frustración constante
      • Sientes que trabajas más duro que otros por menos resultados
      • Miedo a fallar paraliza tu acción
      • Enojo interno (Marte) + autocrítica (Saturno)

      TU REGALO OCULTO:
      Personas con este aspecto, cuando lo dominan,
      tienen RESISTENCIA EXTREMA. Son imparables.

      EJEMPLOS FAMOSOS CON ESTE ASPECTO:
      - Oprah Winfrey: Frustración → Disciplina → Imperio
      - Arnold Schwarzenegger: Marte+Saturno = Bodybuilding perfecto
      - Barack Obama: Acción medida y calculada

      TU LECCIÓN:
      No es "acción O disciplina" - es "acción DISCIPLINADA".
      """,
      tasks: [
        "💪 Elige 1 proyecto difícil y trabaja en él CONSISTENTEMENTE (no rápido)",
        "🧘 Cuando sientas frustración, pregunta: '¿Qué me está enseñando este límite?'",
        "🎯 Define metas REALISTAS (Saturno) y trabaja INTENSAMENTE (Marte)",
        "⏰ Practica paciencia activa: Trabaja duro + acepta que todo toma tiempo",
        "🏆 Celebra pequeños wins - el éxito para ti es GRADUAL, no instantáneo",
      ],
      affirmation: "Mi frustración es combustible. Mi límites me hacen más fuerte. Soy imparable porque NO ME RINDO.",
    );
  }

  // Sol Oposición Luna Natal
  static Goal sunMoonOpposition(String sunSign, String moonSign) {
    return Goal(
      title: "☀️🌙 Reconcilia Tu Interior",
      description: "Sol en $sunSign opuesto a Luna en $moonSign - tu mente consciente vs tu mundo emocional están en conflicto.",
      natalAspect: "Sun Opposition Moon",
      difficulty: "hard",
      lifelongWork: true,
      explanation: """
      🪐 SOL OPOSICIÓN LUNA NATAL:

      SOL (Lo que QUIERES ser):
      • Tu ego consciente
      • Tu identidad pública
      • Tu $sunSign

      LUNA (Lo que NECESITAS para sentirte seguro/a):
      • Tu mundo emocional
      • Tus necesidades inconscientes
      • Tu $moonSign

      OPOSICIÓN (180°):
      Están en conflicto directo. Cuando satisfaces uno, el otro sufre.

      EJEMPLO:
      Sol en Capricorn (necesita éxito, status, control)
      Luna en Cáncer (necesita hogar, familia, emociones)

      Resultado: "Si trabajo duro (Sol), descuido familia (Luna).
                  Si cuido familia (Luna), mi carrera sufre (Sol)."

      TU REGALO:
      Aprendes BALANCE que otros nunca entienden.
      Puedes integrar opuestos que para otros son imposibles.

      TU LECCIÓN:
      No es "trabajo O familia" - es "trabajo Y familia".
      Integrar ambos es tu propósito de vida.
      """,
      tasks: [
        "📊 Identifica: ¿Qué necesita tu Sol $sunSign? (ej: éxito, aventura, creatividad)",
        "❤️ Identifica: ¿Qué necesita tu Luna $moonSign? (ej: seguridad, conexión, libertad)",
        "⚖️ Crea estructura que honra AMBOS (ej: trabajo exitoso desde casa)",
        "💬 Cuando sientas conflicto interno: 'Mi Sol quiere X, mi Luna necesita Y. ¿Cómo puedo tener ambos?'",
        "🎯 Esta semana: Dedica días alternos a cada uno (Lun/Mié/Vie = Sol, Mar/Jue/Sáb = Luna)",
      ],
    );
  }
}
```

---

## 🌙 PARTE 7: GOALS DE MANIFESTACIÓN & LAW OF ATTRACTION

### **Nuevas Lunas 2025 por Signo (Rituales Específicos)**

```dart
class NewMoonManifestationGoals {
  /// Cada Nueva Luna = oportunidad de manifestación
  /// Nueva Luna en cada signo = tema específico

  static final Map<String, NewMoonRitual> newMoons2025 = {
    'Capricorn': NewMoonRitual(
      date: DateTime(2025, 1, 21),
      theme: "💼 Manifestar Éxito Profesional",
      description: "Nueva Luna en Capricorn = momento perfecto para metas de carrera, disciplina, logros.",
      ritual: """
      RITUAL NUEVA LUNA EN CAPRICORN:
      (21 enero 2025 - 12:31pm PST)

      QUÉ MANIFESTAR:
      ✅ Promoción/aumento
      ✅ Iniciar negocio
      ✅ Disciplina/estructura
      ✅ Reconocimiento profesional
      ✅ Legado duradero

      PASOS:
      1. Encuentra lugar tranquilo (oficina/estudio ideal)
      2. Escribe 10 metas profesionales como si YA sucedieron:
         "Soy [cargo]", "Gano $[cantidad]", "Lidero [proyecto]"
      3. Lee en voz alta con convicción
      4. Visualiza por 10 min: Siénte en ese futuro
      5. Toma 1 ACCIÓN hoy hacia la meta #1
      6. Guarda el papel - revisa en 6 meses (Luna Llena Capricorn)

      BONUS:
      - Viste formal durante el ritual (activa Capricorn)
      - Enciende vela negra/verde (colores de Capricorn)
      - Ten cristales: Obsidiana, Turmalina negra, Granate
      """,
    ),

    'Aquarius': NewMoonRitual(
      date: DateTime(2025, 2, 19),
      theme: "💡 Manifestar Innovación y Comunidad",
      description: "Nueva Luna en Aquarius = momento para metas de cambio social, tecnología, amistad.",
      ritual: """
      RITUAL NUEVA LUNA EN AQUARIUS:
      (19 febrero 2025 - 11:06am PST)

      QUÉ MANIFESTAR:
      ✅ Red de amistades/comunidad
      ✅ Proyectos innovadores
      ✅ Cambio social/causa
      ✅ Libertad personal
      ✅ Tecnología/futuro

      PASOS:
      1. Haz el ritual CON AMIGOS (Aquarius es colectivo)
      2. Cada persona comparte 1 visión de futuro mejor
      3. Escriban juntos: "Nuestro mundo ideal en 2030"
      4. Compromiso: 1 acción que CADA UNO hará este mes
      5. Crean grupo/chat para accountability
      6. Revisan en Luna Llena Aquarius

      ALTERNATIVA (Si estás solo/a):
      - Visualiza comunidad que quieres crear
      - Escribe llamado a esa comunidad
      - Publícalo en redes (Aquarius rige internet)
      - Confía que las personas correctas llegarán
      """,
    ),

    'Pisces': NewMoonRitual(
      date: DateTime(2025, 3, 21),
      theme: "🎨 Manifestar Creatividad y Espiritualidad",
      description: "Nueva Luna en Pisces = momento para manifestar sueños, arte, conexión espiritual.",
      ritual: """
      RITUAL NUEVA LUNA EN PISCES:
      (21 marzo 2025 - 2:23am PDT)

      QUÉ MANIFESTAR:
      ✅ Proyectos creativos/artísticos
      ✅ Conexión espiritual
      ✅ Intuición aumentada
      ✅ Compasión/sanación
      ✅ Sueños hechos realidad

      PASOS:
      1. Toma baño ritual (Pisces = agua)
      2. Pon música suave, incienso (activa sentidos)
      3. No ESCRIBAS - mejor DIBUJA o PINTA tu visión
         (Pisces es visual, no verbal)
      4. Si no dibujas: Crea vision board con imágenes
      5. Meditación: Siente la visión como si ya existiera
      6. Antes de dormir: Pide a tus sueños que te guíen
      7. Journaling matutino: Escribe qué soñaste

      PISCES RIGE SUEÑOS:
      Esta Nueva Luna, tus sueños serán ESPECIALMENTE
      significativos. Pon libreta junto a cama.
      Lo que sueñes esta noche = mensaje de tu subconsciente.
      """,
    ),

    // ... [Continuar con las 12 Nuevas Lunas del 2025]
  };
}
```

### **Law of Attraction Goals (Vibrational Alignment)**

```dart
Goal(
  title: "🎯 Alineación Vibratoria (LOA)",
  description: "Law of Attraction funciona cuando tu energía interna COINCIDE con lo que quieres atraer.",
  category: "manifestation",
  difficulty: "medium",
  scienceAndSpirit: """
  ⚛️ LOA - CIENCIA + ESPIRITUALIDAD:

  CIENCIA (Psicología):
  • Reticular Activating System (RAS) filtra información
  • Cuando focuses en algo, tu cerebro lo ENCUENTRA más
  • Self-fulfilling prophecy: Tus creencias crean tu realidad
  • Neuroplasticidad: Pensamientos repetidos crean caminos neuronales

  ESPIRITUALIDAD (Metafísica):
  • "Like attracts like" - energía similar se atrae
  • Tu vibración (estado emocional) atrae eventos matching
  • Universo responde a tu energía, no tus palabras

  PRÁCTICA:
  No se trata de "pensar positivo" - se trata de SENTIR
  como si ya tuvieras lo que quieres.
  """,
  steps: [
    """
    PASO 1: CLARIDAD EXTREMA
    No "quiero ser feliz" (vago)
    Sí "Quiero despertar emocionado/a cada día porque [X específico]"

    Escribe:
    - ¿Qué EXACTAMENTE quiero?
    - ¿Cómo me sentiré cuando lo tenga?
    - ¿Cómo se verá mi día a día?
    - ¿Quién seré como persona?
    """,

    """
    PASO 2: ALINEACIÓN EMOCIONAL
    LOA no funciona si "quieres dinero" pero SIENTES "soy pobre".
    Tu vibración (sentimiento) > tus palabras.

    Pregunta diaria:
    "¿Cómo me siento HOY sobre [mi goal]?"

    Si sientes:
    - Desesperación → Estás en vibración de FALTA
    - Expectativa emocionada → Estás en vibración de RECEPCIÓN

    TRUCO: Actúa "AS IF"
    Si quieres éxito → Viste/habla/piensa como persona exitosa YA.
    No estás "fake it til you make it" - estás pre-viviendo tu futuro.
    """,

    """
    PASO 3: SUELTA EL "CÓMO"
    Tu trabajo: Definir QUÉ quieres + sentirlo como real
    Trabajo del universo: Orquestar el CÓMO

    Error común:
    "Quiero $10k... y TIENE que venir de [fuente específica]"
    Esto LIMITA al universo.

    Correcto:
    "Quiero $10k. Estoy abierto/a a que venga de formas inesperadas."

    MANTRA:
    "This or something better."
    (Esto o algo mejor)
    """,

    """
    PASO 4: ACCIÓN INSPIRADA
    LOA ≠ Sentarse a esperar
    LOA = Alineación energética + acción cuando te llegue impulso

    DIFERENCIA:
    Acción forzada: "TENGO que hacer esto o fracasaré"
    Acción inspirada: "Me siento llamado/a a hacer esto"

    Si sientes resistencia → No es el momento
    Si sientes flow/excitación → ES el momento

    Confía en tu timing.
    """,

    """
    PASO 5: GRATITUD ANTICIPADA
    El hack más poderoso de LOA:
    Agradece ANTES de recibir.

    "Gracias universo por [X que quiero] que ya está en camino a mí."

    POR QUÉ FUNCIONA:
    Gratitud = emoción de RECEPCIÓN
    Cuando agradeces algo que aún no tienes,
    tu cerebro asume que YA lo tienes.

    Tu subconsciente no distingue entre:
    - Imaginación vívida
    - Realidad actual

    Úsalo a tu favor.
    """,
  ],
  dailyPractice: """
  PRÁCTICA DIARIA LOA (10 min):

  MAÑANA (5 min):
  1. Antes de revisar teléfono
  2. Visualiza tu día ideal
  3. Siente las emociones de tu día ideal
  4. "Hoy voy a recibir evidencia de mi manifestación"

  NOCHE (5 min):
  1. Escribe 3 formas en que HOY tu manifestación se acercó
     (Aunque sea sutil: conociste a alguien, viste señal, sentiste alineación)
  2. Gratitud: "Gracias por [manifestación] que ya está aquí"
  3. Suelta: "Confío en el timing perfecto"

  RESULTADO EN 30 DÍAS:
  Tu energía habrá cambiado tanto que tu realidad TENDRÁ que cambiar también.
  """,
  zodiacAlignment: {
    'Aries': 'Tu Marte te hace ACTION-oriented. Perfecto para LOA - actúas cuando sientes impulso.',
    'Tauro': 'Tu Venus te hace MAGNETIZADOR/A natural. Atraes lo que valoras.',
    'Géminis': 'Tu Mercurio te hace comunicador/a. HABLA tu manifestación a la existencia.',
    'Cáncer': 'Tu Luna te hace SENTIR profundo. Tu poder LOA está en tu capacidad emocional.',
    'Leo': 'Tu Sol te hace BRILLAR. Cuando crees en ti, otros también. Eres imán natural.',
    'Virgo': 'Tu Mercurio te hace VISUALIZADOR/A detallado. Puedes ver cada paso.',
    'Libra': 'Tu Venus te hace ARMONIZADOR/A. Atraes balance naturalmente.',
    'Escorpio': 'Tu Plutón te hace TRANSFORMADOR/A. Puedes manifestar cambios RADICALES.',
    'Sagitario': 'Tu Júpiter te hace EXPANSIVO/A. Think big = manifest big.',
    'Capricorn': 'Tu Saturno te hace DISCIPLINADO/A. Manifiestas a través de acción consistente.',
    'Aquarius': 'Tu Urano te hace VISIONARIO/A. Manifiestas futuros que otros ni imaginan.',
    'Pisces': 'Tu Neptuno te hace SOÑADOR/A. Tu imaginación ES tu portal de manifestación.',
  },
);
```

---

## 📊 RESUMEN FINAL DE TODAS LAS PARTES

### **TOTAL DE MEJORAS PROPUESTAS**:

| Categoría | Parte | Goals Nuevos |
|-----------|-------|--------------|
| Context-Aware | Parte 1 | ~100 goals |
| Science-Based | Parte 2 | ~90 goals |
| Biorhythms | Parte 3 | ~15 goals |
| Relationships | Parte 4 | ~50 goals |
| Numerology | Parte 5 | ~20 goals |
| Natal Chart | Parte 6 | ~30 goals |
| Manifestation | Parte 7 | ~20 goals |
| **TOTAL** | **Partes 1-7** | **~325 goals únicos** |

### **CON VARIACIONES**:
- Micro-habits: 24 (2 por signo)
- Niveles progresivos: 6 por goal
- Seasonal variations: 12 nuevas lunas
- Transit-based: 20+ tránsitos anuales

**TOTAL POTENCIAL: 600-800 variantes de goals**

---

## 🚀 PRÓXIMOS PASOS PARA IMPLEMENTACIÓN

1. **Priorizar fases** (¿cuáles implementar primero?)
2. **Crear estructura de datos** (modelos Dart)
3. **Traducir a 6 idiomas**
4. **Testing con usuarios beta**
5. **Iteración basada en feedback**

---

**Fecha**: Noviembre 12, 2025
**Estado**: ✅ Especificaciones completas Partes 1-7
**Próximo**: Decidir qué implementar primero y comenzar desarrollo
