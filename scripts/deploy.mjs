import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const node = process.execPath;
const vercel = path.join(root, 'node_modules/vercel/dist/vc.js');
const astro = path.join(root, 'node_modules/astro/astro.js');

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

run('Building site', astro, ['build']);
run('Deploying to Vercel', vercel, ['deploy', '--prod', '--yes']);

console.log('\nDeploy finished.');