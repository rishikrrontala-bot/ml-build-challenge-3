# Product

<!-- impeccable:product-schema 1 -->

> **How this file was written:** Rishik delegated every product and design decision for this unattended build ("I'm not available to answer questions. Every decision… is yours"). So impeccable's interview round was not run; every fact below is inferred from `CLAUDE.md`, `HACKATHON.md`, `CONCEPT.md` and the research in `research/`. Inferences are marked *(inferred)*.

## Platform

web

## Stack

Delegated: Vite + TypeScript (no framework; the UI is one tool surface plus a short explainer), TensorFlow.js for the YAMNet backbone with self-hosted weights, pure-TypeScript DSP + trained head + post-processing + caption writer, Web Audio for decoding and the microphone, Vitest + Playwright, GitHub Pages. Chosen because CLAUDE.md sets Vite + TS as the default, the site must be static and keyless, and every model file must be self-hosted (the build environment can't reach CDNs, and judges must never depend on one).

## Users

- **Primary: the person publishing a video** *(inferred)*: a small creator, a teacher, a community group, a student club. They have a finished video and maybe an auto-generated dialogue caption file. They want the video to be accessible to Deaf and hard-of-hearing (DHH) viewers without paying per minute for human SDH captioning, and without uploading private footage. They sit at a laptop, in the editing/publishing moment.
- **Beneficiary: DHH viewers** who read captions and today get "[Music]" at best. We have **no DHH collaborator**; their needs come from published research (*Beyond Subtitles*, ASSETS 2022; *Unspoken Sound*, CHI 2024; DCMP Captioning Key) and must be cited, never ventriloquised.
- **Secondary: a DHH person in a room** *(inferred)*, using **Live** mode on a laptop or phone to see which sounds are happening around them, in very large type.
- **Evaluators: hackathon judges**, on a laptop, often watching the demo video muted, spending minutes, not hours. They need the first screen to explain itself and the sample to work with zero setup.

## Product Purpose

Turn the non-speech part of a soundtrack into standards-style captions (`[knocking on door]`, `[glass shatters]`), on the user's own device, with a model we trained and evaluated openly, so that the caption track tells the whole story and not just the words. Success: a user drops a file (or presses **Try the sample**), reviews the proposed sound captions on a timeline, and leaves with a `.vtt`/`.srt` file (or their dialogue captions merged with sound captions) that they trust because they saw the evidence and approved every line.

## Positioning

- The only tool that treats non-speech captioning as the *whole* job: 50 everyday sound classes (vs YouTube's three tags) written in DCMP style.
- Fully on-device: the audio never leaves the machine, it costs nothing per minute, and it works offline once loaded.
- Honest by construction: every caption shows its confidence and its evidence (the waveform region), nothing exports without human review, and the model's held-out accuracy and **false-caption rate** are published on the site itself.

## Operating Context

- Input: a video (mp4/webm/mov) or audio (wav/mp3/m4a/ogg) file the browser can decode, typically 10 s to 10 min, plus optionally an existing `.srt`/`.vtt` dialogue caption file.
- Output: WebVTT or SRT caption files, downloaded locally.
- Live mode: microphone permission, continuous streaming, a phone or laptop left on a table.
- Caption conventions: DCMP Captioning Key (brackets, lowercase, present tense, name the source).

## Capabilities and Constraints

- Detects the 50 ESC-50 sound classes with our trained head. Speech and music presence come from YAMNet's own pretrained AudioSet head, and are labelled as such.
- It can't tell on-screen from off-screen sounds (DCMP italicises off-screen), identify speakers, caption dialogue (it merges with existing dialogue captions instead), or guarantee detection of safety-critical sounds. It must never be presented as a smoke/fire alarm substitute.
- Temporal resolution ≈ 0.48 s (YAMNet patch hop).
- No backend, no account, no analytics, no API key.

## Brand Commitments

- Name: **Brackets**. The square bracket is the product's own notation (the SDH convention).
- Credit: a visible "Built by Rishik Rontala" plus `<meta name="author" content="Rishik Rontala">`.
- Voice: plain, precise, unshowy; the language of a careful captioner. Present tense, lowercase inside brackets. No hype words, no "AI-powered magic".

## Evidence on Hand

- ESC-50 (Piczak 2015, CC BY-NC 3.0): 2,000 labelled 5-s clips in 50 classes, 5 official folds. Training/eval data.
- Speech Commands (Warden 2018, CC BY 4.0): speech and background-noise negatives, and soundscape backgrounds.
- YAMNet (Google, Apache 2.0): the frozen embedding network.
- Every metric shown anywhere is produced by `ml/` scripts in this repo and stored in `ml/results/`.
- **Absent, and never to be fabricated:** users, testimonials, DHH interviews, usage numbers, partnerships.

## Product Principles

1. **Never caption a sound that wasn't there.** Precision over recall; a false caption misleads the very person relying on it. Measure it, publish it, tune for it.
2. **The human approves.** The model proposes; the person publishing decides. Export is a review outcome, not a button press.
3. **Nothing leaves the device.** Privacy is a feature and the architecture, not a setting.
4. **Speak the captioner's language.** Output follows published captioning standards, so it drops into any player that exists today.
5. **Show the evidence.** Confidence, waveform and evaluation are visible, not buried in docs.

## Accessibility & Inclusion

- WCAG 2.2 AA throughout: contrast, full keyboard path (including the timeline and caption editor), visible focus, `prefers-reduced-motion`, semantic HTML, captions for any media we ship.
- The product's own users include DHH people, so **no information may be conveyed by sound alone** anywhere in the UI; Live mode's alert emphasis is visual (and optional vibration).
- Works at 375 px wide; Live mode is designed phone-first.
