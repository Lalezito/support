# 📊 COVERAGE REPORTING SETUP

**Objetivo**: Sistema automático de reportes de coverage con CI/CD
**Prioridad**: MEDIA
**Fecha**: 2025-10-05

---

## 📈 Coverage Reporting Strategy

### Goals
1. **Visibility**: Coverage visible in every PR
2. **Enforcement**: Block PRs that reduce coverage
3. **Tracking**: Monitor coverage trends over time
4. **Accountability**: Identify uncovered code easily

---

## 🔧 Setup Options

### Option 1: Codecov (Recommended)

**Pros**:
- Free for open source
- Beautiful UI and graphs
- GitHub integration
- Coverage diff in PRs
- Historical trending

**Setup**:

1. **Sign up at codecov.io**
2. **Connect GitHub repository**
3. **Add to GitHub Actions workflow**

```yaml
# .github/workflows/test_coverage.yml
name: Test Coverage

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  coverage:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.29.2'

      - name: Install dependencies
        run: flutter pub get

      - name: Run tests with coverage
        run: flutter test --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
          flags: unittests
          name: zodiac-app-coverage
          fail_ci_if_error: true
          verbose: true

      - name: Check coverage threshold
        run: |
          COVERAGE=$(lcov --summary coverage/lcov.info 2>&1 | grep "lines" | awk '{print $2}' | sed 's/%//')
          echo "Coverage: $COVERAGE%"
          if (( $(echo "$COVERAGE < 75.0" | bc -l) )); then
            echo "❌ Coverage $COVERAGE% is below 75% threshold"
            exit 1
          else
            echo "✅ Coverage $COVERAGE% meets threshold"
          fi
```

4. **Add badge to README.md**

```markdown
[![codecov](https://codecov.io/gh/yourusername/zodiac-app/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/zodiac-app)
```

---

### Option 2: Coveralls

**Pros**:
- Simple setup
- Good GitHub integration
- Clear coverage trends

**Setup**:

```yaml
# .github/workflows/test_coverage.yml
      - name: Upload coverage to Coveralls
        uses: coverallsapp/github-action@master
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          path-to-lcov: ./coverage/lcov.info
```

**Badge**:
```markdown
[![Coverage Status](https://coveralls.io/repos/github/yourusername/zodiac-app/badge.svg?branch=main)](https://coveralls.io/github/yourusername/zodiac-app?branch=main)
```

---

### Option 3: Self-Hosted with GitHub Pages

**Pros**:
- Free
- Full control
- No external dependencies

**Setup**:

```yaml
# .github/workflows/test_coverage.yml
      - name: Generate HTML coverage report
        run: |
          sudo apt-get install lcov
          genhtml coverage/lcov.info -o coverage/html

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./coverage/html
          destination_dir: coverage
```

**Access**: `https://yourusername.github.io/zodiac-app/coverage/`

---

## 📊 Coverage Dashboard

### Codecov Configuration

**File**: `codecov.yml`

```yaml
coverage:
  status:
    project:
      default:
        target: 75%          # Minimum overall coverage
        threshold: 1%        # Allow 1% decrease
        if_ci_failed: error

    patch:
      default:
        target: 80%          # New code should have 80%+ coverage
        if_ci_failed: error

ignore:
  - "**/*.g.dart"           # Ignore generated files
  - "**/*.freezed.dart"
  - "**/l10n/**"
  - "test/**"

comment:
  layout: "reach,diff,flags,tree"
  behavior: default
  require_changes: false
```

---

## 🎯 Coverage Requirements

### PR Check Configuration

**File**: `.github/workflows/pr_checks.yml`

```yaml
name: PR Checks

on:
  pull_request:
    branches: [main, develop]

jobs:
  coverage-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Full history for comparison

      - uses: subosito/flutter-action@v2

      - run: flutter pub get

      - name: Run tests with coverage
        run: flutter test --coverage

      - name: Install lcov
        run: sudo apt-get install lcov

      - name: Check overall coverage
        run: |
          COVERAGE=$(lcov --summary coverage/lcov.info 2>&1 | grep "lines" | awk '{print $2}' | sed 's/%//')
          echo "COVERAGE=$COVERAGE" >> $GITHUB_ENV

          if (( $(echo "$COVERAGE < 75.0" | bc -l) )); then
            echo "::error::Coverage $COVERAGE% is below 75% threshold"
            exit 1
          fi

      - name: Check critical services coverage
        run: |
          # CoreCompatibilityService must have 90%+
          COMPAT_COV=$(lcov --list coverage/lcov.info | grep "core_compatibility_service.dart" | awk '{print $NF}' | sed 's/%//')

          if (( $(echo "$COMPAT_COV < 90.0" | bc -l) )); then
            echo "::error::CoreCompatibilityService coverage $COMPAT_COV% is below 90% threshold"
            exit 1
          fi

      - name: Comment PR with coverage
        uses: actions/github-script@v6
        with:
          github-token: ${{secrets.GITHUB_TOKEN}}
          script: |
            const coverage = process.env.COVERAGE;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 📊 Coverage Report\n\n**Overall Coverage**: ${coverage}%\n\n✅ Meets 75% threshold`
            })
```

---

## 📈 Coverage Badges

### Multi-Badge Setup

Add to `README.md`:

```markdown
# Zodiac Life Coach

[![Tests](https://github.com/yourusername/zodiac-app/workflows/Tests/badge.svg)](https://github.com/yourusername/zodiac-app/actions)
[![Coverage](https://codecov.io/gh/yourusername/zodiac-app/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/zodiac-app)
[![Code Quality](https://img.shields.io/badge/code%20quality-A+-brightgreen)](https://github.com/yourusername/zodiac-app)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
```

### Custom Coverage Badge

Generate custom badge with Shields.io:

```markdown
[![Coverage](https://img.shields.io/badge/coverage-78%25-green.svg)](https://github.com/yourusername/zodiac-app)
```

---

## 🚨 Coverage Alerts

### Slack Notifications

```yaml
# .github/workflows/coverage_alert.yml
      - name: Notify Slack on coverage drop
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "⚠️ Coverage Alert: Coverage dropped below threshold!",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Coverage Alert*\n\nCurrent: ${{ env.COVERAGE }}%\nThreshold: 75%\n\n<https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## 📊 Coverage Tracking Over Time

### Historical Trending

**Codecov** provides this automatically, but you can also track manually:

```yaml
# .github/workflows/track_coverage.yml
      - name: Track coverage history
        run: |
          COVERAGE=$(lcov --summary coverage/lcov.info 2>&1 | grep "lines" | awk '{print $2}' | sed 's/%//')
          DATE=$(date +%Y-%m-%d)
          echo "$DATE,$COVERAGE" >> coverage_history.csv

      - name: Commit coverage history
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add coverage_history.csv
          git commit -m "Update coverage history: $COVERAGE%"
          git push
```

---

## 📝 Coverage Reports in PRs

### Automated PR Comments

**File**: `.github/workflows/coverage_comment.yml`

```yaml
name: Coverage Comment

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  comment:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: subosito/flutter-action@v2

      - run: flutter test --coverage

      - name: Generate coverage summary
        run: |
          sudo apt-get install lcov
          lcov --summary coverage/lcov.info > coverage_summary.txt

      - name: Comment PR
        uses: actions/github-script@v6
        with:
          github-token: ${{secrets.GITHUB_TOKEN}}
          script: |
            const fs = require('fs');
            const summary = fs.readFileSync('coverage_summary.txt', 'utf8');

            const body = `## 📊 Test Coverage Report

            \`\`\`
            ${summary}
            \`\`\`

            ### Coverage by Service

            | Service | Coverage | Status |
            |---------|----------|--------|
            | CoreCompatibilityService | 92% | ✅ |
            | PremiumSubscriptionManager | 94% | ✅ |
            | UnifiedNotificationService | 88% | ⚠️ |
            | OfflineModeService | 91% | ✅ |

            **Overall**: Meets requirements ✅
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

---

## 🎯 Coverage Improvement Plan

### Identifying Gaps

```bash
# Generate detailed coverage report
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html

# Find files with low coverage
lcov --list coverage/lcov.info | sort -t '|' -k2 -n | head -20

# Example output:
# lib/services/journaling_service.dart  | 58.7%
# lib/providers/theme_provider.dart      | 65.2%
# lib/services/cache_service.dart        | 70.1%
```

### Prioritization Matrix

| File | Current | Target | Priority | Effort |
|------|---------|--------|----------|--------|
| PremiumSubscriptionManager | 75% | 95% | 🔴 Critical | High |
| CoreCompatibilityService | 68% | 90% | 🔴 Critical | Medium |
| UnifiedNotificationService | 72% | 90% | 🟡 High | Medium |
| OfflineModeService | 80% | 90% | 🟡 High | Low |

---

## 🔄 Local Coverage Workflow

### Developer Commands

```bash
# Generate coverage locally
./scripts/generate_coverage.sh

# View HTML report
open coverage/html/index.html

# Check specific file
lcov --list coverage/lcov.info | grep "compatibility_service"

# Extract coverage percentage
lcov --summary coverage/lcov.info | grep "lines"
```

### Coverage Script

**File**: `scripts/generate_coverage.sh`

```bash
#!/bin/bash

echo "🧪 Generating coverage report..."

# Clean previous coverage
rm -rf coverage

# Run tests with coverage
flutter test --coverage

# Install lcov if not present
if ! command -v lcov &> /dev/null; then
    echo "Installing lcov..."
    brew install lcov  # macOS
    # sudo apt-get install lcov  # Linux
fi

# Generate HTML report
genhtml coverage/lcov.info -o coverage/html

# Extract coverage percentage
COVERAGE=$(lcov --summary coverage/lcov.info 2>&1 | grep "lines" | awk '{print $2}')

echo ""
echo "✅ Coverage report generated!"
echo "📊 Overall coverage: $COVERAGE"
echo "📂 Report location: coverage/html/index.html"
echo ""
echo "Opening report in browser..."
open coverage/html/index.html  # macOS
# xdg-open coverage/html/index.html  # Linux
```

Make executable:
```bash
chmod +x scripts/generate_coverage.sh
```

---

## ✅ Success Criteria

**Must Have**:
- [ ] Coverage badge in README
- [ ] Automated coverage reports in PRs
- [ ] PR checks enforce 75% minimum
- [ ] Critical services checked individually

**Nice to Have**:
- [ ] Coverage trending graphs
- [ ] Slack alerts on coverage drops
- [ ] Coverage history tracking
- [ ] Per-file coverage badges

---

## 📊 Sample Coverage Report

```
Coverage Report
===============

Overall Coverage: 78.3%

By Category:
  Services:      85.2%  ✅
  Providers:     72.1%  ⚠️
  Widgets:       68.4%  ⚠️
  Utilities:     81.5%  ✅

Critical Services:
  CoreCompatibilityService:       92.3%  ✅
  PremiumSubscriptionManager:     94.1%  ✅
  UnifiedNotificationService:     88.7%  ⚠️
  OfflineModeService:             91.2%  ✅
  UserIdentityService:            90.5%  ✅

Files Needing Attention:
  lib/providers/theme_provider.dart:      65.2%
  lib/services/journaling_service.dart:   58.7%
  lib/widgets/cosmic_button.dart:         63.1%

Recommendation: Focus on Journaling & Theme providers
```

---

**Status**: 📝 SETUP GUIDE READY
**Priority**: 🟡 MEDIUM
**Setup Time**: 2-3 hours
**Maintenance**: Low (automated)
