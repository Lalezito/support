#!/usr/bin/env python3
"""
Add missing translations to German and French ARB files.
Professional quality translations maintaining tone and style.
"""

import json
from pathlib import Path
from collections import OrderedDict

def load_arb_ordered(file_path):
    """Load ARB file preserving order."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f, object_pairs_hook=OrderedDict)

def save_arb(file_path, data):
    """Save ARB file with proper formatting."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')  # Add final newline

def main():
    base_path = Path('/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n')

    # Professional German translations
    german_translations = {
        # Review feedback - Critical UI
        "reviewFeedbackAppCrashes": "App stürzt ab/Fehler",
        "reviewFeedbackCommonIssues": "Häufige Probleme:",
        "reviewFeedbackConfusingUI": "Verwirrende Benutzeroberfläche",
        "reviewFeedbackHelpsImprove": "Ihr Feedback hilft uns, uns zu verbessern",
        "reviewFeedbackInaccurateHoroscopes": "Ungenaue Horoskope",
        "reviewFeedbackMissingFeatures": "Fehlende Funktionen",
        "reviewFeedbackOther": "Sonstiges",
        "reviewFeedbackPlaceholder": "Erzählen Sie uns mehr...",
        "reviewFeedbackSend": "Feedback senden",
        "reviewFeedbackSubtitle": "Was können wir verbessern?",
        "reviewFeedbackThankYou": "Vielen Dank! Wir werden es prüfen und verbessern.",
        "reviewFeedbackTitle": "Es tut uns leid, dass Ihnen Zodiac Life noch nicht gefällt.",
        "reviewFeedbackTooExpensive": "Zu teuer",
        "reviewSubmit": "Senden",

        # Review rating
        "reviewRatingTitle": "Wie würden Sie Zodiac Life bewerten?",
        "reviewNotNow": "Nicht jetzt",
        "reviewRatingExcellent": "Ausgezeichnet!",
        "reviewRatingGood": "Gut",
        "reviewRatingOkay": "In Ordnung",
        "reviewRatingPoor": "Schlecht",
        "reviewRatingVeryPoor": "Sehr schlecht",
        "reviewWasThisHelpful": "War das hilfreich?",
    }

    # Professional French translations
    french_translations = {
        # Review feedback - Critical UI
        "reviewFeedbackAppCrashes": "Plantages/bugs de l'app",
        "reviewFeedbackCommonIssues": "Problèmes courants :",
        "reviewFeedbackConfusingUI": "Interface confuse",
        "reviewFeedbackHelpsImprove": "Votre avis nous aide à nous améliorer",
        "reviewFeedbackInaccurateHoroscopes": "Horoscopes imprécis",
        "reviewFeedbackMissingFeatures": "Fonctionnalités manquantes",
        "reviewFeedbackOther": "Autre",
        "reviewFeedbackPlaceholder": "Dites-nous en plus...",
        "reviewFeedbackSend": "Envoyer un avis",
        "reviewFeedbackSubtitle": "Que pouvons-nous améliorer ?",
        "reviewFeedbackThankYou": "Merci ! Nous allons examiner et améliorer.",
        "reviewFeedbackTitle": "Nous sommes désolés que Zodiac Life ne vous enchante pas encore.",
        "reviewFeedbackTooExpensive": "Trop cher",
        "reviewSubmit": "Envoyer",

        # Review rating
        "reviewRatingTitle": "Comment évalueriez-vous Zodiac Life ?",
        "reviewNotNow": "Pas maintenant",
        "reviewRatingExcellent": "Excellent !",
        "reviewRatingGood": "Bien",
        "reviewRatingOkay": "Correct",
        "reviewRatingPoor": "Médiocre",
        "reviewRatingVeryPoor": "Très médiocre",
        "reviewWasThisHelpful": "Était-ce utile ?",

        # Compatibility - Medium/Low priority
        "compatibility_adviceLabel": "Conseil",
        "compatibility_monthlyPredictionsTitle": "Prédictions mensuelles",
        "compatibility_dimensionChemistry": "Chimie",
        "compatibility_dimensionCommunication": "Communication",
        "compatibility_dimensionConflicts": "Conflits",
        "compatibility_dimensionFriendship": "Amitié",
        "compatibility_dimensionGoals": "Objectifs",
        "compatibility_dimensionIntellectual": "Intellectuel",
        "compatibility_dimensionRomantic": "Romantique",
        "compatibility_dimensionWork": "Travail",
        "compatibility_levelExcellent": "Excellent",
        "compatibility_levelFair": "Correct",
        "compatibility_levelGood": "Bon",
        "compatibility_levelLow": "Faible",
        "compatibility_monthApril": "Avril",
        "compatibility_monthFebruary": "Février",
        "compatibility_monthJanuary": "Janvier",
        "compatibility_monthMarch": "Mars",
        "compatibility_prediction1": "Vénus favorise la communication romantique",
        "compatibility_prediction2": "Période idéale pour résoudre les différends",
        "compatibility_prediction3": "Mars intensifie la passion mutuelle",
        "compatibility_prediction4": "Jupiter élargit les opportunités communes",
        "compatibility_selectPartnerSign": "Sélectionnez le signe de votre partenaire",
    }

    # Load and update German ARB
    print("📝 Updating German (DE) translations...")
    de_data = load_arb_ordered(base_path / 'app_de.arb')

    added_de = 0
    for key, value in german_translations.items():
        if key not in de_data:
            de_data[key] = value
            added_de += 1
            print(f"  ✓ Added: {key}")

    save_arb(base_path / 'app_de.arb', de_data)
    print(f"✅ German: Added {added_de} translations\n")

    # Load and update French ARB
    print("📝 Updating French (FR) translations...")
    fr_data = load_arb_ordered(base_path / 'app_fr.arb')

    added_fr = 0
    for key, value in french_translations.items():
        if key not in fr_data:
            fr_data[key] = value
            added_fr += 1
            print(f"  ✓ Added: {key}")

    save_arb(base_path / 'app_fr.arb', fr_data)
    print(f"✅ French: Added {added_fr} translations\n")

    print("="*80)
    print("📊 SUMMARY")
    print("="*80)
    print(f"German (DE): {added_de} keys added")
    print(f"French (FR): {added_fr} keys added")
    print(f"Italian (IT): Already complete ✓")
    print(f"Portuguese (PT): Already complete ✓")
    print()
    print("Next step: Run 'flutter gen-l10n' to generate localization files")

if __name__ == '__main__':
    main()
