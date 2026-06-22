# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**Project:** Ray Lim's motorcycle accident PTSD legal case documentation system
**Case Reference:** GCW.PI.6806.2024 (Civil) / GCW.CRIM.6805.2024 (Criminal)
**Accident Date:** April 13, 2024, ~5:06 AM, Cairnhill Road, Singapore

---

## Repository Structure

```
H:/My Drive/Driving Legal Issue/     ← Main case folder (this repo)
├── Court/                            ← All court documents (ENE, aCDR, criminal, civil)
├── Hospitalisation Bill/            ← Medical records, MC certs, Dr Wuan reports
├── Certification/                    ← NS transcript, SMU MBA, awards, photos
├── Accident Reconstruction/          ← Videos, PC-Crash files, calculations
├── docs/superpowers/plans/         ← Planning docs, gap logs, evidence compilations
├── NotebookLM_Upload/               ← Medical PDFs ready for NotebookLM upload
├── Calculations/                    ← Physics speed/braking calculations (Calculations.xlsx)
├── PDPA ACT and Advisory/           ← PDPA legislation and PDPC complaint documents
├── PDPC Complain/                   ← CCTV deletion complaint to PDPC
├── PDPC Rulings/                   ← PDPC decisions on MCST 3615/4599
├── PDPC Appeal Committee/          ← Ray Lim's appeal against PDPC decision
└── docs/superpowers/plans/         ← Affidavit gap logs, WhatsApp evidence compilations

C:\Users\limzi\Documents\AntiGravity\Driving Legal Emails\  ← Email data (external)
├── email-timeline/                  ← Processed Gmail JSON exports (law-case-complete.json, sent-all-threads.json)
├── obsidian-vault/                  ← Auto-generated Obsidian timeline notes
├── scripts/                         ← Email processing pipeline (01-deduplicate.js through 13-*.js)
└── notebook-lm-export/              ← Topic-organized exports for NotebookLM upload

C:\Users\limzi\whatsapp_export\      ← WhatsApp chat exports (external)
├── extract-and-rename.js            ← Extract zip files, rename by chat name
├── format-chats.js                  ← Format raw _chat.txt → formatted .md
├── filter-legal-chats.js            ← Filter to 13/04/2024 onwards
└── LegalChatTxt/                    ← 135 filtered .md files ready for evidence
```

**Critical path distinction:**
- `H:/My Drive/Driving Legal Issue/` = this repository, case documents
- `C:\Users\limzi\Documents\AntiGravity\Driving Legal Emails\` = email data (external, not in repo)
- `C:\Users\limzi\whatsapp_export\` = WhatsApp chat exports (external)

---

## Case Overview

**Claimant:** Lim Zirui (Ray Lim, Lin Zirui)
**Defendant:** Quak Chee Wah (taxi driver)
**Civil Reference:** GCW.PI.6806.2024
**Criminal Reference:** GCW.CRIM.6805.2024
**Total Files:** 863 files — full catalog at `FILE_CATALOG.md`
**Solicitors:** Characterist LLC (CLLC) — Mitchell Leon, mitchell@characterist.com, +65 6222 5562, 51 Goldhill Plaza #10-01

### Accident
- **Date:** 13 April 2024, approximately 5:06 AM
- **Location:** Cairnhill Road (near The Scotts Tower / Blk 6807 Springleaf), Singapore
- **Motorcycle:** FBM 8124G (Yamaha) — claimant's
- **Taxi:** SHA 4517A (ComfortDelGro, driven by Quak Chee Wah) — defendant's

### Liability
- **90% liability against Defendant** — confirmed at two ENE sessions: **1 December 2025** and **20 February 2026**
- Defendant insurer accepts liability but disputes quantum

### Injuries
1. Mild traumatic brain injury / concussion (subarachnoid haemorrhage)
2. PTSD with anxiety and depression — ongoing psychiatric treatment (Dr Eugene Wuan)
3. Cranial nerve IV (trochlear) palsy — diplopia resolved by Jun 21, 2024 (~2 months)
4. Cervical spondylosis + strains
5. Left shoulder, wrist, knee injuries

### Criminal
- **s 67(1)(b) RTA** — breath alcohol 45 mcg/100ml (limit 35)
- Pleaded guilty; no prior convictions
- Case closed September 2025 after 18 months bail reporting

---

## Case Status

**Stage:** Supporting Affidavit for Interim Payment — 13 gaps to fill
**Interim Payment Sought:** $100,000 (legal basis: O.29 r 9 ROC)
**Court permission:** pending

Full gap log: `docs/superpowers/plans/2026-04-20-affidavit-gap-log.md`
Agent briefing: `docs/superpowers/plans/2026-04-20-affidavit-agent-briefing.md`

---

## Affidavit Gaps (13 total)

| # | Gap | Status |
|---|---|---|
| 1 | Head/brain symptoms | Filled from MC certs + discharge info |
| 2 | Eye resolution (~2 months) | ✅ confirmed — resolved by Jun 2024 |
| 3 | Neck resolution | NOT resolved — user confirmed always aching |
| 4 | Psychiatric detailed account | MUST come from Ray personally |
| 5 | Physiotherapy confirmation | Started Aug 2024, 1-2 sessions only |
| 6 | MC total days | CLLC to provide |
| 7 | MBA details (SMU) | ✅ confirmed — full-time, March 2024 grad, 4.0 GPA |
| 8 | MOH employment dates | May 1, 2022 to Dec 30, 2023 |
| 9 | BD Director job | cprint.com.sg, $10K/month, Jan 19–Feb 6 2026 |
| 10 | Financial need / $100K | Lost $10K/month job Feb 2026, personal loans taken |
| 11 | Declaration date | Late May 2026 (affirm after return from retreat) |
| 12 | Grab Food employment | ✅ confirmed — short stints May–Aug 2024 |
| 13 | Job application records | 74 applications from Jul 2024, Gmail API data collected |

---

## Key Documents

### Affidavit & Interim Payment
| Document | Path |
|---|---|
| Supporting Affidavit (in progress) | `Court/Civil Case/Interim Payment/6806_20260420_IP Supporting Affidavit.docx` |
| Mitchell Email re: interim payment | `Court/Civil Case/Interim Payment/Mitchell Email Interim Payment.pdf` |

### Medical
- Dr Eugene Wuan (Psychiatrist): Better Life Psychological Medicine Clinic
- Asst Prof Vincent Nga: NUH Neurosurgery
- Dr Kristen Wong: NUH Ophthalmology
- Eye specialist discharged October 2025 (diplopia resolved, VA 6/6)
- Physiotherapy started August 2024

### Liability
- ENE Judge Comments Dec 2025: `Court/ENE/6806_20251201_ENE Comments by Judge.pdf`
- ENE Judge Comments Feb 2026: `Court/ENE/20260223 20260220_ENE Comments by Judge.pdf`
- AEIC (Liability) Claimant: `Court/Civil Case/6806_20260318_AEIC (Liability).pdf`
- AEIC (Liability) Defendant: `Court/aCDR/AFFIDAVIT_OF_EVIDENCE_IN_CHIEF_(QUAK_CHEE_WAH).pdf` (scanned, not OCR'd)

### PDPA/CCTV Complaint
- PDPC decision (MCST 4599): `PDPC Rulings/Decision MCST 4599 DP-2405-C2318.pdf`
- PDPC summary (MCST 3615): `PDPC Rulings/Summary of Commission's Findings - MCST 3615 DP-2405-C2445.pdf`
- Ray's appeal: `PDPC Appeal Committee/NOTICE OF APPEAL.docx`
- White paper: `PDPC Complain/White Paper - PDPA CCTV Loophole (20 Aug 2025).pdf`

---

## Evidence Compilations

### WhatsApp Evidence
All in `docs/superpowers/plans/`:
- `2026-05-04-whatsapp-quantum-evidence.md` — 928-line compiled evidence across 10 topics
- `2026-05-04-whatsapp-search-results.md` — Full search results with timestamps
- `2026-05-04-annex-affidavit-paragraphs-9-35.md` — AFFIDAVIT ANNEX (paragraphs 9-35)
- `2026-05-04-quantum-narrative-mensa-harassment.md` — Mensa harassment verbatim quotes
- `2026-05-04-quantum-narrative-police-bail.md` — Police bail narrative
- `2026-05-04-quantum-narrative-vipassana-travel.md` — Vipassana + travel narrative
- `2026-05-04-quantum-narrative-may-2025-jan-2026.md` — May 2025–Jan 2026 narrative

### Mensa Harassment Evidence
- **Jin Sheng** (Bits & Bites SIG, 06/09/2025): "You are sick and I have no time for you" (3:00 PM)
- **Jude** (Bits & Bites SIG, 30/10/2024): "keep a low profile... there is word that's been out about what you've done"
- NotebookLM: `e5523905-4915-46e5-a8a3-8042cc6a088d`

---

## NotebookLM

**Notebook:** "Legal Documents" (ID: `9f4326df-af48-4bfb-a785-c63108a79695`)
- 121 files uploaded
- Videos/frames: Already on Google Drive

### Email Export Data
**Source:** `C:\Users\limzi\Documents\AntiGravity\Driving Legal Emails\notebook-lm-export\`
- 7 files, 317 threads (law-case-complete.json: 206, sent-all-threads.json: 156)

### Gmail Label Structure

```
INBOX/
├── 0001 Job Search [Label_19]
│   ├── Linkedin [Label_20]         ← large, pending (Label_54 = Law Case sub-label)
│   ├── Others [Label_21]           ← 11 threads done
│   ├── Consulting [Label_23]       ← 681 threads done
│   └── Jobslead advice [Label_45]   ← 8 threads done
├── 001 Law Case [Label_42]
│   └── Linkedin Job Search [Label_54] ← 4,962 threads done
└── 02 Consulting Jobs [Label_30]
```

---

## Workflow

1. Check `CLAUDE.md` (this file) for case overview and document paths
2. Check `FILE_CATALOG.md` for complete file index
3. Check gap log (`docs/superpowers/plans/2026-04-20-affidavit-gap-log.md`) for affidavit progress
4. Always cite paths and quotes when making factual claims

## 12 Rules

These rules apply to every task in this project unless explicitly overridden.
Bias: caution over speed on non-trivial work. Use judgment on trivial tasks.

### Rule 1 — Think Before Coding
State assumptions explicitly. If uncertain, ask rather than guess.
Present multiple interpretations when ambiguity exists.
Push back when a simpler approach exists.
Stop when confused. Name what's unclear.

### Rule 2 — Simplicity First
Minimum code that solves the problem. Nothing speculative.
No features beyond what was asked. No abstractions for single-use code.
Test: would a senior engineer say this is overcomplicated? If yes, simplify.

### Rule 3 — Surgical Changes
Touch only what you must. Clean up only your own mess.
Don't "improve" adjacent code, comments, or formatting.
Don't refactor what isn't broken. Match existing style.

### Rule 4 — Goal-Driven Execution
Define success criteria. Loop until verified.
Don't follow steps. Define success and iterate.
Strong success criteria let you loop independently.

### Rule 5 — Use the model only for judgment calls
Use me for: classification, drafting, summarization, extraction.
Do NOT use me for: routing, retries, deterministic transforms.
If code can answer, code answers.

### Rule 6 — Token budgets are not advisory
Per-task: 4,000 tokens. Per-session: 30,000 tokens.
If approaching budget, summarize and start fresh.
Surface the breach. Do not silently overrun.

### Rule 7 — Surface conflicts, don't average them
If two patterns contradict, pick one (more recent / more tested).
Explain why. Flag the other for cleanup.
Don't blend conflicting patterns.

### Rule 8 — Read before you write
Before adding code, read exports, immediate callers, shared utilities.
"Looks orthogonal" is dangerous. If unsure why code is structured a way, ask.

### Rule 9 — Tests verify intent, not just behavior
Tests must encode WHY behavior matters, not just WHAT it does.
A test that can't fail when business logic changes is wrong.

### Rule 10 — Checkpoint after every significant step
Summarize what was done, what's verified, what's left.
Don't continue from a state you can't describe back.
If you lose track, stop and restate.

### Rule 11 — Match the codebase's conventions, even if you disagree
Conformance > taste inside the codebase.
If you genuinely think a convention is harmful, surface it. Don't fork silently.

### Rule 12 — Fail loud
"Completed" is wrong if anything was skipped silently.
"Tests pass" is wrong if any were skipped.
Default to surfacing uncertainty, not hiding it.

---

## PDPC Grievance Site (`pdpc-grievance-site/`)

A sub-project of the case folder. A deployed public site presenting the Complainant's documented grievance against PDPC, IMDA, MCST 3615 (Suites@Cairnhill), and MCST 4599 (The Scotts Tower). The site is the Parliament-facing version of the case. **"Ray Lim" is anonymized throughout the site as "the Complainant" / "the Complainant's".**

### Key paths

- **Site repo:** `pdpc-grievance-site/` (GitHub repo, deployed via GitHub Pages)
- **Live URL:** https://pdpaaccessrights.sg/
- **GitHub repo:** https://github.com/SonwinLim/pdpc-grievance-site
- **Analytics:** GoatCounter at https://sonwin.goatcounter.com/ (privacy-respecting, no cookies)
- **Design spec:** `docs/superpowers/specs/2026-06-17-pdpc-grievance-site-design.md`
- **All deliverables (specs, plans, extracts):** `docs/superpowers/plans/` and `docs/superpowers/specs/`
- **Hosting:** GitHub Pages with custom domain **pdpaaccessrights.sg** (live).

### Site structure (15 sections, current order as of 2026-06-21)

1. `#hook` — the one-sentence "what happened"
2. `#summary` — 3-minute executive summary; 3 CTA cards (MPs / public "Rights on paper" / lawyers)
3. `#story` — **The explanatory narrative in full** (added 2026-06-20): 5-act synthesis that states the single explanation fitting all documented facts; opens with brain injury / memory loss context; closes with parliamentary question callout on zero Access Obligation breach findings
4. `#promise` — **The parliamentary assurance centrepiece** (added 2026-06-21): reproduces Singapore Parliament Written Answer 19596 in full (Q by Mr Zhulkarnain Abdul Rahim, A by Minister Josephine Teo) framed as an official-record document, then juxtaposes the Minister's three guarantees against what happened in this case. The canonical home for the verbatim Q&A (Failure #3 and #process now link here)
5. `#cases` — MCST 3615 vs MCST 4599 side-by-side (credibility foundation)
6. `#reform` — 4 legislative asks + 2 question groups (Questions about the PDPA / Questions about PDPC's conduct; Access Obligation zero-breach question leads group one)
7. `#why` — "Why this matters to every Singaporean": real consequences; enforcer/damager inversion; Street View removal; public-as-check-and-balance
8. `#process` — "A documented pattern": PDPC ceased correspondence; PSC misled; filter contrast (filter previously showed breach breakdown; new layout hides it)
9. `#narrative` — "PDPC's Narrative vs. The Record" (**6 contrasts** + 3 structural callouts: "no data, no investigation", "The investigation itself is an acknowledgment", "Nine questions PDPC has declined to answer")
10. `#contradictions` — 10 contradiction cards (card #2 strengthened with on-site identification evidence from both condos)
11. `#transparency` — the filter-state observation
12. `#failures` — **12 documented failures** (accordion; failures #9–12 added 2026-06-19)
13. `#timeline` — 19-month vertical timeline
14. `#verify` — embeds (YouTube video + NotebookLM)
15. `#evidence` — source-documents index

Plus an auxiliary page: `enforcement-index.html` — filter-by-obligation matrix over PDPC's 374 published enforcement actions.

### Recent changes (2026-06-21 session)

- **Entry gate overlay** added: full-screen Parliamentary assurance vs PDPC findings, every visit. Minister Teo's verbatim Written Answer 19596 side-by-side with PDPC's no-breach findings.
- **`#reform` section rewritten:** 4 themed legislative asks (deletion loophole, identifiability, non-statutory grounds, independent oversight) + 2 question groups. Lead ask and question flagged.
- **`#promise` section added:** Written Answer 19596 reproduced in full as an official-record centrepiece. Three-guarantee juxtaposition against this case. Canonical home for the verbatim Q&A.
- **Voice:** explanatory narration converted to third person ("the Complainant") throughout. Hero/testimony and verbatim quotes remain first person. Street View section aligned.
- **Pre-MP review pass:** timeline corrected (MP appeals May–Jun 2024; decisions issued privately; IMDA IAU Aug 2025 entry). §5.1(b) mis-citation removed. Security-guard statements attributed. Street View tightened.
- **Masking "money shot" figure** in `#why`: PDPC's own Advisory Guidelines page 42 (para 4.59: blurred/pixelated images still identifiable) embedded with verbatim quote, refuting the invented clarity test.
- **Shared-CEO references** updated: acknowledge CEO/Commissioner separation (Apr 2026); former Deputy Commissioner promoted to Commissioner.
- **Case reference numbers** (GCW) and criminal references removed from site narration.
- **Nav:** wraps to two rows on desktop, collapses to single scrollable row on mobile.
- **Emails drafted** to MP Zhulkarnain and IMDA/PDPC leadership.
- **Style:** 17 straight apostrophes in evidence subpages converted to curly. 0 straight quotes or em-dashes site-wide.
- **GoatCounter analytics** added (privacy-respecting, no cookies).
- **Video summary** (Minimax, YouTube) embedded in #verify as third column.
- **Gate improvements:** MP question beside Minister photo, full citation with sitting date (9 Sep 2025), linked Hansard, sub-list for PDPC non-engagement, punch line moved to left panel.
- **Responsive redesign:** three-tier breakpoints (phone <560px, tablet 560–820px, desktop 820–1200px, large desktop 1200px+). Nav scroll only on phones.

### Recent changes (2026-06-19 session)

- **Anonymized** "Ray Lim" → "the Complainant" / "the Complainant's" site-wide (13 replacements)
- **Failures #9–12 added:** whistleblower leak (#9), IMDA IAU "no wrongdoing" (#10, expanded with full IMDA arc + apology request), proof barrier (#11), MBS double standard (#12)
- **New narrative callout** "The investigation itself is an acknowledgment" — PDPC/IMDA chose to investigate (not dismiss as frivolous per Advisory Guidelines s.22(1)(a)); no apology given; findings departed from law
- **Card #2 strengthened** with on-site identification evidence: security staff identified the incident within minutes in both cases; the footage obtained through on-site identification was then used by PDPC to rule out identifiability
- **Section order reflow:** summary moved to position 2; reform moved to position 4 (accessible to MPs without wading through evidence)
- **Section 3 of #process** updated with filter contrast: filter previously showed obligation breakdown; new layout hides zero-Access-Obligation-breach pattern
- **4th parliamentary question added** to #reform: how many Access Obligation complaints filed; why zero breach findings
- **CTA card for public** updated: "Rights on paper" — PDPA promises access right; PDPC's rulings left it unenforceable in practice

### Recent changes (2026-06-20 session)

- **MCST 4599 case card** updated: added verbal refusal on 17 Apr 2024 (privacy cited as blanket reason; when challenged, claimed no footage — refuted by PDPC's own finding that footage existed until 30 Apr); refused to provide DPO contact, company name, or escalation path
- **MCST 3615 case card** updated: managing agent named (Property Facility Services Pte Ltd, unnamed in published summary); new "DPO conduct" row added — Mohamed Nasir Mustaffa (Director/DPO, PFS) gave false legal advice in writing on 21 May 2024 ("Only by police direct/order the MCST to disclose the footage"); dismissed Complainant's correct PDPA challenge on 23 May as "difficulty understanding" and refused further communication
- **"Stated refusal grounds" row** added to both case cards: neither MCST cited a ground listed in s.21(3) or the Fifth Schedule; PDPC did not test the stated grounds — substituted its own reasoning in each case
- **Contradiction card #3** strengthened: MCST 3615 column now has verbatim DPO quote attributed by name and date (previously vague paraphrase)
- **Narrative contrast #6** added: "The stated refusal grounds were never tested against the Fifth Schedule" — documents that PDPC invented reasoning for the MCSTs rather than testing what they actually said against the statute
- **"Nine questions PDPC has declined to answer"** callout added in #narrative (3rd structural callout): 9 specific questions spanning 6 PDPA sections, all met with identical one-line response ("Guidelines not determinative; PDPA takes precedence") without naming the guideline, clause, or conflict
- **Q9 expanded** with "clarity test" argument: PDPC's invented pixel-clarity standard (absent from PDPA) effectively removes most real-world CCTV footage from access protection
- **#why section** expanded under "enforcer became damager": clarity test systemic implications added
- **New `#story` section** inserted between `#summary` and `#cases` (commits `0626bae`, `a7b4fb7`): 5-act top-down synthesis giving readers the single explanatory framework before detailed evidence. Lede opens with traumatic brain injury context — subarachnoid haemorrhage, all memory lost — foregrounding that the footage was needed to understand what happened to him personally, not only for legal proceedings. Five parts: (1) what the Complainant needed, (2) what both condos did and why they weren't acting recklessly, (3) what PDPC did — invented reasoning, clarity test, nine identical non-answers, withheld decisions, declared closed, (4) zero s.21 breach findings across 384 cases — clarity test explains it, (5) the only parsimonious explanation: de facto policy of non-enforcement implemented through the clarity test. Closes with parliamentary callout: "if the Access Obligation has produced zero breach findings across over a decade of PDPC enforcement, is the obligation being enforced at all?"

### Pending

- **Institutional direction callout** — BLOCKED on Ray downloading PDPC correspondence emails. See handoff for details.
- **Stray duplicate PNGs** — `pdpc-masking-42.png` and `pdpc-masking-p41-41.png` in repo root (duplicates of `evidence/` copies). Untracked, not deployed. Delete to tidy.
- **Send drafted emails** — WhatsApp to MP Zhulkarnain + email to IMDA/PDPC leadership, both drafted and ready.

### Site-specific design rules (apply in addition to the 12 above)

#### Source-discipline rule

**Every claim on the site must be grounded in either a verbatim primary-source quote or a verifiable live URL.** Author's evidence subpages (in `evidence/`) are *further reading*, never the *reference*.

- Card footers use primary sources only (PDPC website / specific case decisions / PDPA statute).
- "Further reading:" lines below the footer point to the author's evidence subpages as analysis.
- Refactor commit `a5e0558` made this change site-wide.

#### Style rules

- **Curly quotes throughout** (no straight ASCII `"` or `'` in any visible text).
- **No em-dashes anywhere.** Use commas, periods, parentheses, or colons instead. En-dashes for numeric ranges are OK.
- **En-dashes for numeric ranges** are OK in body (e.g. "20–30 days"). This is the one body-prose dash exception.
- **Tone:** documentary, factual, willing-to-be-corrected. No "cover-up" word in body prose (use "documented pattern" instead). No "gaslight" or adversarial framing unless explicitly approved by Ray.
- **No fabricated quotes.** Every quote must come from a verifiable source. If in doubt, leave it out or paraphrase with a clear "[paraphrased]" marker.
- **"the Complainant"** (capital C) throughout — never "Ray Lim" or "Ray" in visible body text.

### Critical primary-source documents (live, on the record)

- **PDPC email to the Complainant admitting the s.22A preservation gap:** "we are aware and presently reviewing this issue, which we will raise to the Ministry for their consideration." (Failure #3 on the site.)
- **Singapore Parliament Written Answer 19596** (Minister Josephine Teo in reply to Mr Zhulkarnain Abdul Rahim): organisations required to preserve data while requests are being processed; criminal penalties for intentional concealment. URL: https://sprs.parl.gov.sg/search/#/sprs3topic?reportid=written-answer-19596
- **MCST 4436 (River Isles) — direct precedent for MCST 3615.** PDPC applied s.4(6) PDPA subordination and concluded the MCST could provide the footage. MCST 3615 never engaged s.4(6).
- **MCST 4375 + MCST 3593** — direct precedents for MCST 4599. Security companies acting as data intermediaries were assessed under s.24 in both. MCST 4599 silently departed.
- **PDPC's published-decisions page** has no obligation-type filter (verified 19 Jun 2026): https://www.pdpc.gov.sg/organisations/regulations-decisions/enforcement-decisions
- **White Paper (20 Aug 2025):** `PDPC Complain/White Paper - PDPA CCTV Loophole (20 Aug 2025).pdf` — documents on-site identification by security staff in both condos; "other information" limb argument.
- **PDPA legislation:** https://sso.agc.gov.sg/Act/PDPA2012

### Git workflow

- Single branch: `main`
- Push triggers GitHub Actions workflow (`.github/workflows/pages.yml`) → GitHub Pages deploy
- Repo is **public** (required for free GitHub Pages); pages are served publicly
- GitHub Pages must be enabled in repo Settings → Pages → Source: "GitHub Actions" (one-time setup; otherwise deploys fail with "Get Pages site failed")
- All commits should include a clear message describing what changed; commit messages often cite the deliverable document (e.g. "Add contradictions #8, #9, #10")

### Local development

```bash
cd pdpc-grievance-site
python3 -m http.server 8099  # static server, no build step
# visit http://localhost:8099/index.html
```

Verification uses puppeteer (installed in `../PDPC Rulings/Other Rulings/node_modules/`). Standard check:

```javascript
const puppeteer = require('puppeteer');
// launch headless, navigate, check DOM, screenshot
```

### Card numbering convention

- **Cards #1–#7** are the original 7 contradictions (added in initial contradictions-section build).
- **Cards #8, #9, #10** added later from the 384-case pattern matrix extraction (commits `c9c5757`, `eda857e`).
- **Card #2** strengthened 2026-06-19 with on-site identification evidence from both condos (White Paper source).
- New contradiction cards should pick up at **#11** if added.
- All cards use the 4-column template (Their own guideline/precedent · What they did · Why it contradicts · Their response & what's missing).

### Failure numbering convention

- **14 failures**, accordion layout (failures #1–8 original; #9–12 added 2026-06-19; #13–14 added 2026-06-20).
- Failure titles must NOT use em-dashes in body prose (header-only exception applies to titles that act as headers).
- Failure bodies are paragraphs, no `<h4>` etc. — keep it flat.

### Common pitfalls (learned the hard way)

- **Edit tool:** when replacing text that contains literal `—` or curly quotes, use the literal character in `old_string`, NOT the `—` escape — `Edit` may not match the escape.
- **Card footers:** never link to `evidence/*.html` for the *reference*; only for *further reading*. Always link to a primary source (PDPC, statute) for the reference.
- **Nested anchors:** `<a>` inside `<a>` is invalid HTML. The "Also:" follow-up link in #summary must be a sibling of the cta-card `<a>`, not a child.
- **PDPC URLs:** `pdpc.gov.sg/undertakings/...` and `pdpc.gov.sg/all-commissions-decisions/...` returned 404 after a recent site restructure (verified June 2026). For broken links, point to `https://www.pdpc.gov.sg/` root with the document name as anchor text.
- **Source-discipline audits** have been run multiple times. Always check `index.html` for `grep -cE "[a-z]'[a-z]"` (straight apostrophe in word) and `grep -cE "[a-z]\"[a-z]"` (straight quote in word) after every change. Both must be 0.
- **Section reorder (2026-06-19):** sections were reordered via a Python script (not Edit tool). If reordering again, use the same approach: extract sections by line number, reassemble, write the full file. Do not attempt to move large HTML blocks with Edit.

### Session continuity

This file is the entry point for a fresh session. Read it first, then `git log --oneline -10` in `pdpc-grievance-site/` for the live state of the site. Check the handoff for full context.

**Full handoff document:** `../docs/superpowers/plans/2026-06-20-full-handoff.md` (updated 22 Jun 2026). — comprehensive session-state capture including both workstreams (PDPC site + civil affidavit), all pending tasks, key contacts, primary sources, and entry-point checklist for a fresh session.