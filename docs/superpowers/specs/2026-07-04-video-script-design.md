# Video Script Design — PDPC Grievance: The Story

**Date:** 2026-07-04
**Status:** Approved (awaiting implementation plan)
**Output:** 10-minute YouTube video, first-person narration by Ray Lim, produced via `/yt-intake`

---

## Summary

A 13-scene, 10-minute YouTube video telling the story behind [pdpaaccessrights.sg](https://pdpaaccessrights.sg/). Ray Lim narrates in first person — from the motorcycle accident that erased his memory, through the double denial by two condominiums, PDPC's invented reasoning (the "clarity test"), IMDA's non-oversight, and the discovery that across 384 published PDPC enforcement actions, the Access Obligation has produced zero breach findings. The script is structured as a yt-intake-ready markdown file: each scene is a self-contained block with narration text, image generation prompt, timestamp, and visual style tag.

**Audience:** General public (YouTube)
**Narrator:** Ray Lim, first person
**Tone:** Documentary-first, crescendo — factual and understated for the first half; emotional register rises as the systemic pattern becomes undeniable

---

## Scene Breakdown (13 scenes, ~10 minutes)

| # | Scene | Time | Duration | Visual style |
|---|---|---|---|---|
| 1 | **Hook** — "Parliament said X. PDPC did Y." The contradiction in 30 seconds. | 0:00 | 30s | Clean/systemic |
| 2 | **The accident** — Brain injury, subarachnoid haemorrhage, total memory loss. The footage is the only record of what happened. | 0:30 | 60s | Hand-drawn |
| 3 | **The denials** — Scotts Tower MA refuses footage, company name, DPO contact, escalation path. Complainant hunts DPO identity from zero. Suites@Cairnhill DPO gives false legal advice in writing ("police-only"), then dismisses Complainant's correct PDPA challenge as "difficulty understanding." Neither cites a ground in s.21(3) or the Fifth Schedule. | 1:30 | 105s | Hand-drawn |
| 4 | **The deletion window** — Security guards: "many months." New MA later: "20–30 days." PDPC later: "17 days" (accepted without verification). At the time, the Complainant knew none of this. All he knew: the footage existed, and nobody would tell him how long he had. | 3:15 | 45s | Hand-drawn |
| 5 | **Filing with PDPC** — Complaint filed. And then — silence. Months pass. No investigation opens. No update. | 4:00 | 45s | Hand-drawn |
| 6 | **The clarity test (Maradona Beat 1)** — PDPC uses the Complainant's own handphone video of the CCTV screen to determine "not personal data." The standard they applied — face or plate must be visible — appears nowhere in the PDPA. The original footage is gone. Nobody can check what was on it. The handball: a goal scored with something not in the rules. | 4:45 | 60s | Mixed (opens hand-drawn, cross-fades to systemic) |
| 7 | **Two cases, two invented reasonings** — MCST 3615: "not personal data" (the MCST never said that — they said "police-only"). MCST 4599: "footage overwritten before formal refusal" (ignoring the verbal refusal and the false "no footage" claim that preceded the overwrite). PDPC substituted its own reasoning for what both condos actually said. Neither stated refusal ground was tested against s.21(3) or the Fifth Schedule. | 5:45 | 75s | Clean/systemic |
| 8 | **Nine questions, one response** — Escalation to PMO, ministers, President's Office. Nine legal questions spanning six PDPA sections. PDPC's response to every question is identical: "The Guidelines are not determinative; the PDPA takes precedence." They never name which guideline, which clause, or how they conflict. The decisions were withheld until forced. Matter declared closed. | 7:00 | 60s | Clean/systemic |
| 9 | **IMDA — the oversight that didn't oversee** — IMDA IAU finds "no wrongdoing" without addressing the material facts. Same pattern: delay, non-engagement, dismissal. The oversight body mirrors the regulated body. | 8:00 | 45s | Clean/systemic |
| 10 | **The 384 cases (Maradona Beat 2)** — Across 384 published PDPC enforcement actions, the Access Obligation has produced zero breach findings. Not one. Across that entire register, only two cases involve a complainant demanding access to their own CCTV data and being refused — and both are the Complainant's. The clarity test, applied consistently, explains this. Maradona's quote: "a little bit the hand of God, a little bit the head of Maradona." Not quite admitting. Not quite denying. PDPC's one-line reply sent nine times — same energy. | 8:45 | 60s | Clean/systemic |
| 11 | **The only explanation** — This is not uneven regulatory failure. Every decision, at every level, in the same direction. Invented reasoning, uniform non-responses, withheld decisions, declared closed. Inconsistent with ordinary error. Consistent with a de facto policy of non-enforcement. | 9:45 | 30s | Clean/systemic |
| 12 | **pdpaaccessrights.sg** — The site. Why it exists. All the evidence is public. The enforcement register is public. The parliamentary answer is public. The decisions are public. | 10:15 | 20s | Mixed |
| 13 | **Call to action** — "If the Access Obligation has produced zero breach findings across over a decade, is the obligation being enforced at all? And if not, by what mechanism, and by whom?" | 10:35 | 10s | Clean/systemic |

**Total runtime:** ~10:35 (10 minutes with headroom for pacing)

---

## Output Format

The script file (`docs/superpowers/specs/2026-07-04-video-script.md`) contains 13 scene blocks. Each block follows this template:

```markdown
---
## Scene N — Title [start–end] · duration · visual-style
---

**What happened:**
[2–4 sentences of factual context — the source-anchor for verification]

**Narration:**
[Voice-over text Ray will read. Conversational, short sentences, active
voice. No "furthermore" or "notwithstanding." Natural speech patterns.]

**Image prompt:**
[Visual generation prompt including: subject, composition, colour
direction, emotional register, visual style tag. Sufficient detail
for MiniMax image generation via yt-intake frame batch.]
```

### Field definitions

| Field | Purpose | Feeds into |
|---|---|---|
| `Scene N — Title [start–end] · duration · visual-style` | Header with timing and style tag | yt-intake timestamp anchoring and frame-batch routing |
| `What happened` | Factual grounding — ensures narration stays true to the verifiable record | Quality control, source verification |
| `Narration` | The actual voice-over text Ray will read | TTS generation or live recording |
| `Image prompt` | Visual generation prompt tagged with style mode | MiniMax image generation via yt-intake frame batch |

### Design rules

- **Narration is spoken-word, not written-prose.** Short sentences. Active voice. No academic connectives. Ray's natural Singapore English speech patterns — not stilted, not scripted-sounding.
- **Image prompts include emotional direction**, not just subject matter. The visual style tag (`hand-drawn` or `clean/systemic`) determines the generation approach.
- **"What happened" is the source-anchor.** Every narrative claim must trace to a verifiable primary source (PDPC decision, PDPA statute, parliamentary record, email correspondence in the Complainant's possession). This mirrors the site's source-discipline rule.
- **No fabricated quotes.** Every quote in narration comes from a verifiable source. If in doubt, paraphrase with a clear "[paraphrased]" marker.
- **Curly quotes throughout** in the script file — matches site style.
- **Total file estimate:** 2,500–3,500 words of narration across 13 scenes.

---

## Visual Style Spec

Two visual modes, each with distinct prompt rules.

### Hand-drawn (scenes 2–5: the personal journey)

| Attribute | Rule |
|---|---|
| **Style reference** | Ink-and-wash illustration, loose linework, soft watercolour undertones |
| **Figures** | Suggestive, not photorealistic. No detailed faces — silhouettes or partially rendered features. The viewer projects themselves in. |
| **Colour palette** | Muted: charcoal grey, warm ochre, hospital blue, muted teal. One accent per frame — a streetlamp glow, a CCTV red dot. |
| **Composition** | Figures are small in frame. The system is big — tall counters, wide desks, long corridors. The Complainant is never centred. |
| **Emotion** | The posture tells the story. Hunched shoulders. Hands gripping a phone. A figure alone at a table stacked with papers. |

### Clean/systemic (scenes 1, 7–13: the mechanism)

| Attribute | Rule |
|---|---|
| **Style reference** | Editorial infographic — flat vectors, typographic layouts, document-like framing |
| **Colour palette** | Black, white, one accent (Singapore statutory red — `#C41230` — used sparingly). Grey for secondary text. |
| **Composition** | Split-screen for contradictions. Quote-in-frame for verbatim text. Number-punch moments (384, 0, 9) get full-frame typography. |
| **Emotion** | Restraint. The power is in juxtaposition — two legal texts side by side that cannot both be true. No melodrama. |

### Transition rule

Scene 6 is the pivot. Opens with the handphone video — hand-drawn for two seconds — then cross-fades into systemic as the invented standard is revealed. Scene 10 is pure systemic: full-frame number, no illustration.

---

## Maradona Two-Beat Treatment

### Beat 1 — Scene 6 (the handball)

The clarity test is the handball: PDPC scored a goal with something never in the rules. The original footage was deleted, so no one can check what was on it — except PDPC, using the Complainant's own handphone recording of a CCTV screen. The image prompt uses a football-field editorial illustration: a goalkeeper claims handball, the flag stays down, the ball is in the net. The goalposts are labelled "s.21 PDPA" and the ball reads "clarity test." Not cartoonish — editorial illustration.

### Beat 2 — Scene 10 (can't admit it)

Maradona after the match: "It was a little bit the hand of God, and a little bit the head of Maradona." Not quite admitting. Not quite denying. PDPC's one-line reply sent nine times to nine different legal questions — same energy. They cannot say what really happened. So they say the same thing nine times and declare the matter closed. Image prompt: nine photocopied sheets, same line highlighted on each, a hand stamping the top one in red — "CLOSED." Flat-vector illustration, bureaucratic indifference.

---

## Source Map

Every claim in the narration must trace to a primary source. This table maps each scene's key claim to its verifiable reference.

| Scene | Key claim | Primary source |
|---|---|---|
| 1 | Parliament promised preservation + penalties; PDPC found no breach | Written Answer 19596, 9 Sep 2025 ([sprs.parl.gov.sg](https://sprs.parl.gov.sg/search/#/sprs3topic?reportid=written-answer-19596)); PDPC Decisions MCST 3615 + 4599 |
| 2 | Subarachnoid haemorrhage, total memory loss | NUH discharge records, Apr 2024 (Complainant's possession) |
| 3 | Scotts Tower refused company name, DPO contact, escalation path; Suites@Cairnhill DPO false legal advice ("police-only") + "difficulty understanding" dismissal | PDPC Decision MCST 4599 ([2025 SGPDPC 3](https://www.pdpc.gov.sg/all-commissions-decisions/2025/08/breach-of-the-accountability-obligation-by-mcst-4599)); Summary MCST 3615; White Paper (20 Aug 2025) |
| 4 | Deletion uncertainty — guards "many months", MA "20–30 days", PDPC "17 days" (unverified) | PDPC Decision MCST 4599 timing findings; White Paper correspondence |
| 5 | Complaint filed, months of silence before substantive response | PDPC correspondence (Complainant's possession); site `#process` section |
| 6 | Handphone video used to determine "not personal data"; clarity test (face or plate must be visible) appears nowhere in PDPA | MCST 3615 Summary; PDPA s.2(1) ([sso.agc.gov.sg](https://sso.agc.gov.sg/Act/PDPA2012)) |
| 7 | Two invented reasonings; neither stated refusal ground tested against s.21(3) or Fifth Schedule | Decisions MCST 3615 + 4599; PDPA s.21(3), Fifth Schedule; site `#cases` |
| 8 | Nine questions, identical response ("Guidelines not determinative; PDPA takes precedence"); decisions withheld until PMO/President's Office escalation; matter declared closed | Email correspondence (Complainant's possession); site `#narrative` structural callout |
| 9 | IMDA IAU "no wrongdoing" without addressing material facts | IMDA correspondence (Complainant's possession); site Failure #10 |
| 10 | 384 published enforcement actions, zero s.21 breach findings; only two CCTV-access-refusal complaints are the Complainant's | `enforcement-index.html` (this site); PDPC public register; site `#narrative` 4th structural callout (added 2026-07-02) |
| 11 | Pattern: every decision, every level, same direction — inconsistent with ordinary regulatory error | Synthesised from site `#story` section — the "only explanation" |
| 12 | pdpaaccessrights.sg content and purpose | [pdpaaccessrights.sg](https://pdpaaccessrights.sg) |
| 13 | "Is the Access Obligation being enforced at all?" | Site `#story` parliamentary callout + `#reform` question groups |

### Key source documents (live, on-the-record)

- **Singapore Parliament Written Answer 19596** (9 Sep 2025): Minister Josephine Teo — organisations required to preserve data while requests are processed; criminal penalties for intentional concealment. [sprs.parl.gov.sg](https://sprs.parl.gov.sg/search/#/sprs3topic?reportid=written-answer-19596)
- **PDPC Decision MCST 4599** (2025 SGPDPC 3): Accountability breach finding; verbal refusal on 17 Apr 2024; footage existed until 30 Apr. [pdpc.gov.sg](https://www.pdpc.gov.sg/all-commissions-decisions/2025/08/breach-of-the-accountability-obligation-by-mcst-4599)
- **PDPC Summary MCST 3615** (DP-2405-C2445): Voluntary undertaking; "not personal data" finding via clarity test. [pdpc.gov.sg](https://www.pdpc.gov.sg/undertakings/undertaking-by-mcst-3615)
- **PDPA 2012**: s.2(1) (definition of personal data), s.21(3) and Fifth Schedule (lawful refusal grounds), s.4(6) (BMSMA subordination), s.22A (preservation obligation). [sso.agc.gov.sg](https://sso.agc.gov.sg/Act/PDPA2012)
- **PDPC email re s.22A preservation gap**: "we are aware and presently reviewing this issue, which we will raise to the Ministry for their consideration." (Failure #3 on site)
- **Site enforcement index**: `enforcement-index.html` — 384-case obligation matrix generated from PDPC public register
- **White Paper (20 Aug 2025)**: `PDPC Complain/White Paper - PDPA CCTV Loophole (20 Aug 2025).pdf`

---

## Technical Notes

### File location
- **Spec (this file):** `docs/superpowers/specs/2026-07-04-video-script-design.md`
- **Script (to be written during implementation):** `docs/superpowers/specs/2026-07-04-video-script.md`

### Integration with /yt-intake
- The script file serves as input to the `/yt-intake` skill
- `/yt-intake` drives the `intake` CLI at `E:/Bespoke/Minimax_Hub/intake/`
- Enforces polish-before-approval discipline, audio-anchored timestamps, and resumable frame batches
- Image prompts in each scene block become MiniMax image generation jobs via yt-intake's frame-batch pipeline

### Site references in the video
- The script should visually show the live site: [pdpaaccessrights.sg](https://pdpaaccessrights.sg/)
- Key site sections to highlight visually: `#story`, `#promise`, `#cases`, `#narrative`, `#failures`, `#contradictions`, `enforcement-index.html`
- The site's source-discipline rule (primary-source grounding) applies to the script as well

### Curly-quote audit
- Before finalising the script file, run: `grep -cE "[a-z]'[a-z]"` and `grep -cE '[a-z]"[a-z]'` — both must be 0
- All visible narration text uses curly quotes

---

## Design Decisions Record

| Decision | Rationale |
|---|---|
| 13 scenes, ~10 min | Keeps pacing tight; no scene exceeds 105s; most are 45–75s |
| yt-intake-ready format | User's explicit workflow: script → `/yt-intake` for voice-over + pictures |
| Mixed visual style | Hand-drawn for personal journey (authenticity, vulnerability); clean/systemic for mechanism (authority, precision). The pivot at scene 6 reinforces the narrative turn. |
| Two Maradona beats | User's creative direction. Beat 1 (handball) lands the clarity test as the moment of illegality. Beat 2 (can't admit) lands the pattern of evasion — they can't say what happened. |
| Documentary-first, crescendo | Preserves credibility for the first half (skeptical viewer stays engaged); emotional register rises as the systemic pattern becomes undeniable. Earned, not performed. |
| First-person narration | User's explicit choice. Authenticity for YouTube. Differs from site convention ("the Complainant") because the video is public-facing, not Parliament-facing. |
| "What happened" field per scene | Source-discipline: every narrative claim must be traceable to a primary source. Prevents drift during script writing. |
| pdpaaccessrights.sg as ending | Domain is live (verified Jul 2026). The site is the video's CTA — all evidence is public there. |
