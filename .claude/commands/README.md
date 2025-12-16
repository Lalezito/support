# Legion of Superagents - Specialized AI Expert Commands

A collection of **14 specialized expert agents** designed to be reusable across any software project.

## Quick Reference

| Command | Domain | Use When |
|---------|--------|----------|
| `/architect` | System Design | Architectural decisions, service design |
| `/security-auditor` | Security | Vulnerability audits, compliance |
| `/performance-optimizer` | Performance | Speed optimization, memory leaks |
| `/test-engineer` | Quality | Testing strategy, coverage |
| `/devops-engineer` | Infrastructure | Deployment, CI/CD, monitoring |
| `/code-reviewer` | Code Quality | PR reviews, code analysis |
| `/refactoring-guru` | Code Improvement | Restructuring, pattern application |
| `/i18n-translator` | Localization | Translations, multi-language |
| `/database-expert` | Data | Schema design, query optimization |
| `/api-designer` | APIs | REST/GraphQL design, documentation |
| `/debugger` | Problem Solving | Bug hunting, root cause analysis |
| `/documentation-writer` | Docs | README, API docs, comments |
| `/git-master` | Version Control | Branching, merging, history |
| `/ux-analyst` | User Experience | Usability, accessibility |

---

## Agent Categories

### Core Development (5)
```
/architect           → System architecture and design patterns
/code-reviewer       → Code quality and PR reviews
/refactoring-guru    → Code improvement without changing behavior
/debugger            → Systematic bug finding and fixing
/documentation-writer → Technical documentation
```

### Quality & Security (3)
```
/security-auditor        → Security vulnerabilities and compliance
/performance-optimizer   → Speed and resource optimization
/test-engineer           → Testing strategy and automation
```

### Infrastructure (2)
```
/devops-engineer → Deployment, CI/CD, infrastructure
/database-expert → Data modeling, query optimization
```

### Specialized (4)
```
/api-designer    → REST/GraphQL API design
/i18n-translator → Internationalization and localization
/git-master      → Version control operations
/ux-analyst      → User experience and accessibility
```

---

## Usage Examples

### Starting a New Feature
```
1. /architect     → Design the feature architecture
2. /api-designer  → Design API endpoints (if needed)
3. /database-expert → Design data model (if needed)
4. Code implementation...
5. /code-reviewer → Review your code
6. /test-engineer → Write tests
```

### Fixing a Bug
```
1. /debugger       → Find root cause
2. Fix the bug...
3. /test-engineer  → Add regression test
4. /code-reviewer  → Verify fix quality
```

### Performance Issue
```
1. /performance-optimizer → Identify bottlenecks
2. /database-expert       → Optimize queries (if DB related)
3. /refactoring-guru      → Restructure code (if needed)
```

### Security Audit
```
1. /security-auditor → Full security scan
2. Fix vulnerabilities...
3. /code-reviewer    → Verify fixes
```

### Adding Translations
```
1. /i18n-translator → Audit current state
2. Add translations...
3. /i18n-translator → Verify completeness
```

### Preparing for Release
```
1. /test-engineer         → Verify test coverage
2. /security-auditor      → Security check
3. /performance-optimizer → Performance check
4. /documentation-writer  → Update docs
5. /devops-engineer       → Deploy
```

---

## Agent Capabilities

### /architect
- Microservices vs Monolithic decisions
- Clean Architecture / DDD
- Service consolidation
- Technical debt assessment

### /security-auditor
- OWASP Top 10 vulnerabilities
- Secret detection
- GDPR compliance
- Security best practices

### /performance-optimizer
- Startup time optimization
- Memory leak detection
- Frame rate analysis
- Caching strategies

### /test-engineer
- Test pyramid strategy
- Coverage analysis
- TDD/BDD methodologies
- Test automation

### /devops-engineer
- Railway/AWS/GCP deployments
- CI/CD pipeline setup
- Docker/Kubernetes
- Monitoring and alerting

### /code-reviewer
- SOLID principles
- Code smells detection
- Clean code practices
- PR review format

### /refactoring-guru
- Extract Method/Class
- Replace conditionals
- Design patterns
- Safe refactoring steps

### /i18n-translator
- ARB/JSON/PO files
- Pluralization
- Cultural adaptation
- Missing translation detection

### /database-expert
- Schema design
- Index strategies
- Query optimization
- Migration management

### /api-designer
- RESTful design
- OpenAPI/Swagger
- GraphQL schemas
- API versioning

### /debugger
- Binary search isolation
- Stack trace analysis
- Race condition detection
- Memory debugging

### /documentation-writer
- README templates
- API documentation
- ADRs (Architecture Decision Records)
- Code comments

### /git-master
- Branching strategies
- Conflict resolution
- History management
- Commit conventions

### /ux-analyst
- Nielsen's 10 heuristics
- WCAG accessibility
- User flow analysis
- Conversion optimization

---

## Best Practices

### Chain Agents for Complex Tasks
```
Big feature? Use: architect → api-designer → database-expert → test-engineer
Production bug? Use: debugger → code-reviewer → test-engineer
Performance issue? Use: performance-optimizer → database-expert → refactoring-guru
```

### Run Parallel for Audits
```
Pre-release audit:
- /security-auditor (security)
- /performance-optimizer (speed)
- /test-engineer (coverage)
- /ux-analyst (usability)
```

### Regular Maintenance
```
Weekly: /code-reviewer on recent changes
Monthly: /security-auditor full scan
Quarterly: /architect review technical debt
```

---

## Customization

Each agent can be customized for your project by:
1. Adding project-specific patterns
2. Including team conventions
3. Setting custom thresholds
4. Adding domain-specific checks

---

## Project-Specific Agents

Additionally, project-specific agents exist:

| Command | Purpose |
|---------|---------|
| `/error-doctor` | Zodiac app error diagnosis |
| `/nano-banana` | PDF icon generation with Gemini AI |

---

**Total: 14 Reusable Superagents + 2 Project-Specific**

Ready to use in any software project!
