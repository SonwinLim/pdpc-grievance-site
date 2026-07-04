# Video Script — pdpaaccessrights.sg Story Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Write a 13-scene, ~10-minute, yt-intake-ready video script at `docs/superpowers/specs/2026-07-04-video-script.md` — first-person narration by Ray Lim, documentary-first tone with crescendo, mixed visual style (hand-drawn for personal journey, clean/systemic for mechanism).

**Architecture:** Single markdown file with 13 self-contained scene blocks. Each block has a timestamped header, "What happened" (source-anchor), "Narration" (voice-over text), and "Image prompt" (MiniMax generation prompt). No dependencies between scenes. The file serves as direct input to `/yt-intake`.

**Tech Stack:** Markdown. No code. MiniMax image generation via yt-intake frame-batch pipeline.

## Global Constraints

- Narration is spoken-word, not written-prose — short sentences, active voice, no academic connectives
- Every claim must trace to a verifiable primary source (mapped in design spec §Source Map)
- No fabricated quotes — verbatim quotes from sources only; paraphrase with "[paraphrased]" marker if needed
- Curly quotes throughout (no straight ASCII `"` or `'` in any narration or visible text)
- Singapore statutory red `#C41230` as accent colour in clean/systemic image prompts
- Hand-drawn visuals use muted palette: charcoal grey, warm ochre, hospital blue, muted teal
- Figures in hand-drawn visuals are silhouettes or partially rendered — no detailed faces
- File output: `docs/superpowers/specs/2026-07-04-video-script.md`
- Total narration: 2,500–3,500 words across 13 scenes

---

### Task 1: Create script file scaffold

**Files:**
- Create: `docs/superpowers/specs/2026-07-04-video-script.md`

**Interfaces:**
- Produces: Empty script file with YAML frontmatter + scene-placeholder structure

- [ ] **Step 1: Write the file header and scene skeleton**

Create `docs/superpowers/specs/2026-07-04-video-script.md`:

```markdown
---
title: "PDPC Grievance — The Story Behind pdpaaccessrights.sg"
narrator: "Ray Lim, first person"
duration: "~10:35"
scenes: 13
visual_style: "mixed (hand-drawn + clean/systemic)"
tone: "documentary-first, crescendo"
spec: "docs/superpowers/specs/2026-07-04-video-script-design.md"
date: "2026-07-04"
---

# PDPC Grievance — The Story Behind pdpaaccessrights.sg

**Voice:** Ray Lim, first-person narration
**Duration:** ~10 minutes 35 seconds across 13 scenes
**Tone:** Documentary-first, crescendo
**Visual:** Mixed — hand-drawn illustration (personal journey) + clean/systemic infographic (mechanism)

This file is the input to `/yt-intake` for voice-over generation and MiniMax frame-batch image generation.

---

<!-- Scene blocks follow. Each scene is a self-contained unit: -->
<!-- header with timestamp + duration + visual-style -->
<!-- What happened (source-anchor) -->
<!-- Narration (voice-over text) -->
<!-- Image prompt (MiniMax generation) -->

---
## Scene 1 — The Hook [0:00–0:30] · 30s · clean/systemic
---

**What happened:**
[TODO — see Task 2]

**Narration:**
[TODO — see Task 2]

**Image prompt:**
[TODO — see Task 2]

---
## Scene 2 — The Accident [0:30–1:30] · 60s · hand-drawn
---

**What happened:**
[TODO — see Task 2]

**Narration:**
[TODO — see Task 2]

**Image prompt:**
[TODO — see Task 2]

---
## Scene 3 — The Denials [1:30–3:15] · 105s · hand-drawn
---

**What happened:**
[TODO — see Task 3]

**Narration:**
[TODO — see Task 3]

**Image prompt:**
[TODO — see Task 3]

---
## Scene 4 — The Deletion Window [3:15–4:00] · 45s · hand-drawn
---

**What happened:**
[TODO — see Task 3]

**Narration:**
[TODO — see Task 3]

**Image prompt:**
[TODO — see Task 3]

---
## Scene 5 — Filing With PDPC [4:00–4:45] · 45s · hand-drawn
---

**What happened:**
[TODO — see Task 4]

**Narration:**
[TODO — see Task 4]

**Image prompt:**
[TODO — see Task 4]

---
## Scene 6 — The Clarity Test [4:45–5:45] · 60s · mixed (hand-drawn → systemic)
---

**What happened:**
[TODO — see Task 4]

**Narration:**
[TODO — see Task 4]

**Image prompt:**
[TODO — see Task 4]

---
## Scene 7 — Two Cases, Two Invented Reasonings [5:45–7:00] · 75s · clean/systemic
---

**What happened:**
[TODO — see Task 5]

**Narration:**
[TODO — see Task 5]

**Image prompt:**
[TODO — see Task 5]

---
## Scene 8 — Nine Questions, One Response [7:00–8:00] · 60s · clean/systemic
---

**What happened:**
[TODO — see Task 5]

**Narration:**
[TODO — see Task 5]

**Image prompt:**
[TODO — see Task 5]

---
## Scene 9 — IMDA — The Oversight That Didn't Oversee [8:00–8:45] · 45s · clean/systemic
---

**What happened:**
[TODO — see Task 6]

**Narration:**
[TODO — see Task 6]

**Image prompt:**
[TODO — see Task 6]

---
## Scene 10 — The 384 Cases (Maradona Beat 2) [8:45–9:45] · 60s · clean/systemic
---

**What happened:**
[TODO — see Task 7]

**Narration:**
[TODO — see Task 7]

**Image prompt:**
[TODO — see Task 7]

---
## Scene 11 — The Only Explanation [9:45–10:15] · 30s · clean/systemic
---

**What happened:**
[TODO — see Task 7]

**Narration:**
[TODO — see Task 7]

**Image prompt:**
[TODO — see Task 7]

---
## Scene 12 — pdpaaccessrights.sg [10:15–10:35] · 20s · mixed
---

**What happened:**
[TODO — see Task 8]

**Narration:**
[TODO — see Task 8]

**Image prompt:**
[TODO — see Task 8]

---
## Scene 13 — Call to Action [10:35–10:45] · 10s · clean/systemic
---

**What happened:**
[TODO — see Task 8]

**Narration:**
[TODO — see Task 8]

**Image prompt:**
[TODO — see Task 8]
```

- [ ] **Step 2: Commit scaffold**

```bash
git add docs/superpowers/specs/2026-07-04-video-script.md
git commit -m "Add video script scaffold with 13 scene placeholders"
```

---

### Task 2: Write scenes 1–2 (Hook + The Accident)

**Files:**
- Modify: `docs/superpowers/specs/2026-07-04-video-script.md` — replace [TODO] blocks for scenes 1–2

**Interfaces:**
- Consumes: Scene 1 source map (Written Answer 19596; PDPC Decisions MCST 3615 + 4599); Scene 2 source map (NUH discharge records, subarachnoid haemorrhage)
- Produces: Completed narration and image prompts for scenes 1–2

- [ ] **Step 1: Write Scene 1 — The Hook (Parliament said X. PDPC did Y.)**

Replace the Scene 1 [TODO] blocks with:

```
**What happened:**
On 9 September 2025, Minister Josephine Teo told Parliament that the PDPA requires organisations to preserve personal data while access requests are processed, with criminal penalties for intentional destruction. In the Complainant's case — the only two CCTV-access-refusal complaints across 384 published PDPC enforcement actions — the footage was deleted. PDPC found no preservation breach and no Access Obligation breach. Both cannot be true. One of them must be wrong.

**Narration:**
In September 2025, a member of parliament asked the minister responsible: when someone requests their own CCTV footage under the Personal Data Protection Act, is the organisation required to preserve that footage while the request is being processed?

The minister's answer was clear. Yes. Organisations must have appropriate measures to preserve the requested data. There are criminal penalties for intentional destruction to avoid access requests.

Those are the words of Minister Josephine Teo. On 9 September 2025. In the Parliament of Singapore.

Here is what happened when I made that request.

**Image prompt:**
Clean/systemic editorial infographic. Split-screen composition. Left panel: a formal parliamentary record page, the words "preserve the requested personal data" highlighted in Singapore statutory red (#C41230). Right panel: a PDPC decision document, the words "no breach" stamped in institutional grey. Between them, a question mark rendered in black. The background is white. No illustrations — pure typographic layout. The viewer should feel the collision of two official documents that cannot both be true.
```

- [ ] **Step 2: Write Scene 2 — The Accident**

Replace the Scene 2 [TODO] blocks with:

```
**What happened:**
On 13 April 2024, at approximately 5:06 AM, the Complainant was injured when a taxi cut into his lane on Cairnhill Road, Singapore. The impact caused a subarachnoid haemorrhage — bleeding around the brain. The Complainant lost all memory of the accident and the period surrounding it. The taxi driver was subsequently charged under the Road Traffic Act for careless driving. The two condominiums flanking the road — The Scotts Tower and Suites@Cairnhill — both had CCTV cameras covering the road. Security staff at both condos identified the relevant footage within minutes of the accident.

**Narration:**
13 April 2024. 5:06 in the morning. I was riding my motorcycle on Cairnhill Road when a taxi cut into my lane.

I woke up in hospital. The diagnosis was a subarachnoid haemorrhage. Bleeding around the brain.

I had no memory of what happened to me. Not the impact. Not the minutes before. Not the ambulance. Nothing.

What I did know — from the police report — was that two condominiums flanked the road where the accident happened. Both had CCTV cameras pointing at the street. Security staff at both buildings had already found the footage within minutes. The taxi cutting into my lane was on video. It existed. It was findable.

That footage was the only record of an event I have no memory of. I needed it for two reasons. One: to understand what happened to me. Two: to support an insurance claim against the driver.

Both seemed straightforward. Both were not.

**Image prompt:**
Hand-drawn ink-and-wash illustration. A hospital bed seen from slightly above and to the side. A figure lies still, head bandaged, eyes closed. The room is dim — muted hospital blue and charcoal grey. Through a window in the background, blurred car headlights streak across a dark road. One warm accent: a small digital clock on the bedside table reads 05:06 in soft ochre. The figure is small in the frame — the bed occupies the centre, but the figure feels diminished in it. The overall mood is not dramatic, but quiet. A question mark hovers faintly, almost imperceptibly, in the window glass.
```

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-07-04-video-script.md
git commit -m "Write scenes 1-2: Hook (Parliament vs PDPC) + The Accident"
```

---

### Task 3: Write scenes 3–4 (The Denials + The Deletion Window)

**Files:**
- Modify: `docs/superpowers/specs/2026-07-04-video-script.md` — replace [TODO] blocks for scenes 3–4

**Interfaces:**
- Consumes: Scene 3 source map (PDPC Decision MCST 4599; Summary MCST 3615; White Paper 20 Aug 2025); Scene 4 source map (PDPC Decision MCST 4599 timing findings; White Paper correspondence)
- Produces: Completed narration and image prompts for scenes 3–4

- [ ] **Step 1: Write Scene 3 — The Denials (both condos, both refusals)**

Replace the Scene 3 [TODO] blocks with:

```
**What happened:**
The Scotts Tower (MCST 4599) refused access on 17 April 2024, citing "privacy" as a blanket reason. When challenged, they claimed no footage existed — refuted by PDPC's own subsequent finding that footage existed until 30 April. The managing agent refused to provide the company name, the DPO contact, or any escalation path. The Complainant had to independently identify the managing agent and track down the DPO himself. Suites@Cairnhill (MCST 3615) refused on 21 May 2024 — its DPO, Mohamed Nasir Mustaffa of Property Facility Services Pte Ltd, stated in writing: "Only by police direct/order the MCST to disclose the footage that MCST is obliged to do so." When the Complainant cited the correct PDPA Advisory Guidelines in reply, the DPO responded: "It seems to me you are having difficulty understanding our position" and refused further communication. Neither condominium cited a lawful refusal ground from s.21(3) or the Fifth Schedule of the PDPA.

**Narration:**
Four days after the accident, I walked into the management office of The Scotts Tower. I explained what happened. I asked for the CCTV footage of the road.

They said no. Privacy reasons.

I asked who the data protection officer was. They wouldn't tell me. I asked what company managed the building. They wouldn't tell me that either. I asked who I could escalate to. No answer.

I left the building knowing less than when I walked in. I had to figure out the company name on my own. I had to hunt down the DPO myself. Every door I tried, someone had already locked it.

The other condominium — Suites@Cairnhill — put their refusal in writing. Their DPO emailed me on 21 May 2024: "Only by police direct or order the MCST to disclose the footage that MCST is obliged to do so."

That is not what the law says. The PDPA gives every individual the right to request their own personal data. Police involvement is not required. I wrote back, citing the correct advisory guidelines.

The DPO's reply: "It seems to me you are having difficulty understanding our position." And he refused to communicate with me further.

Neither condominium cited a single ground from the law. The PDPA lists the only legal reasons a request can be refused — section 21, subsection 3, and the Fifth Schedule. Privacy as a blanket reason is not on that list. Police-only access is not on that list.

Nobody checked.

**Image prompt:**
Hand-drawn ink-and-wash illustration, two-panel composition. Left panel: a figure stands at a tall reception counter in a lobby. The receptionist behind the counter is a silhouette with arms crossed. A security camera on the ceiling glows with a small red dot — the only warm accent in the frame. The figure's posture is slightly forward, one hand resting on the counter edge, trying to explain. Right panel: the same figure sits at a small desk, reading from a phone. On the wall, an email or letter with the text "Only by police direct/order" and a reply "difficulty understanding" is pinned — partially visible, the words are small. The figure's shoulders are hunched. The lighting is cool fluorescent in both frames. Muted charcoal, blue, and teal palette. No faces — postures tell the story.
```

- [ ] **Step 2: Write Scene 4 — The Deletion Window**

Replace the Scene 4 [TODO] blocks with:

```
**What happened:**
At the time of the access requests, the Complainant had no way to know how long the footage would be retained. The security guards at The Scotts Tower initially said footage was kept for "many months." A new managing agent later said "20 to 30 days." PDPC later determined that the footage was overwritten on 30 April 2024 — 17 days after the accident, and months before any substantive investigation opened. PDPC accepted this 17-day figure without independent verification. The Complainant was operating blind: the footage existed, and nobody would tell him how long he had.

**Narration:**
While I was fighting to find out who managed the building, the clock was running.

Nobody told me how long the footage would be kept. The security guards said many months. A new management team later claimed 20 to 30 days. PDPC eventually said 17 days — and accepted that figure without verifying it.

At the time, I knew none of this. All I knew: the footage existed, two condominiums had identified it within minutes of the accident, and nobody would tell me how long I had to get it.

Seventeen days. That was the window. I was still trying to find out the company name on day four.

**Image prompt:**
Hand-drawn ink-and-wash illustration. A calendar on a wall, April 2024, with the 13th circled faintly in red. A clock on the same wall, hands blurred in motion. Below, a CCTV camera is visible but out of focus — it is recording, but the footage is draining away, represented by a faint, dissipating trail of frames dissolving like smoke. The figure is small, seated at a desk in the foreground, hands resting on a closed laptop, staring at the calendar. The overall composition is quiet, tense — not dramatic. Charcoal grey with touches of fading red and muted teal. The viewer should feel the asymmetry: the system knows the clock is running; the figure does not.
```

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-07-04-video-script.md
git commit -m "Write scenes 3-4: The Denials + The Deletion Window"
```

---

### Task 4: Write scenes 5–6 (Filing With PDPC + The Clarity Test / Maradona Beat 1)

**Files:**
- Modify: `docs/superpowers/specs/2026-07-04-video-script.md` — replace [TODO] blocks for scenes 5–6

**Interfaces:**
- Consumes: Scene 5 source map (PDPC correspondence; site #process); Scene 6 source map (MCST 3615 Summary; PDPA s.2(1))
- Produces: Completed narration and image prompts for scenes 5–6

- [ ] **Step 1: Write Scene 5 — Filing With PDPC**

Replace the Scene 5 [TODO] blocks with:

```
**What happened:**
The Complainant filed a formal complaint with PDPC detailing both refusals — the verbal denial from Scotts Tower (no company name, no DPO, no escalation), and the written "police-only" refusal from Suites@Cairnhill. Months passed. PDPC did not open a substantive investigation. It did not issue a preservation notice. The footage was deleted before PDPC took any action.

**Narration:**
So I did what the law says to do. I filed a formal complaint with the Personal Data Protection Commission. I detailed both refusals — the verbal denial with no company name and no DPO contact from Scotts Tower, and the written "police-only" refusal from Suites@Cairnhill.

And then.

Nothing.

Months passed.

No investigation opened. No update. No preservation notice sent. The footage had been deleted in April. Nobody at PDPC had acted to preserve it. Months of silence. And then, eventually, a response — but not the one the law seemed to promise.

**Image prompt:**
Hand-drawn ink-and-wash illustration. A desk piled with papers — the complaint filing, printed emails, advisory guidelines. A figure sits at the desk, one hand resting on the papers, the other hand open and empty, palm up. The window behind shows a calendar with months flipped forward — May, June, July — and a phone on the desk that shows no notifications. The lighting is flat, grey, late-afternoon. The figure is not angry — the posture is one of waiting. The papers are the most detailed element in the frame. The clock on the wall has hands that don't seem to be moving. Muted palette: charcoal, ochre, hospital blue.
```

- [ ] **Step 2: Write Scene 6 — The Clarity Test (Maradona Beat 1)**

Replace the Scene 6 [TODO] blocks with:

```
**What happened:**
For MCST 3615 (Suites@Cairnhill), PDPC determined that the CCTV footage did not contain "personal data." To reach this finding, PDPC reviewed footage the Complainant himself had captured — a handphone video of the CCTV screen taken at the management office. The original footage had been deleted, so PDPC's determination was based entirely on this secondary recording. The standard PDPC applied — that a face or licence plate must be visible for footage to qualify as personal data — appears nowhere in the PDPA. The statute defines personal data by identifiability ("data about an individual who can be identified from that data"), not by image clarity. This is Maradona Beat 1: a goal scored with something not in the rules.

**Narration:**
Eventually, PDPC issued its findings. Two cases. Two sets of reasoning.

For Suites@Cairnhill, they said the CCTV footage did not contain "personal data."

Here is how they made that determination. They used my own evidence — a handphone video I had taken of the CCTV screen at the management office, to document what the footage showed. The original footage was long gone by then. Deleted. Overwritten.

So PDPC looked at a phone recording of a CCTV screen — a copy of a copy — and said: not clear enough. Not personal data.

They invented a standard that appears nowhere in the PDPA. Face or licence plate must be visible. The statute says nothing about image quality. It defines personal data as data about an individual who can be identified from that data or from that data and other information.

Identifiability. Not clarity.

This is the moment to understand. PDPC took my own evidence. Used it against me. And the test they applied — the clarity test — does not exist in the legislation. It was invented. By the regulator. To dismiss my case.

In football, there is a famous goal scored by Diego Maradona — his hand made contact with the ball. The referee missed it. The goal stood. Afterwards, Maradona called it "the hand of God."

PDPC's clarity test is the regulatory equivalent. They scored a goal with something never in the rules. The footage was gone, so nobody could check what was really on it. They declared victory. And moved on.

**Image prompt:**
Opens with 2 seconds of hand-drawn style — a hand holding a phone, angled up at a CCTV monitor. The monitor shows a grainy night scene. The phone screen glows. Then cross-fades to clean/systemic editorial illustration: a football field seen from above. One figure — the goalkeeper — has arms raised, claiming a handball. The referee's flag stays down — the linesman is a silhouette, motionless. In the distance, the ball is already in the net. The goalposts are subtly labelled "s.21 PDPA" — not cartoonish, but editorial. The ball carries the text "clarity test." The composition is spare — black, white, the goal net rendered in thin grey lines, the ball in Singapore statutory red (#C41230). The feeling is not anger, but a quiet, disbelieving stillness — the moment after a goal that shouldn't have counted, when the players are looking at each other and the crowd hasn't yet reacted.
```

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-07-04-video-script.md
git commit -m "Write scenes 5-6: Filing With PDPC + The Clarity Test (Maradona Beat 1)"
```

---

### Task 5: Write scenes 7–8 (Two Cases + Nine Questions)

**Files:**
- Modify: `docs/superpowers/specs/2026-07-04-video-script.md` — replace [TODO] blocks for scenes 7–8

**Interfaces:**
- Consumes: Scene 7 source map (Decisions MCST 3615 + 4599; PDPA s.21(3), Fifth Schedule; site #cases); Scene 8 source map (email correspondence; site #narrative structural callout)
- Produces: Completed narration and image prompts for scenes 7–8

- [ ] **Step 1: Write Scene 7 — Two Cases, Two Invented Reasonings**

Replace the Scene 7 [TODO] blocks with:

```
**What happened:**
PDPC applied different reasoning to each case, and in both cases, it was not the reasoning the condominium had given. For MCST 3615, PDPC found "no personal data" — but the MCST had never claimed this. The MCST's stated ground was "police-only access." The regulator substituted its own justification. For MCST 4599, PDPC found "footage overwritten before formal refusal" — but this ignored the verbal refusal on 17 April 2024 and the false "no footage" claim made when challenged, both of which preceded the 30 April overwrite. In neither case did PDPC test the condominium's actual stated refusal ground against s.21(3) or the Fifth Schedule — the only provisions that authorise a lawful refusal of an access request. PDPC invented reasoning for the respondents rather than testing what they actually said against the statute.

**Narration:**
Let me show you what PDPC did, side by side.

First condominium — Suites@Cairnhill. The DPO said: "Only by police order." PDPC said: "The footage contains no personal data." The condominium never said that. PDPC invented that reason for them.

Second condominium — The Scotts Tower. They verbally refused on April 17th. When challenged, they claimed no footage existed. That was false — PDPC's own later finding confirmed the footage was there until April 30th. But PDPC's conclusion: "footage overwritten before formal refusal." They ignored the verbal refusal. They ignored the false statement. They invented a timeline that conveniently made the deletion before any refusal.

In both cases, PDPC substituted its own reasoning for what the condominiums actually said. And in neither case did they test the actual stated grounds against the law. Section 21, subsection 3, together with the Fifth Schedule — these are the only provisions that authorise an organisation to lawfully refuse an access request.

"Privacy" is not listed. "Police-only" is not listed. PDPC never even checked.

**Image prompt:**
Clean/systemic split-screen editorial layout. Two columns, labelled "MCST 3615" and "MCST 4599." Each column has two rows: top row shows the condominium's stated refusal ground in black text (left: "Police-only access"; right: "Privacy / No footage"). Bottom row shows PDPC's substituted reasoning in grey, with a strike-through line connecting the two (left: "No personal data"; right: "Footage overwritten before formal refusal"). Between the two columns, the Fifth Schedule of the PDPA is rendered as a partial document — a checklist with all items unchecked. Black, white, Singapore statutory red (#C41230) for the unchecked boxes. Flat-vector, no illustration — pure typographic layout. The viewer should understand at a glance: the stated grounds were never tested against the statute.
```

- [ ] **Step 2: Write Scene 8 — Nine Questions, One Response**

Replace the Scene 8 [TODO] blocks with:

```
**What happened:**
The Complainant sent PDPC nine legal questions spanning six sections of the PDPA. Every question received an identical one-line response: "The Guidelines are not determinative; the PDPA takes precedence." PDPC did not name which guideline, which clause of the PDPA, or how the two conflict. The decisions themselves were withheld from the Complainant until he escalated to the Prime Minister's Office, multiple government ministers, and the President's Office. Only then were the decisions released. PDPC then declared the matter closed.

**Narration:**
I wrote to PDPC with nine questions. Specific, legal questions across six sections of the PDPA. About the clarity test — which section of the Act authorises it? About the Fifth Schedule — why were the stated refusal grounds never tested against it? About the deletion — why was no preservation notice issued?

The response to every question was the same. One line. Copied and pasted — nine times.

"The Guidelines are not determinative. The PDPA takes precedence."

They did not name which guideline they were dismissing. They did not name which clause of the PDPA overrides it. They did not explain how the two conflict.

Nine legal questions. Six sections of the PDPA. One identical non-answer. Nine times.

And here is the part I still find difficult to believe. The decisions themselves — PDPC's actual written findings — were withheld from me. I had filed the complaint. I was the complainant. And I was not given the decisions. They were released only after I escalated to the Prime Minister's Office, to government ministers, to the President's Office. Only then did PDPC release them.

Then they declared the matter closed.

**Image prompt:**
Clean/systemic editorial layout. A single sheet of paper, photocopied nine times, each sheet with the same line highlighted in Singapore statutory red (#C41230): "The Guidelines are not determinative; the PDPA takes precedence." The nine sheets are fanned out on a surface like a dealt hand of cards. A red stamp reads "CLOSED" — the stamp is slightly misaligned, the ink slightly uneven. In the corner of the composition, partially visible, a stack of unopened letters with faint postmarks: "PMO," "President's Office," "Ministry." Flat-vector illustration, black and white with one accent colour. No human figures. The documents themselves are the subject. Bureaucratic, indifferent, final.
```

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-07-04-video-script.md
git commit -m "Write scenes 7-8: Two Cases Two Reasonings + Nine Questions One Response"
```

---

### Task 6: Write scene 9 (IMDA — The Oversight That Didn't Oversee)

**Files:**
- Modify: `docs/superpowers/specs/2026-07-04-video-script.md` — replace [TODO] blocks for scene 9

**Interfaces:**
- Consumes: Scene 9 source map (IMDA correspondence; site Failure #10)
- Produces: Completed narration and image prompt for scene 9

- [ ] **Step 1: Write Scene 9 — IMDA**

Replace the Scene 9 [TODO] blocks with:

```
**What happened:**
The Info-communications Media Development Authority (IMDA) is the parent body that oversees PDPC. The Complainant escalated the grievance to IMDA's Internal Audit Unit (IAU). The IAU found "no wrongdoing" without addressing the material facts: the invented clarity test, the untested refusal grounds, the identical non-responses to nine legal questions, the withheld decisions. The oversight body replicated the pattern of the body it oversees — delay, non-engagement, dismissal without engagement with the evidence.

**Narration:**
So I went to the oversight body. IMDA — the Info-communications Media Development Authority. PDPC's parent organisation. If the regulator won't engage with the merits, surely the body that oversees the regulator will.

IMDA's Internal Audit Unit reviewed my complaint. I sent them everything. The clarity test — where is it in the statute? The Fifth Schedule — why weren't the condominiums' actual refusal grounds tested against it? The nine identical non-responses. The withheld decisions.

Their finding: "No wrongdoing."

They did not address the clarity test. They did not address the Fifth Schedule. They did not address the nine identical responses. They did not address the withheld decisions.

The oversight body had replicated the pattern of the body it was supposed to oversee. Delay. Non-engagement. Dismissal without engagement with the evidence.

**Image prompt:**
Clean/systemic editorial illustration. Two identical building silhouettes, side by side, one labelled "PDPC" and the other "IMDA IAU." Between them, a document travels from the first building to the second — it has a red "NO BREACH" stamp on it. At the second building, a hand simply adds a second stamp: "NO WRONGDOING." The document has not been read — it is still sealed, the fold lines visible. The two stamps partially overlap. Flat-vector, black and white with Singapore statutory red (#C41230) accents. The buildings are generic institutional shapes — not specific to Singapore. The point is the mirroring: the oversight body stamped what it was given, without opening the envelope.
```

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/specs/2026-07-04-video-script.md
git commit -m "Write scene 9: IMDA — The Oversight That Didn't Oversee"
```

---

### Task 7: Write scenes 10–11 (The 384 Cases / Maradona Beat 2 + The Only Explanation)

**Files:**
- Modify: `docs/superpowers/specs/2026-07-04-video-script.md` — replace [TODO] blocks for scenes 10–11

**Interfaces:**
- Consumes: Scene 10 source map (enforcement-index.html; PDPC public register; site #narrative 4th structural callout); Scene 11 source map (site #story section synthesis)
- Produces: Completed narration and image prompts for scenes 10–11

- [ ] **Step 1: Write Scene 10 — The 384 Cases (Maradona Beat 2)**

Replace the Scene 10 [TODO] blocks with:

```
**What happened:**
Compiled in June 2026 from PDPC's public enforcement register: across 384 published enforcement actions, the Access Obligation (s.21 of the PDPA) has produced zero breach findings. Not one. Across that entire register, only two cases involve a complainant demanding access to their own CCTV data and being refused — and both are the Complainant's. The dominant pattern of enforcement is data protection (s.24) and consent (s.13) — obligations that run against organisations mishandling data they hold. The right of a citizen to retrieve their own data from an organisation is the least enforced provision in the entire register. The clarity test, applied consistently, explains this: if face or licence plate must be visible for CCTV to qualify as personal data, most real-world CCTV footage falls outside access protection. This is Maradona Beat 2: after the goal, Maradona was asked about it. He said — "It was a little bit the hand of God, and a little bit the head of Maradona." Not quite admitting. Not quite denying. PDPC's one-line reply sent nine times — same energy. They cannot say what really happened, so they say the same thing nine times and close the file.

**Narration:**
By this point, I stopped asking whether my case was handled wrongly. I started asking a different question. How many cases like mine has PDPC ever found a breach on?

I went through PDPC's entire published enforcement register. Every decision. Every finding. Three hundred and eighty-four cases, compiled as of June 2026.

The Access Obligation — section 21 of the PDPA, the right of a citizen to access their own personal data — has produced zero breach findings. Zero. Across three hundred and eighty-four published enforcement actions. Not one.

The dominant pattern of PDPC enforcement is data protection and consent — organisations mishandling data they hold. The right of a citizen to retrieve their own data from an organisation? That is the least enforced provision in the entire register.

Across those three hundred and eighty-four cases, only two involve a complainant demanding access to their own CCTV data and being refused. Both are mine. Both from the same accident on Cairnhill Road. Both dismissed without a finding that the Access Obligation was breached.

The clarity test explains this. If face or licence plate must be visible for CCTV footage to qualify as personal data — and that standard exists nowhere in the statute — then any organisation can deny an access request by asserting the footage is too unclear. And the Complainant has no tools to challenge that assertion.

After the 1986 World Cup quarter-final, Maradona was asked about his goal. He said: "It was a little bit the hand of God, and a little bit the head of Maradona."

Not quite admitting. Not quite denying.

PDPC's one-line reply — "The Guidelines are not determinative; the PDPA takes precedence" — sent nine times to nine different legal questions. Same energy. They cannot say what really happened. So they say the same thing nine times, and declare the file closed.

**Image prompt:**
Clean/systemic editorial composition. Centre frame: a giant number — "0" — rendered in bold black typography, filling most of the frame. Below it, in smaller text: "Access Obligation breach findings across 384 published PDPC enforcement actions." To the side, a thin document stack icon labelled "384 cases." At the bottom, two tiny document icons, isolated, labelled "Complainant's 2 cases" — the only CCTV-access-refusal complaints in the entire register. The composition is deliberately stark — black text on white, with the "0" in Singapore statutory red (#C41230). No illustrations. No metaphors. The number is the argument. Below the 0, in fine print: "Source: PDPC public enforcement register, compiled June 2026." This is an infographic, not a poster.
```

- [ ] **Step 2: Write Scene 11 — The Only Explanation**

Replace the Scene 11 [TODO] blocks with:

```
**What happened:**
The documented pattern is not what ordinary regulatory failure looks like. Ordinary failure is uneven — mistakes in different directions, inconsistent outcomes, different responses to different challenges. What is documented here is coherent: every decision at every level, in the same direction. PDPC substituted invented reasoning for the MCSTs' actual stated grounds. IMDA replicated the same pattern of non-engagement. Nine legal questions received one identical non-answer. Zero breach findings across 384 cases. This is inconsistent with ordinary regulatory error. It is consistent with a de facto policy of non-enforcement of the Access Obligation for CCTV footage. The clarity test is the legal mechanism. The zero-breach history is the outcome. The non-engagement is what follows when a regulator cannot defend its position on the merits.

**Narration:**
Here is what I have learned, going through every document, every decision, every response.

Ordinary regulatory failure is uneven. It makes mistakes in different directions. It produces inconsistent outcomes. It responds differently to different challenges.

What is documented here — across two PDPC cases, an IMDA review, nine legal questions, and three hundred and eighty-four enforcement actions — is not uneven.

Every decision. At every level. In the same direction.

PDPC invented reasoning for the condominiums instead of testing what they actually said. IMDA stamped "no wrongdoing" without opening the envelope. Nine legal questions got one identical line. Zero breach findings across three hundred and eighty-four cases.

This is the shape of a policy. Not necessarily an explicit one. Nobody needs to have written it down. But the evidence is consistent with a de facto policy of non-enforcement of the Access Obligation for CCTV footage — and inconsistent with ordinary regulatory error.

The clarity test is the legal mechanism. The zero-breach history is the outcome. The non-engagement is what follows when a regulator cannot defend its position on the merits.

**Image prompt:**
Clean/systemic editorial layout. A single horizontal line representing time, broken into four segments labelled: "MCST refusals" → "PDPC invented reasoning" → "IMDA no wrongdoing" → "384 cases, zero breaches." A red arrow arcs above the line, sweeping from left to right, labelled: "Every decision, at every level, in the same direction." Below the line, in smaller text: "Inconsistent with ordinary regulatory error. Consistent with de facto non-enforcement." Black, white, Singapore statutory red (#C41230) for the arrow. Flat-vector, no illustration. This is a conclusion diagram — it should read like the final slide of a legal submission.
```

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-07-04-video-script.md
git commit -m "Write scenes 10-11: 384 Cases (Maradona Beat 2) + The Only Explanation"
```

---

### Task 8: Write scenes 12–13 (pdpaaccessrights.sg + Call to Action)

**Files:**
- Modify: `docs/superpowers/specs/2026-07-04-video-script.md` — replace [TODO] blocks for scenes 12–13

**Interfaces:**
- Consumes: Scene 12 source map (pdpaaccessrights.sg live site); Scene 13 source map (site #story parliamentary callout + #reform question groups)
- Produces: Completed narration and image prompts for scenes 12–13

- [ ] **Step 1: Write Scene 12 — pdpaaccessrights.sg**

Replace the Scene 12 [TODO] blocks with:

```
**What happened:**
The Complainant built pdpaaccessrights.sg — a public site presenting every document, every decision, every response. The site includes: the full story in five acts; the parliamentary Written Answer 19596 juxtaposed against what happened; the two case cards side by side; PDPC's narrative versus the record; the 10 contradiction cards; the 12 documented failures; the 19-month timeline; the full enforcement register analysis; and all source documents. All evidence is public. Nothing on the site is not sourced from a PDPC decision, the PDPA statute, parliamentary record, or correspondence in the Complainant's possession.

**Narration:**
I built a site.

pdpaaccessrights.sg.

Every document is there. Both PDPC decisions — the one that found "no personal data" using my own handphone video, and the one that reframed a deleted-footage case as an accountability breach. The parliamentary answer from Minister Teo promising preservation and penalties — next to what happened in my case. The nine questions and the nine identical replies. The enforcement register analysis — three hundred and eighty-four cases, zero access obligation breach findings. The timeline. The contradictions. The documented failures.

Everything on that site comes from a PDPC decision, the PDPA statute, a parliamentary record, or correspondence in my possession. Nothing is asserted that is not sourced. Every claim has a footnote. Every source is primary.

The evidence is public. You can check it yourself.

**Image prompt:**
Mixed style. A laptop screen showing pdpaaccessrights.sg — the site's #story section visible, with the 5-act structure headings. The screen glows softly. The hands in front of the keyboard are rendered in hand-drawn style — ink lines, suggestive, unfinished. The screen content is clean/systemic — sharp, legible, the site's actual visual design. The contrast between the human figure (hand-drawn, warm charcoal and ochre) and the machine output (clean, sharp, institutional black and white) is intentional. The site's URL is visible in the browser bar: pdpaaccessrights.sg. On the wall behind, faintly, pinned papers and notes — the work that went into building it. The overall mood is quiet resolution — not triumph, but completion. The evidence is public now.
```

- [ ] **Step 2: Write Scene 13 — Call to Action**

Replace the Scene 13 [TODO] blocks with:

```
**What happened:**
The site closes its #story section with a parliamentary callout: if the Access Obligation has produced zero breach findings across over a decade of PDPC enforcement, is the obligation being enforced at all? And if not, what is the mechanism by which it is being rendered unenforceable, and by whom? The site's #reform section presents these questions, along with four legislative asks, for Parliament to examine. The video ends on this question — not as a demand, but as an invitation to check the evidence.

**Narration:**
I am not a lawyer. I am not an MP. I am a citizen who asked for footage of an accident that erased his memory, and found that the right the law promised me did not exist in practice.

The Access Obligation has produced zero breach findings across over a decade of PDPC enforcement. Zero. Across three hundred and eighty-four published cases.

If a statutory right has never been enforced — not once — is it being enforced at all?

And if not — by what mechanism, and by whom, is it being rendered unenforceable?

All the evidence is at pdpaaccessrights.sg.

Check it yourself.

**Image prompt:**
Clean/systemic. A single line of text, centred on a black background, in white: "If the Access Obligation has produced zero breach findings across over a decade of PDPC enforcement, is the obligation being enforced at all?" Below it, in a smaller size, in Singapore statutory red (#C41230): "pdpaaccessrights.sg." Below that, smallest: "All evidence is public. Check it yourself." No illustrations. No imagery. The viewer sits with the question. Fade to black over the final 3 seconds.
```

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-07-04-video-script.md
git commit -m "Write scenes 12-13: pdpaaccessrights.sg + Call to Action"
```

---

### Task 9: Final review — source verification, curly-quote audit, duration check

**Files:**
- Modify: `docs/superpowers/specs/2026-07-04-video-script.md` — fix any issues found

**Interfaces:**
- Consumes: Completed script file (all 13 scenes)
- Produces: Verified, polished script file ready for /yt-intake

- [ ] **Step 1: Curly-quote audit**

```bash
grep -cE "[a-z]'[a-z]" docs/superpowers/specs/2026-07-04-video-script.md
# Expected: 0 — any positive number means straight apostrophes found
```

```bash
grep -cE '[a-z]"[a-z]' docs/superpowers/specs/2026-07-04-video-script.md
# Expected: 0 — any positive number means straight quotes found
```

If any straight quotes or apostrophes found: fix them inline (replace `'` with `‘`/`’`, replace `"` with `“`/`”` as appropriate).

- [ ] **Step 2: Remove all [TODO] markers**

```bash
grep -c "TODO" docs/superpowers/specs/2026-07-04-video-script.md
# Expected: 0 — any positive number means a scene wasn't completed
```

If any TODOs remain: identify which scene and complete it (re-run the relevant task).

- [ ] **Step 3: Duration sum check**

```bash
# Sum all scene durations (listed in headers as "· NNs ·")
grep -oP '\d+s' docs/superpowers/specs/2026-07-04-video-script.md | sed 's/s//' | paste -sd+ | bc
# Expected: ~635 (10 min 35 sec). Acceptable range: 590–680.
```

If outside acceptable range: adjust scene durations in headers (not narration text) to match ~10:35 target.

- [ ] **Step 4: Source-map cross-check**

For each scene, verify one key claim against the source map:
- Scene 1: Minister Teo verbatim quote matches Written Answer 19596
- Scene 3: DPO quote "Only by police direct/order" matches MCST 3615 Summary
- Scene 6: "face or licence plate must be visible" standard — verify it is not in PDPA s.2(1)
- Scene 8: "Guidelines are not determinative" verbatim quote matches email correspondence
- Scene 10: "384 cases" count matches enforcement-index.html
- Scene 12: pdpaaccessrights.sg resolves and #story section is reachable

Document any corrections needed and apply them.

- [ ] **Step 5: Word count check**

```bash
# Count words in all Narration blocks
grep -A100 '^\*\*Narration:\*\*' docs/superpowers/specs/2026-07-04-video-script.md | wc -w
# Expected: 2500–3500 words of narration
```

If outside range: trim or expand narration in the most flexible scenes (2, 5, 9, 11 are the shortest — easiest to adjust).

- [ ] **Step 6: Final commit**

```bash
git add docs/superpowers/specs/2026-07-04-video-script.md
git commit -m "Final review: source verification, curly-quote audit, duration check passed"
```

---

## Plan Self-Review

- [x] **Spec coverage:** All 13 scenes from the design spec are covered (Tasks 2–8). Visual style rules applied in every image prompt. Maradona two-beat treatment implemented in scenes 6 and 10. Source map cross-check built into Task 9. Curly-quote audit built into Task 9.
- [x] **Placeholder scan:** No TBD, TODO, or incomplete sections in plan body. Task 1 intentionally uses [TODO] markers as scaffold placeholders — these are resolved by Tasks 2–8 and verified-removed by Task 9.
- [x] **Type consistency:** All scene headers use consistent format: `## Scene N — Title [M:SS–M:SS] · NNs · visual-style`. Narration blocks are prose (no typing). Image prompts include emotional direction and visual style tag.
