/**
 * Build-time asset optimizer — recompresses images for fast mobile/tablet/desktop loads.
 * Run: node scripts/optimize-assets.mjs
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ASSETS = path.join(__dirname, '..', 'public', 'assets');
const SPEAKERS = path.join(ASSETS, 'speakers');

const webp = (q = 82) => ({ quality: q, effort: 6, smartSubsample: true });

async function loadSource(input) {
  return typeof input === 'string' ? fs.readFileSync(input) : input;
}

async function writeWebp(input, output, { width, quality = 82, blur } = {}) {
  const source = await loadSource(input);
  let pipe = sharp(source);
  if (width) pipe = pipe.resize(width, null, { withoutEnlargement: true, fit: 'inside' });
  if (blur) pipe = pipe.blur(blur);
  const buffer = await pipe.webp(webp(quality)).toBuffer();
  const meta = await sharp(buffer).metadata();
  const kb = Math.round(buffer.length / 1024);
  console.log(`  ${path.basename(output)}: ${meta.width}x${meta.height} ${kb} KB`);

  const tmp = path.join(os.tmpdir(), `natcon-${path.basename(output)}`);
  fs.writeFileSync(tmp, buffer);
  fs.copyFileSync(tmp, output);
  fs.unlinkSync(tmp);

  return { width: meta.width, height: meta.height, size: buffer.length };
}

async function optimizeHeroes() {
  console.log('\nHero images');
  const heroes = [
    ['hero.webp', { quality: 72 }],
    ['hero@2x.webp', { width: 2560, quality: 70 }],
    ['hero-mobile.webp', { quality: 72 }],
    ['hero-mobile@2x.webp', { width: 1620, quality: 70 }],
  ];
  for (const [name, opts] of heroes) {
    const file = path.join(ASSETS, name);
    const source = await loadSource(file);
    await writeWebp(source, file, opts);
  }
}

async function optimizeHeroBg() {
  console.log('\nStream background');
  const src = path.join(ASSETS, 'hero-bg.webp');
  const source = await loadSource(src);
  await writeWebp(source, src, { width: 960, quality: 72, blur: 0.6 });
}

async function optimizeExperienceVisuals() {
  console.log('\nExperience visuals');
  const files = [
    'visual-keynote-stage.webp',
    'visual-strategy.webp',
    'visual-panel-room.webp',
    'visual-technology-showcase.webp',
  ];
  for (const name of files) {
    const base = name.replace('.webp', '');
    const src = path.join(ASSETS, name);
    const source = await loadSource(src);
    await writeWebp(source, path.join(ASSETS, `${base}-640.webp`), { width: 640, quality: 82 });
    await writeWebp(source, src, { width: 1280, quality: 84 });
  }
}

async function optimizeSectionVisuals() {
  console.log('\nTheme & highlights visuals');
  const pairs = [
    ['visual-theme-2026.webp', 800],
    ['visual-theme-2026@2x.webp', 1362],
    ['visual-streamed-library.webp', 800],
    ['visual-streamed-library@2x.webp', 1362],
  ];
  for (const [name, width] of pairs) {
    const file = path.join(ASSETS, name);
    const source = await loadSource(file);
    await writeWebp(source, file, { width, quality: 82 });
  }
}

async function optimizeSpeakers() {
  console.log('\nSpeaker photos');
  const entries = fs.readdirSync(SPEAKERS).filter((f) => /\.(jpe?g|png)$/i.test(f));
  for (const file of entries) {
    const stem = path.parse(file).name;
    const src = path.join(SPEAKERS, file);
    await writeWebp(src, path.join(SPEAKERS, `${stem}.webp`), { width: 480, quality: 82 });
    await writeWebp(src, path.join(SPEAKERS, `${stem}@2x.webp`), { width: 600, quality: 84 });
  }
}

async function optimizeLogos() {
  console.log('\nPartner & brand logos');
  const logos = [
    ['partner-plai.webp', 280, 78],
    ['partner-up-library.webp', 280, 78],
    ['partner-paarl.webp', 200, 80],
    ['ce-logic-logo-on-dark.webp', 296, 85],
    ['ce-logic-logo.webp', 440, 85],
    ['ceals-logo.webp', 400, 85],
  ];
  for (const [name, width, quality] of logos) {
    const file = path.join(ASSETS, name);
    if (!fs.existsSync(file)) continue;
    const source = await loadSource(file);
    await writeWebp(source, file, { width, quality });
  }
}

async function main() {
  console.log('Optimizing assets in', ASSETS);
  await optimizeHeroes();
  await optimizeHeroBg();
  await optimizeExperienceVisuals();
  await optimizeSectionVisuals();
  await optimizeSpeakers();
  await optimizeLogos();
  console.log('\nDone.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});