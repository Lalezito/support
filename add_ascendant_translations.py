#!/usr/bin/env python3
"""
Script para agregar traducciones del Ascendant a los archivos .arb
"""
import json
import os

# Definir las traducciones para cada idioma
translations = {
    'en': {
        "calculatingRisingSign": "Calculating your rising sign...",
        "unableToLoadAscendantData": "Unable to load ascendant data",
        "completeBirthDataInSettings": "Please complete your birth data in Settings",
        "goBack": "Go Back",
        "yourRisingSign": "Your Rising Sign",
        "risingSignAscendant": "Rising Sign (Ascendant)",
        "aboutYourAscendant": "About Your Ascendant",
        "personalityTraits": "Personality Traits",
        "physicalPresence": "Physical Presence",
        "firstImpression": "First Impression",
        "yourStrengths": "Your Strengths",
        "growthAreas": "Growth Areas",
        "careerPath": "Career Path",
        "solarEnergyAnalysis": "Solar Energy Analysis",
        "todaysGuidance": "Today's Guidance"
    },
    'es': {
        "calculatingRisingSign": "Calculando tu signo ascendente...",
        "unableToLoadAscendantData": "No se pudieron cargar los datos del ascendente",
        "completeBirthDataInSettings": "Por favor completa tus datos de nacimiento en Configuración",
        "goBack": "Volver",
        "yourRisingSign": "Tu Signo Ascendente",
        "risingSignAscendant": "Signo Ascendente",
        "aboutYourAscendant": "Acerca de Tu Ascendente",
        "personalityTraits": "Rasgos de Personalidad",
        "physicalPresence": "Presencia Física",
        "firstImpression": "Primera Impresión",
        "yourStrengths": "Tus Fortalezas",
        "growthAreas": "Áreas de Crecimiento",
        "careerPath": "Camino Profesional",
        "solarEnergyAnalysis": "Análisis de Energía Solar",
        "todaysGuidance": "Guía de Hoy"
    },
    'fr': {
        "calculatingRisingSign": "Calcul de votre signe ascendant...",
        "unableToLoadAscendantData": "Impossible de charger les données de l'ascendant",
        "completeBirthDataInSettings": "Veuillez compléter vos données de naissance dans les Paramètres",
        "goBack": "Retour",
        "yourRisingSign": "Votre Signe Ascendant",
        "risingSignAscendant": "Signe Ascendant",
        "aboutYourAscendant": "À propos de votre Ascendant",
        "personalityTraits": "Traits de Personnalité",
        "physicalPresence": "Présence Physique",
        "firstImpression": "Première Impression",
        "yourStrengths": "Vos Forces",
        "growthAreas": "Axes d'Amélioration",
        "careerPath": "Parcours Professionnel",
        "solarEnergyAnalysis": "Analyse de l'Énergie Solaire",
        "todaysGuidance": "Guidance du Jour"
    },
    'it': {
        "calculatingRisingSign": "Calcolo del tuo segno ascendente in corso...",
        "unableToLoadAscendantData": "Impossibile caricare i dati dell'ascendente",
        "completeBirthDataInSettings": "Completa i tuoi dati di nascita nelle Impostazioni",
        "goBack": "Torna Indietro",
        "yourRisingSign": "Il Tuo Segno Ascendente",
        "risingSignAscendant": "Segno Ascendente",
        "aboutYourAscendant": "Riguardo al Tuo Ascendente",
        "personalityTraits": "Tratti della Personalità",
        "physicalPresence": "Presenza Fisica",
        "firstImpression": "Prima Impressione",
        "yourStrengths": "I Tuoi Punti di Forza",
        "growthAreas": "Aree di Crescita",
        "careerPath": "Percorso Professionale",
        "solarEnergyAnalysis": "Analisi dell'Energia Solare",
        "todaysGuidance": "Guida di Oggi"
    },
    'pt': {
        "calculatingRisingSign": "Calculando seu signo ascendente...",
        "unableToLoadAscendantData": "Não foi possível carregar os dados do ascendente",
        "completeBirthDataInSettings": "Por favor, complete seus dados de nascimento nas Configurações",
        "goBack": "Voltar",
        "yourRisingSign": "Seu Signo Ascendente",
        "risingSignAscendant": "Signo Ascendente (Ascendente)",
        "aboutYourAscendant": "Sobre Seu Ascendente",
        "personalityTraits": "Traços de Personalidade",
        "physicalPresence": "Presença Física",
        "firstImpression": "Primeira Impressão",
        "yourStrengths": "Seus Pontos Fortes",
        "growthAreas": "Áreas de Crescimento",
        "careerPath": "Caminho Profissional",
        "solarEnergyAnalysis": "Análise de Energia Solar",
        "todaysGuidance": "Orientação de Hoje"
    },
    'de': {
        "calculatingRisingSign": "Berechne dein aufsteigendes Zeichen...",
        "unableToLoadAscendantData": "Aszendentdaten konnten nicht geladen werden",
        "completeBirthDataInSettings": "Bitte vervollständige deine Geburtsdaten in den Einstellungen",
        "goBack": "Zurück",
        "yourRisingSign": "Dein Aszendent",
        "risingSignAscendant": "Aszendent (Aufsteigendes Zeichen)",
        "aboutYourAscendant": "Über deinen Aszendenten",
        "personalityTraits": "Persönlichkeitsmerkmale",
        "physicalPresence": "Äußere Erscheinung",
        "firstImpression": "Erster Eindruck",
        "yourStrengths": "Deine Stärken",
        "growthAreas": "Wachstumsbereiche",
        "careerPath": "Beruflicher Weg",
        "solarEnergyAnalysis": "Sonnenenergie-Analyse",
        "todaysGuidance": "Heutige Orientierung"
    }
}

base_path = "/Users/alejandrocaceres/Desktop/appstore.zodia/zodiac_app/assets/l10n"

for lang_code, new_translations in translations.items():
    file_path = os.path.join(base_path, f"app_{lang_code}.arb")

    print(f"\n✅ Processing {lang_code.upper()}...")

    # Leer el archivo existente
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse JSON
    data = json.loads(content)

    # Extraer las keys especiales (@@locale y @...)
    special_keys = {}
    regular_keys = {}

    for key, value in data.items():
        if key.startswith('@@') or key.startswith('@'):
            special_keys[key] = value
        else:
            regular_keys[key] = value

    # Agregar las nuevas traducciones a las keys regulares
    for key, value in new_translations.items():
        if key not in regular_keys:
            regular_keys[key] = value
            print(f"  + Added: {key}")
        else:
            print(f"  ⚠️  Skipped (already exists): {key}")

    # Combinar todo: regular keys + special keys al final
    final_data = {**regular_keys, **special_keys}

    # Escribir de vuelta al archivo con formato bonito
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)

    print(f"✅ {lang_code.upper()} updated successfully!")

print("\n🎉 All translations added successfully!")
