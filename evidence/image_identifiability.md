# Image Identifiability — PDPC Advisory Guidelines on Video Masking

## Source document

| Field | Value |
|---|---|
| **Title** | Advisory Guidelines on the Personal Data Protection Act for Selected Topics |
| **Issued** | 24 September 2013 |
| **Revised** | 17 May 2022 |
| **Publisher** | Personal Data Protection Commission (PDPC), Singapore |
| **Format** | PDF, 63 pages, A4 |
| **File path in repo** | `../PDPA ACT and Advisory/Advisory Guidelines on the PDPA for Selected Topics 17 May 2022.pdf` |
| **Live URL** | https://www.pdpc.gov.sg/help-and-resources/2020/03/advisory-guidelines-on-the-pdpa-for-selected-topics (verify; may have been updated/replaced since 2022) |

## Screenshots

Two PNG screenshots extracted at 200 DPI from the PDF:

| File | Page | Content |
|---|---|---|
| `pdpa-masking-p41-41.png` | Page 41 | Preceding Q&A: paragraphs 4.53–4.57 (access requests, deletion, contracts, minimum resolution). Bottom of page leads into para 4.58. |
| `pdpa-masking-42.png` | **Page 42** (the money page) | Paragraphs 4.58–4.59 in full, plus the three visual masking examples (Solid / Blur / Pixelated). |

Both files live in the same directory as this markdown file:

```
evidence/pdpa-masking-p41-41.png
evidence/pdpa-masking-42.png
```

## Verbatim text — Pages 41–42

### Paragraph 4.54 (page 41)

> **4.54** Yes. It would be reasonable for certain groups of individuals (e.g. a married couple, parents of a class of students etc.) to make an access request for the same footage containing their personal data. Organisations may apply the same considerations in determining whether to provide access as they would for a request made by a single individual. Please refer to Chapter 15 of the Key Concepts Guidelines.

### Paragraph 4.55 (page 41)

> **4.55** No. The PDPA does not require an organisation to delete personal data upon request from an individual. Section 25 of the PDPA requires an organisation to cease to retain its documents containing personal data, or remove the means by which the personal data can be associated with particular individuals, as soon as it is reasonable to assume that the purpose for which that personal data was collected is no longer being served by retention of the personal data, and retention is no longer necessary for legal or business purposes.

### Paragraph 4.56 (page 41)

> **4.56** The PDPA does not prohibit this. However, such a contract would not override any rights or obligations under the PDPA.

### Paragraph 4.57 (page 41)

> **4.57** The PDPA does not prescribe any minimum resolution. However, given that the requirement is for the organisation to provide the personal data in its possession or under its control, the organisation should provide the CCTV footage in the form and of the resolution it holds for its purposes. If the individual's purpose for making the request may be met by a lower resolution extract or printout, the organisation may inform the individual of this less costly option.

### Paragraph 4.58 (page 42)

> **4.58** The PDPA does not specify the format of the personal data to be provided in relation to an access request made by an individual. In the case of personal data captured in CCTV footage, organisations may respond to access requests for CCTV footage by providing either still frames of the footage or the actual footage itself, with appropriate masking of the personal data of other individuals if required.

### Paragraph 4.59 — THE KEY PASSAGE (page 42)

> **4.59** "Video masking" of images refers to the process of concealing parts of the video from view. This may include masking certain body parts or inanimate objects that could potentially disclose the personal data of an individual. The common types of masking include (i) solid colour masked areas; (ii) blurred masking; or (iii) pixelated masking. Where solid colour masking is used, no details or movement in the scene covered by the masked area can be viewed. **However, when pixelated or blurred masking is used, the resulting image enables a partial outline to be seen but with detailed features obscured. This may be a less fool proof method as it is possible for pixelated or blurred images of individuals to still be identifiable.** Examples of the different masking techniques are shown below. These can be applied to both video and still imagery.

Page 42 includes three visual examples side-by-side with these labels:

- **Solid** — a black rectangle completely obscuring the face; no details visible
- **Blur** — a Gaussian blur over the face; outline and shape still visible
- **Pixelated** — a mosaic/pixelation effect; outline and shape still visible

## Why this matters for the PDPC grievance site

PDPC's own published advisory guidelines explicitly state:

1. **Blurred and pixelated masking is not foolproof** — individuals can still be identifiable from partial outlines and movement.
2. **Only solid-colour masking** (i.e., blacking out entirely) reliably prevents identification — "no details or movement in the scene covered by the masked area can be viewed."

### The contradiction

In the Complainant's case (MCST 4599, DP-2405-C2318), PDPC:

- Invented a **"clarity test"** for identifiability — determining that individuals in CCTV footage were not identifiable based on pixel resolution / image clarity.
- Used this test to rule that the Access Obligation was not engaged, because the footage did not contain "personal data" of identifiable individuals.
- **Did not apply or acknowledge its own published guideline (para 4.59)** — which states that even pixelated or blurred images can still be identifiable.

### The systemic implication

PDPC's clarity test, if applied generally, would exclude nearly all real-world CCTV footage from Access Obligation protection — because most CCTV footage lacks studio-quality facial resolution. This is directly at odds with PDPC's own published guidance, which contemplates masking obligations precisely because CCTV footage routinely captures identifiable individuals.

### How this connects to the site

- **Narrative contrast #6** ("The stated refusal grounds were never tested against the Fifth Schedule"): PDPC substituted its own reasoning rather than testing the MCSTs' stated grounds. The clarity test is an example of PDPC-invented reasoning that departs from its own published guidelines.
- **Failure #3** (s.22A preservation gap): PDPC admitted the preservation gap exists and referred it to the Ministry. The masking guideline underscores that even if footage were preserved, PDPC has a ready-made tool (the clarity test) to rule it non-personal-data.
- **"Nine questions PDPC has declined to answer"** — Q9 specifically addresses the clarity test.
- **#why section** ("enforcer became damager"): The clarity test's systemic implications are documented here.

## Cross-reference: relevant PDPA sections

- **s.21(3) and Fifth Schedule** — Exceptions to the Access Obligation. Neither MCST cited a ground listed here; PDPC did not test the stated refusal grounds against the schedule.
- **s.4(6)** — PDPA subordination to other written law. Applied in MCST 4436 (River Isles) to conclude the MCST could provide footage; never engaged in MCST 3615.
- **s.24** — Data intermediary provisions. Applied in MCST 4375 and MCST 3593 (security companies as data intermediaries); silently departed from in MCST 4599.
- **s.22A** — Offence of obstructing/hindering the Commission. PDPC admitted the preservation gap exists and referred it to the Ministry.

## How screenshots were generated

```bash
pdftoppm -f 41 -l 42 -png -r 200 \
  'PDPA ACT and Advisory/Advisory Guidelines on the PDPA for Selected Topics 17 May 2022.pdf' \
  /tmp/pdpa-masking
```

This produced two files: `pdpa-masking-41.png` (page 41) and `pdpa-masking-42.png` (page 42), at 200 DPI resolution. The source PDF is 63 pages; the CCTV section (Part 4) spans roughly pages 34–42, with the video masking Q&A appearing at the end of the CCTV subsection.
