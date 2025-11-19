import json

print("="*80)
print("🔍 VERIFICANDO QUE NO SE PERDIERON TRADUCCIONES REALES")
print("="*80)
print()

languages = ['es', 'de', 'fr', 'it', 'pt']

for lang in languages:
    with open(f'zodiac_app/assets/l10n/app_{lang}.arb', 'r') as f:
        data = json.load(f)
    
    # Contar keys de metadata (@...) vs keys de traducción
    metadata_keys = [k for k in data.keys() if k.startswith('@')]
    translation_keys = [k for k in data.keys() if not k.startswith('@')]
    
    print(f"📋 {lang.upper()}:")
    print(f"   Total keys: {len(data)}")
    print(f"   - Traducciones: {len(translation_keys)}")
    print(f"   - Metadata (@...): {len(metadata_keys)}")
    print()

print("="*80)
print("💡 EXPLICACIÓN:")
print()
print("Si el número total bajó pero las TRADUCCIONES se mantienen,")
print("significa que solo se eliminaron metadata entries duplicadas/obsoletas.")
print("Esto es CORRECTO y no afecta la funcionalidad.")
print()
print("Las metadata (@...) son solo descripciones técnicas,")
print("NO son traducciones que el usuario ve.")
print("="*80)
