# Utilities Implementation - Ready to Use Code

Este archivo contiene el código completo listo para copiar/pegar en los archivos correspondientes.

---

## 1. lib/utils/constants.dart

```dart
/// Application-wide constants
///
/// This file centralizes all magic numbers, strings, and configuration values
/// used throughout the application. This makes it easier to maintain and update
/// configuration without hunting through multiple files.
class AppConstants {
  // Prevent instantiation
  AppConstants._();

  // ========================================================================
  // API CONFIGURATION
  // ========================================================================

  /// Base URL for the backend API
  ///
  /// Can be overridden with environment variable: API_BASE_URL
  static const baseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'https://zodiac-backend-api-production-8ded.up.railway.app',
  );

  /// API version
  static const apiVersion = 'v1';

  /// Default API timeout
  static const apiTimeout = Duration(seconds: 30);

  // ========================================================================
  // API ENDPOINTS
  // ========================================================================

  static String get validateReceiptEndpoint => '$baseUrl/api/validate-receipt';
  static String get paymentsEndpoint => '$baseUrl/api/payments';
  static String get weeklyHoroscopeEndpoint => '$baseUrl/api/weekly-horoscope';

  // ========================================================================
  // TIMEOUT DURATIONS
  // ========================================================================

  /// Short timeout for quick operations (e.g., crypto operations)
  static const shortTimeout = Duration(seconds: 5);

  /// Medium timeout for standard operations
  static const mediumTimeout = Duration(seconds: 10);

  /// Long timeout for complex operations
  static const longTimeout = Duration(seconds: 20);

  // ========================================================================
  // CACHE TTL (Time To Live)
  // ========================================================================

  /// Short-lived cache (3 hours) - for frequently changing data
  static const shortCacheTTL = Duration(hours: 3);

  /// Default cache duration (6 hours) - for most compatibility analyses
  static const defaultCacheTTL = Duration(hours: 6);

  /// Medium-lived cache (12 hours) - for communication patterns
  static const mediumCacheTTL = Duration(hours: 12);

  /// Long-lived cache (24 hours) - for user profiles and static data
  static const longCacheTTL = Duration(hours: 24);

  /// Weekly cache (6 days) - for weekly horoscopes
  static const weeklyCacheTTL = Duration(days: 6);

  /// Monthly cache (30 days) - for historical data
  static const monthlyCacheTTL = Duration(days: 30);

  /// Crypto cache validation duration
  static const cryptoCacheValidDuration = Duration(minutes: 30);

  // ========================================================================
  // CLEANUP & MAINTENANCE INTERVALS
  // ========================================================================

  /// Short interval for frequent checks (5 minutes)
  static const shortInterval = Duration(minutes: 5);

  /// Default cleanup interval (10 minutes)
  static const defaultInterval = Duration(minutes: 10);

  /// Medium interval for less frequent checks (15 minutes)
  static const mediumInterval = Duration(minutes: 15);

  /// Long interval for periodic maintenance (30 minutes)
  static const longInterval = Duration(minutes: 30);

  // ========================================================================
  // RETRY CONFIGURATION
  // ========================================================================

  /// Maximum number of retry attempts for failed operations
  static const maxRetries = 3;

  /// Initial delay between retries
  static const retryDelay = Duration(seconds: 2);

  /// Maximum delay between retries (for exponential backoff)
  static const maxRetryDelay = Duration(seconds: 10);

  // ========================================================================
  // COOLDOWN PERIODS
  // ========================================================================

  /// Cooldown period for gamification notifications
  static const gamificationCooldown = Duration(hours: 1);

  /// Cooldown period between general notifications
  static const notificationCooldown = Duration(minutes: 5);

  // ========================================================================
  // DATA RETENTION
  // ========================================================================

  /// How long to keep analytics data
  static const analyticsRetention = Duration(days: 30);

  /// When to clean up old cache entries
  static const cacheCleanupAge = Duration(days: 7);

  // ========================================================================
  // VALIDATION LIMITS
  // ========================================================================

  /// Maximum age in years for birth date validation
  static const maxAgeYears = 120;

  /// Minimum password length
  static const minPasswordLength = 8;

  /// Maximum input length for user inputs
  static const maxInputLength = 2000;

  /// Maximum length for user names
  static const maxNameLength = 50;

  // ========================================================================
  // SOCIAL MEDIA CHARACTER LIMITS
  // ========================================================================

  static const maxCharsFacebook = 2200;
  static const maxCharsInstagram = 150;
  static const maxCharsTwitter = 280;
  static const maxCharsWhatsApp = 500;

  // ========================================================================
  // LOCALE CONFIGURATION
  // ========================================================================

  static const defaultLocale = 'en';
  static const supportedLocales = ['en', 'es', 'fr', 'de', 'it', 'pt'];

  // ========================================================================
  // CACHE LIMITS
  // ========================================================================

  /// Maximum number of items in memory cache
  static const maxCacheSize = 100;

  /// Maximum number of cache entries before cleanup
  static const maxCacheEntries = 1000;

  // ========================================================================
  // RATE LIMITING
  // ========================================================================

  /// Maximum API requests per minute
  static const maxApiRequestsPerMinute = 100;

  /// Maximum burst of API requests
  static const maxApiRequestsBurst = 10;

  /// Cooldown period after rate limit hit
  static const rateLimitCooldown = Duration(seconds: 60);

  // ========================================================================
  // EXTERNAL API ENDPOINTS
  // ========================================================================

  /// OpenStreetMap Nominatim API for geocoding
  static const geocodingBaseUrl = 'https://nominatim.openstreetmap.org';

  /// Google Calendar API scope
  static const googleCalendarScope = 'https://www.googleapis.com/auth/calendar';

  /// Apple iTunes receipt verification (sandbox)
  static const appleReceiptSandboxUrl = 'https://sandbox.itunes.apple.com/verifyReceipt';

  /// Apple iTunes receipt verification (production)
  static const appleReceiptProductionUrl = 'https://buy.itunes.apple.com/verifyReceipt';

  // ========================================================================
  // FEATURE FLAGS (can be overridden by remote config)
  // ========================================================================

  static const enableAdvancedAnalytics = bool.fromEnvironment(
    'ENABLE_ADVANCED_ANALYTICS',
    defaultValue: true,
  );

  static const enableCrashReporting = bool.fromEnvironment(
    'ENABLE_CRASH_REPORTING',
    defaultValue: true,
  );

  static const enablePerformanceMonitoring = bool.fromEnvironment(
    'ENABLE_PERFORMANCE_MONITORING',
    defaultValue: true,
  );

  // ========================================================================
  // DEBUG CONFIGURATION
  // ========================================================================

  static const debugLogLevel = String.fromEnvironment(
    'LOG_LEVEL',
    defaultValue: 'info',
  );
}
```

---

## 2. lib/utils/validators.dart

```dart
/// Input validation utilities
///
/// Provides centralized validation logic for common data types used throughout
/// the application. All validators return consistent results and have proper
/// null-safety handling.
class Validators {
  // Prevent instantiation
  Validators._();

  // ========================================================================
  // EMAIL VALIDATION
  // ========================================================================

  static final _emailRegex = RegExp(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
  );

  /// Validates an email address format
  ///
  /// Returns `true` if the email matches the standard email pattern.
  /// Returns `false` for null, empty, or invalid email addresses.
  ///
  /// Example:
  /// ```dart
  /// Validators.isValidEmail('user@example.com')  // true
  /// Validators.isValidEmail('invalid')           // false
  /// Validators.isValidEmail('')                  // false
  /// ```
  static bool isValidEmail(String? email) {
    if (email == null || email.isEmpty) return false;
    return _emailRegex.hasMatch(email.trim());
  }

  // ========================================================================
  // PASSWORD VALIDATION
  // ========================================================================

  /// Validates password strength
  ///
  /// Requirements:
  /// - Minimum 8 characters
  /// - At least one uppercase letter
  /// - At least one lowercase letter
  /// - At least one number
  /// - At least one special character
  ///
  /// Returns `true` if all requirements are met.
  static bool isValidPassword(String? password) {
    if (password == null || password.length < 8) return false;

    // Check for at least one uppercase letter
    if (!RegExp(r'[A-Z]').hasMatch(password)) return false;

    // Check for at least one lowercase letter
    if (!RegExp(r'[a-z]').hasMatch(password)) return false;

    // Check for at least one number
    if (!RegExp(r'[0-9]').hasMatch(password)) return false;

    // Check for at least one special character
    if (!RegExp(r'[!@#$%^&*(),.?":{}|<>]').hasMatch(password)) return false;

    return true;
  }

  /// Returns a list of unmet password requirements
  ///
  /// Useful for showing specific feedback to users.
  static List<String> getPasswordRequirements(String? password) {
    final requirements = <String>[];

    if (password == null || password.isEmpty) {
      requirements.add('Password is required');
      return requirements;
    }

    if (password.length < 8) {
      requirements.add('At least 8 characters');
    }
    if (!RegExp(r'[A-Z]').hasMatch(password)) {
      requirements.add('At least one uppercase letter');
    }
    if (!RegExp(r'[a-z]').hasMatch(password)) {
      requirements.add('At least one lowercase letter');
    }
    if (!RegExp(r'[0-9]').hasMatch(password)) {
      requirements.add('At least one number');
    }
    if (!RegExp(r'[!@#$%^&*(),.?":{}|<>]').hasMatch(password)) {
      requirements.add('At least one special character');
    }

    return requirements;
  }

  // ========================================================================
  // ZODIAC SIGN VALIDATION
  // ========================================================================

  /// Valid zodiac sign names (lowercase)
  static const validZodiacSigns = {
    'aries', 'taurus', 'gemini', 'cancer',
    'leo', 'virgo', 'libra', 'scorpio',
    'sagittarius', 'capricorn', 'aquarius', 'pisces',
  };

  /// Validates a zodiac sign name
  ///
  /// Returns `true` if the sign is one of the 12 valid zodiac signs.
  /// Case-insensitive and trims whitespace.
  ///
  /// Example:
  /// ```dart
  /// Validators.isValidZodiacSign('Aries')        // true
  /// Validators.isValidZodiacSign('aries')        // true
  /// Validators.isValidZodiacSign('  Aries  ')   // true
  /// Validators.isValidZodiacSign('Invalid')     // false
  /// ```
  static bool isValidZodiacSign(String? sign) {
    if (sign == null || sign.isEmpty) return false;
    return validZodiacSigns.contains(sign.toLowerCase().trim());
  }

  /// Normalizes a zodiac sign name to lowercase
  ///
  /// Throws `ArgumentError` if the sign is invalid.
  ///
  /// Example:
  /// ```dart
  /// Validators.normalizeZodiacSign('ARIES')  // 'aries'
  /// Validators.normalizeZodiacSign('Leo')    // 'leo'
  /// ```
  static String normalizeZodiacSign(String sign) {
    final normalized = sign.toLowerCase().trim();
    if (!validZodiacSigns.contains(normalized)) {
      throw ArgumentError('Invalid zodiac sign: $sign');
    }
    return normalized;
  }

  // ========================================================================
  // DATE VALIDATION
  // ========================================================================

  /// Validates a birth date
  ///
  /// Checks:
  /// - Date is not null
  /// - Date is not in the future
  /// - Date is not more than 120 years ago
  ///
  /// Returns a `ValidationResult` with details about the validation.
  static ValidationResult validateBirthDate(DateTime? date) {
    if (date == null) {
      return const ValidationResult(
        isValid: false,
        sanitizedInput: '',
        errorMessage: 'Birth date is required',
      );
    }

    final now = DateTime.now();

    if (date.isAfter(now)) {
      return const ValidationResult(
        isValid: false,
        sanitizedInput: '',
        errorMessage: 'Birth date cannot be in the future',
      );
    }

    final minDate = now.subtract(const Duration(days: 365 * 120));
    if (date.isBefore(minDate)) {
      return const ValidationResult(
        isValid: false,
        sanitizedInput: '',
        errorMessage: 'Birth date cannot be more than 120 years ago',
      );
    }

    return ValidationResult(
      isValid: true,
      sanitizedInput: date.toIso8601String(),
    );
  }

  /// Calculates age from birth date
  ///
  /// Returns the age in years, accounting for whether the birthday has
  /// occurred this year.
  static int calculateAge(DateTime birthDate) {
    final now = DateTime.now();
    int age = now.year - birthDate.year;

    if (now.month < birthDate.month ||
        (now.month == birthDate.month && now.day < birthDate.day)) {
      age--;
    }

    return age;
  }

  // ========================================================================
  // NULL/EMPTY STRING CHECKS
  // ========================================================================

  /// Checks if a string is null or empty
  ///
  /// Example:
  /// ```dart
  /// Validators.isNullOrEmpty(null)      // true
  /// Validators.isNullOrEmpty('')        // true
  /// Validators.isNullOrEmpty('  ')     // false (not empty, has spaces)
  /// Validators.isNullOrEmpty('text')   // false
  /// ```
  static bool isNullOrEmpty(String? str) {
    return str == null || str.isEmpty;
  }

  /// Checks if a string is null, empty, or contains only whitespace
  ///
  /// Example:
  /// ```dart
  /// Validators.isNullOrBlank(null)      // true
  /// Validators.isNullOrBlank('')        // true
  /// Validators.isNullOrBlank('  ')     // true
  /// Validators.isNullOrBlank('text')   // false
  /// ```
  static bool isNullOrBlank(String? str) {
    return str == null || str.trim().isEmpty;
  }

  /// Checks if a string is not null and not empty
  static bool isNotNullOrEmpty(String? str) {
    return str != null && str.isNotEmpty;
  }

  /// Checks if a string is not null, not empty, and not only whitespace
  static bool isNotNullOrBlank(String? str) {
    return str != null && str.trim().isNotEmpty;
  }
}

/// Result of a validation operation
class ValidationResult {
  final bool isValid;
  final String sanitizedInput;
  final List<String> warnings;
  final String? errorMessage;

  const ValidationResult({
    required this.isValid,
    required this.sanitizedInput,
    this.warnings = const [],
    this.errorMessage,
  });
}
```

---

## 3. lib/utils/string_utils.dart

```dart
/// String manipulation utilities
///
/// Provides common string operations used throughout the application.
class StringUtils {
  // Prevent instantiation
  StringUtils._();

  /// Capitalizes the first letter of a string
  ///
  /// Example:
  /// ```dart
  /// StringUtils.capitalize('hello')      // 'Hello'
  /// StringUtils.capitalize('HELLO')      // 'Hello'
  /// StringUtils.capitalize('hELLO')      // 'Hello'
  /// StringUtils.capitalize('')           // ''
  /// ```
  static String capitalize(String str) {
    if (str.isEmpty) return str;
    return str[0].toUpperCase() + str.substring(1).toLowerCase();
  }

  /// Capitalizes the first letter of each word
  ///
  /// Example:
  /// ```dart
  /// StringUtils.capitalizeWords('hello world')     // 'Hello World'
  /// StringUtils.capitalizeWords('HELLO WORLD')     // 'Hello World'
  /// StringUtils.capitalizeWords('hello  world')    // 'Hello  World'
  /// ```
  static String capitalizeWords(String str) {
    if (str.isEmpty) return str;

    return str.split(' ').map((word) {
      if (word.isEmpty) return word;
      return capitalize(word);
    }).join(' ');
  }

  /// Converts a string to title case
  ///
  /// Similar to capitalizeWords but also lowercases the entire string first.
  ///
  /// Example:
  /// ```dart
  /// StringUtils.toTitleCase('HELLO WORLD')      // 'Hello World'
  /// StringUtils.toTitleCase('hello world')      // 'Hello World'
  /// ```
  static String toTitleCase(String str) {
    return capitalizeWords(str.toLowerCase());
  }

  /// Sanitizes a string by trimming and lowercasing
  ///
  /// Useful for normalizing user input before comparison.
  ///
  /// Example:
  /// ```dart
  /// StringUtils.sanitize('  Hello World  ')     // 'hello world'
  /// StringUtils.sanitize('ARIES')               // 'aries'
  /// ```
  static String sanitize(String str) {
    return str.trim().toLowerCase();
  }

  /// Removes extra whitespace (multiple spaces become single space)
  ///
  /// Example:
  /// ```dart
  /// StringUtils.removeExtraSpaces('hello    world')      // 'hello world'
  /// StringUtils.removeExtraSpaces('  hello  world  ')   // 'hello world'
  /// ```
  static String removeExtraSpaces(String str) {
    return str.replaceAll(RegExp(r'\s+'), ' ').trim();
  }

  /// Checks if a string is empty or contains only whitespace
  ///
  /// Same as `Validators.isNullOrBlank` but for convenience in string operations.
  static bool isEmpty(String? str) {
    return str == null || str.trim().isEmpty;
  }

  /// Truncates a string to a maximum length
  ///
  /// If the string is longer than `maxLength`, it will be truncated and
  /// the `suffix` will be appended.
  ///
  /// Example:
  /// ```dart
  /// StringUtils.truncate('Hello World', 8)                    // 'Hello...'
  /// StringUtils.truncate('Hello World', 8, suffix: '…')       // 'Hello W…'
  /// StringUtils.truncate('Hello', 10)                         // 'Hello'
  /// ```
  static String truncate(String str, int maxLength, {String suffix = '...'}) {
    if (str.length <= maxLength) return str;
    return str.substring(0, maxLength - suffix.length) + suffix;
  }

  /// Extracts initials from a name
  ///
  /// Example:
  /// ```dart
  /// StringUtils.getInitials('John Doe')             // 'JD'
  /// StringUtils.getInitials('Mary Jane Watson')     // 'MJW'
  /// StringUtils.getInitials('Prince')               // 'P'
  /// ```
  static String getInitials(String name) {
    if (name.isEmpty) return '';

    final words = name.trim().split(RegExp(r'\s+'));
    if (words.length == 1) {
      return words[0][0].toUpperCase();
    }

    return words
        .take(3) // Max 3 initials
        .map((word) => word.isEmpty ? '' : word[0].toUpperCase())
        .join();
  }

  /// Converts a string to snake_case
  ///
  /// Example:
  /// ```dart
  /// StringUtils.toSnakeCase('HelloWorld')       // 'hello_world'
  /// StringUtils.toSnakeCase('helloWorld')       // 'hello_world'
  /// StringUtils.toSnakeCase('Hello World')      // 'hello_world'
  /// ```
  static String toSnakeCase(String str) {
    return str
        .replaceAllMapped(
          RegExp(r'[A-Z]'),
          (match) => '_${match.group(0)!.toLowerCase()}',
        )
        .replaceAll(' ', '_')
        .replaceAll('-', '_')
        .replaceAll(RegExp(r'_+'), '_')
        .replaceFirst(RegExp(r'^_'), '');
  }

  /// Converts a string to camelCase
  ///
  /// Example:
  /// ```dart
  /// StringUtils.toCamelCase('hello_world')      // 'helloWorld'
  /// StringUtils.toCamelCase('Hello World')      // 'helloWorld'
  /// ```
  static String toCamelCase(String str) {
    final words = str.split(RegExp(r'[_\s-]+'));
    if (words.isEmpty) return '';

    final first = words[0].toLowerCase();
    final rest = words.skip(1).map((word) => capitalize(word)).join();

    return first + rest;
  }
}
```

---

## 4. lib/utils/date_utils.dart

```dart
import 'package:intl/intl.dart';

/// Date and time manipulation utilities
///
/// Provides consistent date formatting, parsing, and manipulation throughout
/// the application.
class DateUtils {
  // Prevent instantiation
  DateUtils._();

  // ========================================================================
  // DATE FORMATTERS
  // ========================================================================

  static final _dateFormat = DateFormat('dd/MM/yyyy');
  static final _timeFormat = DateFormat('HH:mm');
  static final _dateTimeFormat = DateFormat('dd/MM/yyyy HH:mm');
  static final _dateKeyFormat = DateFormat('yyyy-MM-dd');

  /// Formats a date as DD/MM/YYYY
  ///
  /// Example:
  /// ```dart
  /// DateUtils.formatDate(DateTime(2025, 10, 15))  // '15/10/2025'
  /// ```
  static String formatDate(DateTime date) {
    return _dateFormat.format(date);
  }

  /// Formats time as HH:MM (24-hour format)
  ///
  /// Example:
  /// ```dart
  /// DateUtils.formatTime(DateTime(2025, 10, 15, 14, 30))  // '14:30'
  /// ```
  static String formatTime(DateTime date) {
    return _timeFormat.format(date);
  }

  /// Formats date and time as DD/MM/YYYY HH:MM
  ///
  /// Example:
  /// ```dart
  /// DateUtils.formatDateTime(DateTime(2025, 10, 15, 14, 30))  // '15/10/2025 14:30'
  /// ```
  static String formatDateTime(DateTime date) {
    return _dateTimeFormat.format(date);
  }

  /// Formats date as YYYY-MM-DD (ISO 8601 date, useful for cache keys)
  ///
  /// Example:
  /// ```dart
  /// DateUtils.formatDateKey(DateTime(2025, 10, 15))  // '2025-10-15'
  /// ```
  static String formatDateKey(DateTime date) {
    return _dateKeyFormat.format(date);
  }

  /// Formats date according to locale
  ///
  /// Example:
  /// ```dart
  /// DateUtils.formatDateLocalized(DateTime(2025, 10, 15), 'en')  // 'October 15, 2025'
  /// DateUtils.formatDateLocalized(DateTime(2025, 10, 15), 'es')  // '15 de octubre de 2025'
  /// ```
  static String formatDateLocalized(DateTime date, String languageCode) {
    final locale = _getLocale(languageCode);
    return DateFormat.yMMMMd(locale).format(date);
  }

  static String _getLocale(String languageCode) {
    switch (languageCode.toLowerCase()) {
      case 'es':
        return 'es_ES';
      case 'fr':
        return 'fr_FR';
      case 'de':
        return 'de_DE';
      case 'it':
        return 'it_IT';
      case 'pt':
        return 'pt_PT';
      default:
        return 'en_US';
    }
  }

  // ========================================================================
  // RELATIVE TIME FORMATTING
  // ========================================================================

  /// Formats date as relative time (e.g., "2 hours ago")
  ///
  /// Example:
  /// ```dart
  /// DateUtils.timeAgo(DateTime.now().subtract(Duration(hours: 2)))  // '2 hours ago'
  /// DateUtils.timeAgo(DateTime.now().subtract(Duration(days: 1)))   // '1 day ago'
  /// ```
  static String timeAgo(DateTime date) {
    final diff = DateTime.now().difference(date);

    if (diff.inDays > 365) {
      final years = (diff.inDays / 365).floor();
      return '$years ${years == 1 ? 'year' : 'years'} ago';
    }
    if (diff.inDays > 30) {
      final months = (diff.inDays / 30).floor();
      return '$months ${months == 1 ? 'month' : 'months'} ago';
    }
    if (diff.inDays > 0) {
      return '${diff.inDays} ${diff.inDays == 1 ? 'day' : 'days'} ago';
    }
    if (diff.inHours > 0) {
      return '${diff.inHours} ${diff.inHours == 1 ? 'hour' : 'hours'} ago';
    }
    if (diff.inMinutes > 0) {
      return '${diff.inMinutes} ${diff.inMinutes == 1 ? 'minute' : 'minutes'} ago';
    }
    return 'just now';
  }

  // ========================================================================
  // DURATION FORMATTING
  // ========================================================================

  /// Formats duration as HH:MM:SS or MM:SS
  ///
  /// Example:
  /// ```dart
  /// DateUtils.formatDuration(Duration(hours: 1, minutes: 30, seconds: 45))  // '1:30:45'
  /// DateUtils.formatDuration(Duration(minutes: 5, seconds: 30))             // '5:30'
  /// DateUtils.formatDuration(Duration(seconds: 45))                         // '45s'
  /// ```
  static String formatDuration(Duration duration) {
    final hours = duration.inHours;
    final minutes = duration.inMinutes.remainder(60);
    final seconds = duration.inSeconds.remainder(60);

    if (hours > 0) {
      return '$hours:${minutes.toString().padLeft(2, '0')}:${seconds.toString().padLeft(2, '0')}';
    } else if (minutes > 0) {
      return '$minutes:${seconds.toString().padLeft(2, '0')}';
    } else {
      return '${seconds}s';
    }
  }

  /// Formats duration in human-readable format
  ///
  /// Example:
  /// ```dart
  /// DateUtils.formatDurationHumanReadable(Duration(days: 2))       // '2 days'
  /// DateUtils.formatDurationHumanReadable(Duration(hours: 5))      // '5 hours'
  /// DateUtils.formatDurationHumanReadable(Duration(minutes: 30))   // '30 minutes'
  /// ```
  static String formatDurationHumanReadable(Duration duration) {
    final days = duration.inDays;
    final hours = duration.inHours.remainder(24);
    final minutes = duration.inMinutes.remainder(60);

    if (days > 0) return '$days ${days == 1 ? 'day' : 'days'}';
    if (hours > 0) return '$hours ${hours == 1 ? 'hour' : 'hours'}';
    if (minutes > 0) return '$minutes ${minutes == 1 ? 'minute' : 'minutes'}';
    return 'less than a minute';
  }

  // ========================================================================
  // DATE PARSING
  // ========================================================================

  /// Parses a timestamp (milliseconds since epoch) to DateTime
  ///
  /// Example:
  /// ```dart
  /// DateUtils.parseTimestamp(1697385600000)  // DateTime(2025, 10, 15, 12, 0)
  /// ```
  static DateTime parseTimestamp(int timestamp) {
    return DateTime.fromMillisecondsSinceEpoch(timestamp);
  }

  /// Safely parses a date string to DateTime
  ///
  /// Returns null if parsing fails instead of throwing an exception.
  ///
  /// Example:
  /// ```dart
  /// DateUtils.tryParseDate('2025-10-15')     // DateTime(2025, 10, 15)
  /// DateUtils.tryParseDate('invalid')        // null
  /// DateUtils.tryParseDate(null)             // null
  /// ```
  static DateTime? tryParseDate(String? dateString) {
    if (dateString == null || dateString.isEmpty) return null;
    try {
      return DateTime.parse(dateString);
    } catch (e) {
      return null;
    }
  }

  // ========================================================================
  // DATE COMPARISON HELPERS
  // ========================================================================

  /// Checks if a date is today
  static bool isToday(DateTime date) {
    final now = DateTime.now();
    return date.year == now.year &&
           date.month == now.month &&
           date.day == now.day;
  }

  /// Checks if a date is yesterday
  static bool isYesterday(DateTime date) {
    final yesterday = DateTime.now().subtract(const Duration(days: 1));
    return date.year == yesterday.year &&
           date.month == yesterday.month &&
           date.day == yesterday.day;
  }

  /// Checks if a date is in the past
  static bool isPast(DateTime date) {
    return date.isBefore(DateTime.now());
  }

  /// Checks if a date is in the future
  static bool isFuture(DateTime date) {
    return date.isAfter(DateTime.now());
  }

  /// Checks if two dates are on the same day
  static bool isSameDay(DateTime date1, DateTime date2) {
    return date1.year == date2.year &&
           date1.month == date2.month &&
           date1.day == date2.day;
  }
}
```

---

## 5. lib/utils/converters.dart

```dart
/// Type conversion utilities
///
/// Provides safe type conversions with proper error handling and default values.
class Converters {
  // Prevent instantiation
  Converters._();

  // ========================================================================
  // INTEGER PARSING
  // ========================================================================

  /// Safely parses a string to int
  ///
  /// Returns `defaultValue` if parsing fails.
  ///
  /// Example:
  /// ```dart
  /// Converters.tryParseInt('42')              // 42
  /// Converters.tryParseInt('  42  ')          // 42
  /// Converters.tryParseInt('invalid')         // null
  /// Converters.tryParseInt('invalid', defaultValue: 0)  // 0
  /// Converters.tryParseInt(null)              // null
  /// ```
  static int? tryParseInt(String? value, {int? defaultValue}) {
    if (value == null || value.isEmpty) return defaultValue;
    return int.tryParse(value.trim()) ?? defaultValue;
  }

  /// Parses a string to int with a default value
  ///
  /// Never returns null - always returns a valid int.
  ///
  /// Example:
  /// ```dart
  /// Converters.parseInt('42')              // 42
  /// Converters.parseInt('invalid')         // 0
  /// Converters.parseInt('invalid', defaultValue: -1)  // -1
  /// ```
  static int parseInt(String value, {int defaultValue = 0}) {
    return tryParseInt(value, defaultValue: defaultValue) ?? defaultValue;
  }

  // ========================================================================
  // DOUBLE PARSING
  // ========================================================================

  /// Safely parses a string to double
  ///
  /// Returns `defaultValue` if parsing fails.
  ///
  /// Example:
  /// ```dart
  /// Converters.tryParseDouble('42.5')              // 42.5
  /// Converters.tryParseDouble('  42.5  ')          // 42.5
  /// Converters.tryParseDouble('invalid')           // null
  /// Converters.tryParseDouble('invalid', defaultValue: 0.0)  // 0.0
  /// ```
  static double? tryParseDouble(String? value, {double? defaultValue}) {
    if (value == null || value.isEmpty) return defaultValue;
    return double.tryParse(value.trim()) ?? defaultValue;
  }

  /// Parses a string to double with a default value
  ///
  /// Never returns null - always returns a valid double.
  ///
  /// Example:
  /// ```dart
  /// Converters.parseDouble('42.5')              // 42.5
  /// Converters.parseDouble('invalid')           // 0.0
  /// Converters.parseDouble('invalid', defaultValue: -1.0)  // -1.0
  /// ```
  static double parseDouble(String value, {double defaultValue = 0.0}) {
    return tryParseDouble(value, defaultValue: defaultValue) ?? defaultValue;
  }

  // ========================================================================
  // BOOLEAN PARSING
  // ========================================================================

  /// Safely parses a string to bool
  ///
  /// Accepts various formats:
  /// - true: 'true', '1', 'yes', 'y', 'on'
  /// - false: 'false', '0', 'no', 'n', 'off'
  ///
  /// Returns null for unrecognized values.
  ///
  /// Example:
  /// ```dart
  /// Converters.tryParseBool('true')       // true
  /// Converters.tryParseBool('1')          // true
  /// Converters.tryParseBool('yes')        // true
  /// Converters.tryParseBool('false')      // false
  /// Converters.tryParseBool('0')          // false
  /// Converters.tryParseBool('invalid')    // null
  /// ```
  static bool? tryParseBool(String? value) {
    if (value == null || value.isEmpty) return null;

    final normalized = value.toLowerCase().trim();

    if (normalized == 'true' || normalized == '1' ||
        normalized == 'yes' || normalized == 'y' || normalized == 'on') {
      return true;
    }

    if (normalized == 'false' || normalized == '0' ||
        normalized == 'no' || normalized == 'n' || normalized == 'off') {
      return false;
    }

    return null;
  }

  /// Parses a string to bool with a default value
  ///
  /// Example:
  /// ```dart
  /// Converters.parseBool('true')              // true
  /// Converters.parseBool('invalid')           // false
  /// Converters.parseBool('invalid', defaultValue: true)  // true
  /// ```
  static bool parseBool(String value, {bool defaultValue = false}) {
    return tryParseBool(value) ?? defaultValue;
  }

  // ========================================================================
  // TIME STRING PARSING
  // ========================================================================

  /// Parses a time string in HH:MM format
  ///
  /// Returns a map with 'hour' and 'minute' keys.
  /// Throws `FormatException` if the format is invalid.
  ///
  /// Example:
  /// ```dart
  /// Converters.parseTimeString('14:30')  // {'hour': 14, 'minute': 30}
  /// Converters.parseTimeString('09:05')  // {'hour': 9, 'minute': 5}
  /// Converters.parseTimeString('25:00')  // throws FormatException
  /// ```
  static Map<String, int> parseTimeString(String timeStr) {
    final parts = timeStr.split(':');
    if (parts.length != 2) {
      throw FormatException('Invalid time format: $timeStr. Expected HH:MM');
    }

    final hour = tryParseInt(parts[0]);
    final minute = tryParseInt(parts[1]);

    if (hour == null || minute == null ||
        hour < 0 || hour > 23 ||
        minute < 0 || minute > 59) {
      throw FormatException('Invalid time values in: $timeStr');
    }

    return {'hour': hour, 'minute': minute};
  }

  /// Formats hour and minute to time string HH:MM
  ///
  /// Throws `ArgumentError` if values are out of range.
  ///
  /// Example:
  /// ```dart
  /// Converters.formatTimeString(14, 30)  // '14:30'
  /// Converters.formatTimeString(9, 5)    // '09:05'
  /// Converters.formatTimeString(25, 0)   // throws ArgumentError
  /// ```
  static String formatTimeString(int hour, int minute) {
    if (hour < 0 || hour > 23 || minute < 0 || minute > 59) {
      throw ArgumentError('Invalid time values: hour=$hour, minute=$minute');
    }
    return '${hour.toString().padLeft(2, '0')}:${minute.toString().padLeft(2, '0')}';
  }

  // ========================================================================
  // JSON DATETIME PARSING
  // ========================================================================

  /// Parses a DateTime from JSON value
  ///
  /// Accepts:
  /// - String in ISO 8601 format
  /// - int as milliseconds since epoch
  ///
  /// Throws `ArgumentError` for null or invalid types.
  ///
  /// Example:
  /// ```dart
  /// Converters.parseJsonDateTime('2025-10-15T14:30:00.000Z')  // DateTime
  /// Converters.parseJsonDateTime(1697385600000)               // DateTime
  /// ```
  static DateTime parseJsonDateTime(dynamic value) {
    if (value == null) {
      throw ArgumentError('DateTime value cannot be null');
    }

    if (value is String) {
      return DateTime.parse(value);
    }

    if (value is int) {
      return DateTime.fromMillisecondsSinceEpoch(value);
    }

    throw ArgumentError('Invalid DateTime value type: ${value.runtimeType}');
  }

  /// Safely parses a DateTime from JSON value
  ///
  /// Returns null instead of throwing for invalid values.
  ///
  /// Example:
  /// ```dart
  /// Converters.tryParseJsonDateTime('2025-10-15')  // DateTime
  /// Converters.tryParseJsonDateTime('invalid')     // null
  /// Converters.tryParseJsonDateTime(null)          // null
  /// ```
  static DateTime? tryParseJsonDateTime(dynamic value) {
    try {
      return parseJsonDateTime(value);
    } catch (e) {
      return null;
    }
  }

  // ========================================================================
  // ENUM PARSING
  // ========================================================================

  /// Parses an enum from a dynamic value
  ///
  /// Useful for parsing enums from JSON.
  ///
  /// Example:
  /// ```dart
  /// enum Status { active, inactive }
  /// final enumMap = {'active': Status.active, 'inactive': Status.inactive};
  ///
  /// Converters.parseEnum(enumMap, 'active', Status.inactive)     // Status.active
  /// Converters.parseEnum(enumMap, 'unknown', Status.inactive)    // Status.inactive
  /// Converters.parseEnum(enumMap, null, Status.inactive)         // Status.inactive
  /// ```
  static T parseEnum<T>(
    Map<String, T> enumMap,
    dynamic value,
    T defaultValue,
  ) {
    if (value == null) return defaultValue;
    final strValue = value.toString();
    return enumMap[strValue] ?? defaultValue;
  }

  // ========================================================================
  // JSON LIST PARSING
  // ========================================================================

  /// Parses a JSON list to a typed list
  ///
  /// Example:
  /// ```dart
  /// final json = [
  ///   {'id': 1, 'name': 'Item 1'},
  ///   {'id': 2, 'name': 'Item 2'},
  /// ];
  ///
  /// final items = Converters.parseJsonList(
  ///   json,
  ///   (map) => Item.fromJson(map),
  /// );
  /// ```
  static List<T> parseJsonList<T>(
    dynamic value,
    T Function(Map<String, dynamic>) fromJson,
  ) {
    if (value == null) return [];
    if (value is! List) return [];

    return value
        .where((item) => item is Map<String, dynamic>)
        .map((item) => fromJson(item as Map<String, dynamic>))
        .toList();
  }
}
```

---

## 6. lib/utils/retry_helper.dart

```dart
import 'dart:math' as math;
import 'constants.dart';

/// Retry logic utilities
///
/// Provides reusable retry logic with exponential backoff for handling
/// transient failures.
class RetryHelper {
  // Prevent instantiation
  RetryHelper._();

  /// Retries an operation with exponential backoff
  ///
  /// Parameters:
  /// - `operation`: The async operation to retry
  /// - `maxAttempts`: Maximum number of attempts (default: 3)
  /// - `initialDelay`: Initial delay between retries (default: 2 seconds)
  /// - `maxDelay`: Maximum delay between retries (default: 10 seconds)
  /// - `exponentialBackoff`: Whether to use exponential backoff (default: true)
  /// - `retryIf`: Optional predicate to determine if error should trigger retry
  ///
  /// Example:
  /// ```dart
  /// final result = await RetryHelper.retry(
  ///   operation: () => apiService.fetchData(),
  ///   maxAttempts: 3,
  ///   retryIf: (e) => e is NetworkException,
  /// );
  /// ```
  static Future<T> retry<T>({
    required Future<T> Function() operation,
    int maxAttempts = AppConstants.maxRetries,
    Duration initialDelay = AppConstants.retryDelay,
    Duration maxDelay = AppConstants.maxRetryDelay,
    bool exponentialBackoff = true,
    bool Function(Exception)? retryIf,
  }) async {
    int attempt = 0;
    Duration currentDelay = initialDelay;

    while (true) {
      try {
        return await operation();
      } catch (e) {
        attempt++;

        // Check if we've exhausted all attempts
        if (attempt >= maxAttempts) {
          rethrow;
        }

        // If there's a custom retry condition, check it
        if (retryIf != null && e is Exception && !retryIf(e)) {
          rethrow;
        }

        // Wait before retrying
        await Future.delayed(currentDelay);

        // Calculate next delay (exponential backoff)
        if (exponentialBackoff) {
          currentDelay = Duration(
            milliseconds: math.min(
              currentDelay.inMilliseconds * 2,
              maxDelay.inMilliseconds,
            ),
          );
        }
      }
    }
  }

  /// Retries an operation and returns a default value on failure
  ///
  /// Useful when you want to handle errors gracefully without throwing.
  ///
  /// Example:
  /// ```dart
  /// final result = await RetryHelper.retryWithDefault(
  ///   operation: () => apiService.fetchData(),
  ///   defaultValue: [],
  ///   maxAttempts: 3,
  /// );
  /// ```
  static Future<T> retryWithDefault<T>({
    required Future<T> Function() operation,
    required T defaultValue,
    int maxAttempts = AppConstants.maxRetries,
    Duration initialDelay = AppConstants.retryDelay,
    Duration maxDelay = AppConstants.maxRetryDelay,
    bool exponentialBackoff = true,
  }) async {
    try {
      return await retry(
        operation: operation,
        maxAttempts: maxAttempts,
        initialDelay: initialDelay,
        maxDelay: maxDelay,
        exponentialBackoff: exponentialBackoff,
      );
    } catch (e) {
      return defaultValue;
    }
  }

  /// Retries an operation with jittered exponential backoff
  ///
  /// Jitter helps prevent "thundering herd" problems when many clients
  /// retry simultaneously.
  ///
  /// Example:
  /// ```dart
  /// final result = await RetryHelper.retryWithJitter(
  ///   operation: () => apiService.fetchData(),
  /// );
  /// ```
  static Future<T> retryWithJitter<T>({
    required Future<T> Function() operation,
    int maxAttempts = AppConstants.maxRetries,
    Duration initialDelay = AppConstants.retryDelay,
    Duration maxDelay = AppConstants.maxRetryDelay,
    bool Function(Exception)? retryIf,
  }) async {
    int attempt = 0;
    Duration currentDelay = initialDelay;
    final random = math.Random();

    while (true) {
      try {
        return await operation();
      } catch (e) {
        attempt++;

        if (attempt >= maxAttempts) {
          rethrow;
        }

        if (retryIf != null && e is Exception && !retryIf(e)) {
          rethrow;
        }

        // Add jitter (randomness) to delay
        final jitter = random.nextDouble(); // 0.0 to 1.0
        final jitteredDelay = Duration(
          milliseconds: (currentDelay.inMilliseconds * jitter).round(),
        );

        await Future.delayed(jitteredDelay);

        // Exponential backoff for next attempt
        currentDelay = Duration(
          milliseconds: math.min(
            currentDelay.inMilliseconds * 2,
            maxDelay.inMilliseconds,
          ),
        );
      }
    }
  }
}
```

---

## Migration Examples

### Example 1: Migrating Email Validation

**Before:**
```dart
// user_authentication_service.dart
bool isValidEmail(String email) {
  return RegExp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
      .hasMatch(email);
}

// Usage
if (isValidEmail(email)) {
  // ...
}
```

**After:**
```dart
// Add import at top
import 'package:zodiac_app/utils/validators.dart';

// Remove isValidEmail method entirely

// Usage
if (Validators.isValidEmail(email)) {
  // ...
}
```

---

### Example 2: Migrating Zodiac Sign Validation

**Before:**
```dart
// isolate_service.dart
static bool _isValidSign(String sign) {
  const validSigns = [
    'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces',
  ];
  return validSigns.contains(sign.toLowerCase());
}

// Usage
if (_isValidSign(sign)) {
  // ...
}
```

**After:**
```dart
// Add import at top
import 'package:zodiac_app/utils/validators.dart';

// Remove _isValidSign method entirely

// Usage
if (Validators.isValidZodiacSign(sign)) {
  // ...
}
```

---

### Example 3: Migrating Unsafe Parsing

**Before:**
```dart
// zodiac_service.dart (UNSAFE - can throw exception)
final hour = int.parse(birthTime.split(':')[0]);
final minute = int.parse(birthTime.split(':')[1]);
```

**After:**
```dart
// Add import at top
import 'package:zodiac_app/utils/converters.dart';

// SAFE - handles errors gracefully
try {
  final time = Converters.parseTimeString(birthTime);
  final hour = time['hour']!;
  final minute = time['minute']!;
  // ...
} catch (e) {
  // Handle invalid time format
  logger.warning('Invalid birth time format: $birthTime');
  return null;
}
```

---

### Example 4: Migrating Backend URL

**Before:**
```dart
// weekly_horoscope_service.dart
static const String _backendUrl =
    'https://zodiac-backend-api-production-8ded.up.railway.app';

final url = '$_backendUrl/api/weekly-horoscope';
```

**After:**
```dart
// Add import at top
import 'package:zodiac_app/utils/constants.dart';

// Remove _backendUrl constant

final url = '${AppConstants.baseUrl}/api/weekly-horoscope';
// Or use the helper:
final url = AppConstants.weeklyHoroscopeEndpoint;
```

---

### Example 5: Migrating Retry Logic

**Before:**
```dart
// receipt_validation_service.dart
static const int _maxRetries = 3;

int retryCount = 0;
while (retryCount < _maxRetries) {
  try {
    final result = await _validateWithServer(receipt);
    return result;
  } catch (e) {
    retryCount++;
    if (retryCount >= _maxRetries) {
      throw e;
    }
    await Future.delayed(Duration(seconds: 2 * retryCount));
  }
}
```

**After:**
```dart
// Add import at top
import 'package:zodiac_app/utils/retry_helper.dart';

// Replace entire retry loop with:
return await RetryHelper.retry(
  operation: () => _validateWithServer(receipt),
  maxAttempts: 3,
  retryIf: (e) => e is NetworkException || e is TimeoutException,
);
```

---

## Testing Examples

### validators_test.dart

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:zodiac_app/utils/validators.dart';

void main() {
  group('Validators - Email', () {
    test('validates correct email formats', () {
      expect(Validators.isValidEmail('user@example.com'), true);
      expect(Validators.isValidEmail('test.user@example.co.uk'), true);
      expect(Validators.isValidEmail('user+tag@example.com'), true);
    });

    test('rejects invalid email formats', () {
      expect(Validators.isValidEmail('invalid'), false);
      expect(Validators.isValidEmail('@example.com'), false);
      expect(Validators.isValidEmail('user@'), false);
      expect(Validators.isValidEmail(''), false);
      expect(Validators.isValidEmail(null), false);
    });

    test('handles whitespace in emails', () {
      expect(Validators.isValidEmail('  user@example.com  '), true);
    });
  });

  group('Validators - Zodiac Signs', () {
    test('validates all zodiac signs', () {
      for (final sign in Validators.validZodiacSigns) {
        expect(Validators.isValidZodiacSign(sign), true);
      }
    });

    test('is case insensitive', () {
      expect(Validators.isValidZodiacSign('ARIES'), true);
      expect(Validators.isValidZodiacSign('Aries'), true);
      expect(Validators.isValidZodiacSign('aries'), true);
    });

    test('handles whitespace', () {
      expect(Validators.isValidZodiacSign('  aries  '), true);
    });

    test('rejects invalid signs', () {
      expect(Validators.isValidZodiacSign('invalid'), false);
      expect(Validators.isValidZodiacSign(''), false);
      expect(Validators.isValidZodiacSign(null), false);
    });
  });

  group('Validators - Birth Date', () {
    test('validates normal birth dates', () {
      final birthDate = DateTime(1990, 5, 15);
      final result = Validators.validateBirthDate(birthDate);
      expect(result.isValid, true);
    });

    test('rejects future dates', () {
      final futureDate = DateTime.now().add(Duration(days: 1));
      final result = Validators.validateBirthDate(futureDate);
      expect(result.isValid, false);
      expect(result.errorMessage, contains('future'));
    });

    test('rejects dates too far in the past', () {
      final tooOld = DateTime.now().subtract(Duration(days: 365 * 150));
      final result = Validators.validateBirthDate(tooOld);
      expect(result.isValid, false);
    });

    test('rejects null dates', () {
      final result = Validators.validateBirthDate(null);
      expect(result.isValid, false);
      expect(result.errorMessage, contains('required'));
    });
  });
}
```

---

**Note**: Este código está listo para usar. Solo copia el contenido de cada sección al archivo correspondiente y ejecuta `dart analyze` para verificar que no hay errores.
