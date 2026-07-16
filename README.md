# CE-Logic National Conference 2026 (Astro)

Static landing page for the **18th CE-Logic National Conference** (July 30–31, 2026).

## Quick start (developers)

```bash
npm install
npm run dev
```

Open the local URL printed in the terminal (usually `http://localhost:4321`).

```bash
npm run build    # output → dist/
npm run preview  # preview production build locally
```

## Deploy for IT (any static web server)

This site is **fully static**. No database, API, or Node.js runtime is required in production.

### Build once

Requirements: **Node.js 18+** and npm (build machine only).

```bash
npm ci
npm run build
```

The deployable site is everything inside **`dist/`**.

### Serve `dist/`

Copy the `dist/` folder to your web server and point the site root at it.

| Platform | Notes |
|----------|--------|
| **Nginx / Apache** | Set document root to `dist/`. Enable `gzip` / `brotli` for `.css`, `.js`, `.webp`, `.woff2`. |
| **IIS** | Create a site with physical path = `dist/`. Add a default document for `index.html`. |
| **Object storage + CDN** | Upload `dist/` contents (S3, Azure Blob, etc.) and enable static website hosting. |
| **Vercel** | Import the Git repo; build command `npm run build`, output `dist`. Or run `npm run deploy:vercel`. |

### Before go-live

1. **Stream URL** — edit `src/components/Stream.astro` and set `STREAM_URL` to the live Facebook or video URL, then rebuild.
2. **Custom domain** — configure on your host after upload.
3. **Rebuild** after any content change; do not edit files inside `dist/` by hand.

### What not to deploy

These are development-only and are excluded from production builds:

- `node_modules/`
- `scripts/` (asset processing helpers)
- `terminals/`, `mcps/`, `agent-tools/`

## Project structure

```
public/assets/          # images, PDFs, videos (served as /assets/...)
src/
  components/           # page sections
  data/                 # conference resources manifest
  layouts/BaseLayout.astro
  pages/index.astro     # home route
  styles/               # design system CSS
```

## Assets

- Hero and section images: WebP with responsive `srcset` where applicable.
- Partner brochures and sponsor videos: Google Drive folders (linked from the Resources section).
- Favicon: `public/assets/ce-mark.webp`.

## Optional: Vercel (GitHub)

1. Commit and push to GitHub (exclude `node_modules/` and `dist/`).
2. Vercel → **Add New Project** → import repo.
3. Framework: **Astro**; build `npm run build`; output `dist`.
4. Every push redeploys automatically.