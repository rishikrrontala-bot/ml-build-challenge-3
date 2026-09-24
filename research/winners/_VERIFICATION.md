# How these winners were verified (read this first)

This cloud session's egress policy **blocks devpost.com, kaggle.com, youtube.com, blog.google, stanforddaily.com and x.com**, for both `curl` and WebFetch (see `PROGRESS.md`, *Environment facts*). So the skill's "open the submission page" step could not be done literally. Each brief says exactly what *was* checked:

| Check | How it was done here |
|---|---|
| Project exists + prize | The search index (WebSearch) returned the project's own page (Devpost / Kaggle writeup) **and** an independent report of the prize (a newspaper, the organiser's or sponsor's blog, or the team's own repo README). A winner goes in only when two independent sources agree. |
| Repo | Where a public repo exists, it was **cloned and read** (GitHub is reachable). The README's prize claim and commit dates are quoted from the clone. |
| Demo video | **Not played** (YouTube blocked). Where the URL is known it's recorded, so Rishik can watch it. |

**Prior editions of this exact event** (ML Empowerment Build Challenge 1.0, `ml-empowerment-build-challenge.devpost.com`, Apr–Jun 2026; 2.0, `ml-empowerment-2.devpost.com`, Jun 30–Jul 31 2026) exist, but no winning project from either is in the search index, and the galleries can't be opened from here. **No prior-edition winner is cited, because none could be verified.** The research falls back down the skill's ladder: same sponsors (Featherless, Momen: no indexed winner write-ups either), then same-domain winners from the last ~18 months (student hackathons + "AI for good" challenges judged on impact and technical execution).
