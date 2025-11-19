#!/usr/bin/env python3
"""
🌍 Script de Validación de Paridad de Traducciones
Verifica que todas las claves existan en todos los idiomas
Parte del Plan Maestro Premium i18n - Oct 31, 2025
"""

import json
import sys
from pathlib import Path

# Colores para terminal
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

# Idiomas soportados
LANGUAGES = ['en', 'es', 'de', 'fr', 'it', 'pt']
BASE_LANG = 'en'

# Directorio de localizaciones
L10N_DIR = Path('zodiac_app/assets/l10n')

def load_arb_file(lang: str) -> dict:
    """Carga un archivo .arb y retorna sus claves"""
    file_path = L10N_DIR / f'app_{lang}.arb'

    if not file_path.exists():
        print(f"{Colors.RED}❌ Archivo no encontrado: {file_path}{Colors.NC}")
        return {}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Filtrar claves que empiezan con @ (metadata)
        keys = {k for k in data.keys() if not k.startswith('@')}
        return keys

    except json.JSONDecodeError as e:
        print(f"{Colors.RED}❌ Error al parsear JSON en {file_path}:{Colors.NC}")
        print(f"   {str(e)}")
        return set()
    except Exception as e:
        print(f"{Colors.RED}❌ Error al leer {file_path}:{Colors.NC}")
        print(f"   {str(e)}")
        return set()

def main():
    print(f"{Colors.BLUE}Verificando paridad de traducciones...{Colors.NC}\n")

    # Cargar claves de idioma base (inglés)
    base_keys = load_arb_file(BASE_LANG)

    if not base_keys:
        print(f"{Colors.RED}❌ No se pudieron cargar las claves del idioma base (EN){Colors.NC}")
        sys.exit(1)

    print(f"{Colors.GREEN}✅ Idioma base (EN): {len(base_keys)} claves{Colors.NC}\n")

    errors = []
    warnings = []

    # Verificar cada idioma
    for lang in LANGUAGES:
        if lang == BASE_LANG:
            continue

        print(f"Verificando {lang.upper()}...", end=' ')

        lang_keys = load_arb_file(lang)

        if not lang_keys:
            errors.append(f"❌ {lang.upper()}: No se pudieron cargar las claves")
            print(f"{Colors.RED}ERROR{Colors.NC}")
            continue

        # Claves faltantes (en base pero no en este idioma)
        missing = base_keys - lang_keys

        # Claves extras (en este idioma pero no en base)
        extra = lang_keys - base_keys

        if missing or extra:
            print(f"{Colors.YELLOW}ADVERTENCIAS{Colors.NC}")

            if missing:
                errors.append(f"❌ {lang.upper()}: Faltan {len(missing)} claves")
                print(f"\n{Colors.RED}   Claves faltantes en {lang.upper()}:{Colors.NC}")
                for key in sorted(list(missing))[:10]:  # Mostrar primeras 10
                    print(f"   - {key}")
                if len(missing) > 10:
                    print(f"   ... y {len(missing) - 10} más\n")

            if extra:
                warnings.append(f"⚠️  {lang.upper()}: {len(extra)} claves extras (no en EN)")
                print(f"\n{Colors.YELLOW}   Claves extras en {lang.upper()} (no en EN):{Colors.NC}")
                for key in sorted(list(extra))[:5]:  # Mostrar primeras 5
                    print(f"   - {key}")
                if len(extra) > 5:
                    print(f"   ... y {len(extra) - 5} más\n")
        else:
            print(f"{Colors.GREEN}OK ({len(lang_keys)} claves){Colors.NC}")

    # Reporte final
    print("\n" + "━" * 50)
    print()

    if errors:
        print(f"{Colors.RED}❌ ERRORES ENCONTRADOS:{Colors.NC}\n")
        for error in errors:
            print(f"   {error}")
        print()

    if warnings:
        print(f"{Colors.YELLOW}⚠️  ADVERTENCIAS:{Colors.NC}\n")
        for warning in warnings:
            print(f"   {warning}")
        print()

    if not errors and not warnings:
        print(f"{Colors.GREEN}✅ Todas las traducciones están sincronizadas{Colors.NC}")
        print(f"\nTotal de claves: {len(base_keys)} en {len(LANGUAGES)} idiomas")
        return 0

    if errors:
        print(f"{Colors.RED}❌ Validación falló: {len(errors)} errores{Colors.NC}")
        return 1
    else:
        print(f"{Colors.YELLOW}⚠️  Validación con advertencias (no críticas){Colors.NC}")
        return 0

if __name__ == '__main__':
    sys.exit(main())
