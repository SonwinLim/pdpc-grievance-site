# Hero video repositioning — design

**Date:** 2026-07-19
**Status:** approved by Ray (brainstorming session 19 Jul 2026)

## Goal

The new 18-minute YouTube video ("Denied CCTV After Brain Injury: Why Zero PDPA Access Breach Findings on Record Despite Two Refusals?", ID `aV-i5ts7zFo`) becomes the site's main explainer. The site is repositioned as the supporting evidence layer for the video.

## Decisions (all confirmed with Ray)

1. **Placement:** video embedded in the hero (`#hook`), after the conclusion diagram, before `hook__irony`.
2. **Entry gate:** unchanged; visitors pass the Parliament-assurance gate, then land on the video hero.
3. **`#verify` section:** both older videos (`ldJW-LeMsao` 2025, `HB19sK8jCTw` 2026) and NotebookLM stay; add one `meta` pointer line at the top of the verify grid pointing back to the hero video as the current full account.
4. **Copy:** light touch only. Lead-in above the video + one pointer sentence in `#summary`. Neutral wording chosen over "hides" (site's documentary tone; intent not asserted).
5. **Hero layout:** two-column, video left (~62%), clickable chapter list right (~38%); stacks below 820px per existing breakpoints.

## Approved copy

Lead-in (above video in `#hook`):

> The full account, from the accident to the questions now before Parliament, in one 18-minute video. This video and this site were produced after PDPC revamped its enforcement decisions page without a filter by obligation, a change that removed the public's ability to see the zero-breach pattern the video documents. Everything it states is sourced on this page below.

(Apply curly quotes/apostrophes when inserting into HTML.)

`#summary` pointer (end of lede area, links `#hook`):

> If you prefer to watch rather than read, the video above covers the full account; each section below documents the sources behind it.

`#verify` pointer (meta line, top of verify grid):

> The current full account is the 18-minute video at the top of this page. The items below are earlier summaries, kept as part of the record.

## Implementation notes

- Embed: `https://www.youtube-nocookie.com/embed/aV-i5ts7zFo`, `loading="lazy"`, `allowfullscreen`, iframe title = exact YouTube title. Reuse `.video-frame` 16:9 wrapper.
- Chapter links: `https://youtu.be/aV-i5ts7zFo?t=<seconds>`, `target="_blank" rel="noopener"` (no YouTube JS API; deep-seek inside a nocookie iframe is unreliable without it).
- Chapters (verbatim from YouTube description, curly apostrophes applied):

| t (s) | Label |
|---|---|
| 0 | Parliament's assurance that requested data must be preserved |
| 41 | The accident, brain injury, and need for CCTV evidence |
| 111 | Two CCTV access requests and two refusals |
| 227 | The deletion window and section 22A preservation gap |
| 292 | Formal complaints filed with PDPC |
| 413 | PDPC's "clarity" reasoning and the definition of personal data |
| 518 | The condominiums' stated refusal grounds were not tested as stated |
| 616 | Nine legal questions across six PDPA provisions |
| 768 | Escalation to IMDA and the PDPC Commissioner |
| 835 | Reconstructing the enforcement filter by obligation |
| 860 | Zero adjudicated Access Obligation breach findings in the reconstructed index |
| 946 | Why ordinary regulatory error may not explain the pattern |
| 1017 | Source documents at pdpaaccessrights.sg |
| 1065 | Questions for Parliament |

- New CSS classes `hook__video-row`, `hook__video`, `hook__chapters` in the existing stylesheet; chapter column scrolls independently on desktop if taller than the video.
- Existing "Read the 3-minute summary" button stays below the video block.

## Verification

1. Puppeteer: iframe present with correct src; 14 chapter links with correct `?t=` values.
2. Style audits on `index.html`: `grep -cE "[a-z]'[a-z]"` = 0, straight-quote-in-word = 0, no em-dashes in body prose.
3. Commit, push (GitHub Pages auto-deploy), confirm live page.
