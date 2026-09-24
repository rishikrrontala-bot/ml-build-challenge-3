# Design: Brackets

> Art direction for this entry, chosen through impeccable's new-work flow (roll seed `e70982b7`, degraded, no challengers; see `.impeccable/surfaces/index-html.md`). This file was written before the build to fix the direction, and is **re-documented from the shipped UI at the finish** so it describes what exists, not what was hoped for.

## The idea

A screenplay is where sound is first written down: *"A door SLAMS. Somewhere, a dog BARKS."* Brackets does the reverse. It listens to a finished soundtrack and writes the sounds back into words. So the tool **is a shooting-script page that types itself as it listens**, and its output wears the other uniform everyone recognises: the **broadcast caption box** (white monospaced text on an opaque black box).

Two artefacts, one grammar:

| Artefact | Where it appears | What it carries |
|---|---|---|
| **The shooting script** (white 20-lb pages, two brass brads, Courier, margin numbers, revision colours) | the review surface, section structure, the evaluation ("coverage") | the model's proposals, the human's revisions, the evidence |
| **The CEA-608 caption box** (white Courier on black) | captions over video, Live mode, primary buttons | the output a viewer actually reads |

**Refused:** the category default (a gradient "AI caption generator" hero with an upload card and testimonials) and its opposite (a dark pro editor with neon waveforms). Also banned by CLAUDE.md: purple/blue gradients, centered-card SaaS, emoji headers, Playfair + drop shadows, blobs, stock illustration.

## Colour

Strategy: **Drenched ground + paper + ink**, with the WGA revision colours as *state*, never as decoration.

| Token | Value | Role |
|---|---|---|
| `--ground` | `#C9DBEE` | Revision-blue paper. The whole viewport field. |
| `--page` | `#FFFFFF` | Script pages, panels. |
| `--ink` | `#161514` | Typewriter ink: all body text, rules, primary fills. |
| `--ink-soft` | `#4B4A47` | Secondary text (8.86:1 on page, 6.27:1 on ground, ≥ 4.63:1 on every revision colour). |
| `--rule` | `rgba(22,21,20,.16)` | Hairlines, page edges. |
| `--rev-pink` | `#F4C6D2` | Struck/rejected lines (with strikethrough; colour is never the only signal). |
| `--rev-yellow` | `#F4E48C` | "Needs review": low confidence. |
| `--rev-green` | `#C6E4BA` | Approved lines. |
| `--rev-goldenrod` | `#E3B54A` | The current cue (playhead highlight). |
| `--brass` | `#A7843B` | The two brads. The only metallic, the only ornament. Decorative only, never text (3.5:1 on page). |
| `--box` / `--box-ink` | `#000` / `#FFF` | Caption boxes (608), primary buttons, Live mode. |

Every text/ground pair meets WCAG 2.2 AA (computed, not eyeballed): ink on page 18.24:1, ink on ground 12.90:1, ink on the lowest revision colour (goldenrod) 9.53:1, white on box 21:1.

## Type

**Courier Prime** (Quote-Unquote Apps, SIL OFL), 400 / 700 / italics, **self-hosted** (no request leaves the page, consistent with "nothing leaves your device"). One family, because a screenplay has one family. Hierarchy comes from what scripts use: CAPS, underline, indentation, weight, and white space, not size ladders.

| Role | Spec |
|---|---|
| Body / script lines | 16 px / 1.5 (the web's 12-pt), `ch`-based measure of 61ch (Courier 10 cpi × 6 in) |
| Slug lines (section heads) | 16 px CAPS bold, e.g. `INT. YOUR BROWSER — NIGHT` |
| Title page | `BRACKETS` in bold caps, underlined, 2.25–4 rem fluid; everything else stays at script size |
| Margin numbers / timecodes | 14 px tabular (Courier is monospaced), `--ink-soft` |
| Caption box text | 20–28 px (fluid) 400, white on black, 0.25em horizontal padding per line, as broadcasters do |

Screenplay indents are expressed in `ch` from the text edge: action 0, parenthetical 15ch, dialogue 10ch (35ch wide), character cue 22ch, transition right-aligned.

## Space

One rhythm, counted in script **lines**: `--line: 1.5rem`. Gaps are 1, 2 or 4 lines. More space above a slug line than below it, as in a script.

## Components (grammar)

- **Page:** white, 1 px `--rule` edge, a second sheet offset 4 px behind (a paper stack, not a blur shadow), two brass brads at the left margin (3-hole punch, middle hole empty). The page number at top right, followed by a period, as scripts do: `1.`
- **Cue line** (one detected sound): margin timecode (left), the caption in brackets at the dialogue indent, a confidence parenthetical below it (`(0.91 — dog)`), and controls in the right margin. Human-edited lines get a revision asterisk `*` in the right margin.
- **Primary button:** a caption box: black, white Courier caps. **Secondary:** 1.5 px ink outline. Hit area ≥ 44 px.
- **Caption over video:** a 608 box, centred bottom, max 32 characters per line, 2 lines, never over burned-in content.
- **Sound strip:** under the video, one lane per detected class, events as ink bars; the playhead is a goldenrod rule.
- **Coverage grid** (evaluation): a script-coverage form (Premise / Structure… become Accuracy / Precision / False captions / Timing), graded honestly with real numbers.

## Motion

Decided with Emil Kowalski's *animate* sequence (should it animate → purpose → tool → properties → curve and duration → interruption → exit):

- **Typewriter reveal** of a new cue line: *purpose*, it shows the model writing as it listens. CSS `steps()` clip reveal, ≤ 320 ms per line, interruptible (a new line finishes the old one instantly). Reduced motion: appears instantly.
- **Caption box pop-on:** no animation. Broadcast pop-on captions appear instantly, and a fade would delay reading.
- **Playhead:** tied to `currentTime` (rAF), no easing.
- **Page stack on file load:** a single 180 ms `ease-out` translate of the new page, once. Reduced motion: none.
- Nothing loops, nothing floats, nothing parallaxes.

## Live mode

The script disappears; the screen becomes one enormous caption box (black field, white Courier, 8–12 vw). A brief invert flash for alarm-class sounds (off under reduced motion, never faster than 3 Hz).
