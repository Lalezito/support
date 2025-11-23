# COMPREHENSIVE TESTING CHECKLIST
## Zodiac App - 100+ Test Cases
### Date: 2025-01-23
### Version: 1.0
### Coverage: All Critical User Flows

---

## TEST EXECUTION LEGEND

```
Status Indicators:
[ ] Not Started
[⏳] In Progress
[✅] Passed
[❌] Failed
[⚠️ ] Partial/Flaky
[⏭️ ] Skipped
[🔄] Needs Retest

Priority Levels:
P0 - BLOCKER: Must pass before any release
P1 - CRITICAL: Must pass before full launch
P2 - HIGH: Should pass before full launch
P3 - MEDIUM: Can be fixed post-launch
P4 - LOW: Nice to have
```

---

## CATEGORY 1: AUTHENTICATION & USER IDENTITY (15 tests)

### 1.1 User Registration

**TC-001: Email Registration - Happy Path** [P0]
```
[ ] Preconditions: Fresh app install, no existing account
[ ] Steps:
    1. Open app
    2. Navigate to Register screen
    3. Enter valid email (test@example.com)
    4. Enter strong password (Test123!@#)
    5. Accept terms and privacy policy
    6. Tap "Register"
[ ] Expected:
    - Registration succeeds
    - Verification email sent
    - User logged in automatically
    - Home screen displayed
    - Analytics event "user_registered" fired
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-002: Email Registration - Duplicate Email** [P0]
```
[ ] Preconditions: Account exists for test@example.com
[ ] Steps:
    1. Attempt to register with test@example.com
[ ] Expected:
    - Error message: "Email already in use"
    - User remains on registration screen
    - Can try different email
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-003: Email Registration - Weak Password** [P1]
```
[ ] Preconditions: Fresh registration attempt
[ ] Steps:
    1. Enter email
    2. Enter weak password (e.g., "123")
    3. Tap "Register"
[ ] Expected:
    - Error message: "Password too weak"
    - Password requirements shown
    - Registration blocked
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-004: Email Registration - Invalid Email Format** [P1]
```
[ ] Preconditions: Registration screen
[ ] Steps:
    1. Enter invalid email (e.g., "notanemail")
    2. Enter valid password
    3. Tap "Register"
[ ] Expected:
    - Error message: "Invalid email format"
    - Registration blocked
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-005: Email Registration - Network Error** [P1]
```
[ ] Preconditions: Device in airplane mode
[ ] Steps:
    1. Attempt registration with valid credentials
[ ] Expected:
    - Loading spinner shows
    - After timeout: "Network error, please try again"
    - Registration data preserved
    - User can retry when online
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 1.2 User Login

**TC-006: Login - Happy Path** [P0]
```
[ ] Preconditions: Valid account exists
[ ] Steps:
    1. Open app
    2. Navigate to Login screen
    3. Enter valid email
    4. Enter correct password
    5. Tap "Login"
[ ] Expected:
    - Login succeeds
    - User redirected to home screen
    - Previous session restored
    - Analytics event "user_logged_in" fired
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-007: Login - Wrong Password** [P0]
```
[ ] Preconditions: Valid account exists
[ ] Steps:
    1. Enter correct email
    2. Enter wrong password
    3. Tap "Login"
[ ] Expected:
    - Error message: "Incorrect password"
    - Login blocked
    - Can retry
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-008: Login - Non-existent Account** [P1]
```
[ ] Preconditions: Email not registered
[ ] Steps:
    1. Enter non-existent email
    2. Enter any password
    3. Tap "Login"
[ ] Expected:
    - Error message: "No account found with this email"
    - Suggestion to register
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-009: Login - Account Locked** [P2]
```
[ ] Preconditions: Account locked due to failed attempts
[ ] Steps:
    1. Attempt login
[ ] Expected:
    - Error message: "Account temporarily locked"
    - Unlock instructions displayed
    - Cannot login until unlock period
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-010: Anonymous Auth - First Launch** [P1]
```
[ ] Preconditions: Fresh app install
[ ] Steps:
    1. Open app
    2. Skip registration
[ ] Expected:
    - Anonymous user created automatically
    - User ID generated
    - Can access free features
    - Prompted to register for premium features
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 1.3 Password Reset

**TC-011: Password Reset - Happy Path** [P1]
```
[ ] Preconditions: Valid account exists
[ ] Steps:
    1. Tap "Forgot Password"
    2. Enter registered email
    3. Tap "Send Reset Email"
    4. Check email inbox
    5. Click reset link
    6. Enter new password
    7. Confirm new password
[ ] Expected:
    - Reset email received within 2 minutes
    - Reset link valid for 1 hour
    - Password successfully changed
    - Can login with new password
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-012: Password Reset - Invalid Email** [P2]
```
[ ] Preconditions: Email not registered
[ ] Steps:
    1. Request password reset for non-existent email
[ ] Expected:
    - Generic message: "If email exists, reset link sent"
    - (No account enumeration vulnerability)
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-013: Password Reset - Expired Link** [P2]
```
[ ] Preconditions: Password reset link generated > 1 hour ago
[ ] Steps:
    1. Click expired reset link
[ ] Expected:
    - Error message: "Reset link expired"
    - Option to request new link
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 1.4 Logout & Session Management

**TC-014: Logout - Clean Logout** [P0]
```
[ ] Preconditions: User logged in
[ ] Steps:
    1. Navigate to Settings
    2. Tap "Logout"
    3. Confirm logout
[ ] Expected:
    - User logged out
    - Redirected to login screen
    - Local data cleared (except anonymous data)
    - Session token invalidated
    - Analytics event "user_logged_out" fired
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-015: Session Expiry - Auto Re-auth** [P1]
```
[ ] Preconditions: User logged in, token expires
[ ] Steps:
    1. Use app after token expiry (simulate by waiting/manipulating time)
[ ] Expected:
    - Token automatically refreshed
    - User remains logged in
    - No interruption to UX
[ ] Actual:
[ ] Status:
[ ] Notes:
```

---

## CATEGORY 2: PREMIUM PURCHASE FLOW (20 tests)

### 2.1 Purchase - Cosmic Tier (Monthly)

**TC-016: Purchase Cosmic - Happy Path** [P0]
```
[ ] Preconditions: Free user, valid payment method
[ ] Steps:
    1. Navigate to Premium screen
    2. Select "Cosmic" tier
    3. Tap "Subscribe Now"
    4. Confirm with Touch ID/Face ID
    5. Payment completes
[ ] Expected:
    - Purchase sheet appears
    - Price displayed correctly ($9.99/month)
    - Payment processes
    - Success message shown
    - Premium features unlock immediately
    - Receipt sent to email
    - RevenueCat subscription created
    - Analytics event "purchase_success" fired
    - StateNotifier shows success state
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-017: Purchase Cosmic - Payment Cancelled** [P0]
```
[ ] Preconditions: Free user on premium screen
[ ] Steps:
    1. Select Cosmic tier
    2. Tap "Subscribe"
    3. Cancel payment sheet
[ ] Expected:
    - Payment cancelled
    - User returns to premium screen
    - Paywall still displayed
    - No charge made
    - Analytics event "purchase_cancelled" fired
    - StateNotifier resets to idle
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-018: Purchase Cosmic - Payment Failed** [P0]
```
[ ] Preconditions: Free user, invalid payment method
[ ] Steps:
    1. Attempt purchase with declined card
[ ] Expected:
    - Payment fails
    - Error message: "Payment failed, please try again"
    - User can retry with different payment method
    - No partial unlock of premium features
    - Analytics event "purchase_failed" fired
    - StateNotifier shows error state
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-019: Purchase Cosmic - Network Error During Purchase** [P1]
```
[ ] Preconditions: Start purchase, then enable airplane mode
[ ] Steps:
    1. Initiate purchase
    2. Enable airplane mode mid-transaction
    3. Complete payment (if possible)
    4. Re-enable network
[ ] Expected:
    - App shows "Verifying purchase..." loading state
    - When network restored: Receipt validated
    - Premium unlocks correctly
    - No duplicate charges
    - StateNotifier handles gracefully
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-020: Purchase Cosmic - Already Subscribed** [P1]
```
[ ] Preconditions: User already has active Cosmic subscription
[ ] Steps:
    1. Navigate to Premium screen
    2. Attempt to purchase Cosmic again
[ ] Expected:
    - Message: "You already have an active subscription"
    - "Manage Subscription" button shown
    - Cannot purchase duplicate
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 2.2 Purchase - Stellar Tier (Annual)

**TC-021: Purchase Stellar - Happy Path** [P0]
```
[ ] Preconditions: Free user, valid payment method
[ ] Steps:
    1. Navigate to Premium screen
    2. Select "Stellar" tier (annual)
    3. Confirm purchase ($59.99/year)
[ ] Expected:
    - Correct price displayed
    - Payment succeeds
    - Premium features unlock
    - Analytics shows annual tier
    - Subscription renews in 1 year
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-022: Purchase Stellar - Switch from Cosmic** [P1]
```
[ ] Preconditions: User has active Cosmic (monthly) subscription
[ ] Steps:
    1. Navigate to Premium screen
    2. Select "Stellar" tier (annual)
    3. Confirm upgrade
[ ] Expected:
    - App shows upgrade flow
    - Pro-rated credit applied
    - Subscription switches to annual
    - RevenueCat handles migration
    - No loss of premium features during switch
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-023: Purchase Stellar - Free Trial** [P2]
```
[ ] Preconditions: Eligible for free trial
[ ] Steps:
    1. Select Stellar with free trial
    2. Complete purchase
[ ] Expected:
    - Trial starts immediately
    - Premium unlocked during trial
    - No charge until trial ends (7 days)
    - Reminder notification before trial ends
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 2.3 Purchase - HR Professional Tier

**TC-024: Purchase HR Pro - Happy Path** [P1]
```
[ ] Preconditions: Free user
[ ] Steps:
    1. Select HR Professional tier ($19.99/month)
    2. Complete purchase
[ ] Expected:
    - Payment succeeds
    - Advanced features unlock
    - HR-specific content accessible
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-025: Purchase HR Pro - Downgrade from Stellar** [P2]
```
[ ] Preconditions: User has Stellar annual subscription
[ ] Steps:
    1. Attempt to "downgrade" to HR Pro (different feature set)
[ ] Expected:
    - App explains feature differences
    - Confirms user intent
    - Manages subscription change
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 2.4 Restore Purchases

**TC-026: Restore Purchases - Active Subscription** [P0]
```
[ ] Preconditions:
    - User has active subscription (purchased on different device)
    - Currently signed in to same Apple ID
    - App shows as "Free" user
[ ] Steps:
    1. Navigate to Premium screen
    2. Tap "Restore Purchases"
[ ] Expected:
    - Loading indicator shows
    - Subscription detected from RevenueCat
    - Premium features unlock immediately
    - Success message: "Subscription restored!"
    - Premium UI displayed
    - Analytics event "restore_success" fired
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-027: Restore Purchases - Expired Subscription** [P1]
```
[ ] Preconditions: User had subscription that expired
[ ] Steps:
    1. Tap "Restore Purchases"
[ ] Expected:
    - Message: "No active subscription found"
    - Paywall remains
    - Option to subscribe shown
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-028: Restore Purchases - Never Purchased** [P1]
```
[ ] Preconditions: User never bought premium
[ ] Steps:
    1. Tap "Restore Purchases"
[ ] Expected:
    - Message: "No purchases to restore"
    - No premium unlock
    - User remains on paywall
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-029: Restore Purchases - Multiple Devices Sync** [P1]
```
[ ] Preconditions:
    - Purchase on Device A
    - Sign in to same account on Device B
[ ] Steps:
    1. On Device B, tap "Restore Purchases"
[ ] Expected:
    - Subscription syncs via RevenueCat
    - Premium unlocks on Device B
    - Both devices show premium status
    - No duplicate charges
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 2.5 Subscription Management

**TC-030: Cancel Subscription - iOS Settings** [P1]
```
[ ] Preconditions: Active subscription
[ ] Steps:
    1. Open iOS Settings → Apple ID → Subscriptions
    2. Cancel Zodiac App subscription
    3. Return to app
[ ] Expected:
    - App detects cancellation (may take up to 24h)
    - Premium remains active until end of billing period
    - After period: Premium features locked
    - User notified of cancellation
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-031: Subscription Renewal - Auto-Renew Success** [P1]
```
[ ] Preconditions: Subscription approaching renewal date
[ ] Steps:
    1. Wait for renewal date (or simulate)
[ ] Expected:
    - Auto-renew succeeds
    - Premium continues uninterrupted
    - Receipt generated
    - RevenueCat updated
    - No user action required
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-032: Subscription Renewal - Payment Failed** [P1]
```
[ ] Preconditions: Renewal date, invalid payment method
[ ] Steps:
    1. Renewal attempt with expired card
[ ] Expected:
    - Renewal fails
    - User notified: "Update payment method"
    - Grace period starts (if configured)
    - Premium features remain for grace period
    - After grace period: Downgrade to free
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-033: Refund Handling** [P2]
```
[ ] Preconditions: User requests refund via Apple
[ ] Steps:
    1. User gets refund from Apple
    2. App detects refund via RevenueCat webhook
[ ] Expected:
    - Premium features revoked immediately
    - User downgraded to free tier
    - Access to premium content blocked
    - Analytics event "refund_issued" fired
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 2.6 Race Conditions & Edge Cases

**TC-034: Rapid Purchase Attempts** [P1]
```
[ ] Preconditions: Free user
[ ] Steps:
    1. Tap "Subscribe" button multiple times rapidly
[ ] Expected:
    - Only one purchase flow initiates
    - Subsequent taps ignored
    - No duplicate charges
    - StateNotifier prevents race condition
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-035: Purchase During App Backgrounding** [P2]
```
[ ] Preconditions: Purchase in progress
[ ] Steps:
    1. Initiate purchase
    2. Background app (home button)
    3. Return to app
[ ] Expected:
    - Purchase continues or gracefully retries
    - No stuck "loading" state
    - Premium unlocks correctly
[ ] Actual:
[ ] Status:
[ ] Notes:
```

---

## CATEGORY 3: COSMIC COACH FEATURES (15 tests)

### 3.1 Cosmic Coach Onboarding

**TC-036: Cosmic Coach - First Time Onboarding** [P1]
```
[ ] Preconditions: New user, never used Cosmic Coach
[ ] Steps:
    1. Navigate to Cosmic Coach tab
[ ] Expected:
    - Onboarding screen displayed
    - Feature explanation shown
    - "Get Started" button present
    - Analytics event "cosmic_coach_onboarding_shown"
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-037: Cosmic Coach - Skip Onboarding** [P2]
```
[ ] Preconditions: Onboarding screen
[ ] Steps:
    1. Tap "Skip" button
[ ] Expected:
    - Onboarding dismissed
    - User taken directly to chat
    - Can re-access onboarding from settings
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 3.2 Goal Setting

**TC-038: Create Goal - Happy Path** [P1]
```
[ ] Preconditions: Cosmic Coach unlocked (premium or trial)
[ ] Steps:
    1. Tap "Set New Goal"
    2. Select category (e.g., "Career")
    3. Enter goal description
    4. Set timeline
    5. Tap "Create Goal"
[ ] Expected:
    - Goal created successfully
    - Appears in goals list
    - Analytics event "goal_created"
    - AI generates personalized suggestions
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-039: Create Goal - Empty Description** [P2]
```
[ ] Preconditions: Goal creation screen
[ ] Steps:
    1. Leave goal description empty
    2. Tap "Create"
[ ] Expected:
    - Validation error: "Please describe your goal"
    - Creation blocked
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-040: Edit Goal** [P2]
```
[ ] Preconditions: Existing goal created
[ ] Steps:
    1. Select goal from list
    2. Tap "Edit"
    3. Change description/timeline
    4. Save changes
[ ] Expected:
    - Changes saved
    - Goal updated in list
    - Version history maintained
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-041: Delete Goal** [P2]
```
[ ] Preconditions: Existing goal
[ ] Steps:
    1. Swipe to delete or tap delete icon
    2. Confirm deletion
[ ] Expected:
    - Goal removed from list
    - Confirmation dialog shown
    - Analytics event "goal_deleted"
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-042: Mark Goal Complete** [P1]
```
[ ] Preconditions: Active goal in progress
[ ] Steps:
    1. Tap goal
    2. Mark as "Completed"
[ ] Expected:
    - Goal moved to "Completed" section
    - Congratulatory message shown
    - Analytics event "goal_completed"
    - Achievement unlocked (if applicable)
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 3.3 AI Chat Interaction

**TC-043: Send Message - Happy Path** [P1]
```
[ ] Preconditions: Cosmic Coach chat screen
[ ] Steps:
    1. Type message "What is my horoscope for today?"
    2. Tap Send
[ ] Expected:
    - Message appears in chat
    - Loading indicator shows
    - AI response received within 10s
    - Response formatted correctly
    - Analytics event "cosmic_coach_message_sent"
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-044: Send Message - Network Error** [P1]
```
[ ] Preconditions: Device in airplane mode
[ ] Steps:
    1. Send message
[ ] Expected:
    - Error message: "No internet connection"
    - Message saved locally
    - Can retry when online
    - No message loss
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-045: Send Message - Empty Message** [P2]
```
[ ] Preconditions: Chat screen
[ ] Steps:
    1. Type nothing
    2. Tap Send
[ ] Expected:
    - Send button disabled until text entered
    - OR error message "Please enter a message"
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-046: Conversation History** [P2]
```
[ ] Preconditions: Multiple chat sessions
[ ] Steps:
    1. Navigate to "Conversation History"
[ ] Expected:
    - All past conversations listed
    - Can tap to view full conversation
    - Messages persisted across app restarts
    - Sorted by date (newest first)
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-047: Delete Conversation** [P2]
```
[ ] Preconditions: Conversation history with items
[ ] Steps:
    1. Swipe to delete a conversation
    2. Confirm deletion
[ ] Expected:
    - Conversation removed
    - Data deleted from Firebase
    - Analytics event "conversation_deleted"
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 3.4 Biorhythm Features

**TC-048: View Biorhythm Chart** [P2]
```
[ ] Preconditions: User has birthdate set
[ ] Steps:
    1. Navigate to Biorhythm screen
[ ] Expected:
    - Chart loads within 2s
    - Shows physical, emotional, intellectual cycles
    - Current date highlighted
    - Chart interactive (can scroll)
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-049: Biorhythm without Birthdate** [P2]
```
[ ] Preconditions: User has NOT set birthdate
[ ] Steps:
    1. Navigate to Biorhythm screen
[ ] Expected:
    - Prompt: "Set your birthdate to view biorhythm"
    - "Set Birthdate" button shown
    - Redirects to birth data collection
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-050: Biorhythm Multi-language** [P2]
```
[ ] Preconditions: User in non-English language
[ ] Steps:
    1. Change language to French/German/Spanish
    2. View biorhythm messages
[ ] Expected:
    - Messages displayed in selected language
    - Chart labels translated
    - No hardcoded English text
[ ] Actual:
[ ] Status:
[ ] Notes:
```

---

## CATEGORY 4: HOROSCOPE FEATURES (10 tests)

### 4.1 Daily Horoscope

**TC-051: View Daily Horoscope - Happy Path** [P0]
```
[ ] Preconditions: User has zodiac sign selected
[ ] Steps:
    1. Open app
    2. Navigate to Home screen
[ ] Expected:
    - Today's horoscope displayed
    - Correct zodiac sign shown
    - Content loads within 3s
    - Can refresh to reload
    - Analytics event "daily_horoscope_viewed"
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-052: Daily Horoscope - No Zodiac Sign** [P1]
```
[ ] Preconditions: New user, no sign selected
[ ] Steps:
    1. Open app
[ ] Expected:
    - Prompt: "Select your zodiac sign"
    - Redirects to sign selection screen
    - After selection: Horoscope loads
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-053: Daily Horoscope - Offline Caching** [P2]
```
[ ] Preconditions: Device online, horoscope loaded
[ ] Steps:
    1. View today's horoscope
    2. Enable airplane mode
    3. Close and reopen app
[ ] Expected:
    - Cached horoscope still visible
    - Indicator shown: "Offline - showing cached content"
    - No crash
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-054: Daily Horoscope - Refresh** [P2]
```
[ ] Preconditions: Horoscope displayed
[ ] Steps:
    1. Pull to refresh
[ ] Expected:
    - Loading indicator shown
    - New content fetched (if available)
    - Analytics event "horoscope_refreshed"
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 4.2 Weekly & Monthly Horoscopes

**TC-055: View Weekly Horoscope** [P1]
```
[ ] Preconditions: User on horoscope screen
[ ] Steps:
    1. Switch to "Weekly" tab
[ ] Expected:
    - Weekly horoscope loads
    - Date range shown (e.g., "Dec 18-24")
    - Content relevant to current week
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-056: View Monthly Horoscope** [P1]
```
[ ] Preconditions: User on horoscope screen
[ ] Steps:
    1. Switch to "Monthly" tab
[ ] Expected:
    - Monthly horoscope loads
    - Current month shown (e.g., "December 2025")
    - Content relevant to current month
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 4.3 Horoscope Notifications

**TC-057: Enable Daily Notifications** [P2]
```
[ ] Preconditions: Notifications permission granted
[ ] Steps:
    1. Go to Settings
    2. Toggle "Daily Horoscope Notifications" ON
    3. Select preferred time (e.g., 9:00 AM)
[ ] Expected:
    - Setting saved
    - Next day at 9:00 AM: Notification received
    - Tapping notification opens app to horoscope
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-058: Disable Daily Notifications** [P2]
```
[ ] Preconditions: Notifications enabled
[ ] Steps:
    1. Toggle notifications OFF
[ ] Expected:
    - No more notifications received
    - Setting persists across app restarts
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 4.4 Multi-language Horoscopes

**TC-059: Horoscope in Spanish** [P1]
```
[ ] Preconditions: None
[ ] Steps:
    1. Change app language to Spanish
    2. View daily horoscope
[ ] Expected:
    - Horoscope text in Spanish
    - All UI labels in Spanish
    - No English text visible
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-060: Horoscope in French** [P1]
```
[ ] Preconditions: None
[ ] Steps:
    1. Change app language to French
    2. View weekly horoscope
[ ] Expected:
    - Content in French
    - Date formatting French-style
    - All strings translated
[ ] Actual:
[ ] Status:
[ ] Notes:
```

---

## CATEGORY 5: COMPATIBILITY FEATURES (8 tests)

### 5.1 Compatibility Calculation

**TC-061: Calculate Compatibility - Two Signs** [P1]
```
[ ] Preconditions: User's sign selected (e.g., Aries)
[ ] Steps:
    1. Navigate to Compatibility screen
    2. Select partner's sign (e.g., Leo)
    3. Tap "Calculate"
[ ] Expected:
    - Compatibility score shown (e.g., 85%)
    - Detailed breakdown displayed
    - Strengths and challenges listed
    - Analytics event "compatibility_calculated"
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-062: Compatibility - Save Result** [P2]
```
[ ] Preconditions: Compatibility calculated
[ ] Steps:
    1. Tap "Save Result"
    2. Name the relationship (optional)
[ ] Expected:
    - Result saved to "Saved Compatibilities"
    - Can view later
    - Can share result
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-063: Compatibility - Share Result** [P2]
```
[ ] Preconditions: Compatibility result displayed
[ ] Steps:
    1. Tap "Share" button
    2. Select share method (e.g., Messages)
[ ] Expected:
    - Share sheet appears
    - Image/text prepared for sharing
    - Analytics event "compatibility_shared"
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 5.2 Advanced Compatibility (Premium)

**TC-064: Advanced Compatibility - Premium User** [P2]
```
[ ] Preconditions: User has premium subscription
[ ] Steps:
    1. Navigate to Compatibility screen
    2. Tap "Advanced Analysis"
[ ] Expected:
    - Advanced features unlocked
    - Detailed planetary analysis shown
    - Additional insights available
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-065: Advanced Compatibility - Free User** [P1]
```
[ ] Preconditions: User is free tier
[ ] Steps:
    1. Tap "Advanced Analysis"
[ ] Expected:
    - Paywall displayed
    - "Upgrade to Premium" button shown
    - Basic compatibility still accessible
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 5.3 Birth Chart Integration

**TC-066: View Birth Chart** [P2]
```
[ ] Preconditions: User has birthdate, time, location set
[ ] Steps:
    1. Navigate to "Birth Chart" screen
[ ] Expected:
    - Chart renders correctly
    - All planetary positions shown
    - Interactive elements work
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-067: Birth Chart without Complete Data** [P2]
```
[ ] Preconditions: Birthdate set, but no time/location
[ ] Steps:
    1. Navigate to Birth Chart
[ ] Expected:
    - Prompt: "Complete your birth data for accurate chart"
    - "Add Birth Time" and "Add Location" buttons shown
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-068: Share Birth Chart** [P2]
```
[ ] Preconditions: Birth chart displayed
[ ] Steps:
    1. Tap "Share Chart"
[ ] Expected:
    - Chart exported as image
    - Share sheet appears
    - Can share to social media
[ ] Actual:
[ ] Status:
[ ] Notes:
```

---

## CATEGORY 6: SETTINGS & PREFERENCES (10 tests)

### 6.1 Language Settings

**TC-069: Change Language - English to Spanish** [P1]
```
[ ] Preconditions: App in English
[ ] Steps:
    1. Go to Settings
    2. Tap "Language"
    3. Select "Español"
    4. Confirm change
[ ] Expected:
    - All UI immediately updates to Spanish
    - Content reloads in Spanish
    - Setting persists across app restarts
    - No crash or UI glitches
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-070: Change Language - All 6 Languages** [P1]
```
[ ] Preconditions: None
[ ] Steps:
    1. Cycle through all 6 languages (EN, ES, FR, DE, IT, PT)
[ ] Expected:
    - All languages render correctly
    - No missing translations
    - No layout issues
    - All features work in all languages
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 6.2 Notification Settings

**TC-071: Enable/Disable All Notifications** [P2]
```
[ ] Preconditions: Settings screen
[ ] Steps:
    1. Toggle "All Notifications" OFF
[ ] Expected:
    - All notification toggles disabled
    - No notifications received
    - Can re-enable anytime
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-072: Notification Time Preferences** [P2]
```
[ ] Preconditions: Notifications enabled
[ ] Steps:
    1. Set "Preferred Time" to 10:00 AM
    2. Save changes
[ ] Expected:
    - Notifications arrive at 10:00 AM daily
    - Time persists across restarts
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 6.3 Privacy Settings

**TC-073: Delete Account** [P2]
```
[ ] Preconditions: User logged in
[ ] Steps:
    1. Go to Settings → Privacy
    2. Tap "Delete Account"
    3. Confirm deletion (with password)
[ ] Expected:
    - Confirmation dialog shown
    - All user data deleted from Firebase
    - User logged out
    - Cannot login with deleted account
    - GDPR compliance
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-074: Export User Data** [P2]
```
[ ] Preconditions: User logged in
[ ] Steps:
    1. Go to Settings → Privacy
    2. Tap "Export My Data"
[ ] Expected:
    - Data export initiated
    - JSON file emailed to user
    - Contains all user data
    - GDPR compliance
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 6.4 Theme & Appearance

**TC-075: Dark Mode Toggle** [P2]
```
[ ] Preconditions: App in light mode
[ ] Steps:
    1. Go to Settings
    2. Toggle "Dark Mode" ON
[ ] Expected:
    - App immediately switches to dark theme
    - All screens render correctly in dark mode
    - Setting persists
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-076: Auto Theme (System)** [P2]
```
[ ] Preconditions: None
[ ] Steps:
    1. Select "Follow System"
    2. Change device theme
[ ] Expected:
    - App theme matches device theme
    - Updates automatically when device theme changes
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 6.5 Birth Data Management

**TC-077: Edit Birth Data** [P2]
```
[ ] Preconditions: Birth data already set
[ ] Steps:
    1. Go to Settings → Birth Data
    2. Tap "Edit"
    3. Change birthdate/time/location
    4. Save changes
[ ] Expected:
    - Changes saved
    - Horoscope recalculated
    - Birth chart updated
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-078: Delete Birth Data** [P2]
```
[ ] Preconditions: Birth data set
[ ] Steps:
    1. Tap "Delete Birth Data"
    2. Confirm deletion
[ ] Expected:
    - Birth data cleared
    - Features requiring birth data show prompts again
    - No crash
[ ] Actual:
[ ] Status:
[ ] Notes:
```

---

## CATEGORY 7: PERFORMANCE & STABILITY (12 tests)

### 7.1 App Startup Performance

**TC-079: Cold Start Time - Optimized** [P1]
```
[ ] Preconditions: App not in memory, device restarted
[ ] Steps:
    1. Launch app
    2. Measure time to interactive
[ ] Expected:
    - Time to interactive < 3.7s (with Quick Win 1)
    - Target: < 2.0s (with full optimization)
    - Splash screen shows immediately
    - No ANR (Application Not Responding)
[ ] Actual Time:
[ ] Status:
[ ] Notes:
```

**TC-080: Warm Start Time** [P2]
```
[ ] Preconditions: App in memory (backgrounded)
[ ] Steps:
    1. Resume app from background
[ ] Expected:
    - Resume time < 1.5s
    - State preserved
    - No reload required
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-081: Memory Usage - Normal Operation** [P2]
```
[ ] Preconditions: App running
[ ] Steps:
    1. Navigate through all main screens
    2. Monitor memory usage (Xcode Instruments/Android Profiler)
[ ] Expected:
    - Average memory < 120 MB (target: < 80 MB)
    - No memory leaks detected
    - Memory released when backgrounded
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-082: Memory Usage - Premium Screen** [P1]
```
[ ] Preconditions: Navigate to premium screen
[ ] Steps:
    1. Monitor memory while on premium screen
[ ] Expected:
    - Memory < 180 MB (target: < 120 MB)
    - No steady increase (leak)
    - Memory drops when leaving screen
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 7.2 Network Performance

**TC-083: API Response Time** [P2]
```
[ ] Preconditions: Good network connection
[ ] Steps:
    1. Measure time for horoscope API call
[ ] Expected:
    - Response time < 1000ms (average 850ms)
    - 95th percentile < 1500ms
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-084: Offline Mode - Graceful Degradation** [P1]
```
[ ] Preconditions: None
[ ] Steps:
    1. Enable airplane mode
    2. Use app features
[ ] Expected:
    - Cached content shown
    - "Offline" indicator visible
    - No crashes
    - Clear error messages
    - Can queue actions for when online
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 7.3 UI Performance

**TC-085: Scroll Performance - Long Lists** [P2]
```
[ ] Preconditions: Conversation history with 50+ items
[ ] Steps:
    1. Scroll rapidly through list
[ ] Expected:
    - 60 FPS maintained
    - No jank or dropped frames
    - Smooth scrolling
[ ] Actual FPS:
[ ] Status:
[ ] Notes:
```

**TC-086: Animation Smoothness** [P2]
```
[ ] Preconditions: None
[ ] Steps:
    1. Navigate between screens
    2. Observe transitions
[ ] Expected:
    - All animations 60 FPS
    - No stuttering
    - Consistent timing
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 7.4 Crash Resistance

**TC-087: No Crashes - Main User Flows** [P0]
```
[ ] Preconditions: None
[ ] Steps:
    1. Execute all critical user flows
    2. Monitor for crashes
[ ] Expected:
    - Zero crashes
    - Crash-free rate > 99.5%
    - All errors handled gracefully
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-088: Background/Foreground Cycling** [P2]
```
[ ] Preconditions: App running
[ ] Steps:
    1. Background app
    2. Wait 5 seconds
    3. Foreground app
    4. Repeat 20 times
[ ] Expected:
    - No crashes
    - State preserved
    - No memory leaks
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-089: Low Memory Conditions** [P2]
```
[ ] Preconditions: Simulate low memory
[ ] Steps:
    1. Open multiple large apps
    2. Return to Zodiac app
[ ] Expected:
    - App handles low memory warning
    - Caches cleared if needed
    - No crash
    - Graceful recovery
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-090: Network Timeout Handling** [P2]
```
[ ] Preconditions: Simulate slow network (throttling)
[ ] Steps:
    1. Make API calls with very slow connection
[ ] Expected:
    - Timeout after 30 seconds
    - Error message shown
    - User can retry
    - No infinite loading
[ ] Actual:
[ ] Status:
[ ] Notes:
```

---

## CATEGORY 8: LOCALIZATION & i18n (8 tests)

### 8.1 Language Coverage

**TC-091: All Strings Translated - English** [P1]
```
[ ] Preconditions: App in English
[ ] Steps:
    1. Navigate through entire app
    2. Check all screens, dialogs, errors
[ ] Expected:
    - Zero hardcoded strings
    - All text uses l10n system
    - Proper grammar and tone
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-092: All Strings Translated - Spanish** [P1]
```
[ ] Preconditions: App in Spanish
[ ] Steps:
    1. Navigate through entire app
[ ] Expected:
    - All strings in Spanish
    - No missing translations (no English fallback shown)
    - Culturally appropriate translations
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-093: All Strings Translated - French** [P1]
```
[ ] Preconditions: App in French
[ ] Steps:
    1. Full app walkthrough
[ ] Expected:
    - Complete French translations
    - Proper accents and grammar
    - No English text visible
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-094: All Strings Translated - German** [P1]
```
[ ] Preconditions: App in German
[ ] Steps:
    1. Full app walkthrough
[ ] Expected:
    - Complete German translations
    - Formal "Sie" vs informal "du" correctly used
    - No English text
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 8.2 Locale-Specific Formatting

**TC-095: Date Formatting - All Locales** [P2]
```
[ ] Preconditions: None
[ ] Steps:
    1. Change language to each of 6 languages
    2. Check date display (e.g., birthdate, horoscope dates)
[ ] Expected:
    - Dates formatted per locale:
      - EN: MM/DD/YYYY
      - ES: DD/MM/YYYY
      - FR: DD/MM/YYYY
      - DE: DD.MM.YYYY
      - IT: DD/MM/YYYY
      - PT: DD/MM/YYYY
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-096: Currency Formatting** [P2]
```
[ ] Preconditions: View pricing in different locales
[ ] Steps:
    1. Check premium pricing display
[ ] Expected:
    - Currency symbols correct ($ for US, € for EU, etc.)
    - Decimal separators correct (. vs ,)
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-097: Pluralization Rules** [P2]
```
[ ] Preconditions: Features with counts (e.g., "5 messages")
[ ] Steps:
    1. Test with 0, 1, 2, 5 items in different languages
[ ] Expected:
    - Correct plural forms:
      - EN: "1 message" vs "5 messages"
      - ES: "1 mensaje" vs "5 mensajes"
      - FR: Correct liaison rules
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-098: RTL Language Support** [P3]
```
[ ] Preconditions: If Arabic/Hebrew support planned
[ ] Steps:
    1. Switch to RTL language
[ ] Expected:
    - UI mirrors correctly
    - Text alignment right-to-left
    - Icons/images flipped appropriately
[ ] Actual:
[ ] Status:
[ ] Notes:
```

---

## CATEGORY 9: ACCESSIBILITY (7 tests)

### 9.1 VoiceOver / TalkBack

**TC-099: VoiceOver Navigation - iOS** [P2]
```
[ ] Preconditions: VoiceOver enabled
[ ] Steps:
    1. Navigate through app with VoiceOver
[ ] Expected:
    - All elements have labels
    - Navigation logical and clear
    - Buttons announce their action
    - No "Unlabeled button" errors
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-100: TalkBack Navigation - Android** [P2]
```
[ ] Preconditions: TalkBack enabled
[ ] Steps:
    1. Navigate through app with TalkBack
[ ] Expected:
    - All elements accessible
    - Logical focus order
    - Announcements clear
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 9.2 Dynamic Type / Font Scaling

**TC-101: Large Text Support** [P2]
```
[ ] Preconditions: System font size set to largest
[ ] Steps:
    1. Open app with large font setting
[ ] Expected:
    - All text scales correctly
    - No text truncation
    - No layout breaks
    - Buttons/UI elements resize
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-102: Small Text Support** [P3]
```
[ ] Preconditions: System font size set to smallest
[ ] Steps:
    1. Open app with small font setting
[ ] Expected:
    - Text readable
    - UI still usable
    - No excessive whitespace
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 9.3 Color Contrast

**TC-103: High Contrast Mode** [P2]
```
[ ] Preconditions: Enable high contrast mode
[ ] Steps:
    1. Navigate through app
[ ] Expected:
    - All text meets WCAG AA standards (4.5:1 ratio)
    - Important elements meet AAA (7:1)
    - Colors adjust in high contrast mode
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-104: Color Blind Modes** [P3]
```
[ ] Preconditions: Test with color blindness simulators
[ ] Steps:
    1. Simulate protanopia, deuteranopia, tritanopia
[ ] Expected:
    - Information not conveyed by color alone
    - Icons/labels used in addition to color
    - UI usable in all modes
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 9.4 Keyboard Navigation

**TC-105: Keyboard Navigation - External Keyboard** [P3]
```
[ ] Preconditions: iPad/Android tablet with keyboard
[ ] Steps:
    1. Navigate app using Tab/Arrow keys
[ ] Expected:
    - All interactive elements reachable
    - Focus indicator visible
    - Enter activates buttons
    - Esc dismisses dialogs
[ ] Actual:
[ ] Status:
[ ] Notes:
```

---

## CATEGORY 10: EDGE CASES & ERROR HANDLING (10 tests)

### 10.1 Invalid Input Handling

**TC-106: Invalid Email Format** [P2]
```
[ ] Preconditions: Registration/login screen
[ ] Steps:
    1. Enter various invalid emails (no @, multiple @, etc.)
[ ] Expected:
    - Validation error shown
    - Cannot proceed
    - Helpful error message
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-107: SQL Injection Attempt** [P3]
```
[ ] Preconditions: Any text input field
[ ] Steps:
    1. Enter SQL injection strings (e.g., "'; DROP TABLE users;--")
[ ] Expected:
    - Input sanitized
    - No SQL execution (Firebase NoSQL, but test anyway)
    - No error, just treated as text
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-108: XSS Attempt** [P3]
```
[ ] Preconditions: Text input that displays in UI
[ ] Steps:
    1. Enter script tags: "<script>alert('XSS')</script>"
[ ] Expected:
    - Input escaped/sanitized
    - No script execution
    - Displayed as plain text
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 10.2 Boundary Conditions

**TC-109: Maximum Input Length** [P2]
```
[ ] Preconditions: Text fields with limits
[ ] Steps:
    1. Enter text exceeding max length
[ ] Expected:
    - Input truncated or blocked at limit
    - Character count shown
    - No crash
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-110: Empty Required Fields** [P2]
```
[ ] Preconditions: Form with required fields
[ ] Steps:
    1. Leave required fields empty
    2. Attempt to submit
[ ] Expected:
    - Validation errors shown
    - Required fields highlighted
    - Cannot submit
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-111: Future/Past Dates** [P2]
```
[ ] Preconditions: Birthdate input
[ ] Steps:
    1. Enter future date (2099-01-01)
    2. Enter very old date (1800-01-01)
[ ] Expected:
    - Future dates rejected: "Birthdate cannot be in future"
    - Very old dates rejected or warning shown
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 10.3 Concurrent Operations

**TC-112: Multiple Tabs/Windows (iPad Split View)** [P3]
```
[ ] Preconditions: iPad with split view
[ ] Steps:
    1. Open app in both split view windows
[ ] Expected:
    - App handles gracefully
    - No data corruption
    - State syncs or shows warning
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-113: Rapid Screen Navigation** [P2]
```
[ ] Preconditions: None
[ ] Steps:
    1. Rapidly tap navigation buttons
    2. Navigate back/forward quickly
[ ] Expected:
    - No crashes
    - Navigation stable
    - No stuck states
[ ] Actual:
[ ] Status:
[ ] Notes:
```

### 10.4 System Interruptions

**TC-114: Phone Call During Purchase** [P2]
```
[ ] Preconditions: Purchase in progress
[ ] Steps:
    1. Initiate purchase
    2. Receive phone call
    3. Accept call
    4. Return to app
[ ] Expected:
    - Purchase resumes or retries
    - No double charge
    - State preserved
[ ] Actual:
[ ] Status:
[ ] Notes:
```

**TC-115: System Alert During App Use** [P2]
```
[ ] Preconditions: App in use
[ ] Steps:
    1. Trigger system alert (low battery, etc.)
[ ] Expected:
    - App handles gracefully
    - State preserved
    - Resumes normally
[ ] Actual:
[ ] Status:
[ ] Notes:
```

---

## TEST EXECUTION SUMMARY

### Overall Progress

```
Total Test Cases:        115
Critical (P0):           15  [ ] 0% Complete
High Priority (P1):      45  [ ] 0% Complete
Medium Priority (P2):    40  [ ] 0% Complete
Low Priority (P3):       15  [ ] 0% Complete

Status Distribution:
Not Started:             115 (100%)
In Progress:             0   (0%)
Passed:                  0   (0%)
Failed:                  0   (0%)
```

### Testing Priorities for Soft Launch

**Week 1: Critical Path (P0 + High Priority P1)**
```
Must Pass Before Soft Launch:
[ ] All P0 tests (15 tests)
[ ] Payment flow P1 tests (10 tests)
[ ] Auth flow P1 tests (5 tests)
[ ] Core horoscope P1 tests (5 tests)
────────────────────────────────
Total: 35 tests (Week 1 focus)
```

**Week 2: Extended Coverage (Remaining P1 + P2)**
```
Should Pass Before Full Launch:
[ ] Remaining P1 tests (25 tests)
[ ] Critical P2 tests (20 tests)
────────────────────────────────
Total: 45 tests (Week 2 focus)
```

**Week 3+: Full Coverage (P3 + Regression)**
```
Nice to Have:
[ ] All P3 tests (15 tests)
[ ] Regression suite (20 tests)
[ ] Load/stress testing (10 tests)
────────────────────────────────
Total: 45 tests (Ongoing)
```

---

## TEST ENVIRONMENT SETUP

### Required Test Accounts

```
1. Free User Account
   Email: test.free@zodiacapp.test
   Password: TestFree123!
   Premium: No

2. Cosmic Subscriber
   Email: test.cosmic@zodiacapp.test
   Password: TestCosmic123!
   Premium: Yes (Cosmic Monthly)

3. Stellar Subscriber
   Email: test.stellar@zodiacapp.test
   Password: TestStellar123!
   Premium: Yes (Stellar Annual)

4. HR Professional
   Email: test.hrpro@zodiacapp.test
   Password: TestHRPro123!
   Premium: Yes (HR Professional)

5. Expired Subscription
   Email: test.expired@zodiacapp.test
   Password: TestExpired123!
   Premium: Expired
```

### Test Devices

```
iOS:
- iPhone 15 Pro (iOS 17.2) - Primary
- iPhone 12 (iOS 16.5) - Regression
- iPad Pro 12.9" (iOS 17.2) - Tablet

Android:
- Pixel 8 (Android 14) - Primary
- Samsung Galaxy S21 (Android 13) - Regression
- Samsung Galaxy Tab S8 (Android 13) - Tablet
```

### Test Data

```
Birth Data Samples:
1. Complete: 1990-03-21, 14:30, New York, NY
2. Date only: 1985-07-15
3. Missing time: 1992-11-30, Unknown time, London
4. Missing location: 1988-05-10, 08:00, Unknown

Zodiac Signs to Test:
- Aries (Ram)
- Taurus (Bull)
- Gemini (Twins)
- Cancer (Crab)
- Leo (Lion)
- Virgo (Virgin)
- Libra (Scales)
- Scorpio (Scorpion)
- Sagittarius (Archer)
- Capricorn (Goat)
- Aquarius (Water Bearer)
- Pisces (Fish)
```

---

## AUTOMATION RECOMMENDATIONS

### High Priority for Automation (Post-Launch)

```
1. Purchase Flow End-to-End
   - Estimated ROI: Very High
   - Effort: Medium (2 weeks)
   - Maintenance: Low

2. Auth Flow (Login/Register/Logout)
   - Estimated ROI: High
   - Effort: Low (3 days)
   - Maintenance: Low

3. Language Switching
   - Estimated ROI: High
   - Effort: Low (2 days)
   - Maintenance: Very Low

4. Horoscope Loading
   - Estimated ROI: Medium
   - Effort: Low (1 day)
   - Maintenance: Low

5. Regression Suite (Smoke Tests)
   - Estimated ROI: Very High
   - Effort: High (4 weeks)
   - Maintenance: Medium
```

### Tools Recommended

```
iOS:
- XCUITest (native)
- Fastlane (CI/CD)
- Firebase Test Lab

Android:
- Espresso (native)
- Fastlane (CI/CD)
- Firebase Test Lab

Cross-platform:
- Patrol (Flutter testing framework)
- Integration tests (Flutter built-in)
```

---

## DEFECT TRACKING

### Severity Levels

```
S1 - BLOCKER:     Prevents release, no workaround
S2 - CRITICAL:    Major feature broken, workaround exists
S3 - HIGH:        Important feature broken, alternative exists
S4 - MEDIUM:      Minor feature issue, low user impact
S5 - LOW:         Cosmetic issue, trivial impact
```

### Defect Template

```
Defect ID: [Auto-generated]
Test Case: TC-XXX
Severity: [S1/S2/S3/S4/S5]
Priority: [P0/P1/P2/P3/P4]
Status: [New/Assigned/In Progress/Fixed/Verified/Closed]

Summary:
[Brief description]

Steps to Reproduce:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Expected Result:
[What should happen]

Actual Result:
[What actually happened]

Environment:
- Device: [iPhone 15 Pro]
- OS: [iOS 17.2]
- App Version: [1.0.0]
- Build: [123]

Screenshots/Videos:
[Attached]

Additional Notes:
[Any other relevant information]
```

---

**Document Version:** 1.0
**Last Updated:** 2025-01-23
**Next Review:** After first testing cycle
**Owner:** QA Team Lead

---

**Related Documents:**
- COMPLETE_VALIDATION_REPORT.md (Master quality assessment)
- RISK_ASSESSMENT.md (Detailed risk analysis)
- DEPLOYMENT_PRIORITIES.md (Deployment roadmap)
