# Winner brief: GEM-4 (Gemma Embodied 4 Physical Assistance)

**Hackathon:** Google: The Gemma 4 Good Challenge (Kaggle, 2026) · **Prize won:** 1st place
**Submission URL:** https://www.kaggle.com/competitions/gemma-4-good-hackathon/writeups/new-writeup-1778618527713 · **Repo:** not located · **Demo video:** https://www.youtube.com/watch?v=OhaIA3bYwmg (not played; blocked)
**Verified:** Kaggle writeup + YouTube video returned by the search index ☑ (not opened; blocked) · placing stated by independent sources ☑ ([blog.google winners post](https://blog.google/innovation-and-ai/technology/developers-tools/winning-entries-gemma-4-good-challenge/); [StartupHub.ai](https://www.startuphub.ai/hardware/gemma-4-good-challenge-winners-showcase-edge-ai-innovation): "1st Place: GEM-4") · video played ☐

## Pitch, verbatim (as indexed)
> GEM-4 is a physical robotic assistant and control pipeline built to physically assist elderly and disabled individuals with daily living tasks.

## The wow moment
Someone says "hey GEM" and a wearable robot arm does a physical task: a language model's output becoming motion.

## Demo teardown
- Not observable (video not played).

## Scope reality
- Wake word → speech-to-text → a Gemma 4 E2B vision-language-action model taking images + joint state → robot control, plus a human-demonstration data pipeline for training.

## Stack
Gemma 4 E2B VLA + custom data-generation and training pipeline. **They trained something**, and the training pipeline is part of the pitch.

## Why this won (one sentence)
The most technically ambitious entry (a trained VLA on real hardware) pointed at the most sympathetic users (people who need physical help), and demoed physically.

## Transferable to us
- **Copy:** show the *training* story (our own data pipeline, our own trained model, our own held-out numbers), not just inference on someone else's model.
- **Don't copy:** hardware scope. A student online hackathon rewards what a judge can open in a browser.
