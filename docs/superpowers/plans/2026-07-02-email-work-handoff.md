# Email Campaign Handoff — 2 July 2026

**Status:** Phase 2 complete. Ready for first-wave send.

---

## What was done

A personalised MP email campaign targeting Singapore's 15th-Parliament MPs and Ministers about the documented PDPC grievance. The campaign centres on the live grievance site at https://pdpaaccessrights.sg and the three central points (PDPC filter hiding, Maradona/Hand-of-God analogy, zero Access Obligation investigation statistic).

**Generated:**

- **108 personalised .md emails** in `data/personalised-emails/` — one per recipient, organised in 3 tiers.
- **`data/personalised-emails.csv`** — master mail-merge file (108 rows, 6 columns: tier, name, slug, email, subject, body).
- **`data/personalised-emails-INDEX.md`** — review index grouped by tier.
- **`data/personalised-emails/gpc-digital-development-and-information.md`** — new GPC email (added during consolidation).
- **`data/consolidated-send.csv`** — 5-row first-wave send list (MDDI portfolio + GPC).
- **`docs/superpowers/specs/2026-07-02-mp-email-personalisation-design.md`** — approved design spec.
- **`docs/superpowers/plans/2026-07-02-mp-email-personalisation-plan.md`** — implementation plan.
- **`docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md`** — trimmed base draft (the body of every email).

**Tier counts:**
- Tier 1A: 10 (PAP senior Ministers — bespoke prose)
- Tier 1B: 12 (Workers' Party MPs — bespoke prose, collaborative framing)
- Tier 1C: 3 (personal-relationship — Kenneth Goh / Dinesh Vasu Dash / Cai Yinzhou, with disclosure paragraph at end)
- Tier 2: 34 (role-templated)
- Tier 3: 49 (base-draft with name substitution, Maradona dropped)
- Total: 108

---

## First-wave campaign: 5 emails (consolidated)

User decided on 2 July 2026 to consolidate to a focused subset. The 5-email first wave targets only the MDDI portfolio plus the GPC:

| # | Recipient | Tier | Role | Email |
|---|---|---|---|---|
| 1 | Mrs Josephine Teo | 1A | Minister for Digital Development and Information | kaks.mps@pap.org.sg |
| 2 | Mr Tan Kiat How | 2 | Senior Minister of State, MDDI & MOH | Kg.Chai.Chee.MPS@pap.org.sg |
| 3 | Ms Jasmin Lau | 2 | Minister of State, MDDI & MOE | Jasmin.Lau@pap.org.sg |
| 4 | Ms Rahayu Mahzam | 2 | Minister of State, MDDI & MOH | Rahayu.Mahzam@pap.org.sg |
| 5 | GPC for Digital Development and Information | 1A-style | 7 members; **send as BCC** | (see `data/personalised-emails/gpc-digital-development-and-information.md` for the 7 addresses) |

**Send-list CSV:** `data/consolidated-send.csv` (5 rows + header).

### Send instructions

1. **Use BCC for all 5 emails.** Especially the GPC email — 7 recipients in one message.
2. **Send each email separately** (5 distinct sends). Do not bundle.
3. **Wait 2-3 days** between email #1 (Minister Teo) and email #5 (GPC). Reason: allow her office to absorb the matter before the GPC begins its inquiry.
4. **Send order recommended:**
   - Day 1: Minister Teo (lead recipient — direct portfolio responsibility)
   - Day 3-4: SMS Tan Kiat How + MOS Jasmin Lau + MOS Rahayu Mahzam (her team)
   - Day 5-7: GPC for Digital Development and Information
5. **Reply handling**: any replies are out of scope of this handoff. Handle manually in a separate workflow.

### Body sources

Each row in `consolidated-send.csv` references the corresponding `.md` body file in `data/personalised-emails/`. Read that file for the full body text and copy-paste into the email client.

For the GPC email, the body is in `data/personalised-emails/gpc-digital-development-and-information.md`. The 7 BCC addresses are listed in the frontmatter `recipients:` block AND in the `recipients-BCC` column of `consolidated-send.csv`.

---

## Reserved: 103 wider emails (second wave)

The remaining 103 emails (Tier 1A: 9 — all except Josephine Teo; Tier 1B: 12 — all WP; Tier 1C: 2 — Kenneth Goh + Cai Yinzhou; Tier 2: 31; Tier 3: 49) remain available in `data/personalised-emails/`.

The user has not decided whether to send a second wave or not. The 103 files are kept as a reserve; do not delete.

If a second wave is later approved, use the master `data/personalised-emails.csv` (108 rows). Apply BCC for every send.

**Dinesh Vasu Dash is in Tier 1C** (personal-relationship — was the user's MOH group director during Covid). He is **not** in the consolidated-send because his portfolio is MCCY & MOM, not MDDI. To include him as a 6th first-wave recipient (or in any second wave), see `data/personalised-emails/dinesh-vasu-dash.md` and use the same BCC discipline.

---

## Tone, style, and source-discipline rules (binding for any future email edit or addition)

These come from `docs/superpowers/specs/2026-07-02-mp-email-personalisation-design.md` and `CLAUDE.md` (site voice rules). Apply to any future email added to this campaign.

### Tone
- **First-person.** "I am writing..." not "the Complainant is writing...". Hero/testimony and verbatim quotes remain first-person; third-person only when referring to the documented subject in legal-context.
- **Factual, willing to be corrected.** Match the register of `evidence/letter-to-parliament.html`. Pattern: "I stand ready to be corrected" / "I do not insist that I must be right" / etc.
- **No adversarial framing.** Never use "cover-up" / "gaslight". Use "documented pattern" / "regulatory interpretation gap" / "departure from statute".

### Style
- **Curly quotes throughout.** No straight `"` or `'` in visible text. Verify with `grep -cE "[a-z]'[a-z]"` (must be 0) and `grep -cE "[a-z]\"[a-z]"` (must be 0) on each output file.
- **No em-dashes (`—`) in body prose.** Use commas, periods, parentheses, colons. En-dashes (`–`) OK only in numeric ranges. Verify with `grep -c '—'` on body prose (em-dash in YAML subject lines is allowed for Tier 1C first-name flag).
- **No fabricated quotes.** Every quote must come from one of:
  - PDPC's published correspondence (`evidence/*.html`)
  - PDPC's published rulings
  - The PDPA at https://sso.agc.gov.sg/Act/PDPA2012
  - Singapore Parliament records (https://sprs.parl.gov.sg/)
  - The live site at https://pdpaaccessrights.sg
- **No criminal/civil case references.** No "GCW.PI", "GCW.CRIM", "motorcycle", "taxi", "Quak Chee Wah", "Ray Lim" in body text. Use "Lim Zirui" in signature, "the Complainant" only when referring to the documented subject in third person.
- **"the Complainant" (capital C)** only for documented third-person reference. Never in first-person voice.

### Signature (every email)
```
Yours sincerely,
Lim Zirui (Ray Lim)
SMU MBA (Mar 2024, 4.0 GPA); Commendation Medal, Ministry of Health, Covid period.
```

### Three-point central message (binding for all 108 emails)
Every email — Tier 1, 2, and 3 — must hit these three points clearly and directly. The personalisation wraps around them; it does not displace them.

1. **PDPC hid the filter on their website** instead of addressing the underlying issues. PDPC redesigned its enforcement-decisions page so it is no longer possible to filter published cases by obligation type. The previous filter exposed the zero-Access-Obligation-breach pattern; the new layout hides it.

2. **The Maradona / Hand-of-God analogy.** Referee PDPC was asked to review the play. It denied every request to look at the evidence and let the goal stand. Today's game has VAR — and still the referee looked away. The enforcer sits in judgement of itself. Nothing happens. (Carried in Tier 1 and Tier 2; **dropped in Tier 3 only**.)

3. **The zero-Access-Obligation-investigation statistic.** Across PDPC's entire published enforcement record, PDPC has never once found a breach of the Access Obligation (s.21 PDPA). Site at https://pdpaaccessrights.sg/enforcement-index.html documents this. Parallel: PDPC aggressively enforces the Protection Obligation (s.24) against data leaks (e.g. Marina Bay Sands); it has never enforced the Access Obligation.

**Writing discipline**: each point in 1–2 sentences. Personal narrative ("I still do not know what happened to me on the night of the accident, because the footage was denied and then destroyed.") allowed as brief context (one sentence) but should not displace the three points.

### Tier 1C disclosure (only for the 3 personal-relationship emails)
Three required elements, placed **after the sign-off** as a final paragraph (not in the opening):
1. Acknowledge the relationship in one sentence (use the exact phrasing per recipient — see `data/personalised-emails/{slug}.md` for the specific phrasing used).
2. State explicitly that the case stands on its own merits.
3. Affirm no special treatment is asked.

---

## Quality gate (already passed for all 108 emails)

Verified on 2 July 2026:
- 0 em-dashes in body prose (only in YAML subject lines for Tier 1C — allowed per spec)
- 0 straight apostrophes in words
- 0 straight quotes in words
- 0 criminal-case references (GCW / motorcycle / taxi / Quak Chee Wah)
- "Ray Lim" appears exactly 1 time in each file (in the signature only)
- Maradona absent from all 49 Tier 3 files
- All 3 Tier 1C files have all 3 disclosure elements (relationship + case-stands-on-its-own + no-special-treatment)

To re-verify at any time:

```bash
cd pdpc-grievance-site

# Em-dashes in body prose only (not YAML)
for f in data/personalised-emails/*.md; do
  awk 'BEGIN{fm=0} /^---$/{fm=!fm; next} !fm{print}' "$f" | grep -q "—" && echo "BODY EM-DASH: $f"
done

# Straight quotes
grep -lE "[a-z]'[a-z]" data/personalised-emails/*.md
grep -lE "[a-z]\"[a-z]" data/personalised-emails/*.md

# Criminal refs
grep -lE "GCW|motorcycle|taxi |Quak Chee Wah" data/personalised-emails/*.md

# Tier 3 must have no Maradona
for f in data/personalised-emails/*.md; do
  tier=$(grep '^tier:' "$f" | awk '{print $2}')
  [ "$tier" = "3" ] && grep -qF 'World Cup\|Hand of God' "$f" && echo "MARADONA IN TIER 3: $f"
done
```

---

## What to do if you find a problem with an existing email

1. Identify which `.md` file has the issue. Each file is in `data/personalised-emails/{slug}.md`.
2. Identify the file's tier from the frontmatter `tier:` field (1 or 2 or 3). Tier 1 is bespoke; Tier 2 is role-templated; Tier 3 is base-draft substitution.
3. Edit the file. Re-run the quality-gate checks above.
4. Commit with a clear message: `[tier] fix: <description>` (e.g., `Tier 3 fix: replace straight apostrophe in desmond-tan-kok-ming.md`).
5. If the fix changes the body content, regenerate `data/personalised-emails.csv` (the master CSV) by running a small Node.js script:

```javascript
// regenerate-csv.js — runs from pdpc-grievance-site/
import fs from 'node:fs';
import path from 'node:path';

const csvEscape = (s) => `"${(s ?? '').toString().replace(/"/g, '""')}"`;

const files = fs.readdirSync('data/personalised-emails').filter(f => f.endsWith('.md')).sort();
const rows = [];
for (const f of files) {
  const content = fs.readFileSync(path.join('data/personalised-emails', f), 'utf8');
  const fmMatch = content.match(/^---\n([\s\S]+?)\n---\n([\s\S]+)$/);
  if (!fmMatch) continue;
  const fm = {};
  for (const line of fmMatch[1].split('\n')) {
    const m = line.match(/^(\w+):\s*(.*)$/);
    if (m) fm[m[1]] = m[2].trim();
  }
  rows.push([fm.tier, fm.name, fm.slug, fm.email, fm.subject, fmMatch[2].trim()]);
}

const header = ['tier', 'name', 'slug', 'email', 'subject', 'body'].join(',');
const out = [header, ...rows.map(r => r.map(csvEscape).join(','))].join('\n');
fs.writeFileSync('data/personalised-emails.csv', out + '\n', 'utf8');
console.log('CSV rows: ' + rows.length);
```

6. If you add new emails (e.g., a new MDDI portfolio member), follow the same frontmatter pattern. The CSV regeneration script handles new files automatically.

---

## Site links to reference

- **Live grievance site:** https://pdpaaccessrights.sg
- **Enforcement-index filter matrix** (cited in every Tier 1 / Tier 2 email): https://pdpaaccessrights.sg/enforcement-index.html
- **PDPA statute:** https://sso.agc.gov.sg/Act/PDPA2012 (sections 21, 22A, 24, 25, 4(2), 4(3), 2(1), 3)
- **Written Answer 19596** (cited in the Minister Teo email): https://sprs.parl.gov.sg/search/#/sprs3topic?reportid=written-answer-19596

---

## Open questions / pending decisions

1. **Should a second wave go out?** The 103 reserved emails are still there. The user has not decided.
2. **Should Dinesh Vasu Dash be a 6th first-wave recipient?** He is a personal contact of the complainant (was his MOH group director during Covid). His current portfolio is MCCY & MOM, not MDDI. The user excluded him from the consolidated-send because of portfolio mismatch, not because of any other reason.
3. **Should the institutional direction callout** (in `CLAUDE.md` — pattern of decisions suggesting institutional rather than investigator-level direction) be added to a follow-up email after the first responses come in? **Blocked on**: Ray to download all PDPC correspondence emails into a folder for review. Look for emails signed by/referencing Deputy Commissioner Wong Huiwen Denise; timing inconsistencies suggesting IMDA notified PDPC of the complaint before it should have. Once primary-source quotes found, the callout can be drafted into a follow-up email.
4. **Should the disclosure paragraph in Tier 1C emails be tightened?** The current disclosure in `kenneth-goh.md` / `dinesh-vasu-dash.md` / `cai-yinzhou.md` works. If the user wants more warmth gradient, the wording can be tuned per recipient.

---

## Commit history (relevant subset)

```
082a1b8 Phase 2F: quality gate — replace straight apostrophe with curly in desmond-tan-kok-ming.md
6f0bee5 INDEX: add consolidated-send set section highlighting 5-email first wave
f376c13 Add consolidated-send.csv: 5-row tight campaign list
d4f5a1c Add consolidated-send: GPC for Digital Development and Information email
15ed161 Phase 2E-fix4: INDEX sub-grouping — move Zhulkarnain to PAP, separate personal-relationship sub-section
109380d Phase 2E: review index for all 108 personalised emails
3a5b69b Phase 2E-fix3: regenerate CSV with tier populated for all 108 rows
9f86139 Phase 2E-fix2: insert closing --- delimiter in 34 Tier 2 files + refresh CSV
bf52bde Phase 2E: master mail-merge CSV (108 rows)
b551227 Phase 2D: Tier 3 — ~49 base-draft emails with name substitution
24f2aae Phase 2C: Tier 2 — 6 full Cabinet Minister emails
a28fb7f Phase 2C: Tier 2 — 28 role-templated emails
da52538 Phase 2C: Tier 2 — 3 role-templated templates
c974d02 Phase 2B: Tier 1C — 3 personal-relationship emails with closing disclosure
f4c499e Phase 2B-TaskC-fix: unique personal-narrative across 12 WP emails
0d95ecc Phase 2B: Tier 1B — 12 bespoke Workers' Party MP emails
a9564e6 Phase 2B-revise: tighten 10 Tier 1A emails around 3-point central message
db117cf Phase 2B: Tier 1A — 10 bespoke PAP senior Minister emails
cc3fc80 Phase 2A: trim base draft to ~250 words (Task A)
f5d28d5 Plan: MP email personalisation — 9 tasks (A-I) with TDD-style verifications
f8677af Spec: also update length-target row in tone-quality rules table
7ebb30d Spec/Plan: correct Tier length targets (300w was spec error)
e1926e0 Spec: move Tier 1C disclosure from opening to closing note
6ff8f1a Spec: add Tier 1C personal-relationship disclosure (3 recipients)
4246447 Spec: MP & Minister email personalisation (Approach C, tiered)
1f26ac2 Plan: propagate 3-point central message to global constraints
e3d4a86 Spec: add three-point central message binding for all 108 emails
47434fb Spec: also update length-target row in tone-quality rules table
b0d48bb Spec/Plan: relax Tier 1 length to soft ceiling (400-550w)
e3d4a86 Spec: add three-point central message binding for all 108 emails
```

---

## Final summary

| Artefact | Path | Purpose |
|---|---|---|
| Spec (approved) | `docs/superpowers/specs/2026-07-02-mp-email-personalisation-design.md` | Design decisions + global constraints |
| Plan | `docs/superpowers/plans/2026-07-02-mp-email-personalisation-plan.md` | 9-task implementation plan |
| Base draft | `docs/superpowers/plans/2026-07-02-mp-followup-email-base-trimmed.md` | The ~240-word body shared across all 108 emails |
| Tier 2 templates | `docs/superpowers/plans/2026-07-02-mp-email-tier2-templates.md` | The 3 templates (T2-A MDDI / T2-B Coord Min / T2-C Other) |
| 108 .md emails | `data/personalised-emails/*.md` | One per recipient |
| Master CSV | `data/personalised-emails.csv` | Mail-merge source for the wider 108-recipient set |
| Consolidated send CSV | `data/consolidated-send.csv` | 5-row first-wave list (MDDI portfolio + GPC) |
| INDEX | `data/personalised-emails-INDEX.md` | Review index grouped by tier |
| GPC email | `data/personalised-emails/gpc-digital-development-and-information.md` | New email for the 7 GPC members |

**Next step for the user**: open `data/consolidated-send.csv`, copy each row's body into your mail client, send as **BCC**, wait 2-3 days between Minister Teo and the GPC. Replies are out of scope of this handoff.