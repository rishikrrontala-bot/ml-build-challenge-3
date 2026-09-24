# PROGRESS: ML Empowerment Build Challenge 3.0

Running log for the unattended cloud build. **A resumed session should read this first and continue from the first unchecked phase.**

**Deadline:** Mon Oct 5, 2026 · 8:00 PM EDT (`2026-10-06T00:00:00Z`)
**Internal "all deliverables done" target:** Sun Oct 4, 2026 · 8:00 PM EDT (24 h buffer, per CLAUDE.md lesson 2)

## Countdown log

| When (ET) | Hours to deadline | Phase |
|---|---|---|
| Wed Sep 23 2026 · 10:39 PM EDT | 285.3 h | 0: kickoff |
| Wed Sep 23 2026 · 10:55 PM EDT | 285.1 h | 1–3 done (research + concept pushed); starting ML pipeline |
| Wed Sep 23 2026 · 11:06 PM EDT | 285.0 h | **Paused by Rishik** ("push everything and stop"). Phase 4 done, phase 5 started. |

## Phase plan (hackathon-win Phase 4 budget, backwards from the 24 h-early target)

~261 h of working window before the internal target. This session works continuously; the shares below are the skill's ratios, and the calendar dates are hard gates, not estimates.

| Phase | Share | Gate (must be done by, ET) |
|---|---|---|
| 0. Countdown + tool check ✅ | – | Sep 23 |
| 1–2. Research: event facts, 5–8 verified winners, research brief ✅ | – | Sep 24 |
| 3. Concepts ×3 scored, pick, CONCEPT.md pushed ✅ (**Brackets**) | – | Sep 24 |
| 4. Design direction: PRODUCT.md + DESIGN.md ✅ (screenplay world) | – | Sep 25 |
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
- **Phases 1–3 (Sep 23, 10:55 PM ET, 285.1 h left):** research + concept pushed (`eed83dd`). Devpost is blocked, so the 7 winners were verified via search index + independent sources + cloned repos (`research/winners/_VERIFICATION.md`). Concept **A. Brackets** (non-speech SDH sound captions, on-device, trained head on YAMNet embeddings) scored 4.60 vs 4.00 / 3.65. Deadline re-check: Oct 5 5 PM PDT confirmed via index; one aggregator says "apply by Oct 1", so **aim to be fully submittable before Oct 1**.
- **Rishik's instruction (10:55 PM ET):** save (commit + push) at **11:20 PM ET** and whenever credits may be running low. This session can't see the credit balance, so **push after every step**.

## Resume guide (if this session dies)

The work dir `/home/user/work` (data, venv) is NOT in the repo; recreate it:
```bash
mkdir -p /home/user/work/data && cd /home/user/work
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/karolpiczak/ESC-50 data/ESC-50   # 1.4 GB, 2000 clips
curl -o data/yamnet.h5 https://storage.googleapis.com/audioset/yamnet.h5                    # YAMNet Keras weights
curl -o data/mini_speech_commands.zip https://storage.googleapis.com/download.tensorflow.org/data/mini_speech_commands.zip
git clone --depth 1 --filter=blob:none --sparse https://github.com/tensorflow/models tfmodels && (cd tfmodels && git sparse-checkout set research/audioset/yamnet)
python3 -m venv venv && venv/bin/pip install "tensorflow-cpu==2.18.*" "tf_keras==2.18.*" tensorflowjs numpy scipy soundfile resampy scikit-learn pandas sed_eval matplotlib
```
(`scaper` fails to build here because of soxbindings, so we use our own soundscape mixer.)

ML plan (see CONCEPT.md): TS log-mel front end (YAMNet params: 16 kHz, 25 ms/10 ms STFT, 512 FFT, 64 mel 125–7500 Hz, log(x+0.001), 96-frame patches hop 48) → YAMNet backbone in TF.js (self-hosted, float16) → our MLP head (trained on ESC-50 folds 1–4, energy-gated frame labels + speech/background negatives) → hysteresis post-processing → DCMP-style caption writer. Eval: ESC-50 5-fold CV clip accuracy; held-out fold-5 synthetic soundscapes with sed_eval segment/event F1; false captions per minute on speech-only audio; all vs a zero-training baseline that maps YAMNet's AudioSet labels.

- **Phase 4 (Sep 23, ~11:00 PM ET):** PRODUCT.md (inferences labelled, since Rishik delegated all decisions), DESIGN.md, and the impeccable surface brief with direction contract (`.impeccable/surfaces/index-html.md`). Roll seed `e70982b7` ran degraded (impeccable.style blocked), assigned candidate 4 = **screenplay / shooting-script world** (Courier Prime, white pages + brass brads on revision-blue ground, WGA revision colours as states, CEA-608 caption boxes). Contrast ratios computed.
- **Phase 5 started (Sep 23, 11:06 PM ET), then PAUSED on Rishik's instruction.** Done so far:
  - `ml/common.py`, `ml/yamnet_core.py`: NumPy front end == TF to 5e-5; backbone embeddings == official to 3e-5.
  - `ml/export_backbone.py` → `public/model/yamnet.{json,bin}` (BN folded, float16, 7.46 MB) + `audioset-classes.json`. Fidelity: `ml/results/backbone_export.json` (cosine ≥ 0.99998, top-1 agreement 100 %).
  - `ml/extract.py` (ESC-50 + speech/background negative embeddings → `/home/user/work/cache/*.npz`). **It was still running when paused (~40 % done); the cache lives outside the repo, so rerun it on resume** (`cd ml && ../../work/venv/bin/python extract.py`, ~30 min).
  - Web app scaffold: `package.json` (Vite 6, TS 5, Vitest 3, Playwright 1.56, tfjs-core/webgl/cpu 4), `src/dsp/fft.ts`, `src/dsp/logmel.ts`, `src/model/half.ts`. **Not yet tested or wired up.**

## Next steps on resume (in order)

1. Recreate `/home/user/work` (Resume guide above; also `sc_bg`: stream `speech_commands_v0.02.tar.gz` from GCS and extract `_background_noise_/`; `unzip mini_speech_commands.zip -d data/msc`). Rerun `ml/extract.py`.
2. `ml/make_fixtures.py`: dump a deterministic synthetic waveform + its patches/embeddings/scores (float16 path) to `tests/fixtures/`; Vitest parity tests for `fft.ts`, `logmel.ts`, `half.ts`, then `src/model/backbone.ts` (TF.js ops forward pass reading `public/model/yamnet.json`) against the embeddings.
3. `ml/train.py`: MLP head (1024→256→50, sigmoid, energy-gated frame labels, speech/background negatives); ESC-50 5-fold CV; zero-training baseline = YAMNet AudioSet labels mapped to ESC-50 classes; export `public/model/head.json`.
4. `ml/soundscapes.py` + `ml/evaluate.py`: held-out fold-5 soundscapes (own mixer; scaper won't build), sed_eval segment/event F1, false captions/min on speech-only audio, onset error; results in `ml/results/`.
5. TS: head, post-processing (hysteresis, median, min duration), DCMP caption writer, VTT/SRT export + dialogue merge, the screenplay UI, Live mode, the sample clip; then Vitest + Playwright e2e + CI workflow; deploy and verify live.
6. Then phases 6–9 as planned. Aim to be fully submittable before **Oct 1** (aggregator "apply by" hedge).
