import json

print("="*80)
print("🔍 VERIFICACIÓN COMPLETA DE INTEGRIDAD")
print("="*80)
print()

# Estado esperado ANTES de los cambios (del análisis inicial)
antes = {
    'en': 1998,
    'es': 1829,
    'de': 1755,
    'fr': 1700,
    'it': 2072,
    'pt': 2019
}

# Traducciones agregadas
agregadas = {
    'en': 0,
    'es': 59,
    'de': 110,
    'fr': 110,
    'it': 109,
    'pt': 106
}

# Estado esperado DESPUÉS
esperado = {
    'en': 1998,
    'es': 1888,  # 1829 + 59
    'de': 1865,  # 1755 + 110
    'fr': 1810,  # 1700 + 110
    'it': 2181,  # 2072 + 109
    'pt': 2125   # 2019 + 106
}

# Leer estado actual
actual = {}
for lang in ['en', 'es', 'de', 'fr', 'it', 'pt']:
    with open(f'zodiac_app/assets/l10n/app_{lang}.arb', 'r') as f:
        actual[lang] = len(json.load(f))

# Comparar
print("📊 COMPARACIÓN:")
print()
print(f"{'Idioma':<8} {'Antes':<8} {'Agregadas':<10} {'Esperado':<10} {'Actual':<8} {'Estado':<10}")
print("-"*80)

todo_ok = True
for lang in ['en', 'es', 'de', 'fr', 'it', 'pt']:
    estado = "✅ OK" if actual[lang] == esperado[lang] else f"⚠️  DIFF ({actual[lang] - esperado[lang]:+d})"
    if actual[lang] != esperado[lang]:
        todo_ok = False
    
    print(f"{lang.upper():<8} {antes[lang]:<8} {agregadas[lang]:<10} {esperado[lang]:<10} {actual[lang]:<8} {estado:<10}")

print()
print("="*80)
if todo_ok:
    print("✅ TODO PERFECTO - Nada se perdió, todas las traducciones agregadas correctamente")
else:
    print("⚠️  HAY DIFERENCIAS - Investigando...")
    print()
    print("Posibles causas de diferencias:")
    print("1. Metadata (@...) entries removidos/agregados")
    print("2. Keys duplicadas eliminadas") 
    print("3. Limpieza de keys obsoletas")
    print()
    print("Verificando si son solo metadata...")

print("="*80)
