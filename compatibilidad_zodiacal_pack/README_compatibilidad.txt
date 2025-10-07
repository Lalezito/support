Compatibilidad Zodiacal - Pack de Datos
======================================

Incluye:
- compatibilidad_zodiacal.json  -> 144 objetos (12x12) con campos listos para app/UI.
- compatibilidad_resumen.csv    -> resumen tabular para análisis rápido.

Campos principales por objeto JSON:
- pair_id: id único 'signoA_signoB' (minúsculas, sin acentos).
- sign_a, sign_b (+ en): nombres ES/EN.
- element_*, modality_*: elemento y modalidad.
- aspect: aspecto zodiacal (conjunción, sextil, trígono, cuadratura, oposición, inconjunción).
- level: A (Alta), M (Media), R (Retadora). 'flash' en flags indica química elevada.
- overall, chemistry, emotional, communication, values, stability: puntajes 0–99 aproximados según heurística del informe.
- summary, strengths, challenges, tips, date_ideas, copy_hooks, seo_tags: strings/listas útiles para UI y marketing.

Licencia de uso: libre para tu app/proyecto. Ajusta pesos/algoritmos según §7 del informe en tu canvas.
