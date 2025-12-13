#!/usr/bin/env node

/**
 * 🍌 Nano Banana PDF Icon Generator
 * Uses Google Gemini 2.5 Flash Image API
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

// Configuration
const CONFIG = {
  apiKey: "AIzaSyA6AzY_xFxVPrf-HRsuQwKIojXOMAtfU6o",
  model: "gemini-3-pro-image-preview",
  outputDir: path.join(__dirname, "../../zodiac_app/assets/images/pdf_icons"), // Base dir
};

// Base style - Estilo "Zodiac 3" (Referencia Original: Pastel, Celeste/Dorado, Soft)
const BASE_STYLE =
  "3D cute icon, soft pastel colors, light cyan and baby blue background gradient, golden decorative corners, orange and gold star sparkles, central zodiac symbol in matte gold, minimalist but cute, rounded corners, high resolution, soft lighting, Apple app icon aesthetic";

// ============================================================================
// ICON DEFINITIONS
// ============================================================================

const ZODIAC_SIGNS = [
  { name: "aries", prompt: "cute aries ram zodiac symbol golden pastel" },
  { name: "taurus", prompt: "cute taurus bull zodiac symbol golden pastel" },
  // { name: 'gemini', prompt: 'cute gemini twins zodiac symbol golden pastel' }, // YA EXISTE (Referencia Original)
  { name: "cancer", prompt: "cute cancer crab zodiac symbol golden pastel" },
  { name: "leo", prompt: "cute leo lion zodiac symbol golden pastel" },
  { name: "virgo", prompt: "cute virgo maiden zodiac symbol golden pastel" },
  { name: "libra", prompt: "cute libra scales zodiac symbol golden pastel" },
  {
    name: "scorpio",
    prompt: "cute scorpio scorpion zodiac symbol golden pastel",
  },
  {
    name: "sagittarius",
    prompt: "cute sagittarius archer zodiac symbol golden pastel",
  },
  {
    name: "capricorn",
    prompt: "cute capricorn goat zodiac symbol golden pastel",
  },
  {
    name: "aquarius",
    prompt: "cute aquarius water bearer zodiac symbol golden pastel",
  },
  { name: "pisces", prompt: "cute pisces fish zodiac symbol golden pastel" },
];

const PLANETS = [
  { name: "venus", prompt: "venus planet female symbol astronomical icon" },
  { name: "mars", prompt: "mars planet male symbol astronomical icon" },
  { name: "jupiter", prompt: "jupiter planet symbol astronomical icon" },
  { name: "saturn", prompt: "saturn planet rings symbol astronomical icon" },
  { name: "mercury", prompt: "mercury planet winged symbol astronomical icon" },
  { name: "moon", prompt: "crescent moon astronomical symbol icon" },
  { name: "sun", prompt: "sun rays circle astronomical symbol icon" },
  { name: "uranus", prompt: "uranus planet symbol astronomical icon" },
  {
    name: "neptune",
    prompt: "neptune trident planet symbol astronomical icon",
  },
  { name: "pluto", prompt: "pluto planet symbol astronomical icon" },
];

const MOON_PHASES = [
  { name: "new_moon", prompt: "new moon dark circle moon phase icon" },
  { name: "waxing_crescent", prompt: "waxing crescent moon phase icon" },
  { name: "first_quarter", prompt: "first quarter half moon phase icon" },
  { name: "waxing_gibbous", prompt: "waxing gibbous moon phase icon" },
  { name: "full_moon", prompt: "full moon complete circle moon phase icon" },
  { name: "waning_gibbous", prompt: "waning gibbous moon phase icon" },
  { name: "last_quarter", prompt: "last quarter half moon phase icon" },
  { name: "waning_crescent", prompt: "waning crescent moon phase icon" },
];

const ACTIVITIES = [
  { name: "stargazing", prompt: "telescope stars stargazing activity icon" },
  { name: "dinner", prompt: "dinner plate fork knife romantic dinner icon" },
  { name: "theater", prompt: "theater comedy tragedy masks icon" },
  { name: "meditation", prompt: "meditation lotus pose zen icon" },
  { name: "sports", prompt: "running person athletic sports icon" },
  { name: "art", prompt: "painter palette brush art creativity icon" },
  { name: "travel", prompt: "airplane travel adventure icon" },
  { name: "cooking", prompt: "chef hat cooking kitchen icon" },
  { name: "music", prompt: "musical notes music icon" },
  { name: "reading", prompt: "open book reading icon" },
  { name: "nature", prompt: "tree leaf nature outdoors icon" },
  { name: "spa", prompt: "lotus flower spa relaxation wellness icon" },
];

const DECORATIVE = [
  { name: "star_gold", prompt: "five pointed star simple icon" },
  { name: "heart_pink", prompt: "heart love romantic simple icon" },
  { name: "checkmark", prompt: "checkmark tick success simple icon" },
  { name: "sparkles", prompt: "three sparkle stars magic simple icon" },
  { name: "infinity", prompt: "infinity symbol eternal simple icon" },
  { name: "arrow_up", prompt: "arrow pointing up simple icon" },
  { name: "arrow_down", prompt: "arrow pointing down simple icon" },
  { name: "circle_dot", prompt: "circle with dot center simple icon" },
  { name: "diamond", prompt: "diamond shape simple icon" },
  { name: "cross", prompt: "plus cross simple icon" },
];

// ============================================================================
// GEMINI API
// ============================================================================

async function generateImage(prompt, outputPath) {
  return new Promise((resolve, reject) => {
    const fullPrompt = `Generate an icon: ${prompt}. Style: ${BASE_STYLE}`;

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

async function generateBatch(items, category, subdir, size) {
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
      // Small delay between requests
      if (i < items.length - 1) await new Promise((r) => setTimeout(r, 2000));
    } catch (error) {
      console.log(` ❌ ${error.message}`);
      failed++;
    }
  }

  console.log(`\n   ✨ ${success}/${items.length} completados`);
  return { success, failed };
}

// Generation functions
const generateZodiac = () =>
  generateBatch(ZODIAC_SIGNS, "Zodiac Signs (128x128)", "zodiac 3", 128);
const generatePlanets = () =>
  generateBatch(PLANETS, "Planets (64x64)", "planets", 64);
const generateMoonPhases = () =>
  generateBatch(MOON_PHASES, "Moon Phases (48x48)", "moon_phases", 48);
const generateActivities = () =>
  generateBatch(ACTIVITIES, "Activities (32x32)", "activities", 32);
const generateDecorative = () =>
  generateBatch(DECORATIVE, "Decorative (24x24)", "decorative", 24);

async function generateAll() {
  console.log("\n🍌 NANO BANANA - GENERANDO TODOS LOS ICONOS");
  console.log("=============================================");
  console.log("📊 54 iconos | ⏱️  ~3-5 minutos\n");

  const results = {
    zodiac: await generateZodiac(),
    planets: await generatePlanets(),
    moon: await generateMoonPhases(),
    activities: await generateActivities(),
    decorative: await generateDecorative(),
  };

  console.log("\n📊 RESUMEN FINAL");
  console.log("================");
  let total = 0,
    ok = 0;
  for (const [cat, r] of Object.entries(results)) {
    console.log(`   ${cat}: ${r.success}/${r.success + r.failed}`);
    total += r.success + r.failed;
    ok += r.success;
  }
  console.log(`\n   TOTAL: ${ok}/${total} iconos`);
  console.log(`   📁 ${CONFIG.outputDir}`);
}

// ============================================================================
// CLI
// ============================================================================

function printHelp() {
  console.log(`
🍌 Nano Banana PDF Icon Generator
==================================
Google Gemini 2.5 Flash Image API

USO:
  node nano-banana-generator.js --type <tipo>

TIPOS:
  all          Todo (~54 iconos, ~3-5 min)
  zodiac       12 signos zodiacales
  planets      10 planetas
  moon         8 fases lunares
  activities   12 actividades
  decorative   10 decorativos

EJEMPLOS:
  node nano-banana-generator.js --type all
  node nano-banana-generator.js --type zodiac
`);
}

async function main() {
  const args = process.argv.slice(2);
  const typeIndex = args.indexOf("--type");
  const type = typeIndex !== -1 ? args[typeIndex + 1] : null;

  if (!type || args.includes("--help")) {
    printHelp();
    return;
  }

  console.log("🍌 Nano Banana Icon Generator");
  console.log("=============================");
  console.log("Usando: Google Gemini 2.5 Flash Image\n");

  switch (type) {
    case "all":
      await generateAll();
      break;
    case "zodiac":
      await generateZodiac();
      break;
    case "planets":
      await generatePlanets();
      break;
    case "moon":
      await generateMoonPhases();
      break;
    case "activities":
      await generateActivities();
      break;
    case "decorative":
      await generateDecorative();
      break;
    default:
      console.log(`❌ Tipo inválido: ${type}`);
      printHelp();
  }
}

main().catch(console.error);
