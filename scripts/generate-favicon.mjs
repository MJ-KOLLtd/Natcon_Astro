import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, '..');
const source = path.join(root, 'public', 'assets', 'ceals-emblem-source.png');
const publicDir = path.join(root, 'public');

if (!fs.existsSync(source)) {
  console.error('Source emblem not found:', source);
  process.exit(1);
}

fs.mkdirSync(publicDir, { recursive: true });

const square = await sharp(source)
  .resize(512, 512, { fit: 'contain', background: { r: 0, g: 0, b: 0, alpha: 1 } })
  .png()
  .toBuffer();

const sizes = [
  { name: 'favicon-16x16.png', size: 16 },
  { name: 'favicon-32x32.png', size: 32 },
  { name: 'favicon-48x48.png', size: 48 },
  { name: 'apple-touch-icon.png', size: 180 },
  { name: 'icon-192.png', size: 192 },
  { name: 'icon-512.png', size: 512 },
];

for (const { name, size } of sizes) {
  await sharp(square).resize(size, size).png().toFile(path.join(publicDir, name));
  console.log(`Wrote ${name}`);
}

await sharp(square).resize(48, 48).toFile(path.join(publicDir, 'favicon.ico'));
console.log('Wrote favicon.ico');