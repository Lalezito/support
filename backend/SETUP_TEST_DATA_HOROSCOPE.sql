-- ✨ DATOS DE PRUEBA - Horóscopos Personalizados
-- Fecha: 19 Noviembre 2025
-- Propósito: Testing de personalización astrológica en Cosmic Coach

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 🦁 LEO - Español (Para ti, Alejandro!)
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSERT INTO daily_horoscopes (
  sign,
  date,
  language_code,
  content,
  energy_level,
  lucky_colors,
  favorable_times,
  love_focus,
  career_focus,
  wellness_focus
) VALUES (
  'leo',
  CURRENT_DATE,
  'es',
  'Hoy el Sol en tu signo está haciendo un aspecto armonioso con Júpiter, amplificando tu carisma natural y tu capacidad de liderazgo. Es un día para brillar y tomar la iniciativa en los proyectos que te apasionan. La Luna en Géminis favorece la comunicación creativa.',
  'high',
  'dorado, púrpura, naranja',
  '14:00-16:00, 20:00-22:00',
  'Venus favorece tus conexiones románticas. Es un momento ideal para conversaciones profundas y expresar tus sentimientos auténticos. Si estás en pareja, planea algo especial para esta noche.',
  'Excelente día para presentaciones y proyectos creativos. Tu liderazgo natural brilla con especial intensidad. Aprovecha para hacer networking o lanzar nuevas iniciativas.',
  'Alta energía leonina. Canaliza con ejercicio vigoroso, baile o actividades creativas. Necesitas movimiento físico para equilibrar tu fuego interno.'
) ON CONFLICT (sign, date, language_code) DO UPDATE SET
  content = EXCLUDED.content,
  energy_level = EXCLUDED.energy_level,
  lucky_colors = EXCLUDED.lucky_colors,
  favorable_times = EXCLUDED.favorable_times,
  love_focus = EXCLUDED.love_focus,
  career_focus = EXCLUDED.career_focus,
  wellness_focus = EXCLUDED.wellness_focus;

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 🔥 ARIES - Español
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSERT INTO daily_horoscopes (
  sign,
  date,
  language_code,
  content,
  energy_level,
  lucky_colors,
  favorable_times,
  love_focus,
  career_focus,
  wellness_focus
) VALUES (
  'aries',
  CURRENT_DATE,
  'es',
  'Marte, tu planeta regente, te da energía extra hoy. Es momento de actuar, no de dudar. Confía en tus instintos pioneros y atrévete a tomar la iniciativa en aquello que has estado posponiendo. Tu valentía natural está amplificada.',
  'very_high',
  'rojo, naranja, amarillo',
  '08:00-10:00, 18:00-20:00',
  'Sé directo pero no impulsivo en el amor. La honestidad atrae. Si estás soltero, tu seguridad magnética atrae miradas. En pareja, evita discusiones innecesarias.',
  'Inicia ese proyecto que has pospuesto. Tu valentía inspira a otros. Momento excelente para emprendimientos y para demostrar tu capacidad de liderazgo.',
  'Necesitas movimiento físico intenso. Deportes de alta intensidad, artes marciales o running son ideales. Tu energía marciana necesita canalizarse de forma constructiva.'
) ON CONFLICT (sign, date, language_code) DO UPDATE SET
  content = EXCLUDED.content,
  energy_level = EXCLUDED.energy_level,
  lucky_colors = EXCLUDED.lucky_colors,
  favorable_times = EXCLUDED.favorable_times,
  love_focus = EXCLUDED.love_focus,
  career_focus = EXCLUDED.career_focus,
  wellness_focus = EXCLUDED.wellness_focus;

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 🦁 LEO - English
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSERT INTO daily_horoscopes (
  sign,
  date,
  language_code,
  content,
  energy_level,
  lucky_colors,
  favorable_times,
  love_focus,
  career_focus,
  wellness_focus
) VALUES (
  'leo',
  CURRENT_DATE,
  'en',
  'Today the Sun in your sign makes a harmonious aspect with Jupiter, amplifying your natural charisma and leadership abilities. It''s a day to shine and take the initiative on projects you''re passionate about. The Moon in Gemini favors creative communication.',
  'high',
  'gold, purple, orange',
  '2:00 PM - 4:00 PM, 8:00 PM - 10:00 PM',
  'Venus favors your romantic connections. This is an ideal time for deep conversations and expressing your authentic feelings. If you''re in a relationship, plan something special for tonight.',
  'Excellent day for presentations and creative projects. Your natural leadership shines with special intensity. Take advantage for networking or launching new initiatives.',
  'High Leonine energy. Channel it through vigorous exercise, dancing, or creative activities. You need physical movement to balance your inner fire.'
) ON CONFLICT (sign, date, language_code) DO UPDATE SET
  content = EXCLUDED.content,
  energy_level = EXCLUDED.energy_level,
  lucky_colors = EXCLUDED.lucky_colors,
  favorable_times = EXCLUDED.favorable_times,
  love_focus = EXCLUDED.love_focus,
  career_focus = EXCLUDED.career_focus,
  wellness_focus = EXCLUDED.wellness_focus;

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 🐟 PISCES - Español (Para testing diferenciación)
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSERT INTO daily_horoscopes (
  sign,
  date,
  language_code,
  content,
  energy_level,
  lucky_colors,
  favorable_times,
  love_focus,
  career_focus,
  wellness_focus
) VALUES (
  'pisces',
  CURRENT_DATE,
  'es',
  'Neptuno, tu planeta regente, te invita a conectar con tu intuición profunda. Es un día para soñar, visualizar y confiar en tus corazonadas. Tu sensibilidad está especialmente afinada para captar las emociones de quienes te rodean.',
  'medium',
  'azul marino, lavanda, plateado',
  '06:00-08:00, 21:00-23:00',
  'Tu empatía natural crea conexiones profundas. Escucha con el corazón, no solo con los oídos. La vulnerabilidad compartida fortalece vínculos.',
  'Confía en tu creatividad e intuición para resolver problemas. Los proyectos artísticos o que requieran imaginación están especialmente favorecidos.',
  'Necesitas tiempo a solas para recargar. Meditación, baños relajantes o arte terapia son ideales. El agua es tu elemento - úsalo para sanación.'
) ON CONFLICT (sign, date, language_code) DO UPDATE SET
  content = EXCLUDED.content,
  energy_level = EXCLUDED.energy_level,
  lucky_colors = EXCLUDED.lucky_colors,
  favorable_times = EXCLUDED.favorable_times,
  love_focus = EXCLUDED.love_focus,
  career_focus = EXCLUDED.career_focus,
  wellness_focus = EXCLUDED.wellness_focus;

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- ♉ TAURUS - Español (Para testing variedad)
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSERT INTO daily_horoscopes (
  sign,
  date,
  language_code,
  content,
  energy_level,
  lucky_colors,
  favorable_times,
  love_focus,
  career_focus,
  wellness_focus
) VALUES (
  'taurus',
  CURRENT_DATE,
  'es',
  'Venus, tu planeta regente, te bendice con encanto extra y aprecio por la belleza. Es un día perfecto para disfrutar los placeres sensoriales de la vida. Tu paciencia y determinación están en su punto óptimo.',
  'balanced',
  'verde esmeralda, rosa, café',
  '10:00-12:00, 17:00-19:00',
  'El romance está en los pequeños detalles. Un gesto considerado vale más que grandes gestos hoy. Disfruta momentos de calidad sin prisa.',
  'Tu enfoque práctico y persistente rinde frutos. Es día para consolidar, no para iniciar. Finaliza proyectos pendientes antes de empezar nuevos.',
  'Conecta con la naturaleza. Una caminata al aire libre, jardinería o simplemente sentarte bajo un árbol te recarga completamente.'
) ON CONFLICT (sign, date, language_code) DO UPDATE SET
  content = EXCLUDED.content,
  energy_level = EXCLUDED.energy_level,
  lucky_colors = EXCLUDED.lucky_colors,
  favorable_times = EXCLUDED.favorable_times,
  love_focus = EXCLUDED.love_focus,
  career_focus = EXCLUDED.career_focus,
  wellness_focus = EXCLUDED.wellness_focus;

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- ✅ VERIFICACIÓN
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- Query para verificar que se insertaron correctamente
SELECT
  sign,
  date,
  language_code,
  LEFT(content, 80) as preview,
  energy_level,
  lucky_colors
FROM daily_horoscopes
WHERE date = CURRENT_DATE
ORDER BY sign, language_code;

-- Expected output:
-- aries   | 2025-11-19 | es | Marte, tu planeta regente, te da energía extra hoy...    | very_high | rojo, naranja, amarillo
-- leo     | 2025-11-19 | en | Today the Sun in your sign makes a harmonious aspect...  | high      | gold, purple, orange
-- leo     | 2025-11-19 | es | Hoy el Sol en tu signo está haciendo un aspecto...       | high      | dorado, púrpura, naranja
-- pisces  | 2025-11-19 | es | Neptuno, tu planeta regente, te invita a conectar...     | medium    | azul marino, lavanda, plateado
-- taurus  | 2025-11-19 | es | Venus, tu planeta regente, te bendice con encanto...     | balanced  | verde esmeralda, rosa, café
