#!/usr/bin/env python3
"""
Fix Metadata Keys in Cosmic Coach ARB files
Replace MISSING_TRANSLATION in @key metadata with proper descriptions
"""

import json

# Metadata descriptions (language-neutral, professional descriptions)
METADATA = {
    "@advancedCosmicAnalysis": {
        "description": "Advanced cosmic analysis feature label"
    },
    "@advancedCosmicAnalysisDescription": {
        "description": "Description of advanced cosmic analysis features"
    },
    "@ai_coach_onboarding": {
        "description": "AI coach onboarding screen label"
    },
    "@analyticsCoachSessionsLabel": {
        "description": "Analytics label for coach sessions count"
    },
    "@analyticsCosmicCoachFeature": {
        "description": "Analytics label for cosmic coach feature"
    },
    "@analyticsGoalsCompleted": {
        "description": "Analytics label for completed goals count"
    },
    "@analyticsGoalsProgressTitle": {
        "description": "Analytics title for goals progress section"
    },
    "@cosmicBalance": {
        "description": "Cosmic balance message",
        "placeholders": {
            "element": {
                "type": "String",
                "example": "Fire"
            }
        }
    },
    "@cosmicGrowthPeriod": {
        "description": "Cosmic growth period label"
    },
    "@cosmicIntrospectionPeriod": {
        "description": "Cosmic introspection period label"
    },
    "@goalDetails": {
        "description": "Goal details screen title"
    },
    "@goals_empty_state": {
        "description": "Empty state message when no goals exist"
    },
    "@goal_completed_success": {
        "description": "Success message when goal is completed"
    },
    "@new_goals_generated": {
        "description": "Message shown when new goals are generated",
        "placeholders": {
            "userSign": {
                "type": "String",
                "example": "Aries"
            }
        }
    },
    "@smart_goals_generated": {
        "description": "Message shown when smart goals are generated",
        "placeholders": {
            "userSign": {
                "type": "String",
                "example": "Aries"
            }
        }
    },
    "@completeGoalQuestion": {
        "description": "Dialog title asking to confirm goal completion"
    },
    "@confirmCompleteGoal": {
        "description": "Confirmation message for completing a goal"
    },
    "@confirmDeleteGoal": {
        "description": "Confirmation message for deleting a goal"
    },
    "@deleteGoal": {
        "description": "Delete goal button label"
    },
    "@pauseGoal": {
        "description": "Pause goal button label"
    },
    "@premiumCosmicAnalysis": {
        "description": "Premium cosmic analysis feature label"
    },
    "@premiumCosmicAnalysisDescription": {
        "description": "Description of premium cosmic analysis features"
    },
}

# Add all celebration message metadata
categories = [
    "adventure", "career", "creativity", "finance", "fitness",
    "growth", "healing", "leadership", "learning", "mindfulness",
    "nature", "relationships", "service", "wellness"
]

for category in categories:
    for i in range(1, 4):
        key = f"@celebration_{category}_{i}"
        METADATA[key] = {
            "description": f"Celebration message {i} for {category} goal completion"
        }


def fix_metadata_keys(lang_code):
    """Fix metadata keys in ARB file"""

    input_path = f'/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output/features/cosmic_coach/cosmic_coach_{lang_code}.arb'

    # Read the current ARB file
    with open(input_path, 'r', encoding='utf-8') as f:
        arb_data = json.load(f)

    replacements = 0

    # Replace MISSING_TRANSLATION in metadata keys
    for key in list(arb_data.keys()):
        if key.startswith('@'):
            if arb_data[key] == "MISSING_TRANSLATION":
                if key in METADATA:
                    arb_data[key] = METADATA[key]
                    replacements += 1
                else:
                    # Provide a generic metadata object
                    arb_data[key] = {
                        "description": f"Translation for {key[1:]}"
                    }
                    replacements += 1

    # Write the updated ARB file
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(arb_data, f, indent=2, ensure_ascii=False)

    return replacements


def verify_no_missing(lang_code):
    """Verify that no MISSING_TRANSLATION strings remain"""

    input_path = f'/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output/features/cosmic_coach/cosmic_coach_{lang_code}.arb'

    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    missing_count = content.count('"MISSING_TRANSLATION"')
    return missing_count


def main():
    """Main execution function"""

    print("=" * 80)
    print("FIXING METADATA KEYS IN COSMIC COACH ARB FILES")
    print("=" * 80)
    print()

    languages = ['es', 'de', 'fr', 'it', 'pt']
    language_names = {
        'es': 'Spanish',
        'de': 'German',
        'fr': 'French',
        'it': 'Italian',
        'pt': 'Portuguese'
    }

    total_replacements = 0

    # Process each language
    for lang in languages:
        print(f"\n📝 Processing {language_names[lang]} ({lang})...")
        replacements = fix_metadata_keys(lang)
        total_replacements += replacements

        # Verify
        missing_count = verify_no_missing(lang)

        print(f"   ✅ Fixed {replacements} metadata entries")
        if missing_count == 0:
            print(f"   ✅ NO MISSING_TRANSLATION values remain!")
        else:
            print(f"   ⚠️  WARNING: {missing_count} MISSING_TRANSLATION values still remain")

    print("\n" + "=" * 80)
    print("FINAL VERIFICATION")
    print("=" * 80)

    all_clean = True
    for lang in languages:
        missing_count = verify_no_missing(lang)
        status = "✅ CLEAN" if missing_count == 0 else f"⚠️  {missing_count} MISSING"
        print(f"{language_names[lang]:12} ({lang}): {status}")
        if missing_count > 0:
            all_clean = False

    print("\n" + "=" * 80)
    if all_clean:
        print("✅ SUCCESS! All files are clean - no MISSING_TRANSLATION values remain!")
    else:
        print("⚠️  Some files still have MISSING_TRANSLATION values")
    print("=" * 80)


if __name__ == "__main__":
    main()
