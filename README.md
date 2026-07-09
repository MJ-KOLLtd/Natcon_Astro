# CE-Logic National Conference 2026 (Astro)

Static landing page for the **18th CE-Logic National Conference** (July 30–31, 2026). Refactored from a single WordPress HTML block into an [Astro](https://astro.build) project for deployment on **Vercel**.

## Quick start

```bash
npm install
npm run dev
```

Open the local URL printed in the terminal (usually `http://localhost:4321`).

```bash
npm run build    # output → dist/
npm run preview  # preview production build
```

## Project structure

```
public/assets/          # images (served as /assets/...)
src/
  components/           # page sections (Hero, Speakers, Stream, …)
  layouts/BaseLayout.astro
  pages/index.astro     # home route
  styles/natcon.css     # design system + section styles
```

The original `natcon-landing.html` is kept for reference only; the live page is Astro.

## Event-day stream URL

Edit `src/components/Stream.astro` and set:

```ts
const STREAM_URL = 'https://your-stream-url';
```

When `STREAM_URL` is not `#`, the button becomes an active “Watch live stream” link.

## Deploy to Vercel (via GitHub Desktop)

1. **Install dependencies once** (optional locally; Vercel also installs on deploy):
   ```bash
   npm install
   ```
2. **Create a GitHub repo** and open this folder in **GitHub Desktop**.
3. **Commit** all project files (not `node_modules/` or `dist/` — they are gitignored).
4. **Publish** the branch to GitHub.
5. In [Vercel](https://vercel.com):
   - **Add New Project** → import the GitHub repo
   - Framework: **Astro** (auto-detected)
   - Build command: `npm run build`
   - Output directory: `dist`
   - Deploy

Every push from GitHub Desktop will trigger a new Vercel deployment.

### Custom domain (optional)

Vercel → Project → **Settings → Domains** → add your conference domain.

## Notes

- Static output only (`output: 'static'`) — no server runtime required.
- Styles keep the original `.cel-nc` scope so the TED-like CE-Logic design stays intact.
