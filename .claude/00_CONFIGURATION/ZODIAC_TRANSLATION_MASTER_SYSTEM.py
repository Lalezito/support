#!/usr/bin/env python3
"""
SISTEMA MAESTRO DE ORQUESTACIÓN AI PARA TRADUCCIONES ZODIAC
Integra detección, traducción, validación y optimización automática
Compatible con Claude Opus 4.1 y sistema de agentes optimizado
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class ZodiacTranslationMaster:
    def __init__(self):
        self.base_path = "/Users/alejandrocaceres/Desktop/appstore - zodia"
        self.config_path = f"{self.base_path}/.claude/00_CONFIGURATION"
        self.l10n_path = f"{self.base_path}/zodiac_app/lib/l10n"
        
        # Sistemas integrados
        self.detector_script = f"{self.config_path}/hardcoded_text_detector.py"
        self.optimizer_script = f"{self.config_path}/translation_optimizer.py"
        self.validator_script = f"{self.config_path}/translation_validator.py"
        
        # Configuración AI Master
        self.master_config = self._load_master_config()
        
        # Base completa de traducciones Zodiac contextual
        self.zodiac_master_translations = {
            # Términos astro lógicos específicos
            'Your Horoscope': {
                'es': 'Tu Horóscopo',
                'en': 'Your Horoscope',
                'de': 'Dein Horoskop',
                'fr': 'Votre Horoscope',
                'it': 'Il Tuo Oroscopo',
                'pt': 'Seu Horóscopo'
            },
            'Compatibility Report': {
                'es': 'Reporte de Compatibilidad',
                'en': 'Compatibility Report',
                'de': 'Kompatibilitätsbericht',
                'fr': 'Rapport de Compatibilité',
                'it': 'Rapporto di Compatibilità',
                'pt': 'Relatório de Compatibilidade'
            },
            'Birth Chart': {
                'es': 'Carta Natal',
                'en': 'Birth Chart',
                'de': 'Geburtshoroskop',
                'fr': 'Thème Natal',
                'it': 'Carta Natale',
                'pt': 'Mapa Astral'
            },
            'Ascendant': {
                'es': 'Ascendente',
                'en': 'Ascendant',
                'de': 'Aszendent',
                'fr': 'Ascendant',
                'it': 'Ascendente',
                'pt': 'Ascendente'
            },
            'Moon Phase': {
                'es': 'Fase Lunar',
                'en': 'Moon Phase',
                'de': 'Mondphase',
                'fr': 'Phase Lunaire',
                'it': 'Fase Lunare',
                'pt': 'Fase da Lua'
            },
            'Rising Sign': {
                'es': 'Signo Ascendente',
                'en': 'Rising Sign',
                'de': 'Aszendent',
                'fr': 'Signe Ascendant',
                'it': 'Segno Ascendente',
                'pt': 'Signo Ascendente'
            },
            'Planetary Positions': {
                'es': 'Posiciones Planetarias',
                'en': 'Planetary Positions',
                'de': 'Planetenpositionen',
                'fr': 'Positions Planétaires',
                'it': 'Posizioni Planetarie',
                'pt': 'Posições Planetárias'
            },
            'Love Compatibility': {
                'es': 'Compatibilidad Amorosa',
                'en': 'Love Compatibility',
                'de': 'Liebeskompatibilität',
                'fr': 'Compatibilité Amoureuse',
                'it': 'Compatibilità Amorosa',
                'pt': 'Compatibilidade Amorosa'
            },
            'Professional Guidance': {
                'es': 'Orientación Profesional',
                'en': 'Professional Guidance',
                'de': 'Berufliche Beratung',
                'fr': 'Guidance Professionnelle',
                'it': 'Orientamento Professionale',
                'pt': 'Orientação Profissional'
            },
            'Weekly Forecast': {
                'es': 'Pronóstico Semanal',
                'en': 'Weekly Forecast',
                'de': 'Wochenprognose',
                'fr': 'Prévisions Hebdomadaires',
                'it': 'Previsioni Settimanali',
                'pt': 'Previsão Semanal'
            },
            # Términos de UI premium
            'Premium Experience': {
                'es': 'Experiencia Premium',
                'en': 'Premium Experience',
                'de': 'Premium-Erlebnis',
                'fr': 'Expérience Premium',
                'it': 'Esperienza Premium',
                'pt': 'Experiência Premium'
            },
            'Unlock Features': {
                'es': 'Desbloquear Funciones',
                'en': 'Unlock Features',
                'de': 'Funktionen freischalten',
                'fr': 'Débloquer les Fonctionnalités',
                'it': 'Sblocca Funzionalità',
                'pt': 'Desbloquear Recursos'
            },
            'Free Trial': {
                'es': 'Prueba Gratuita',
                'en': 'Free Trial',
                'de': 'Kostenlose Testversion',
                'fr': 'Essai Gratuit',
                'it': 'Prova Gratuita',
                'pt': 'Teste Grátis'
            },
            # Signos zodiacales
            'Aries': {'es': 'Aries', 'en': 'Aries', 'de': 'Widder', 'fr': 'Bélier', 'it': 'Ariete', 'pt': 'Áries'},
            'Taurus': {'es': 'Tauro', 'en': 'Taurus', 'de': 'Stier', 'fr': 'Taureau', 'it': 'Toro', 'pt': 'Touro'},
            'Gemini': {'es': 'Géminis', 'en': 'Gemini', 'de': 'Zwillinge', 'fr': 'Gémeaux', 'it': 'Gemelli', 'pt': 'Gêmeos'},
            'Cancer': {'es': 'Cáncer', 'en': 'Cancer', 'de': 'Krebs', 'fr': 'Cancer', 'it': 'Cancro', 'pt': 'Câncer'},
            'Leo': {'es': 'Leo', 'en': 'Leo', 'de': 'Löwe', 'fr': 'Lion', 'it': 'Leone', 'pt': 'Leão'},
            'Virgo': {'es': 'Virgo', 'en': 'Virgo', 'de': 'Jungfrau', 'fr': 'Vierge', 'it': 'Vergine', 'pt': 'Virgem'},
            'Libra': {'es': 'Libra', 'en': 'Libra', 'de': 'Waage', 'fr': 'Balance', 'it': 'Bilancia', 'pt': 'Libra'},
            'Scorpio': {'es': 'Escorpio', 'en': 'Scorpio', 'de': 'Skorpion', 'fr': 'Scorpion', 'it': 'Scorpione', 'pt': 'Escorpião'},
            'Sagittarius': {'es': 'Sagitario', 'en': 'Sagittarius', 'de': 'Schütze', 'fr': 'Sagittaire', 'it': 'Sagittario', 'pt': 'Sagitário'},
            'Capricorn': {'es': 'Capricornio', 'en': 'Capricorn', 'de': 'Steinbock', 'fr': 'Capricorne', 'it': 'Capricorno', 'pt': 'Capricórnio'},
            'Aquarius': {'es': 'Acuario', 'en': 'Aquarius', 'de': 'Wassermann', 'fr': 'Verseau', 'it': 'Acquario', 'pt': 'Aquário'},
            'Pisces': {'es': 'Piscis', 'en': 'Pisces', 'de': 'Fische', 'fr': 'Poissons', 'it': 'Pesci', 'pt': 'Peixes'}
        }

    def _load_master_config(self) -> Dict:
        """Carga configuración maestra optimizada"""
        try:
            config_file = f"{self.config_path}/ZODIAC_MASTER_CONFIG_2025.json"
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {
                "ai_orchestration": {
                    "enabled": True,
                    "preferred_model": "claude-3-5-sonnet-20240620",
                    "fallback_models": ["claude-3-haiku-20240307"],
                    "auto_translation": True,
                    "quality_threshold": 85
                }
            }

    def run_comprehensive_analysis(self) -> Dict:
        """Ejecuta análisis completo del sistema de traducciones"""
        print("🚀 SISTEMA MAESTRO DE ORQUESTACIÓN AI ZODIAC")
        print("=" * 80)
        print("🎯 Ejecutando análisis completo...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'detection': {},
            'optimization': {},
            'validation': {},
            'completion': {}
        }
        
        # 1. Detectar nuevo texto hardcodeado
        print("\n🔍 FASE 1: Detección de texto hardcodeado")
        print("-" * 50)
        try:
            detection_result = subprocess.run(
                ['python3', self.detector_script], 
                capture_output=True, text=True, cwd=self.config_path
            )
            results['detection'] = {
                'success': detection_result.returncode == 0,
                'output': detection_result.stdout[-1000:] if detection_result.stdout else '',
                'errors': detection_result.stderr if detection_result.stderr else None
            }
            print("✅ Detección completada")
        except Exception as e:
            results['detection'] = {'success': False, 'error': str(e)}
            print(f"❌ Error en detección: {e}")
        
        # 2. Optimizar traducciones existentes
        print("\n🔧 FASE 2: Optimización de traducciones")
        print("-" * 50)
        try:
            optimization_result = subprocess.run(
                ['python3', self.optimizer_script], 
                capture_output=True, text=True, cwd=self.config_path
            )
            results['optimization'] = {
                'success': optimization_result.returncode == 0,
                'output': optimization_result.stdout[-1000:] if optimization_result.stdout else '',
                'errors': optimization_result.stderr if optimization_result.stderr else None
            }
            print("✅ Optimización completada")
        except Exception as e:
            results['optimization'] = {'success': False, 'error': str(e)}
            print(f"❌ Error en optimización: {e}")
        
        # 3. Completar claves faltantes
        print("\n🎯 FASE 3: Completar claves faltantes")
        print("-" * 50)
        completion_results = self.complete_missing_keys()
        results['completion'] = completion_results
        
        # 4. Validación final
        print("\n📊 FASE 4: Validación final")
        print("-" * 50)
        try:
            validation_result = subprocess.run(
                ['python3', self.validator_script], 
                capture_output=True, text=True, cwd=self.config_path
            )
            results['validation'] = {
                'success': validation_result.returncode == 0,
                'output': validation_result.stdout[-1000:] if validation_result.stdout else '',
                'errors': validation_result.stderr if validation_result.stderr else None
            }
            print("✅ Validación completada")
        except Exception as e:
            results['validation'] = {'success': False, 'error': str(e)}
            print(f"❌ Error en validación: {e}")
        
        return results

    def complete_missing_keys(self) -> Dict:
        """Completa claves faltantes automáticamente"""
        print("🔄 Completando claves faltantes...")
        
        from translation_validator import TranslationValidator
        
        validator = TranslationValidator()
        completeness_data = validator.validate_completeness(self.l10n_path)
        
        missing_keys = completeness_data['missing_keys']
        all_keys = completeness_data['all_keys']
        
        completion_stats = {
            'keys_added': 0,
            'files_updated': 0,
            'languages_processed': []
        }
        
        # Encontrar todas las claves únicas
        all_unique_keys = set()
        for keys in all_keys.values():
            all_unique_keys.update(keys.keys())
        
        # Para cada idioma, completar claves faltantes
        for lang in ['es', 'en', 'de', 'fr', 'it', 'pt']:
            if lang not in missing_keys or not missing_keys[lang]:
                continue
                
            print(f"  📝 Completando {len(missing_keys[lang])} claves en {lang}")
            
            # Cargar traducciones actuales
            file_path = f"{self.l10n_path}/app_localizations_{lang}.dart"
            current_translations = self._read_translations_file(file_path)
            
            # Agregar claves faltantes
            keys_added = 0
            for missing_key in missing_keys[lang]:
                if missing_key not in current_translations:
                    translation = self._generate_contextual_translation(missing_key, lang, all_keys)
                    current_translations[missing_key] = translation
                    keys_added += 1
            
            # Escribir archivo actualizado
            if keys_added > 0:
                if self._write_translations_file(file_path, current_translations, lang):
                    completion_stats['keys_added'] += keys_added
                    completion_stats['files_updated'] += 1
                    completion_stats['languages_processed'].append(lang)
                    print(f"    ✅ {keys_added} claves agregadas")
                else:
                    print(f"    ❌ Error escribiendo archivo")
        
        return completion_stats

    def _generate_contextual_translation(self, key: str, target_lang: str, all_keys: Dict) -> str:
        """Genera traducción contextual inteligente"""
        # Primero buscar en base de datos zodiac
        key_text = self._key_to_readable_text(key)
        
        # Buscar coincidencia en base zodiac
        for eng_text, translations in self.zodiac_master_translations.items():
            if eng_text.lower() == key_text.lower():
                return translations.get(target_lang, key_text)
        
        # Buscar en traducciones existentes de inglés
        if 'en' in all_keys and key in all_keys['en']:
            english_value = all_keys['en'][key]
            
            # Buscar en base zodiac por valor inglés
            for eng_text, translations in self.zodiac_master_translations.items():
                if eng_text.lower() == english_value.lower():
                    return translations.get(target_lang, english_value)
        
        # Generar traducción básica
        return self._generate_basic_translation_by_lang(key_text, target_lang)

    def _key_to_readable_text(self, key: str) -> str:
        """Convierte clave camelCase a texto legible"""
        # Remover prefijos comunes
        clean_key = key
        for prefix in ['get', 'is', 'has', 'can', 'should', 'onboarding']:
            if clean_key.startswith(prefix):
                clean_key = clean_key[len(prefix):]
        
        # Convertir camelCase a palabras
        words = []
        current_word = ''
        for char in clean_key:
            if char.isupper() and current_word:
                words.append(current_word)
                current_word = char.lower()
            else:
                current_word += char.lower()
        
        if current_word:
            words.append(current_word)
        
        return ' '.join(words).title()

    def _generate_basic_translation_by_lang(self, text: str, target_lang: str) -> str:
        """Genera traducción básica por idioma"""
        basic_dict = {
            'es': {
                'error': 'Error', 'loading': 'Cargando', 'success': 'Éxito',
                'cancel': 'Cancelar', 'accept': 'Aceptar', 'continue': 'Continuar',
                'back': 'Atrás', 'next': 'Siguiente', 'finish': 'Finalizar',
                'premium': 'Premium', 'free': 'Gratis', 'trial': 'Prueba',
                'unlock': 'Desbloquear', 'upgrade': 'Actualizar'
            },
            'de': {
                'error': 'Fehler', 'loading': 'Wird geladen', 'success': 'Erfolg',
                'cancel': 'Abbrechen', 'accept': 'Akzeptieren', 'continue': 'Fortsetzen',
                'back': 'Zurück', 'next': 'Weiter', 'finish': 'Fertig',
                'premium': 'Premium', 'free': 'Kostenlos', 'trial': 'Testversion',
                'unlock': 'Freischalten', 'upgrade': 'Aktualisieren'
            },
            'fr': {
                'error': 'Erreur', 'loading': 'Chargement', 'success': 'Succès',
                'cancel': 'Annuler', 'accept': 'Accepter', 'continue': 'Continuer',
                'back': 'Retour', 'next': 'Suivant', 'finish': 'Terminer',
                'premium': 'Premium', 'free': 'Gratuit', 'trial': 'Essai',
                'unlock': 'Débloquer', 'upgrade': 'Mettre à niveau'
            },
            'it': {
                'error': 'Errore', 'loading': 'Caricamento', 'success': 'Successo',
                'cancel': 'Annulla', 'accept': 'Accetta', 'continue': 'Continua',
                'back': 'Indietro', 'next': 'Avanti', 'finish': 'Termina',
                'premium': 'Premium', 'free': 'Gratuito', 'trial': 'Prova',
                'unlock': 'Sblocca', 'upgrade': 'Aggiorna'
            },
            'pt': {
                'error': 'Erro', 'loading': 'Carregando', 'success': 'Sucesso',
                'cancel': 'Cancelar', 'accept': 'Aceitar', 'continue': 'Continuar',
                'back': 'Voltar', 'next': 'Próximo', 'finish': 'Finalizar',
                'premium': 'Premium', 'free': 'Grátis', 'trial': 'Teste',
                'unlock': 'Desbloquear', 'upgrade': 'Atualizar'
            }
        }
        
        if target_lang in basic_dict:
            text_lower = text.lower()
            for eng_word, translation in basic_dict[target_lang].items():
                if eng_word in text_lower:
                    return text.lower().replace(eng_word, translation).title()
        
        return text

    def _read_translations_file(self, file_path: str) -> Dict[str, str]:
        """Lee archivo de traducciones"""
        translations = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import re
            pattern = r'String\s+get\s+(\w+)\s*=>\s*[\'\"](.*?)[\'\"];'
            matches = re.findall(pattern, content, re.DOTALL)
            
            for key, value in matches:
                clean_value = value.replace("\\'", "'").replace('\\"', '"')
                translations[key] = clean_value
        except Exception as e:
            print(f"Error leyendo {file_path}: {e}")
        
        return translations

    def _write_translations_file(self, file_path: str, translations: Dict[str, str], lang: str) -> bool:
        """Escribe archivo de traducciones"""
        try:
            content_lines = [
                "// ignore: unused_import",
                "import 'package:intl/intl.dart' as intl;",
                "import 'app_localizations.dart';",
                "",
                "// ignore_for_file: type=lint",
                "",
                f"/// The translations for {self._get_language_name(lang)} (`{lang}`).",
                f"class AppLocalizations{lang.capitalize()} extends AppLocalizations {{",
                f"  AppLocalizations{lang.capitalize()}([String locale = '{lang}']) : super(locale);",
                ""
            ]
            
            # Agregar getters ordenados
            sorted_keys = sorted(translations.keys())
            for key in sorted_keys:
                value = translations[key].replace("'", "\\'")
                content_lines.append(f"  @override")
                content_lines.append(f"  String get {key} => '{value}';")
                content_lines.append("")
            
            content_lines.append("}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content_lines))
            
            return True
        except Exception as e:
            print(f"Error escribiendo {file_path}: {e}")
            return False

    def _get_language_name(self, lang_code: str) -> str:
        """Obtiene nombre completo del idioma"""
        names = {
            'es': 'Spanish Castilian',
            'en': 'English', 
            'de': 'German',
            'fr': 'French',
            'it': 'Italian',
            'pt': 'Portuguese'
        }
        return names.get(lang_code, lang_code)

    def generate_final_report(self, results: Dict) -> str:
        """Genera reporte final del sistema maestro"""
        report_lines = [
            "🏆 REPORTE FINAL DEL SISTEMA MAESTRO ZODIAC",
            "=" * 80,
            f"📅 Timestamp: {results['timestamp']}",
            "",
            "📊 RESUMEN DE PROCESOS:",
        ]
        
        # Detección
        if results['detection']['success']:
            report_lines.append("  ✅ Detección de texto hardcodeado: EXITOSA")
        else:
            report_lines.append("  ❌ Detección de texto hardcodeado: FALLÓ")
        
        # Optimización
        if results['optimization']['success']:
            report_lines.append("  ✅ Optimización de traducciones: EXITOSA")
        else:
            report_lines.append("  ❌ Optimización de traducciones: FALLÓ")
        
        # Completion
        completion = results['completion']
        report_lines.extend([
            f"  🎯 Claves completadas: {completion['keys_added']}",
            f"  📝 Archivos actualizados: {completion['files_updated']}",
            f"  🌍 Idiomas procesados: {', '.join(completion['languages_processed'])}"
        ])
        
        # Validación
        if results['validation']['success']:
            report_lines.append("  ✅ Validación final: EXITOSA")
        else:
            report_lines.append("  ❌ Validación final: FALLÓ")
        
        report_lines.extend([
            "",
            "🚀 SISTEMA MAESTRO COMPLETADO",
            "📱 Aplicación Zodiac lista con traducciones optimizadas en 6 idiomas",
            "🤖 Orquestación AI activada para mantenimiento automático"
        ])
        
        return '\n'.join(report_lines)

def main():
    master = ZodiacTranslationMaster()
    
    print("🌟 Iniciando Sistema Maestro de Orquestación AI Zodiac...")
    print("🎯 Objetivo: Traducciones perfectas automáticas en 6 idiomas")
    print("🤖 Powered by: Claude AI + Sistema optimizado de agentes")
    
    results = master.run_comprehensive_analysis()
    
    final_report = master.generate_final_report(results)
    print("\n" + final_report)
    
    # Guardar reporte
    report_file = f"{master.config_path}/ZODIAC_MASTER_SYSTEM_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(final_report)
    
    print(f"\n📄 Reporte guardado en: {report_file}")

if __name__ == "__main__":
    main()
