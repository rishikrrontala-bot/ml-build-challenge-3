# Winner brief: HawkWatch

**Hackathon:** TreeHacks 2025 (Stanford, 36 h, in person, Feb 2025) · **Prize won:** Grand Prize, $11,000
**Submission URL:** https://devpost.com/software/hawkwatch · **Repo:** not found publicly · **Demo video:** not located
**Verified:** Devpost page returned by the search index ☑ (not opened; blocked) · prize stated by an independent source ☑ ([Stanford Daily, 2025-02-18](https://stanforddaily.com/2025/02/18/treehacks-awards-200000-in-prizes-to-students-from-around-the-world/): "The grand prize of $11,000 was awarded to Hawkwatch") · team member's write-up ☑ ([nilsfleig.com/projects/hawkwatch](https://www.nilsfleig.com/projects/hawkwatch)) · video played ☐

## Pitch, verbatim (as quoted by the Stanford Daily)
> Inspired by the failures of modern surveillance where "crucial moments were missed despite having camera coverage", the team wanted to tackle the "overwhelming challenge security personnel face in monitoring multiple video feeds simultaneously."

## The wow moment
Several live camera feeds on one screen, and the system itself raising an alert, with a written explanation, the moment something dangerous happens. The human only confirms or dismisses.

## Demo teardown
- Length / first 15 s: not observable (video not located).
- Real data: live webcam streams plus uploaded mp4s.

## Scope reality (from the indexed Devpost text)
- Four features described: real-time detection (audio + video + TensorFlow body-pose data sent to Gemini's VLM, email alerts), mp4 upload analysis, a library of saved footage with analysis, and a statistics page with an AI summary, charts and CSV export.
- Commit window: repo not public, so unknown.

## Stack
TensorFlow pose estimation + Gemini VLM + web UI. The stack is part of the story ("pose data + VLM") but the pitch leads with the problem.

## Why this won (one sentence)
A universally understood problem (humans can't watch every feed) turned into a live, visual "the machine noticed first" moment, with a multimodal pipeline that is visibly harder than a chat wrapper.

## Transferable to us
- **Copy:** machine perception running on a *real stream* in real time, with a visible alert as the payoff. Frame the human as the one who confirms.
- **Don't copy:** the surveillance framing (privacy baggage) or a hosted-VLM dependency. Our judges visit cold, with no key.
