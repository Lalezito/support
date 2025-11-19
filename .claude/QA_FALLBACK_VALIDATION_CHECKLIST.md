# 🧪 QA FALLBACK VALIDATION CHECKLIST

**Purpose**: Validate graceful degradation behaves correctly across all scenarios
**Owner**: QA Team
**Priority**: P1 - Must validate before v1.0 launch
**Estimated Time**: 2-3 hours

---

## 📋 Pre-Test Setup

### Environment Preparation

- [ ] **Device/Simulator**: iOS 14+ or Android 8+
- [ ] **Build**: Debug build with logging enabled
- [ ] **Tools**:
  - Charles Proxy or similar for network manipulation
  - Console/logs access for monitoring
  - Test account with no premium subscription

### Monitoring Setup

- [ ] Enable verbose logging: `flutter run --verbose`
- [ ] Have console open to monitor logs
- [ ] Prepare screenshot tool for evidence
- [ ] Create test report template

---

## 🎯 Test Suite 1: Cosmic Chat Service Fallbacks

### Scenario 1.1: Network Offline Mode

**Setup**:
1. Launch app
2. Navigate to Cosmic Chat
3. Enable airplane mode

**Test Steps**:
1. Type "Hello" and send
2. Type "I need help with my goals" and send
3. Type "I'm feeling anxious" and send

**Expected Results**:
- [ ] Chat continues to work (no error screens)
- [ ] Responses are contextually relevant
- [ ] Response time < 2 seconds
- [ ] Console logs show: `Fallback used: service=cosmic_chat, reason=ai_service_error`

**Evidence**: Take screenshots of:
- [ ] Chat working offline
- [ ] Console logs showing fallback

---

### Scenario 1.2: Backend Maintenance Window

**Setup**:
1. Use Charles Proxy to block AI API endpoints
2. Launch app
3. Navigate to Cosmic Chat

**Test Steps**:
1. Send 5 different message types (greeting, goal, emotion, energy, help)

**Expected Results**:
- [ ] All messages get responses
- [ ] Responses match message pattern (greeting → greeting response)
- [ ] No error messages shown
- [ ] Console logs track each fallback

**Evidence**:
- [ ] Screenshot of 5 successful responses
- [ ] Console log excerpt

---

### Scenario 1.3: Rate Limit Exceeded

**Setup**:
1. Configure Charles to return 429 (Too Many Requests)
2. Launch app

**Test Steps**:
1. Send rapid messages (10 in 30 seconds)

**Expected Results**:
- [ ] All messages receive responses
- [ ] No "rate limit" error shown to user
- [ ] Fallback responses vary (not all identical)

---

## 🎯 Test Suite 2: Premium Orchestrator Fallbacks

### Scenario 2.1: Personal AI Coach Unavailable

**Setup**:
1. Block EmotionalAI, CoachingAI, PersonalizationAI endpoints
2. Launch app as premium user

**Test Steps**:
1. Navigate to Premium AI Coach
2. Ask for coaching on a decision
3. Request personalized guidance

**Expected Results**:
- [ ] Feature remains accessible
- [ ] Generic but helpful guidance provided
- [ ] No "service unavailable" errors
- [ ] Console logs: `Fallback used: service=premium_orchestrator`

**Evidence**:
- [ ] Screenshot of working feature
- [ ] Console logs

---

### Scenario 2.2: Decision Timing Calculation Error

**Setup**:
1. Block PredictiveAstrologyService endpoint
2. Launch as premium user

**Test Steps**:
1. Request optimal timing for a decision
2. Check provided date and reasoning

**Expected Results**:
- [ ] Timing recommendation provided (3 days from now)
- [ ] Reasoning is astrologically sound
- [ ] Success probability shown (~60%)
- [ ] Console logs: `Fallback used: service=decision_timing`

---

### Scenario 2.3: Deep Compatibility Analysis Failure

**Setup**:
1. Block NeuralCompatibilityService endpoint
2. Launch as premium user

**Test Steps**:
1. Navigate to Compatibility feature
2. Enter partner information
3. Request analysis

**Expected Results**:
- [ ] Analysis completes
- [ ] Basic compatibility tips provided
- [ ] Relationship advice shown
- [ ] Console logs: `Fallback used: service=deep_compatibility`

---

## 🎯 Test Suite 3: Fallback Quality Validation

### Scenario 3.1: Response Quality Check

**Goal**: Ensure fallback responses are production-quality

**Test Steps**:
1. Compare AI response vs fallback response side-by-side
2. Rate fallback on:
   - Relevance (1-5)
   - Helpfulness (1-5)
   - Astrological context (1-5)

**Acceptance Criteria**:
- [ ] Average rating ≥ 3.5/5
- [ ] No Lorem Ipsum or placeholder text
- [ ] Responses are personalized (use zodiac sign)

---

### Scenario 3.2: Fallback Variety

**Goal**: Ensure fallbacks don't feel repetitive

**Test Steps**:
1. Trigger same fallback 5 times
2. Check response variation

**Expected Results**:
- [ ] At least 3 different responses for same pattern
- [ ] Responses feel natural, not mechanical
- [ ] User wouldn't notice it's a fallback

---

## 🎯 Test Suite 4: Analytics & Monitoring

### Scenario 4.1: Log Verification

**Test Steps**:
1. Trigger 3 different fallbacks
2. Check console logs

**Expected Logs**:
- [ ] `Fallback used: service=cosmic_chat, reason=ai_service_error`
- [ ] `Fallback used: service=premium_orchestrator, reason=ai_unavailable`
- [ ] `Fallback used: service=decision_timing, reason=calculation_error`

**Verification**:
- [ ] Service name is correct
- [ ] Reason is descriptive
- [ ] Timestamp is present

---

### Scenario 4.2: SharedPreferences Storage

**Test Steps**:
1. Trigger fallback
2. Check SharedPreferences keys

**Expected**:
- [ ] Key format: `last_fallback_{timestamp}`
- [ ] Value format: `{service}:{reason}`
- [ ] Data persists between app restarts

**Validation Command** (iOS Simulator):
```bash
xcrun simctl get_app_container booted com.zodiac.app data
# Navigate to Library/Preferences
# Open plist file and verify fallback keys exist
```

---

## 🎯 Test Suite 5: Edge Cases

### Scenario 5.1: Rapid Fallback Switching

**Test Steps**:
1. Start with network on (AI works)
2. Toggle airplane mode on/off rapidly
3. Send messages during transitions

**Expected Results**:
- [ ] No crashes
- [ ] Smooth transition between AI and fallback
- [ ] User doesn't notice switching

---

### Scenario 5.2: Long-Duration Offline

**Test Steps**:
1. Enable airplane mode
2. Use app for 30 minutes (chat, coach, compatibility)
3. Re-enable network

**Expected Results**:
- [ ] App functions throughout
- [ ] Seamless transition back to AI when online
- [ ] No data loss or corruption

---

### Scenario 5.3: Partial Service Failure

**Test Steps**:
1. Block only CoachingAI (keep EmotionalAI, PersonalizationAI working)
2. Test Premium Orchestrator

**Expected Results**:
- [ ] Orchestrator uses available services
- [ ] Falls back only for blocked service
- [ ] Combined response uses both real + fallback data

---

## 📊 Success Criteria

### Must Pass (Blockers)

- [ ] **Zero user-visible errors**: No "service unavailable" messages
- [ ] **100% feature availability**: All features work in fallback mode
- [ ] **Response quality**: Average rating ≥ 3.5/5
- [ ] **Logging coverage**: 100% of fallbacks logged
- [ ] **No crashes**: 0 crashes during fallback scenarios

### Nice to Have (Improvements)

- [ ] Fallback response time < 1 second
- [ ] Response variety ≥ 5 per pattern
- [ ] Analytics integration working
- [ ] User can't distinguish fallback from AI

---

## 🐛 Bug Reporting Template

If any test fails, use this template:

```markdown
### Bug: [Short Description]

**Scenario**: [Test scenario number]
**Expected**: [What should happen]
**Actual**: [What actually happened]
**Severity**: [Critical/High/Medium/Low]

**Reproduction Steps**:
1.
2.
3.

**Evidence**:
- Screenshot: [attach]
- Console log: [paste]

**Environment**:
- Device: [iOS 16 / Android 12]
- Build: [Debug/Release]
- Network: [Offline/Rate limited/etc]
```

---

## 📈 Test Execution Log

### Test Run #1
- **Date**: __________
- **Tester**: __________
- **Build**: __________
- **Pass Rate**: _____ / _____ tests
- **Blockers Found**: ___
- **Notes**:

### Test Run #2 (After Fixes)
- **Date**: __________
- **Tester**: __________
- **Build**: __________
- **Pass Rate**: _____ / _____ tests
- **Blockers Found**: ___
- **Notes**:

---

## ✅ Sign-Off

**QA Lead**: _________________________ Date: _______
**Product Owner**: ____________________ Date: _______
**Engineering Lead**: _________________ Date: _______

**Status**: [ ] APPROVED FOR PRODUCTION  [ ] NEEDS FIXES

---

**Document Version**: 1.0
**Created**: October 6, 2025
**Last Updated**: October 6, 2025
**Next Review**: Before v1.0 launch
