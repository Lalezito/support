#!/bin/bash
# ============================================================================
# AGENT 11: TRANSLATION_COMPLETER - Completador de Traducciones Faltantes
# ============================================================================
# Completa todas las traducciones marcadas como "MISSING_TRANSLATION"
# con traducciones profesionales en los 5 idiomas
# ============================================================================

set -e

echo "🌍 AGENT 11: TRANSLATION_COMPLETER - Iniciando..."
echo ""

# Paths
FEATURES_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output/features/cosmic_coach"
EN_SOURCE="/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n/app_en.arb"
OUTPUT_DIR="/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output"

cd "$FEATURES_DIR"

echo "📁 Directorio: $FEATURES_DIR"
echo ""

# Create translation dictionary JSON file
cat > /tmp/cosmic_coach_translations.json << 'EOF'
{
  "celebration_adventure_1": {
    "en": "🗺️ Explorer mode!",
    "es": "🗺️ ¡Modo explorador!",
    "de": "🗺️ Entdeckermodus!",
    "fr": "🗺️ Mode explorateur !",
    "it": "🗺️ Modalità esploratore!",
    "pt": "🗺️ Modo explorador!"
  },
  "celebration_adventure_2": {
    "en": "🌟 Journey unlocked!",
    "es": "🌟 ¡Viaje desbloqueado!",
    "de": "🌟 Reise freigeschaltet!",
    "fr": "🌟 Voyage débloqué !",
    "it": "🌟 Viaggio sbloccato!",
    "pt": "🌟 Jornada desbloqueada!"
  },
  "celebration_adventure_3": {
    "en": "✈️ Adventure awaits!",
    "es": "✈️ ¡La aventura te espera!",
    "de": "✈️ Abenteuer wartet!",
    "fr": "✈️ L'aventure vous attend !",
    "it": "✈️ L'avventura ti aspetta!",
    "pt": "✈️ A aventura aguarda!"
  },
  "celebration_career_1": {
    "en": "🚀 Career win!",
    "es": "🚀 ¡Victoria profesional!",
    "de": "🚀 Karriere-Erfolg!",
    "fr": "🚀 Victoire de carrière !",
    "it": "🚀 Successo di carriera!",
    "pt": "🚀 Vitória profissional!"
  },
  "celebration_career_2": {
    "en": "💼 Professional growth!",
    "es": "💼 ¡Crecimiento profesional!",
    "de": "💼 Berufliches Wachstum!",
    "fr": "💼 Croissance professionnelle !",
    "it": "💼 Crescita professionale!",
    "pt": "💼 Crescimento profissional!"
  },
  "celebration_career_3": {
    "en": "🎯 Goal achieved!",
    "es": "🎯 ¡Meta alcanzada!",
    "de": "🎯 Ziel erreicht!",
    "fr": "🎯 Objectif atteint !",
    "it": "🎯 Obiettivo raggiunto!",
    "pt": "🎯 Meta alcançada!"
  },
  "celebration_creativity_1": {
    "en": "🎨 Creative spark!",
    "es": "🎨 ¡Chispa creativa!",
    "de": "🎨 Kreativer Funke!",
    "fr": "🎨 Étincelle créative !",
    "it": "🎨 Scintilla creativa!",
    "pt": "🎨 Faísca criativa!"
  },
  "celebration_creativity_2": {
    "en": "✨ Innovation unlocked!",
    "es": "✨ ¡Innovación desbloqueada!",
    "de": "✨ Innovation freigeschaltet!",
    "fr": "✨ Innovation débloquée !",
    "it": "✨ Innovazione sbloccata!",
    "pt": "✨ Inovação desbloqueada!"
  },
  "celebration_creativity_3": {
    "en": "🌈 Imagination soars!",
    "es": "🌈 ¡La imaginación vuela!",
    "de": "🌈 Fantasie schwebt!",
    "fr": "🌈 L'imagination s'envole !",
    "it": "🌈 L'immaginazione vola!",
    "pt": "🌈 A imaginação voa!"
  },
  "celebration_finance_1": {
    "en": "💰 Financial milestone!",
    "es": "💰 ¡Hito financiero!",
    "de": "💰 Finanzieller Meilenstein!",
    "fr": "💰 Étape financière !",
    "it": "💰 Traguardo finanziario!",
    "pt": "💰 Marco financeiro!"
  },
  "celebration_finance_2": {
    "en": "💎 Wealth step forward!",
    "es": "💎 ¡Paso hacia la riqueza!",
    "de": "💎 Wohlstandsschritt vorwärts!",
    "fr": "💎 Pas vers la richesse !",
    "it": "💎 Passo verso la ricchezza!",
    "pt": "💎 Passo rumo à riqueza!"
  },
  "celebration_finance_3": {
    "en": "📈 Money mastery!",
    "es": "📈 ¡Dominio financiero!",
    "de": "📈 Geldbeherrschung!",
    "fr": "📈 Maîtrise de l'argent !",
    "it": "📈 Padronanza del denaro!",
    "pt": "📈 Maestria financeira!"
  },
  "celebration_fitness_1": {
    "en": "💪 Strength gained!",
    "es": "💪 ¡Fuerza ganada!",
    "de": "💪 Stärke gewonnen!",
    "fr": "💪 Force gagnée !",
    "it": "💪 Forza acquisita!",
    "pt": "💪 Força adquirida!"
  },
  "celebration_fitness_2": {
    "en": "🏃 Fitness victory!",
    "es": "🏃 ¡Victoria fitness!",
    "de": "🏃 Fitness-Sieg!",
    "fr": "🏃 Victoire fitness !",
    "it": "🏃 Vittoria fitness!",
    "pt": "🏃 Vitória fitness!"
  },
  "celebration_fitness_3": {
    "en": "⚡ Energy unleashed!",
    "es": "⚡ ¡Energía liberada!",
    "de": "⚡ Energie freigesetzt!",
    "fr": "⚡ Énergie libérée !",
    "it": "⚡ Energia liberata!",
    "pt": "⚡ Energia liberada!"
  },
  "celebration_health_1": {
    "en": "🌱 Wellness achieved!",
    "es": "🌱 ¡Bienestar logrado!",
    "de": "🌱 Wohlbefinden erreicht!",
    "fr": "🌱 Bien-être atteint !",
    "it": "🌱 Benessere raggiunto!",
    "pt": "🌱 Bem-estar alcançado!"
  },
  "celebration_health_2": {
    "en": "❤️ Health milestone!",
    "es": "❤️ ¡Hito de salud!",
    "de": "❤️ Gesundheitsmeilenstein!",
    "fr": "❤️ Étape de santé !",
    "it": "❤️ Traguardo di salute!",
    "pt": "❤️ Marco de saúde!"
  },
  "celebration_health_3": {
    "en": "🧘 Balance restored!",
    "es": "🧘 ¡Equilibrio restaurado!",
    "de": "🧘 Gleichgewicht wiederhergestellt!",
    "fr": "🧘 Équilibre restauré !",
    "it": "🧘 Equilibrio ripristinato!",
    "pt": "🧘 Equilíbrio restaurado!"
  },
  "celebration_learning_1": {
    "en": "📚 Knowledge gained!",
    "es": "📚 ¡Conocimiento adquirido!",
    "de": "📚 Wissen erworben!",
    "fr": "📚 Connaissance acquise !",
    "it": "📚 Conoscenza acquisita!",
    "pt": "📚 Conhecimento adquirido!"
  },
  "celebration_learning_2": {
    "en": "🎓 Learning victory!",
    "es": "🎓 ¡Victoria de aprendizaje!",
    "de": "🎓 Lernsieg!",
    "fr": "🎓 Victoire d'apprentissage !",
    "it": "🎓 Vittoria di apprendimento!",
    "pt": "🎓 Vitória de aprendizado!"
  },
  "celebration_learning_3": {
    "en": "🧠 Mind expanded!",
    "es": "🧠 ¡Mente expandida!",
    "de": "🧠 Geist erweitert!",
    "fr": "🧠 Esprit élargi !",
    "it": "🧠 Mente espansa!",
    "pt": "🧠 Mente expandida!"
  },
  "celebration_relationships_1": {
    "en": "💕 Connection deepened!",
    "es": "💕 ¡Conexión profundizada!",
    "de": "💕 Verbindung vertieft!",
    "fr": "💕 Connexion approfondie !",
    "it": "💕 Connessione approfondita!",
    "pt": "💕 Conexão aprofundada!"
  },
  "celebration_relationships_2": {
    "en": "🤝 Bond strengthened!",
    "es": "🤝 ¡Vínculo fortalecido!",
    "de": "🤝 Bindung gestärkt!",
    "fr": "🤝 Lien renforcé !",
    "it": "🤝 Legame rafforzato!",
    "pt": "🤝 Vínculo fortalecido!"
  },
  "celebration_relationships_3": {
    "en": "💖 Love grows!",
    "es": "💖 ¡El amor crece!",
    "de": "💖 Liebe wächst!",
    "fr": "💖 L'amour grandit !",
    "it": "💖 L'amore cresce!",
    "pt": "💖 O amor cresce!"
  },
  "celebration_spirituality_1": {
    "en": "🕉️ Inner peace found!",
    "es": "🕉️ ¡Paz interior encontrada!",
    "de": "🕉️ Innerer Frieden gefunden!",
    "fr": "🕉️ Paix intérieure trouvée !",
    "it": "🕉️ Pace interiore trovata!",
    "pt": "🕉️ Paz interior encontrada!"
  },
  "celebration_spirituality_2": {
    "en": "☯️ Harmony achieved!",
    "es": "☯️ ¡Armonía lograda!",
    "de": "☯️ Harmonie erreicht!",
    "fr": "☯️ Harmonie atteinte !",
    "it": "☯️ Armonia raggiunta!",
    "pt": "☯️ Harmonia alcançada!"
  },
  "celebration_spirituality_3": {
    "en": "🌟 Enlightenment step!",
    "es": "🌟 ¡Paso hacia la iluminación!",
    "de": "🌟 Erleuchtungsschritt!",
    "fr": "🌟 Étape d'illumination !",
    "it": "🌟 Passo di illuminazione!",
    "pt": "🌟 Passo de iluminação!"
  }
}
EOF

echo "1️⃣ Aplicando traducciones a archivos segmentados..."
echo ""

# Function to apply translations
apply_translations() {
  local LANG=$1
  local FILE="cosmic_coach_${LANG}.arb"

  if [ ! -f "$FILE" ]; then
    echo "   ⚠️  Archivo no encontrado: $FILE"
    return
  fi

  echo "   Procesando: $FILE"

  # Create a temporary Python script to update JSON
  cat > /tmp/update_translations.py << 'PYTHON_EOF'
import json
import sys

lang = sys.argv[1]
arb_file = sys.argv[2]
translations_file = sys.argv[3]

# Load files
with open(arb_file, 'r', encoding='utf-8') as f:
    arb_data = json.load(f)

with open(translations_file, 'r', encoding='utf-8') as f:
    translations = json.load(f)

# Count updates
updated = 0

# Update MISSING_TRANSLATION values
for key, value in arb_data.items():
    if value == "MISSING_TRANSLATION":
        # Remove @ prefix for lookup
        lookup_key = key.lstrip('@')

        if lookup_key in translations and lang in translations[lookup_key]:
            arb_data[key] = translations[lookup_key][lang]
            updated += 1

# Save updated file
with open(arb_file, 'w', encoding='utf-8') as f:
    json.dump(arb_data, f, ensure_ascii=False, indent=2)

print(f"      ✅ Actualizadas {updated} traducciones")
PYTHON_EOF

  python3 /tmp/update_translations.py "$LANG" "$FILE" /tmp/cosmic_coach_translations.json
}

# Apply translations to each language
for LANG in es de fr it pt; do
  apply_translations "$LANG"
done

echo ""
echo "2️⃣ Verificando resultado..."
echo ""

# Verify no MISSING_TRANSLATION remains
for LANG in es de fr it pt; do
  FILE="cosmic_coach_${LANG}.arb"
  MISSING_COUNT=$(grep -c "MISSING_TRANSLATION" "$FILE" || true)

  if [ "$MISSING_COUNT" -eq 0 ]; then
    echo "   ✅ $LANG: Sin traducciones faltantes"
  else
    echo "   ⚠️  $LANG: Aún quedan $MISSING_COUNT traducciones faltantes"
  fi
done

echo ""
echo "✅ AGENT 11: TRANSLATION_COMPLETER - Completado"
echo ""
echo "📊 Resultado:"
echo "   - Celebraciones traducidas en 5 idiomas"
echo "   - Archivos actualizados en: $FEATURES_DIR"
echo ""
