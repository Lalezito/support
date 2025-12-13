#!/usr/bin/env python3
"""
Extract missing keys from English and Spanish ARB files to create translations.
"""

import json
from pathlib import Path

def load_arb(file_path):
    """Load ARB file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    base_path = Path('/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n')

    # Load English and Spanish
    en_data = load_arb(base_path / 'app_en.arb')
    es_data = load_arb(base_path / 'app_es.arb')

    # Missing keys for each language
    missing = {
        'de': [
            'reviewFeedbackAppCrashes', 'reviewFeedbackCommonIssues', 'reviewFeedbackConfusingUI',
            'reviewFeedbackHelpsImprove', 'reviewFeedbackInaccurateHoroscopes', 'reviewFeedbackMissingFeatures',
            'reviewFeedbackOther', 'reviewFeedbackPlaceholder', 'reviewFeedbackSend',
            'reviewFeedbackSubtitle', 'reviewFeedbackThankYou', 'reviewFeedbackTitle',
            'reviewFeedbackTooExpensive', 'reviewSubmit', 'reviewRatingTitle',
            'reviewNotNow', 'reviewRatingExcellent', 'reviewRatingGood', 'reviewRatingOkay',
            'reviewRatingPoor', 'reviewRatingVeryPoor', 'reviewWasThisHelpful'
        ],
        'fr': [
            'reviewFeedbackAppCrashes', 'reviewFeedbackCommonIssues', 'reviewFeedbackConfusingUI',
            'reviewFeedbackHelpsImprove', 'reviewFeedbackInaccurateHoroscopes', 'reviewFeedbackMissingFeatures',
            'reviewFeedbackOther', 'reviewFeedbackPlaceholder', 'reviewFeedbackSend',
            'reviewFeedbackSubtitle', 'reviewFeedbackThankYou', 'reviewFeedbackTitle',
            'reviewFeedbackTooExpensive', 'reviewSubmit', 'compatibility_adviceLabel',
            'compatibility_monthlyPredictionsTitle', 'reviewRatingTitle',
            'compatibility_dimensionChemistry', 'compatibility_dimensionCommunication',
            'compatibility_dimensionConflicts', 'compatibility_dimensionFriendship',
            'compatibility_dimensionGoals', 'compatibility_dimensionIntellectual',
            'compatibility_dimensionRomantic', 'compatibility_dimensionWork',
            'compatibility_levelExcellent', 'compatibility_levelFair', 'compatibility_levelGood',
            'compatibility_levelLow', 'compatibility_monthApril', 'compatibility_monthFebruary',
            'compatibility_monthJanuary', 'compatibility_monthMarch', 'compatibility_prediction1',
            'compatibility_prediction2', 'compatibility_prediction3', 'compatibility_prediction4',
            'compatibility_selectPartnerSign', 'reviewNotNow', 'reviewRatingExcellent',
            'reviewRatingGood', 'reviewRatingOkay', 'reviewRatingPoor', 'reviewRatingVeryPoor',
            'reviewWasThisHelpful'
        ]
    }

    for lang in ['de', 'fr']:
        print(f"\n{'='*80}")
        print(f"Missing translations for {lang.upper()}")
        print('='*80)

        for key in missing[lang]:
            en_value = en_data.get(key, 'NOT FOUND')
            es_value = es_data.get(key, 'NOT FOUND')
            print(f"\nKey: {key}")
            print(f"  EN: {en_value}")
            print(f"  ES: {es_value}")

if __name__ == '__main__':
    main()
