#!/usr/bin/env python3
"""
Script para añadir traducciones del chat de horóscopo a todos los idiomas
"""

import json
import os

# Definir traducciones para todos los idiomas
translations = {
    'de': {
        "horoscopeChatTitle": "Horoskop-Chat",
        "horoscopeChatWelcome": "Hallo! Ich bin dein persönlicher astrologischer Führer. Frag mich über dein Horoskop, Kompatibilität oder jedes astrologische Thema.",
        "horoscopeChatPlaceholder": "Frage über dein Horoskop...",
        "horoscopeChatTyping": "Dein Astrologe konsultiert die Sterne...",

        "chatCategoryDailyGuidance": "Tägliche Führung",
        "chatCategoryCompatibility": "Kompatibilität",
        "chatCategoryCareerTiming": "Karriere-Timing",
        "chatCategoryPlanetaryInfluence": "Planetare Einflüsse",
        "chatCategoryBirthChart": "Geburtschart",
        "chatCategoryMoonPhase": "Mondphase",

        "quickReplyDailyHoroscope": "Wie ist mein Tag?",
        "quickReplyCompatibility": "Liebeskompatibilität",
        "quickReplyCareerTiming": "Gute Zeit für Veränderungen?",
        "quickReplyMoonPhase": "Wie beeinflusst mich der Mond?",
        "quickReplyBirthChart": "Erzähl mir über mein Geburtschart",

        "horoscopeChatPremiumTitle": "Premium Horoskop-Chat",
        "horoscopeChatPremiumDescription": "Chatte unbegrenzt mit deinem persönlichen KI-Astrologen. Erhalte sofortige Antworten über Horoskop, Kompatibilität, kosmisches Timing und mehr.",
        "horoscopeChatRequiresStellar": "Horoskop-Chat ist exklusiv für Stellar-Stufe ($19,99/Monat)",

        "featureUnlimitedHoroscopeChat": "Unbegrenzter Horoskop-Chat",
        "featurePersonalizedAstrology": "Ultra-personalisierte Astrologie",
        "featureTransitAnalysis": "Planetare Transit-Analyse",
        "featureBirthChartIntegration": "Geburtschart-Integration",

        "horoscopeChatEmptyStateTitle": "Frag mich über dein Horoskop",
        "horoscopeChatEmptyStateSubtitle": "Ich bin dein persönlicher Astrologe, 24/7 verfügbar. Was möchtest du wissen?",

        "horoscopeChatRateLimitTitle": "Tageslimit erreicht",
        "horoscopeChatRateLimitMessage": "Du hast deine 50 täglichen Nachrichten verwendet. Zähler wird um Mitternacht zurückgesetzt.",

        "horoscopeChatErrorTitle": "Verbindungsfehler",
        "horoscopeChatErrorMessage": "Ich konnte die Sterne nicht konsultieren. Bitte versuche es in einigen Momenten erneut."
    },
    'fr': {
        "horoscopeChatTitle": "Chat Horoscope",
        "horoscopeChatWelcome": "Bonjour ! Je suis ton guide astrologique personnel. Demande-moi sur ton horoscope, la compatibilité ou tout sujet astrologique.",
        "horoscopeChatPlaceholder": "Demande sur ton horoscope...",
        "horoscopeChatTyping": "Ton astrologue consulte les étoiles...",

        "chatCategoryDailyGuidance": "Guidage Quotidien",
        "chatCategoryCompatibility": "Compatibilité",
        "chatCategoryCareerTiming": "Timing de Carrière",
        "chatCategoryPlanetaryInfluence": "Influences Planétaires",
        "chatCategoryBirthChart": "Carte Natale",
        "chatCategoryMoonPhase": "Phase Lunaire",

        "quickReplyDailyHoroscope": "Comment est ma journée ?",
        "quickReplyCompatibility": "Compatibilité amoureuse",
        "quickReplyCareerTiming": "Bon moment pour des changements ?",
        "quickReplyMoonPhase": "Comment la lune m'affecte ?",
        "quickReplyBirthChart": "Parle-moi de ma carte natale",

        "horoscopeChatPremiumTitle": "Chat Horoscope Premium",
        "horoscopeChatPremiumDescription": "Chatte illimité avec ton astrologue IA personnel. Obtiens des réponses instantanées sur l'horoscope, la compatibilité, le timing cosmique et plus.",
        "horoscopeChatRequiresStellar": "Le Chat Horoscope est exclusif au niveau Stellar ($19,99/mois)",

        "featureUnlimitedHoroscopeChat": "Chat horoscope illimité",
        "featurePersonalizedAstrology": "Astrologie ultra-personnalisée",
        "featureTransitAnalysis": "Analyse des transits planétaires",
        "featureBirthChartIntegration": "Intégration de la carte natale",

        "horoscopeChatEmptyStateTitle": "Demande-moi sur ton horoscope",
        "horoscopeChatEmptyStateSubtitle": "Je suis ton astrologue personnel disponible 24/7. Que voudrais-tu savoir ?",

        "horoscopeChatRateLimitTitle": "Limite quotidienne atteinte",
        "horoscopeChatRateLimitMessage": "Tu as utilisé tes 50 messages quotidiens. Le compteur se réinitialise à minuit.",

        "horoscopeChatErrorTitle": "Erreur de connexion",
        "horoscopeChatErrorMessage": "Je n'ai pas pu consulter les étoiles. Réessaye dans quelques instants."
    },
    'it': {
        "horoscopeChatTitle": "Chat Oroscopo",
        "horoscopeChatWelcome": "Ciao! Sono la tua guida astrologica personale. Chiedimi del tuo oroscopo, compatibilità o qualsiasi argomento astrologico.",
        "horoscopeChatPlaceholder": "Chiedi del tuo oroscopo...",
        "horoscopeChatTyping": "Il tuo astrologo sta consultando le stelle...",

        "chatCategoryDailyGuidance": "Guida Giornaliera",
        "chatCategoryCompatibility": "Compatibilità",
        "chatCategoryCareerTiming": "Timing di Carriera",
        "chatCategoryPlanetaryInfluence": "Influenze Planetarie",
        "chatCategoryBirthChart": "Tema Natale",
        "chatCategoryMoonPhase": "Fase Lunare",

        "quickReplyDailyHoroscope": "Come va la mia giornata?",
        "quickReplyCompatibility": "Compatibilità amorosa",
        "quickReplyCareerTiming": "Buon momento per cambiamenti?",
        "quickReplyMoonPhase": "Come mi influenza la luna?",
        "quickReplyBirthChart": "Parlami del mio tema natale",

        "horoscopeChatPremiumTitle": "Chat Oroscopo Premium",
        "horoscopeChatPremiumDescription": "Chatta illimitatamente con il tuo astrologo IA personale. Ottieni risposte istantanee su oroscopo, compatibilità, timing cosmico e altro.",
        "horoscopeChatRequiresStellar": "La Chat Oroscopo è esclusiva del livello Stellar ($19,99/mese)",

        "featureUnlimitedHoroscopeChat": "Chat oroscopo illimitata",
        "featurePersonalizedAstrology": "Astrologia ultra-personalizzata",
        "featureTransitAnalysis": "Analisi dei transiti planetari",
        "featureBirthChartIntegration": "Integrazione del tema natale",

        "horoscopeChatEmptyStateTitle": "Chiedimi del tuo oroscopo",
        "horoscopeChatEmptyStateSubtitle": "Sono il tuo astrologo personale disponibile 24/7. Cosa vorresti sapere?",

        "horoscopeChatRateLimitTitle": "Limite giornaliero raggiunto",
        "horoscopeChatRateLimitMessage": "Hai usato i tuoi 50 messaggi giornalieri. Il contatore si resetta a mezzanotte.",

        "horoscopeChatErrorTitle": "Errore di connessione",
        "horoscopeChatErrorMessage": "Non ho potuto consultare le stelle. Riprova tra qualche istante."
    },
    'pt': {
        "horoscopeChatTitle": "Chat de Horóscopo",
        "horoscopeChatWelcome": "Olá! Sou seu guia astrológico pessoal. Pergunte-me sobre seu horóscopo, compatibilidade ou qualquer tópico astrológico.",
        "horoscopeChatPlaceholder": "Pergunte sobre seu horóscopo...",
        "horoscopeChatTyping": "Seu astrólogo está consultando as estrelas...",

        "chatCategoryDailyGuidance": "Orientação Diária",
        "chatCategoryCompatibility": "Compatibilidade",
        "chatCategoryCareerTiming": "Timing de Carreira",
        "chatCategoryPlanetaryInfluence": "Influências Planetárias",
        "chatCategoryBirthChart": "Mapa Astral",
        "chatCategoryMoonPhase": "Fase Lunar",

        "quickReplyDailyHoroscope": "Como está meu dia?",
        "quickReplyCompatibility": "Compatibilidade amorosa",
        "quickReplyCareerTiming": "Bom momento para mudanças?",
        "quickReplyMoonPhase": "Como a lua me afeta?",
        "quickReplyBirthChart": "Fale sobre meu mapa astral",

        "horoscopeChatPremiumTitle": "Chat de Horóscopo Premium",
        "horoscopeChatPremiumDescription": "Converse ilimitadamente com seu astrólogo IA pessoal. Obtenha respostas instantâneas sobre horóscopo, compatibilidade, timing cósmico e mais.",
        "horoscopeChatRequiresStellar": "O Chat de Horóscopo é exclusivo do nível Stellar ($19,99/mês)",

        "featureUnlimitedHoroscopeChat": "Chat de horóscopo ilimitado",
        "featurePersonalizedAstrology": "Astrologia ultra-personalizada",
        "featureTransitAnalysis": "Análise de trânsitos planetários",
        "featureBirthChartIntegration": "Integração com mapa astral",

        "horoscopeChatEmptyStateTitle": "Pergunte sobre seu horóscopo",
        "horoscopeChatEmptyStateSubtitle": "Sou seu astrólogo pessoal disponível 24/7. O que gostaria de saber?",

        "horoscopeChatRateLimitTitle": "Limite diário atingido",
        "horoscopeChatRateLimitMessage": "Você usou suas 50 mensagens diárias. O contador reinicia à meia-noite.",

        "horoscopeChatErrorTitle": "Erro de conexão",
        "horoscopeChatErrorMessage": "Não consegui consultar as estrelas. Tente novamente em alguns momentos."
    }
}

def add_translations_to_file(lang_code, translations_dict):
    """Añade traducciones al archivo .arb correspondiente"""
    file_path = f"/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n/app_{lang_code}.arb"

    try:
        # Leer archivo existente
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remover el último }
        content = content.rstrip()
        if content.endswith('}'):
            content = content[:-1].rstrip()

        # Agregar las nuevas traducciones
        new_section = ',\n\n  "@_HOROSCOPE_CHAT": {},\n'

        for key, value in translations_dict.items():
            # Escapar comillas en el valor
            value_escaped = value.replace('"', '\\"')
            new_section += f'  "{key}": "{value_escaped}",\n'

        # Remover última coma
        new_section = new_section.rstrip(',\n') + '\n'

        # Cerrar JSON
        content += new_section + '}'

        # Escribir archivo actualizado
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ {lang_code.upper()}: {len(translations_dict)} claves añadidas exitosamente")
        return True

    except Exception as e:
        print(f"❌ Error en {lang_code.upper()}: {e}")
        return False

def main():
    """Ejecutar proceso de traducción"""
    print("🌟 Añadiendo traducciones del Chat de Horóscopo...\n")

    results = {}
    for lang_code, trans_dict in translations.items():
        results[lang_code] = add_translations_to_file(lang_code, trans_dict)

    print("\n" + "="*50)
    print("📊 RESUMEN")
    print("="*50)

    success_count = sum(1 for result in results.values() if result)
    total_count = len(results)

    print(f"Completados: {success_count}/{total_count} idiomas")
    print(f"Español (ES): ✅ (manual)")
    print(f"Inglés (EN): ✅ (manual)")

    for lang_code, success in results.items():
        status = "✅" if success else "❌"
        print(f"{lang_code.upper()}: {status}")

    if success_count == total_count:
        print("\n🎉 ¡Todas las traducciones completadas exitosamente!")
    else:
        print(f"\n⚠️  {total_count - success_count} idioma(s) con errores")

if __name__ == "__main__":
    main()
