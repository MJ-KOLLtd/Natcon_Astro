import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const node = process.execPath;
const vercel = path.join(root, 'node_modules/vercel/dist/vc.js');
const astro = path.join(root, 'node_modules/astro/astro.js');
const distDir = path.join(root, 'dist');
const outputDir = path.join(root, '.vercel', 'output');
const staticDir = path.join(outputDir, 'static');

function run(label, script, args = []) {
  console.log(`\n> ${label}`);
  const result = spawnSync(node, [script, ...args], {
    cwd: root,
    stdio: 'inherit',
    env: process.env,
  });

  if (result.error) {
    console.error(result.error.message);
    process.exit(1);
  }

  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

function preparePrebuiltOutput() {
  if (!fs.existsSync(distDir)) {
    console.error('Build output missing: dist/');
    process.exit(1);
  }

  fs.rmSync(outputDir, { recursive: true, force: true });
  fs.mkdirSync(staticDir, { recursive: true });

  for (const entry of fs.readdirSync(distDir)) {
    fs.cpSync(path.join(distDir, entry), path.join(staticDir, entry), { recursive: true });
  }

  fs.writeFileSync(
    path.join(outputDir, 'config.json'),
    JSON.stringify({
      version: 3,
      routes: [{ handle: 'filesystem' }],
    }),
  );

  console.log('\n> Prepared .vercel/output from dist/');
}

run('Building site', astro, ['build']);
preparePrebuiltOutput();
run('Deploying to Vercel (prebuilt)', vercel, ['deploy', '--prebuilt', '--prod', '--yes']);

console.log('\nDeploy finished.');