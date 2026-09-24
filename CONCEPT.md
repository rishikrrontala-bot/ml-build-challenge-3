# CONCEPT: Brackets

**Event:** ML Empowerment Build Challenge 3.0 · **Lane:** applied ML for accessibility (outside health, school, law) · **Claimed:** Thu Sep 24 2026, 12:05 AM EDT

**One line:** *Captions for every sound that isn't speech.* Brackets listens to a video's soundtrack on your own device, detects everyday sound events with a model we trained, and writes standards-style sound captions like `[knocking on door]` and `[glass shatters]`. You review them on a timeline and export a caption file.

**The problem:** auto-captions write down the words and drop everything else. YouTube's automatic captions describe exactly three non-speech sounds: [MUSIC], [APPLAUSE], [LAUGHTER] ([Google Research, 2017](https://research.google/blog/adding-sound-effect-information-to-youtube-captions/)). So a Deaf or hard-of-hearing viewer never learns that the door just slammed, the baby is crying offscreen, or the alarm is going off, and the story stops making sense. 430 million people live with disabling hearing loss ([WHO, 2026](https://www.who.int/news-room/fact-sheets/detail/deafness-and-hearing-loss)). Human SDH captioning costs money most small creators, teachers and community groups never spend.

**The users:** (1) DHH viewers who need the sound track in text. (2) The person publishing the video, who wants a standards-compliant caption file without paying per minute or uploading private footage. (These are target users, not people we've interviewed. We lean on published DHH research instead: *Beyond Subtitles*, ASSETS 2022; *Unspoken Sound*, CHI 2024.)

**What it does**
1. Drop in a video or audio file, or press **Try the sample**. Everything runs in the browser; nothing is uploaded.
2. A TypeScript log-mel front end + YAMNet embeddings (in-browser) + **our trained sound-event head** → per-frame probabilities → hysteresis + smoothing → sound events.
3. A caption writer turns events into DCMP-style captions: bracketed, lowercase, present tense, naming the source. It never adds a word the model didn't detect.
4. Review on a timeline (confidence shown, accept/reject/edit), then export **WebVTT / SRT**, or **merge** into an existing dialogue caption file without overlapping lines.
5. **Live** mode: large-type captions of the sounds in the room, from the microphone, on-device.

**Wow moment (first 15 s of the video):** a clip plays muted. `[knocking on door]` lands exactly as the knock does, then `[dog barking]`, then `[glass shatters]`, while a sound strip draws each event under the playhead.

**The ML component (the 30 % criterion):** a model we trained on ESC-50 (2,000 labelled clips, 50 classes, official folds) plus speech and background negatives, on frozen YAMNet embeddings. The held-out evaluation covers clip accuracy (5-fold CV), event-based and segment-based F1 on soundscapes built only from the held-out fold, and **false captions per minute on speech-only audio**, each against a zero-training baseline (YAMNet's own AudioSet labels). Details go in `docs/MODEL-CARD.md` and the README's *Evaluation* section.

**Named prior art:** YouTube auto-captions (3 tags); ElevenLabs and Sonix captioning (a few audio-event tags, cloud, paid); Apple Sound Recognition / Android Sound Notifications (live alerts, not caption files); the *Beyond Subtitles* research prototype (ASSETS 2022). Brackets differs in being fully on-device and free, having an open trained model with a published held-out evaluation and hallucination rate, following DCMP wording, merging into your existing captions, and offering a live room mode.

**Stack:** Vite + TypeScript, TensorFlow.js (YAMNet backbone, self-hosted weights), a pure-TS DSP front end and trained head, Web Audio, Vitest + Playwright, GitHub Pages. Training and evaluation in Python (TensorFlow, scikit-learn, sed_eval, Scaper). No backend, no key, no tracking.

Full scoring: `research/CONCEPTS.md` (A 4.60 · C 4.00 · B 3.65). Research: `research/RESEARCH-BRIEF.md`.
