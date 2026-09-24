# PROGRESS: ML Empowerment Build Challenge 3.0

Running log for the unattended cloud build. **A resumed session should read this first and continue from the first unchecked phase.**

**Deadline:** Mon Oct 5, 2026 · 8:00 PM EDT (`2026-10-06T00:00:00Z`)
**Internal "all deliverables done" target:** Sun Oct 4, 2026 · 8:00 PM EDT (24 h buffer, per CLAUDE.md lesson 2)

## Countdown log

| When (ET) | Hours to deadline | Phase |
|---|---|---|
| Wed Sep 23 2026 · 10:39 PM EDT | 285.3 h | 0: kickoff |

## Phase plan (hackathon-win Phase 4 budget, backwards from the 24 h-early target)

~261 h of working window before the internal target. This session works continuously; the shares below are the skill's ratios, and the calendar dates are hard gates, not estimates.

| Phase | Share | Gate (must be done by, ET) |
|---|---|---|
| 0. Countdown + tool check | – | Sep 23 |
| 1–2. Research: event facts, 5–8 verified winners, research brief | – | Sep 24 |
| 3. Concepts ×3 scored, pick, CONCEPT.md pushed | – | Sep 24 |
| 4. Design direction: PRODUCT.md + DESIGN.md | – | Sep 25 |
| 5. Core build: the wow moment end to end, demo path, model + eval, tests, CI, deploy | ~50 % | Sep 29 |
| 6. Quality passes: critique → audit → polish, live headless pass | (buffer) | Sep 30 |
| 7. Demo video 2:00–3:00, captioned | ~20 % | Oct 2 |
| 8. Submission kit: README, docs, DEVPOST.md, gallery, checklist, model card | ~15 % | Oct 3 |
| 9. Ship: merge to main, live check, HANDOFF.md | ~15 % buffer | Oct 4 · 8:00 PM |

## Environment facts (checked at kickoff)

- Node v22.22.2, npm 10.9.7, Python 3.11.15. 4 vCPU, 15 GB RAM, ~30 GB disk allowance.
- Playwright Chromium present at `/opt/pw-browsers/chromium-1194` (plus Playwright's own ffmpeg-1011 for video capture).
- No system ffmpeg; installed `imageio-ffmpeg` (bundled ffmpeg 7.0.2 at `/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2`).
- `N8N_BASE_URL` is **unset**, so there's no n8n API access in this environment. Any n8n workflow ships as an importable `n8n/*.json` file.
- **Egress policy is restrictive.** Reachable: GitHub (git, api, raw), npm registry, PyPI, Google Fonts, `storage.googleapis.com` (MediaPipe models, TF datasets, Quick, Draw!). **Blocked:** devpost.com (incl. WebFetch), huggingface.co, cdn.jsdelivr.net, unpkg, cdnjs, kaggle, zenodo, UCI, openml, wikipedia, archive.org, download.pytorch.org.
  - Consequence for research: Devpost pages can't be opened directly. Winners are verified through the search index (WebSearch) plus their public GitHub repos, and each brief states exactly which verification it got.
  - Consequence for the build: no Hugging Face weights. On-device ML must use MediaPipe / TF models from `storage.googleapis.com`, or models trained here from data reachable on GitHub / GCS / PyPI. All model files get self-hosted in the repo so the live site has no third-party runtime dependency.
- Design skills available in this session: `ui-demo`, `dataviz`, `make-interfaces-feel-better`, `accessibility`, `web-design-cheatcode`, `3d-motion-site`, `frontend-design-direction`. **Missing:** `impeccable`, `emil-design-skills:animate`, taste-skill, `hypersite`, so these fall back to cloning their public sources (CLAUDE.md *Fallbacks*).

## Log

- **Phase 0 (Sep 23, 10:39 PM ET, 285.3 h left):** kickoff. Read CLAUDE.md, HACKATHON.md, the hackathon-win skill + references + templates. Tool check done (above).
