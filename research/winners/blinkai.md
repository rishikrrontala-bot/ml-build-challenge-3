# Winner brief: BlinkAI

**Hackathon:** TreeHacks 2025 · **Prize won:** "Best Beginner" (per the Stanford Daily)
**Submission URL:** https://devpost.com/software/blinkai · **Repo:** not located (the `github.com/blink-ai` org is unrelated) · **Demo video:** not located
**Verified:** Devpost page returned by the search index ☑ (not opened; blocked) · prize stated by an independent source ☑ ([Stanford Daily, 2025-02-18](https://stanforddaily.com/2025/02/18/treehacks-awards-200000-in-prizes-to-students-from-around-the-world/): "BlinkAI, an accessibility software program which translates blinked morse code messages into text, received the 'Best Beginner' award") · video played ☐

## Pitch, verbatim (Devpost text as indexed)
> BlinkAI translates blinks into Morse code, converts them into text, and sends prompts to AI, unlocking seamless, hands-free communication instantly. […] built to help millions of people living with Parkinson's, ALS, and other mobility challenges.

## The wow moment
A person blinks at a webcam and words appear. A body signal becomes language, with no special hardware.

## Demo teardown
- Not observable (video not located). The indexed text shows a live webcam loop.

## Scope reality
- One loop working end to end: webcam → blink detection → Morse decode → text → AI prompt.
- The follow-up project "Aloud" (indexed on Devpost) later reused the technical foundation.

## Stack
Webcam computer vision + Morse decoding + an LLM call. The algorithm (blink → Morse → text) is the story.

## Why this won (one sentence)
A specific group with a specific barrier, and a single cheap sensor (the webcam) turned into a communication channel, legible in five seconds of demo.

## Transferable to us
- **Copy:** accessibility with a *single obvious loop*: a signal the user can't access (for us, sound) turned into the text they need, shown live.
- **Don't copy:** medical framing (our lane excludes health; the event also says nothing about clinical claims) or the LLM step that adds nothing to the core loop.
