// @ts-check
import { defineConfig } from 'astro/config';

// Static site — deploys cleanly to Vercel via GitHub Desktop / Git push.
// Vercel auto-detects Astro; no adapter required for static output.
export default defineConfig({
  output: 'static',
  // Optional: set your production domain once known
  // site: 'https://natcon.example.com',
  compressHTML: true,
  build: {
    inlineStylesheets: 'auto',
  },
});
