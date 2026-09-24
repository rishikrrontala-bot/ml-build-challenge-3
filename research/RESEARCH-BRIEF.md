# Research brief: ML Empowerment Build Challenge 3.0

*Compiled Sep 23–24 2026 (ET) in the unattended cloud session. Winner evidence is in `research/winners/`, and how it was verified (Devpost, Kaggle and YouTube are blocked from this environment) is in `research/winners/_VERIFICATION.md`.*

## 1. The event, verified

| Fact | Value | Source / status |
|---|---|---|
| Deadline | **Mon Oct 5 2026, 5:00 PM PDT = 8:00 PM EDT** | HACKATHON.md (read from Devpost on Sep 23) + the search index's copy of the Devpost overview ("Deadline: Oct 5, 2026 @ 5:00pm PDT"). ⚠ One aggregator ([Startup Grants India](https://www.startupgrantsindia.com/competitions/ml-empowerment-build-challenge-30)) says "Apply by 1 Oct". Devpost is authoritative, but **we plan to be fully submittable before Oct 1** so the discrepancy can't hurt. |
| Organiser | ML Empowerment Foundation (@mlempowermentfoundation, mlempowerfdn@gmail.com) | Devpost title + aggregators |
| Format | Online, global, students (high school + college), **teams 1–5, solo allowed** | search index of the Devpost overview |
| Judges | "Judges will be announced on 9/21/2026" | search index. Names not retrievable from here, so there's no judge-specific bias to exploit. |
| Rubric | Technical Implementation 30 · Creativity & Innovation 20 · Real-World Impact 20 · Design & UX 15 · Presentation & Documentation 15 | HACKATHON.md (Devpost, Sep 23) |
| Required | Title + detailed description (problem, solution, features, technologies, target users); screenshots/videos/demo files; repo + live demo (optional but "provide both"); team details | HACKATHON.md + indexed overview |
| Prior editions | 1.0 (`ml-empowerment-build-challenge.devpost.com`, Apr 7–Jun 16 2026: Best Overall $1,000 + single-winner categories incl. *Most Innovative, Most Impactful, Best Use of Machine Learning, Best Web AI App, Sustainability AI, Data-Driven Insights*). 2.0 (`ml-empowerment-2.devpost.com`, Jun 30–Jul 31 2026). | search index. **No prior-edition winning project could be verified**, so none is cited. |
| Curriculum | The foundation's free, 12-lesson self-paced beginner AI curriculum | search index |

**What the event's own language rewards:** "Learn AI, build real-world projects and create impact". Past category names (*Best Use of Machine Learning*, *Most Impactful*, *Best Web AI App*) say a web app with a *real ML component* aimed at *social good* is exactly on brief. The field is beginner-heavy (a 12-lesson beginner curriculum, ages 13+), so a trained model with an honest held-out evaluation will stand far above the median entry, **as long as the video and page make that visible to a non-expert judge.**

## 2. What won (7 verified winners, 2025–2026)

| Project | Event · prize | Problem shape | Wow moment |
|---|---|---|---|
| [HawkWatch](winners/hawkwatch.md) | TreeHacks 2025 · Grand Prize | institutional pain (too many feeds for humans) | live feeds + the machine flags danger first |
| [BlinkAI](winners/blinkai.md) | TreeHacks 2025 · Best Beginner | accessibility: a channel people can't use | blink at a webcam and words appear |
| [FaceTimeOS](winners/facetimeos.md) | Cal Hacks 12.0 · 1st overall (of 695) | familiar interface → unexpected power | FaceTime your Mac and it works |
| [Gemma Vision](winners/gemma-vision.md) | Gemma 3n Impact Challenge · Google AI Edge prize | accessibility, designed with a blind user | hands-free scene description, no screen |
| [Vite Vere Offline](winners/vite-vere-offline.md) | Gemma 3n Impact Challenge · winner | accessibility (cognitive disability) | photo of a room → 3 spoken steps, offline |
| [PenguinAgent](winners/penguinagent.md) | Gemma 4 Good · 3rd | environment/science, expert user, no connectivity | video in → behaviour report out, offline |
| [GEM-4](winners/gem-4.md) | Gemma 4 Good · 1st | accessibility, physical assistance | "hey GEM" → a robot arm helps |

## 3. The pattern

**Problem shape that keeps winning: accessibility, one missing channel, turned into another.** Five of seven winners take information a person can't access (sight, speech, movement, attention across feeds) and convert it into a form they can. The judged "impact" challenges (Gemma 3n, Gemma 4 Good) were dominated by disability access: 5 of the 7 briefs here, and every Gemma 3n winner named in Google's post.

**Demo shape that keeps winning:** *one live loop, on real input, with the output appearing where the user already looks.* Blink → text. Camera → voice. Feed → alert. Nobody wins with a settings page.

**On-device / offline is now a prize category, not a limitation.** Google created a *Google AI Edge* prize, and three of the seven winners make "no data leaves the device, works with no signal" a headline. For us it's doubly right: CLAUDE.md requires a keyless static site, and a cold judge visit must never fail.

**Training visibly beats wrapping.** The 1st place at Gemma 4 Good trained its own VLA and put the training pipeline in the pitch. For a 30 %-weighted *Technical Implementation* criterion, "we trained a model on real data and here's our held-out evaluation" is the strongest possible claim, and the event's own asks (HACKATHON.md: *evaluation section with real metrics on a held-out set + a model card*) point the same way.

**Scope ceiling:** multi-week online windows (Gemma challenges ran ~6 weeks) let winners ship one loop *plus* real polish: a demo video, a writeup with genuine technical sections, and multiple languages or features. Our window (~11 days of calendar, working continuously) supports: one loop done superbly, one supporting surface, a real evaluation, a real video.

**What winners consistently skipped:** accounts/log-in, settings, dashboards, multi-page marketing sites, test-suite bragging. (We still write tests, because CLAUDE.md requires them, but they're not the pitch.)

**Judge bias:** unknown (judge names not retrievable). Assume a mixed panel of students, educators and practitioners in a beginner-friendly foundation: **explain the ML plainly and show numbers a non-expert can read** ("it caught 8 of 10 door knocks; it invented a caption 0.4 times per minute").

## 4. How judges will likely experience entries (the core asymmetry, applied)

- They'll **watch the video, probably muted** (what-wins.md). A product whose output *is captions* demos perfectly on mute.
- They'll open the live link on a laptop, sometimes a phone. It must work instantly with no key, no upload required (a built-in sample) and no mic permission required.
- They skim the first two sentences. These must state a specific problem: *auto-captions write "[Music]" and nothing else, so a Deaf viewer never learns the door just slammed.*

## 5. Implications for our concept (carried into CONCEPTS.md)

1. **Lane:** accessibility (the suggested lane, and the dominant winning shape). Avoid health, school and law (HACKATHON.md) and the siblings' lanes (`scripts/siblings.sh`: *Low Sun* sun-glare calendar is the only claim so far).
2. **ML:** a model *we train* on real public data, with a held-out evaluation that a non-expert can read, running **in the browser** with no key.
3. **Demo:** one live loop whose output is visible on mute, with the wow in the first 15 s.
4. **Honesty:** name the prior art, and state the limitations first (what-wins.md: "naming the limitation yourself").

## 6. Domain facts we'll lean on (all cited)

- **430 million people** have disabling hearing loss, projected to exceed 700 million by 2050 ([WHO fact sheet, updated Mar 2026](https://www.who.int/news-room/fact-sheets/detail/deafness-and-hearing-loss)).
- YouTube's automatic captions describe **exactly three** non-speech sounds: [MUSIC], [APPLAUSE], [LAUGHTER]. Google chose them because other sounds are ambiguous ("a sound like [RING] raises the question of what rang") ([Google Research blog, 2017](https://research.google/blog/adding-sound-effect-information-to-youtube-captions/); [TechCrunch](https://techcrunch.com/2017/03/23/youtubes-automatic-captioning-system-can-now-describe-sound-effects/)).
- Captioning standards: sound effects go **in brackets, lowercase, present tense, and name the source** unless it's visible on screen ([DCMP Captioning Key: Sound Effects and Music](https://dcmp.org/learn/602-captioning-key---sound-effects-and-music)).
- DHH research: interviews with 11 DHH participants found interest in having important non-speech sounds included in captions, and a sound-event-detection authoring prototype was tested with creators ([*Beyond Subtitles*, ACM ASSETS 2022](https://dl.acm.org/doi/10.1145/3517428.3544808)). Automatic captioning omits many non-speech elements that matter to the narrative ([*Unspoken Sound*, CHI 2024](https://dl.acm.org/doi/full/10.1145/3613904.3642162)). Related work: *OnomaCap* (CHI 2025), and *"Choices? That's the dream"* ([Frontiers in Computer Science, 2025](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1575176/full)).
