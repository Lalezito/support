/// 📚 EJEMPLOS DE USO - COSMIC COACH BACKEND SERVICES
/// ====================================================
/// Guía rápida de cómo usar los servicios implementados por el Agente 1

import 'package:zodiac_app/services/preferences_service.dart';
import 'package:zodiac_app/services/conversation_history_service.dart';
import 'package:zodiac_app/services/chat_cache_service.dart';
import 'package:zodiac_app/services/favorite_message_service.dart';
import 'package:zodiac_app/models/conversation_history.dart';
import 'package:zodiac_app/models/favorite_message.dart';
import 'package:zodiac_app/models/chat_models.dart';
import 'package:zodiac_app/models/horoscope_chat_models.dart';

// ============================================================================
// EJEMPLO 1: PREFERENCES SERVICE - CONFIGURACIÓN DE COSMIC COACH
// ============================================================================

Future<void> examplePreferencesService() async {
  final prefs = PreferencesService.instance;
  await prefs.initialize();

  // 1️⃣ OBTENER CONFIGURACIÓN ACTUAL
  final chatMode = await prefs.getChatMode(); // 'quick' | 'balanced' | 'detailed'
  final personality = await prefs.getCoachPersonality(); // 'professional' | 'friendly' | 'mystical'
  final showQuickReplies = await prefs.getShowQuickReplies();
  final autoSave = await prefs.getAutoSaveConversations();
  final preferBackend = await prefs.getPreferBackend(); // Premium only
  final dailyLimit = await prefs.getDailyMessageLimit();

  print('Modo de chat: $chatMode');
  print('Personalidad: $personality');
  print('Límite diario: $dailyLimit mensajes');

  // 2️⃣ CAMBIAR CONFIGURACIÓN
  // Usuario premium quiere respuestas detalladas con personalidad mística
  if (prefs.isPremium) {
    await prefs.setChatMode('detailed');
    await prefs.setCoachPersonality('mystical');
    await prefs.setDailyMessageLimit(500); // Premium gets more messages
    await prefs.setPreferBackend(true); // Use advanced AI backend
  }

  // 3️⃣ CONFIGURACIÓN PARA FREE USER
  // Usuario free quiere respuestas rápidas
  if (!prefs.isPremium) {
    await prefs.setChatMode('quick');
    await prefs.setCoachPersonality('friendly');
    await prefs.setDailyMessageLimit(50); // Free limit
    await prefs.setShowQuickReplies(true); // Help with suggestions
  }
}

// ============================================================================
// EJEMPLO 2: CONVERSATION HISTORY SERVICE - GESTIÓN DE CONVERSACIONES
// ============================================================================

Future<void> exampleConversationHistoryService() async {
  final service = ConversationHistoryService.instance;
  await service.initialize();

  // 1️⃣ CREAR NUEVA CONVERSACIÓN
  final messages = <ChatMessage>[
    ChatMessage(
      id: 'msg_1',
      type: MessageType.user,
      content: '¿Qué me depara el día de hoy?',
      timestamp: DateTime.now(),
    ),
    ChatMessage(
      id: 'msg_2',
      type: MessageType.ai,
      content: 'Hoy es un día perfecto para nuevos comienzos...',
      timestamp: DateTime.now(),
      aiPersonality: 'mystical',
    ),
  ];

  final conversation = ConversationHistory(
    id: 'conv_${DateTime.now().millisecondsSinceEpoch}',
    title: ConversationHistory.generateAutoTitle(messages, 'es'),
    messages: messages,
    createdAt: DateTime.now(),
    lastModified: DateTime.now(),
    category: 'daily',
    tags: ['horóscopo', 'guía diaria'],
  );

  // 2️⃣ GUARDAR CONVERSACIÓN
  await service.saveConversation(conversation);

  // 3️⃣ AGREGAR MENSAJE A CONVERSACIÓN EXISTENTE
  final newMessage = ChatMessage(
    id: 'msg_3',
    type: MessageType.user,
    content: '¿Y qué hay del amor?',
    timestamp: DateTime.now(),
  );
  await service.addMessageToConversation(conversation.id, newMessage);

  // 4️⃣ OBTENER TODAS LAS CONVERSACIONES
  final allConversations = await service.getAllConversations();
  print('Total de conversaciones: ${allConversations.length}');

  // 5️⃣ BUSCAR CONVERSACIONES POR CATEGORÍA
  final dailyConversations = await service.getConversationsByCategory('daily');
  final loveConversations = await service.getConversationsByCategory('love');

  // 6️⃣ BUSCAR CONVERSACIONES POR TEXTO
  final searchResults = await service.searchConversations('amor');
  print('Encontradas ${searchResults.length} conversaciones sobre amor');

  // 7️⃣ EXPORTAR CONVERSACIÓN A TEXTO
  final textExport = service.exportConversationToText(conversation, 'es');
  // Ahora puedes compartir o guardar este texto

  // 8️⃣ OBTENER ESTADÍSTICAS
  final stats = await service.getStats();
  print('Total de conversaciones: ${stats.totalConversations}');
  print('Total de mensajes: ${stats.totalMessages}');
  print('Duración total: ${stats.totalDuration}');

  // 9️⃣ LIMPIAR CONVERSACIONES ANTIGUAS (más de 90 días)
  await service.deleteOldConversations(daysOld: 90);

  // 🔟 ELIMINAR CONVERSACIÓN ESPECÍFICA
  await service.deleteConversation(conversation.id);
}

// ============================================================================
// EJEMPLO 3: CHAT CACHE SERVICE - GESTIÓN DE CACHE
// ============================================================================

Future<void> exampleChatCacheService() async {
  final service = ChatCacheService.instance;
  await service.initialize();

  // 1️⃣ OBTENER ESTADÍSTICAS DE CACHE
  final stats = await service.getCacheStats();
  print('Tamaño del cache: ${stats.sizeInMB.toStringAsFixed(2)} MB');
  print('Conversaciones: ${stats.conversationCount}');
  print('Favoritos: ${stats.favoriteCount}');
  print('Total items: ${stats.totalItems}');

  // 2️⃣ VERIFICAR SI ESTÁ CERCA DEL LÍMITE
  final usagePercentage = await service.getCacheUsagePercentage();
  if (usagePercentage > 80) {
    print('⚠️ Cache al $usagePercentage% - considera limpiar');
  }

  // 3️⃣ LIMPIAR CACHE AUTOMÁTICAMENTE SI EXCEDE LÍMITE
  if (await service.isCacheSizeLimitExceeded()) {
    final result = await service.optimizeCache();
    print('Optimización: ${result.wasOptimized}');
    print('Items eliminados: ${result.itemsDeleted}');
    print('Espacio liberado: ${result.mbFreed.toStringAsFixed(2)} MB');
  }

  // 4️⃣ LIMPIAR CACHE MANUALMENTE
  // Limpiar conversaciones de más de 30 días
  final deletedCount = await service.clearOldCache(daysToKeep: 30);
  print('Eliminadas $deletedCount conversaciones antiguas');

  // 5️⃣ LIMPIAR TODO EL CACHE (nuclear option)
  // await service.clearAllCache();

  // 6️⃣ LIMPIAR SOLO CONVERSACIONES (mantener favoritos)
  // await service.clearConversationsCache();

  // 7️⃣ HEALTH CHECK
  final health = service.getHealthStatus();
  print('Estado del cache: ${health['status']}');
}

// ============================================================================
// EJEMPLO 4: FAVORITE MESSAGE SERVICE - GESTIÓN DE FAVORITOS
// ============================================================================

Future<void> exampleFavoriteMessageService() async {
  final service = FavoriteMessageService.instance;
  await service.initialize();

  // 1️⃣ CREAR MENSAJE FAVORITO
  final message = ChatMessage(
    id: 'msg_cosmic_1',
    type: MessageType.ai,
    content: 'Tu energía está alineada con Venus, este es tu momento para el amor.',
    timestamp: DateTime.now(),
    aiPersonality: 'mystical',
  );

  // 2️⃣ AGREGAR A FAVORITOS CON CATEGORÍA
  final favorite = await service.addFavorite(
    message,
    category: HoroscopeQuestionCategory.loveCompatibility,
    userNote: 'Me encantó esta predicción sobre el amor',
    tags: ['amor', 'venus', 'inspirador'],
  );

  print('Favorito agregado: ${favorite.id}');

  // 3️⃣ VERIFICAR SI UN MENSAJE ES FAVORITO
  final isFav = service.isFavorite(message.id);
  print('¿Es favorito? $isFav');

  // 4️⃣ TOGGLE FAVORITO (add si no existe, remove si existe)
  final nowIsFavorite = await service.toggleFavorite(
    message,
    category: HoroscopeQuestionCategory.dailyGuidance,
  );
  print('Estado del favorito: $nowIsFavorite');

  // 5️⃣ OBTENER TODOS LOS FAVORITOS
  final allFavorites = await service.getAllFavorites();
  print('Total de favoritos: ${allFavorites.length}');

  // 6️⃣ FILTRAR POR CATEGORÍA
  final loveFavorites = await service.getFavoritesByCategory(
    HoroscopeQuestionCategory.loveCompatibility
  );
  final careerFavorites = await service.getFavoritesByCategory(
    HoroscopeQuestionCategory.careerTiming
  );

  // 7️⃣ BUSCAR POR TAG
  final venusRelated = await service.getFavoritesByTag('venus');
  final inspiringMessages = await service.getFavoritesByTag('inspirador');

  // 8️⃣ BUSCAR POR TEXTO (en contenido y notas)
  final searchResults = await service.searchFavorites('amor');
  print('Encontrados ${searchResults.length} favoritos sobre amor');

  // 9️⃣ AGREGAR NOTA A FAVORITO EXISTENTE
  await service.addNoteToFavorite(
    favorite.id,
    'Esta predicción se cumplió! 💕'
  );

  // 🔟 AGREGAR TAG A FAVORITO
  await service.addTagToFavorite(favorite.id, 'cumplido');
  await service.addTagToFavorite(favorite.id, 'preciso');

  // 1️⃣1️⃣ OBTENER ESTADÍSTICAS DE FAVORITOS
  final stats = await service.getStats();
  print('Total de favoritos: ${stats.totalFavorites}');
  print('Categoría más popular: ${stats.mostPopularCategory?.name}');

  // 1️⃣2️⃣ OBTENER CATEGORÍAS ÚNICAS
  final categories = service.uniqueCategories;
  print('Categorías usadas: ${categories.length}');

  // 1️⃣3️⃣ OBTENER TODOS LOS TAGS
  final allTags = service.uniqueTags;
  print('Tags únicos: $allTags');

  // 1️⃣4️⃣ OBTENER BREAKDOWN POR CATEGORÍA
  final breakdown = service.categoryBreakdown;
  breakdown.forEach((category, count) {
    print('$category: $count favoritos');
  });

  // 1️⃣5️⃣ EXPORTAR FAVORITOS A TEXTO
  final textExport = await service.exportFavoritesToText('es');
  // Compartir o guardar el texto exportado

  // 1️⃣6️⃣ ELIMINAR FAVORITO
  await service.removeFavorite(favorite.id);

  // 1️⃣7️⃣ ELIMINAR POR MESSAGE ID
  await service.removeFavoriteByMessageId(message.id);

  // 1️⃣8️⃣ ELIMINAR TODOS LOS FAVORITOS DE UNA CATEGORÍA
  final deletedCount = await service.removeFavoritesByCategory(
    HoroscopeQuestionCategory.dailyGuidance
  );
  print('Eliminados $deletedCount favoritos de guía diaria');
}

// ============================================================================
// EJEMPLO 5: FLUJO COMPLETO - CONVERSACIÓN CON FAVORITOS Y CACHE
// ============================================================================

Future<void> exampleCompleteFlow() async {
  // Inicializar todos los servicios
  final prefs = PreferencesService.instance;
  final conversations = ConversationHistoryService.instance;
  final favorites = FavoriteMessageService.instance;
  final cache = ChatCacheService.instance;

  await Future.wait([
    prefs.initialize(),
    conversations.initialize(),
    favorites.initialize(),
    cache.initialize(),
  ]);

  // 1️⃣ CONFIGURAR PREFERENCIAS DEL USUARIO
  await prefs.setChatMode('balanced');
  await prefs.setCoachPersonality('friendly');
  await prefs.setAutoSaveConversations(true);

  // 2️⃣ CREAR CONVERSACIÓN
  final messages = <ChatMessage>[
    ChatMessage(
      id: 'msg_1',
      type: MessageType.user,
      content: '¿Qué predicciones tienes para mí hoy?',
      timestamp: DateTime.now(),
    ),
    ChatMessage(
      id: 'msg_2',
      type: MessageType.ai,
      content: 'Hoy es un día especial para ti. Las estrellas están alineadas...',
      timestamp: DateTime.now(),
      aiPersonality: 'friendly',
    ),
  ];

  final conversation = ConversationHistory(
    id: 'conv_${DateTime.now().millisecondsSinceEpoch}',
    title: ConversationHistory.generateAutoTitle(messages, 'es'),
    messages: messages,
    createdAt: DateTime.now(),
    lastModified: DateTime.now(),
    category: 'daily',
    tags: ['predicción', 'guía diaria'],
  );

  // 3️⃣ GUARDAR CONVERSACIÓN (auto-save está activado)
  final autoSaveEnabled = await prefs.getAutoSaveConversations();
  if (autoSaveEnabled) {
    await conversations.saveConversation(conversation);
  }

  // 4️⃣ MARCAR MENSAJE COMO FAVORITO
  final aiMessage = messages[1];
  await favorites.addFavorite(
    aiMessage,
    category: HoroscopeQuestionCategory.dailyGuidance,
    userNote: 'Gran predicción!',
    tags: ['inspirador'],
  );

  // 5️⃣ VERIFICAR ESTADO DEL CACHE
  final cacheStats = await cache.getCacheStats();
  if (await cache.isCacheSizeLimitExceeded()) {
    print('⚠️ Cache lleno, optimizando...');
    await cache.optimizeCache();
  }

  // 6️⃣ OBTENER RESUMEN DE TODO
  final conversationStats = await conversations.getStats();
  final favoriteStats = await favorites.getStats();

  print('═' * 50);
  print('RESUMEN DE COSMIC COACH');
  print('═' * 50);
  print('Conversaciones: ${conversationStats.totalConversations}');
  print('Mensajes totales: ${conversationStats.totalMessages}');
  print('Favoritos: ${favoriteStats.totalFavorites}');
  print('Cache usado: ${cacheStats.sizeInMB.toStringAsFixed(2)} MB');
  print('═' * 50);
}

// ============================================================================
// EJEMPLO 6: SETTINGS SCREEN - INTEGRACIÓN UI
// ============================================================================

Future<void> exampleSettingsScreen() async {
  final prefs = PreferencesService.instance;
  await prefs.initialize();

  // OBTENER VALORES ACTUALES PARA MOSTRAR EN UI
  final currentMode = await prefs.getChatMode();
  final currentPersonality = await prefs.getCoachPersonality();
  final showQuickReplies = await prefs.getShowQuickReplies();
  final autoSave = await prefs.getAutoSaveConversations();

  // CUANDO EL USUARIO CAMBIA UN SETTING
  // Ejemplo: DropdownButton onChange
  void onChatModeChanged(String newMode) async {
    await prefs.setChatMode(newMode);
    // UI se actualizará automáticamente si usas Provider/ChangeNotifierProvider
  }

  void onPersonalityChanged(String newPersonality) async {
    await prefs.setCoachPersonality(newPersonality);
  }

  void onQuickRepliesToggle(bool value) async {
    await prefs.setShowQuickReplies(value);
  }

  void onAutoSaveToggle(bool value) async {
    await prefs.setAutoSaveConversations(value);
  }

  // PREMIUM FEATURES
  if (prefs.isPremium) {
    void onPreferBackendToggle(bool value) async {
      await prefs.setPreferBackend(value);
    }

    void onDailyLimitChanged(int limit) async {
      await prefs.setDailyMessageLimit(limit);
    }
  }
}

// ============================================================================
// MAIN - EJECUTAR TODOS LOS EJEMPLOS
// ============================================================================

void main() async {
  print('🚀 COSMIC COACH BACKEND SERVICES - EJEMPLOS DE USO\n');

  // Ejecutar ejemplos
  await examplePreferencesService();
  await exampleConversationHistoryService();
  await exampleChatCacheService();
  await exampleFavoriteMessageService();
  await exampleCompleteFlow();

  print('\n✅ Todos los ejemplos ejecutados correctamente!');
}
