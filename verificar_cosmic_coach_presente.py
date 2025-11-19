import json

print("="*80)
print("🎯 VERIFICANDO TRADUCCIONES DE COSMIC COACH")
print("="*80)
print()

# Cargar las 187 keys de Cosmic Coach
with open('multiagent_output/cosmic_coach_keys.txt', 'r') as f:
    cosmic_keys = [line.strip() for line in f if line.strip() and not line.startswith('@')]

print(f"📋 Keys de Cosmic Coach a verificar: {len(cosmic_keys)}")
print()

languages = ['en', 'es', 'de', 'fr', 'it', 'pt']

for lang in languages:
    with open(f'zodiac_app/assets/l10n/app_{lang}.arb', 'r') as f:
        data = json.load(f)
    
    # Verificar cuántas keys de Cosmic Coach están presentes
    presentes = sum(1 for key in cosmic_keys if key in data)
    faltantes = len(cosmic_keys) - presentes
    
    status = "✅ COMPLETO" if faltantes == 0 else f"⚠️  Faltan {faltantes}"
    
    print(f"{lang.upper()}: {presentes}/{len(cosmic_keys)} keys - {status}")
    
    # Mostrar algunas keys faltantes si las hay
    if faltantes > 0:
        missing = [key for key in cosmic_keys if key not in data]
        print(f"   Faltantes: {missing[:5]}...")
        print()

print()
print("="*80)
print("✅ VERIFICACIÓN FINAL:")
print()
print("Si todos los idiomas muestran 'COMPLETO', entonces TODAS")
print("las traducciones de Cosmic Coach están presentes y nada se perdió.")
print("="*80)
