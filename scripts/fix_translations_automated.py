#!/usr/bin/env python3
"""
Automated Translation Fixes Script
==================================
Fixes spacing issues, renames duplicates, adds missing keys, and validates parity.

Usage:
    python3 fix_translations_automated.py [--dry-run] [--backup]

Options:
    --dry-run    Show changes without applying them
    --backup     Create backup before applying changes

Author: Claude Code Agent
Date: October 15, 2025
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple
import argparse
import shutil

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
L10N_DIR = PROJECT_ROOT / "zodiac_app" / "assets" / "l10n"
BACKUP_DIR = PROJECT_ROOT / "backups" / f"translations_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

LANGUAGES = ['en', 'es', 'de', 'fr', 'it', 'pt']

# Key consolidation mappings
KEY_CONSOLIDATIONS = {
    # Duplicates to consolidate
    'update_available': 'updateAvailable',
    'coming_soon': 'comingSoon',
    'keyWords': 'keywords',

    # Feature keys to rename
    'feature1': 'premium_feature_unlimitedHoroscopes',
    'feature2': 'premium_feature_advancedAI',
    'feature3': 'premium_feature_extendedTracking',
    'feature4': 'premium_feature_personalizedRecommendations',
    'feature5': 'premium_feature_customGoals',
    'feature6': 'premium_feature_adFree',
    'feature7': 'premium_feature_fullCompatibility',
    'feature8': 'premium_feature_predictionsDashboard',
    'feature9': 'premium_feature_detailedForecasts',
    'feature10': 'premium_feature_aiInsights',
    'feature11': 'premium_feature_unlimitedCoaching',
    'feature12': 'premium_feature_advancedCompatibility',
    'feature13': 'premium_feature_priorityContent',
    'feature14': 'premium_feature_crisisAI',
    'feature15': 'premium_feature_pdfExport',

    # Generic keys to add context
    'error': 'generic_error',
    'success': 'generic_success',
    'warning': 'generic_warning',
}

# Missing IAP error message keys
MISSING_IAP_KEYS = {
    'iap_error_connection': 'Unable to connect to the store. Please check your internet connection.',
    'iap_error_cancelled': 'Purchase was cancelled.',
    'iap_error_payment_invalid': 'Payment method is invalid.',
    'iap_error_payment_not_allowed': 'Payment is not allowed on this device.',
    'iap_error_product_not_available': 'This product is not available.',
    'iap_error_already_owned': 'You already own this product.',
    'iap_error_restoration_failed': 'Failed to restore purchases. Please try again.',
    'iap_error_unknown': 'An unknown error occurred. Please try again.',
}

# Keys with malformed spacing (examples found in analysis)
SPACING_FIXES = {
    'active_activepredictionslength': 'active_activePredictionsLength',
    'pending_pendingpredictionslength': 'pending_pendingPredictionsLength',
    'history_verifiedpredictionslength': 'history_verifiedPredictionsLength',
}

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TranslationFixer:
    def __init__(self, dry_run: bool = False, create_backup: bool = True):
        self.dry_run = dry_run
        self.create_backup = create_backup
        self.stats = {
            'files_processed': 0,
            'spacing_fixes': 0,
            'key_renames': 0,
            'keys_added': 0,
            'duplicates_removed': 0,
            'errors': 0
        }

    def log(self, message: str, color: str = Colors.END, bold: bool = False):
        """Print colored log message"""
        prefix = f"{Colors.BOLD}" if bold else ""
        print(f"{prefix}{color}{message}{Colors.END}")

    def load_arb_file(self, filepath: Path) -> Dict:
        """Load and parse ARB file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.log(f"Error loading {filepath}: {e}", Colors.RED)
            self.stats['errors'] += 1
            return {}

    def save_arb_file(self, filepath: Path, data: Dict):
        """Save ARB file with proper formatting"""
        try:
            if self.dry_run:
                self.log(f"[DRY RUN] Would save: {filepath}", Colors.YELLOW)
                return

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write('\n')  # Add trailing newline
            self.log(f"Saved: {filepath}", Colors.GREEN)
        except Exception as e:
            self.log(f"Error saving {filepath}: {e}", Colors.RED)
            self.stats['errors'] += 1

    def backup_files(self):
        """Create backup of all translation files"""
        if not self.create_backup:
            return

        self.log(f"\nCreating backup in: {BACKUP_DIR}", Colors.CYAN, bold=True)
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)

        for lang in LANGUAGES:
            src = L10N_DIR / f"app_{lang}.arb"
            if src.exists():
                dst = BACKUP_DIR / f"app_{lang}.arb"
                shutil.copy2(src, dst)
                self.log(f"Backed up: app_{lang}.arb", Colors.CYAN)

    def fix_spacing_issues(self, data: Dict) -> Dict:
        """Fix malformed keys with spacing issues"""
        fixed_data = {}

        for key, value in data.items():
            # Skip metadata keys
            if key.startswith('@'):
                fixed_data[key] = value
                continue

            # Apply spacing fixes
            if key in SPACING_FIXES:
                new_key = SPACING_FIXES[key]
                fixed_data[new_key] = value
                self.stats['spacing_fixes'] += 1
                self.log(f"  Fixed spacing: {key} → {new_key}", Colors.GREEN)
            else:
                fixed_data[key] = value

        return fixed_data

    def consolidate_keys(self, data: Dict) -> Dict:
        """Rename duplicate keys to consolidated versions"""
        consolidated_data = {}

        for key, value in data.items():
            # Skip metadata keys
            if key.startswith('@'):
                consolidated_data[key] = value
                continue

            # Apply key consolidation
            if key in KEY_CONSOLIDATIONS:
                new_key = KEY_CONSOLIDATIONS[key]
                consolidated_data[new_key] = value
                self.stats['key_renames'] += 1
                self.log(f"  Renamed: {key} → {new_key}", Colors.YELLOW)
            else:
                consolidated_data[key] = value

        return consolidated_data

    def add_missing_keys(self, data: Dict, lang: str) -> Dict:
        """Add missing IAP error message keys"""
        # For English, use the defined messages
        if lang == 'en':
            for key, message in MISSING_IAP_KEYS.items():
                if key not in data:
                    data[key] = message
                    self.stats['keys_added'] += 1
                    self.log(f"  Added: {key}", Colors.BLUE)
        else:
            # For other languages, mark as needing translation
            for key in MISSING_IAP_KEYS.keys():
                if key not in data:
                    data[key] = f"[TRANSLATE] {MISSING_IAP_KEYS[key]}"
                    self.stats['keys_added'] += 1
                    self.log(f"  Added (needs translation): {key}", Colors.YELLOW)

        return data

    def remove_duplicates(self, data: Dict) -> Dict:
        """Remove duplicate keys (old versions after consolidation)"""
        keys_to_remove = set()

        # If we renamed a key, remove the old one
        for old_key in KEY_CONSOLIDATIONS.keys():
            if old_key in data and KEY_CONSOLIDATIONS[old_key] in data:
                keys_to_remove.add(old_key)
                self.stats['duplicates_removed'] += 1
                self.log(f"  Removed duplicate: {old_key}", Colors.RED)

        return {k: v for k, v in data.items() if k not in keys_to_remove}

    def validate_key_consistency(self, all_data: Dict[str, Dict]) -> Tuple[bool, List[str]]:
        """Validate that all languages have the same keys"""
        issues = []

        # Get all keys from English (base)
        en_keys = set(k for k in all_data['en'].keys() if not k.startswith('@'))

        for lang in LANGUAGES:
            if lang == 'en':
                continue

            lang_keys = set(k for k in all_data[lang].keys() if not k.startswith('@'))

            # Check for missing keys
            missing = en_keys - lang_keys
            if missing:
                issues.append(f"{lang}: Missing {len(missing)} keys: {list(missing)[:5]}...")

            # Check for extra keys
            extra = lang_keys - en_keys
            if extra:
                issues.append(f"{lang}: Has {len(extra)} extra keys: {list(extra)[:5]}...")

        return len(issues) == 0, issues

    def check_english_in_translations(self, data: Dict, lang: str) -> List[str]:
        """Check for English text in non-English files"""
        if lang == 'en':
            return []

        issues = []

        # Common English words that shouldn't appear in translations
        english_indicators = [
            'the', 'and', 'or', 'but', 'your', 'you', 'with', 'this', 'that',
            'have', 'from', 'they', 'been', 'which', 'their'
        ]

        for key, value in data.items():
            if key.startswith('@'):
                continue

            if isinstance(value, str):
                lower_value = value.lower()
                # Check if value contains multiple English indicator words
                english_count = sum(1 for word in english_indicators if f' {word} ' in f' {lower_value} ')
                if english_count >= 3:
                    issues.append(f"{key}: '{value[:50]}...'")

        return issues

    def validate_naming_convention(self, data: Dict) -> Dict[str, int]:
        """Validate naming conventions"""
        conventions = {
            'camelCase': 0,
            'snake_case': 0,
            'lowercase': 0,
            'mixed': 0
        }

        for key in data.keys():
            if key.startswith('@'):
                continue

            # Check naming pattern
            if '_' in key and any(c.isupper() for c in key):
                conventions['mixed'] += 1
            elif '_' in key:
                conventions['snake_case'] += 1
            elif any(c.isupper() for c in key):
                conventions['camelCase'] += 1
            else:
                conventions['lowercase'] += 1

        return conventions

    def process_file(self, lang: str) -> Dict:
        """Process a single translation file"""
        filepath = L10N_DIR / f"app_{lang}.arb"

        self.log(f"\n{Colors.BOLD}Processing: app_{lang}.arb{Colors.END}", Colors.CYAN, bold=True)

        # Load file
        data = self.load_arb_file(filepath)
        if not data:
            return data

        # Apply fixes
        data = self.fix_spacing_issues(data)
        data = self.consolidate_keys(data)
        data = self.add_missing_keys(data, lang)
        data = self.remove_duplicates(data)

        # Save file
        self.save_arb_file(filepath, data)
        self.stats['files_processed'] += 1

        return data

    def run(self):
        """Run the complete fix process"""
        self.log(f"\n{Colors.BOLD}{'='*80}{Colors.END}", Colors.CYAN)
        self.log(f"{Colors.BOLD}Translation Automation Script{Colors.END}", Colors.CYAN, bold=True)
        self.log(f"{Colors.BOLD}{'='*80}{Colors.END}", Colors.CYAN)

        if self.dry_run:
            self.log("\n[DRY RUN MODE] No changes will be made", Colors.YELLOW, bold=True)

        # Backup files
        if self.create_backup and not self.dry_run:
            self.backup_files()

        # Process all files
        all_data = {}
        for lang in LANGUAGES:
            all_data[lang] = self.process_file(lang)

        # Validation
        self.log(f"\n{Colors.BOLD}Running Validation...{Colors.END}", Colors.CYAN, bold=True)

        # Check key consistency
        is_consistent, issues = self.validate_key_consistency(all_data)
        if is_consistent:
            self.log("✓ All languages have consistent keys", Colors.GREEN)
        else:
            self.log("✗ Key consistency issues found:", Colors.RED)
            for issue in issues:
                self.log(f"  - {issue}", Colors.RED)

        # Check for English text in translations
        for lang in LANGUAGES:
            if lang == 'en':
                continue
            english_issues = self.check_english_in_translations(all_data[lang], lang)
            if english_issues:
                self.log(f"\n⚠ Potential English text in {lang}:", Colors.YELLOW)
                for issue in english_issues[:5]:  # Show first 5
                    self.log(f"  - {issue}", Colors.YELLOW)

        # Check naming conventions
        self.log(f"\n{Colors.BOLD}Naming Convention Analysis:{Colors.END}", Colors.CYAN)
        conventions = self.validate_naming_convention(all_data['en'])
        for convention, count in conventions.items():
            self.log(f"  {convention}: {count} keys", Colors.CYAN)

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print summary of changes"""
        self.log(f"\n{Colors.BOLD}{'='*80}{Colors.END}", Colors.CYAN)
        self.log(f"{Colors.BOLD}Summary{Colors.END}", Colors.CYAN, bold=True)
        self.log(f"{Colors.BOLD}{'='*80}{Colors.END}", Colors.CYAN)

        self.log(f"Files processed:      {self.stats['files_processed']}", Colors.GREEN)
        self.log(f"Spacing fixes:        {self.stats['spacing_fixes']}", Colors.GREEN)
        self.log(f"Keys renamed:         {self.stats['key_renames']}", Colors.YELLOW)
        self.log(f"Keys added:           {self.stats['keys_added']}", Colors.BLUE)
        self.log(f"Duplicates removed:   {self.stats['duplicates_removed']}", Colors.RED)
        self.log(f"Errors:               {self.stats['errors']}", Colors.RED if self.stats['errors'] > 0 else Colors.GREEN)

        if self.create_backup and not self.dry_run:
            self.log(f"\nBackup location: {BACKUP_DIR}", Colors.CYAN)

        self.log(f"\n{Colors.BOLD}{'='*80}{Colors.END}\n", Colors.CYAN)

def main():
    parser = argparse.ArgumentParser(
        description='Automated translation fixes for Zodiac App'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show changes without applying them'
    )
    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Skip creating backup'
    )

    args = parser.parse_args()

    fixer = TranslationFixer(
        dry_run=args.dry_run,
        create_backup=not args.no_backup
    )

    try:
        fixer.run()
        sys.exit(0)
    except KeyboardInterrupt:
        fixer.log("\n\nProcess interrupted by user", Colors.YELLOW)
        sys.exit(1)
    except Exception as e:
        fixer.log(f"\nFatal error: {e}", Colors.RED, bold=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
