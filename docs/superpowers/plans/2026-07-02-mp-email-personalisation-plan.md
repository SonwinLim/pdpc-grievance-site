# MP & Minister Email Personalisation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce 108 personalised MP/Minister emails across 3 tiers, output as `data/personalised-emails.csv` (mail-merge ready) + 108 per-recipient .md files + `data/personalised-emails-INDEX.md` (review index). Each email reads as if written for that specific recipient and meets the source-discipline, tone, and style rules from the spec.

**Architecture:** Markdown content generation, no app code. Each tier uses a different strategy: Tier 1 (25 emails, bespoke prose), Tier 2 (~28 emails, role-templated), Tier 3 (~55 emails, base-draft with name substitution). Outputs are pure static files for the user to mail-merge externally.

**Tech Stack:** Markdown + bash for verification. No build step, no dependencies. Verification via grep + wc. Python or Node for Tier 3 bulk generation.

## Global Constraints (binding for every task)

From the spec at `docs/superpowers/specs/2026-07-02-mp-email-personalisation-design.md`:

1. **Tone**: first-person ("I am writing..."), factual, willing to be corrected. Match `evidence/letter-to-parliament.html` and `evidence/final-email-to-parliament.html`.
2. **Curly quotes throughout**. No straight `"` or `'` in visible text. Verify with `grep -cE "[a-z]'[a-z]"` (must be 0) and `grep -cE "[a-z]\"[a-z]"` (must be 0) on each output file.
3. **No em-dashes (`—`) in body prose**. Use commas, periods, parentheses, colons. En-dashes (`–`) OK only in numeric ranges. Verify with `grep -c '—'` (must be 0) on each output file.
4. **No adversarial framing**. Never use "cover-up", "gaslight". Use "documented pattern", "regulatory interpretation gap", "departure from statute".
5. **No fabricated quotes**. Every quote must come from one of: PDPC's published correspondence (`evidence/*.html`), PDPC's published rulings, the PDPA at https://sso.agc.gov.sg/Act/PDPA2012, or Singapore Parliament records.
6. **No criminal/civil case references**. No "GCW.PI", "GCW.CRIM", "motorcycle", "taxi", "Quak Chee Wah", "Ray Lim" in body text. Use "Lim Zirui" in signature, "the Complainant" only when referring to the documented subject in third-person.
7. **Signature (every email)**: `Yours sincerely,` + `Lim Zirui (Ray Lim)` + one context line: `SMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, Ministry of Health, Covid period.`
8. **Length targets** (soft, not hard ceilings): Tier 1 **typically 400-550 words** (bespoke opening 60-90w + base body ~240w + Maradona ~90w + bespoke closing 30-50w; longer is acceptable when personalisation depth requires it per the user's "spare no tokens" direction); Tier 2 **280-330 words** (role-templated opening 40-60w + trimmed body ~240w + Maradona ~90w + role closing 30-50w); Tier 3 **240-280 words** (no opening or closing changes; no Maradona).
9. **Trim base draft** from ~400 to ~250 words. Drop Maradona/Hand-of-God analogy in Tier 3 only (keep for Tier 1 and Tier 2). Preserve every primary-source quote.
9a. **Three-point central message (binding for all 108 emails)**: every email must hit these three points clearly and directly:
   1. **PDPC hid the filter on their website** instead of addressing the underlying issues. PDPC redesigned their enforcement-decisions page so that it is no longer possible to filter published cases by the type of obligation breached. The previous filter exposed the zero-Access-Obligation-breach pattern; the new layout hides it.
   2. **The Maradona / Hand-of-God analogy** (Tier 1 and Tier 2; dropped in Tier 3 only). Referee PDPC was asked to review the play; denied every request to look at the evidence; let the goal stand. Today's game has VAR — still the referee looked away. The enforcer sits in judgement of itself. Nothing happens.
   3. **The zero-Access-Obligation-investigation statistic**. Across PDPC's entire published enforcement record, PDPC has never once found a breach of the Access Obligation (s.21 PDPA). The site at https://pdpaaccessrights.sg/enforcement-index.html documents this. Parallel: PDPC aggressively enforces the Protection Obligation (s.24) against data leaks (e.g. Marina Bay Sands); it has never enforced the Access Obligation.

   **Writing discipline**: state each point directly in 1–2 sentences. Do not bury the points in personal-history prose. The personal narrative ("I still do not know what happened to me on the night of the accident") is allowed as brief context but should not displace the three points — place it as a one-sentence opening, not as a lead-in.

10. **Tier 1C disclosure (3 emails only)** — three required elements, placed AFTER sign-off as a final paragraph:
    - (a) Acknowledge relationship in one sentence.
    - (b) State explicitly that the case stands on its own merits.
    - (c) Affirm no special treatment is asked.
11. **No email body may start with anything other than "Dear [Full Name],"**. No first-name-only greetings except in Tier 1C where the relationship warrants informality (use first name only for the 3 personal-relationship recipients; use full name for all others).
12. **Subject line policy**:
    - Tier 1, Tier 2: `Follow-up on the PDPC grievance, an update and a request for your attention`
    - Tier 3: `Follow-up on my PDPC complaint, an update and a request for your attention`
    - Tier 1C: may use the recipient's first name (`Kenneth,`) followed by the standard subject to flag personal-relationship status. Keep subject within 80 chars.

**Source matrix (binding, applies to all emails — never invent quotes beyond these):**
- PDPC's email to the Complainant (s.22A preservation gap): in `evidence/correspondence-no-data-no-breach.html` — verifiable verbatim.
- Written Answer 19596 (Minister Josephine Teo, 9 Sep 2025): https://sprs.parl.gov.sg/search/#/sprs3topic?reportid=written-answer-19596
- MCST 3615 (DP-2405-C2445): `PDPC Rulings/Summary of Commission's Findings - MCST 3615 DP-2405-C2445.pdf`
- MCST 4599 (DP-2405-C2318): `PDPC Rulings/Decision MCST 4599 DP-2405-C2318.pdf`
- PDPC's officer Ahmad Syakir emails: `evidence/email-from-ahmad.html`
- PDPC guideline inconsistency: `evidence/correspondence-pdpc-guideline-inconsistency.html`
- Statute sections: https://sso.agc.gov.sg/Act/PDPA2012 (s.21, s.22A, s.24, s.25, s.4(2), s.4(3), s.2(1), s.3)
- Site link (for both URLs and Marinabay Sands / clarity-test references): https://pdpaaccessrights.sg

---

## Task A: Trim base draft to ~250 words

**Files:**
- Create: `docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md`

**Consumes:** `docs/superpowers/plans/2026-07-02-mp-followup-email-draft.md` (the ~400-word source).

**Produces:** The trimmed base draft, ~250 words. This becomes the source from which all 108 emails are derived.

- [ ] **Step 1: Read the source draft**

Run: `wc -w docs/superpowers/plans/2026-07-02-mp-followup-email-draft.md`
Expected: ~400 words (range: 390–420).

- [ ] **Step 2: Write the trimmed base draft**

Create `docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md` with the content from the original draft, with these edits:

- **Keep**: greeting placeholder `[MP name]` (Tier 3 will substitute); the update on PDPC's filter removal and the rebuilt enforcement index; the link to https://pdpaaccessrights.sg; the chart reference (BreachBreakdown.jpg attachment is **dropped** — too many attachments may flag the email); the personal-data limb (b) argument; the Advisory Guidelines page 42 quote (para 4.59); the World Cup / Maradona analogy (kept for Tier 1 and Tier 2 only — remove from this base file; Tier 3 drafter must not include it; Tier 1/2 drafters re-add it after copying the body).
- **Drop**: the "I sent PDPC and IMDA the new website on 21 June 2026" paragraph (sent 2 weeks before the email goes out — replace with a generic reference to the website existing); the verbose closing rhetorical question paragraph (replace with a single closing question template).
- **Trim**: paragraphs that restate the same point in different words (especially the "regulator sits in judgment of itself" paragraph — keep one version only).

Target: 250 words ±10. Count with `wc -w`.

- [ ] **Step 3: Verify no em-dashes, no straight quotes in words**

Run:
```bash
grep -c '—' docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md
grep -cE "[a-z]'[a-z]" docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md
grep -cE "[a-z]\"[a-z]" docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md
```

Expected: all three return `0`. Fix any matches inline.

- [ ] **Step 4: Verify word count**

Run: `wc -w docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md`
Expected: 240–260 words.

- [ ] **Step 5: Verify every primary-source quote is in `evidence/` or on a verifiable URL**

Manual check: each quoted phrase in the trimmed draft must be either:
- verbatim from `evidence/letter-to-parliament.html` / `evidence/final-email-to-parliament.html` / `evidence/correspondence-no-data-no-breach.html` / `evidence/correspondence-pdpc-guideline-inconsistency.html`, OR
- a direct citation of PDPA section text (s.21, s.22A, etc.) that can be verified at https://sso.agc.gov.sg/Act/PDPA2012, OR
- a URL reference (e.g., https://pdpaaccessrights.sg).

Document the source for each quote in the commit message.

- [ ] **Step 6: Commit**

```bash
git add docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md
git commit -m "Phase 2A: trim base draft to ~250 words"
```

---

## Task B: Draft 10 Tier 1A bespoke PAP emails

**Files:**
- Create (10 files): `data/personalised-emails/josephine-teo.md`, `lawrence-wong.md`, `lee-hsien-loong.md`, `gan-kim-yong.md`, `chan-chun-sing.md`, `k-shanmugam.md`, `edwin-tong-chun-fai.md`, `indranee-rajah.md`, `seah-kian-peng.md`, `zhulkarnain-abdul-rahim.md`

**Consumes:** `data/mp-contact-list.csv` (slugs, names, designations), `docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md` (body), `evidence/letter-to-parliament.html` (tone reference).

**Produces:** 10 .md files, one per recipient. Each ~300 words. Subject = `Follow-up on the PDPC grievance, an update and a request for your attention`. Greeting = `Dear [Full Name],`. Each has a unique opening paragraph (the bespoke hook from the matrix below) and a unique closing paragraph. The middle 2–3 paragraphs are the trimmed base draft.

**Bespoke hooks (each email's opening is built around this hook; closing ties to it):**

| File | Recipient | Opening hook | Closing hook |
|---|---|---|---|
| `josephine-teo.md` | Mrs Josephine Teo (Minister, MDDI) | Reference her Written Answer 19596 — organisations must preserve data while requests are being processed; criminal penalties for intentional concealment | Ask whether her office still stands by those statements given what is documented on the site |
| `lawrence-wong.md` | Mr Lawrence Wong (PM) | 19 months of escalation through every channel; PSC was misled by IMDA; no MP-led appeal received substantive reply | Ask whether, given this pattern, the matter warrants a direct Prime-Ministerial review |
| `lee-hsien-loong.md` | Mr Lee Hsien Loong (Senior Minister) | PDPA was enacted in 2012; the statute's plain text vs PDPC's interpretation gap | Historical perspective on the enforcement norm the PDPA was meant to set |
| `gan-kim-yong.md` | Mr Gan Kim Yong (DPM, MTI) | Senior Cabinet rank; the question is whether the regulator's posture toward the Access Obligation is institutional | DPM-level governance lens; ask whether the matter warrants Cabinet-level review |
| `chan-chun-sing.md` | Mr Chan Chun Sing (Coord. Minister, Public Services) | PSC was misled by IMDA per the Parliament letter — a Public Service process failure | As Coordinating Minister for Public Services, ask whether IMDA's representation to PSC warrants review |
| `k-shanmugam.md` | Mr K Shanmugam (Coord. Minister, National Security & Home Affairs; Law) | CCTV loophole affects public safety (footage that should be obtainable under PDPA becomes unobtainable); statutory interpretation gap on personal-data definition | As both Law and Home Affairs Minister, ask whether the Personal Data Protection Act is being read consistently with its purpose |
| `edwin-tong-chun-fai.md` | Mr Edwin Tong (Minister for Law) | PDPC's stated reason that guidelines are not determinative while using them to dismiss the Complainant's case | As Law Minister, ask whether the Law Ministry has reviewed PDPC's interpretation of personal-data sections (s.2(1)(b), s.21) |
| `indranee-rajah.md` | Mrs Indranee Rajah (Minister, PMO / Leader of the House) | Procedural: as Leader of the House, can a substantive motion or order-paper item be raised to address this gap | Procedural ask; offer to provide a one-page summary for the Order Paper if helpful |
| `seah-kian-peng.md` | Mr Seah Kian Peng (Speaker of Parliament) | Procedural ask — can a Member raise the documented regulatory interpretation gap under substantive motion procedure | Procedural only; offer to brief any MP who wishes to raise it |
| `zhulkarnain-abdul-rahim.md` | Mr Zhulkarnain Abdul Rahim (MOS, MFA & MSF) | Thank him for the parliamentary question that yielded Written Answer 19596; provide an update on what has happened since 9 Sep 2025 (his sitting date) | Ask whether he would consider a follow-up written question on the zero-Access-Obligation-breach pattern |

- [ ] **Step 1: Confirm Tier 1A recipient slugs are in the contact list**

Run:
```bash
grep -F '"josephine-teo"' data/mp-contact-list.csv
grep -F '"lawrence-wong"' data/mp-contact-list.csv
grep -F '"lee-hsien-loong"' data/mp-contact-list.csv
grep -F '"gan-kim-yong"' data/mp-contact-list.csv
grep -F '"chan-chun-sing"' data/mp-contact-list.csv
grep -F '"k-shanmugam"' data/mp-contact-list.csv
grep -F '"edwin-tong-chun-fai"' data/mp-contact-list.csv
grep -F '"indranee-rajah"' data/mp-contact-list.csv
grep -F '"seah-kian-peng"' data/mp-contact-list.csv
grep -F '"zhulkarnain-abdul-rahim"' data/mp-contact-list.csv
```

Expected: each returns one row.

- [ ] **Step 2: Draft each of the 10 .md files**

For each file in the table above, create `data/personalised-emails/{slug}.md` with:

```markdown
---
tier: 1
name: [Full Name from contact-list]
slug: [slug]
email: [primary email]
designation: [role from contact-list]
subject: Follow-up on the PDPC grievance, an update and a request for your attention
---

Dear [Full Name],

[Bespoke opening paragraph — 60-90 words — built from the hook above]

[2-3 paragraphs from the trimmed base draft — verbatim from `docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md`, with the Maradona/Hand-of-God analogy re-added in this Tier-1 email]

[Bespoke closing question — 30-50 words — built from the closing hook above]

Yours sincerely,
Lim Zirui (Ray Lim)
SMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, Ministry of Health, Covid period.
```

Tone reference: read `evidence/letter-to-parliament.html` (entire file) before drafting the first email. Match its register.

Each file MUST be unique. Do not copy-paste openings or closings between recipients.

- [ ] **Step 3: Per-file verification (run after each .md is written)**

For each file:
```bash
wc -w data/personalised-emails/{slug}.md
grep -c '—' data/personalised-emails/{slug}.md
grep -cE "[a-z]'[a-z]" data/personalised-emails/{slug}.md
grep -cE "[a-z]\"[a-z]" data/personalised-emails/{slug}.md
grep -F 'GCW' data/personalised-emails/{slug}.md
grep -F 'motorcycle' data/personalised-emails/{slug}.md
grep -F 'Ray Lim' data/personalised-emails/{slug}.md
```

Expected: word count 290-310; all `grep -c` return 0; all `grep -F` return no output. The `Ray Lim` check is intentional — only "Lim Zirui (Ray Lim)" appears in the signature line, not the body. Verify each match is in the signature line only.

- [ ] **Step 4: Verify each file's opening is unique**

Run:
```bash
for f in data/personalised-emails/josephine-teo.md data/personalised-emails/lawrence-wong.md data/personalised-emails/lee-hsien-loong.md data/personalised-emensions/gan-kim-yong.md data/personalised-emails/chan-chun-sing.md data/personalised-emails/k-shanmugam.md data/personalised-emails/edwin-tong-chun-fai.md data/personalised-emails/indranee-rajah.md data/personalised-emails/seah-kian-peng.md data/personalised-emails/zhulkarnain-abdul-rahim.md; do
  echo "=== $f ==="
  awk '/^Dear /{found=1} found{print; if(/Yours sincerely/) exit}' "$f"
done
```

Expected: 10 distinct opening paragraphs. If two files share an opening, the second one is wrong — revise.

- [ ] **Step 5: Commit**

```bash
git add data/personalised-emails/josephine-teo.md data/personalised-emails/lawrence-wong.md data/personalised-emails/lee-hsien-loong.md data/personalised-emails/gan-kim-yong.md data/personalised-emails/chan-chun-sing.md data/personalised-emails/k-shanmugam.md data/personalised-emails/edwin-tong-chun-fai.md data/personalised-emails/indranee-rajah.md data/personalised-emails/seah-kian-peng.md data/personalised-emails/zhulkarnain-abdul-rahim.md
git commit -m "Phase 2B: Tier 1A — 10 bespoke PAP senior Minister emails"
```

---

## Task C: Draft 12 Tier 1B bespoke WP emails

**Files:**
- Create (12 files): for every MP with `party_affliation == "Workers' Party"` in `data/mp-contact-list.csv`, create `data/personalised-emails/{slug}.md`. Slugs pulled deterministically:
  - `abdul-muhaimin-bin-abdul-malik` (Abdul Muhaimin Abdul Malik, Sengkang GRC)
  - `chua-kheng-wee-louis` (Chua Kheng Wee Louis, Sengkang GRC — note: verify slug matches CSV exactly)
  - `eileen-chong-pei-shan` (Eileen Chong Pei Shan, NCMP)
  - `andre-low-wu-yang` (Andre Low Wu Yang, NCMP, Sengkang)
  - `fadli-fawzi` (Muhammad Fadli bin Mohammed Fawzi, Aljunied GRC)
  - `kenneth-tiong-boon-kiat` (Kenneth Tiong Boon Kiat, Aljunied GRC)
  - `mariam-jaafar` (Mariam Jaafar, Sembawang GRC)
  - `pritam-singh` (Pritam Singh, Sengkang GRC)
  - `sylvia-lim` (Sylvia Lim, Aljunied GRC)
  - plus 3 more: query the contact list with `awk -F'","' '$5=="Workers'\'' Party"{print $2}' data/mp-contact-list.csv` to confirm the full WP list.

**Consumes:** Same as Task B. WP MPs are natural legislative allies; tone is collaborative and respectful, but the body (substantive content) is identical to other Tier 1 emails.

**Produces:** 12 .md files, ~300 words each. Subject = `Follow-up on the PDPC grievance, an update and a request for your attention`. Greeting = `Dear [Full Name],` (full name, not first name — these are not personal contacts).

- [ ] **Step 1: Get the canonical WP list**

Run: `awk -F'","' '$5 ~ /Workers/ {print $1, $2, $4, $5}' data/mp-contact-list.csv | sed 's/"//g'`
Expected: 12 rows. If not 12, halt and report the count — the spec assumes 12; if reality differs, update the spec.

- [ ] **Step 2: Draft each of the 12 .md files**

For each WP MP, create `data/personalised-emails/{slug}.md`:

```markdown
---
tier: 1
name: [Full Name from contact-list]
slug: [slug]
email: [primary email]
designation: [role from contact-list]
subject: Follow-up on the PDPC grievance, an update and a request for your attention
---

Dear [Full Name],

[Bespoke opening paragraph — 60-90 words — WP-flavored: acknowledge the WP bloc's engagement on PDPA / civil-liberties issues; reference the recipient's specific public record if known; frame the ask as procedural / legislative, not adversarial]

[2-3 paragraphs from the trimmed base draft — verbatim from `docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md`, with the Maradona/Hand-of-God analogy re-added in this Tier-1 email]

[Closing question — 30-50 words — what the WP MP can do procedurally (raise in Parliament, file a substantive motion, question in Committee of Supply, etc.)]

Yours sincerely,
Lim Zirui (Ray Lim)
SMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, Ministry of Health, Covid period.
```

Each WP opening should be distinct. Suggested hooks:
- Pritam Singh (WP chief): thank him as the senior opposition voice; reference any prior WP questions on PDPA if known.
- Sylvia Lim (WP chair): acknowledge her long record on civil liberties / administrative law.
- Senior WP MPs (Jamus Jerome Lim, Dennis Tan, others as identified): reference their public-record statements if any exist.
- Newer WP MPs (Fadli Fawzi, Kenneth Tiong, Mariam Jaafar, Andre Low NCMP, Eileen Chong NCMP, Louis Chua, Abdul Muhaimin): personalised variant focusing on their background and why this case fits their advocacy areas. Use information from `data/mp-contact-list.csv` only (name, role, constituency, party). Do not invent biographical facts.

- [ ] **Step 3: Per-file verification**

Same checks as Task B Step 3 — `wc -w`, no em-dashes, no straight quotes in words, no criminal/civil case references, no "Ray Lim" outside signature.

- [ ] **Step 4: Verify each WP opening is unique**

Run:
```bash
for f in data/personalised-emails/abdul-muhaimin-bin-abdul-malik.md data/personalised-emails/chua-kheng-wee-louis.md data/personalised-emails/eileen-chong-pei-shan.md data/personalised-emails/andre-low-wu-yang.md data/personalised-emails/fadli-fawzi.md data/personalised-emails/kenneth-tiong-boon-kiat.md data/personalised-emails/mariam-jaafar.md data/personalised-emails/pritam-singh.md data/personalised-emails/sylvia-lim.md; do
  awk '/^Dear /{found=1} found{print; if(/Yours sincerely/) exit}' "$f"
done
```

Expected: 9 distinct opening paragraphs (the 12 WP files minus 3 not yet listed; verify each is distinct).

- [ ] **Step 5: Commit**

```bash
git add data/personalised-emails/$(awk -F'","' '$5 ~ /Workers/ {gsub(/"/,"",$2); print $2".md"}' data/mp-contact-list.csv | tr '\n' ' ')
git commit -m "Phase 2B: Tier 1B — 12 bespoke Workers' Party MP emails"
```

---

## Task D: Draft 3 Tier 1C personal-relationship emails

**Files:**
- Create (3 files): `data/personalised-emails/kenneth-goh.md`, `data/personalised-emails/dinesh-vasu-dash.md`, `data/personalised-emails/cai-yinzhou.md`

**Consumes:** Same as Tasks B and C, plus the Tier 1C disclosure policy in the spec.

**Produces:** 3 .md files, ~300 words each. Subject line MAY use first-name flag per Global Constraint #12. Greeting uses first name only (the relationship warrants informality): `Dear Kenneth,` / `Dear Dinesh,` / `Dear Yinzhou,`. Each file has the **disclosure paragraph at the END, after the sign-off** (NOT in the opening).

- [ ] **Step 1: Confirm the 3 recipients and their relationships**

| Recipient | Relationship | Disclosure tone |
|---|---|---|
| Mr Kenneth Goh (NMP) | The Complainant's SMU professor during his MBA | Academic / collegial |
| Mr Dinesh Vasu Dash (Minister of State, MDDI & MOH) | The Complainant's group director at MOH during Covid | Professional / first-hand observer |
| Mr Cai Yinzhou (MP, Bishan-Toa Payoh GRC) | Friend since youth | Personal / direct |

- [ ] **Step 2: Draft each of the 3 .md files**

For each, create `data/personalised-emails/{slug}.md`:

```markdown
---
tier: 1
name: [Full Name]
slug: [slug]
email: [primary email]
designation: [role]
subject: [recipient first name, e.g. "Kenneth — follow-up on the PDPC grievance"]
---

Dear [First Name],

[Bespoke opening paragraph — case-focused, no relationship mention, ~60-90 words]

[2-3 paragraphs from the trimmed base draft — verbatim, with Maradona/Hand-of-God analogy re-added]

[Closing question — what they can do, ~30-50 words]

Yours sincerely,
Lim Zirui (Ray Lim)
SMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, Ministry of Health, Covid period.

---

[Disclosure paragraph — 3-4 sentences, must contain all three required elements:]

(a) Acknowledge the relationship in one sentence. Use the exact phrasing:
    - Kenneth Goh: "You were my SMU professor during my MBA."
    - Dinesh Vasu Dash: "You were my group director at MOH when I served there during Covid."
    - Cai Yinzhou: "We've known each other since youth."

(b) State explicitly that the case stands on its own merits. Suggested wording (drafter may refine):
    "I am writing not as a favour, but because the documentary record supports the case and you can verify each claim against the primary sources you know how to read."

(c) Affirm no special treatment is asked. Suggested wording (drafter may refine):
    "I want nothing from this email that the public record does not warrant. If the case did not hold on the documents, I would not be writing."

[Optional warmth gradient line — appropriate to relationship, drafter composes]
```

- [ ] **Step 3: Per-file verification (Tier 1C checks are stricter)**

For each file, run:
```bash
wc -w data/personalised-emails/{slug}.md
grep -c '—' data/personalised-emails/{slug}.md
grep -cE "[a-z]'[a-z]" data/personalised-emails/{slug}.md
grep -cE "[a-z]\"[a-z]" data/personalised-emails/{slug}.md
grep -F 'GCW' data/personalised-emails/{slug}.md
grep -F 'motorcycle' data/personalised-emails/{slug}.md
grep -F 'Ray Lim' data/personalised-emails/{slug}.md
```

Expected: word count 290-310; all `grep -c` return 0; no criminal references; "Ray Lim" appears only in the signature line.

- [ ] **Step 4: Verify disclosure paragraph is at the END (after sign-off)**

For each file:
```bash
grep -n "You were\|We've known" data/personalised-emails/{slug}.md
grep -n "Yours sincerely" data/personalised-emails/{slug}.md
```

Expected: disclosure line is on a line number GREATER than the sign-off line.

- [ ] **Step 5: Verify the 3 required elements are present**

For each file:
```bash
grep -c "favour\|favor" data/personalised-emails/{slug}.md     # element (b) key word
grep -c "public record\|public-record" data/personalised-emails/{slug}.md   # element (b)
grep -c "special treatment\|nothing from\|did not hold" data/personalised-emails/{slug}.md   # element (c)
```

Expected: all return ≥1. If any return 0, the disclosure paragraph is incomplete.

- [ ] **Step 6: Commit**

```bash
git add data/personalised-emails/kenneth-goh.md data/personalised-emails/dinesh-vasu-dash.md data/personalised-emails/cai-yinzhou.md
git commit -m "Phase 2B: Tier 1C — 3 personal-relationship emails with closing disclosure"
```

---

## Task E: Tier 2 templates + ~28 emails

**Files:**
- Create: `docs/superpowers/plans/2026-07-02-mp-email-tier2-templates.md` — the 3 templates
- Create (28 files): `data/personalised-emails/{slug}.md` for each Tier 2 recipient

**Tier 2 recipient slugs (defined as: every MP not in Tier 1A, 1B, or 1C, AND whose `designation` matches one of the role-template patterns below):**

```
MDDI SMS/MOS tier (excluding Dinesh Vasu Dash, who is Tier 1C):
  - jasmin-lau
  - rahayu-mahzam
  - tan-kiat-how

Coordinating Minister rank:
  - ong-ye-kung

Other Senior Ministers of State (~5):
  - masagos-zulkifli-bin-masagos-mohamad
  - grace-fu-hai-yien
  - chee-hong-tat (if Senior Minister of State; verify against CSV)
  - (others from CSV where role starts with "Senior Minister of State")

Other Ministers of State (~10):
  - muhammad-faishal-ibrahim (Acting Minister-in-charge of Muslim Affairs; qualifies)
  - david-neo (Acting Minister; qualifies)
  - denise-phua-lay-peng (if Minister of State; verify)
  - (others from CSV where role contains "Minister of State" but not "Senior Minister of State" and not "Acting")

Deputy Speaker:
  - christopher-de-souza
  - (any other from CSV whose role contains "Deputy Speaker")

Mayors (excluding Alex Yam who is in... actually let me note: I previously did not include mayors in Tier 1A or 1B):
  - alex-yam-ziming (Mayor, North West District)

NMPs with relevant expertise (excluding Kenneth Goh who is Tier 1C):
  - kuah-boon-theng (Senior Counsel)
```

**Consumes:** `data/mp-contact-list.csv` (filtering by designation pattern), `docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md` (body), evidence/letter-to-parliament.html (tone).

**Produces:** 1 templates file + 28 .md emails.

- [ ] **Step 1: Generate the canonical Tier 2 recipient list**

Run: `awk -F'","' '!/Tier 1/ && /Minister of State|Senior Minister|Coordinating Minister|Deputy Speaker|Mayor|Senior Counsel|Nominated/{print $2, $3, $4, $5, $6}' data/mp-contact-list.csv`
Expected: ~28 rows. Verify against the spec list above. Adjust if reality differs from spec; update the spec if so.

- [ ] **Step 2: Write the 3 templates**

Create `docs/superpowers/plans/2026-07-02-mp-email-tier2-templates.md` containing 3 templates, each with `[RECIPIENT_NAME]`, `[RECIPIENT_DESIGNATION]`, `[RECIPIENT_CONSTITUENCY]`, `[RECIPIENT_PARTY]` placeholders:

**Template T2-A — MDDI SMS/MOS (3 recipients)**
Opening references the recipient's role in the MDDI portfolio; acknowledges the link to PDPC oversight; closes by asking for a direct statement of the MDDI's enforcement posture.

**Template T2-B — Coordinating Minister / Senior Cabinet rank (1+ recipient)**
Opening references the senior Cabinet rank; closes by asking for a Cabinet-level review of the pattern.

**Template T2-C — Other Ministers of State / NMPs / Deputy Speaker / Mayors (~24 recipients)**
Opening references the recipient's role in parliamentary procedure or civic leadership; closes by asking for whatever procedural / civic action is in the recipient's remit.

Each template structure:
```
Dear [RECIPIENT_NAME],

[Opening paragraph — 1 sentence of context + 1 sentence of role reference]

[2-3 paragraphs from the trimmed base draft, with Maradona/Hand-of-God analogy re-added]

[Closing question — what they can do]

Yours sincerely,
Lim Zirui (Ray Lim)
SMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, Ministry of Health, Covid period.
```

Target length per template: ~250 words when filled in.

- [ ] **Step 3: Per-template verification**

For each template:
```bash
wc -w docs/superpowers/plans/2026-07-02-mp-email-tier2-templates.md
grep -c '—' docs/superpowers/plans/2026-07-02-mp-email-tier2-templates.md
grep -cE "[a-z]'[a-z]" docs/superpowers/plans/2026-07-02-mp-email-tier2-templates.md
grep -cE "[a-z]\"[a-z]" docs/superpowers/plans/2026-07-02-mp-email-tier2-templates.md
```

Expected: word count 700-900 (3 templates); all `grep -c` return 0.

- [ ] **Step 4: Commit templates**

```bash
git add docs/superpowers/plans/2026-07-02-mp-email-tier2-templates.md
git commit -m "Phase 2C: Tier 2 — 3 role-templated templates"
```

- [ ] **Step 5: Generate the 28 Tier 2 emails by filling in the templates**

For each Tier 2 recipient, create `data/personalised-emails/{slug}.md` by filling in the appropriate template's placeholders with values from `data/mp-contact-list.csv`.

For each generated file, run per-file verification:
```bash
wc -w data/personalised-emails/{slug}.md
grep -c '—' data/personalised-emails/{slug}.md
grep -cE "[a-z]'[a-z]" data/personalised-emails/{slug}.md
grep -cE "[a-z]\"[a-z]" data/personalised-emails/{slug}.md
grep -F 'GCW' data/personalised-emails/{slug}.md
grep -F 'motorcycle' data/personalised-emails/{slug}.md
grep -F 'Ray Lim' data/personalised-emails/{slug}.md
```

Expected: word count 240-260; all `grep -c` return 0; no criminal references; "Ray Lim" only in signature.

- [ ] **Step 6: Commit Tier 2 emails**

```bash
git add data/personalised-emails/<tier-2-slugs>.md
git commit -m "Phase 2C: Tier 2 — 28 role-templated emails"
```

---

## Task F: Tier 3 base-draft substitution (~55 emails)

**Files:**
- Create (~55 files): `data/personalised-emails/{slug}.md` for each Tier 3 recipient.

**Tier 3 recipient definition (deterministic)**: every MP in `data/mp-contact-list.csv` whose slug does NOT appear in any of:
- Tier 1A list (10 slugs)
- Tier 1B list (12 WP slugs)
- Tier 1C list (3 slugs)
- Tier 2 list (~28 slugs)

**Consumes:** `docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md` (body), `data/mp-contact-list.csv` (names).

**Produces:** ~55 .md files, ~250 words each. Subject = `Follow-up on my PDPC complaint, an update and a request for your attention`. Greeting = `Dear [Full Name],`. NO Maradona/Hand-of-God analogy (per Global Constraint #9). Body = trimmed base draft verbatim. Closing = the closing question from the base draft.

- [ ] **Step 1: Generate the canonical Tier 3 recipient list**

```bash
# Find all Tier 1 + Tier 2 slugs from existing files
ls data/personalised-emails/ | sed 's/.md$//' | sort -u > /tmp/tier12-slugs.txt
# Tier 3 = every slug in contact-list NOT in tier12-slugs.txt
awk -F'","' 'NR>1 {slug=$2; gsub(/"/,"",slug); if (slug != "") print slug}' data/mp-contact-list.csv | sort -u > /tmp/all-slugs.txt
comm -23 /tmp/all-slugs.txt /tmp/tier12-slugs.txt > /tmp/tier3-slugs.txt
wc -l /tmp/tier3-slugs.txt
cat /tmp/tier3-slugs.txt
```

Expected: ~55 lines. If count differs from spec, halt and report.

- [ ] **Step 2: Generate each Tier 3 .md file**

For each slug in `/tmp/tier3-slugs.txt`:

```markdown
---
tier: 3
name: [Full Name from CSV — column 1]
slug: [slug]
email: [primary email from CSV]
designation: [designation from CSV]
subject: Follow-up on my PDPC complaint, an update and a request for your attention
---

Dear [Full Name],

[Body paragraphs — VERBATIM from the trimmed base draft, but with the "Dear [MP name]," line replaced by the recipient's full name, and the Maradona/Hand-of-God paragraph REMOVED. The rest of the base draft applies as-is.]

Yours sincerely,
Lim Zirui (Ray Lim)
SMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, Ministry of Health, Covid period.
```

For batch generation, the drafter may write a small Node.js script that reads `/tmp/tier3-slugs.txt`, looks up each in `data/mp-contact-list.csv`, and writes the .md file. The script:
- Reads CSV row by row
- For each Tier 3 slug, constructs the .md content
- Writes to `data/personalised-emails/{slug}.md`

Suggested Node script (use only as starting point; verify outputs):

```javascript
import fs from 'node:fs';
import path from 'node:path';

const tier3Slugs = fs.readFileSync('/tmp/tier3-slugs.txt', 'utf8').trim().split('\n');
const tier3Set = new Set(tier3Slugs);

const baseDraft = fs.readFileSync('docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md', 'utf8');
// Extract body paragraphs (everything between "Dear [MP name]," and "Yours sincerely,")
const bodyMatch = baseDraft.match(/Dear \[MP name\],\n\n([\s\S]+?)\n\nYours sincerely,/);
const body = bodyMatch ? bodyMatch[1] : '';
// Remove Maradona/Hand-of-God paragraph (the World Cup paragraph)
const bodyNoMaradona = body.split('\n\n').filter(p => !p.includes('World Cup') && !p.includes('Hand of God')).join('\n\n');

const csvText = fs.readFileSync('data/mp-contact-list.csv', 'utf8');
const rows = csvText.trim().split('\n').slice(1); // skip header
const records = rows.map(line => {
  const cols = line.match(/("([^"]|"")*"|[^,]+)/g) || [];
  return {
    name: cols[0]?.replace(/^"|"$/g, '').replace(/""/g, '"'),
    slug: cols[1]?.replace(/^"|"$/g, ''),
    role: cols[2]?.replace(/^"|"$/g, ''),
    constituency: cols[3]?.replace(/^"|"$/g, ''),
    party: cols[4]?.replace(/^"|"$/g, ''),
    email: cols[5]?.replace(/^"|"$/g, ''),
  };
});

for (const rec of records) {
  if (!tier3Set.has(rec.slug)) continue;
  const body = `Dear ${rec.name},\n\n${bodyNoMaradona}\n\nYours sincerely,\nLim Zirui (Ray Lim)\nSMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, Ministry of Health, Covid period.`;
  const content = `---
tier: 3
name: ${rec.name}
slug: ${rec.slug}
email: ${rec.email}
designation: ${rec.role}
subject: Follow-up on my PDPC complaint, an update and a request for your attention
---

${body}
`;
  fs.writeFileSync(path.join('data/personalised-emails', `${rec.slug}.md`), content, 'utf8');
}
console.log('Tier 3 generated: ' + tier3Slugs.length);
```

Drafter runs this script from `pdpc-grievance-site/` (so paths resolve correctly).

- [ ] **Step 3: Per-file verification (sample 5 random Tier 3 files)**

For each sampled file:
```bash
wc -w data/personalised-emails/{slug}.md
grep -c '—' data/personalised-emails/{slug}.md
grep -cE "[a-z]'[a-z]" data/personalised-emails/{slug}.md
grep -cE "[a-z]\"[a-z]" data/personalised-emails/{slug}.md
grep -F 'GCW' data/personalised-emails/{slug}.md
grep -F 'motorcycle' data/personalised-emails/{slug}.md
grep -F 'Ray Lim' data/personalised-emails/{slug}.md
grep -F 'World Cup' data/personalised-emails/{slug}.md    # MUST be 0 — Maradona dropped in Tier 3
grep -F 'Hand of God' data/personalised-emails/{slug}.md  # MUST be 0
```

Expected: word count 240-260; no em-dashes; no straight quotes in words; no criminal references; "Ray Lim" only in signature; no Maradona/Hand-of-God references.

- [ ] **Step 4: Bulk verification (all Tier 3 files)**

Run:
```bash
for f in data/personalised-emails/*.md; do
  slug=$(basename "$f" .md)
  if grep -q "$slug" /tmp/tier3-slugs.txt 2>/dev/null; then
    issues=""
    [ "$(wc -w < "$f")" -lt 240 ] || [ "$(wc -w < "$f")" -gt 260 ] && issues="$issues wc"
    grep -q '—' "$f" && issues="$issues emdash"
    grep -qE "[a-z]'[a-z]" "$f" && issues="$issues apos"
    grep -qE "[a-z]\"[a-z]" "$f" && issues="$issues quote"
    grep -q 'World Cup\|Hand of God' "$f" && issues="$issues maradona"
    grep -q 'GCW\|motorcycle' "$f" && issues="$issues case"
    [ -n "$issues" ] && echo "$slug: $issues"
  fi
done
```

Expected: no output (all Tier 3 files pass).

- [ ] **Step 5: Commit**

```bash
git add data/personalised-emails/<tier-3-slugs>.md
git commit -m "Phase 2D: Tier 3 — ~55 base-draft emails with name substitution"
```

---

## Task G: Master CSV

**Files:**
- Create: `data/personalised-emails.csv`

**Consumes:** All 108 .md files in `data/personalised-emails/`, `data/mp-contact-list.csv`.

**Produces:** A CSV with 109 lines (header + 108 rows), mail-merge ready. Columns: `tier,name,slug,email,subject,body`.

- [ ] **Step 1: Write the CSV generation script**

Create a small Node script (or Python) that:
- Reads `data/mp-contact-list.csv` (for canonical name/email).
- Walks `data/personalised-emails/*.md`.
- For each .md file:
  - Parses frontmatter for `tier`, `name`, `slug`, `email`, `subject`.
  - Extracts the body (everything after the closing `---` of the frontmatter).
- Writes `data/personalised-emails.csv` with columns: `tier,name,slug,email,subject,body`.
- The `body` column contains the full email body as plain text with `\n` newlines preserved.

Suggested Node.js approach (one-shot, not committed):

```javascript
import fs from 'node:fs';
import path from 'node:path';

const csvEscape = (s) => `"${(s ?? '').toString().replace(/"/g, '""')}"`;

const files = fs.readdirSync('data/personalised-emails').filter(f => f.endsWith('.md')).sort();
const rows = [];
for (const f of files) {
  const content = fs.readFileSync(path.join('data/personalised-emails', f), 'utf8');
  const fmMatch = content.match(/^---\n([\s\S]+?)\n---\n([\s\S]+)$/);
  if (!fmMatch) { console.error('No frontmatter:', f); continue; }
  const fm = {};
  for (const line of fmMatch[1].split('\n')) {
    const m = line.match(/^(\w+):\s*(.*)$/);
    if (m) fm[m[1]] = m[2].trim();
  }
  const body = fmMatch[2].trim();
  rows.push([fm.tier, fm.name, fm.slug, fm.email, fm.subject, body]);
}

const header = ['tier', 'name', 'slug', 'email', 'subject', 'body'].join(',');
const out = [header, ...rows.map(r => r.map(csvEscape).join(','))].join('\n');
fs.writeFileSync('data/personalised-emails.csv', out + '\n', 'utf8');
console.log('CSV rows: ' + rows.length);
```

- [ ] **Step 2: Run the script and verify CSV**

Run the script. Expected output: `CSV rows: 108`.

Verify:
```bash
wc -l data/personalised-emails.csv   # Expected: 109
head -1 data/personalised-emails.csv # Expected: tier,name,slug,email,subject,body
head -2 data/personalised-emails.csv | tail -1 | awk -F'","' '{print NF}'   # Expected: 6 columns
```

- [ ] **Step 3: Spot-check 3 random rows**

Pick 3 random recipients, open their row in the CSV, and compare the `body` column to their .md file. They must match exactly.

- [ ] **Step 4: Commit**

```bash
git add data/personalised-emails.csv
git commit -m "Phase 2E: master mail-merge CSV (108 rows)"
```

---

## Task H: INDEX.md

**Files:**
- Create: `data/personalised-emails-INDEX.md`

**Consumes:** `data/mp-contact-list.csv` and all 108 .md frontmatter.

**Produces:** A single review index, grouped by tier, with one-line note per recipient describing the personalisation hook.

- [ ] **Step 1: Draft INDEX.md**

Structure:
```markdown
# Personalised MP Emails — Review Index

Generated: [date]
Total: 108 emails across 3 tiers.

## Tier 1 — bespoke (25)

### A. PAP Ministers
- **Mrs Josephine Teo** (`josephine-teo`, MDDI) — references Written Answer 19596; asks if her office still stands by it
- **Mr Zhulkarnain Abdul Rahim** (`zhulkarnain-abdul-rahim`, MOS) — thank-you + update on outcome of his PQ
... (10 rows)

### B. WP MPs (12)
- **Mr Pritam Singh** (`pritam-singh`, WP chief) — collaborative framing; references prior WP PQ on PDPA
... (12 rows)

### C. Personal-relationship (3)
- **Mr Kenneth Goh** (`kenneth-goh`, NMP) — SMU professor during MBA; relationship disclosure + case-stands-on-merits
- **Mr Dinesh Vasu Dash** (`dinesh-vasu-dash`, MOS) — MOH group director during Covid; relationship disclosure + case-stands-on-merits
- **Mr Cai Yinzhou** (`cai-yinzhou`, PAP backbencher) — friend since youth; relationship disclosure + case-stands-on-merits

## Tier 2 — role-templated (~28)

- **Ms Jasmin Lau** (`jasmin-lau`, MDDI MOS) — MDDI PDPC-oversight variant
... (~28 rows)

## Tier 3 — base-draft (~55)

- **Mr [name]** (`slug`, [constituency], [party]) — base draft with name substituted
... (~55 rows)
```

- [ ] **Step 2: Verify counts**

Verify the row counts in INDEX.md match the actual file counts:
- Tier 1A: 10
- Tier 1B: 12
- Tier 1C: 3
- Tier 2: ~28
- Tier 3: ~55
- Total: 108

Run: `ls data/personalised-emails/*.md | wc -l`
Expected: 108.

- [ ] **Step 3: Commit**

```bash
git add data/personalised-emails-INDEX.md
git commit -m "Phase 2E: review index for all 108 personalised emails"
```

---

## Task I: Quality gate + final commit

**Files:** (reads all)

**Produces:** A single commit verifying all 108 emails pass the quality checks.

- [ ] **Step 1: Bulk em-dash check across all 108 files**

```bash
grep -l '—' data/personalised-emails/*.md
```

Expected: no output.

- [ ] **Step 2: Bulk straight-quote-in-word check**

```bash
grep -lE "[a-z]'[a-z]" data/personalised-emails/*.md
grep -lE "[a-z]\"[a-z]" data/personalised-emails/*.md
```

Expected: no output from either.

- [ ] **Step 3: Bulk criminal-case-reference check**

```bash
grep -lF 'GCW' data/personalised-emails/*.md
grep -lF 'motorcycle' data/personalised-emails/*.md
grep -lF 'taxi' data/personalised-emails/*.md
grep -lF 'Quak Chee Wah' data/personalised-emails/*.md
grep -lF 'Cairnhill Road' data/personalised-emails/*.md
```

Expected: no output from any.

- [ ] **Step 4: Verify "Ray Lim" appears only in signature lines**

```bash
for f in data/personalised-emails/*.md; do
  matches=$(grep -c 'Ray Lim' "$f")
  if [ "$matches" -gt 1 ]; then
    echo "$f: Ray Lim appears $matches times (should be 1)"
  fi
done
```

Expected: no output (each file has exactly 1 occurrence, in the signature).

- [ ] **Step 5: Verify Maradona/Hand-of-God is in Tier 1 / Tier 2 only**

```bash
# Tier 3 files must not have it
for f in data/personalised-emails/*.md; do
  tier=$(grep '^tier:' "$f" | awk '{print $2}')
  if [ "$tier" = "3" ]; then
    grep -qF 'World Cup' "$f" && echo "$f: Tier 3 contains 'World Cup'"
    grep -qF 'Hand of God' "$f" && echo "$f: Tier 3 contains 'Hand of God'"
  fi
done
```

Expected: no output.

- [ ] **Step 6: Verify all 108 .md files have a corresponding CSV row**

```bash
ls data/personalised-emails/*.md | wc -l   # Expected: 108
wc -l data/personalised-emails.csv          # Expected: 109
```

- [ ] **Step 7: Verify Tier 1C disclosure paragraphs contain all 3 required elements**

```bash
for f in data/personalised-emails/kenneth-goh.md data/personalised-emails/dinesh-vasu-dash.md data/personalised-emails/cai-yinzhou.md; do
  has_favour=$(grep -cF "favour\|favor" "$f")
  has_record=$(grep -cF "public record" "$f")
  has_special=$(grep -cF "special treatment\|nothing from\|did not hold" "$f")
  echo "$f: favour=$has_favour, record=$has_record, special=$has_special"
done
```

Expected: each shows `favour≥1, record≥1, special≥1`.

- [ ] **Step 8: Final commit (if any fixes were needed)**

```bash
git add data/personalised-emails/ data/personalised-emails.csv data/personalised-emails-INDEX.md
git commit -m "Phase 2F: quality-gate pass — all 108 emails verified"
```

If no fixes were needed, the commit can be empty (`git commit --allow-empty`).

---

## Self-Review

**1. Spec coverage:**
- Tier 1A (10 PAP bespoke) → Task B ✓
- Tier 1B (12 WP bespoke) → Task C ✓
- Tier 1C (3 personal-relationship with disclosure at end) → Task D ✓
- Tier 2 (~28 role-templated) → Task E ✓
- Tier 3 (~55 base-draft substitution) → Task F ✓
- Trim base draft to ~250 words → Task A ✓
- Outputs (CSV, INDEX) → Tasks G, H ✓
- Quality verification (grep checks) → Task I ✓
- 3 mandatory disclosure content elements → Task D Step 2 + Task I Step 7 ✓
- Maradona analogy dropped in Tier 3 → Task F Step 2 (script removes World Cup/Hand-of-God paragraph) + Task I Step 5 ✓
- No criminal/civil case references → global grep check in Task I Step 3 ✓
- "the Complainant" / "Lim Zirui" naming → Global Constraints #6 + per-file verification ✓

**2. Placeholder scan:** No "TBD" or "TODO" in the plan. Each step has concrete commands. The drafter writes the email prose (creative work), but the structure, length targets, hooks, and verification are all concrete.

**3. Type consistency:**
- File paths consistent across tasks: `data/personalised-emails/{slug}.md`, `data/personalised-emails.csv`, `data/personalised-emails-INDEX.md`.
- Frontmatter fields consistent across tasks: `tier`, `name`, `slug`, `email`, `designation`, `subject`.
- CSV columns consistent across tasks: `tier, name, slug, email, subject, body`.
- Signature block consistent: `Yours sincerely,\nLim Zirui (Ray Lim)\nSMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, Ministry of Health, Covid period.`

Plan is internally consistent. No revision needed.