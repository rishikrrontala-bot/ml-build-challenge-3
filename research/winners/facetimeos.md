# Winner brief: FaceTimeOS

**Hackathon:** Cal Hacks 12.0 (Oct 2025, SF, in person; 695 projects per the team) · **Prize won:** 1st Place Grand Prize / 1st Overall
**Submission URL:** https://devpost.com/software/facetime-macos-ai-agent · **Repo:** https://github.com/ThePickleGawd/FaceTimeOS (cloned and read) · **Demo video:** https://www.youtube.com/watch?v=zN96RdE0OSg (not played; YouTube blocked)
**Verified:** repo README opened ☑ ("🏆 **1st Place Grand Prize** at Cal Hacks 12.0 (world's largest collegiate hackathon)") · independent source ☑ (team member's post, [blog.dylanlu.com/cal-hacks-12](https://blog.dylanlu.com/cal-hacks-12/), "1st Place Grand Prize out of 695 projects") · Devpost page ☐ (blocked) · video played ☐

## Pitch, verbatim (repo README)
> Control your entire Mac with AI voice Agents, via: FaceTime: Text your Mac asking to start a FaceTime, it start a session and share screen. Then, talk naturally to instruct any computer-related task.

## The wow moment
You FaceTime your own computer and talk to it, and it does the task on screen. A native, familiar interface (FaceTime) turned into a control surface nobody expected.

## Demo teardown
- A YouTube demo plus an embedded iMessage demo clip in the README. Recorded, not live.
- Real data: the actual Mac being controlled.

## Scope reality
- Three parts working together: a fork of Agent-S (computer use), a Flask backend for iMessage/FaceTime + voice, and a front-end showing the agent's actions.
- The README admits a dependency is gone ("The UI Grounding endpoint is no longer live"), which is honest scope-telling.
- Last commit 2025-10-31, after the event (README polish).

## Stack
Agent-S (open-source SoTA computer-use agent), Flask, a web UI, a hosted LLM (Grok/OpenAI), Fish Audio TTS/STT, BlackHole audio routing. The "we built on the SoTA open-source framework and extended it" claim is part of the story.

## Submission page shape
README leads with the prize, then the video thumbnail, then a system diagram (`docs/diagram.png`), then quick start and "Why FaceTimeOS?".

## Why this won (one sentence)
An absurdly simple interaction (call your computer) on top of a genuinely hard system, demoed end to end on real hardware.

## Transferable to us
- **Copy:** a familiar format carrying an unexpected capability. For us, the familiar format is the **caption track** everyone already knows. Lead the README with the video, then a diagram.
- **Don't copy:** the key-gated setup. Ours must work cold in a browser.
