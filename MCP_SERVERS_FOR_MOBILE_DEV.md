# MCP Servers for Mobile App Development & App Store Submission

**Research Date:** February 6, 2026
**Project:** Arcanapp (Flutter wellness app with 6-language localization)
**Context:** App going through Apple review (rejected under 4.3b Spam)

This document catalogs practical, installable MCP (Model Context Protocol) servers that can help with Flutter development, App Store submission, localization, analytics, and marketing.

---

## Table of Contents

1. [App Store & Developer Portal](#1-app-store--developer-portal)
2. [Flutter & Dart Development](#2-flutter--dart-development)
3. [Localization & Translation](#3-localization--translation)
4. [Mobile Automation & Testing](#4-mobile-automation--testing)
5. [Screenshots & Design](#5-screenshots--design)
6. [Analytics & Monitoring](#6-analytics--monitoring)
7. [In-App Purchases](#7-in-app-purchases)
8. [Additional Resources](#8-additional-resources)

---

## 1. App Store & Developer Portal

### 1.1 App Store Connect MCP Server ⭐⭐⭐⭐⭐

**Relevance Score: 5/5** - Critical for managing App Store submissions, beta testing, and analytics

**What it does:**
- Manage apps, beta testers, bundle IDs, devices, and user access
- Download sales and finance reports
- Access App Store analytics
- Manage App Store version localizations
- List beta feedback and screenshots
- Control Xcode Cloud builds

**GitHub:** [JoshuaRileyDev/app-store-connect-mcp-server](https://github.com/JoshuaRileyDev/app-store-connect-mcp-server)

**Installation:**
```bash
# Recommended (using Smithery)
npx @smithery/cli install appstore-connect-mcp-server --client claude

# Or manual
npm install @joshuarileydev/app-store-connect-mcp-server
```

**Configuration for Claude Code:**

Add to `.claude/settings.json`:
```json
{
  "mcpServers": {
    "app-store-connect": {
      "command": "npx",
      "args": ["-y", "appstore-connect-mcp-server"],
      "env": {
        "APP_STORE_CONNECT_KEY_ID": "YOUR_KEY_ID",
        "APP_STORE_CONNECT_ISSUER_ID": "YOUR_ISSUER_ID",
        "APP_STORE_CONNECT_P8_PATH": "/path/to/auth-key.p8",
        "APP_STORE_CONNECT_VENDOR_NUMBER": "YOUR_VENDOR_NUMBER_OPTIONAL"
      }
    }
  }
}
```

**Authentication:**
1. Go to App Store Connect → Users and Access → Integrations → App Store Connect API
2. Generate API Key and download the `.p8` private key file
3. Note your Key ID and Issuer ID
4. (Optional) Add vendor number for sales/finance reports

**Available Tools:**
- `list_apps`, `get_app_info`
- `list_beta_groups`, `list_group_testers`, `add_tester_to_group`, `remove_tester_from_group`
- `create_app_store_version`, `list_app_store_versions`
- `list_app_store_version_localizations`, `get_app_store_version_localization`, `update_app_store_version_localization`
- `create_bundle_id`, `list_bundle_ids`, `get_bundle_id_info`
- `enable_bundle_capability`, `disable_bundle_capability`
- `list_registered_devices`
- `list_team_members`
- `create_analytics_report`, `download_app_store_analytics`
- `download_sales_report`, `download_finance_report`
- `list_xcode_schemes`
- `list_beta_feedback_screenshots`, `get_beta_feedback_screenshot`

**Sources:**
- [GitHub Repository](https://github.com/JoshuaRileyDev/app-store-connect-mcp-server)
- [MCP.so Profile](https://mcp.so/server/app-store-connect-mcp-server)
- [Glama.ai Listing](https://glama.ai/mcp/servers/@JoshuaRileyDev/app-store-connect-mcp-server)

**Alternative implementations:**
- [TrialAndErrorAI/appstore-connect-mcp](https://github.com/TrialAndErrorAI/appstore-connect-mcp)
- [gjeltep/app-store-connect-mcp](https://github.com/gjeltep/app-store-connect-mcp)
- [Stig-Johnny/appstoreconnect-mcp](https://github.com/Stig-Johnny/appstoreconnect-mcp) - Xcode Cloud builds
- [SardorbekR/appstore-connect-mcp](https://github.com/SardorbekR/appstore-connect-mcp)

---

### 1.2 Apple Developer Documentation MCP Servers ⭐⭐⭐⭐

**Relevance Score: 4/5** - Helpful for understanding iOS/Swift APIs and guidelines

**What they do:**
- Search iOS/macOS/SwiftUI/UIKit documentation
- Access WWDC videos and code examples
- Search Apple Human Interface Guidelines (HIG)
- Get framework-specific documentation

**GitHub:**
- [MightyDillah/apple-doc-mcp](https://github.com/MightyDillah/apple-doc-mcp) - Smart search with wildcards
- [kimsungwhee/apple-docs-mcp](https://github.com/kimsungwhee/apple-docs-mcp) - Comprehensive docs + WWDC
- [tmaasen/apple-dev-mcp](https://github.com/tmaasen/apple-dev-mcp) - HIG + Dev Docs

**Related:**
- [sosumi.ai](https://sosumi.ai/) - Apple docs translated to AI-friendly Markdown

**Sources:**
- [Apple Doc MCP on MCPmarket](https://mcpmarket.com/server/apple-doc)
- [GitHub: apple-doc-mcp](https://github.com/MightyDillah/apple-doc-mcp)
- [PulseMCP Profile](https://www.pulsemcp.com/servers/apple-developer-documentation)

---

## 2. Flutter & Dart Development

### 2.1 Official Dart & Flutter MCP Server ⭐⭐⭐⭐⭐

**Relevance Score: 5/5** - Essential for Flutter development with AI assistance

**What it does:**
- Analyze and fix errors in Dart/Flutter code
- Resolve symbols and fetch documentation
- Format code using `dart format` config
- Search pub.dev for packages and add dependencies
- Run tests and analyze results
- **Introspect running Flutter apps** (widget tree, runtime errors)
- Identify and fix layout issues

**Official Docs:** [docs.flutter.dev/ai/mcp-server](https://docs.flutter.dev/ai/mcp-server)

**Installation for Claude Code:**
```bash
claude mcp add --transport stdio dart -- dart mcp-server
```

**Requirements:**
- Dart SDK 3.9 or later
- Status: Experimental (subject to rapid evolution)

**Key Features:**
- Code analysis & fixing
- Package management (pub.dev search, dependency management)
- Application introspection (widget tree, runtime errors)
- Testing & quality checks
- Static and runtime analysis

**Sources:**
- [Flutter Official Docs](https://docs.flutter.dev/ai/mcp-server)
- [Flutter Blog: Supercharge Your Development](https://blog.flutter.dev/supercharge-your-dart-flutter-development-experience-with-the-dart-mcp-server-2edcc8107b49)
- [freeCodeCamp Guide](https://www.freecodecamp.org/news/how-to-use-the-model-context-protocol-mcp-with-flutter-and-dart/)

---

### 2.2 DCM (Dart Code Metrics) MCP Server ⭐⭐⭐⭐

**Relevance Score: 4/5** - Advanced code quality analysis for production apps

**What it does:**
- Analyze and fix errors with custom rules
- Detect unused code, files, and dependencies
- Calculate code metrics and complexity
- Widget and image asset analysis
- Code formatting and baseline generation
- Technical debt management

**Official Docs:** [dcm.dev/docs/ide-integrations/mcp-server](https://dcm.dev/docs/ide-integrations/mcp-server)

**Installation for Claude Code:**
```bash
# Basic installation
claude mcp add --transport stdio dcm -- dcm start-mcp-server --client=claude-code

# With fallback for connection issues
claude mcp add --transport stdio dcm -- dcm start-mcp-server --force-roots-fallback --client=claude-code
```

**Configuration Scopes:**
- Local scope (default): Project-specific personal config
- Project scope: Shared team setup via `.mcp.json`
- User scope: Available across all projects

**Management Commands:**
```bash
claude mcp list          # View configured servers
claude mcp get dcm       # Details for DCM server
claude mcp remove dcm    # Uninstall DCM server
/mcp                     # Check status within Claude Code
```

**Sources:**
- [DCM Official Docs](https://dcm.dev/docs/ide-integrations/mcp-server)
- [DCM Blog: Agentic Code Quality](https://dcm.dev/blog/2025/08/25/agentic-code-quality-dcm-mcp/)

---

### 2.3 Flutter Tools MCP Server ⭐⭐⭐⭐

**Relevance Score: 4/5** - Streamlined Dart/Flutter diagnostics and fixes

**What it does:**
- `get_diagnostics` - Retrieve diagnostic information for Dart/Flutter files
- `apply_fixes` - Automatically apply suggested fixes

**Links:**
- [MCPmarket: Flutter Tools](https://mcpmarket.com/server/flutter-tools)
- [Glama: Flutter Tools by dkpoulsen](https://glama.ai/mcp/servers/@dkpoulsen/flutter-tools)

---

### 2.4 MCP Flutter (Dynamic Tooling) ⭐⭐⭐

**Relevance Score: 3/5** - Advanced runtime inspection for debugging

**What it does:**
- **Dynamic MCP tool registration** - Apps can register custom tools at runtime
- Error retrieval with duplicate filtering
- Screenshot capture with PNG compression
- View inspection (dimensions, pixel ratio, widget details)
- Requires Flutter app running in debug mode

**GitHub:** [Arenukvern/mcp_flutter](https://github.com/Arenukvern/mcp_flutter)

**Key Difference from Official Server:**
The official Dart MCP server exposes static Dart tooling, while this project enables Flutter apps to register custom, application-specific tools at runtime without server modifications.

**Installation:**
- AI-Assisted: Use prompt with [llm_install.md](https://github.com/Arenukvern/mcp_flutter/blob/main/llm_install.md)
- Manual: Review [QUICK_START.md](https://github.com/Arenukvern/mcp_flutter/blob/main/QUICK_START.md)

**Requirements:**
- Flutter app in debug mode
- Port matching (default 8181)
- `mcp_toolkit` package integration

**Sources:**
- [GitHub Repository](https://github.com/Arenukvern/mcp_flutter)
- [Glama Profile](https://glama.ai/mcp/servers/@Arenukvern/mcp_flutter)

---

### 2.5 MCP Mobile Server (Cross-Platform) ⭐⭐⭐⭐⭐

**Relevance Score: 5/5** - Comprehensive Flutter/iOS/Android development toolkit

**What it does:**
- **36 tools** across Flutter, Android, and iOS platforms
- Hot reload sessions with intelligent device selection
- Automated environment setup and dependency management
- iOS simulator discovery, control, and screenshots
- Xcode integration (macOS only)
- Production build generation (APK, App Bundle, IPA)
- Test suite execution with coverage analysis
- Self-healing build processes with automatic error resolution
- Multi-platform release builds with obfuscation

**GitHub:** [cristianoaredes/mcp-mobile-server](https://github.com/cristianoaredes/mcp-mobile-server)

**Installation:**
```bash
# Global install
npm install -g @cristianoaredes/mcp-mobile-server

# Or run directly with npx
npx @cristianoaredes/mcp-mobile-server
```

**Configuration for Claude Code:**

Add to `.claude/settings.json`:
```json
{
  "mcpServers": {
    "mobile-dev": {
      "command": "npx",
      "args": ["@cristianoaredes/mcp-mobile-server"]
    }
  }
}
```

**System Requirements:**

Minimum:
- Node.js 18.0+
- One of: Flutter, Android SDK, or Xcode

Recommended:
- Flutter 3.0+
- Android Studio or Android SDK
- Xcode 14+ (macOS only)
- VS Code with Flutter extension

**Initial Setup Commands:**
```bash
mcp-mobile-server health_check
mcp-mobile-server flutter_setup_environment --action=full
mcp-mobile-server flutter_dev_session --cwd=/path/to/project
```

**Platform Support:**
- ✅ macOS
- ✅ Linux
- ⚠️ Windows (in-progress)

**Sources:**
- [GitHub Repository](https://github.com/cristianoaredes/mcp-mobile-server)

---

### 2.6 Mobile MCP (Automation) ⭐⭐⭐⭐

**Relevance Score: 4/5** - Advanced mobile automation for testing and data extraction

**What it does:**
- Native app automation across iOS and Android for testing/data entry
- Screenshot and accessibility analysis
- Structured data extraction from screens
- Multi-step user journey automation (LLM-guided)
- Agent-to-agent communication for complex workflows

**GitHub:** [mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp)

**Installation for Claude Code:**
```bash
claude mcp add mobile-mcp -- npx -y @mobilenext/mobile-mcp@latest
```

**Supported Platforms:**
- ✅ iOS Real Device
- ✅ iOS Simulator
- ✅ Android Real Device
- ✅ Android Emulator

**System Requirements:**
- Xcode command line tools (macOS)
- Android Platform Tools
- Node.js v22+
- MCP-compatible AI tools (Claude, OpenAI Agents, Copilot Studio)

**Automation Approach:**
- Uses native accessibility trees when available
- Falls back to screenshot-based coordinate tapping
- Operates headless (no visual display required)
- Suitable for CI/CD pipelines

**Sources:**
- [GitHub Repository](https://github.com/mobile-next/mobile-mcp)
- [Smithery Listing](https://smithery.ai/server/@mobile-next/mobile-mcp)

---

## 3. Localization & Translation

### 3.1 SimpleLocalize MCP Server ⭐⭐⭐⭐⭐

**Relevance Score: 5/5** - Perfect for managing 6-language localizations in Arcanapp

**What it does:**
- Create and update translation keys
- Retrieve all keys or specific key details
- Manage tags and languages
- Access translations via natural language
- Supports Claude, Cursor AI, GitHub Copilot, Windsurf

**Official Docs:** [simplelocalize.io/docs/integrations/model-context-protocol](https://simplelocalize.io/docs/integrations/model-context-protocol/)

**Installation:**

Get API key from SimpleLocalize → Settings → Credentials

Add to `.claude/settings.json`:
```json
{
  "mcpServers": {
    "simplelocalize": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@simplelocalize/simplelocalize-mcp", "--api-key=YOUR_API_KEY"]
    }
  }
}
```

**Available Tools (9 functions):**
- Create and update translation keys
- Retrieve all keys or specific key details
- Manage tags and languages
- Access translations

**Usage Examples:**
- "Localize this component and update it to SimpleLocalize"
- "Add all translation keys together with translations to SimpleLocalize"

**Additional:**
- VS Code Extension compatible with Cursor AI

**Sources:**
- [SimpleLocalize Docs](https://simplelocalize.io/docs/integrations/model-context-protocol/)
- [Blog Post](https://simplelocalize.io/blog/posts/introducing-mcp-server/)

---

### 3.2 Lokalise MCP Server ⭐⭐⭐⭐⭐

**Relevance Score: 5/5** - Enterprise-grade localization management

**What it does:**
- **59 MCP tools** across 11 domains
- Bulk key operations (1000+)
- Language addition and progress tracking
- Team orchestration (permissions, workload distribution)
- Workflow automation (file processing, TM+MT integration)
- Real-time monitoring with audit trails
- **17 production-ready prompt templates**

**GitHub:** [AbdallahAHO/lokalise-mcp](https://github.com/AbdallahAHO/lokalise-mcp)

**Installation:**

One-click install:
```bash
npx -y @smithery/cli install @AbdallahAHO/lokalise-mcp --client claude
```

Alternative methods:
- Claude Desktop Extension (.dxt) from Releases
- NPX: `npx lokalise-mcp`
- Global: `npm install -g lokalise-mcp`

**Authentication (priority order):**
1. Environment Variable: `export LOKALISE_API_KEY="your-key"`
2. `.env` file in project root
3. Global MCP config (`~/.mcp/configs.json`)

**Get API Key:**
- Log into [Lokalise](https://app.lokalise.com)
- Profile → API Tokens → Generate new token

**Configuration for Claude Code:**

`.claude/settings.json`:
```json
{
  "mcpServers": {
    "lokalise": {
      "command": "npx",
      "args": ["-y", "lokalise-mcp"],
      "env": {
        "LOKALISE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Key Capabilities by Domain:**

| Domain | Features |
|--------|----------|
| Strategic Management | Portfolio analysis, project health monitoring, team coordination |
| Content Operations | Bulk key operations (1000+), filename filtering, platform tagging |
| Global Expansion | Language addition, progress tracking, completion analytics |
| Team Orchestration | User groups, permissions, workload distribution, reviewer assignment |
| Workflow Automation | File processing, TM+MT integration, multi-stage review pipelines |
| Real-time Monitoring | Process dashboards, audit trails, bulk operation tracking |

**Built-in Automation Templates (17):**
- `project_portfolio_overview` - Strategic analysis across all projects
- `post_upload_review_workflow` - Complete review pipeline for uploaded files
- `bulk_key_creation` - Smart content organization for new features
- `language_expansion` - Add new markets with proper configuration
- `team_translation_setup` - Organize teams with optimal workload distribution

**Test Your Setup:**
```
"Can you list my Lokalise projects?"
```

**Sources:**
- [GitHub Repository](https://github.com/AbdallahAHO/lokalise-mcp)

---

### 3.3 Smartling MCP Server ⭐⭐⭐⭐

**Relevance Score: 4/5** - Enterprise translation platform with AI integration

**What it does:**
- Access Smartling's translation capabilities in AI platforms
- Pull existing translations without leaving IDE
- Check job statuses
- Kick off new translation work
- Leverages translation memories, glossaries, style guides

**Official Site:** [smartling.com/company-news/smartling-launches-mcp-server](https://www.smartling.com/company-news/smartling-launches-mcp-server)

**Sources:**
- [Smartling Blog](https://www.smartling.com/blog/meet-smartlings-mcp-server)

---

### 3.4 Lara Translate MCP Server ⭐⭐⭐

**Relevance Score: 3/5** - First dedicated translation MCP server

**What it does:**
- Language translation for 100+ languages
- Smart tone customization
- Language detection and contextual accuracy

**Blog:** [blog.laratranslate.com/translation-mcp-server](https://blog.laratranslate.com/translation-mcp-server/)

---

### 3.5 Xcode i18n MCP ⭐⭐⭐

**Relevance Score: 3/5** - iOS-specific localization automation

**What it does:**
- Automate Xcode localization workflows
- Streamline iOS/macOS app translation
- Internationalization process automation

**GitHub:** [zhangyu1818/xcode-i18n-mcp](https://github.com/zhangyu1818/xcode-i18n-mcp)

---

## 4. Mobile Automation & Testing

### 4.1 iOS Simulator MCP Server ⭐⭐⭐⭐

**Relevance Score: 4/5** - Essential for iOS simulator management

**What it does:**
- Get information about iOS simulators
- Control UI interactions (taps, swipes)
- Inspect UI elements
- Capture screenshots
- Device lifecycle management
- App installation
- Log retrieval

**GitHub:** [joshuayoes/ios-simulator-mcp](https://github.com/joshuayoes/ios-simulator-mcp)

**Alternative:**
- [InditexTech/mcp-server-simulator-ios-idb](https://github.com/InditexTech/mcp-server-simulator-ios-idb) - LLM natural language commands

**Sources:**
- [GitHub Repository](https://github.com/joshuayoes/ios-simulator-mcp)
- [Awesome MCP Servers](https://mcpservers.org/servers/atom2ueki/mcp-server-ios-simulator)

---

### 4.2 Xcode Build MCP ⭐⭐⭐⭐

**Relevance Score: 4/5** - Build automation for iOS/macOS projects

**What it does:**
- MCP server and CLI for iOS/macOS projects
- Agent-compatible build tools
- Xcode project integration

**GitHub:** [cameroncooke/XcodeBuildMCP](https://github.com/cameroncooke/XcodeBuildMCP)

**Sources:**
- [Skywork.ai Article](https://skywork.ai/skypage/en/xcode-ai-copilot-ios-development/1981539267078320128)

---

### 4.3 Fastlane MCP Server ⭐⭐⭐⭐

**Relevance Score: 4/5** - Automate iOS/Android deployment pipelines

**What it does:**
- Integration with Fastlane for building, testing, deploying
- Firebase and AppCenter support
- Automate beta deployments and releases

**GitHub:** [lyderdev/fastlane-mcp-server](https://github.com/lyderdev/fastlane-mcp-server)

**Configuration:**
Typically requires environment variables:
- `FASTLANE_USER`
- `FASTLANE_PASSWORD`

**Sources:**
- [GitHub Repository](https://github.com/lyderdev/fastlane-mcp-server)
- [Fastlane Docs](https://docs.fastlane.tools/)

---

## 5. Screenshots & Design

### 5.1 iOS Simulator Screenshot MCP ⭐⭐⭐⭐⭐

**Relevance Score: 5/5** - Critical for generating App Store screenshots

**What it does:**
- Capture screenshots from iOS Simulator
- Automatic compression and resizing
- Organized output to subdirectories
- Timestamp-based naming
- Metadata (dimensions, file size, format, timestamp)

**GitHub:** [yorifuji/mcp-ios-simulator-screenshot](https://github.com/yorifuji/mcp-ios-simulator-screenshot)

**Installation:**

For Cline and Roo Code:
```json
{
  "mcpServers": {
    "mcp-ios-simulator-screenshot": {
      "command": "npx",
      "args": ["-y", "mcp-ios-simulator-screenshot"]
    }
  }
}
```

For Cursor and Claude Desktop (requires output directory):
```json
{
  "mcpServers": {
    "mcp-ios-simulator-screenshot": {
      "command": "npx",
      "args": ["-y", "mcp-ios-simulator-screenshot", "--output-dir", "/path/to/screenshots"]
    }
  }
}
```

**Features:**
- `get_screenshot` function with parameters:
  - Output filename (default: timestamp-based)
  - Subdirectory organization (default: `.screenshots`)
  - Image resizing (default: VGA-sized reduction)
  - Maximum width (default: 640px)
  - Device selection (targets booted simulator by default)

**System Requirements:**
- Node.js 16.0.0+
- macOS with iOS Simulator installed
- Xcode Command Line Tools

**Sources:**
- [GitHub Repository](https://github.com/yorifuji/mcp-ios-simulator-screenshot)
- [Glama Profile](https://glama.ai/mcp/servers/@yorifuji/mcp-ios-simulator-screenshot)
- [LobeHub Listing](https://lobehub.com/mcp/yorifuji-mcp-ios-simulator-screenshot)

---

### 5.2 Store Screenshot MCP Server ⭐⭐⭐⭐

**Relevance Score: 4/5** - Professional App Store/Play Store screenshots

**What it does:**
- Generate beautiful App Store & Play Store screenshots
- iPhone mockups with device frames
- Text overlays (headline, subheadline)
- Gradient backgrounds with color presets
- Batch processing

**GitHub:** [k984530/store-screenshot-mcp](https://github.com/k984530/store-screenshot-mcp)

**Installation:**
```bash
npm install
npm run build
```

**Configuration for Claude Code:**

Add to `.claude/settings.json`:
```json
{
  "mcpServers": {
    "store-screenshot": {
      "command": "node",
      "args": ["/path/to/store-screenshot-mcp/dist/index.js"]
    }
  }
}
```

**Supported Devices:**

Free Plan:
- iPhone 15 Pro Max (1290 x 2796)

Pro Plan ($4.90/month):
- iPhone 15 Pro
- iPhone SE
- iPad Pro 12.9"
- iPad Pro 11"
- iPad Air
- iPad Mini

**Customization Options:**
- Text overlays: headline and subheadline
- Backgrounds: 7 color presets (2 free, 5 pro)
- Custom colors: `bgColor1` and `bgColor2` (Pro)
- Input formats: file paths or Base64-encoded images

**Subscription:**
- Free: 3 daily generations with watermark
- Pro: Unlimited at $4.90/month

**Sources:**
- [GitHub Repository](https://github.com/k984530/store-screenshot-mcp)

---

### 5.3 Figma MCP Server ⭐⭐⭐⭐⭐

**Relevance Score: 5/5** - Essential for design-to-code workflows

**What it does:**
- Turn Figma frames into code
- Extract design context (variables, components, layout data)
- Access hierarchy, layout rules, text styles, component properties
- FigJam resource retrieval
- Code Connect integration

**Official Docs:** [help.figma.com/hc/en-us/articles/32132100833559](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)

**Developer Docs:** [developers.figma.com/docs/figma-mcp-server](https://developers.figma.com/docs/figma-mcp-server/)

**Setup:**

1. Open Figma desktop app (latest version)
2. Create or open a Design file
3. Enter Dev Mode (Shift+D)
4. Enable desktop MCP server in inspect panel
5. Configure Claude Code to connect to `http://127.0.0.1:3845/mcp`

Alternative: Remote server at `https://mcp.figma.com/mcp`

**Rate Limits:**
- Starter/View/Collab seats: 6 tool calls/month
- Dev/Full seats on paid plans: per-minute limits (Tier 1 REST API)

**Supported Tools:**
- VS Code, Cursor, Windsurf, Claude Code, Codex

**Use Cases:**
- Generate code from selected frames
- Product teams building new flows
- Design systems and component libraries
- Extract variables and components directly into IDE

**Claude Skills Support:**
Claude Code supports Claude Skills for design system alignment and production-ready code generation.

**Sources:**
- [Figma Help Center](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)
- [Developer Docs](https://developers.figma.com/docs/figma-mcp-server/)
- [Figma Blog](https://www.figma.com/blog/introducing-figma-mcp-server/)
- [Builder.io Guide](https://www.builder.io/blog/figma-mcp-server)

---

## 6. Analytics & Monitoring

### 6.1 Google Analytics MCP Server ⭐⭐⭐⭐

**Relevance Score: 4/5** - Essential for analyzing app performance and user behavior

**What it does:**
- Chat with your Analytics data using LLMs
- Retrieve account summaries
- Get property details
- List Google Ads account links
- Run Google Analytics reports
- Build custom agents with data access
- **Read-only** (cannot edit GA configuration)

**GitHub:** [googleanalytics/google-analytics-mcp](https://github.com/googleanalytics/google-analytics-mcp)

**Official Docs:** [developers.google.com/analytics/devguides/MCP](https://developers.google.com/analytics/devguides/MCP)

**Usage Examples:**
- "How many users did I have yesterday?"
- "What were my top selling products?"
- "Compare mobile vs desktop performance"

**APIs Used:**
- Google Analytics Admin API
- Google Analytics Data API

**Sources:**
- [Google Developers](https://developers.google.com/analytics/devguides/MCP)
- [GitHub Repository](https://github.com/googleanalytics/google-analytics-mcp)
- [Two Octobers Guide](https://twooctobers.com/blog/connecting-to-the-google-analytics-mcp-with-claude/)
- [Pipedream Integration](https://mcp.pipedream.com/app/google_analytics)

---

### 6.2 Microsoft Clarity MCP Server ⭐⭐⭐⭐

**Relevance Score: 4/5** - Free behavioral analytics with privacy focus

**What it does:**
- Query and visualize Clarity data (heatmaps, session recordings)
- Compare mobile vs desktop performance
- Analyze scroll depth by device type
- Transform behavioral analytics queries using AI

**Official Blog:** [clarity.microsoft.com/blog/introducing-the-microsoft-clarity-mcp-server](https://clarity.microsoft.com/blog/introducing-the-microsoft-clarity-mcp-server-a-smarter-way-to-fetch-analytics-with-ai/)

**Key Features:**
- Free website analytics
- Privacy & performance focused
- Works with Claude and Cursor
- Mobile vs desktop analytics

**Sources:**
- [Microsoft Clarity Blog](https://clarity.microsoft.com/blog/introducing-the-microsoft-clarity-mcp-server-a-smarter-way-to-fetch-analytics-with-ai/)
- [MCP.so Profile](https://mcp.so/server/microsoft-clarity/Microsoft)

---

### 6.3 MCP Analytics (Tinybird) ⭐⭐⭐

**Relevance Score: 3/5** - Real-time analytics infrastructure

**What it does:**
- Real-time data analytics
- Custom analytics pipelines

**Template:** [tinybird.co/templates/mcp-server-analytics](https://www.tinybird.co/templates/mcp-server-analytics)

---

## 7. In-App Purchases

### 7.1 RevenueCat MCP Server ⭐⭐⭐⭐⭐

**Relevance Score: 5/5** - Critical for managing IAP subscriptions (Arcanapp uses RevenueCat)

**What it does:**
- Create subscription products across iOS, Android, Amazon, Stripe, Roku
- Manage apps, products, entitlements without dashboard access
- Run multi-step setups via natural language
- Real-time configuration through AI assistant

**Official Docs:** [revenuecat.com/docs/tools/mcp](https://www.revenuecat.com/docs/tools/mcp)

**Installation for Claude Code:**
```bash
claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp --header "Authorization: Bearer YOUR_API_V2_SECRET_KEY"
```

**Authentication Methods:**
1. **API v2 Secret Key** (universal) - Scoped key with Bearer authentication
2. **OAuth** (VSCode/Cursor) - Seamless credential management

**Getting Your API Key:**
1. RevenueCat dashboard → Project Settings
2. API Keys section
3. Generate new API v2 secret key
4. Use write-enabled key for creating/modifying resources, or read-only for viewing

**Configuration Format:**

For manual setup:
```json
{
  "servers": {
    "revenuecat": {
      "url": "https://mcp.revenuecat.ai/mcp",
      "headers": {
        "Authorization": "Bearer {your API v2 token}"
      }
    }
  }
}
```

**Key Capabilities:**
- Create apps and subscription products
- Attach products to entitlements
- Multi-step configuration: "Create an app, add products, and attach them to entitlements" in one command
- First subscription platform to offer AI-native configuration

**VS Code Extension:**
- [RevenueCat MCP Extension](https://marketplace.visualstudio.com/items?itemName=RevenueCat.revenuecat-mcp-extension)

**Sources:**
- [RevenueCat Docs](https://www.revenuecat.com/docs/tools/mcp)
- [Blog Announcement](https://www.revenuecat.com/blog/company/introducing-revenuecat-mcp/)
- [Setup Guide](https://www.revenuecat.com/docs/tools/mcp/setup)
- [GitHub (community)](https://github.com/iamhenry/revenuecat-mcp)
- [Firebender Docs](https://docs.firebender.com/context/mcp/revenuecat)

---

## 8. Additional Resources

### 8.1 MCP Server Directories & Registries

**Awesome MCP Servers Lists:**
- [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) - Curated list with 8,500+ awesome lists
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- [appcypher/awesome-mcp-servers](https://github.com/appcypher/awesome-mcp-servers)

**MCP Registries:**
- [Smithery.ai](https://smithery.ai/) - Largest open marketplace of MCP servers
  - [Mobile Automation Server](https://smithery.ai/server/@mobile-next/mobile-mcp)
  - [Smithery CLI](https://github.com/smithery-ai/cli) - Install, manage, develop MCP servers
  - [Smithery MCP Servers](https://github.com/smithery-ai/mcp-servers)

**Search & Discovery:**
- [Glama.ai](https://glama.ai/mcp/servers) - Searchable MCP server catalog
  - [Flutter servers](https://glama.ai/mcp/servers?query=flutter)
  - [Mobile servers](https://glama.ai/mcp/servers?query=mobile)
- [MCPservers.org](https://mcpservers.org/) - Awesome MCP Servers directory
- [MCPmarket.com](https://mcpmarket.com/) - MCP server marketplace
- [PulseMCP](https://www.pulsemcp.com/) - MCP server catalog
- [MCP Server Finder](https://www.mcpserverfinder.com/)
- [FastMCP](https://fastmcp.me/) - The AppStore for MCP Servers

**Articles & Guides:**
- [K2View: Top 15 MCP Servers for 2026](https://www.k2view.com/blog/awesome-mcp-servers)
- [KDnuggets: 10 Awesome MCP Servers](https://www.kdnuggets.com/10-awesome-mcp-servers)
- [Snyk: 11 Data Science MCP Servers](https://snyk.io/articles/11-data-science-mcp-servers-for-sourcing-analyzing-and-visualizing-data/)

---

### 8.2 Other Notable MCP Servers

**General Development:**
- [Flutter MCP (adamsmaka)](https://github.com/adamsmaka/flutter-mcp) - Real-time Flutter/Dart docs + 50,000+ pub.dev packages
- [Flutter MCP Service (dvillegastech)](https://glama.ai/mcp/servers/@dvillegastech/flutter_mcp_2) - Widget analysis, docs search, performance optimization
- [flutter-mcp-ai-chat](https://github.com/leehack/flutter-mcp-ai-chat) - MCP Client implementation demo for Flutter
- [mcp_client (Dart plugin)](https://github.com/app-appplayer/mcp_client) - Flutter MCP client library

**iOS Development:**
- [iOS Development MCP (dagba)](https://glama.ai/mcp/servers/@dagba/ios-mcp) - Comprehensive iOS dev tools
- [Xcode MCP (airdrop-alpha)](https://glama.ai/mcp/servers/@airdrop-alpha/xcode-mcp) - Xcode project management

**Translation Platforms:**
- [Crowdin MCP](https://crowdin.com/blog/2025/08/19/what-is-a-model-context-protocol) - Enterprise localization platform
- [Language Translation MCP Servers on Glama](https://glama.ai/mcp/servers/categories/language-translation)

---

## Summary: Top 10 MCP Servers for Arcanapp

Based on relevance for a Flutter wellness app going through Apple review with 6-language localization:

1. **App Store Connect MCP** (5/5) - Essential for managing submissions, beta testing, analytics
2. **Official Dart & Flutter MCP** (5/5) - Core development tool for AI-assisted coding
3. **RevenueCat MCP** (5/5) - Critical for managing existing IAP setup (m69, m199)
4. **SimpleLocalize or Lokalise MCP** (5/5) - Manage 6-language translations (EN, ES, FR, DE, IT, PT)
5. **MCP Mobile Server** (5/5) - 36 tools for Flutter/iOS/Android development
6. **iOS Simulator Screenshot MCP** (5/5) - Generate App Store screenshots for all locales
7. **Figma MCP** (5/5) - Design-to-code for wellness UI improvements
8. **DCM MCP** (4/5) - Code quality analysis before submission
9. **Store Screenshot MCP** (4/5) - Professional App Store screenshots with mockups
10. **Google Analytics MCP** (4/5) - Analyze user behavior post-launch

---

## Quick Start Configuration

Here's a recommended `.claude/settings.json` configuration for Arcanapp development:

```json
{
  "mcpServers": {
    "app-store-connect": {
      "command": "npx",
      "args": ["-y", "appstore-connect-mcp-server"],
      "env": {
        "APP_STORE_CONNECT_KEY_ID": "YOUR_KEY_ID",
        "APP_STORE_CONNECT_ISSUER_ID": "YOUR_ISSUER_ID",
        "APP_STORE_CONNECT_P8_PATH": "/path/to/auth-key.p8"
      }
    },
    "dart": {
      "command": "dart",
      "args": ["mcp-server"]
    },
    "dcm": {
      "command": "dcm",
      "args": ["start-mcp-server", "--client=claude-code"]
    },
    "mobile-dev": {
      "command": "npx",
      "args": ["@cristianoaredes/mcp-mobile-server"]
    },
    "simplelocalize": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@simplelocalize/simplelocalize-mcp", "--api-key=YOUR_API_KEY"]
    },
    "ios-screenshot": {
      "command": "npx",
      "args": ["-y", "mcp-ios-simulator-screenshot", "--output-dir", "/Users/alejandrocaceres/Desktop/appstore.zodia/screenshots"]
    },
    "figma": {
      "url": "https://mcp.figma.com/mcp"
    }
  }
}
```

Add RevenueCat via CLI:
```bash
claude mcp add --transport http revenuecat https://mcp.revenuecat.ai/mcp --header "Authorization: Bearer YOUR_API_V2_SECRET_KEY"
```

---

## Next Steps for Arcanapp

Given your current App Store rejection (4.3b Spam, 2.3.2 Metadata, Guideline 5):

1. **Use App Store Connect MCP** to:
   - Update app metadata in all 6 languages
   - Check current version localizations
   - Monitor beta feedback
   - Download analytics to prove differentiation

2. **Use iOS Simulator Screenshot MCP** to:
   - Generate new screenshots emphasizing wellness features (Mood Tracker, Journal, Breathing)
   - Create localized screenshots for all 6 languages
   - Remove any GPT/AI references from visuals

3. **Use SimpleLocalize/Lokalise MCP** to:
   - Verify all wellness-first language is consistent across 6 locales
   - Ensure no hardcoded English strings remain
   - Add any new wellness feature copy

4. **Use Figma MCP** to:
   - Refine wellness hub UI to look distinct from other astrology apps
   - Generate code for improved home screen layout

5. **Use RevenueCat MCP** to:
   - Update IAP metadata to emphasize wellness/self-care value
   - Verify `m69` (Cosmic) and `m199` (Pro) descriptions align with wellness positioning

6. **Use Official Dart & Flutter MCP** to:
   - Run `dart analyze` on critical files
   - Fix any remaining bugs before resubmission

---

**Research compiled on:** February 6, 2026
**Total MCP servers researched:** 40+
**Practical, installable servers:** 25+
**High-relevance (4-5/5) for Arcanapp:** 15

---

## Sources

### Primary MCP Directories
- [GitHub: wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
- [Smithery.ai](https://smithery.ai/)
- [Glama.ai](https://glama.ai/mcp/servers)
- [MCPservers.org](https://mcpservers.org/)

### Official Documentation
- [Flutter MCP Server Docs](https://docs.flutter.dev/ai/mcp-server)
- [RevenueCat MCP Docs](https://www.revenuecat.com/docs/tools/mcp)
- [Figma MCP Guide](https://help.figma.com/hc/en-us/articles/32132100833559)
- [Google Analytics MCP](https://developers.google.com/analytics/devguides/MCP)
- [DCM MCP Docs](https://dcm.dev/docs/ide-integrations/mcp-server)
- [SimpleLocalize MCP Docs](https://simplelocalize.io/docs/integrations/model-context-protocol/)

### Community Resources
- [Flutter Blog: Dart MCP Server](https://blog.flutter.dev/supercharge-your-dart-flutter-development-experience-with-the-dart-mcp-server-2edcc8107b49)
- [freeCodeCamp: MCP with Flutter](https://www.freecodecamp.org/news/how-to-use-the-model-context-protocol-mcp-with-flutter-and-dart/)
- [Two Octobers: Google Analytics MCP with Claude](https://twooctobers.com/blog/connecting-to-the-google-analytics-mcp-with-claude/)
- [Smartling MCP Announcement](https://www.smartling.com/company-news/smartling-launches-mcp-server)