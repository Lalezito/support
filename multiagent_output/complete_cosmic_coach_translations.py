#!/usr/bin/env python3
"""
Complete Cosmic Coach Translation Replacement Script
Replaces all MISSING_TRANSLATION values with proper translations
"""

import json
import os

# Comprehensive translation dictionary for ALL missing keys
TRANSLATIONS = {
    "es": {
        # Analytics
        "analyticsCoachSessionsLabel": "Sesiones de Coach",
        "analyticsCosmicCoachFeature": "Coach Cósmico",
        "analyticsGoalsCompleted": "Metas Completadas",
        "analyticsGoalsProgressTitle": "Progreso de Metas",

        # Premium Features
        "advancedCosmicAnalysis": "💎 Análisis Cósmico Avanzado",
        "premiumCosmicAnalysis": "🔒 Análisis Cósmico Premium",

        # Cosmic Periods
        "cosmicBalance": "⚖️ Mantienes un equilibrio admirable. Tu naturaleza {element} está en armonía.",
        "cosmicGrowthPeriod": "Período de Crecimiento Cósmico",
        "cosmicIntrospectionPeriod": "Período de Introspección Cósmica",

        # Goal Management
        "ai_coach_onboarding": "Incorporación del Coach IA",
        "goalDetails": "Detalles de la Meta",
        "goals_empty_state": "Aún no hay metas. ¡Genera algunas abajo!",
        "goal_completed_success": "¡Meta completada exitosamente!",
        "new_goals_generated": "✨ Nuevas metas generadas para {userSign}",
        "smart_goals_generated": "🧠 Metas inteligentes generadas para {userSign}",
        "completeGoalQuestion": "¿Completar Meta?",
        "confirmCompleteGoal": "¿Estás seguro de que quieres marcar esta meta como completada? Esta acción no se puede deshacer.",
        "confirmDeleteGoal": "Esta acción no se puede deshacer. La meta y todo su progreso se eliminarán permanentemente.",
        "deleteGoal": "Eliminar Meta",
        "pauseGoal": "Pausar Meta",

        # Celebration Messages - Adventure
        "celebration_adventure_1": "🗺️ ¡Modo explorador!",
        "celebration_adventure_2": "🌟 ¡Aventura ganada!",
        "celebration_adventure_3": "🏔️ ¡Cumbre alcanzada!",

        # Celebration Messages - Career
        "celebration_career_1": "🚀 ¡Victoria profesional!",
        "celebration_career_2": "💼 ¡Hito profesional!",
        "celebration_career_3": "🏆 ¡Éxito desbloqueado!",

        # Celebration Messages - Creativity
        "celebration_creativity_1": "🎨 ¡Genio creativo!",
        "celebration_creativity_2": "✨ ¡Inspiración fluyendo!",
        "celebration_creativity_3": "🌟 ¡Brillantez artística!",

        # Celebration Messages - Finance
        "celebration_finance_1": "💰 ¡Construyendo riqueza!",
        "celebration_finance_2": "📈 ¡Victoria financiera!",
        "celebration_finance_3": "💎 ¡Maestría del dinero!",

        # Celebration Messages - Fitness
        "celebration_fitness_1": "💪 ¡Aplastándolo!",
        "celebration_fitness_2": "🔥 ¡Modo bestia activado!",
        "celebration_fitness_3": "⚡ ¡Campeón de energía!",

        # Celebration Messages - Growth
        "celebration_growth_1": "🌱 ¡Evolución completa!",
        "celebration_growth_2": "🦋 ¡Transformación!",
        "celebration_growth_3": "✨ ¡Subiste de nivel!",

        # Celebration Messages - Healing
        "celebration_healing_1": "💜 ¡Progreso sanador!",
        "celebration_healing_2": "🌸 ¡Hito de recuperación!",
        "celebration_healing_3": "✨ ¡Plenitud restaurada!",

        # Celebration Messages - Leadership
        "celebration_leadership_1": "👑 ¡Líder emergiendo!",
        "celebration_leadership_2": "⭐ ¡La influencia crece!",
        "celebration_leadership_3": "💫 ¡Inspirando a otros!",

        # Celebration Messages - Learning
        "celebration_learning_1": "📚 ¡Conocimiento ganado!",
        "celebration_learning_2": "🧠 ¡Mente expandida!",
        "celebration_learning_3": "🎓 ¡Sabiduría desbloqueada!",

        # Celebration Messages - Mindfulness
        "celebration_mindfulness_1": "🧘 Paz interior alcanzada",
        "celebration_mindfulness_2": "✨ Nivel maestro zen",
        "celebration_mindfulness_3": "🌸 ¡Tranquilidad dominada!",

        # Celebration Messages - Nature
        "celebration_nature_1": "🌿 ¡Conectado con la tierra!",
        "celebration_nature_2": "🌍 ¡Naturaleza abrazada!",
        "celebration_nature_3": "🏞️ ¡Arraigo logrado!",

        # Celebration Messages - Relationships
        "celebration_relationships_1": "❤️ ¡Conexión profundizada!",
        "celebration_relationships_2": "💕 ¡Amor multiplicado!",
        "celebration_relationships_3": "🤝 ¡Vínculo fortalecido!",

        # Celebration Messages - Service
        "celebration_service_1": "🤝 ¡Impacto logrado!",
        "celebration_service_2": "🌟 ¡La bondad se expande!",
        "celebration_service_3": "💖 ¡Servicio entregado!",

        # Celebration Messages - Wellness
        "celebration_wellness_1": "🌟 ¡Brillando! ¡Estás floreciendo!",
        "celebration_wellness_2": "💚 ¡Rey/Reina del autocuidado!",
        "celebration_wellness_3": "🌈 ¡Guerrero del bienestar!",
    },

    "de": {
        # Analytics
        "analyticsCoachSessionsLabel": "Coach-Sitzungen",
        "analyticsCosmicCoachFeature": "Kosmischer Coach",
        "analyticsGoalsCompleted": "Ziele Erreicht",
        "analyticsGoalsProgressTitle": "Zielfortschritt",

        # Premium Features
        "advancedCosmicAnalysis": "💎 Erweiterte Kosmische Analyse",
        "premiumCosmicAnalysis": "🔒 Premium Kosmische Analyse",

        # Cosmic Periods
        "cosmicBalance": "⚖️ Du bewahrst bewundernswerte Balance. Deine {element} Natur ist in Harmonie.",
        "cosmicGrowthPeriod": "Kosmische Wachstumsperiode",
        "cosmicIntrospectionPeriod": "Kosmische Introspektion",

        # Goal Management
        "ai_coach_onboarding": "KI-Coach Einführung",
        "goalDetails": "Zieldetails",
        "goals_empty_state": "Noch keine Ziele. Generiere welche unten!",
        "goal_completed_success": "Ziel erfolgreich abgeschlossen!",
        "new_goals_generated": "✨ Neue Ziele für {userSign} generiert",
        "smart_goals_generated": "🧠 Smarte Ziele für {userSign} generiert",
        "completeGoalQuestion": "Ziel Abschließen?",
        "confirmCompleteGoal": "Bist du sicher, dass du dieses Ziel als abgeschlossen markieren möchtest? Diese Aktion kann nicht rückgängig gemacht werden.",
        "confirmDeleteGoal": "Diese Aktion kann nicht rückgängig gemacht werden. Das Ziel und sein gesamter Fortschritt werden dauerhaft gelöscht.",
        "deleteGoal": "Ziel Löschen",
        "pauseGoal": "Ziel Pausieren",

        # Celebration Messages - Adventure
        "celebration_adventure_1": "🗺️ Entdecker-Modus!",
        "celebration_adventure_2": "🌟 Abenteuer gewonnen!",
        "celebration_adventure_3": "🏔️ Gipfel erreicht!",

        # Celebration Messages - Career
        "celebration_career_1": "🚀 Karriere-Sieg!",
        "celebration_career_2": "💼 Beruflicher Meilenstein!",
        "celebration_career_3": "🏆 Erfolg freigeschaltet!",

        # Celebration Messages - Creativity
        "celebration_creativity_1": "🎨 Kreatives Genie!",
        "celebration_creativity_2": "✨ Inspiration fließt!",
        "celebration_creativity_3": "🌟 Künstlerische Brillanz!",

        # Celebration Messages - Finance
        "celebration_finance_1": "💰 Vermögensaufbau!",
        "celebration_finance_2": "📈 Finanzieller Sieg!",
        "celebration_finance_3": "💎 Geld-Meisterschaft!",

        # Celebration Messages - Fitness
        "celebration_fitness_1": "💪 Du rockst es!",
        "celebration_fitness_2": "🔥 Bestien-Modus aktiviert!",
        "celebration_fitness_3": "⚡ Energie-Champion!",

        # Celebration Messages - Growth
        "celebration_growth_1": "🌱 Evolution abgeschlossen!",
        "celebration_growth_2": "🦋 Transformation!",
        "celebration_growth_3": "✨ Level aufgestiegen!",

        # Celebration Messages - Healing
        "celebration_healing_1": "💜 Heilungsfortschritt!",
        "celebration_healing_2": "🌸 Erholungs-Meilenstein!",
        "celebration_healing_3": "✨ Ganzheit wiederhergestellt!",

        # Celebration Messages - Leadership
        "celebration_leadership_1": "👑 Anführer im Werden!",
        "celebration_leadership_2": "⭐ Einfluss wächst!",
        "celebration_leadership_3": "💫 Andere inspirieren!",

        # Celebration Messages - Learning
        "celebration_learning_1": "📚 Wissen gewonnen!",
        "celebration_learning_2": "🧠 Geist erweitert!",
        "celebration_learning_3": "🎓 Weisheit freigeschaltet!",

        # Celebration Messages - Mindfulness
        "celebration_mindfulness_1": "🧘 Innerer Frieden erreicht",
        "celebration_mindfulness_2": "✨ Zen-Meister-Level",
        "celebration_mindfulness_3": "🌸 Ruhe gemeistert!",

        # Celebration Messages - Nature
        "celebration_nature_1": "🌿 Mit der Erde verbunden!",
        "celebration_nature_2": "🌍 Natur umarmt!",
        "celebration_nature_3": "🏞️ Erdung erreicht!",

        # Celebration Messages - Relationships
        "celebration_relationships_1": "❤️ Verbindung vertieft!",
        "celebration_relationships_2": "💕 Liebe vervielfacht!",
        "celebration_relationships_3": "🤝 Bindung gestärkt!",

        # Celebration Messages - Service
        "celebration_service_1": "🤝 Wirkung erzielt!",
        "celebration_service_2": "🌟 Freundlichkeit verbreitet!",
        "celebration_service_3": "💖 Dienst geleistet!",

        # Celebration Messages - Wellness
        "celebration_wellness_1": "🌟 Strahlend! Du blühst auf!",
        "celebration_wellness_2": "💚 Selbstfürsorge-König/in!",
        "celebration_wellness_3": "🌈 Wellness-Krieger!",
    },

    "fr": {
        # Analytics
        "analyticsCoachSessionsLabel": "Sessions de Coach",
        "analyticsCosmicCoachFeature": "Coach Cosmique",
        "analyticsGoalsCompleted": "Objectifs Complétés",
        "analyticsGoalsProgressTitle": "Progrès des Objectifs",

        # Premium Features
        "advancedCosmicAnalysis": "💎 Analyse Cosmique Avancée",
        "premiumCosmicAnalysis": "🔒 Analyse Cosmique Premium",

        # Cosmic Periods
        "cosmicBalance": "⚖️ Tu maintiens un équilibre admirable. Ta nature {element} est en harmonie.",
        "cosmicGrowthPeriod": "Période de Croissance Cosmique",
        "cosmicIntrospectionPeriod": "Période d'Introspection Cosmique",

        # Goal Management
        "ai_coach_onboarding": "Intégration du Coach IA",
        "goalDetails": "Détails de l'Objectif",
        "goals_empty_state": "Pas encore d'objectifs. Générez-en ci-dessous !",
        "goal_completed_success": "Objectif complété avec succès !",
        "new_goals_generated": "✨ Nouveaux objectifs générés pour {userSign}",
        "smart_goals_generated": "🧠 Objectifs intelligents générés pour {userSign}",
        "completeGoalQuestion": "Compléter l'Objectif ?",
        "confirmCompleteGoal": "Êtes-vous sûr de vouloir marquer cet objectif comme complété ? Cette action est irréversible.",
        "confirmDeleteGoal": "Cette action est irréversible. L'objectif et toute sa progression seront définitivement supprimés.",
        "deleteGoal": "Supprimer l'Objectif",
        "pauseGoal": "Mettre en Pause",

        # Celebration Messages - Adventure
        "celebration_adventure_1": "🗺️ Mode explorateur !",
        "celebration_adventure_2": "🌟 Aventure gagnée !",
        "celebration_adventure_3": "🏔️ Sommet atteint !",

        # Celebration Messages - Career
        "celebration_career_1": "🚀 Victoire de carrière !",
        "celebration_career_2": "💼 Jalon professionnel !",
        "celebration_career_3": "🏆 Succès débloqué !",

        # Celebration Messages - Creativity
        "celebration_creativity_1": "🎨 Génie créatif !",
        "celebration_creativity_2": "✨ L'inspiration coule !",
        "celebration_creativity_3": "🌟 Brillance artistique !",

        # Celebration Messages - Finance
        "celebration_finance_1": "💰 Bâtir la richesse !",
        "celebration_finance_2": "📈 Victoire financière !",
        "celebration_finance_3": "💎 Maîtrise de l'argent !",

        # Celebration Messages - Fitness
        "celebration_fitness_1": "💪 Tu assures !",
        "celebration_fitness_2": "🔥 Mode bête activé !",
        "celebration_fitness_3": "⚡ Champion d'énergie !",

        # Celebration Messages - Growth
        "celebration_growth_1": "🌱 Évolution complète !",
        "celebration_growth_2": "🦋 Transformation !",
        "celebration_growth_3": "✨ Niveau supérieur !",

        # Celebration Messages - Healing
        "celebration_healing_1": "💜 Progrès de guérison !",
        "celebration_healing_2": "🌸 Jalon de récupération !",
        "celebration_healing_3": "✨ Plénitude restaurée !",

        # Celebration Messages - Leadership
        "celebration_leadership_1": "👑 Leader en devenir !",
        "celebration_leadership_2": "⭐ L'influence grandit !",
        "celebration_leadership_3": "💫 Inspirer les autres !",

        # Celebration Messages - Learning
        "celebration_learning_1": "📚 Connaissance acquise !",
        "celebration_learning_2": "🧠 Esprit élargi !",
        "celebration_learning_3": "🎓 Sagesse déverrouillée !",

        # Celebration Messages - Mindfulness
        "celebration_mindfulness_1": "🧘 Paix intérieure atteinte",
        "celebration_mindfulness_2": "✨ Niveau maître zen",
        "celebration_mindfulness_3": "🌸 Tranquillité maîtrisée !",

        # Celebration Messages - Nature
        "celebration_nature_1": "🌿 Connecté à la terre !",
        "celebration_nature_2": "🌍 Nature embrassée !",
        "celebration_nature_3": "🏞️ Ancrage atteint !",

        # Celebration Messages - Relationships
        "celebration_relationships_1": "❤️ Connexion approfondie !",
        "celebration_relationships_2": "💕 Amour multiplié !",
        "celebration_relationships_3": "🤝 Lien renforcé !",

        # Celebration Messages - Service
        "celebration_service_1": "🤝 Impact réalisé !",
        "celebration_service_2": "🌟 La gentillesse se répand !",
        "celebration_service_3": "💖 Service rendu !",

        # Celebration Messages - Wellness
        "celebration_wellness_1": "🌟 Rayonnant ! Tu t'épanouis !",
        "celebration_wellness_2": "💚 Roi/Reine du soin de soi !",
        "celebration_wellness_3": "🌈 Guerrier du bien-être !",
    },

    "it": {
        # Analytics
        "analyticsCoachSessionsLabel": "Sessioni di Coach",
        "analyticsCosmicCoachFeature": "Coach Cosmico",
        "analyticsGoalsCompleted": "Obiettivi Completati",
        "analyticsGoalsProgressTitle": "Progressi degli Obiettivi",

        # Premium Features
        "advancedCosmicAnalysis": "💎 Analisi Cosmica Avanzata",
        "premiumCosmicAnalysis": "🔒 Analisi Cosmica Premium",

        # Cosmic Periods
        "cosmicBalance": "⚖️ Mantieni un equilibrio ammirevole. La tua natura {element} è in armonia.",
        "cosmicGrowthPeriod": "Periodo di Crescita Cosmica",
        "cosmicIntrospectionPeriod": "Periodo di Introspezione Cosmica",

        # Goal Management
        "ai_coach_onboarding": "Integrazione Coach IA",
        "goalDetails": "Dettagli dell'Obiettivo",
        "goals_empty_state": "Nessun obiettivo ancora. Generane alcuni qui sotto!",
        "goal_completed_success": "Obiettivo completato con successo!",
        "new_goals_generated": "✨ Nuovi obiettivi generati per {userSign}",
        "smart_goals_generated": "🧠 Obiettivi intelligenti generati per {userSign}",
        "completeGoalQuestion": "Completare Obiettivo?",
        "confirmCompleteGoal": "Sei sicuro di voler contrassegnare questo obiettivo come completato? Questa azione non può essere annullata.",
        "confirmDeleteGoal": "Questa azione non può essere annullata. L'obiettivo e tutti i suoi progressi verranno eliminati permanentemente.",
        "deleteGoal": "Elimina Obiettivo",
        "pauseGoal": "Metti in Pausa",

        # Celebration Messages - Adventure
        "celebration_adventure_1": "🗺️ Modalità esploratore!",
        "celebration_adventure_2": "🌟 Avventura vinta!",
        "celebration_adventure_3": "🏔️ Vetta raggiunta!",

        # Celebration Messages - Career
        "celebration_career_1": "🚀 Vittoria di carriera!",
        "celebration_career_2": "💼 Traguardo professionale!",
        "celebration_career_3": "🏆 Successo sbloccato!",

        # Celebration Messages - Creativity
        "celebration_creativity_1": "🎨 Genio creativo!",
        "celebration_creativity_2": "✨ Ispirazione che fluisce!",
        "celebration_creativity_3": "🌟 Brillantezza artistica!",

        # Celebration Messages - Finance
        "celebration_finance_1": "💰 Costruendo ricchezza!",
        "celebration_finance_2": "📈 Vittoria finanziaria!",
        "celebration_finance_3": "💎 Maestria del denaro!",

        # Celebration Messages - Fitness
        "celebration_fitness_1": "💪 Spacchi tutto!",
        "celebration_fitness_2": "🔥 Modalità bestia attivata!",
        "celebration_fitness_3": "⚡ Campione di energia!",

        # Celebration Messages - Growth
        "celebration_growth_1": "🌱 Evoluzione completa!",
        "celebration_growth_2": "🦋 Trasformazione!",
        "celebration_growth_3": "✨ Salito di livello!",

        # Celebration Messages - Healing
        "celebration_healing_1": "💜 Progresso nella guarigione!",
        "celebration_healing_2": "🌸 Traguardo di recupero!",
        "celebration_healing_3": "✨ Pienezza ripristinata!",

        # Celebration Messages - Leadership
        "celebration_leadership_1": "👑 Leader emergente!",
        "celebration_leadership_2": "⭐ L'influenza cresce!",
        "celebration_leadership_3": "💫 Ispirare gli altri!",

        # Celebration Messages - Learning
        "celebration_learning_1": "📚 Conoscenza acquisita!",
        "celebration_learning_2": "🧠 Mente espansa!",
        "celebration_learning_3": "🎓 Saggezza sbloccata!",

        # Celebration Messages - Mindfulness
        "celebration_mindfulness_1": "🧘 Pace interiore raggiunta",
        "celebration_mindfulness_2": "✨ Livello maestro zen",
        "celebration_mindfulness_3": "🌸 Tranquillità padroneggiata!",

        # Celebration Messages - Nature
        "celebration_nature_1": "🌿 Connesso alla terra!",
        "celebration_nature_2": "🌍 Natura abbracciata!",
        "celebration_nature_3": "🏞️ Radicamento raggiunto!",

        # Celebration Messages - Relationships
        "celebration_relationships_1": "❤️ Connessione approfondita!",
        "celebration_relationships_2": "💕 Amore moltiplicato!",
        "celebration_relationships_3": "🤝 Legame rafforzato!",

        # Celebration Messages - Service
        "celebration_service_1": "🤝 Impatto realizzato!",
        "celebration_service_2": "🌟 La gentilezza si diffonde!",
        "celebration_service_3": "💖 Servizio reso!",

        # Celebration Messages - Wellness
        "celebration_wellness_1": "🌟 Splendente! Stai fiorendo!",
        "celebration_wellness_2": "💚 Re/Regina della cura di sé!",
        "celebration_wellness_3": "🌈 Guerriero del benessere!",
    },

    "pt": {
        # Analytics
        "analyticsCoachSessionsLabel": "Sessões de Coach",
        "analyticsCosmicCoachFeature": "Coach Cósmico",
        "analyticsGoalsCompleted": "Metas Concluídas",
        "analyticsGoalsProgressTitle": "Progresso das Metas",

        # Premium Features
        "advancedCosmicAnalysis": "💎 Análise Cósmica Avançada",
        "premiumCosmicAnalysis": "🔒 Análise Cósmica Premium",

        # Cosmic Periods
        "cosmicBalance": "⚖️ Você mantém um equilíbrio admirável. Sua natureza {element} está em harmonia.",
        "cosmicGrowthPeriod": "Período de Crescimento Cósmico",
        "cosmicIntrospectionPeriod": "Período de Introspecção Cósmica",

        # Goal Management
        "ai_coach_onboarding": "Integração do Coach IA",
        "goalDetails": "Detalhes da Meta",
        "goals_empty_state": "Ainda sem metas. Gere algumas abaixo!",
        "goal_completed_success": "Meta concluída com sucesso!",
        "new_goals_generated": "✨ Novas metas geradas para {userSign}",
        "smart_goals_generated": "🧠 Metas inteligentes geradas para {userSign}",
        "completeGoalQuestion": "Concluir Meta?",
        "confirmCompleteGoal": "Tem certeza de que deseja marcar esta meta como concluída? Esta ação não pode ser desfeita.",
        "confirmDeleteGoal": "Esta ação não pode ser desfeita. A meta e todo o seu progresso serão excluídos permanentemente.",
        "deleteGoal": "Excluir Meta",
        "pauseGoal": "Pausar Meta",

        # Celebration Messages - Adventure
        "celebration_adventure_1": "🗺️ Modo explorador!",
        "celebration_adventure_2": "🌟 Aventura vencida!",
        "celebration_adventure_3": "🏔️ Topo alcançado!",

        # Celebration Messages - Career
        "celebration_career_1": "🚀 Vitória na carreira!",
        "celebration_career_2": "💼 Marco profissional!",
        "celebration_career_3": "🏆 Sucesso desbloqueado!",

        # Celebration Messages - Creativity
        "celebration_creativity_1": "🎨 Gênio criativo!",
        "celebration_creativity_2": "✨ Inspiração fluindo!",
        "celebration_creativity_3": "🌟 Brilho artístico!",

        # Celebration Messages - Finance
        "celebration_finance_1": "💰 Construindo riqueza!",
        "celebration_finance_2": "📈 Vitória financeira!",
        "celebration_finance_3": "💎 Maestria do dinheiro!",

        # Celebration Messages - Fitness
        "celebration_fitness_1": "💪 Arrasando!",
        "celebration_fitness_2": "🔥 Modo fera ativado!",
        "celebration_fitness_3": "⚡ Campeão de energia!",

        # Celebration Messages - Growth
        "celebration_growth_1": "🌱 Evolução completa!",
        "celebration_growth_2": "🦋 Transformação!",
        "celebration_growth_3": "✨ Subiu de nível!",

        # Celebration Messages - Healing
        "celebration_healing_1": "💜 Progresso na cura!",
        "celebration_healing_2": "🌸 Marco de recuperação!",
        "celebration_healing_3": "✨ Plenitude restaurada!",

        # Celebration Messages - Leadership
        "celebration_leadership_1": "👑 Líder emergente!",
        "celebration_leadership_2": "⭐ Influência crescendo!",
        "celebration_leadership_3": "💫 Inspirando outros!",

        # Celebration Messages - Learning
        "celebration_learning_1": "📚 Conhecimento adquirido!",
        "celebration_learning_2": "🧠 Mente expandida!",
        "celebration_learning_3": "🎓 Sabedoria desbloqueada!",

        # Celebration Messages - Mindfulness
        "celebration_mindfulness_1": "🧘 Paz interior alcançada",
        "celebration_mindfulness_2": "✨ Nível mestre zen",
        "celebration_mindfulness_3": "🌸 Tranquilidade dominada!",

        # Celebration Messages - Nature
        "celebration_nature_1": "🌿 Conectado à terra!",
        "celebration_nature_2": "🌍 Natureza abraçada!",
        "celebration_nature_3": "🏞️ Enraizamento alcançado!",

        # Celebration Messages - Relationships
        "celebration_relationships_1": "❤️ Conexão aprofundada!",
        "celebration_relationships_2": "💕 Amor multiplicado!",
        "celebration_relationships_3": "🤝 Vínculo fortalecido!",

        # Celebration Messages - Service
        "celebration_service_1": "🤝 Impacto realizado!",
        "celebration_service_2": "🌟 A bondade se espalha!",
        "celebration_service_3": "💖 Serviço prestado!",

        # Celebration Messages - Wellness
        "celebration_wellness_1": "🌟 Brilhando! Você está florescendo!",
        "celebration_wellness_2": "💚 Rei/Rainha do autocuidado!",
        "celebration_wellness_3": "🌈 Guerreiro do bem-estar!",
    }
}


def replace_missing_translations(lang_code, translations):
    """Replace MISSING_TRANSLATION values in cosmic_coach ARB file"""

    input_path = f'/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output/features/cosmic_coach/cosmic_coach_{lang_code}.arb'

    # Read the current ARB file
    with open(input_path, 'r', encoding='utf-8') as f:
        arb_data = json.load(f)

    replacements = 0

    # Replace MISSING_TRANSLATION values
    for key, value in arb_data.items():
        if not key.startswith('@'):  # Skip metadata keys
            if value == "MISSING_TRANSLATION" and key in translations:
                arb_data[key] = translations[key]
                replacements += 1

    # Write the updated ARB file
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(arb_data, f, indent=2, ensure_ascii=False)

    return replacements


def verify_no_missing_translations(lang_code):
    """Verify that no MISSING_TRANSLATION strings remain"""

    input_path = f'/Users/alejandrocaceres/Desktop/appstore.zodia/multiagent_output/features/cosmic_coach/cosmic_coach_{lang_code}.arb'

    with open(input_path, 'r', encoding='utf-8') as f:
        arb_data = json.load(f)

    missing_count = 0
    missing_keys = []

    for key, value in arb_data.items():
        if not key.startswith('@') and value == "MISSING_TRANSLATION":
            missing_count += 1
            missing_keys.append(key)

    return missing_count, missing_keys


def main():
    """Main execution function"""

    print("=" * 80)
    print("COSMIC COACH TRANSLATION REPLACEMENT")
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
    results = {}

    # Process each language
    for lang in languages:
        print(f"\n📝 Processing {language_names[lang]} ({lang})...")
        replacements = replace_missing_translations(lang, TRANSLATIONS[lang])
        total_replacements += replacements

        # Verify
        missing_count, missing_keys = verify_no_missing_translations(lang)

        results[lang] = {
            'replacements': replacements,
            'missing_count': missing_count,
            'missing_keys': missing_keys
        }

        print(f"   ✅ Replaced {replacements} translations")
        if missing_count == 0:
            print(f"   ✅ NO MISSING_TRANSLATION values remain!")
        else:
            print(f"   ⚠️  WARNING: {missing_count} MISSING_TRANSLATION values still remain")
            print(f"   Missing keys: {', '.join(missing_keys[:5])}")

    # Summary Report
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)

    for lang in languages:
        print(f"\n{language_names[lang]} ({lang}):")
        print(f"  - Translations replaced: {results[lang]['replacements']}")
        print(f"  - Remaining MISSING_TRANSLATION: {results[lang]['missing_count']}")
        if results[lang]['missing_count'] == 0:
            print(f"  - Status: ✅ COMPLETE")
        else:
            print(f"  - Status: ⚠️  INCOMPLETE")

    print(f"\n📊 Total translations replaced: {total_replacements}")

    # Sample translations
    print("\n" + "=" * 80)
    print("SAMPLE TRANSLATIONS (5 examples)")
    print("=" * 80)

    sample_keys = [
        "celebration_wellness_1",
        "smart_goals_generated",
        "confirmCompleteGoal",
        "celebration_adventure_3",
        "analyticsCosmicCoachFeature"
    ]

    for key in sample_keys:
        print(f"\n🔑 {key}:")
        print(f"   EN: {TRANSLATIONS['es'].get(key, 'N/A')}")  # Using ES as reference to show it exists
        for lang in languages:
            print(f"   {lang.upper()}: {TRANSLATIONS[lang].get(key, 'N/A')}")

    print("\n" + "=" * 80)
    print("✨ Translation replacement complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
