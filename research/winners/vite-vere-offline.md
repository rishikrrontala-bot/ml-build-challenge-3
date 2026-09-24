# Winner brief: Vite Vere Offline

**Hackathon:** Google: The Gemma 3n Impact Challenge (Kaggle, 2025) · **Prize won:** listed among the challenge winners in Google's winners post
**Submission URL:** https://www.kaggle.com/competitions/google-gemma-3n-hackathon/writeups/vite-vere-offline · **Repo:** https://github.com/guidomarangoni/vite-vere-offline (cloned and read) · **Demo video:** not located
**Verified:** repo opened ☑ (Flutter app, MIT licence, last commit 2025-08-06; README: "Developed by Guido Marangoni for the Google Gemma 3n Hackathon") · winner status stated by independent sources ☑ ([blog.google winners post](https://blog.google/innovation-and-ai/technology/developers-tools/developers-changing-lives-with-gemma-3n/); StartupHub.ai: "Vite Vere Offline, which empowers individuals with cognitive disabilities by translating images into spoken instructions for daily tasks while operating without an internet connection") · Kaggle page ☐ (blocked) · video played ☐

## Pitch, verbatim (repo README)
> A Flutter application demonstrating the power of on-device multimodal AI using the `flutter_gemma` package with Google Gemma 3 Nano models. The app works completely offline and offers two main features: an inclusive AI assistant for people with intellectual disabilities and assistance for room organization.

## The wow moment
Photograph a messy room and get three concrete, simple steps read aloud, fully offline.

## Demo teardown
- Not observable (video not located).

## Scope reality
- Two features working (inclusive chat assistant; room-photo → structured 3-step plan with TTS), 5 languages, model download manager, retries and JSON repair.
- It is the **offline evolution of an earlier Gemini-API project** by the same author (Gemini API Developer Competition). Much of the design was pre-existing; the hackathon work was the port to on-device.

## Stack
Flutter + `flutter_gemma` (MediaPipe LLM Inference) + Gemma 3n E2B/E4B. The offline port is the story.

## Submission page shape
README: badges → one-paragraph pitch → "Project Genesis" (from online to offline) → "Advantages of the Offline Approach" (privacy, cost, accessibility) → features → architecture.

## Why this won (one sentence)
A clear population (people with intellectual disabilities), a concrete daily task, and a principled "offline = private, free, works anywhere" argument.

## Transferable to us
- **Copy:** spell out *why* on-device matters for this user (privacy of home audio, no cost per minute, works offline), as its own README section.
- **Don't copy:** LLM-generated instructions whose correctness can't be measured. Our output must be evaluable against ground truth.
