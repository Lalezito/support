# 🧠 COSMIC COACH - MEJORAS AVANZADAS PARTE 2
## Noviembre 12, 2025 - Especificaciones Detalladas

---

## 🔬 PARTE 1: GOALS BASADOS EN CIENCIA REAL

### **Categoría: Salud & Longevidad** (Harvard Study 2025)

Estudio de Harvard siguió 100,000+ personas por décadas y encontró que 5 hábitos específicos agregan 12-14 años de vida:

#### 1. **Goal: "💜 Power Foods Morados"**
```dart
Goal(
  title: "💜 Antioxidantes Poderosos",
  description: "Come 1 alimento morado hoy: arándanos, col morada, berenjena o moras. Los antocianinas son antioxidantes anti-inflamatorios y protegen el cerebro.",
  category: "nutrition",
  difficulty: "easy",
  scienceProof: """
  📊 ESTUDIO 2025: Purple foods contienen antocianinas - antioxidantes
  con propiedades anti-inflamatorias y neuroprotectoras.

  Beneficios comprobados:
  • Reducen inflamación (medido por proteína C-reactiva)
  • Mejoran memoria y función cognitiva
  • Protegen contra enfermedades cardíacas
  • Reducen riesgo de diabetes tipo 2

  APLICACIÓN PRÁCTICA: 1 porción = 1 taza de arándanos,
  media taza de col morada, o 1 berenjena mediana.
  """,
  zodiacConnection: {
    'Tauro': 'Tu conexión con la tierra te hace apreciar alimentos naturales y coloridos. Estos alimentos activan tu Venus interno.',
    'Virgo': 'Tu atención a la salud perfecta se alinea con nutrición científica. Este hábito optimiza tu Mercurio sanador.',
    'Capricorn': 'Tu disciplina saturnina convierte este simple hábito en longevidad real. 1 decisión diaria = años de vida.',
  },
  microHabits: [
    MicroHabit(
      habit: "Agrega arándanos al desayuno",
      when: "Cada mañana al preparar tu primera comida",
      why: "Antocianinas se absorben mejor en ayunas",
      difficulty: HabitDifficulty.easy,
    ),
    MicroHabit(
      habit: "Snack de col morada + hummus",
      when: "Cuando tengas hambre entre comidas (3pm ideal)",
      why: "Combate el bajón de energía de la tarde con nutrientes reales",
      difficulty: HabitDifficulty.easy,
    ),
  ],
  successMetrics: [
    "Comiste 1 alimento morado hoy",
    "Sentiste más energía en la tarde",
    "Lo convertiste en hábito (7 días seguidos)",
  ],
);
```

#### 2. **Goal: "🫀 Monitorea Tu HRV (Heart Rate Variability)"**
```dart
Goal(
  title: "🫀 Mide Tu Estrés Real",
  description: "Usa tu Apple Watch o Fitbit para medir tu HRV (Heart Rate Variability). HRV alto = mejor manejo de estrés.",
  category: "biohacking",
  difficulty: "medium",
  scienceProof: """
  📊 CIENCIA 2025: HRV mide la variación entre latidos del corazón.

  HRV ALTO (bueno):
  • >50ms en promedio = sistema nervioso resiliente
  • Mejor recuperación de estrés
  • Mayor capacidad de adaptación

  HRV BAJO (alerta):
  • <30ms = sistema nervioso sobrecargado
  • Necesitas descanso, no más esfuerzo
  • Riesgo de burnout

  CÓMO MEJORARLO:
  1. Meditación (sube HRV 10-20% en 8 semanas)
  2. Ejercicio moderado (no intenso cuando HRV está bajo)
  3. Sueño de calidad (7-9 horas)
  4. Respiración 4-7-8 (4 seg inhala, 7 retén, 8 exhala)
  """,
  zodiacConnection: {
    'Aries': 'Tu Marte te empuja a ir duro siempre. HRV te dice CUÁNDO descansar - no es debilidad, es estrategia.',
    'Escorpio': 'Tu intensidad plutoniana agota tu sistema nervioso. HRV es tu ventana a lo invisible - tus límites reales.',
    'Capricorn': 'Tu disciplina saturnina puede llevarte al burnout. HRV te permite optimizar rendimiento SIN quebrarte.',
  },
  requiredDevices: ['Apple Watch', 'Fitbit', 'Oura Ring', 'Whoop'],
  microHabits: [
    MicroHabit(
      habit: "Revisa tu HRV cada mañana",
      when: "Inmediatamente al despertar (antes de levantarte de la cama)",
      why: "HRV matutino es el indicador más confiable de tu estado",
      difficulty: HabitDifficulty.easy,
    ),
    MicroHabit(
      habit: "Si HRV <30: día de recuperación (yoga, meditación, caminar)",
      when: "Cuando veas HRV bajo en la app",
      why: "Forzar entrenamientos intensos con HRV bajo causa más daño que beneficio",
      difficulty: HabitDifficulty.medium,
    ),
    MicroHabit(
      habit: "Si HRV >50: día de alta performance (puedes ir duro)",
      when: "Cuando veas HRV alto",
      why: "Tu cuerpo está listo para máximo rendimiento",
      difficulty: HabitDifficulty.medium,
    ),
  ],
);
```

#### 3. **Goal: "🧘 Gratitud Científica (Reduce Cortisol 23%)"**
```dart
Goal(
  title: "🙏 Gratitud Anti-Estrés",
  description: "Escribe 3 cosas por las que estás agradecido/a hoy. Reduce cortisol (hormona del estrés) en 23% y re-cablea tu cerebro.",
  category: "mindfulness",
  difficulty: "easy",
  scienceProof: """
  📊 NEUROCIENCIA 2025: Gratitud cambia estructura cerebral.

  BENEFICIOS MEDIDOS:
  • ↓23% cortisol (hormona del estrés)
  • ↓Síntomas de ansiedad y depresión
  • ↑Actividad en corteza prefrontal (área de decisiones)
  • ↑Dopamina y serotonina naturales

  TIEMPO PARA VER RESULTADOS:
  • 21 días = cambios notorios en mood
  • 66 días = hábito automático
  • 6 meses = cambios estructurales en cerebro (visible en fMRI)

  POR QUÉ FUNCIONA:
  El cerebro tiene "negativity bias" (sesgo de negatividad) por evolución.
  Gratitud ENTRENA al cerebro a buscar lo positivo - literalmente
  crea nuevas conexiones neuronales.
  """,
  zodiacConnection: {
    'Cáncer': 'Tu sensibilidad lunar necesita nutrición emocional. Gratitud es alimento para tu alma.',
    'Libra': 'Tu Venus rige la apreciación y la belleza. Gratitud activa tu superpoder natural.',
    'Pisces': 'Tu conexión neptuniana con lo divino se profundiza con gratitud. Es tu portal espiritual.',
  },
  microHabits: [
    MicroHabit(
      habit: "3 gratitudes cada noche antes de dormir",
      when: "En la cama, antes de cerrar los ojos",
      why: "Última cosa que piensas antes de dormir afecta tu sueño y sueños",
      difficulty: HabitDifficulty.easy,
    ),
    MicroHabit(
      habit: "Sé ESPECÍFICO (no 'familia' sino 'cuando mi mamá me abrazó hoy')",
      when: "Al escribir cada gratitud",
      why: "Especificidad activa más áreas cerebrales = mayor impacto",
      difficulty: HabitDifficulty.medium,
    ),
  ],
  progressionLevels: {
    'Nivel 1 (Días 1-7)': 'Escribe 3 gratitudes',
    'Nivel 2 (Días 8-21)': 'Escribe 3 gratitudes + POR QUÉ te importa',
    'Nivel 3 (Días 22-66)': 'Escribe 3 gratitudes + revisa gratitudes de ayer',
    'Nivel 4 (66+ días)': 'Gratitud en voz alta + comparte 1 con alguien',
  },
);
```

---

## 🌌 PARTE 2: GOALS BASADOS EN TRÁNSITOS ASTROLÓGICOS REALES (NOV-DIC 2025)

### **Transit 1: Mercurio Retrógrado (Nov 9 - Nov 29, 2025)**

**Dato Astrológico Real**:
- Inicia: Nov 9, 2025 a las 2:01pm EST en 6°51 Sagitario
- Retrocede a Escorpio: Nov 18
- Vuelve directo: Nov 29
- Sale de shadow: Dic 16

#### Goal: "🔄 Re-Vision Quest (Mercurio Retrógrado)"
```dart
Goal(
  title: "🔄 Temporada de RE-hacer",
  description: "Mercurio retrógrado (Nov 9-29). Perfecto para RE-visar, RE-hacer, RE-conectar. NO para empezar cosas nuevas.",
  category: "astro_timing",
  difficulty: "medium",
  activeFrom: DateTime(2025, 11, 9),
  activeUntil: DateTime(2025, 11, 29),
  astroExplanation: """
  🪐 ASTROLOGÍA REAL:

  Mercurio retrógrado ocurre 3-4 veces al año cuando Mercurio
  aparentemente "retrocede" desde la Tierra.

  QUÉ RIGE MERCURIO:
  • Comunicación (hablar, escribir, emails)
  • Tecnología (computadoras, celulares, apps)
  • Viajes cortos y transporte
  • Contratos y documentos legales
  • Pensamiento lógico y decisiones

  POR QUÉ "RE-":
  Cuando un planeta retrograda, su energía se voltea HACIA ADENTRO.
  Es momento de RE-visión, no de avance nuevo.

  LO QUE FUNCIONA BIEN:
  ✅ RE-conectar con ex amigos/colegas (no parejas románticas)
  ✅ RE-visar proyectos antiguos y perfeccionarlos
  ✅ RE-escribir, RE-editar, RE-diseñar
  ✅ RE-solver problemas pendientes
  ✅ RE-flexionar sobre decisiones importantes
  ✅ RE-cuperar archivos borrados o información olvidada

  LO QUE CAUSA PROBLEMAS:
  ❌ Firmar contratos importantes (espera hasta dic 16)
  ❌ Comprar electrónicos caros (o guarda recibo)
  ❌ Empezar negocios nuevos
  ❌ Lanzar productos/servicios
  ❌ Hacer declaraciones de amor importantes
  ❌ Tomar decisiones de vida mayores

  MOMENTO MÁGICO:
  Nov 20, 2025 1:23am PT - Mercury Cazimi (28°18 Escorpio)
  = momento de máxima claridad en medio del caos.
  Toma nota de insights que lleguen ese día.
  """,
  zodiacConnection: {
    'Géminis': 'TÚ eres regido por Mercurio. Este retrógrado te afecta MÁS. Usa este tiempo para procesar información acumulada.',
    'Virgo': 'También eres de Mercurio. Tu atención al detalle brilla en retrógrado - encuentra errores que otros perdieron.',
    'Sagitario': 'Retrógrado empieza EN TU SIGNO. Re-evalúa tus creencias y filosofía de vida.',
    'Escorpio': 'Retrógrado termina en tu signo. Secretos salen a la luz - úsalo para sanación profunda.',
  },
  tasksForRetrograde: [
    "📧 Limpia tu inbox (llega a 0)",
    "🗄️ Organiza archivos digitales viejos",
    "👥 Contacta a 3 amigos con quien perdiste contacto",
    "📝 Re-lee y edita proyectos pendientes",
    "🔧 Haz backup de toda tu data importante",
    "📱 Actualiza contraseñas y seguridad digital",
    "🧹 Termina proyectos incompletos (no empiecesnuevos)",
    "💬 Ten conversaciones pendientes importantes",
  ],
);
```

### **Transit 2: Venus en Escorpio (Nov 6-30) → Venus en Sagitario (Nov 30+)**

#### Goal: "💖 Venus Transit Power Move"
```dart
Goal(
  title: "💖 Transformación de Amor",
  description: "Venus en Escorpio (hasta Nov 30) = amor profundo e intenso. Venus en Sagitario (Nov 30+) = aventura y expansión.",
  category: "relationships",
  difficulty: "medium",
  activeFrom: DateTime(2025, 11, 6),
  activeUntil: DateTime(2025, 12, 31),
  astroExplanation: """
  🪐 VENUS EN ESCORPIO (Nov 6-30, 2025):

  Venus (planeta del amor, belleza, valores) en Escorpio
  (signo de profundidad, transformación, intensidad).

  ENERGÍA:
  • Amor ALL-IN o nada
  • Intensidad emocional en relaciones
  • Deseo de fusión profunda
  • Celos y posesividad pueden surgir
  • Momento perfecto para terapia de pareja
  • Transformar relaciones superficiales en profundas

  BEST PARA:
  ✅ Conversaciones difíciles en relaciones
  ✅ Sanación de heridas relacionales
  ✅ Compromiso profundo (matrimonio, mudarse juntos)
  ✅ Terapia sexual/intimidad
  ✅ Trabajo de shadow en amor
  ✅ Eliminar relaciones tóxicas

  ---

  🪐 VENUS EN SAGITARIO (Nov 30 - Dic 24, 2025):

  Venus en Sagitario = amor ligero, aventurero, expansivo.

  ENERGÍA:
  • Libertad en amor
  • Aventuras con tu pareja
  • Conocer gente nueva
  • Honestidad brutal pero refrescante
  • Optimismo en relaciones
  • Deseo de explorar juntos

  BEST PARA:
  ✅ Primeras citas y nuevas relaciones
  ✅ Viajes con tu pareja
  ✅ Probar cosas nuevas juntos
  ✅ Conversaciones filosóficas profundas
  ✅ Darle espacio a la relación
  ✅ Aventuras sexuales consensuadas
  """,
  tasksByPhase: {
    'Venus en Escorpio (hasta Nov 30)': [
      "💬 Ten 1 conversación difícil pero necesaria",
      "🔥 Profundiza intimidad (emocional o física)",
      "🩹 Sana 1 herida relacional vieja",
      "🚫 Corta 1 relación que ya no sirve",
      "💎 Invierte en tu relación principal (tiempo de calidad)",
    ],
    'Venus en Sagitario (Nov 30+)': [
      "✈️ Planea una aventura con tu pareja",
      "📚 Aprende algo nuevo juntos",
      "🎯 Date espacio mutuamente (independencia saludable)",
      "🌍 Conoce gente nueva (social, no romántico)",
      "🎉 Haz algo espontáneo y divertido",
    ],
  },
  zodiacMostAffected: [
    'Tauro', // Regido por Venus
    'Libra', // Regido por Venus
    'Escorpio', // Venus EN tu signo (Nov 6-30)
    'Sagitario', // Venus EN tu signo (Nov 30+)
  ],
);
```

### **Transit 3: Marte Cuadra Saturno (Dic 8, 2025)**

#### Goal: "⚔️ Frustración Productiva (Marte-Saturno)"
```dart
Goal(
  title: "⚔️ Canaliza Frustración en Acción",
  description: "Dic 8: Marte cuadra Saturno. Sentirás frustración/bloqueos. NO explotes - canalízalo en trabajo productivo.",
  category: "astro_challenge",
  difficulty: "hard",
  activeFrom: DateTime(2025, 12, 5), // 3 días antes
  activeUntil: DateTime(2025, 12, 11), // 3 días después
  astroExplanation: """
  🪐 TRÁNSITO DESAFIANTE:

  Dic 8, 2025: Marte (25°15 Sagitario) ⚔️ Saturno (25°15 Piscis)

  QUÉ SIGNIFICA:
  Marte = acción, drive, impulso, energía guerrera
  Saturno = límites, restricciones, disciplina, estructura
  Cuadrado (90°) = aspecto de FRICCIÓN y desafío

  LO QUE SENTIRÁS:
  • Frustración extrema
  • Querer avanzar pero sentir muros
  • Impulso de explotar o renunciar
  • Energía bloqueada y estancada
  • Impaciencia con procesos lentos
  • Ganas de romper reglas/límites

  ERRORES COMUNES:
  ❌ Explotar con alguien (jefe, pareja, familia)
  ❌ Renunciar a proyectos importantes
  ❌ Tomar decisiones impulsivas
  ❌ Manejar agresivamente
  ❌ Empezar peleas

  CÓMO USARLO BIEN:
  ✅ Trabajo físico INTENSO (gym, correr, construcción)
  ✅ Proyectos que requieren RESISTENCIA
  ✅ Tareas difíciles que postergaste
  ✅ Disciplina extrema (ayuno, reto fitness)
  ✅ Romper límites PROPIOS (no externos)

  MANTRA:
  "Esta frustración es COMBUSTIBLE, no una señal de rendirme.
  Saturno me enseña MAESTRÍA a través de la resistencia."
  """,
  strategyBySign: {
    'Aries': 'Tu Marte está frustrado. Canaliza en un desafío físico extremo (marathon training, crossfit, escalada).',
    'Escorpio': 'Tu co-regente Marte siente el bloqueo. Usa la energía para transformación profunda (rompe un patrón viejo).',
    'Sagitario': 'Marte está EN TU SIGNO - mucha energía pero bloqueada. Viaje corto o aprende algo que requiere esfuerzo.',
    'Piscis': 'Saturno está EN TU SIGNO - límites son tu maestro. Acepta restricciones y trabaja DENTRO de ellas.',
    'Géminis': 'Cuadrado te afecta (Mutable cross). Enfócate en UNA cosa, no disperses energía.',
    'Virgo': 'También en el cross mutable. Tu perfeccionismo + frustración = burnout. Acepta lo "suficientemente bueno".',
    'Capricorn': 'Saturno es TU regente. Tienes ventaja - eres experto en frustración productiva. Guía a otros.',
  },
  warningTasks: [
    "🚫 NO tomes decisiones de carrera este día",
    "🚫 NO tengas conversaciones difíciles (espera 3 días)",
    "🚫 NO manejes si estás enojado/a",
    "🚫 NO bebas alcohol en exceso (desinhibe agresión)",
  ],
  productiveTasks: [
    "💪 Workout DURO (2 horas+)",
    "📦 Proyecto físico (limpiar garage, mover muebles, construcción)",
    "📊 Tarea aburrida pero necesaria que has postergado",
    "🧗 Desafío físico (escalada, hiking difícil, clase intensa)",
    "🎯 Meta difícil que requiere disciplina extrema (empezar ayuno, quit smoking)",
  ],
);
```

---

## 🎯 PARTE 3: MICRO-HABITS INTELIGENTES (Modelo "Habit Stacking")

### **Concepto: Habit Stacking de BJ Fogg (Stanford)**

Basado en el libro "Tiny Habits" del Dr. BJ Fogg de Stanford:
- Pequeños hábitos son más efectivos que grandes cambios
- "After I [EXISTING HABIT], I will [NEW TINY HABIT]"
- Celebración inmediata refuerza el hábito

#### Micro-Habit Generator por Signo:

```dart
class ZodiacMicroHabits {
  // ARIES (Energía Física)
  static List<MicroHabit> ariesHabits = [
    MicroHabit(
      habit: "10 jumping jacks al despertar",
      when: "Después de apagar la alarma, antes de revisar el teléfono",
      why: "Activa tu Marte inmediatamente - sets the tone del día",
      difficulty: HabitDifficulty.easy,
      celebration: "Grita '¡SÍ!' con los brazos arriba después",
    ),
    MicroHabit(
      habit: "Pausa de 3 respiraciones antes de responder cuando estés molesto/a",
      when: "Cuando sientas impulso de reaccionar agresivamente",
      why: "Marte necesita 3 segundos para que corteza prefrontal tome control",
      difficulty: HabitDifficulty.medium,
      celebration: "Nota cómo tu respuesta fue más efectiva",
    ),
  ];

  // TAURO (Placer Sensorial)
  static List<MicroHabit> taurusHabits = [
    MicroHabit(
      habit: "Huele tu café/té antes de beber",
      when: "Cada mañana al preparar tu bebida",
      why: "Activa tu Venus sensorial - placer consciente",
      difficulty: HabitDifficulty.easy,
      celebration: "Sonríe y di 'mmm' en voz alta",
    ),
    MicroHabit(
      habit: "Toca algo con textura agradable (planta, tela suave)",
      when: "Cada vez que te sientas ansioso/a",
      why: "Tu elemento Tierra necesita contacto táctil para grounding",
      difficulty: HabitDifficulty.easy,
      celebration: "Nota cómo la ansiedad baja",
    ),
  ];

  // GÉMINIS (Curiosidad Mental)
  static List<MicroHabit> geminiHabits = [
    MicroHabit(
      habit: "Lee 1 página de algo interesante",
      when: "Mientras esperas (fila, uber, cita médica)",
      why: "Alimenta tu Mercurio insaciable con micro-learning",
      difficulty: HabitDifficulty.easy,
      celebration: "Comparte 1 fact interesante que aprendiste",
    ),
    MicroHabit(
      habit: "Finish 1 thought antes de empezar otro",
      when: "En conversaciones, cuando quieras interrumpir",
      why: "Entrena a tu Mercurio hiperactivo a tener ENFOQUE",
      difficulty: HabitDifficulty.hard,
      celebration: "Nota cómo la otra persona te escucha más",
    ),
  ];

  // CÁNCER (Conexión Emocional)
  static List<MicroHabit> cancerHabits = [
    MicroHabit(
      habit: "Di 'te amo' o 'te aprecio' a 1 persona",
      when: "Cada noche antes de dormir",
      why: "Tu Luna necesita expresar cariño - es tu naturaleza",
      difficulty: HabitDifficulty.easy,
      celebration: "Nota la reacción de la otra persona",
    ),
    MicroHabit(
      habit: "Pon límites diciendo 'déjame pensarlo' en lugar de 'sí' automático",
      when: "Cuando alguien te pida un favor",
      why: "Tu sensibilidad lunar te hace decir sí cuando quieres decir no",
      difficulty: HabitDifficulty.hard,
      celebration: "Siente el poder de proteger tu energía",
    ),
  ];

  // LEO (Expresión Auténtica)
  static List<MicroHabit> leoHabits = [
    MicroHabit(
      habit: "Comparte algo creativo tuyo en redes",
      when: "Cada viernes a las 5pm",
      why: "Tu Sol necesita brillar - no escondas tu luz",
      difficulty: HabitDifficulty.medium,
      celebration: "Lee los comentarios positivos en voz alta",
    ),
    MicroHabit(
      habit: "Pregunta '¿y tú cómo estás?' después de hablar de ti",
      when: "En TODA conversación después de compartir sobre ti",
      why: "Balance tu Sol (yo) con escuchar a otros - te hace MÁS carismático/a",
      difficulty: HabitDifficulty.medium,
      celebration: "Nota cómo se siente ser curioso/a sobre otros",
    ),
  ];

  // VIRGO (Optimización Práctica)
  static List<MicroHabit> virgoHabits = [
    MicroHabit(
      habit: "Mejora 1 cosa pequeña en tu rutina",
      when: "Cada domingo por la mañana (planea la semana)",
      why: "Tu Mercurio NECESITA optimizar - dale algo concreto",
      difficulty: HabitDifficulty.easy,
      celebration: "Escribe el cambio y nota el impacto en una semana",
    ),
    MicroHabit(
      habit: "Declare algo 'suficientemente bueno' y SUÉLTALO",
      when: "Cuando sientas ganas de perfeccionar algo más",
      why: "Perfeccionismo es tu talón de Aquiles - practica 80/20",
      difficulty: HabitDifficulty.hard,
      celebration: "Nota cuánto tiempo liberaste para otras cosas",
    ),
  ];

  // LIBRA (Balance Relacional)
  static List<MicroHabit> libraHabits = [
    MicroHabit(
      habit: "Toma 1 decisión rápida (<1 min) cada día",
      when: "Primera decisión del día (qué desayunar, qué ropa, etc)",
      why: "Entrena a tu Venus indeciso a confiar en tu juicio",
      difficulty: HabitDifficulty.medium,
      celebration: "Di '¡Decidido!' en voz alta y sigue adelante",
    ),
    MicroHabit(
      habit: "Pregunta '¿qué QUIERO yo?' antes de preguntar qué quieren otros",
      when: "Toda vez que necesites decidir algo",
      why: "Tu Venus se pierde en perspectivas de otros - reconéctate contigo",
      difficulty: HabitDifficulty.hard,
      celebration: "Honra tu decisión aunque otros no estén de acuerdo",
    ),
  ];

  // ESCORPIO (Transformación Profunda)
  static List<MicroHabit> scorpioHabits = [
    MicroHabit(
      habit: "Escribe 1 emoción intensa que sentiste hoy",
      when: "Cada noche en tu diario privado",
      why: "Tu Plutón genera emociones intensas - nómbralas para procesarlas",
      difficulty: HabitDifficulty.medium,
      celebration: "Nota cómo nombrar la emoción la hace menos intensa",
    ),
    MicroHabit(
      habit: "Comparte 1 cosa vulnerable con alguien de confianza",
      when: "1 vez por semana mínimo",
      why: "Tu Plutón tiende a ocultar - vulnerabilidad es poder real",
      difficulty: HabitDifficulty.hard,
      celebration: "Nota cómo la intimidad se profundiza",
    ),
  ];

  // SAGITARIO (Expansión Consciente)
  static List<MicroHabit> sagittariusHabits = [
    MicroHabit(
      habit: "Termina 1 proyecto antes de empezar otro",
      when: "Cuando sientas ganas de empezar algo nuevo",
      why: "Tu Júpiter te da ideas infinitas pero poca finalización",
      difficulty: HabitDifficulty.hard,
      celebration: "Tacha el proyecto completado y siente la satisfacción",
    ),
    MicroHabit(
      habit: "Lee/aprende sobre 1 cultura diferente a la tuya",
      when: "Cada domingo por la mañana (30 min)",
      why: "Alimenta tu Júpiter curioso - expansión sin salir de casa",
      difficulty: HabitDifficulty.easy,
      celebration: "Comparte 1 fact fascinante que aprendiste",
    ),
  ];

  // CAPRICORN (Disciplina Productiva)
  static List<MicroHabit> capricornHabits = [
    MicroHabit(
      habit: "Haz algo SOLO por placer (sin productividad) 15 min",
      when: "Cada día después del trabajo",
      why: "Tu Saturno es tan disciplinado que olvidas disfrutar - esto es TRABAJO también",
      difficulty: HabitDifficulty.hard,
      celebration: "Nota cómo el placer mejora tu productividad al día siguiente",
    ),
    MicroHabit(
      habit: "Avanza 1% en tu meta #1 cada día",
      when: "Primera cosa en la mañana (antes de emails)",
      why: "Tu Saturno necesita progreso constante - 1% diario = 37x mejor en 1 año",
      difficulty: HabitDifficulty.medium,
      celebration: "Marca un ✓ en calendario - visualiza tu streak",
    ),
  ];

  // AQUARIUS (Innovación Social)
  static List<MicroHabit> aquariusHabits = [
    MicroHabit(
      habit: "Haz 1 cosa de forma totalmente diferente",
      when: "Cada día (ruta al trabajo, forma de cocinar, etc)",
      why: "Tu Urano NECESITA novedad - dale pequeñas dosis diarias",
      difficulty: HabitDifficulty.easy,
      celebration: "Nota cómo te sientes más vivo/a con variación",
    ),
    MicroHabit(
      habit: "Comparte tus sentimientos (no solo ideas)",
      when: "En conversaciones íntimas con seres queridos",
      why: "Tu Urano vive en la cabeza - reconéctate con tu corazón",
      difficulty: HabitDifficulty.hard,
      celebration: "Nota cómo las personas se acercan más a ti",
    ),
  ];

  // PISCES (Creatividad Intuitiva)
  static List<MicroHabit> piscesHabits = [
    MicroHabit(
      habit: "Captura 1 idea/sueño/visión inmediatamente",
      when: "En cuanto llegue a tu mente (usa notas de voz si es necesario)",
      why: "Tu Neptuno te da visiones - pero se evaporan si no las capturas",
      difficulty: HabitDifficulty.easy,
      celebration: "Lee tus ideas al final de semana - son oro",
    ),
    MicroHabit(
      habit: "Define 1 acción concreta para 1 sueño",
      when: "Cada lunes por la mañana",
      why: "Tu Neptuno sueña infinito - Tierra lo con ACCIÓN",
      difficulty: HabitDifficulty.hard,
      celebration: "Ejecuta esa 1 acción antes del viernes",
    ),
  ];
}
```

---

## 📊 SISTEMA DE GAMIFICACIÓN AVANZADO

### **Levels & Progression**

```dart
enum GoalMasteryLevel {
  novice,        // 0-4 completions
  apprentice,    // 5-9 completions
  adept,         // 10-19 completions
  expert,        // 20-49 completions
  master,        // 50-99 completions
  grandmaster,   // 100+ completions
}

class GoalMastery {
  final String goalId;
  final int completionCount;
  final GoalMasteryLevel level;
  final DateTime firstCompletion;
  final DateTime? lastCompletion;
  final int currentStreak;
  final int longestStreak;

  // Unlockables por nivel
  final Map<GoalMasteryLevel, Reward> rewards = {
    GoalMasteryLevel.apprentice: Reward(
      badge: "🌱 Seedling",
      title: "Consistency Builder",
      unlocks: ["Harder version of this goal"],
    ),
    GoalMasteryLevel.adept: Reward(
      badge: "🔥 Fire Starter",
      title: "Habit Former",
      unlocks: ["Related advanced goals", "Can teach this goal to others"],
    ),
    GoalMasteryLevel.expert: Reward(
      badge: "⭐ Rising Star",
      title: "Dedicated Practitioner",
      unlocks: ["Custom goal variations", "Mentor status"],
    ),
    GoalMasteryLevel.master: Reward(
      badge: "💎 Diamond",
      title: "Master of [Goal Category]",
      unlocks: ["Create custom goals", "Community leader badge"],
    ),
    GoalMasteryLevel.grandmaster: Reward(
      badge: "👑 Cosmic Legend",
      title: "[Zodiac Sign] Archetype Embodied",
      unlocks: ["Lifetime achievement", "Feature in app hall of fame"],
    ),
  };
}
```

### **Achievements Específicos**

```dart
enum Achievement {
  // Streak Achievements
  sevenDayStreak("🔥 Week Warrior"),
  thirtyDayStreak("📅 Monthly Master"),
  hundredDayStreak("💯 Centurion"),
  threeSixtyFiveDayStreak("🌟 Year of Excellence"),

  // Category Achievements
  fitnessFreak("💪 Fitness Fanatic - 50 workouts"),
  zenMaster("🧘 Zen Master - 100 meditations"),
  scholarSupreme("📚 Scholar Supreme - 50 learning goals"),
  relationshipGuru("❤️ Relationship Guru - 50 connection goals"),

  // Special Achievements
  mercuryRetrogradeSurvivor("🔄 Mercury Retrograde Survivor"),
  fullMoonRitualAdept("🌕 Full Moon Ritualist"),
  shadowWorkWarrior("🌑 Shadow Integrated"),

  // Zodiac-Specific
  ariesWarriorComplete("⚔️ Aries Warrior Path - All Aries goals mastered"),
  taurusSensualComplete("🌹 Taurus Embodied - All Tauro goals mastered"),
  // ... etc para los 12 signos

  // Meta Achievements
  allElementsMastered("🌍🔥💨💧 Four Elements Balanced"),
  allModalitiesMastered("⚡🔄🌟 Cardinal-Fixed-Mutable Trinity"),
  zodiacWheelComplete("♈♉♊♋♌♍♎♏♐♑♒♓ Zodiac Wheel Master - 1 goal de cada signo"),
}
```

---

## 🎓 EDUCATIONAL GOALS (Teach Astrology)

### **Mini-Courses Dentro de Goals**

Cada goal puede incluir mini-lecciones de astrología:

```dart
class EducationalGoal extends Goal {
  final AstroLesson lesson;

  // Ejemplo:
  AstroLesson(
    concept: "¿Qué es un Tránsito Planetario?",
    explanation: """
    🪐 ASTROLOGÍA 101: TRÁNSITOS

    ANALOGÍA:
    Tu carta natal = mapa de tu ciudad (fijo)
    Tránsitos = tráfico actual en esas calles (cambia diariamente)

    CÓMO FUNCIONA:
    Los planetas siguen moviéndose después de que naciste.
    Cuando un planeta en movimiento (tránsito) toca un planeta
    en tu carta natal, ACTIVA esa área de tu vida.

    EJEMPLO:
    • Naciste con Sol en Aries
    • Hoy Marte (planeta de acción) está tocando tu Sol
    • = Sentirás MUCHA energía y motivación HOY

    TIPOS DE CONTACTOS:
    • Conjunción (0°): Fusión, inicio nuevo
    • Oposición (180°): Tensión, necesidad de balance
    • Trígono (120°): Flujo fácil, suerte
    • Cuadrado (90°): Fricción, crecimiento a través de reto
    • Sextil (60°): Oportunidad, cooperación
    """,
    quiz: [
      Question(
        "Si Venus transita tu signo solar, ¿qué esperas?",
        options: [
          "Más atractivo/a, relaciones fluyen, dinero mejora",
          "Peleas y conflictos",
          "Nada, los tránsitos no afectan",
        ],
        correctAnswer: 0,
        explanation: "Venus trae armonía, belleza y facilidad a lo que toca.",
      ),
    ],
    practicalApplication: """
    CÓMO USAR ESTO:
    1. Identifica tránsitos importantes (app te dice)
    2. Lee qué planeta es y qué área de vida activa
    3. Agenda tareas relevantes para ese día
    4. Observa si sientes la energía descrita
    5. Journaling: ¿el tránsito se manifestó como esperabas?
    """,
  );
}
```

---

**CONTINÚA EN PARTE 3...**

Este documento será PARTE 2 de las mejoras. ¿Quieres que continúe con:
- Parte 3: Goals Basados en Biorhythms (ciclos de 23/28/33 días)
- Parte 4: Goals de Relaciones Específicas (por compatibilidad de signos)
- Parte 5: Goals Basados en Numerología (números de vida, año personal)
- O profundizar aún más en alguna sección específica?
