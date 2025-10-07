# 🤖 AGENT CAPABILITY MATRIX - ZODIAC APP IMPLEMENTATION
## Matriz de Capacidades y Asignación de Tareas por Agente Especializado

**Referencia para**: Plan de Ejecución Multi-Agente  
**Total Agentes**: 29 especializados  
**Propósito**: Asignación rápida de tareas basada en capacidades específicas

---

## 🏛️ PRINCIPAL AGENTS - AUTORIDAD MÁXIMA

### **🔧 arquitecto_principal**
**Authority Level**: Principal (máxima autoridad)  
**Coordinates with**: Todos los agentes  
**Best For**:
- [ ] **Architectural decisions & strategic planning**
- [ ] **Service consolidation strategies (152→80 services)**
- [ ] **System-wide refactoring plans**
- [ ] **Conflict resolution between agents**
- [ ] **Technical debt assessment and remediation**
- [ ] **Cross-platform architecture design**

**Activation Triggers**:
```yaml
- architectural_decisions
- strategic_planning
- service_consolidation_needed
- agent_conflict_resolution
- system_wide_changes_required
```

**Example Task Assignment**:
```
[arquitecto_principal] Design service consolidation strategy
- Analyze current 152 services for consolidation opportunities
- Create consolidation groups (AI: 16→4, Premium: 23→6)
```

---

### **📱 flutter_developer**
**Authority Level**: Principal  
**Coordinates with**: ui_specialist, animation_expert  
**Best For**:
- [ ] **Flutter code implementation and optimization**
- [ ] **Widget development and custom components**
- [ ] **State management implementation (Provider→Riverpod)**
- [ ] **Navigation and routing systems**
- [ ] **Performance optimization in Flutter context**
- [ ] **Service implementation and refactoring**

**Activation Triggers**:
```yaml
- flutter_issues
- mobile_optimization
- widget_development
- state_management_migration
- ui_implementation
```

**Example Task Assignment**:
```
[flutter_developer] Implement AI services consolidation
- Create CoreAIService.dart consolidating 8 AI services
- Migrate functionality from individual AI services
- Update imports and dependencies throughout app
```

---

## 🎯 SPECIALIST AGENTS - EXPERTISE ESPECÍFICA

### **🔒 compliance_checker**
**Authority Level**: Specialist  
**Coordinates with**: monetization_specialist, data_manager  
**Best For**:
- [ ] **Security vulnerability auditing and fixes**
- [ ] **GDPR compliance implementation**
- [ ] **Data protection and sanitization**
- [ ] **Privacy policy compliance**
- [ ] **App Store guidelines compliance**
- [ ] **Secret management and encryption**

**Activation Triggers**:
```yaml
- security_vulnerabilities
- privacy_compliance
- data_protection
- hardcoded_secrets_detected
- gdpr_compliance_needed
```

**Example Task Assignment**:
```
[compliance_checker] Implement secure logging service
- Create SecureLoggingService.dart with automatic data sanitization
- Define sensitive fields list (email, phone, location, etc.)
- Replace all logging calls with secure sanitization
```

---

### **🖥️ backend_specialist**
**Authority Level**: Specialist  
**Coordinates with**: data_manager, sync_manager  
**Best For**:
- [ ] **Railway deployment and configuration**
- [ ] **API endpoint development and optimization**
- [ ] **Database connectivity and queries**
- [ ] **Server-side validation and security**
- [ ] **Backend performance optimization**
- [ ] **Environment variable management**

**Activation Triggers**:
```yaml
- railway_deployment
- api_issues
- backend_optimization
- database_problems
- server_connectivity_issues
```

**Example Task Assignment**:
```
[backend_specialist] Fix backend connectivity issues
- Resolve database connection pool exhaustion
- Fix SSL certificate issues if present
- Update environment variables for production
```

---

### **💰 monetization_specialist**
**Authority Level**: Specialist  
**Coordinates with**: compliance_checker, subscription_manager  
**Best For**:
- [ ] **Premium feature implementation and gating**
- [ ] **Subscription system development**
- [ ] **Payment validation and security**
- [ ] **Revenue optimization strategies**
- [ ] **App Store IAP integration**
- [ ] **Business model implementation**

**Activation Triggers**:
```yaml
- subscription_issues
- monetization_strategy
- payment_security_vulnerabilities
- premium_features_implementation
- revenue_optimization
```

**Example Task Assignment**:
```
[monetization_specialist] Design astrologer marketplace business model
- Define astrologer onboarding process
- Create revenue sharing structure
- Implement booking and payment flow
```

---

### **🎨 ui_specialist**
**Authority Level**: Specialist  
**Coordinates with**: flutter_developer, animation_expert  
**Best For**:
- [ ] **UI/UX design and implementation**
- [ ] **Accessibility compliance (WCAG 2.1 AA)**
- [ ] **Design system development**
- [ ] **Conversion rate optimization**
- [ ] **A/B testing for UI elements**
- [ ] **Responsive design implementation**

**Activation Triggers**:
```yaml
- design_issues
- user_experience
- accessibility_compliance
- conversion_optimization
- ui_implementation
```

**Example Task Assignment**:
```
[ui_specialist] Implement A/B testing framework
- Create ABTestingService.dart for conversion testing
- Design premium paywall variations
- Implement user assignment to test variants
```

---

### **⚡ performance_monitor**
**Authority Level**: Specialist  
**Coordinates with**: qa_tester, cache_optimizer  
**Best For**:
- [ ] **Performance metrics collection and analysis**
- [ ] **Memory leak detection and prevention**
- [ ] **CPU usage optimization**
- [ ] **Battery consumption monitoring**
- [ ] **Real-time performance tracking**
- [ ] **Performance threshold alerts**

**Activation Triggers**:
```yaml
- performance_issues
- memory_leaks
- optimization_needed
- battery_consumption
- performance_monitoring_required
```

**Example Task Assignment**:
```
[performance_monitor] Implement advanced performance monitoring
- Create real-time performance metrics collection
- Implement automatic optimization triggers
- Add memory leak detection system
```

---

### **🚀 deployment_specialist**
**Authority Level**: Specialist  
**Coordinates with**: build_manager, dependency_resolver  
**Best For**:
- [ ] **Production deployment execution**
- [ ] **CI/CD pipeline management**
- [ ] **Environment configuration**
- [ ] **Build process optimization**
- [ ] **App Store submission process**
- [ ] **Infrastructure monitoring**

**Activation Triggers**:
```yaml
- deployment_issues
- production_deployment
- ci_cd_problems
- build_failures
- app_store_submission
```

**Example Task Assignment**:
```
[deployment_specialist] Execute production deployment
- Deploy backend to Railway production
- Execute database migrations
- Build and submit to App Stores
```

---

## 🧪 TESTING AGENTS - QUALITY ASSURANCE

### **✅ test_automation**
**Authority Level**: Specialist  
**Coordinates with**: qa_tester, performance_monitor  
**Best For**:
- [ ] **Automated test suite development**
- [ ] **Unit test creation and maintenance**
- [ ] **Integration test implementation**
- [ ] **Widget test development**
- [ ] **API test automation**
- [ ] **Test coverage improvement**

**Activation Triggers**:
```yaml
- unit_testing
- test_coverage_improvement
- automated_testing
- model_validation_needed
- service_testing_required
```

**Example Task Assignment**:
```
[test_automation] Create comprehensive model tests
- Implement tests for all 13 models
- Cover serialization/deserialization for each model
- Achieve >95% line coverage for all models
```

---

### **🔍 qa_tester**
**Authority Level**: Specialist  
**Coordinates with**: test_automation, performance_monitor  
**Best For**:
- [ ] **Manual testing and validation**
- [ ] **User acceptance testing**
- [ ] **Bug verification and validation**
- [ ] **Test result analysis**
- [ ] **Quality metrics reporting**
- [ ] **Critical path validation**

**Activation Triggers**:
```yaml
- quality_assurance_needed
- bug_verification
- user_acceptance_testing
- critical_path_validation
- final_validation_required
```

**Example Task Assignment**:
```
[qa_tester] Final production validation
- Execute complete test suite on production
- Validate all critical user journeys
- Ensure all performance targets met
```

---

## 📊 ANALYSIS AGENTS - INSIGHT & EVALUATION

### **📈 performance_analysis_expert**
**Authority Level**: Analysis  
**Coordinates with**: performance_monitor, cache_optimizer  
**Best For**:
- [ ] **Performance bottleneck identification**
- [ ] **Optimization recommendation generation**
- [ ] **System performance analysis**
- [ ] **Resource usage evaluation**
- [ ] **Performance trend analysis**

**Activation Triggers**:
```yaml
- performance_analysis
- bottleneck_identification
- optimization_recommendations
- performance_audit_required
```

---

### **🔒 security_analysis_expert**
**Authority Level**: Analysis  
**Coordinates with**: compliance_checker, data_manager  
**Best For**:
- [ ] **Security vulnerability assessment**
- [ ] **Compliance gap analysis**
- [ ] **Risk evaluation and mitigation planning**
- [ ] **Security audit execution**
- [ ] **Threat modeling**

**Activation Triggers**:
```yaml
- security_audit
- vulnerability_assessment
- compliance_review
- security_analysis_required
```

---

## 🎯 SPECIALIZED DOMAIN EXPERTS

### **🧠 ai_coach_developer**
**Authority Level**: Specialist  
**Coordinates with**: mood_analyzer, insight_generator  
**Best For**:
- [ ] **AI coaching system implementation**
- [ ] **Content generation and management**
- [ ] **Personalization algorithm development**
- [ ] **Manifestation Academy content creation**
- [ ] **AI-driven insights implementation**

**Activation Triggers**:
```yaml
- ai_coaching_issues
- content_generation
- personalization_problems
- manifestation_features
- cosmic_insights_required
```

---

### **🌍 i18n_specialist**
**Authority Level**: Specialist  
**Coordinates with**: arb_manager, translation_validator  
**Best For**:
- [ ] **Internationalization implementation**
- [ ] **Translation management and validation**
- [ ] **Multi-language support**
- [ ] **ARB file management**
- [ ] **Localization testing**

**Activation Triggers**:
```yaml
- translation_issues
- localization_bugs
- arb_file_problems
- multi_language_support
- internationalization_required
```

---

## ⚙️ SUPPORTING AGENTS - TECHNICAL INFRASTRUCTURE

### **📦 data_manager**
**Authority Level**: Supporting  
**Coordinates with**: backend_specialist, sync_manager  
**Best For**:
- [ ] **Data persistence and storage**
- [ ] **Database schema management**
- [ ] **Data synchronization**
- [ ] **Backup and recovery**
- [ ] **Data migration**

---

### **💾 cache_optimizer**  
**Authority Level**: Supporting  
**Coordinates with**: performance_monitor  
**Best For**:
- [ ] **Cache strategy implementation**
- [ ] **Memory optimization**
- [ ] **Cache invalidation logic**
- [ ] **Performance cache tuning**

---

### **🔗 dependency_resolver**
**Authority Level**: Supporting  
**Coordinates with**: deployment_specialist  
**Best For**:
- [ ] **Dependency conflict resolution**
- [ ] **Package management**
- [ ] **Version compatibility**
- [ ] **Build dependency optimization**

---

## 📋 TASK ASSIGNMENT QUICK REFERENCE

### **🚨 CRITICAL SECURITY TASKS**
```yaml
Secret Management: compliance_checker + backend_specialist
Payment Security: monetization_specialist + compliance_checker
Data Sanitization: compliance_checker + data_manager
GDPR Compliance: compliance_checker + i18n_specialist
```

### **⚡ PERFORMANCE OPTIMIZATION TASKS**
```yaml
Memory Leaks: performance_monitor + flutter_developer
Cache Optimization: cache_optimizer + performance_monitor
Database Queries: backend_specialist + data_manager
UI Performance: ui_specialist + flutter_developer
```

### **🧪 TESTING IMPLEMENTATION TASKS**
```yaml
Unit Tests: test_automation + flutter_developer
Integration Tests: test_automation + backend_specialist
Widget Tests: test_automation + ui_specialist
E2E Tests: test_automation + qa_tester
```

### **🏗️ ARCHITECTURE REFACTORING TASKS**
```yaml
Service Consolidation: arquitecto_principal + flutter_developer
State Management Migration: flutter_developer + ui_specialist
Monolithic Breakdown: flutter_developer + arquitecto_principal
Dependency Optimization: dependency_resolver + deployment_specialist
```

### **💰 BUSINESS FEATURE TASKS**
```yaml
Premium Features: monetization_specialist + flutter_developer
Live Astrologers: monetization_specialist + backend_specialist
B2B Enterprise: ui_specialist + backend_specialist
Manifestation Academy: ai_coach_developer + flutter_developer
```

### **🚀 DEPLOYMENT TASKS**
```yaml
Production Deploy: deployment_specialist + backend_specialist
App Store Submission: deployment_specialist + compliance_checker
Environment Config: deployment_specialist + backend_specialist
Monitoring Setup: performance_monitor + deployment_specialist
```

---

## 🔄 AGENT COORDINATION WORKFLOWS

### **STANDARD TASK EXECUTION FLOW:**
1. **Assignment** → Primary agent identifies task requirements
2. **Coordination** → Primary agent coordinates with supporting agents
3. **Execution** → Parallel execution with defined deliverables
4. **Verification** → Cross-agent validation of results
5. **Integration** → Integration testing and final validation

### **ESCALATION PROTOCOLS:**
```yaml
Task Conflicts:
  Same Level: collaborative_decision
  Cross Level: defer_to_higher_authority
  Deadlock: escalate_to_arquitecto_principal

Emergency Situations:
  Critical Bug: qa_tester → arquitecto_principal
  Security Incident: compliance_checker → arquitecto_principal
  Deployment Failure: deployment_specialist → arquitecto_principal
```

### **QUALITY GATES:**
- **Every deliverable** must be validated by assigned verification agent
- **Critical tasks** require dual-agent verification
- **Production changes** require arquitecto_principal approval
- **Security changes** require compliance_checker validation

---

## 🎯 ACTIVATION COMMAND EXAMPLES

### **FOR SECURITY TASKS:**
```bash
# Activate secret management task
Trigger: security_vulnerabilities + hardcoded_secrets_detected
Primary: compliance_checker
Supporting: backend_specialist, deployment_specialist
```

### **FOR PERFORMANCE TASKS:**
```bash
# Activate performance optimization
Trigger: performance_issues + memory_optimization
Primary: performance_monitor  
Supporting: flutter_developer, cache_optimizer
```

### **FOR TESTING TASKS:**
```bash
# Activate comprehensive testing
Trigger: unit_testing + model_validation_needed
Primary: test_automation
Supporting: flutter_developer, qa_tester
```

### **FOR ARCHITECTURE TASKS:**
```bash
# Activate service consolidation
Trigger: architectural_decisions + code_complexity_reduction
Primary: arquitecto_principal
Supporting: flutter_developer, backend_specialist
```

---

## ✅ AGENT READINESS CHECKLIST

### **BEFORE TASK ACTIVATION:**
- [ ] **Agent Availability**: Confirm primary and supporting agents are available
- [ ] **Prerequisites Met**: Ensure all required dependencies and inputs are ready
- [ ] **Coordination Channels**: Establish communication between coordinating agents
- [ ] **Success Criteria Defined**: Clear deliverables and validation criteria set
- [ ] **Escalation Path Clear**: Know who to escalate to if problems arise

### **DURING TASK EXECUTION:**
- [ ] **Progress Tracking**: Monitor task progress and deliverable completion
- [ ] **Cross-Agent Communication**: Ensure coordinating agents are synchronizing
- [ ] **Quality Validation**: Verify deliverables meet specified criteria
- [ ] **Issue Management**: Handle any conflicts or blockers immediately

### **AFTER TASK COMPLETION:**
- [ ] **Deliverable Verification**: Confirm all deliverables meet success criteria
- [ ] **Integration Testing**: Validate that changes work with existing system
- [ ] **Documentation Update**: Update relevant documentation and status
- [ ] **Next Task Preparation**: Prepare inputs and prerequisites for dependent tasks

---

**STATUS**: ✅ **MATRIX COMPLETA - READY FOR TASK ASSIGNMENT**  
**TOTAL AGENTS MAPPED**: 29 especializados  
**TASK CATEGORIES COVERED**: Security, Performance, Testing, Architecture, Business, Deployment  

*Matriz creada: 8 Septiembre 2025*  
*Para uso con: Multi-Agent Execution Plan*  
*Próxima referencia: Durante asignación de tareas específicas*