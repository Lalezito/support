#!/usr/bin/env python3
"""
Script to add new compatibility translation keys to all ARB files.
"""
import json
import os

# Define base path
base_path = "/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n"

# Define the new keys for each language
translations = {
    "app_en.arb": {
        "pdfReport": "PDF Report",
        "@pdfReport": {"description": "Title for PDF report export option"},
        "generateProfessionalAnalysis": "Generate complete professional analysis",
        "@generateProfessionalAnalysis": {"description": "Description for PDF export"},
        "shareAnalysis": "Share Analysis",
        "@shareAnalysis": {"description": "Title for share option"},
        "shareViaAnyPlatform": "Share via social media, messaging or email",
        "@shareViaAnyPlatform": {"description": "Description for share option"},
        "shareAndExport": "Share & Export",
        "@shareAndExport": {"description": "Tab title for sharing section"},
        "compatibilityResultTitle": "Zodiac Compatibility",
        "@compatibilityResultTitle": {"description": "Title for sharing compatibility"},
        "downloadAppMessage": "Discover your cosmic compatibility at Zodiac App!",
        "@downloadAppMessage": {"description": "CTA message for sharing"}
    },
    "app_es.arb": {
        "pdfReport": "Reporte PDF",
        "generateProfessionalAnalysis": "Genera análisis profesional completo",
        "shareAnalysis": "Compartir Análisis",
        "shareViaAnyPlatform": "Comparte por redes sociales, mensajería o email",
        "shareAndExport": "Compartir y Exportar",
        "compatibilityResultTitle": "Compatibilidad Zodiacal",
        "downloadAppMessage": "¡Descubre tu compatibilidad cósmica en Zodiac App!"
    },
    "app_de.arb": {
        "pdfReport": "PDF-Bericht",
        "generateProfessionalAnalysis": "Vollständige professionelle Analyse erstellen",
        "shareAnalysis": "Analyse teilen",
        "shareViaAnyPlatform": "Über soziale Medien, Messaging oder E-Mail teilen",
        "shareAndExport": "Teilen & Exportieren",
        "compatibilityResultTitle": "Sternzeichen-Kompatibilität",
        "downloadAppMessage": "Entdecke deine kosmische Kompatibilität in Zodiac App!"
    },
    "app_fr.arb": {
        "pdfReport": "Rapport PDF",
        "generateProfessionalAnalysis": "Générer une analyse professionnelle complète",
        "shareAnalysis": "Partager l'analyse",
        "shareViaAnyPlatform": "Partager via réseaux sociaux, messagerie ou email",
        "shareAndExport": "Partager et Exporter",
        "compatibilityResultTitle": "Compatibilité Zodiacale",
        "downloadAppMessage": "Découvrez votre compatibilité cosmique sur Zodiac App!"
    },
    "app_it.arb": {
        "pdfReport": "Rapporto PDF",
        "generateProfessionalAnalysis": "Genera analisi professionale completa",
        "shareAnalysis": "Condividi Analisi",
        "shareViaAnyPlatform": "Condividi tramite social, messaggistica o email",
        "shareAndExport": "Condividi ed Esporta",
        "compatibilityResultTitle": "Compatibilità Zodiacale",
        "downloadAppMessage": "Scopri la tua compatibilità cosmica su Zodiac App!"
    },
    "app_pt.arb": {
        "pdfReport": "Relatório PDF",
        "generateProfessionalAnalysis": "Gerar análise profissional completa",
        "shareAnalysis": "Compartilhar Análise",
        "shareViaAnyPlatform": "Compartilhar via redes sociais, mensagens ou email",
        "shareAndExport": "Compartilhar e Exportar",
        "compatibilityResultTitle": "Compatibilidade Zodiacal",
        "downloadAppMessage": "Descubra sua compatibilidade cósmica no Zodiac App!"
    }
}

def add_keys_to_arb_file(filename, new_keys):
    """Add new keys to an ARB file while preserving formatting."""
    filepath = os.path.join(base_path, filename)

    print(f"\n📝 Processing {filename}...")

    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing {filename}: {e}")
        return False

    # Check if keys already exist
    existing_keys = []
    for key in new_keys.keys():
        if key in data:
            existing_keys.append(key)

    if existing_keys:
        print(f"⚠️  Found existing keys in {filename}: {', '.join(existing_keys)}")
        print(f"   Skipping these keys to avoid duplicates")
        # Remove existing keys from new_keys
        for key in existing_keys:
            del new_keys[key]

    if not new_keys:
        print(f"✅ All keys already exist in {filename}, nothing to add")
        return True

    # Add new keys
    data.update(new_keys)

    # Write back with pretty formatting
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')  # Add newline at end of file

    print(f"✅ Added {len(new_keys)} new keys to {filename}")
    return True

def main():
    print("🚀 Starting translation key addition process...")
    print(f"📁 Base path: {base_path}")

    success_count = 0
    fail_count = 0

    for filename, new_keys in translations.items():
        if add_keys_to_arb_file(filename, new_keys.copy()):
            success_count += 1
        else:
            fail_count += 1

    print("\n" + "="*60)
    print(f"✨ Process completed!")
    print(f"   ✅ Success: {success_count} files")
    print(f"   ❌ Failed: {fail_count} files")
    print("="*60)

    if fail_count == 0:
        print("\n🎉 All translation keys added successfully!")
        print("\n📋 Next step: Run 'flutter gen-l10n' in the zodiac_app directory")
    else:
        print("\n⚠️  Some files had errors. Please check the output above.")

if __name__ == "__main__":
    main()
