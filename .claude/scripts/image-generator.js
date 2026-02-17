#!/usr/bin/env node

/**
 * 🎨 Universal AI Image Generator
 * Uses Google Gemini Image API
 *
 * Works in any project - just configure OUTPUT_DIR
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

// ============================================================================
// CONFIGURATION - Modify these for your project
// ============================================================================

const CONFIG = {
  // API Key - Set via environment variable or replace here
  apiKey: process.env.GEMINI_API_KEY || "AIzaSyA6AzY_xFxVPrf-HRsuQwKIojXOMAtfU6o",

  // Model
  model: "gemini-2.0-flash-exp-image-generation",

  // Output directory - relative to where you run the script
  // Change this for your project!
  outputDir: process.env.IMAGE_OUTPUT_DIR || "./generated_images",

  // Delay between API calls (ms) to avoid rate limiting
  delayBetweenCalls: 2000,
};

// ============================================================================
// STYLE PRESETS - Choose or customize
// ============================================================================

const STYLES = {
  // Cute pastel style (like Zodiac app)
  cute_pastel: "3D cute icon, soft pastel colors, light cyan and baby blue background gradient, golden decorative corners, orange and gold star sparkles, minimalist but cute, rounded corners, high resolution, soft lighting, Apple app icon aesthetic",

  // Flat minimalist
  flat_minimal: "flat design icon, minimalist, single color, clean lines, no shadows, no gradients, centered composition, modern app icon style",

  // Gradient modern
  gradient_modern: "modern gradient icon, vibrant colors, soft shadows, rounded corners, 3D effect, glossy finish, app icon style",

  // Line art
  line_art: "line art icon, single stroke, minimal detail, clean lines, monochrome, simple elegant design",

  // Glassmorphism
  glassmorphism: "glassmorphism icon, frosted glass effect, subtle transparency, soft blur, modern UI design, light colors",

  // Neon
  neon: "neon glow icon, dark background, vibrant neon colors, glowing edges, cyberpunk style, futuristic",
};

// Default style
let currentStyle = STYLES.cute_pastel;

// ============================================================================
// PRESET ICON CATEGORIES
// ============================================================================

const PRESETS = {
  // App navigation icons
  navigation: [
    { name: "home", prompt: "home house icon" },
    { name: "search", prompt: "magnifying glass search icon" },
    { name: "settings", prompt: "gear cog settings icon" },
    { name: "profile", prompt: "person user profile icon" },
    { name: "menu", prompt: "hamburger menu three lines icon" },
    { name: "back", prompt: "arrow left back navigation icon" },
    { name: "forward", prompt: "arrow right forward navigation icon" },
    { name: "close", prompt: "x close dismiss icon" },
    { name: "add", prompt: "plus add create icon" },
    { name: "edit", prompt: "pencil edit modify icon" },
  ],

  // Status icons
  status: [
    { name: "success", prompt: "checkmark success complete icon" },
    { name: "error", prompt: "x error failed icon" },
    { name: "warning", prompt: "exclamation triangle warning icon" },
    { name: "info", prompt: "i information info icon" },
    { name: "loading", prompt: "circular spinner loading icon" },
    { name: "sync", prompt: "circular arrows sync refresh icon" },
  ],

  // Social/actions
  social: [
    { name: "share", prompt: "share arrow up box icon" },
    { name: "like", prompt: "heart like love icon" },
    { name: "comment", prompt: "speech bubble comment icon" },
    { name: "bookmark", prompt: "bookmark save icon" },
    { name: "download", prompt: "arrow down download icon" },
    { name: "upload", prompt: "arrow up upload icon" },
  ],

  // Media controls
  media: [
    { name: "play", prompt: "triangle play button icon" },
    { name: "pause", prompt: "two bars pause button icon" },
    { name: "stop", prompt: "square stop button icon" },
    { name: "volume", prompt: "speaker sound volume icon" },
    { name: "mute", prompt: "speaker muted no sound icon" },
    { name: "fullscreen", prompt: "expand fullscreen icon" },
  ],

  // E-commerce
  ecommerce: [
    { name: "cart", prompt: "shopping cart icon" },
    { name: "bag", prompt: "shopping bag icon" },
    { name: "wallet", prompt: "wallet payment icon" },
    { name: "credit_card", prompt: "credit card payment icon" },
    { name: "tag", prompt: "price tag discount icon" },
    { name: "gift", prompt: "gift box present icon" },
  ],

  // Communication
  communication: [
    { name: "mail", prompt: "envelope email mail icon" },
    { name: "chat", prompt: "chat bubble message icon" },
    { name: "phone", prompt: "phone call icon" },
    { name: "video", prompt: "video camera call icon" },
    { name: "notification", prompt: "bell notification alert icon" },
    { name: "send", prompt: "paper airplane send icon" },
  ],

  // Zodiac signs (original nano-banana)
  zodiac: [
    { name: "aries", prompt: "aries ram zodiac symbol" },
    { name: "taurus", prompt: "taurus bull zodiac symbol" },
    { name: "gemini", prompt: "gemini twins zodiac symbol" },
    { name: "cancer", prompt: "cancer crab zodiac symbol" },
    { name: "leo", prompt: "leo lion zodiac symbol" },
    { name: "virgo", prompt: "virgo maiden zodiac symbol" },
    { name: "libra", prompt: "libra scales zodiac symbol" },
    { name: "scorpio", prompt: "scorpio scorpion zodiac symbol" },
    { name: "sagittarius", prompt: "sagittarius archer zodiac symbol" },
    { name: "capricorn", prompt: "capricorn goat zodiac symbol" },
    { name: "aquarius", prompt: "aquarius water bearer zodiac symbol" },
    { name: "pisces", prompt: "pisces fish zodiac symbol" },
  ],

  // Planets
  planets: [
    { name: "sun", prompt: "sun star astronomical symbol" },
    { name: "moon", prompt: "crescent moon astronomical symbol" },
    { name: "mercury", prompt: "mercury planet symbol" },
    { name: "venus", prompt: "venus planet female symbol" },
    { name: "mars", prompt: "mars planet male symbol" },
    { name: "jupiter", prompt: "jupiter planet symbol" },
    { name: "saturn", prompt: "saturn planet rings symbol" },
    { name: "uranus", prompt: "uranus planet symbol" },
    { name: "neptune", prompt: "neptune trident symbol" },
    { name: "pluto", prompt: "pluto planet symbol" },
  ],

  // Weather
  weather: [
    { name: "sunny", prompt: "sun sunny clear weather icon" },
    { name: "cloudy", prompt: "cloud cloudy weather icon" },
    { name: "rainy", prompt: "rain cloud rainy weather icon" },
    { name: "stormy", prompt: "lightning thunder storm weather icon" },
    { name: "snowy", prompt: "snowflake snow winter weather icon" },
    { name: "windy", prompt: "wind blowing weather icon" },
  ],
};

// ============================================================================
// GEMINI API
// ============================================================================

async function generateImage(prompt, outputPath) {
  return new Promise((resolve, reject) => {
    const fullPrompt = `Generate an icon: ${prompt}. Style: ${currentStyle}`;

    const requestBody = JSON.stringify({
      contents: [{ parts: [{ text: fullPrompt }] }],
      generationConfig: {
        responseModalities: ["TEXT", "IMAGE"],
      },
    });

    const options = {
      hostname: "generativelanguage.googleapis.com",
      path: `/v1beta/models/${CONFIG.model}:generateContent?key=${CONFIG.apiKey}`,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(requestBody),
      },
    };

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => {
        data += chunk;
      });
      res.on("end", () => {
        try {
          const response = JSON.parse(data);

          if (response.error) {
            reject(new Error(response.error.message));
            return;
          }

          const parts = response.candidates?.[0]?.content?.parts || [];

          for (const part of parts) {
            if (part.inlineData) {
              const buffer = Buffer.from(part.inlineData.data, "base64");
              const dir = path.dirname(outputPath);
              if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
              fs.writeFileSync(outputPath, buffer);
              resolve(outputPath);
              return;
            }
          }

          reject(new Error("No image in response"));
        } catch (e) {
          reject(new Error(e.message));
        }
      });
    });

    req.on("error", reject);
    req.write(requestBody);
    req.end();
  });
}

// ============================================================================
// BATCH GENERATION
// ============================================================================

async function generateBatch(items, category, subdir) {
  const outputDir = path.join(CONFIG.outputDir, subdir);

  console.log(`\n🎨 ${category} (${items.length} icons)`);
  console.log(`   → ${outputDir}\n`);

  let success = 0,
    failed = 0;

  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    const outputPath = path.join(outputDir, `${item.name}.png`);

    process.stdout.write(`   [${i + 1}/${items.length}] ${item.name}...`);

    try {
      await generateImage(item.prompt, outputPath);
      console.log(" ✅");
      success++;
      // Delay between requests
      if (i < items.length - 1) {
        await new Promise((r) => setTimeout(r, CONFIG.delayBetweenCalls));
      }
    } catch (error) {
      console.log(` ❌ ${error.message}`);
      failed++;
    }
  }

  console.log(`\n   ✨ ${success}/${items.length} completed`);
  return { success, failed };
}

async function generatePreset(presetName) {
  const preset = PRESETS[presetName];
  if (!preset) {
    console.log(`❌ Unknown preset: ${presetName}`);
    console.log(`   Available: ${Object.keys(PRESETS).join(", ")}`);
    return;
  }
  await generateBatch(preset, presetName, presetName);
}

async function generateAll() {
  console.log("\n🎨 GENERATING ALL PRESETS");
  console.log("=========================\n");

  const results = {};
  for (const [name, items] of Object.entries(PRESETS)) {
    results[name] = await generateBatch(items, name, name);
  }

  console.log("\n📊 SUMMARY");
  console.log("==========");
  let total = 0,
    ok = 0;
  for (const [cat, r] of Object.entries(results)) {
    console.log(`   ${cat}: ${r.success}/${r.success + r.failed}`);
    total += r.success + r.failed;
    ok += r.success;
  }
  console.log(`\n   TOTAL: ${ok}/${total} icons`);
  console.log(`   📁 ${CONFIG.outputDir}`);
}

async function generateCustom(prompt, filename) {
  const outputPath = path.join(CONFIG.outputDir, "custom", filename);
  console.log(`\n🎨 Generating custom image...`);
  console.log(`   Prompt: ${prompt}`);
  console.log(`   Output: ${outputPath}\n`);

  try {
    await generateImage(prompt, outputPath);
    console.log(`✅ Success! Saved to ${outputPath}`);
  } catch (error) {
    console.log(`❌ Failed: ${error.message}`);
  }
}

// ============================================================================
// CLI
// ============================================================================

function printHelp() {
  console.log(`
🎨 Universal AI Image Generator
================================
Powered by Google Gemini Image API

USAGE:
  node image-generator.js [command] [options]

COMMANDS:
  --preset <name>     Generate a preset category
  --all               Generate ALL presets
  --custom "<prompt>" <filename.png>  Generate custom image
  --style <name>      Set style before generating
  --list-presets      Show available presets
  --list-styles       Show available styles
  --help              Show this help

PRESETS:
  ${Object.keys(PRESETS).join(", ")}

STYLES:
  ${Object.keys(STYLES).join(", ")}

ENVIRONMENT:
  GEMINI_API_KEY      Your Gemini API key
  IMAGE_OUTPUT_DIR    Output directory (default: ./generated_images)

EXAMPLES:
  # Generate navigation icons with default style
  node image-generator.js --preset navigation

  # Generate zodiac icons with neon style
  node image-generator.js --style neon --preset zodiac

  # Generate all presets
  node image-generator.js --all

  # Generate custom image
  node image-generator.js --custom "a cute robot mascot" robot.png

  # Set output directory
  IMAGE_OUTPUT_DIR=./assets/icons node image-generator.js --preset navigation
`);
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes("--help")) {
    printHelp();
    return;
  }

  if (args.includes("--list-presets")) {
    console.log("\n📦 Available Presets:");
    for (const [name, items] of Object.entries(PRESETS)) {
      console.log(`   ${name} (${items.length} icons)`);
    }
    return;
  }

  if (args.includes("--list-styles")) {
    console.log("\n🎨 Available Styles:");
    for (const name of Object.keys(STYLES)) {
      console.log(`   ${name}`);
    }
    return;
  }

  // Set style if specified
  const styleIndex = args.indexOf("--style");
  if (styleIndex !== -1 && args[styleIndex + 1]) {
    const styleName = args[styleIndex + 1];
    if (STYLES[styleName]) {
      currentStyle = STYLES[styleName];
      console.log(`🎨 Using style: ${styleName}`);
    } else {
      console.log(`⚠️  Unknown style: ${styleName}, using default`);
    }
  }

  console.log("🎨 AI Image Generator");
  console.log("=====================");
  console.log(`📁 Output: ${CONFIG.outputDir}\n`);

  // Handle commands
  if (args.includes("--all")) {
    await generateAll();
  } else if (args.includes("--preset")) {
    const presetIndex = args.indexOf("--preset");
    const presetName = args[presetIndex + 1];
    if (presetName) {
      await generatePreset(presetName);
    } else {
      console.log("❌ Please specify a preset name");
    }
  } else if (args.includes("--custom")) {
    const customIndex = args.indexOf("--custom");
    const prompt = args[customIndex + 1];
    const filename = args[customIndex + 2] || "custom.png";
    if (prompt) {
      await generateCustom(prompt, filename);
    } else {
      console.log("❌ Please provide a prompt");
    }
  } else {
    printHelp();
  }
}

main().catch(console.error);
