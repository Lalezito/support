#!/usr/bin/env python3
"""
Script para extraer FIREBASE_PRIVATE_KEY del service account JSON
y darle el formato correcto para Railway (con \\n como texto literal)
"""

import json
import sys

def extract_private_key():
    """
    Lee el archivo service account JSON y extrae la private key
    en el formato correcto para Railway
    """

    # Pedir path al archivo JSON
    print("🔥 Firebase Private Key Extractor\n")
    print("Este script extrae la private key del archivo service account JSON")
    print("y la formatea correctamente para Railway.\n")

    json_path = input("Path al archivo service account JSON (ej: firebase-service-account.json): ").strip()

    try:
        with open(json_path, 'r') as f:
            service_account = json.load(f)

        # Extraer la private key
        private_key = service_account.get('private_key')

        if not private_key:
            print("❌ Error: No se encontró 'private_key' en el archivo JSON")
            return

        # La private key ya viene con \n como caracteres literales
        # (no saltos de línea reales)
        print("\n✅ Private key extraída correctamente!\n")
        print("=" * 60)
        print("FIREBASE_PRIVATE_KEY (copia esto):")
        print("=" * 60)
        print(private_key)
        print("=" * 60)

        # También extraer otras variables útiles
        print("\n📋 Otras variables de Firebase:\n")
        print(f"FIREBASE_PROJECT_ID={service_account.get('project_id', 'N/A')}")
        print(f"FIREBASE_CLIENT_EMAIL={service_account.get('client_email', 'N/A')}")
        print(f"FIREBASE_PRIVATE_KEY_ID={service_account.get('private_key_id', 'N/A')}")
        print(f"FIREBASE_CLIENT_ID={service_account.get('client_id', 'N/A')}")

    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{json_path}'")
        print("Verifica el path e intenta de nuevo")
    except json.JSONDecodeError:
        print("❌ Error: El archivo no es un JSON válido")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    extract_private_key()
