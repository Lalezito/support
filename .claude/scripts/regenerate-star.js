#!/usr/bin/env node

const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  apiKey: 'AIzaSyA6AzY_xFxVPrf-HRsuQwKIojXOMAtfU6o',
  model: 'gemini-2.0-flash-exp-image-generation',
  outputDir: path.join(__dirname, '../../zodiac_app/assets/images/pdf_icons'),
};

const BASE_STYLE = 'golden amber (#FFD700) line art icon, transparent background, minimalist vector style, clean lines, no text, professional astrology aesthetic, PNG with alpha transparency';

async function generateImage(prompt, outputPath) {
  return new Promise((resolve, reject) => {
    const fullPrompt = `Generate an icon: ${prompt}. Style: ${BASE_STYLE}`;

    const requestBody = JSON.stringify({
      contents: [{ parts: [{ text: fullPrompt }] }],
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

(async () => {
  const outputPath = path.join(CONFIG.outputDir, 'decorative', 'star_gold.png');
  process.stdout.write('🌟 Generando star_gold...');
  try {
    await generateImage('five pointed star simple icon', outputPath);
    console.log(' ✅');
  } catch (error) {
    console.log(` ❌ ${error.message}`);
  }
})();
