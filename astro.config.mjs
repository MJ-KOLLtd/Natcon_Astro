// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// Set SITE_URL in Vercel/host env to your production domain for canonical URLs + sitemap.
const site = process.env.SITE_URL || 'https://celogic-natcon.ceals.ph';

// Static site — deploys cleanly to Vercel via GitHub Desktop / Git push.
// Vercel auto-detects Astro; no adapter required for static output.
export default defineConfig({
  site,
  output: 'static',
  compressHTML: true,
  build: {
    inlineStylesheets: 'auto',
  },
  integrations: [
    sitemap({
      filter: (page) => !page.includes('robots.txt'),
    }),
  ],
});
