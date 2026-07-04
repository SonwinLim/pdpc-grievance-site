# Full Handoff — PDPC Grievance MP & Civil Servant Email Campaign

**Date:** 3 July 2026
**Status:** All emails drafted, formatted as HTML, vetted via individual samples sent to limzirui@gmail.com. **Not yet sent to any external recipients.** Ready for final vetting and send.

**Handoff recipient:** Codex (or any successor agent). Work from `H:/My Drive/Driving Legal Issue/pdpc-grievance-site/`.

---

## What was built

A campaign of 117 personalised HTML emails across 3 groups:

| Group | Count | Directory |
|---|---|---|
| MP emails (Tier 1A, 1B, 1C, 2, 3) | 108 | `data/personalised-emails/` |
| Consolidated first-wave | 5 (subset of above) | `data/consolidated-send.csv` |
| Civil servants (MDDI, PMO, Istana, PSD) | 8 | `data/personalised-emails-civil-servants/` |
| GPC for Digital Development & Information | 1 | `data/personalised-emails/` (separate file) |

**Total unique emails: 117** (108 MPs + 8 civil servants + 1 GPC)

---

## Directory Map

```
pdpc-grievance-site/
├── data/
│   ├── personalised-emails/             ← 109 .md files (108 MPs + 1 GPC), each with YAML frontmatter + full HTML body
│   │   ├── josephine-teo.md             ← Tier 1A: Minister Teo (bespoke, 3-part Maradona analogy, WA19596 hook, 4 attachments)
│   │   ├── lawrence-wong.md             ← Tier 1A: PM Wong
│   │   ├── zhulkarnain-abdul-rahim.md   ← Tier 1A: Your MP (Chua Chu Kang), full personal narrative incl. Minister irony
│   │   ├── pritam-singh.md             ← Tier 1B: WP chief
│   │   ├── sylvia-lim.md               ← Tier 1B: WP chair
│   │   ├── kenneth-goh.md              ← Tier 1C: Personal (SMU prof, disclosure at end)
│   │   ├── dinesh-vasu-dash.md         ← Tier 1C: Personal (MOH group director, disclosure at end)
│   │   ├── cai-yinzhou.md              ← Tier 1C: Personal (youth friend, disclosure at end)
│   │   ├── tan-kiat-how.md             ← Tier 2: MDDI SMS (role-templated)
│   │   ├── alex-yeo-sheng-chye.md      ← Tier 3: Backbencher (base-draft + CCK disclaimer + Mr)
│   │   ├── ... (98 more)
│   │   └── gpc-digital-development-and-information.md  ← GPC email (7 recipients, BCC)
│   ├── personalised-emails-civil-servants/  ← 8 .md files, same frontmatter + HTML structure
│   │   ├── istana-president.md          ← President Tharman, CC zed_teo + rachael_leong
│   │   ├── mddi-ps-chng.md             ← PS MDDI, CC Doris_LEE
│   │   ├── mddi-2ps-foo.md             ← 2PS (Digital Dev), CC NEO_Wenzhu
│   │   ├── mddi-2ps-wong.md            ← 2PS (Information), CC Lynda_NG
│   │   ├── pmo-ps-chan.md              ← PS PMO, CC CHOW_Choi_Foon
│   │   ├── psd-ps-tan.md               ← PS PSD, CC angelina_ong
│   │   ├── psd-ds-han.md               ← DS (Leadership) PSD, CC sally_ong
│   │   └── psd-ds-jamie.md             ← DS (Transformation) PSD, CC kamisah_hassan
│   ├── personalised-emails.csv          ← Master mail-merge CSV (109 rows, 6 cols: tier,name,slug,email,subject,body)
│   ├── personalised-emails-INDEX.md     ← Review index grouped by tier
│   ├── consolidated-send.csv            ← 5-row first-wave list (Teo + 3 MDDI SMS/MOS + GPC BCC)
│   ├── pa-cc-map.json                   ← CC mapping (39 entries: slug -> [cc_emails])
│   ├── mp-contact-list.csv              ← 108 MPs with verified emails (parliament + sgdi fallback)
│   └── mp-contact-list.json             ← Same, programmatic
├── scripts/
│   ├── scrape-mp-emails.mjs             ← Phase 1: scrape parliament.gov.sg + sgdi.gov.sg
│   ├── convert-to-html-v3.py            ← Phase 3A: Markdown-to-HTML converter
│   ├── build-civil-servant-emails-v2.py ← Phase 3B: Build civil servant emails from shared sections
│   └── build-civil-servant-emails.py    ← Phase 3B v1 (superseded by v2)
├── docs/superpowers/
│   ├── specs/2026-07-02-mp-email-personalisation-design.md   ← Approved design spec
│   ├── plans/2026-07-02-mp-email-personalisation-plan.md    ← Implementation plan (9 tasks)
│   ├── plans/2026-07-02-mp-followup-email-draft.md          ← Original ~400w draft
│   ├── plans/2026-07-02-mp-followup-email-base-trimmed.md   ← Trimmed ~240w base (Task A output, now superseded by HTML template)
│   ├── plans/2026-07-02-mp-email-tier2-templates.md         ← 3 tier-2 templates (T2-A MDDI, T2-B CoordMin, T2-C Other)
│   ├── plans/2026-07-02-email-work-handoff.md               ← Previous handoff (2 July, now superseded by this one)
│   └── plans/2026-07-03-full-handoff.md                     ← THIS FILE
├── Template Email PM.md                 ← User's approved visual template (Markdown format)
├── BreachBreakdown.jpg                  ← Attachment 1: 204 Protection vs 0 Access Obligation chart
├── entry-gate-overlay.jpg              ← Attachment 2: pdpaaccessrights.sg entry layover
├── pdpa-masking-42.png                 ← Attachment 3: PDPC Advisory Guidelines p.42
├── hansard.jpg                          ← Attachment 4: Parliament Written Answer 19596
└── samples-bundle.eml                   ← Multipart MIME bundle with 6 sample emails + 4 attachments (for vetting)
```

---

## Email structure (HTML, identical across all 117)

Every email, regardless of tier, follows this exact structure:

```
1. Greeting: <h2 style="font-weight:normal">Dear <strong>{Title} {Name}</strong>,</h2>
2. Bespoke opening paragraph(s) — unique per recipient
3. <h2>What caused me to revisit this issue</h2> (shared)
   - "This is not the first time..." paragraph
   - "PDPC's enforcement website" paragraph
   - "Instead of addressing the pattern..." paragraph
   - "That is why I created pdpaaccessrights.sg" paragraph
   - "I sent the full site to PDPC and IMDA leadership on 21 June 2026... No reply was given."
4. <h2>The Maradona "Hand of God" analogy</h2> (shared, Tier 1+2 only; skipped in Tier 3)
   - Hand of God paragraph
   - Discretion vs dereliction paragraph
   - Rulebook paragraph (PDPC said Guidelines not determinative while using them for other cases)
5. <h2>Why this matters</h2> (shared)
   - CCTV denied and destroyed
   - 204 Protection vs 0 Access Obligation
   - Enforcement body discretion vs permission to disregard the law
6. <h2>Where the full facts are documented</h2> (shared)
   - Links to pdpaaccessrights.sg and enforcement-index
7. <h2>What I am asking</h2> (bespoke per recipient)
8. <h2>Sites for verification</h2> (shared, numbered <ol> with <a> links)
9. <h2>Attachments</h2> (shared, numbered <ol> with descriptions)
10. CC line (where applicable)
11. Closing mission statement (shared, before signature)
    - "My complaints were the only ones where PDPC were compelled to investigate..."
    - "...it is my mission to make sure that other Singaporeans and residents will not suffer what I went through."
12. Signature: Yours sincerely, Ray Lim
```

**CSS (inline in every email):**
```css
body { font-family: Arial, Helvetica, sans-serif; font-size: 16px; max-width: 640px; margin: 0 auto; padding: 20px; color: #222; line-height: 1.5; }
p { margin-bottom: 0.9em; }
h2 { font-size: 1.15em; margin-top: 1.6em; margin-bottom: 0.6em; }
li { margin-bottom: 0.6em; }
ol { margin-bottom: 1em; }
```

**Attachments (4 per email):**
1. `BreachBreakdown.jpg` — PDPC breach-by-obligation chart (204 Protection vs 0 Access)
2. `entry-gate-overlay.jpg` — pdpaaccessrights.sg entry layover
3. `pdpa-masking-42.png` — PDPC Advisory Guidelines p.42 para 4.59 (blurred/pixelated still identifiable)
4. `hansard.jpg` — Parliament Written Answer 19596 (22 Sep 2025)

---

## Tier system

### Tier 1A — Bespoke PAP Senior Ministers (10)
Fully bespoke opening + closing. Role-title greeting. CC to PA per sgdi.gov.sg.

| Slug | Recipient | Greeting | CC |
|---|---|---|---|
| `josephine-teo` | Josephine Teo | Dear Minister Josephine Teo, | Eunice_GAN@mddi.gov.sg |
| `lawrence-wong` | Lawrence Wong | Dear Prime Minister Lawrence Wong, | Agnes_CHUA@pmo.gov.sg |
| `lee-hsien-loong` | Lee Hsien Loong | Dear Senior Minister Lee Hsien Loong, | Annie_LAM@pmo.gov.sg |
| `gan-kim-yong` | Gan Kim Yong | Dear Deputy Prime Minister Gan Kim Yong, | Lilian_NG@mti.gov.sg |
| `chan-chun-sing` | Chan Chun Sing | Dear Coordinating Minister Chan Chun Sing, | Grace_Chan@mindef.gov.sg |
| `k-shanmugam` | K Shanmugam | Dear Coordinating Minister K Shanmugam, | Melissa_Ong@mha.gov.sg |
| `edwin-tong-chun-fai` | Edwin Tong | Dear Minister Edwin Tong, | lau_ai_lin@mlaw.gov.sg |
| `indranee-rajah` | Indranee Rajah | Dear Minister Indranee Rajah, | Jessie_QUEK@mof.gov.sg |
| `seah-kian-peng` | Seah Kian Peng | Dear Speaker Seah Kian Peng, | chloe_tan@parl.gov.sg |
| `zhulkarnain-abdul-rahim` | Zhulkarnain Abdul Rahim | Dear Minister of State Zhulkarnain Abdul Rahim, | wardah_ahmad@mfa.gov.sg |

Zhulkarnain has the most extensive personalisation: constituency MP reference, first email 27 May 2024, "clear as day" paragraph, WA19596 thanks, "now you are a Minister" irony, CCK residency, follow-up PQ ask.

### Tier 1B — Bespoke WP MPs (12)
Fully bespoke opening + closing. Personal honorific (Mr/Ms). No CC. **Includes CCK residency disclaimer.** Each email acknowledges WP's engagement on PDPA/civil-liberties issues.

### Tier 1C — Personal Relationship (3)
First-name greeting. Disclosure paragraph at end (after signature, separated by `---`). No CC.

| Slug | Recipient | Relationship |
|---|---|---|
| `kenneth-goh` | Kenneth Goh | SMU professor during MBA (Associate Prof, NOT Senior Counsel — fact-checked) |
| `dinesh-vasu-dash` | Dinesh Vasu Dash | MOH group director during Covid (MCCY & MOM, NOT MDDI — fact-checked) |
| `cai-yinzhou` | Cai Yinzhou | Friend since youth (Bishan-Toa Payoh GRC, NOT Chua Chu Kang — fact-checked) |

### Tier 2 — Role-Templated (34)
Role-title greeting. CC to PA per sgdi.gov.sg. Same shared sections as Tier 1A, role-templated opening + closing question. Recipients: all Cabinet Ministers, SMS, MOS, SPS, Mayors, Deputy Speakers not in Tier 1A. Full list in `data/pa-cc-map.json`.

### Tier 3 — Base-Draft + Name (49)
Backbencher MPs. Base shared sections, name substituted. No personalisation beyond the greeting. **No Maradona analogy** (dropped per spec). **Includes CCK residency disclaimer.** Honorific from parliament.gov.sg (Mr/Ms/Dr/Prof/Assoc Prof).

---

## Civil servant emails (8)

All in `data/personalised-emails-civil-servants/`. Same HTML structure as MP emails. Bespoke opening + closing per recipient. CC to PA.

| Slug | Recipient | CC |
|---|---|---|
| `istana-president` | President Tharman (tharman_s@istana.gov.sg) | zed_teo, rachael_leong |
| `mddi-ps-chng` | PS CHNG Kai Fong (MDDI) | Doris_LEE |
| `mddi-2ps-foo` | 2PS FOO Chi Hsia (Digital Dev, MDDI) | NEO_Wenzhu |
| `mddi-2ps-wong` | 2PS WONG Kang Jet (Information, MDDI) | Lynda_NG |
| `pmo-ps-chan` | PS CHAN Heng Kee (PMO) | CHOW_Choi_Foon |
| `psd-ps-tan` | PS TAN Gee Keow (PSD) | angelina_ong |
| `psd-ds-han` | DS HAN Neng Hsiu (Leadership, PSD) | sally_ong |
| `psd-ds-jamie` | DS Jamie ANG (Transformation, PSD) | kamisah_hassan |

**PA sources:** All PA emails sourced from sgdi.gov.sg ministry pages (verified 3 July 2026). The PA is the assistant to the senior civil servant — they will handle inbox routing.

---

## MIME format for sending

Every email uses this exact MIME structure:

```
multipart/mixed
├── multipart/alternative
│   └── text/html (the HTML body from the .md file, after --- frontmatter)
├── image/jpeg (BreachBreakdown.jpg)
├── image/jpeg (entry-gate-overlay.jpg)
├── image/png  (pdpa-masking-42.png)
└── image/jpeg (hansard.jpg)
```

**CRITICAL:** The outer container must be `multipart/mixed`. Previous attempts used `multipart/alternative` as the outer container, which caused attachments to be stripped by Gmail. Corrected in commit `02e523e`.

---

## Sending infrastructure

**Tool:** `gws` (Google Workspace CLI) v0.22.5, installed via `npm install -g @googleworkspace/cli`
**Binary:** `C:\Users\limzi\AppData\Roaming\npm\node_modules\@googleworkspace\cli\bin\gws.exe`
**Auth:** OAuth2, stored in OS keyring (`gws auth login` completed 3 July 2026, account: limzirui@gmail.com)
**Scope:** `gmail.modify` (sufficient for sending)

**Send command template (Python subprocess):**
```python
import json, subprocess
GWS = r'C:\Users\limzi\AppData\Roaming\npm\node_modules\@googleworkspace\cli\bin\gws.exe'
result = subprocess.run(
    [GWS, 'gmail', 'users', 'messages', 'send',
     '--params', json.dumps({'userId': 'me'}),
     '--upload', str(eml_path.resolve()),
     '--upload-content-type', 'message/rfc822'],
    capture_output=True, text=True, timeout=120
)
message_id = json.loads(result.stdout).get('id')
```

**IMPORTANT:** Do NOT use `gws` via the `.cmd` shim or shell invocation — the command-line argument length limit on Windows (~32KB) causes truncation of the JSON payload. Always use `subprocess.run()` with the list-of-args form calling `gws.exe` directly, and use `--upload` with a `.eml` file path instead of `--json` with inline content.

**Verification command:**
```bash
gws gmail users messages get --params '{"userId":"me","id":"MESSAGE_ID","format":"metadata","metadataHeaders":["Subject","To","Date"]}'
```

---

## Key decisions & rules (binding for any future edit)

### Style rules (from CLAUDE.md + spec)
1. **Curly quotes** (`‘` `’` `“` `”`) throughout. No straight `'` or `"` in visible text.
2. **No em-dashes (`—`)** in body prose. En-dashes (`–`) OK only in numeric ranges and bullet separators. All em-dashes removed in commit `8c512f9`.
3. **No fabricated quotes.** Every quote must come from: PDPC correspondence (`evidence/*.html`), PDPC rulings, the PDPA (https://sso.agc.gov.sg/Act/PDPA2012), Singapore Parliament records, or the live site (https://pdpaaccessrights.sg).
4. **No criminal/civil case references.** No "GCW.PI", "GCW.CRIM", "motorcycle", "taxi", "Quak Chee Wah" in body text.
5. **No adversarial framing.** No "cover-up", "gaslight" — except where the user explicitly approved "gaslighted" in the closing mission statement. Use "documented pattern", "regulatory interpretation gap", "departure from statute".
6. **Signature:** `Yours sincerely,` + `Ray Lim` (no SMU MBA / Commendation Medal line — removed per user instruction 3 July 2026).
7. **Word count: no limit.** Removed per user instruction 3 July 2026.

### Three-point central message (binding)
1. **PDPC hid the filter** — redesigned website, obligation-type filter removed after the zero-Access-Obligation pattern was raised
2. **Maradona "Hand of God" analogy** — the enforcer sits in judgement of itself (carried in Tier 1+2; dropped in Tier 3)
3. **Zero Access Obligation investigation** — 0 breaches across entire published enforcement record, vs 204 Protection breaches

### Four sites to verify (binding, in every email)
1. https://pdpaaccessrights.sg — full account, rebuilt filter, primary record
2. https://pdpaaccessrights.sg/enforcement-index.html — rebuilt matrix, 0 Access Obligation across 374 decisions
3. https://www.pdpc.gov.sg/organisations/regulations-decisions/enforcement-decisions?type=Commission%27s+Decisions&page=1&sort=latest — official PDPC page (filterable by enforcement/undertaking and years only; obligation-type filter was removed)
4. https://sprs.parl.gov.sg/search/#/sprs3topic?reportid=written-answer-19596 — WA 19596, Minister Teo's assurance on preservation + criminal penalties

### Formatting rules (binding)
1. All emails: line-height 1.5, font-size 16px, Arial, max-width 640px
2. Greeting: `<h2 style="font-weight: normal;">` (same font-size as section headings)
3. Section headings: `<h2>` with 1.6em top margin, 0.6em bottom margin
4. Paragraphs: 0.9em bottom margin
5. All Tier 3 backbencher greetings: honorific from parliament.gov.sg bio pages (Mr/Ms/Dr/Prof/Assoc Prof)
6. All ministerial greetings: role title + name (e.g., "Dear Minister Josephine Teo,") — NOT personal honorifics
7. WP MPs: Mr/Ms + name (personal honorific — they are MPs, not Ministers)
8. CCK residency disclaimer: present in all WP and Tier 3 emails, not in Tier 1A/Tier 2 (those recipients are ex officio addresses)

---

## Fact-check log

All verified against parliament.gov.sg and/or Wikipedia:

| Claim | Verification | Commit |
|---|---|---|
| Kenneth Goh is NOT a Senior Counsel (he is Assoc Prof at SMU) | `a9f1c7d` | Removed "Senior Counsel" → "Associate Professor at SMU" |
| Dinesh Vasu Dash is NOT at MDDI (he is MOS, MCCY & MOM) | `a9f1c7d` | Corrected portfolio |
| Kenneth Tiong has NO legal background (finance/tech) | `a9f1c7d` | "background in law" → "finance and technology" |
| Dennis Tan is an advocate and solicitor (1997), SC unverified | `a9f1c7d` | "Senior Counsel" → "advocate and solicitor" |
| Cai Yinzhou is NOT the sender's MP (sender is in Chua Chu Kang) | `3deb8a5` | "as my MP" → "as a friend" |
| Zhulkarnain is the actual Chua Chu Kang MP | `9af5a18` | Added full personal narrative |
| All honorifics for Tier 3 sourced from parliament.gov.sg bio pages | `fd05e34` | 49 honorifics verified |

---

## Consolidated first-wave send list

5 emails, all MDDI-focused:

| # | Recipient | Slug | Email | Send as |
|---|---|---|---|---|
| 1 | Minister Josephine Teo | `josephine-teo` | kaks.mps@pap.org.sg | Individual |
| 2 | SMS Tan Kiat How | `tan-kiat-how` | Kg.Chai.Chee.MPS@pap.org.sg | Individual |
| 3 | MOS Jasmin Lau | `jasmin-lau` | Jasmin.Lau@pap.org.sg | Individual |
| 4 | MOS Rahayu Mahzam | `rahayu-mahzam` | Rahayu.Mahzam@pap.org.sg | Individual |
| 5 | GPC for Digital Development & Information | `gpc-digital-development-and-information` | (7 BCC addresses) | **BCC** |

**GPC BCC addresses:**
- sharael-taha@parliament.gov.sg (Chairperson)
- henryforkebunbaru@gmail.com (Deputy Chairperson)
- mp@tengah.sg (Choo Pei Ling)
- mps@ulupandan.sg (Christopher de Souza)
- ayer.rajah.mps@pap.org.sg (Cassandra Lee)
- my.mp@changisimei.sg (Jessica Tan Soon Neo)
- tinpeiling@gmail.com (Tin Pei Ling)

**Send order recommended:**
1. Day 1: Minister Teo
2. Day 3-4: SMS Tan Kiat How + MOS Jasmin Lau + MOS Rahayu Mahzam
3. Day 5-7: GPC for DDI (as BCC to all 7 members)

**Rationale:** Allow Teo's office to absorb first; the GPC inquiry follows naturally from the MDDI team being informed.

---

## Send procedure (for any agent)

### To send ALL remaining un-sent emails:

1. **Verify auth:**
   ```bash
   gws auth status | grep auth_method
   # Must return: "auth_method": "oauth2"
   ```

2. **Read the email body from .md file:**
   ```python
   from pathlib import Path
   content = Path('data/personalised-emails/josephine-teo.md').read_text(encoding='utf-8')
   html_body = content.split('---', 2)[2].strip()  # Skip YAML frontmatter
   ```

3. **Build MIME message:**
   ```python
   from email.mime.multipart import MIMEMultipart
   from email.mime.text import MIMEText
   from email.mime.image import MIMEImage

   outer = MIMEMultipart('mixed')
   outer['From'] = 'limzirui@gmail.com'
   outer['To'] = recipient_email  # from frontmatter
   outer['Subject'] = subject     # from frontmatter
   # Add CC if applicable
   if cc_emails:
       outer['Cc'] = cc_emails

   inner = MIMEMultipart('alternative')
   inner.attach(MIMEText(html_body, 'html', 'utf-8'))
   outer.attach(inner)

   # Attach 4 images
   for fn in ['BreachBreakdown.jpg','entry-gate-overlay.jpg','pdpa-masking-42.png','hansard.jpg']:
       with open(fn, 'rb') as fp:
           img = MIMEImage(fp.read())
       img.add_header('Content-Disposition', 'attachment', filename=fn)
       outer.attach(img)

   # Write .eml and send via gws
   eml_path = Path(f'data/outbox/{slug}.eml')
   eml_path.parent.mkdir(exist_ok=True)
   eml_path.write_bytes(outer.as_bytes())
   ```

4. **Send via gws:**
   ```python
   import json, subprocess
   GWS = r'C:\Users\limzi\AppData\Roaming\npm\node_modules\@googleworkspace\cli\bin\gws.exe'
   result = subprocess.run(
       [GWS, 'gmail', 'users', 'messages', 'send',
        '--params', json.dumps({'userId': 'me'}),
        '--upload', str(eml_path.resolve()),
        '--upload-content-type', 'message/rfc822'],
       capture_output=True, text=True, timeout=120
   )
   ```

5. **For BCC (GPC email only):** Add all 7 addresses as `outer['Bcc']` and set `outer['To']` to a placeholder (or `limzirui@gmail.com`). Gmail requires at least one To address.

---

## How to add a new recipient

1. Create a new `.md` file in the appropriate directory (`data/personalised-emails/` or `data/personalised-emails-civil-servants/`)
2. Copy the HTML structure from any existing file (e.g., `josephine-teo.md` for Tier 1A, `alex-yeo-sheng-chye.md` for Tier 3, `istana-president.md` for civil servants)
3. Replace the bespoke opening paragraph and closing question
4. Update the YAML frontmatter (tier, name, slug, email, designation, subject)
5. If Tier 1A or Tier 2: add CC from sgdi.gov.sg by finding the PA entry
6. If Tier 3: source honorific from `https://www.parliament.gov.sg/mps/list-of-current-mps/mp/details/{slug}` (look for `Mr/Ms/Dr/Prof` pattern in the HTML)
7. For the Maradona section: include it for Tier 1+2, skip for Tier 3

---

## Known issues & pending

1. **Tier 3 closing questions are empty** — the HTML conversion script's `extract_closing_question()` returned empty for most Tier 3 files because the base draft's closing question (`"is it right that rights under the law can be denied..."`) was treated as shared body content and replaced by the template's "Why this matters" section. The "What I am asking" section is therefore missing from Tier 3 emails. Either: (a) re-extract the original closing question from the pre-conversion files (available via git), or (b) write a generic Tier 3 closing question.
2. **NMPs in Tier 3** — 9 NMPs are in Tier 3 but have no constituency and no PA. Their emails are base-draft only.
3. **GPC email has "I" typo** — `"The I rebuilt the removed filter at pdpaaccessrights.sg"` has a stray "The". Fix by searching for `"The I rebuilt"` in `gpc-digital-development-and-information.md` and removing the first "The".
4. **The wider 103 MP emails** are reserved for a second wave. The user has not decided whether to send them.
5. **Sending has NOT been done** — all emails are drafted and samples were sent to limzirui@gmail.com for vetting. No email has been sent to any external recipient as of 3 July 2026.
6. **8 civil servant emails are not linked to the master `personalised-emails.csv`** — they are in a separate directory. If you want a unified CSV, run a similar extraction on `data/personalised-emails-civil-servants/`.

---

## Commit history (most recent first, relevant subset)

```
727ada2 Phase 3B: add 3 PSD civil servant emails
6f479a2 Phase 3B v2: add President email, CC all PAs, remove PDPC Commissioner
fa00b1e Phase 3B: create 6 civil servant HTML emails
fd05e34 Phase 3A: add Mr/Ms/Dr/Prof honorifics to all 49 Tier 3 greetings
f8fb421 Phase 3A: add CCK residency disclaimer to WP and Tier 3 emails
41f5085 Phase 3A: add PDPC/IMDA no-reply note (sent site 21 June 2026)
146b854 Phase 3A: add closing mission statement (gaslighting + mission) to 109 emails
03f8fd9 Phase 3A: add security guards + cannot be identified to masking description
18ac6d8 Phase 3A: expand pdpa-masking-42 description with identifiability + PDPC irony
6b927a4 Phase 3A: insert why I revisited section into all 109 emails
33feedf Phase 3A: restore Zhulkarnain full personal narrative
c060ffb Phase 3A: line-height 1.7 -> 1.5
fa7b9b2 Phase 3A: apply 4 formatting fixes (h2 greeting, Maradona title, line-spacing, capital)
02e523e Phase 3A-fix: correct MIME structure (multipart/mixed container)
465b920 Phase 3A: convert 108 emails to HTML format
a44e179 Phase 2R: map PAs from 14 sgdi pages, CC to 39 Tier 1A+2 emails
a66f84e Phase 2Q: reformat sites/attachments to numbered format, clean URLs
a48aed2 Phase 2K: add 3-site explanations, clickable links, hansard URL, hansard.jpg
6e30004 Phase 2L: add Hansard URL to verification block in all 109 emails
8c512f9 Phase 2P: remove all em-dashes from email bodies
a9f1c7d Phase 2M: fact-check 4 role/profession claims across emails
3deb8a5 Phase 2N: remove 'as my MP' claim from cai-yinzhou.md
```

---

## Quick-start: read this first

1. **All MP emails:** `data/personalised-emails/*.md` (109 files)
2. **All civil servant emails:** `data/personalised-emails-civil-servants/*.md` (8 files)
3. **First-wave send list:** `data/consolidated-send.csv` (5 rows)
4. **CC mapping:** `data/pa-cc-map.json` (39 entries)
5. **Design spec:** `docs/superpowers/specs/2026-07-02-mp-email-personalisation-design.md`
6. **User's approved template:** `Template Email PM.md`
7. **gws send binary:** `C:\Users\limzi\AppData\Roaming\npm\node_modules\@googleworkspace\cli\bin\gws.exe`
8. **gws auth:** live OAuth2 for limzirui@gmail.com (stored in OS keyring)
9. **Sending format:** Build `.eml` with multipart/mixed → upload via gws `--upload` flag
10. **BCC for GPC:** Use `outer['Bcc']` header; set `outer['To']` to limzirui@gmail.com
