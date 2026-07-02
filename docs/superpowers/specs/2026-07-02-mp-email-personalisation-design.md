# MP & Minister Email Personalisation — Design

**Date:** 2 July 2026
**Status:** Approved design (Approach C — Hybrid tiered)
**Owner:** the Complainant (Ray Lim)
**Scope:** Phase 2 of the MP email campaign. Phase 1 (collecting the contact list) is complete and produced `data/mp-contact-list.{csv,json,md}` covering all 108 current MPs / Ministers.

---

## Context

The Complainant wants to send a personal, documentary-styled email to every current Singapore Member of Parliament and Minister, alerting them to:
- the new PDPC grievance website at https://pdpaaccessrights.sg
- the documented regulatory pattern behind it (zero Access-Obligation breach findings across PDPC's entire enforcement record)
- the contradiction between that pattern and Singapore Parliament's Written Answer 19596 (Minister Josephine Teo's assurance that organisations must preserve data while requests are being processed, with criminal penalties for intentional concealment)

The 108-strong contact list exists. The base draft of the email exists at `docs/superpowers/plans/2026-07-02-mp-followup-email-draft.md`. Prior correspondence exists in `evidence/letter-to-parliament.html`, `evidence/final-email-to-parliament.html`, `evidence/letter-to-imda-ceo.html`, and `evidence/email-from-ahmad.html`.

What is missing: a personalisation layer. A single base draft sent 108 times with only "Dear [Name]" swapped is the lowest-leverage way to use the contact list. Ministers with direct portfolio responsibility (MDDI → Josephine Teo) and the WP bloc (12 MPs already engaged on PDPA / civil liberties issues) need bespoke versions because:
- a Minister for Digital Development and Information reading a generic email won't feel addressed
- a WP MP will spot a copy-pasted form letter instantly and dismiss it
- the email is the single shot — under-investing here wastes the entire list

This spec designs a tiered personalisation system. It will produce 108 emails across 3 tiers, with bespoke prose for the 25 highest-leverage recipients.

---

## Goals

1. **Quality**: every email reads as if written for that specific recipient. Tier 1 emails must be indistinguishable from a hand-written letter.
2. **Coverage**: 108/108 recipients receive an email. No one is dropped because they fell into a gap.
3. **Source discipline**: every claim is grounded in primary sources. No invented quotes, no em-dashes, no fabricated references. Same rule as the live site (`CLAUDE.md` site-voice rule).
4. **Tone continuity**: every tier matches the tone of `evidence/letter-to-parliament.html` and `evidence/final-email-to-parliament.html`. First-person, factual, willing to be corrected.
5. **Actionability**: outputs are mail-merge ready (CSV) AND reviewable per recipient (one .md file per recipient AND a single index). The user can send without further formatting work.

---

## Non-goals

- Building a mail-merge tool. We assume the user will use Gmail merge / Outlook merge / a third-party tool to send. The CSV output is the contract.
- A/B testing, open tracking, or click tracking. Mass emails to MPs must avoid surveillance optics.
- Multi-language variants. Singapore MPs operate in English.
- Tracking responses. Follow-up on replies is a separate concern.
- Any reference to the underlying motorcycle accident case, the civil reference number, or the criminal reference number (CLAUDE.md: site excludes these; emails follow the same rule).

---

## Tier definitions (25 + ~28 + ~55 = 108)

### Tier 1 — Fully bespoke (~300 words each) — 25 emails

**A. PAP Ministers with direct portfolio / procedural responsibility (10)**
| Minister | Bespoke hook |
|---|---|
| Mrs Josephine Teo (Minister, MDDI) | Reference her Written Answer 19596; ask if her office still stands by it given what's happened |
| Mr Lawrence Wong (PM) | Top of chain; references prior correspondence to PDPC, IMDA CEO, PSC, PSD |
| Mr Lee Hsien Loong (Senior Minister) | PDPA was enacted in 2012 under his watch — historical memory |
| Mr Gan Kim Yong (DPM, MTI) | Senior Cabinet rank; governance lens |
| Mr Chan Chun Sing (Coord. Minister, Public Services) | PSC was misled by IMDA per the Parliament letter — his portfolio |
| Mr K Shanmugam (Coord. Minister, National Security & Home Affairs; Law) | Dual relevance: CCTV for public safety + Law for statutory interpretation |
| Mr Edwin Tong (Minister for Law & Second Minister for Home Affairs) | Law Minister — direct statutory interpretation issues |
| Mrs Indranee Rajah (Minister, PMO / Leader of the House) | Leader of the House — procedural ask |
| Mr Seah Kian Peng (Speaker of Parliament) | Procedural ask: order paper, motion |
| Mr Zhulkarnain Abdul Rahim (MOS, MFA & MSF) | Asked the original PQ that yielded WA 19596 — thank-you + update |

**B. Workers' Party MPs (all 12 — defined deterministically as every MP with `party_affliation == "Workers' Party"` in `data/mp-contact-list.csv`)**
The WP bloc is engaged on PDPA / civil liberties issues. They are natural legislative allies. A bespoke variant for each ensures the email reads as addressed to *that* MP, not as a form letter. Differentiators:

| Sub-group | Hook |
|---|---|
| Pritam Singh (WP chief, Sengkang) | Thanks him as the senior opposition voice; references any prior WP questions on PDPA |
| Sylvia Lim (WP chair, Aljunied) | Acknowledges her long record on civil liberties / administrative law |
| Senior WP MPs (Jamus Jerome Lim, Dennis Tan, others as identified in the contact list) | References their public-record statements |
| Newer WP MPs (Fadli Fawzi, Kenneth Tiong, Mariam Jaafar, Andre Low NCMP, Eileen Chong NCMP, Louis Chua, Abdul Muhaimin, others) | Personalised variant focusing on their background and why this case fits their advocacy areas |

The implementation phase will pull the exact list of 12 from the CSV. Each gets a unique opening + closing. No copy-paste between WP MPs.

**C. Personal-relationship recipients (3) — disclosure framing required**
The Complainant has personal relationships with three of the recipients. The emails to them must disclose the relationship, declare the case stands on its own merits, and avoid any optics of leveraging personal ties. Without disclosure, a reader who discovers the connection would discount the case as favouritism; with disclosure, the case appears principled and the disclosure itself becomes evidence of integrity.

| Recipient | Relationship | Disclosure tone |
|---|---|---|
| Mr Kenneth Goh (NMP) | The Complainant's SMU professor during his MBA | Academic / collegial — references the rigor both teacher and student value in evidence |
| Mr Dinesh Vasu Dash (Minister of State, MDDI & MOH) | The Complainant's group director at MOH during Covid | Professional / first-hand observer — references the direct knowledge of his work and integrity |
| Mr Cai Yinzhou (MP, Bishan-Toa Payoh GRC) | Friend since youth | Personal / direct — acknowledges friendship but states the case is not personal |

**Disclosure content rules (mandatory, applies to all three):**

1. **Acknowledge the relationship in one sentence.** No euphemism. "You were my SMU professor." / "You were my group director at MOH." / "We've known each other since youth."
2. **State explicitly that the case stands on its own merits.** E.g. "I am writing not as a favour, but because the documentary record supports the case and you can verify each claim against the primary sources you know how to read."
3. **Affirm no special treatment is asked.** E.g. "I want nothing from this email that the public record does not warrant." / "If the case did not hold on the documents, I would not be writing."

The disclosure is placed at the **end of the email**, after the sign-off, as a final note of transparency. The case is presented on its merits first; the disclosure then names the relationship, affirms the case stands independently, and states that no special treatment is sought. Rationale: putting disclosure at the close lets the recipient absorb the substance before knowing about the relationship, so they judge the case on its own. Putting it at the open would let the relationship colour the read.

Structure of each Tier 1C email:
1. Subject line
2. Greeting ("Dear Kenneth," / "Dear Dinesh," / "Dear Yinzhou,")
3. Opening paragraph (case-focused, no relationship mention)
4. Body paragraphs (substantive content from base draft, trimmed)
5. Closing question (what they can do)
6. Sign-off ("Yours sincerely,")
7. **Disclosure paragraph (relationship + case-stands-on-its-own affirmation)**
8. Signature with context line ("SMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, MOH, Covid period.")

Each of the three emails has a unique disclosure paragraph reflecting the relationship (academic / professional / personal). No template is shared between them.

The implementation phase drafts each of these with a different warmth gradient (academic → professional → personal), reflecting the relationship.

### Tier 2 — Role-templated (~250 words each) — ~28 emails

Cabinet Ministers + Senior Ministers of State + relevant NMPs outside Tier 1, with role-specific opening line + closing question:

- **MDDI SMS/MOS tier** (Jasmin Lau, Rahayu Mahzam, Tan Kiat How — note: Dinesh Vasu Dash moved to Tier 1C) — PDPC-oversight variant of opening; closing asks MDDI to clarify PDPC's enforcement posture
- **Coordinating Minister rank** (Ong Ye Kung — Coordinating Minister, Social Policies & Health) — public-policy framing on CCTV and access rights
- **Senior Minister of State** (~5 other SMS) — general oversight rank; references 19-month escalation history
- **Minister of State** (~10 MOS) — parliamentary procedure angle
- **Deputy Speaker** — procedural variant
- **Other Mayors** — civic-leadership variant
- **NMPs with relevant expertise** (Kuah Boon Theng — Senior Counsel; note: Kenneth Goh moved to Tier 1C) — legal-expertise variant

### Tier 3 — Base draft + name (~250 words each) — ~55 emails

All other Elected MPs (PAP backbenchers, remaining NMPs without expertise match, remaining NCMPs not in WP). Subject line is the same; opening is "Dear [Name]"; the middle is the trimmed base draft; closing is a generic question. No sport analogy. No Ministry-specific hook. Cai Yinzhou moved to Tier 1C; his seat in Tier 3 is filled by the next backbencher.

---

## Tier 1 / 2 / 3 content rules

| Section | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Opening paragraph | Bespoke — references that Minister's portfolio or past action | Templated per role group | "Dear [Name]" + identical para 1 from base draft |
| Middle paragraphs | Trimmed base draft, with quotes selected to land harder for that recipient | Same trimmed base draft | Same trimmed base draft |
| Closing paragraph | Bespoke question — what they specifically can do | Pre-written role-templated closing (3 variants: PDPC-oversight / procedural / rank-based) | Generic closing question |
| Sport analogy (Maradona / Hand of God) | Keep — adds impact for senior readers | Keep | DROP — slows read for backbenchers who haven't met sender; risk of tone mismatch |
| Length target (soft) | 400-550 words | 280-330 words | 240-280 words |

The base draft at `docs/superpowers/plans/2026-07-02-mp-followup-email-draft.md` is currently ~400 words and must be **trimmed to ~250 words** for the Tier 3 mass version while preserving every primary-source quote (Maradona analogy removed; Annex A reference kept; written answer 19596 link kept). Trim pass is a Phase 2A deliverable.

---

## Personalisation matrix (what facts go where)

Every Tier 1/2 email pulls only from this list of primary sources. **No quote is fabricated.** If a recipient needs a reference we don't have on file, the email paraphrases without quoting and flags `[paraphrased]` so the user knows to verify before sending.

| Recipient class | Primary references |
|---|---|
| Josephine Teo | Written Answer 19596 (https://sprs.parl.gov.sg/search/#/sprs3topic?reportid=written-answer-19596); PDPC's s.22A preservation email quote |
| Zhulkarnain | His original PQ (https://sprs.parl.gov.sg/search/#/result?mpId=); Hansard sitting date 9 Sep 2025 |
| WP leaders (Pritam, Sylvia) | Their prior parliamentary questions on PDPA / civil liberties (pull from sprs.parl.gov.sg search) |
| All MCST context | Decisions DP-2405-C2318 (https://www.pdpc.gov.sg/) and DP-2405-C2445 |
| All PDPC correspondence | `evidence/email-from-ahmad.html`; `evidence/correspondence-no-data-no-breach.html`; `evidence/correspondence-pdpc-guideline-inconsistency.html` |
| IMDA / PSC / PSD chain | `evidence/letter-to-imda-ceo.html`; `evidence/letter-to-parliament.html` § 4 |
| Trend (zero Access breaches) | `data/mp-contact-list.md` link to https://pdpaaccessrights.sg/enforcement-index.html |
| Personal background (signature line) | SMU MBA 2024; Commendation Medal, MOH, Covid period |

---

## Three-point central message (binding for all 108 emails)

Every email — Tier 1, Tier 2, and Tier 3 — must hit these three points clearly and directly. The personalisation (bespoke opening/closing, role framing) wraps around these three points; it does not displace them.

1. **PDPC hid the filter on their website** instead of addressing the underlying issues. Specifically: PDPC redesigned their enforcement-decisions page so that it is no longer possible to filter published cases by the type of obligation breached. The previous filter exposed the zero-Access-Obligation-breach pattern; the new layout hides it.

2. **The Maradona / Hand-of-God analogy.** Referee PDPC was asked to review the play. It denied every request to look at the evidence and let the goal stand. Today's game has VAR, cameras, replay, more evidence than Maradona's referee ever had — and still the referee looked away. The enforcer sits in judgement of itself. Nothing happens. (Carried in Tier 1 and Tier 2; dropped in Tier 3 only.)

3. **The zero-Access-Obligation-investigation statistic.** Across the entirety of PDPC's published enforcement record, PDPC has never once found a breach of the Access Obligation (s.21 PDPA). This is the central empirical claim the site at https://pdpaaccessrights.sg/enforcement-index.html documents. Note the parallel: PDPC aggressively enforces the Protection Obligation (s.24) against data leaks (e.g. Marina Bay Sands); it has never enforced the Access Obligation.

**Writing discipline for the three points** (binding):
- State each point directly, not in long narrative paragraphs.
- One or two sentences per point is the goal; three short sentences is fine if needed.
- Do not bury the points in personal-history prose.
- The personal narrative ("I still do not know what happened to me on the night of the accident") is allowed as brief context but should not displace the three points — place it as a one-sentence opening, not as a lead-in.

## Tone & style (binding for all 3 tiers)

These come from `CLAUDE.md` site-voice rules + the existing correspondence samples:

1. **First-person** — "I am writing..." not "the Complainant is writing..."
2. **Curly quotes** throughout. No straight `"` or `'` in visible text.
3. **No em-dashes** in body prose. Use commas, periods, parentheses, colons. En-dashes OK in numeric ranges ("20–30 days").
4. **No "cover-up" / "gaslight" / adversarial framing**. Use "documented pattern", "regulatory interpretation gap".
5. **No fabricated quotes** — every quote must come from one of: PDPC's website, PDPC's published correspondence (verified in `evidence/`), the PDPA statute, or Singapore Parliament records.
6. **No criminal / civil case references** — the email is about the regulatory interpretation, not about the underlying motorcycle accident case.
7. **Reference, then paraphrase** — when a statute section matters (e.g., s.21, s.22A), cite the section number from https://sso.agc.gov.sg/Act/PDPA2012 and quote the operative language verbatim.
8. **Closing signature** — `Yours sincerely,` + `Lim Zirui (Ray Lim)` + one context line. Same one-liner across all tiers for consistency:
   > SMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, Ministry of Health, Covid period.

---

## Output packaging

### 1. Per-recipient files (`data/personalised-emails/{slug}.md`)

- One file per recipient.
- Filename: `{slug}.md` matching the slug in `data/mp-contact-list.csv`.
- Format: frontmatter (name, slug, email, tier) + Subject line + body in markdown.
- 108 files in total. Inspectable per recipient before send.

### 2. Master CSV (`data/personalised-emails.csv`)

One row per recipient, mail-merge ready. Columns:

| Column | Source |
|---|---|
| `tier` | 1 / 2 / 3 |
| `name` | from contact-list |
| `slug` | from contact-list |
| `email` | primary email |
| `email_source` | parliament / sgdi |
| `subject` | the Subject line |
| `body` | the full email body, plain text with `\n` newlines |

The `body` column is the complete personalised email. Mail-merge tools (Google Contacts import, Outlook, GMass, mailto: link) consume this column.

### 3. Index file (`data/personalised-emails-INDEX.md`)

Lists all 108 recipients grouped by tier, with a one-line note of the personalisation hook for each Tier 1 / Tier 2 recipient. Lets the user scan-review before sending.

Example excerpt:

```markdown
## Tier 1 — bespoke (25)

### A. PAP Ministers
- **Mrs Josephine Teo** (`josephine-teo`, MDDI) — references Written Answer 19596; asks if her office still stands by it
- **Mr Zhulkarnain Abdul Rahim** (`zhulkarnain-abdul-rahim`, MOS) — thank-you + update on outcome of his PQ
- **Mr Lawrence Wong** (`lawrence-wong`, PM) — last-resort contact after 19 months of failed escalation
... [10 rows]

### B. WP MPs (12)
- **Mr Pritam Singh** (`pritam-singh`, WP chief) — collaborative framing; references prior WP PQ on PDPA
- **Ms Sylvia Lim** (`sylvia-lim`, WP chair) — acknowledges her civil-liberties record
... [10 rows]

### C. Personal-relationship (3)
- **Mr Kenneth Goh** (`kenneth-goh`, NMP) — SMU professor during MBA; relationship disclosure + case-stands-on-merits
- **Mr Dinesh Vasu Dash** (`dinesh-vasu-dash`, MOS) — MOH group director during Covid; relationship disclosure + case-stands-on-merits
- **Mr Cai Yinzhou** (`cai-yinzhou`, PAP backbencher) — friend since youth; relationship disclosure + case-stands-on-merits
```

---

## Workflow

1. **Author**: spec is approved.
2. **Plan**: writing-plans skill produces the implementation plan.
3. **Trim pass** (Phase 2A): reduce the base draft from ~400 words to ~250 words while preserving all primary-source quotes. Output: `docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md`.
4. **Draft Tier 1** (Phase 2B): 25 bespoke emails, one at a time, drafting against the matrix above. Drafter must source each cited quote from `evidence/` or the PDPA text.
5. **Draft Tier 2** (Phase 2C): ~28 role-templated emails from 3 templates × sub-groups.
6. **Tier 3** (Phase 2D): 55 base-draft emails — only "Dear [Name]" substituted.
7. **Quality gate** (Phase 2E): for each tier, a verifier checks: no em-dashes, curly quotes only, every quote is in `evidence/` or PDPA text, signature consistent, length target hit.
8. **User review** (checkpoint): user reviews Tier 1 first, signs off, then Tier 2 sample of 3, then approves the lot.
9. **Outputs**: write the 108 .md files + CSV + INDEX.
10. **Send**: user runs mail-merge from CSV with **BCC** (NEVER To/CC). Email is sent once per recipient.

---

## Quality verification

Before any send:

1. **Source discipline**: every quote that appears in any of the 108 emails must be grep-able in `evidence/` + `PDPC Rulings/` + the PDPA at https://sso.agc.gov.sg/Act/PDPA2012 + the Singapore Parliament records. No invented quotes.
2. **Style**: run `grep -cE "[a-z]'[a-z]"` and `grep -cE "[a-z]\"[a-z]"` on each `data/personalised-emails/{slug}.md`. Both must return 0 (no straight quotes in word boundaries).
3. **Em-dash check**: run `grep -cE '—'` on each file. Must return 0 in body prose (en-dash `–` for numeric ranges is OK).
4. **Tier-1B completeness**: all 12 WP MPs have a unique opening + closing (no copy-paste between WP MPs).
5. **CSV valid**: open the CSV in Excel/Sheets, verify 108 rows, headers correct, no broken newlines in the body column.
6. **No accidental leak**: no occurrence of "GCW.PI", "GCW.CRIM", "motorcycle", "taxi", "Quak Chee Wah", "Ray Lim" (use "Lim Zirui" or "the Complainant") in the visible body of any email. The case reference would re-anchor the email to the personal accident, which the site decided to exclude.
7. **Recipient list cross-check**: every email in the CSV appears in `data/mp-contact-list.csv` (no orphans). Every slug in the contact list has a corresponding `.md` file.

---

## Open questions (decided)

1. **Length**: trimming the base draft from ~400 to ~250 words. **Decision**: drop the Maradona analogy in Tier 3 only; preserve every primary-source quote.
2. **BCC prerequisite**: the user must use BCC at send time. The CSV body is the same regardless; BCC is a mail-merge setting. The spec notes this as a hard prerequisite but does not build tooling to enforce it.
3. **WP NCMPs (Andre Low, Eileen Chong)**: they sit in parliament but have no GRC and no constituency office. **Decision**: treated as part of the WP bespoke block — they are legislators and the ask is procedural.
4. **NMPs**: Singapore NMPs include Kenneth Goh (SMU law) and Kuah Boon Theng (Senior Counsel). Their expertise makes them Tier 2 candidates even though they are not in a Cabinet role. **Decision**: Tier 2 with a legal-expertise variant.
5. **Reply handling**: not in this scope. Whatever replies arrive are handled manually by the user in a separate workflow.

---

## Reusable from existing project

- `data/mp-contact-list.csv` — 108-row recipient list with verified emails (parliament + sgdi fallback)
- `docs/superpowers/plans/2026-07-02-mp-followup-email-draft.md` — base draft to be trimmed
- `evidence/email-from-ahmad.html` — PDPC officer correspondence (verbatim)
- `evidence/correspondence-no-data-no-breach.html` — PDPC s.22A preservation gap quote
- `evidence/correspondence-pdpc-guideline-inconsistency.html` — PDPC disowning its own guidelines
- `evidence/letter-to-imda-ceo.html` — full complaint to IMDA CEO
- `evidence/letter-to-parliament.html` — full Parliament letter with PSC, PSD, IMDA chain
- `evidence/final-email-to-parliament.html` — final email with the 4 issues framed
- `CLAUDE.md` site voice rules (curly quotes, no em-dashes, primary-source discipline)
- `docs/superpowers/plans/2026-04-21-email-timeline-catalog-plan.md` — earlier email-catalog work

## Files created

- `data/personalised-emails.csv` — master mail-merge CSV
- `data/personalised-emails/{slug}.md` — 108 per-recipient files
- `data/personalised-emails-INDEX.md` — review index
- `docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md` — trimmed base draft (Phase 2A)
- `docs/superpowers/plans/2026-07-02-mp-email-tier2-templates.md` — 3 tier-2 templates (Phase 2C)

No existing project files modified.

## Verification (end-to-end)

1. Open `data/personalised-emails-INDEX.md` — confirm 108 recipients grouped correctly.
2. Open each Tier 1 `.md` file — confirm unique opening + closing, no source-discipline violations.
3. Open 3 random Tier 2 `.md` files — confirm tone matches Tier 1.
4. Open 3 random Tier 3 `.md` files — confirm "Dear [Name]" substituted and rest matches base.
5. Run all 6 quality-verification grep checks (Section above); all return expected counts.
6. Open CSV in Excel — confirm 109 lines (header + 108 rows), body column shows full email with line breaks preserved.
7. Confirm no criminal/civil case references leaked into any of the 108 emails.
8. (User send step, out of scope of this spec) Run mail-merge from CSV with BCC.

---

## Handoff

Once approved, invoke `superpowers:writing-plans` to produce the implementation plan. The plan decomposes Phase 2 into tasks: A (trim base), B (Tier 1 PAP), C (Tier 1 WP), D (Tier 2 templates + assignments), E (Tier 3 generation), F (outputs), G (quality gate).