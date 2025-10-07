# 🔒 SECRET ROTATION SYSTEM - OPERATIONS RUNBOOK

**Document Version**: 1.0.0  
**Last Updated**: September 8, 2025  
**Maintained By**: Security Operations Team  
**Emergency Contact**: security@zodiac-app.com  

---

## 📋 TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Secret Rotation Architecture](#secret-rotation-architecture)
3. [Automated Rotation Procedures](#automated-rotation-procedures)
4. [Emergency Rotation Procedures](#emergency-rotation-procedures)
5. [Monitoring and Alerting](#monitoring-and-alerting)
6. [Troubleshooting Guide](#troubleshooting-guide)
7. [Manual Recovery Procedures](#manual-recovery-procedures)
8. [Security Incident Response](#security-incident-response)

---

## 🏗️ SYSTEM OVERVIEW

### Purpose
The Zodiac App Secret Rotation System provides automated, zero-downtime rotation of all critical secrets including API keys, Apple shared secrets, Firebase configuration, and encryption keys.

### Key Components
- **AWS Secrets Manager**: Central secret storage
- **Railway Platform**: Deployment and environment management
- **Rotation Scripts**: Automated rotation workflows
- **Monitoring System**: Real-time health and expiration tracking
- **Alert System**: Slack, Teams, and email notifications

### Environments
- **Production**: Live application environment
- **Staging**: Testing and validation environment

---

## 🔄 SECRET ROTATION ARCHITECTURE

### Supported Secret Types

| Secret Type | Production | Staging | Rotation Schedule | Criticality |
|-------------|------------|---------|-------------------|-------------|
| API Keys | ✅ | ✅ | Weekly | Critical |
| Apple Shared Secrets | ✅ | ✅ (Sandbox) | Weekly | Critical |
| Firebase Config | ✅ | ✅ | Weekly | High |
| JWT Secrets | ✅ | ✅ | Weekly | Critical |
| Encryption Keys | ✅ | ✅ | Monthly | Critical |

### Storage Structure

```
AWS Secrets Manager:
zodiac-app/
├── api-keys/
│   ├── production
│   └── staging
├── apple-shared-secrets/
│   ├── production
│   └── sandbox
├── firebase-config/
│   ├── production
│   └── staging
├── jwt-secrets/
│   ├── production
│   └── staging
└── encryption-keys/
    ├── production
    └── staging
```

### Railway Environment Variables

```bash
# Production Environment
ZODIAC_API_KEY_PRODUCTION=<rotated-automatically>
APPLE_SHARED_SECRET_PRODUCTION=<rotated-automatically>
JWT_SECRET_PRODUCTION=<rotated-automatically>
ENCRYPTION_KEY_PRODUCTION=<rotated-automatically>

# Staging Environment
ZODIAC_API_KEY_STAGING=<rotated-automatically>
APPLE_SHARED_SECRET_SANDBOX=<rotated-automatically>
JWT_SECRET_STAGING=<rotated-automatically>
ENCRYPTION_KEY_STAGING=<rotated-automatically>
```

---

## 🤖 AUTOMATED ROTATION PROCEDURES

### Standard Rotation Process

The automated rotation follows this zero-downtime workflow:

1. **Pre-rotation Backup**
   ```bash
   ./scripts/rotate_secrets.sh backup production
   ```

2. **Secret Generation**
   - New secrets are generated with appropriate entropy
   - Format validation ensures compatibility

3. **AWS Secrets Manager Update**
   - New secrets stored in AWS Secrets Manager
   - Old secrets retained for rollback capability

4. **Railway Environment Update**
   - Environment variables updated via Railway API
   - Blue-green deployment pattern used

5. **Health Check Validation**
   - Application health endpoints tested
   - Secret accessibility verified
   - Performance metrics monitored

6. **Rollback on Failure**
   - Automatic rollback if health checks fail
   - Alert notifications sent immediately

### Scheduled Rotation

```bash
# Weekly rotation (Sundays at 02:00 UTC)
0 2 * * 0 /path/to/zodiac_app/scripts/rotate_secrets.sh rotate all

# Daily monitoring (Every day at 06:00 UTC)
0 6 * * * /path/to/zodiac_app/scripts/monitor_secrets.sh monitor
```

### Manual Rotation Commands

```bash
# Rotate all environments
./scripts/rotate_secrets.sh rotate all

# Rotate specific environment
./scripts/rotate_secrets.sh rotate production

# Force rotation (ignores schedule)
./scripts/rotate_secrets.sh rotate production --force

# Check rotation status
./scripts/rotate_secrets.sh status
```

---

## 🚨 EMERGENCY ROTATION PROCEDURES

### When to Perform Emergency Rotation

**IMMEDIATE ROTATION REQUIRED:**
- Secret compromise detected
- Unauthorized access to systems
- Failed security audit
- Developer credential leak
- Third-party breach notification

**WITHIN 24 HOURS:**
- Employee departure with system access
- Suspicious authentication patterns
- Compliance requirement changes

### Emergency Rotation Steps

#### Step 1: Assess the Situation
```bash
# Check current secret status
./scripts/monitor_secrets.sh status

# Verify system health
./scripts/monitor_secrets.sh health production
./scripts/monitor_secrets.sh health staging
```

#### Step 2: Execute Emergency Rotation
```bash
# Rotate all secrets immediately
./scripts/rotate_secrets.sh emergency all

# Or rotate specific environment
./scripts/rotate_secrets.sh emergency production
```

#### Step 3: Validate Rotation Success
```bash
# Verify new secrets are working
./scripts/rotate_secrets.sh validate production

# Check application health
curl -f https://zodiac-app-production.railway.app/health

# Monitor for 15 minutes
./scripts/monitor_secrets.sh monitor
```

#### Step 4: Document and Report
1. Document the incident in security log
2. Update incident response tickets
3. Notify stakeholders via established channels
4. Schedule post-incident review

### Emergency Contacts

| Role | Contact | Method | Response SLA |
|------|---------|--------|--------------|
| Security Lead | security-lead@zodiac-app.com | Email/Slack | 15 minutes |
| DevOps Manager | devops@zodiac-app.com | Email/Phone | 30 minutes |
| CTO | cto@zodiac-app.com | Phone | 1 hour |
| Legal/Compliance | legal@zodiac-app.com | Email | 4 hours |

---

## 🔍 MONITORING AND ALERTING

### Monitoring Dashboard

Access the real-time monitoring dashboard:
```bash
# Generate current dashboard
./scripts/monitor_secrets.sh dashboard

# Open dashboard (macOS)
open logs/secret_dashboard.html
```

### Alert Levels

#### 🟢 INFO
- Normal rotation completed
- Monitoring cycle completed
- Dashboard updated

#### 🟡 WARNING
- Secret expires in 30+ days
- Monitoring delay detected
- Non-critical health check failure

#### 🔴 CRITICAL
- Secret expires in <7 days
- Secret missing or inaccessible
- Rotation failure
- Health check failure
- Emergency rotation triggered

### Alert Channels

#### Slack Integration
```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
./scripts/monitor_secrets.sh monitor
```

#### Microsoft Teams Integration
```bash
export TEAMS_WEBHOOK_URL="https://your-tenant.webhook.office.com/webhookb2/YOUR-WEBHOOK-URL"
./scripts/monitor_secrets.sh monitor
```

#### Email Alerts
```bash
export ALERT_EMAIL="security-team@zodiac-app.com"
./scripts/monitor_secrets.sh monitor
```

### Monitoring Schedule

```bash
# Setup automated monitoring (every 15 minutes)
./scripts/monitor_secrets.sh schedule "*/15 * * * *"

# Setup daily reporting (06:00 UTC)
./scripts/monitor_secrets.sh schedule "0 6 * * *"
```

---

## 🔧 TROUBLESHOOTING GUIDE

### Common Issues and Solutions

#### Issue: Rotation Script Fails with AWS Error

**Symptoms:**
```
❌ Cannot authenticate with AWS
❌ Failed to rotate secret: zodiac-app/api-keys/production
```

**Diagnosis:**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Check AWS region
echo $AWS_REGION

# Test AWS Secrets Manager access
aws secretsmanager list-secrets --region us-west-2
```

**Resolution:**
1. Verify AWS credentials are set correctly in Railway
2. Confirm IAM permissions include SecretsManager actions
3. Check AWS region configuration

#### Issue: Railway Environment Update Fails

**Symptoms:**
```
❌ Failed to update Railway variable: ZODIAC_API_KEY_PRODUCTION
🚂 Railway environment update failed
```

**Diagnosis:**
```bash
# Check Railway CLI installation
railway --version

# Test Railway authentication
railway login --check

# List Railway projects
railway list
```

**Resolution:**
1. Re-authenticate with Railway CLI
2. Verify RAILWAY_TOKEN environment variable
3. Check project permissions and access

#### Issue: Health Check Failures After Rotation

**Symptoms:**
```
❌ Health check failed for production after 10 attempts
⏪ Rolling back secrets for production
```

**Diagnosis:**
```bash
# Check application logs
railway logs --environment production

# Test endpoints directly
curl -v https://zodiac-app-production.railway.app/health

# Check secret accessibility
./scripts/rotate_secrets.sh validate production
```

**Resolution:**
1. Review application logs for authentication errors
2. Verify new secrets are correctly formatted
3. Check for deployment delays
4. Manual rollback if necessary

#### Issue: Monitoring Alerts Not Sent

**Symptoms:**
- No alerts received despite issues
- Webhook failures in logs

**Diagnosis:**
```bash
# Test webhook URLs manually
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test alert"}' $SLACK_WEBHOOK_URL

# Check alert processing
./scripts/monitor_secrets.sh alerts
```

**Resolution:**
1. Verify webhook URLs are correct and active
2. Test webhook permissions
3. Check firewall/network restrictions

### Performance Troubleshooting

#### Slow Rotation Times

**Target Performance:**
- Secret generation: <5 seconds
- AWS update: <10 seconds
- Railway update: <30 seconds
- Health check: <60 seconds
- Total rotation: <2 minutes

**Optimization Steps:**
1. Check AWS region latency
2. Verify Railway API performance
3. Optimize health check timeout values
4. Review network connectivity

---

## 🛠️ MANUAL RECOVERY PROCEDURES

### Manual Secret Rotation

If automated rotation fails completely:

#### Step 1: Generate New Secrets Manually

```bash
# API Key
new_api_key="zodiac_api_$(date +%s)_$(openssl rand -hex 16)"

# Apple Shared Secret  
new_apple_secret=$(openssl rand -hex 32)

# JWT Secret
new_jwt_secret=$(openssl rand -base64 64 | tr -d '\n')

# Encryption Key
new_encryption_key=$(openssl rand -hex 32)
```

#### Step 2: Update AWS Secrets Manager

```bash
# Update each secret manually
aws secretsmanager put-secret-value \
  --secret-id "zodiac-app/api-keys/production" \
  --secret-string "$new_api_key" \
  --region us-west-2

aws secretsmanager put-secret-value \
  --secret-id "zodiac-app/apple-shared-secrets/production" \
  --secret-string "$new_apple_secret" \
  --region us-west-2

# Continue for all secrets...
```

#### Step 3: Update Railway Environment

```bash
# Using Railway CLI
railway variables set ZODIAC_API_KEY_PRODUCTION="$new_api_key" --environment production
railway variables set APPLE_SHARED_SECRET_PRODUCTION="$new_apple_secret" --environment production
railway variables set JWT_SECRET_PRODUCTION="$new_jwt_secret" --environment production
railway variables set ENCRYPTION_KEY_PRODUCTION="$new_encryption_key" --environment production
```

#### Step 4: Trigger Railway Deployment

```bash
# Force deployment with new environment variables
railway up --environment production
```

#### Step 5: Validate Manually

```bash
# Test application endpoints
curl -f https://zodiac-app-production.railway.app/health
curl -f https://zodiac-app-production.railway.app/api/status

# Test secret functionality
flutter test test/services/secret_manager_service_test.dart
```

### Disaster Recovery from Backups

If complete system failure occurs:

#### Step 1: Locate Most Recent Backup

```bash
# List available backups
ls -la backups/secrets/

# Find latest production backup
ls -la backups/secrets/secrets_production_*.json | tail -1
```

#### Step 2: Restore from Backup

```bash
# Use the rollback function with backup file
./scripts/rotate_secrets.sh rollback production backups/secrets/secrets_production_20250908_020000.json
```

#### Step 3: Validate Restoration

```bash
# Verify all secrets are accessible
./scripts/rotate_secrets.sh validate production

# Check application functionality
./scripts/monitor_secrets.sh health production
```

### Database Recovery

If secret metadata corruption occurs:

```sql
-- Connect to production database
-- Verify secret rotation timestamps

SELECT environment, last_rotation, next_rotation_due 
FROM secret_rotation_log 
ORDER BY last_rotation DESC;

-- Update rotation timestamps if necessary
UPDATE secret_rotation_log 
SET last_rotation = NOW(), next_rotation_due = NOW() + INTERVAL '7 days'
WHERE environment = 'production';
```

---

## 🚨 SECURITY INCIDENT RESPONSE

### Incident Classification

#### Level 1: CRITICAL (Immediate Response)
- Secret compromise confirmed
- Active unauthorized access
- Data breach in progress
- Complete system compromise

**Response Time:** 15 minutes  
**Actions:**
1. Execute emergency rotation immediately
2. Notify security team and management
3. Activate incident response team
4. Document all actions

#### Level 2: HIGH (1-Hour Response)
- Suspected secret compromise
- Failed security validation
- Unusual access patterns
- Third-party security notification

**Response Time:** 1 hour  
**Actions:**
1. Investigate and assess threat
2. Prepare for emergency rotation
3. Notify security team
4. Monitor system closely

#### Level 3: MEDIUM (4-Hour Response)
- Scheduled rotation failures
- Monitoring system alerts
- Compliance issues
- Process violations

**Response Time:** 4 hours  
**Actions:**
1. Investigate root cause
2. Plan corrective actions
3. Update procedures if necessary
4. Schedule remediation

### Incident Response Playbook

#### Immediate Response (0-15 minutes)

1. **Assess Severity**
   ```bash
   # Check system status immediately
   ./scripts/monitor_secrets.sh status
   ./scripts/monitor_secrets.sh health production
   ./scripts/monitor_secrets.sh health staging
   ```

2. **Secure the Environment**
   ```bash
   # Execute emergency rotation
   ./scripts/rotate_secrets.sh emergency all
   ```

3. **Notify Stakeholders**
   - Send alert to security team Slack channel
   - Call security lead if outside business hours
   - Create incident ticket in system

#### Investigation Phase (15-60 minutes)

1. **Collect Evidence**
   ```bash
   # Gather logs
   cp logs/secret_rotation.log investigation/incident_$(date +%Y%m%d_%H%M%S)/
   cp logs/secret_monitoring.log investigation/incident_$(date +%Y%m%d_%H%M%S)/
   
   # Generate detailed status report
   ./scripts/monitor_secrets.sh monitor > investigation/incident_$(date +%Y%m%d_%H%M%S)/status_report.txt
   ```

2. **Analyze Impact**
   - Review application logs for suspicious activity
   - Check access logs for unauthorized attempts
   - Verify data integrity
   - Assess potential data exposure

3. **Document Timeline**
   - Record when incident was discovered
   - Note all actions taken with timestamps
   - Identify potential root causes

#### Recovery Phase (1-4 hours)

1. **Validate Security**
   ```bash
   # Confirm all secrets rotated successfully
   ./scripts/rotate_secrets.sh validate production
   ./scripts/rotate_secrets.sh validate staging
   
   # Run comprehensive monitoring
   ./scripts/monitor_secrets.sh monitor
   ```

2. **Restore Normal Operations**
   - Verify application functionality
   - Run integration tests
   - Monitor error rates and performance

3. **Update Security Measures**
   - Apply additional security controls if needed
   - Update monitoring rules
   - Enhance detection capabilities

#### Post-Incident Activities (4-24 hours)

1. **Conduct Post-Mortem**
   - Schedule incident review meeting
   - Analyze root cause
   - Identify preventive measures

2. **Update Documentation**
   - Update runbooks based on lessons learned
   - Enhance procedures if necessary
   - Update incident response playbook

3. **Implement Improvements**
   - Deploy additional monitoring
   - Enhance automation
   - Update training materials

### Communication Templates

#### Initial Incident Notification

```
🚨 SECURITY INCIDENT - ZODIAC APP

Incident ID: INC-$(date +%Y%m%d%H%M%S)
Severity: [CRITICAL|HIGH|MEDIUM]
Environment: [Production|Staging|All]

Issue: [Brief description of the incident]
Impact: [Assessment of potential impact]
Actions Taken: [List of immediate actions]

Status: [Under Investigation|Contained|Resolved]
Next Update: [Time for next update]

Contact: security-lead@zodiac-app.com
```

#### Incident Resolution Notification

```
✅ INCIDENT RESOLVED - ZODIAC APP

Incident ID: INC-$(date +%Y%m%d%H%M%S)
Duration: [Total incident duration]
Impact: [Final assessment of impact]

Resolution: [Summary of resolution actions]
Root Cause: [Identified root cause]
Preventive Actions: [List of preventive measures implemented]

Post-Mortem: Scheduled for [Date/Time]
Report: Will be available within 48 hours

Thank you for your support during this incident.
```

---

## 📊 OPERATIONAL METRICS

### Key Performance Indicators

#### Rotation Success Rate
- **Target:** 99.9%
- **Measurement:** Successful rotations / Total rotation attempts
- **Alert Threshold:** <95%

#### Mean Time to Rotate
- **Target:** <2 minutes
- **Measurement:** Average rotation completion time
- **Alert Threshold:** >5 minutes

#### Secret Age Compliance
- **Target:** 100% within policy
- **Measurement:** Secrets rotated within schedule / Total secrets
- **Alert Threshold:** <98%

#### Health Check Success Rate
- **Target:** 99.5%
- **Measurement:** Successful health checks / Total health checks
- **Alert Threshold:** <95%

#### Incident Response Time
- **Target:** <15 minutes for critical
- **Measurement:** Time from alert to response action
- **Alert Threshold:** >30 minutes

### Reporting Schedule

#### Daily Reports
- Secret status summary
- Health check results
- Alert summary
- Performance metrics

#### Weekly Reports
- Rotation success rates
- Trending analysis
- Security posture assessment
- Operational improvements

#### Monthly Reports
- Comprehensive security review
- Incident analysis
- Process optimization recommendations
- Compliance assessment

---

## 📚 APPENDICES

### Appendix A: Secret Formats and Validation

#### API Key Format
```
Pattern: zodiac_api_[timestamp]_[32-char-hex]
Example: zodiac_api_1694208000_a1b2c3d4e5f6789012345678901234567890abcd
Validation: /^zodiac_api_\d{10}_[a-f0-9]{32}$/
```

#### Apple Shared Secret Format
```
Pattern: 64-character hexadecimal string
Example: a1b2c3d4e5f67890123456789012345678901234567890abcdef1234567890ab
Validation: /^[a-f0-9]{64}$/
```

#### JWT Secret Format
```
Pattern: Base64-encoded string (64 bytes)
Example: YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY3ODkwYWJjZGVmZ2hpams=
Validation: Base64 validation + length check
```

### Appendix B: AWS IAM Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue",
                "secretsmanager:PutSecretValue",
                "secretsmanager:CreateSecret",
                "secretsmanager:UpdateSecret",
                "secretsmanager:DescribeSecret",
                "secretsmanager:ListSecrets"
            ],
            "Resource": [
                "arn:aws:secretsmanager:us-west-2:*:secret:zodiac-app/*"
            ]
        }
    ]
}
```

### Appendix C: Railway Environment Variables

```bash
# Core AWS Configuration
AWS_ACCESS_KEY_ID=<provided_by_railway>
AWS_SECRET_ACCESS_KEY=<provided_by_railway>
AWS_REGION=us-west-2

# Production Secrets (Managed by rotation system)
ZODIAC_API_KEY_PRODUCTION=<managed>
APPLE_SHARED_SECRET_PRODUCTION=<managed>
JWT_SECRET_PRODUCTION=<managed>
ENCRYPTION_KEY_PRODUCTION=<managed>
FIREBASE_CONFIG_PRODUCTION=<managed>

# Staging Secrets (Managed by rotation system)
ZODIAC_API_KEY_STAGING=<managed>
APPLE_SHARED_SECRET_SANDBOX=<managed>
JWT_SECRET_STAGING=<managed>
ENCRYPTION_KEY_STAGING=<managed>
FIREBASE_CONFIG_STAGING=<managed>

# Monitoring and Alerting
SLACK_WEBHOOK_URL=<optional>
TEAMS_WEBHOOK_URL=<optional>
ALERT_EMAIL=<optional>
```

---

**END OF RUNBOOK**

*This document is maintained by the Security Operations Team and should be reviewed quarterly or after any significant security incidents.*

*Version Control: This document is version-controlled in the project repository under `/SECURITY_SECRET_ROTATION_RUNBOOK.md`*

*Last Review: September 8, 2025*  
*Next Review: December 8, 2025*