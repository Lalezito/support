#!/usr/bin/env node

/**
 * Generate App Icon with Nano Banana Pro
 * Creates multiple variations for selection
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  apiKey: 'AIzaSyA6AzY_xFxVPrf-HRsuQwKIojXOMAtfU6o',
  model: 'gemini-3-pro-image-preview',
  outputDir: path.join(__dirname, '../../zodiac_app/assets/images/app_icon_options'),
};

// Different style variations for app icon
const APP_ICON_VARIANTS = [
  {
    name: 'cosmic_modern',
    prompt: `Create a stunning app icon for a zodiac/horoscope app called "Zodiac".
Design: A mystical cosmic zodiac wheel with all 12 constellation symbols arranged in a circle.
Style: Modern, sleek, premium feel like top App Store apps.
Colors: Deep cosmic purple and blue gradient background, glowing golden/amber zodiac symbols, subtle star particles.
Must have: Rounded corners (iOS style), no text, centered composition, high contrast for small sizes.
The icon should look professional, mystical, and immediately recognizable as an astrology app.
1024x1024 pixels, PNG format.`
  },
  {
    name: 'minimalist_constellation',
    prompt: `Create a minimalist app icon for a zodiac/astrology app.
Design: A single elegant constellation pattern (like a stylized zodiac wheel) made of connected stars.
Style: Clean Apple-style minimalism, modern and sophisticated.
Colors: Deep space purple/indigo background with golden glowing star points connected by thin luminous lines.
Must have: iOS rounded square format, no text, simple but memorable, works at any size.
Premium, luxurious feel. Think Apple's design language meets astrology.
1024x1024 pixels, PNG format.`
  },
  {
    name: 'playful_3d',
    prompt: `Create a charming 3D-style app icon for a zodiac horoscope app.
Design: A cute, friendly 3D zodiac wheel or celestial sphere with soft rounded shapes.
Style: Playful 3D clay/plastic aesthetic like modern game icons, soft shadows, smooth gradients.
Colors: Vibrant purple and blue cosmic tones, warm golden accents, soft glow effects.
Must have: iOS app icon shape, no text, inviting and fun while still mystical.
Like a premium casual game icon but for astrology. Approachable and modern.
1024x1024 pixels, PNG format.`
  },
  {
    name: 'elegant_symbol',
    prompt: `Create an elegant app icon featuring a central mystical symbol for a zodiac app.
Design: A luminous sun/moon/star combination symbol in the center, surrounded by subtle zodiac elements.
Style: Luxurious and elegant, like a high-end jewelry brand icon.
Colors: Rich dark purple/navy background, brilliant gold central symbol with subtle glow, tiny star accents.
Must have: iOS rounded corners, no text, sophisticated and timeless design.
Should feel premium, mysterious, and captivating. Like opening a treasure.
1024x1024 pixels, PNG format.`
  }
];

async function generateImage(prompt, outputPath) {
  return new Promise((resolve, reject) => {
    const requestBody = JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: {
        responseModalities: ['TEXT', 'IMAGE'],
      }
    });

    const options = {
      hostname: 'generativelanguage.googleapis.com',
      path: `/v1beta/models/${CONFIG.model}:generateContent?key=${CONFIG.apiKey}`,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(requestBody),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const response = JSON.parse(data);

          if (response.error) {
            reject(new Error(response.error.message));
            return;
          }

          const parts = response.candidates?.[0]?.content?.parts || [];

          for (const part of parts) {
            if (part.inlineData) {
              const buffer = Buffer.from(part.inlineData.data, 'base64');
              const dir = path.dirname(outputPath);
              if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
              fs.writeFileSync(outputPath, buffer);
              resolve(outputPath);
              return;
            }
          }

          reject(new Error('No image in response'));
        } catch (e) {
          reject(new Error(e.message));
        }
      });
    });

    req.on('error', reject);
    req.write(requestBody);
    req.end();
  });
}

async function main() {
  console.log('🎨 Generando opciones de App Icon con Nano Banana Pro');
  console.log('======================================================\n');

  if (!fs.existsSync(CONFIG.outputDir)) {
    fs.mkdirSync(CONFIG.outputDir, { recursive: true });
  }

  let success = 0;

  for (const variant of APP_ICON_VARIANTS) {
    const outputPath = path.join(CONFIG.outputDir, `${variant.name}.png`);
    process.stdout.write(`   🎯 ${variant.name}...`);

    try {
      await generateImage(variant.prompt, outputPath);
      console.log(' ✅');
      success++;
      // Delay between requests
      await new Promise(r => setTimeout(r, 3000));
    } catch (error) {
      console.log(` ❌ ${error.message}`);
    }
  }

  console.log(`\n✨ ${success}/${APP_ICON_VARIANTS.length} opciones generadas`);
  console.log(`📁 ${CONFIG.outputDir}`);
  console.log('\nRevisa las opciones y elegí la que más te guste!');
}

main().catch(console.error);
