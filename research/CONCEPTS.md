# Concepts: three candidates scored against the published rubric

Rubric (HACKATHON.md, from the Devpost page): **Technical Implementation 30 % · Creativity & Innovation 20 % · Real-World Impact 20 % · Project Design & UX 15 % · Presentation & Documentation 15 %.**
Scores are 1–5 per criterion; weighted total = Σ(weight × score). Rishik delegated the pick to this session (CLAUDE.md, *Override*), so **the highest total is chosen**.

Constraints every concept had to pass first:
- Lane (HACKATHON.md): applied ML **outside health, school and law**, e.g. accessibility, environment, creative tools, local community.
- No overlap with the siblings (`bash scripts/siblings.sh` on Sep 23, 10:45 PM ET: only *Low Sun*, a sun-glare commute calendar, is claimed) or Rishik's past projects (Explain It Back, Habitat Pulse, Baseline, Loop Room, Hookline, LeaseLeak, Earshot, SAKSI, LARMOR, Shade Debt, Breathing Room, scent-shelf).
- Buildable in this environment: public data reachable from here (GitHub, `storage.googleapis.com`, PyPI), a model we can **train** on a CPU, and inference **in the browser** with no key.

---

## A. Brackets: captions for every sound that isn't speech

**Pitch:** Auto-captions write down the words and drop everything else. YouTube's automatic captions describe exactly three sounds: [MUSIC], [APPLAUSE], [LAUGHTER]. Brackets listens to a video's soundtrack **on your device**, detects 50+ everyday sound events with a model we trained, and writes standards-style sound captions (`[glass shatters]`, `[knocking on door]`, `[dog barking]`, following DCMP's lowercase, bracketed, present-tense rules). You review them on a timeline and export a `.vtt`/`.srt` track, or merge it into the dialogue captions you already have. A **Live** mode captions the sounds in the room around you, in large type.

**Who:** Deaf and hard-of-hearing viewers (430 M people with disabling hearing loss, WHO 2026), and the creators, teachers and small organisations who publish video without paying for human SDH captioning.

**Wow moment (first 15 s):** a clip plays **muted**. `[knocking on door]` appears the instant the knock lands on the timeline, then `[dog barking]`, then `[glass shatters]`, while a live "sound strip" draws each detected event under the playhead.

**The ML (Technical Implementation):**
1. A log-mel front end written in TypeScript (pure function, parity-tested against the Python reference).
2. YAMNet (Google's AudioSet-pretrained MobileNet) as a frozen embedding network, converted to run in the browser.
3. **Our trained head** (MLP on 1024-d embeddings) learned from ESC-50 (2,000 labelled clips, 50 classes, official 5 folds) plus speech and background negatives, with energy-gated weak labels.
4. Temporal post-processing (per-class hysteresis thresholds tuned on validation folds, median filtering, minimum durations) → events → the caption writer.
5. **Evaluation on held-out data:** ESC-50 5-fold CV; event-based and segment-based F1 on synthetic soundscapes built only from the held-out fold (sed_eval, DCASE-style); **false captions per minute on speech-only audio** (a hallucination rate). Every number is compared against a zero-training baseline that maps YAMNet's own AudioSet labels.

**Riskiest unknown:** converting YAMNet to a browser runtime with bit-for-bit comparable embeddings, and domain shift from ESC-50 recordings to film/TV sound. *Mitigation:* a parity test (Python ↔ browser), a built-in sample the model has never seen, and an honest real-world section in `docs/LIMITATIONS.md`.

**Cut first if time runs short:** the Live mode, then SRT merge. The file → captions → export loop is the product.

| Criterion (weight) | Score | Why |
|---|---|---|
| Technical Implementation (30) | **5** | Our own trained model + a DCASE-style held-out evaluation + a baseline comparison + in-browser inference + a TS signal-processing front end with parity tests. Far above a prompt wrapper. |
| Creativity & Innovation (20) | **4** | Everyone builds speech captions and ASL recognisers. Non-speech SDH captioning is a gap named in CHI/ASSETS research but absent from consumer tools. Prior art exists in research (*Beyond Subtitles*, ASSETS 2022), so not a 5. |
| Real-World Impact (20) | **4** | A large, well-documented population; the output is a standard file that plugs into YouTube, Vimeo, LMSs and players today. Not a 5 because it can't claim safety-critical use (smoke alarms need certified devices) and it has no real users yet. |
| Design & UX (15) | **5** | Video + timeline + caption editor is a rich, visual, native canvas for an award-level art direction (caption typography, the bracket as motif). |
| Presentation & Documentation (15) | **5** | The demo is literally *captions on a muted video*, the exact condition judges watch in. The eval tables and model card write themselves from real runs. |
| **Weighted total** | **4.60** | 1.50 + 0.80 + 0.80 + 0.75 + 0.75 |

---

## B. Knock: personal sound alerts you teach in 20 seconds

**Pitch:** A Deaf person's home is full of sounds that matter only to them: *their* doorbell chime, *their* dryer's buzzer, *their* kettle. Built-in sound recognition knows fixed categories. Knock runs in any browser (an old phone on a shelf) and learns your specific sounds from five examples (few-shot prototypes on audio embeddings), then flashes the screen and vibrates when it hears them.

**Wow moment:** record the doorbell 5× → ring it → the whole screen floods orange with `DOORBELL`.

| Criterion (weight) | Score | Why |
|---|---|---|
| Technical Implementation (30) | 4 | Few-shot learning + an episodic evaluation on ESC-50 is real ML, but the trained component is thinner than A's. |
| Creativity & Innovation (20) | 3 | Apple (Sound Recognition, incl. custom appliance/doorbell sounds) and Google (Sound Notifications) ship this; the cross-platform web angle is incremental. |
| Real-World Impact (20) | 4 | Daily, tangible. But alert reliability is safety-adjacent, which raises the honesty bar. |
| Design & UX (15) | 4 | Big, bold alert surfaces; less visual range than a video editor. |
| Presentation & Documentation (15) | 3 | Live-audio demos are hard to show on a muted video: the judge can't hear the doorbell. |
| **Weighted total** | **3.65** | 1.20 + 0.60 + 0.80 + 0.60 + 0.45 |

**Riskiest unknown:** real-room false alarms. **Cut first:** multi-device pairing.

---

## C. Plot Twist: charts that read themselves to blind readers

**Pitch:** Screen readers hit a chart image and say "image". Plot Twist recovers the data behind a bar or line chart image (chart-type classifier + mark detector trained on synthetic charts rendered with randomised styles), then writes verified alt text from the *extracted numbers* and plays a sonification.

**Wow moment:** paste a screenshot of a bar chart → a data table and the alt text "Sales rose from 12 to 31, peaking in March" appear, and the chart plays as rising tones.

| Criterion (weight) | Score | Why |
|---|---|---|
| Technical Implementation (30) | 4 | Genuinely hard (chart derendering). But trained on synthetic data, and the real-chart evaluation would likely be weak or small. |
| Creativity & Innovation (20) | 4 | Fresh for a hackathon, though DePlot/ChartQA research exists. |
| Real-World Impact (20) | 4 | A real barrier for blind students and professionals (overlaps the school lane, which we're avoiding). |
| Design & UX (15) | 4 | Clean, but a narrow surface. |
| Presentation & Documentation (15) | 4 | Visual demo, but errors on real charts would be obvious on camera. |
| **Weighted total** | **4.00** | 1.20 + 0.80 + 0.80 + 0.60 + 0.60 |

**Riskiest unknown:** accuracy on real-world charts (styles, gridlines, stacked bars). **Cut first:** line charts.

---

## Decision

| Concept | Total |
|---|---|
| **A. Brackets** | **4.60** ← chosen |
| C. Plot Twist | 4.00 |
| B. Knock | 3.65 |

**Why A wins beyond the arithmetic:**
- It is the *dominant winning shape* in the research (accessibility: one missing channel turned into another, on-device), without copying any winner.
- Its output is **visible on mute**, which is the condition judges watch videos in (what-wins.md).
- It gives the event's required *held-out evaluation* a natural, rigorous form (DCASE event metrics + a hallucination rate), which a beginner-heavy field will rarely match.
- It carries the **Hookline lesson** by construction: a caption must never name a sound that wasn't there. We measure false captions per minute, show confidence, and keep the human in the loop before export.

**Pre-mortem ("it's judging day and we lost: why?")** and the fix built into the plan:
- *"The captions on the demo clip were wrong."* → The demo clip is chosen honestly (never tuned on), and the editor makes corrections a feature. The video shows one real miss and its fix.
- *"Judges didn't get what non-speech captions are."* → The first frame shows a muted clip with `[knocking on door]` on it. The first sentence names YouTube's three-tag limit.
- *"It's just a pretrained model."* → The README leads its technical section with *our* head vs the zero-training baseline, on the same held-out data.
- *"It didn't load."* → Static site, self-hosted model files (no CDN), a built-in sample, no permissions needed until the user asks for Live.
