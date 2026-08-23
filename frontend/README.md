# Smart Inventory Replenishment — Frontend

Next.js 16 (App Router) + TypeScript + Tailwind dashboard for the Smart
Inventory Replenishment System. Part of Sprint 4 — see the main repo
README for overall project context.

## Setup

```bash
npm install
cp .env.local.example .env.local
# edit .env.local if your API isn't on http://localhost:8000
npm run dev
```

Open http://localhost:3000. The **Overview** page calls the backend's
`GET /health` directly — if the API isn't running yet, it'll show
"API Unreachable" instead of failing silently, so that's the fastest way
to confirm the two apps are actually talking to each other.

## Scripts

| Command | Purpose |
|---|---|
| `npm run dev` | Local dev server with Turbopack |
| `npm run build` | Production build |
| `npm run start` | Serve the production build |
| `npm run lint` | ESLint (flat config, `eslint-config-next`) |
| `npm run typecheck` | `tsc --noEmit` |

## Current status (Sprint 4)

| Route | Status | Needs |
|---|---|---|
| `/` (Overview) | **Live** | `GET /health` (already implemented) |
| `/inventory` | Scaffolded, stub | `GET /dashboard` (not yet implemented) |
| `/forecasts` | Scaffolded, stub | `GET /products/{id}/forecasts` (not yet implemented) |
| `/alerts` | Scaffolded, stub | `GET /dashboard` (not yet implemented) |
| `/assistant` | Scaffolded, stub | `POST /chat` (not yet implemented) |

`lib/api-client.ts` already has typed functions for the two endpoints
above that don't exist yet (`getDashboardData`, `getForecastHistory`) —
they're written against the agreed contract in `types/api.ts` and will
work as soon as the backend enablement issue lands. No frontend changes
should be needed at that point beyond wiring these into the stub pages.

## Note on `npm run build` in restricted network environments

`app/layout.tsx` loads fonts via `next/font/google`, which fetches from
`fonts.googleapis.com` at build time. If you're building inside a
sandboxed CI environment with a restricted egress allowlist, add that
domain (and `fonts.gstatic.com`) to it — this is unrelated to any
project code and will build normally on a normal machine or in the
Docker image once that domain is reachable.
