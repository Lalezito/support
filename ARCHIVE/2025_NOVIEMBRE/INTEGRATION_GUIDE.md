# 🔧 Cosmic Coach Integration Guide
## Complete System Integration Playbook

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [System Dependencies](#system-dependencies)
3. [Integration Points](#integration-points)
4. [Service Communication](#service-communication)
5. [Data Flow Integration](#data-flow-integration)
6. [API Integration](#api-integration)
7. [Event-Driven Integration](#event-driven-integration)
8. [Testing Integration](#testing-integration)
9. [Deployment Integration](#deployment-integration)
10. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 30-Minute Setup Guide

```bash
# 1. Clone the repository
git clone https://github.com/cosmiccoach/platform.git
cd platform

# 2. Install dependencies
make install-all

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Start infrastructure
docker-compose up -d

# 5. Initialize databases
make db-migrate

# 6. Start services
make start-services

# 7. Verify health
make health-check
```

---

## System Dependencies

### Service Dependency Matrix

```javascript
const serviceDependencies = {
  'prediction-engine': {
    required: ['database', 'cache', 'openai-api'],
    optional: ['analytics', 'notification'],
    healthCheck: async () => {
      return await checkServices(['database', 'cache', 'openai-api']);
    }
  },

  'compatibility-system': {
    required: ['database', 'ml-models', 'cache'],
    optional: ['analytics', 'image-generation'],
    healthCheck: async () => {
      return await checkServices(['database', 'ml-models']);
    }
  },

  'voice-ai': {
    required: ['elevenlabs-api', 'storage'],
    optional: ['cache', 'analytics'],
    healthCheck: async () => {
      return await checkServices(['elevenlabs-api', 'storage']);
    }
  },

  'image-generation': {
    required: ['dalle-api', 'storage'],
    optional: ['cache', 'analytics'],
    healthCheck: async () => {
      return await checkServices(['dalle-api', 'storage']);
    }
  },

  'analytics-engine': {
    required: ['database', 'bigquery'],
    optional: ['cache'],
    healthCheck: async () => {
      return await checkServices(['database', 'bigquery']);
    }
  },

  'notification-engine': {
    required: ['firebase', 'database', 'queue'],
    optional: ['sendgrid', 'analytics'],
    healthCheck: async () => {
      return await checkServices(['firebase', 'database']);
    }
  },

  'ab-testing': {
    required: ['database', 'cache', 'analytics'],
    optional: [],
    healthCheck: async () => {
      return await checkServices(['database', 'cache']);
    }
  },

  'revenue-optimizer': {
    required: ['stripe', 'database', 'ml-models'],
    optional: ['analytics', 'cache'],
    healthCheck: async () => {
      return await checkServices(['stripe', 'database']);
    }
  }
};
```

### Installation Order

```bash
# Phase 1: Infrastructure (Required First)
1. PostgreSQL Database
2. MongoDB
3. Redis Cache
4. Message Queue (Kafka/RabbitMQ)

# Phase 2: Core Services
5. Authentication Service
6. Prediction Engine
7. Analytics Engine

# Phase 3: Feature Services
8. Compatibility System
9. Voice AI Service
10. Image Generation Service

# Phase 4: Business Intelligence
11. Notification Engine
12. A/B Testing Framework
13. Revenue Optimizer

# Phase 5: Gateway & Orchestration
14. API Gateway
15. Master Orchestrator
```

---

## Integration Points

### 1. Prediction Engine Integration

```javascript
// prediction-integration.js
class PredictionIntegration {
  constructor() {
    this.prediction = new PredictionEngine();
    this.cache = new CacheService();
    this.analytics = new AnalyticsService();
    this.notification = new NotificationService();
  }

  async generateDailyPrediction(userId) {
    try {
      // 1. Check cache first
      const cacheKey = `prediction:${userId}:${getCurrentDate()}`;
      const cached = await this.cache.get(cacheKey);
      if (cached) return cached;

      // 2. Get user profile
      const userProfile = await getUserProfile(userId);

      // 3. Generate prediction
      const prediction = await this.prediction.generate({
        userId,
        zodiacSign: userProfile.zodiacSign,
        birthChart: userProfile.birthChart,
        preferences: userProfile.preferences
      });

      // 4. Enhance with additional features
      if (userProfile.isPremium) {
        prediction.voice = await this.generateVoice(prediction.text);
        prediction.image = await this.generateImage(prediction.theme);
      }

      // 5. Cache the result
      await this.cache.set(cacheKey, prediction, 86400);

      // 6. Track analytics
      await this.analytics.track('prediction_generated', {
        userId,
        type: 'daily',
        isPremium: userProfile.isPremium
      });

      // 7. Schedule follow-up notification
      await this.notification.schedule({
        userId,
        type: 'prediction_reminder',
        scheduledFor: getOptimalReminderTime(userId),
        content: prediction.keyInsight
      });

      return prediction;

    } catch (error) {
      logger.error('Prediction generation failed', { userId, error });
      throw new IntegrationError('Failed to generate prediction', error);
    }
  }
}
```

### 2. Compatibility System Integration

```javascript
// compatibility-integration.js
class CompatibilityIntegration {
  constructor() {
    this.compatibility = new CompatibilityEngine();
    this.ml = new MLService();
    this.cache = new CacheService();
  }

  async analyzeCompatibility(user1Id, user2Id) {
    // 1. Load user profiles
    const [user1, user2] = await Promise.all([
      getUserProfile(user1Id),
      getUserProfile(user2Id)
    ]);

    // 2. Check cache
    const cacheKey = `compatibility:${user1Id}:${user2Id}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) return cached;

    // 3. Run neural network analysis
    const analysis = await this.ml.runModel('compatibility_v2', {
      user1Features: this.extractFeatures(user1),
      user2Features: this.extractFeatures(user2)
    });

    // 4. Generate detailed report
    const report = await this.compatibility.generateReport({
      users: [user1, user2],
      analysis,
      includeRecommendations: true
    });

    // 5. Add visualizations
    report.chartUrl = await this.generateCompatibilityChart(analysis);

    // 6. Cache for 7 days
    await this.cache.set(cacheKey, report, 604800);

    // 7. Track event
    await this.analytics.track('compatibility_analyzed', {
      user1Id,
      user2Id,
      score: analysis.overallScore
    });

    return report;
  }

  extractFeatures(userProfile) {
    return {
      zodiacSign: userProfile.zodiacSign,
      elements: userProfile.elements,
      modalities: userProfile.modalities,
      personality: userProfile.personalityTraits,
      preferences: userProfile.relationshipPreferences
    };
  }
}
```

### 3. Voice AI Integration

```javascript
// voice-integration.js
class VoiceIntegration {
  constructor() {
    this.elevenLabs = new ElevenLabsClient(process.env.ELEVENLABS_API_KEY);
    this.storage = new S3Client();
    this.cache = new CacheService();
  }

  async generateVoice(text, options = {}) {
    // 1. Check cache
    const cacheKey = `voice:${hashText(text)}:${options.voiceId || 'default'}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) return cached;

    // 2. Select voice based on user preferences
    const voiceId = options.voiceId || await this.selectVoice(options.userId);

    // 3. Generate audio
    const audioBuffer = await this.elevenLabs.generate({
      text,
      voiceId,
      modelId: 'eleven_multilingual_v2',
      voiceSettings: {
        stability: 0.75,
        similarityBoost: 0.75,
        style: options.style || 'calm'
      }
    });

    // 4. Upload to storage
    const key = `voice/${Date.now()}_${cacheKey}.mp3`;
    const url = await this.storage.upload(key, audioBuffer, {
      contentType: 'audio/mpeg',
      metadata: {
        text: text.substring(0, 100),
        voiceId,
        generatedAt: new Date().toISOString()
      }
    });

    // 5. Cache URL
    await this.cache.set(cacheKey, url, 2592000); // 30 days

    // 6. Track usage
    await this.analytics.track('voice_generated', {
      userId: options.userId,
      textLength: text.length,
      voiceId
    });

    return url;
  }

  async selectVoice(userId) {
    const preferences = await getUserPreferences(userId);
    const voiceMap = {
      'male_calm': 'adam',
      'female_warm': 'bella',
      'male_energetic': 'josh',
      'female_professional': 'rachel'
    };
    return voiceMap[preferences.voiceType] || 'bella';
  }
}
```

### 4. Image Generation Integration

```javascript
// image-integration.js
class ImageIntegration {
  constructor() {
    this.dalle = new OpenAIClient();
    this.storage = new S3Client();
    this.cache = new CacheService();
  }

  async generateDailyImage(userId, theme) {
    try {
      // 1. Get user preferences
      const userProfile = await getUserProfile(userId);

      // 2. Create optimized prompt
      const prompt = this.createPrompt({
        theme,
        zodiacSign: userProfile.zodiacSign,
        style: userProfile.imageStyle || 'mystical',
        colors: userProfile.preferredColors
      });

      // 3. Check cache
      const cacheKey = `image:${hashText(prompt)}`;
      const cached = await this.cache.get(cacheKey);
      if (cached) return cached;

      // 4. Generate image
      const response = await this.dalle.createImage({
        prompt,
        n: 1,
        size: '1024x1024',
        quality: 'standard',
        style: 'vivid'
      });

      // 5. Process and optimize
      const imageBuffer = await this.downloadAndOptimize(response.data[0].url);

      // 6. Upload to storage
      const key = `images/daily/${userId}/${Date.now()}.webp`;
      const url = await this.storage.upload(key, imageBuffer);

      // 7. Create thumbnails
      const thumbnails = await this.createThumbnails(imageBuffer);

      const result = {
        url,
        thumbnails,
        prompt: prompt.substring(0, 100),
        generatedAt: new Date().toISOString()
      };

      // 8. Cache for 7 days
      await this.cache.set(cacheKey, result, 604800);

      return result;

    } catch (error) {
      logger.error('Image generation failed', { userId, error });
      // Return fallback image
      return this.getFallbackImage(theme);
    }
  }

  createPrompt({ theme, zodiacSign, style, colors }) {
    const basePrompt = `A ${style} representation of ${theme} for ${zodiacSign}`;
    const colorString = colors ? `, featuring ${colors.join(' and ')} colors` : '';
    const styleModifiers = ', digital art, highly detailed, ethereal, cosmic';

    return `${basePrompt}${colorString}${styleModifiers}`;
  }
}
```

---

## Service Communication

### Message Queue Integration

```javascript
// message-queue-integration.js
class MessageQueueIntegration {
  constructor() {
    this.kafka = new KafkaClient({
      brokers: ['kafka1:9092', 'kafka2:9092'],
      clientId: 'cosmic-coach'
    });

    this.topics = {
      USER_EVENTS: 'user-events',
      PREDICTIONS: 'predictions',
      COMPATIBILITY: 'compatibility',
      NOTIFICATIONS: 'notifications',
      ANALYTICS: 'analytics',
      REVENUE: 'revenue'
    };
  }

  async publishEvent(topic, event) {
    const message = {
      id: generateId(),
      timestamp: Date.now(),
      type: event.type,
      data: event.data,
      metadata: {
        service: process.env.SERVICE_NAME,
        version: process.env.SERVICE_VERSION
      }
    };

    await this.kafka.producer.send({
      topic,
      messages: [{
        key: event.key || message.id,
        value: JSON.stringify(message)
      }]
    });

    logger.info('Event published', { topic, messageId: message.id });
  }

  async subscribeToEvents(topics, handler) {
    const consumer = this.kafka.consumer({
      groupId: `${process.env.SERVICE_NAME}-consumer`
    });

    await consumer.connect();

    for (const topic of topics) {
      await consumer.subscribe({ topic, fromBeginning: false });
    }

    await consumer.run({
      eachMessage: async ({ topic, partition, message }) => {
        try {
          const event = JSON.parse(message.value.toString());
          await handler(topic, event);

          // Track processing
          metrics.increment(`events.processed.${topic}`);
        } catch (error) {
          logger.error('Event processing failed', { topic, error });
          metrics.increment(`events.failed.${topic}`);
        }
      }
    });
  }
}

// Usage Example
const mq = new MessageQueueIntegration();

// Publish prediction generated event
await mq.publishEvent(mq.topics.PREDICTIONS, {
  type: 'prediction.generated',
  key: userId,
  data: {
    userId,
    predictionId,
    type: 'daily',
    score: 0.95
  }
});

// Subscribe to user events
await mq.subscribeToEvents([mq.topics.USER_EVENTS], async (topic, event) => {
  switch (event.type) {
    case 'user.registered':
      await handleNewUser(event.data);
      break;
    case 'user.upgraded':
      await handleUpgrade(event.data);
      break;
  }
});
```

### REST API Integration

```javascript
// api-integration.js
class APIIntegration {
  constructor() {
    this.baseURL = process.env.API_BASE_URL;
    this.apiKey = process.env.API_KEY;
  }

  async request(method, endpoint, data = null, options = {}) {
    const config = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`,
        'X-Request-ID': generateRequestId(),
        ...options.headers
      }
    };

    if (data) {
      config.body = JSON.stringify(data);
    }

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, config);

      if (!response.ok) {
        throw new APIError(`API request failed: ${response.status}`, response);
      }

      return await response.json();

    } catch (error) {
      logger.error('API request failed', { method, endpoint, error });
      throw error;
    }
  }

  // Service-specific methods
  async getPrediction(userId, date) {
    return this.request('GET', `/predictions/daily`, null, {
      params: { userId, date }
    });
  }

  async analyzeCompatibility(user1Id, user2Id) {
    return this.request('POST', '/compatibility/analyze', {
      user1Id,
      user2Id,
      includeReport: true
    });
  }

  async generateVoice(text, voiceId) {
    return this.request('POST', '/voice/generate', {
      text,
      voiceId,
      format: 'mp3'
    });
  }
}
```

### GraphQL Integration

```javascript
// graphql-integration.js
class GraphQLIntegration {
  constructor() {
    this.client = new ApolloClient({
      uri: process.env.GRAPHQL_ENDPOINT,
      cache: new InMemoryCache(),
      headers: {
        authorization: `Bearer ${process.env.API_KEY}`
      }
    });
  }

  async query(query, variables = {}) {
    try {
      const result = await this.client.query({
        query,
        variables,
        fetchPolicy: 'cache-first'
      });
      return result.data;
    } catch (error) {
      logger.error('GraphQL query failed', { error });
      throw error;
    }
  }

  async mutation(mutation, variables = {}) {
    try {
      const result = await this.client.mutate({
        mutation,
        variables
      });
      return result.data;
    } catch (error) {
      logger.error('GraphQL mutation failed', { error });
      throw error;
    }
  }

  // Common queries
  async getUserWithPredictions(userId) {
    const query = gql`
      query GetUserWithPredictions($userId: ID!) {
        user(id: $userId) {
          id
          email
          profile {
            zodiacSign
            birthDate
          }
          predictions(limit: 10) {
            id
            type
            content
            generatedAt
          }
        }
      }
    `;

    return this.query(query, { userId });
  }

  async generateAndGetPrediction(userId, type) {
    const mutation = gql`
      mutation GeneratePrediction($userId: ID!, $type: PredictionType!) {
        generatePrediction(userId: $userId, type: $type) {
          id
          content
          insights
          audioUrl
          imageUrl
        }
      }
    `;

    return this.mutation(mutation, { userId, type });
  }
}
```

---

## Data Flow Integration

### Real-time Data Pipeline

```javascript
// data-pipeline-integration.js
class DataPipelineIntegration {
  constructor() {
    this.kafka = new KafkaStreams();
    this.redis = new RedisClient();
    this.postgres = new PostgresClient();
    this.bigquery = new BigQueryClient();
  }

  async setupPipeline() {
    // 1. User Activity Stream
    const userActivityStream = this.kafka.stream('user-activity')
      .filter(event => event.type !== 'heartbeat')
      .map(event => this.enrichEvent(event))
      .window(60000) // 1 minute windows
      .aggregate(events => this.aggregateEvents(events));

    // 2. Prediction Stream
    const predictionStream = this.kafka.stream('predictions')
      .map(event => this.processPrediction(event))
      .fork([
        stream => stream.to(this.postgres, 'predictions'),
        stream => stream.to(this.redis, 'recent-predictions'),
        stream => stream.to(this.bigquery, 'predictions-analytics')
      ]);

    // 3. Revenue Stream
    const revenueStream = this.kafka.stream('transactions')
      .filter(event => event.status === 'completed')
      .map(event => this.processTransaction(event))
      .aggregate(transactions => this.calculateRevenue(transactions))
      .to(this.redis, 'revenue-metrics');

    // 4. Real-time Analytics
    const analyticsStream = this.kafka.merge([
      userActivityStream,
      predictionStream,
      revenueStream
    ])
      .map(event => this.transformForAnalytics(event))
      .batch(100)
      .to(this.bigquery, 'real-time-analytics');

    // Start all streams
    await Promise.all([
      userActivityStream.start(),
      predictionStream.start(),
      revenueStream.start(),
      analyticsStream.start()
    ]);
  }

  enrichEvent(event) {
    return {
      ...event,
      enrichedAt: Date.now(),
      serverVersion: process.env.VERSION,
      environment: process.env.NODE_ENV
    };
  }

  aggregateEvents(events) {
    return {
      count: events.length,
      users: [...new Set(events.map(e => e.userId))],
      types: this.countByType(events),
      timestamp: Date.now()
    };
  }
}
```

### Data Synchronization

```javascript
// data-sync-integration.js
class DataSyncIntegration {
  constructor() {
    this.sources = {
      postgres: new PostgresClient(),
      mongodb: new MongoClient(),
      redis: new RedisClient()
    };
  }

  async syncUserData(userId) {
    const syncTasks = [];

    // 1. Sync profile data
    syncTasks.push(this.syncProfile(userId));

    // 2. Sync predictions
    syncTasks.push(this.syncPredictions(userId));

    // 3. Sync analytics
    syncTasks.push(this.syncAnalytics(userId));

    // 4. Sync cache
    syncTasks.push(this.syncCache(userId));

    const results = await Promise.allSettled(syncTasks);

    // Log any failures
    results.forEach((result, index) => {
      if (result.status === 'rejected') {
        logger.error(`Sync task ${index} failed`, {
          userId,
          error: result.reason
        });
      }
    });

    return {
      success: results.every(r => r.status === 'fulfilled'),
      details: results
    };
  }

  async syncProfile(userId) {
    // Get from primary source
    const profile = await this.sources.postgres.query(
      'SELECT * FROM user_profiles WHERE user_id = $1',
      [userId]
    );

    // Update secondary sources
    await Promise.all([
      this.sources.mongodb.collection('profiles').updateOne(
        { userId },
        { $set: profile },
        { upsert: true }
      ),
      this.sources.redis.set(`profile:${userId}`, JSON.stringify(profile), 3600)
    ]);
  }

  async syncPredictions(userId) {
    // Get recent predictions
    const predictions = await this.sources.postgres.query(
      'SELECT * FROM predictions WHERE user_id = $1 ORDER BY created_at DESC LIMIT 10',
      [userId]
    );

    // Update cache
    await this.sources.redis.set(
      `predictions:${userId}`,
      JSON.stringify(predictions),
      86400
    );
  }
}
```

---

## API Integration

### Client SDK Integration

```javascript
// cosmic-coach-sdk.js
class CosmicCoachSDK {
  constructor(apiKey, options = {}) {
    this.apiKey = apiKey;
    this.baseURL = options.baseURL || 'https://api.cosmiccoach.app/v1';
    this.timeout = options.timeout || 30000;
    this.retries = options.retries || 3;
  }

  // Authentication
  async authenticate() {
    const response = await this.request('POST', '/auth/validate', {
      apiKey: this.apiKey
    });
    this.token = response.token;
    return response;
  }

  // Predictions
  async getDailyPrediction(userId) {
    return this.request('GET', `/predictions/daily/${userId}`);
  }

  async generatePrediction(userId, type = 'daily') {
    return this.request('POST', '/predictions/generate', {
      userId,
      type,
      includeAudio: true,
      includeImage: true
    });
  }

  // Compatibility
  async checkCompatibility(user1Id, user2Id) {
    return this.request('POST', '/compatibility/check', {
      user1Id,
      user2Id
    });
  }

  // Voice
  async generateVoice(text, options = {}) {
    return this.request('POST', '/voice/generate', {
      text,
      ...options
    });
  }

  // Chat
  async sendMessage(userId, message) {
    return this.request('POST', '/chat/message', {
      userId,
      message
    });
  }

  // Helper method for requests
  async request(method, endpoint, data = null) {
    let attempts = 0;

    while (attempts < this.retries) {
      try {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
          method,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token || this.apiKey}`,
            'X-SDK-Version': '1.0.0'
          },
          body: data ? JSON.stringify(data) : undefined,
          signal: AbortSignal.timeout(this.timeout)
        });

        if (!response.ok) {
          throw new Error(`API Error: ${response.status}`);
        }

        return await response.json();

      } catch (error) {
        attempts++;
        if (attempts >= this.retries) {
          throw error;
        }
        await this.delay(1000 * attempts); // Exponential backoff
      }
    }
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Usage Example
const sdk = new CosmicCoachSDK('your-api-key');
await sdk.authenticate();

const prediction = await sdk.getDailyPrediction('user123');
const compatibility = await sdk.checkCompatibility('user123', 'user456');
```

### Webhook Integration

```javascript
// webhook-integration.js
class WebhookIntegration {
  constructor() {
    this.webhooks = new Map();
    this.retryQueue = new Queue('webhook-retries');
  }

  async register(userId, config) {
    const webhook = {
      id: generateId(),
      userId,
      url: config.url,
      events: config.events,
      secret: generateSecret(),
      active: true,
      createdAt: Date.now()
    };

    await this.saveWebhook(webhook);
    this.webhooks.set(webhook.id, webhook);

    return {
      id: webhook.id,
      secret: webhook.secret
    };
  }

  async trigger(event) {
    const webhooks = await this.getWebhooksForEvent(event.type);

    const promises = webhooks.map(webhook =>
      this.sendWebhook(webhook, event)
    );

    await Promise.allSettled(promises);
  }

  async sendWebhook(webhook, event) {
    const payload = {
      id: generateId(),
      type: event.type,
      data: event.data,
      timestamp: Date.now()
    };

    const signature = this.generateSignature(payload, webhook.secret);

    try {
      const response = await fetch(webhook.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Webhook-Signature': signature,
          'X-Webhook-Id': webhook.id
        },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(5000)
      });

      if (!response.ok) {
        throw new Error(`Webhook failed: ${response.status}`);
      }

      await this.logSuccess(webhook.id, payload.id);

    } catch (error) {
      await this.handleFailure(webhook, payload, error);
    }
  }

  async handleFailure(webhook, payload, error) {
    logger.error('Webhook failed', {
      webhookId: webhook.id,
      error: error.message
    });

    // Add to retry queue
    await this.retryQueue.add({
      webhook,
      payload,
      attempts: 1,
      lastError: error.message
    });
  }

  generateSignature(payload, secret) {
    const hmac = crypto.createHmac('sha256', secret);
    hmac.update(JSON.stringify(payload));
    return hmac.digest('hex');
  }
}
```

---

## Event-Driven Integration

### Event Bus Architecture

```javascript
// event-bus-integration.js
class EventBusIntegration {
  constructor() {
    this.eventBus = new EventEmitter();
    this.handlers = new Map();
    this.middleware = [];
  }

  // Register event handler
  on(eventType, handler, options = {}) {
    const wrappedHandler = async (event) => {
      try {
        // Apply middleware
        for (const mw of this.middleware) {
          await mw(event);
        }

        // Execute handler
        await handler(event);

        // Track success
        metrics.increment(`events.handled.${eventType}`);

      } catch (error) {
        logger.error('Event handler failed', { eventType, error });

        if (options.retry) {
          await this.retryHandler(eventType, event, handler);
        }
      }
    };

    this.eventBus.on(eventType, wrappedHandler);
    this.handlers.set(`${eventType}:${handler.name}`, wrappedHandler);
  }

  // Emit event
  async emit(eventType, data) {
    const event = {
      id: generateId(),
      type: eventType,
      data,
      timestamp: Date.now(),
      metadata: {
        service: process.env.SERVICE_NAME,
        version: process.env.VERSION
      }
    };

    // Log event
    logger.info('Event emitted', { eventType, eventId: event.id });

    // Emit to local handlers
    this.eventBus.emit(eventType, event);

    // Publish to distributed queue
    await this.publishToQueue(event);

    return event.id;
  }

  // Add middleware
  use(middleware) {
    this.middleware.push(middleware);
  }

  // System event handlers
  setupSystemEvents() {
    // User events
    this.on('user.registered', async (event) => {
      await Promise.all([
        this.createWelcomePrediction(event.data.userId),
        this.sendWelcomeEmail(event.data.userId),
        this.trackRegistration(event.data)
      ]);
    });

    this.on('user.upgraded', async (event) => {
      await Promise.all([
        this.unlockPremiumFeatures(event.data.userId),
        this.sendUpgradeConfirmation(event.data.userId),
        this.trackRevenue(event.data)
      ]);
    });

    // Prediction events
    this.on('prediction.generated', async (event) => {
      await Promise.all([
        this.cacheP
        this.scheduleNotification(event.data),
        this.trackEngagement(event.data)
      ]);
    });

    // Compatibility events
    this.on('compatibility.analyzed', async (event) => {
      if (event.data.score > 0.8) {
        await this.sendHighCompatibilityNotification(event.data);
      }
    });

    // Revenue events
    this.on('payment.successful', async (event) => {
      await Promise.all([
        this.updateSubscription(event.data),
        this.sendReceipt(event.data),
        this.trackLTV(event.data)
      ]);
    });
  }
}

// Usage
const eventBus = new EventBusIntegration();
eventBus.setupSystemEvents();

// Emit events
await eventBus.emit('user.registered', { userId: 'user123' });
await eventBus.emit('prediction.generated', {
  userId: 'user123',
  predictionId: 'pred456'
});
```

---

## Testing Integration

### Integration Test Suite

```javascript
// integration-tests.js
describe('System Integration Tests', () => {
  let services;

  beforeAll(async () => {
    services = await setupTestServices();
  });

  afterAll(async () => {
    await teardownTestServices();
  });

  describe('Prediction Integration', () => {
    test('should generate prediction with all features', async () => {
      const userId = 'test-user-1';

      // Generate prediction
      const prediction = await services.prediction.generate(userId);

      // Verify all integrations worked
      expect(prediction).toHaveProperty('content');
      expect(prediction).toHaveProperty('audioUrl');
      expect(prediction).toHaveProperty('imageUrl');

      // Verify analytics tracked
      const events = await services.analytics.getEvents(userId);
      expect(events).toContainEqual(
        expect.objectContaining({
          type: 'prediction.generated'
        })
      );

      // Verify notification scheduled
      const notifications = await services.notification.getScheduled(userId);
      expect(notifications).toHaveLength(1);
    });
  });

  describe('End-to-End User Flow', () => {
    test('should handle complete user journey', async () => {
      // 1. Register user
      const user = await services.auth.register({
        email: 'test@example.com',
        password: 'Test123!'
      });

      // 2. Complete profile
      await services.profile.update(user.id, {
        birthDate: '1990-01-15',
        birthTime: '14:30',
        location: 'New York, NY'
      });

      // 3. Generate first prediction
      const prediction = await services.prediction.generate(user.id);
      expect(prediction).toBeDefined();

      // 4. Check compatibility
      const compatibility = await services.compatibility.analyze(
        user.id,
        'another-user-id'
      );
      expect(compatibility.score).toBeGreaterThan(0);

      // 5. Upgrade to premium
      await services.subscription.create(user.id, 'premium');

      // 6. Generate voice prediction
      const voicePrediction = await services.voice.generate(
        prediction.content
      );
      expect(voicePrediction).toHaveProperty('audioUrl');

      // 7. Verify all events tracked
      const analytics = await services.analytics.getUserJourney(user.id);
      expect(analytics.events).toContain('user.registered');
      expect(analytics.events).toContain('prediction.generated');
      expect(analytics.events).toContain('subscription.created');
    });
  });
});
```

### Load Testing

```javascript
// load-test-integration.js
import { check } from 'k6';
import http from 'k6/http';

export const options = {
  stages: [
    { duration: '5m', target: 100 },  // Ramp up
    { duration: '10m', target: 100 }, // Stay at 100 users
    { duration: '5m', target: 500 },  // Ramp to 500
    { duration: '10m', target: 500 }, // Stay at 500
    { duration: '5m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'], // 95% of requests under 2s
    http_req_failed: ['rate<0.01'],    // Error rate under 1%
  },
};

export default function () {
  const userId = `user-${__VU}-${__ITER}`;

  // Test prediction generation
  const predictionRes = http.post(
    'https://api.cosmiccoach.app/v1/predictions/generate',
    JSON.stringify({ userId, type: 'daily' }),
    {
      headers: { 'Content-Type': 'application/json' },
    }
  );

  check(predictionRes, {
    'prediction generated': (r) => r.status === 200,
    'has content': (r) => JSON.parse(r.body).content !== undefined,
  });

  // Test compatibility check
  const compatibilityRes = http.post(
    'https://api.cosmiccoach.app/v1/compatibility/check',
    JSON.stringify({
      user1Id: userId,
      user2Id: `user-${__VU + 1}-${__ITER}`
    }),
    {
      headers: { 'Content-Type': 'application/json' },
    }
  );

  check(compatibilityRes, {
    'compatibility calculated': (r) => r.status === 200,
    'has score': (r) => JSON.parse(r.body).score !== undefined,
  });
}
```

---

## Deployment Integration

### Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Databases
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: cosmiccoach
      POSTGRES_USER: cosmic
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  mongodb:
    image: mongo:6
    environment:
      MONGO_INITDB_ROOT_USERNAME: cosmic
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD}
    volumes:
      - mongo-data:/data/db
    ports:
      - "27017:27017"

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"

  # Message Queue
  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
    ports:
      - "9092:9092"

  # Core Services
  prediction-service:
    build: ./services/prediction
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://cosmic:${DB_PASSWORD}@postgres:5432/cosmiccoach
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "3001:3001"

  compatibility-service:
    build: ./services/compatibility
    depends_on:
      - postgres
      - mongodb
    environment:
      DATABASE_URL: postgresql://cosmic:${DB_PASSWORD}@postgres:5432/cosmiccoach
      MONGODB_URL: mongodb://cosmic:${MONGO_PASSWORD}@mongodb:27017
    ports:
      - "3002:3002"

  voice-service:
    build: ./services/voice
    depends_on:
      - redis
    environment:
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
      ELEVENLABS_API_KEY: ${ELEVENLABS_API_KEY}
    ports:
      - "3003:3003"

  # API Gateway
  api-gateway:
    build: ./gateway
    depends_on:
      - prediction-service
      - compatibility-service
      - voice-service
    environment:
      SERVICES: |
        prediction:http://prediction-service:3001
        compatibility:http://compatibility-service:3002
        voice:http://voice-service:3003
    ports:
      - "8080:8080"

volumes:
  postgres-data:
  mongo-data:
  redis-data:

networks:
  default:
    name: cosmic-coach-network
```

### Kubernetes Integration

```yaml
# kubernetes-integration.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cosmic-coach-config
data:
  services.json: |
    {
      "prediction": "http://prediction-service:3001",
      "compatibility": "http://compatibility-service:3002",
      "voice": "http://voice-service:3003",
      "image": "http://image-service:3004",
      "analytics": "http://analytics-service:3005",
      "notification": "http://notification-service:3006",
      "revenue": "http://revenue-service:3008"
    }

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cosmic-coach-gateway
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gateway
  template:
    metadata:
      labels:
        app: gateway
    spec:
      containers:
      - name: gateway
        image: cosmiccoach/gateway:latest
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: config
          mountPath: /config
        env:
        - name: CONFIG_PATH
          value: /config/services.json
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 10
      volumes:
      - name: config
        configMap:
          name: cosmic-coach-config

---
apiVersion: v1
kind: Service
metadata:
  name: gateway-service
spec:
  type: LoadBalancer
  selector:
    app: gateway
  ports:
  - port: 80
    targetPort: 8080
```

---

## Troubleshooting

### Common Integration Issues

```javascript
// troubleshooting-guide.js
const INTEGRATION_ISSUES = {
  'CONNECTION_REFUSED': {
    symptoms: ['ECONNREFUSED errors', 'Service unreachable'],
    causes: ['Service not running', 'Wrong port', 'Network issues'],
    solutions: [
      'Check service health: docker ps',
      'Verify port mapping: docker port <container>',
      'Check logs: docker logs <container>',
      'Restart service: docker-compose restart <service>'
    ]
  },

  'TIMEOUT': {
    symptoms: ['Request timeout', 'Slow responses'],
    causes: ['High load', 'Database locks', 'External API limits'],
    solutions: [
      'Check system resources: top/htop',
      'Review database queries: EXPLAIN ANALYZE',
      'Implement caching',
      'Add circuit breakers'
    ]
  },

  'AUTH_FAILED': {
    symptoms: ['401 Unauthorized', 'Token invalid'],
    causes: ['Expired token', 'Wrong API key', 'CORS issues'],
    solutions: [
      'Verify API keys in .env',
      'Check token expiration',
      'Review CORS configuration',
      'Regenerate credentials'
    ]
  },

  'DATA_INCONSISTENCY': {
    symptoms: ['Missing data', 'Stale cache', 'Wrong values'],
    causes: ['Sync issues', 'Race conditions', 'Cache invalidation'],
    solutions: [
      'Clear cache: redis-cli FLUSHALL',
      'Force data sync',
      'Implement distributed locks',
      'Add data validation'
    ]
  }
};

// Diagnostic tool
class IntegrationDiagnostics {
  async runDiagnostics() {
    const results = {
      timestamp: new Date().toISOString(),
      services: {},
      connections: {},
      performance: {}
    };

    // Check all services
    for (const service of Object.keys(SERVICE_REGISTRY)) {
      results.services[service] = await this.checkService(service);
    }

    // Check connections
    results.connections = {
      database: await this.checkDatabase(),
      redis: await this.checkRedis(),
      kafka: await this.checkKafka(),
      external: await this.checkExternalAPIs()
    };

    // Performance metrics
    results.performance = {
      apiLatency: await this.measureAPILatency(),
      databaseQueries: await this.profileDatabase(),
      cacheHitRate: await this.getCacheMetrics()
    };

    return results;
  }

  async checkService(name) {
    try {
      const url = `${SERVICE_REGISTRY[name].host}:${SERVICE_REGISTRY[name].port}/health`;
      const response = await fetch(url, { timeout: 5000 });

      return {
        status: response.ok ? 'healthy' : 'unhealthy',
        responseTime: response.headers.get('X-Response-Time'),
        version: response.headers.get('X-Service-Version')
      };
    } catch (error) {
      return {
        status: 'unreachable',
        error: error.message
      };
    }
  }
}
```

### Integration Health Monitor

```javascript
// health-monitor.js
class IntegrationHealthMonitor {
  constructor() {
    this.checks = new Map();
    this.alerts = new AlertManager();
  }

  async monitorIntegrations() {
    setInterval(async () => {
      const health = await this.checkAll();

      if (health.issues.length > 0) {
        await this.handleIssues(health.issues);
      }

      // Update metrics
      metrics.gauge('integration.health.score', health.score);

    }, 60000); // Check every minute
  }

  async checkAll() {
    const results = {
      timestamp: Date.now(),
      checks: {},
      issues: [],
      score: 100
    };

    // Service connectivity
    results.checks.services = await this.checkServiceConnectivity();

    // Data consistency
    results.checks.dataConsistency = await this.checkDataConsistency();

    // API response times
    results.checks.apiPerformance = await this.checkAPIPerformance();

    // Queue backlog
    results.checks.queueHealth = await this.checkQueueHealth();

    // Calculate health score
    for (const [category, check] of Object.entries(results.checks)) {
      if (!check.passed) {
        results.issues.push({
          category,
          severity: check.severity,
          message: check.message
        });
        results.score -= check.severity === 'critical' ? 25 : 10;
      }
    }

    return results;
  }

  async handleIssues(issues) {
    for (const issue of issues) {
      if (issue.severity === 'critical') {
        // Page on-call
        await this.alerts.sendCritical(issue);

        // Attempt auto-recovery
        await this.attemptRecovery(issue);
      } else {
        // Log and monitor
        logger.warn('Integration issue detected', issue);
      }
    }
  }
}
```

---

## Conclusion

This Integration Guide provides comprehensive instructions for connecting all 9 systems of the Cosmic Coach platform. Follow the integration patterns, use the provided code examples, and leverage the troubleshooting guides to ensure smooth system integration.

**Key Integration Principles:**
- **Loose Coupling**: Services communicate through well-defined interfaces
- **High Cohesion**: Related functionality grouped together
- **Fault Tolerance**: Graceful degradation when services fail
- **Observability**: Comprehensive monitoring and logging
- **Scalability**: Horizontal scaling through proper integration patterns

**Support Resources:**
- Documentation: https://docs.cosmiccoach.app
- API Reference: https://api.cosmiccoach.app/docs
- Support: support@cosmiccoach.app
- Slack: cosmiccoach.slack.com