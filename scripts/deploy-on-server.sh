#!/usr/bin/env bash
# Run this ON the Ubuntu server (as the deploy user), not on Windows.
set -euxo pipefail

cd /var/www/astro/Natcon_Astro

git fetch origin main
git reset --hard origin/main
git log -1 --oneline

npm ci
export SITE_URL=https://celogic-natcon.ceals.ph
npm run build

test -f dist/favicon.ico
test -f dist/favicon-32x32.png
grep -q 'favicon.ico' dist/index.html

rsync -av --delete dist/ /var/www/html/
sudo systemctl reload nginx

test -f /var/www/html/favicon.ico
echo "Deploy OK: favicon live"