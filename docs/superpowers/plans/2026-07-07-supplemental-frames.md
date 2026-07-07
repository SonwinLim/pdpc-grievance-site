# Supplemental Video Frames Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add ~18 supplemental evidentiary and illustrative frames to the PDPC grievance video (statute screenshots, verbatim official-reply frames, guideline pages, Street View location shots, and repointed Gemini frames), wired into `VISUAL_SCHEDULE` so they actually appear, without touching any of the 13 approved hero frames.

**Architecture:** All frames are produced by `scripts/generate_supplemental_frames.py` into `Screenshots Video/{source,recreated,generated}/`. The video timeline is driven by `VISUAL_SCHEDULE` in `scripts/video_visuals.py`; `assemble_video.py` renders from it. A frame is "in the video" only if it is both generated and scheduled. `generate_supplemental_frames.py` ends with `find_missing_visual_assets(VISUAL_SCHEDULE)` which raises if any scheduled frame is missing, keeping generator and schedule in sync.

**Tech Stack:** Python 3, PyMuPDF (`fitz`), Pillow (`PIL`). Windows, Git Bash available. No test framework in this repo; verification is: generator runs clean, `find_missing_visual_assets` passes, and spot-checks of output PNGs.

## Global Constraints

- **Heroes are never modified or removed.** `cover page.png` and `Scene 1.jpg … scene 13.png` and their `VISUAL_SCHEDULE` hero entries stay exactly as they are.
- **Source-discipline.** Every evidentiary frame traces to the PDPA statute, a published guideline, a PDPC/IMDA decision PDF, or a verbatim official email (sender = a `pdpc.gov.sg` / `imda.gov.sg` / MCST-agent address). No frame is sourced from author-authored analysis or the Complainant's own outgoing letters.
- **Slide template.** Evidentiary frames use the existing helpers (`render_pdf_source`, `image_frame`, `save_card`) unchanged in styling: title bar (`#111` on white, `#C41230` rule), highlighted clause, footer caption. Palette constant `RED = "#C41230"`.
- **Fail loud.** If a statute search term does not match, generation must raise, not silently render the wrong page.
- **Spec:** `docs/superpowers/specs/2026-07-07-supplemental-frames-design.md`.
- **Repo paths:** site root = `D:/Driving Legal Issue/pdpc-grievance-site`; case root = `D:/Driving Legal Issue`; email exports = `C:/Users/limzi/Documents/AntiGravity/PDPC Emails/output`.

---

## File Structure

- Modify: `scripts/generate_supplemental_frames.py` — add new frame calls; add `render_email_quote()` helper; harden `render_pdf_source()` to fail loud; remove 3 superseded `save_simple_generated()` calls.
- Modify: `scripts/video_visuals.py` — `VISUAL_SCHEDULE`: 3 Gemini remaps, new entries, reflow.
- Create: `Screenshots Video/TST CCTV Location.png` (copy of the source photo frame into main heroes folder).
- Read-only sources: `PDPA ACT and Advisory/Personal Data Protection Act 2012.pdf`, `Advisory Guidelines for Management Corporations 17 May 2022.pdf`, `Advisory Guidelines on Key Concepts in the PDPA 17 May 2022.pdf`, `pdpa-masking-42.png`, `TST CCTV GoogleMap.png`, `TST CCTV 2  GoogleMap accident location.png`, email exports under `PDPC Emails/output`.

---

## Task 1: Copy the TST CCTV location photo into main frames

**Files:**
- Create: `Screenshots Video/TST CCTV Location.png`
- Source: `Screenshots Video/source/scene02_tst_cctv_location.png`

**Interfaces:**
- Consumes: nothing.
- Produces: a hero-adjacent copy of the TST CCTV location photo (the user's "other TST CCTV location picture copied").

- [ ] **Step 1: Copy the file**

Run (from site root):
```bash
cp "Screenshots Video/source/scene02_tst_cctv_location.png" "Screenshots Video/TST CCTV Location.png"
```

- [ ] **Step 2: Verify it exists and is non-trivial**

Run:
```bash
ls -la "Screenshots Video/TST CCTV Location.png"
```
Expected: file present, size > 100 KB.

- [ ] **Step 3: Commit**

```bash
git add "Screenshots Video/TST CCTV Location.png"
git commit -m "assets: copy TST CCTV location photo into main frames"
```

---

## Task 2: Harden `render_pdf_source` and add the 4 statute frames

**Files:**
- Modify: `scripts/generate_supplemental_frames.py` — `render_pdf_source()` (fail-loud), and 4 new calls in `main()`.

**Interfaces:**
- Consumes: existing `render_pdf_source(path, title, pdf_path, search_terms, footer)`.
- Produces frames: `source/scene04_pdpa_s22a.png`, `source/scene08_pdpa_s4_2_4_3.png`, `source/scene10_pdpa_s24_protection.png`, `source/scene10_pdpa_s25_retention.png`.

- [ ] **Step 1: Make `render_pdf_source` fail loud when no term matches**

In `scripts/generate_supplemental_frames.py`, replace the search loop inside `render_pdf_source` (currently defaults to `page_index = 0` and highlights only if found) so it raises when nothing matches:

```python
def render_pdf_source(path, title, pdf_path, search_terms, footer):
    doc = fitz.open(pdf_path)
    page_index = None
    highlights = []
    for i, page in enumerate(doc):
        for term in search_terms:
            found = page.search_for(term)
            if found:
                page_index = i
                highlights.extend(found[:3])
        if highlights:
            break
    if page_index is None:
        doc.close()
        raise SystemExit(
            f"[render_pdf_source] no search term matched in {Path(pdf_path).name} "
            f"for {path} (terms: {search_terms})"
        )
    page = doc[page_index]
    for rect in highlights:
        annot = page.add_highlight_annot(rect)
        annot.set_colors(stroke=(1, 0.86, 0.2))
        annot.update()
    pix = page.get_pixmap(matrix=fitz.Matrix(1.8, 1.8), alpha=False)
    page_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    title_bar(draw, title, f"Source page {page_index + 1}: {Path(pdf_path).name}")
    page_img.thumbnail((W - 180, H - 230), Image.Resampling.LANCZOS)
    x = (W - page_img.width) // 2
    y = 150
    canvas.paste(page_img, (x, y))
    draw.rectangle([0, H - 72, W, H], fill="#ffffff")
    draw.text((70, H - 48), footer, fill=MUTED, font=F_SMALL)
    out = FRAMES_DIR / path
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=95)
    doc.close()
```

- [ ] **Step 2: Add the 4 statute calls**

In `main()`, immediately after the existing `render_pdf_source(... "source/scene07_fifth_schedule.png" ...)` line, add:

```python
    render_pdf_source("source/scene04_pdpa_s22a.png", "s.22A Preservation Duty", pdpa,
                      ["Preservation of copy of personal data", "must preserve a complete and accurate copy"],
                      "PDPA 2012, s.22A")
    render_pdf_source("source/scene08_pdpa_s4_2_4_3.png", "Data Intermediary vs Organisation", pdpa,
                      ["as if the personal data were processed by the organisation", "other than the obligations under sections 24"],
                      "PDPA 2012, s.4(2) and s.4(3)")
    render_pdf_source("source/scene10_pdpa_s24_protection.png", "s.24 Protection Obligation", pdpa,
                      ["Protection of personal data", "reasonable security arrangements"],
                      "PDPA 2012, s.24")
    render_pdf_source("source/scene10_pdpa_s25_retention.png", "s.25 Retention Limitation", pdpa,
                      ["Retention of personal data", "cease to retain"],
                      "PDPA 2012, s.25")
```

- [ ] **Step 3: Run just these frames to verify search terms match**

Because `main()` ends with `find_missing_visual_assets` (which will fail until Task 6 updates the schedule), run a scoped check instead. From site root:
```bash
python - <<'PY'
import sys; sys.path.insert(0, "scripts")
import generate_supplemental_frames as g
g.ensure_dirs()
from pathlib import Path
pdpa = g.ROOT / "PDPA ACT and Advisory/Personal Data Protection Act 2012.pdf"
g.render_pdf_source("source/scene04_pdpa_s22a.png", "s.22A Preservation Duty", pdpa,
                    ["Preservation of copy of personal data", "must preserve a complete and accurate copy"], "PDPA 2012, s.22A")
g.render_pdf_source("source/scene08_pdpa_s4_2_4_3.png", "Data Intermediary vs Organisation", pdpa,
                    ["as if the personal data were processed by the organisation", "other than the obligations under sections 24"], "PDPA 2012, s.4(2) and s.4(3)")
g.render_pdf_source("source/scene10_pdpa_s24_protection.png", "s.24 Protection Obligation", pdpa,
                    ["Protection of personal data", "reasonable security arrangements"], "PDPA 2012, s.24")
g.render_pdf_source("source/scene10_pdpa_s25_retention.png", "s.25 Retention Limitation", pdpa,
                    ["Retention of personal data", "cease to retain"], "PDPA 2012, s.25")
print("OK: 4 statute frames rendered")
PY
```
Expected: `OK: 4 statute frames rendered` (no `SystemExit`). If any raises "no search term matched", open the PDPA PDF, find the exact heading/clause wording, and adjust that call's `search_terms`, then re-run.

- [ ] **Step 4: Spot-check the highlighted clause landed on the right page**

Open each of the 4 PNGs in `Screenshots Video/source/` and confirm the yellow highlight sits on the intended provision (s.22A preservation; s.4(2)/(3) intermediary split; s.24 protection; s.25 retention). If a highlight is on the wrong page, tighten the first search term to a phrase unique to that clause.

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_supplemental_frames.py "Screenshots Video/source/scene04_pdpa_s22a.png" "Screenshots Video/source/scene08_pdpa_s4_2_4_3.png" "Screenshots Video/source/scene10_pdpa_s24_protection.png" "Screenshots Video/source/scene10_pdpa_s25_retention.png"
git commit -m "frames: add s.22A, s.4(2)/(3), s.24, s.25 statute screenshots; fail-loud render_pdf_source"
```

---

## Task 3: Add guideline, masking, and Street View frames

**Files:**
- Modify: `scripts/generate_supplemental_frames.py` — new calls in `main()`.

**Interfaces:**
- Consumes: existing `render_pdf_source()` and `image_frame(path, title, src, footer)`.
- Produces frames: `source/scene03_mcst_guideline_police.png`, `source/scene06_key_concepts_identifiability.png`, `source/scene06_masking_still_identifiable.png`, `source/scene02_tst_streetview_cameras.png`, `source/scene02_tst_accident_location.png`.

- [ ] **Step 1: Add the guideline + masking + Street View calls**

In `main()`, after the statute calls from Task 2, add (the guideline PDFs are already assigned to `mcst_guideline` and to a new `key_concepts` variable — add that variable next to the existing `pdpa`/`selected` assignments at the top of `main()`):

```python
    key_concepts = ROOT / "PDPA ACT and Advisory/Advisory Guidelines on Key Concepts in the PDPA 17 May 2022.pdf"
```

Then the calls:

```python
    render_pdf_source("source/scene03_mcst_guideline_police.png", "Access Is Not Police-Only", mcst_guideline,
                      ["may not limit the provision of access", "law enforcement"],
                      "Advisory Guidelines for Management Corporations")
    render_pdf_source("source/scene06_key_concepts_identifiability.png", "Personal Data, Not Narrowly Construed", key_concepts,
                      ["not intended to be narrowly construed", "from which an individual can be identified"],
                      "Advisory Guidelines on Key Concepts in the PDPA")
    image_frame("source/scene06_masking_still_identifiable.png", "Masking Can Still Be Identifiable",
                SITE_ROOT / "pdpa-masking-42.png",
                "Selected Topics Guidelines, para 4.58–4.59 (page 42)")
    image_frame("source/scene02_tst_streetview_cameras.png", "The Scotts Tower CCTV, Facing The Road",
                SITE_ROOT / "TST CCTV GoogleMap.png",
                "Contemporaneous CCTV-location evidence (Google Street View)")
    image_frame("source/scene02_tst_accident_location.png", "Camera Coverage Of The Accident Location",
                SITE_ROOT / "TST CCTV 2  GoogleMap accident location.png",
                "Contemporaneous CCTV-location evidence (Google Street View)")
```

Note: `SITE_ROOT` and `ROOT` are already defined at module top; `mcst_guideline` is already assigned in `main()`. Confirm `key_concepts` is added beside them.

- [ ] **Step 2: Render just these frames to verify sources resolve**

From site root:
```bash
python - <<'PY'
import sys; sys.path.insert(0, "scripts")
import generate_supplemental_frames as g
g.ensure_dirs()
mcst = g.ROOT / "PDPA ACT and Advisory/Advisory Guidelines for Management Corporations 17 May 2022.pdf"
kc = g.ROOT / "PDPA ACT and Advisory/Advisory Guidelines on Key Concepts in the PDPA 17 May 2022.pdf"
g.render_pdf_source("source/scene03_mcst_guideline_police.png", "Access Is Not Police-Only", mcst,
                    ["may not limit the provision of access", "law enforcement"], "Advisory Guidelines for Management Corporations")
g.render_pdf_source("source/scene06_key_concepts_identifiability.png", "Personal Data, Not Narrowly Construed", kc,
                    ["not intended to be narrowly construed", "from which an individual can be identified"], "Advisory Guidelines on Key Concepts in the PDPA")
g.image_frame("source/scene06_masking_still_identifiable.png", "Masking Can Still Be Identifiable", g.SITE_ROOT / "pdpa-masking-42.png", "Selected Topics Guidelines, para 4.58-4.59 (page 42)")
g.image_frame("source/scene02_tst_streetview_cameras.png", "The Scotts Tower CCTV, Facing The Road", g.SITE_ROOT / "TST CCTV GoogleMap.png", "Contemporaneous CCTV-location evidence (Google Street View)")
g.image_frame("source/scene02_tst_accident_location.png", "Camera Coverage Of The Accident Location", g.SITE_ROOT / "TST CCTV 2  GoogleMap accident location.png", "Contemporaneous CCTV-location evidence (Google Street View)")
print("OK: guideline + masking + streetview frames rendered")
PY
```
Expected: `OK: ...`. If the MCST guideline term does not match, open that PDF, find the exact "law enforcement / police" access-limitation sentence, and adjust `search_terms`.

- [ ] **Step 3: Spot-check the 5 PNGs**

Open each in `Screenshots Video/source/`. Confirm: guideline highlight is on the police/law-enforcement access sentence; Key Concepts highlight is on the "narrowly construed / identified" passage; masking page shows the Solid/Blur/Pixelated examples and para 4.59; both Street View frames show the condo entrance with the camera visible.

- [ ] **Step 4: Commit**

```bash
git add scripts/generate_supplemental_frames.py "Screenshots Video/source/scene03_mcst_guideline_police.png" "Screenshots Video/source/scene06_key_concepts_identifiability.png" "Screenshots Video/source/scene06_masking_still_identifiable.png" "Screenshots Video/source/scene02_tst_streetview_cameras.png" "Screenshots Video/source/scene02_tst_accident_location.png"
git commit -m "frames: add MCST guideline, masking-still-identifiable, and TST Street View location frames"
```

---

## Task 4: Add `render_email_quote` helper and 3 verbatim official-reply frames

**Files:**
- Modify: `scripts/generate_supplemental_frames.py` — add `render_email_quote()` helper and 3 calls.

**Interfaces:**
- Consumes: existing `save_card(path, title, blocks, subtitle=None, footer=None, dark=False)`.
- Produces: `render_email_quote(path, title, output_dir, quote, verify_phrase, citation, sender_must_contain)` and frames `source/scene03_suites_dpo_reply.png`, `source/scene05_pdpc_not_channel.png`, `source/scene08_pdpc_publication_delay.png`, `source/scene09_imda_iau_finding.png`.

- [ ] **Step 1: Add the helper**

In `scripts/generate_supplemental_frames.py`, above `def main():`, add:

```python
import re

EMAIL_EXPORTS = Path(r"C:/Users/limzi/Documents/AntiGravity/PDPC Emails/output")


def _norm(text):
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()


def render_email_quote(path, title, output_dir, quote, verify_phrase, citation, sender_must_contain):
    """Render a verbatim official-reply quote card.

    Scans output_dir/*.md for a thread that (a) contains verify_phrase and
    (b) has a `### From:` line whose address contains sender_must_contain,
    guaranteeing the quote comes from an official reply rather than the
    Complainant quoting it back. Fails loud if no such file is found or the
    full quote is not present verbatim.
    """
    needle = _norm(verify_phrase)
    quote_norm = _norm(quote)
    match_file = None
    for md in sorted(Path(output_dir).glob("*.md"), reverse=True):
        text = md.read_text(encoding="utf-8", errors="ignore")
        norm = _norm(text)
        if needle not in norm:
            continue
        from_lines = re.findall(r"^###\s+From:.*$", text, re.M)
        if any(sender_must_contain.lower() in fl.lower() for fl in from_lines):
            if quote_norm not in norm:
                raise SystemExit(
                    f"[render_email_quote] {path}: verify_phrase matched in {md.name} "
                    f"but full quote not present verbatim"
                )
            match_file = md
            break
    if match_file is None:
        raise SystemExit(
            f"[render_email_quote] {path}: no export in {output_dir} contains "
            f"{verify_phrase!r} from sender {sender_must_contain!r}"
        )
    save_card(path, title, [{"kind": "quote", "text": quote}],
              subtitle="Verbatim official reply", footer=citation)
    return match_file.name
```

- [ ] **Step 2: Add the 3 verbatim-reply calls**

In `main()`, after the Task 3 calls, add:

```python
    render_email_quote(
        "source/scene03_suites_dpo_reply.png", "The DPO's Written Refusal", EMAIL_EXPORTS,
        quote="Only by police direct/order the MCST to disclose the footage that MCST is obliged to do so.",
        verify_phrase="police direct",
        citation="Email, Property Facility Services (MCST 3615 managing agent), 21 May 2024",
        sender_must_contain="pfspl.com.sg")
    render_email_quote(
        "source/scene05_pdpc_not_channel.png", "PDPC's Channel Reasoning", EMAIL_EXPORTS,
        quote="An access request made under section 21 of the PDPA is not the appropriate channel.",
        verify_phrase="not the appropriate channel",
        citation="Email from PDPC, 2024",
        sender_must_contain="pdpc.gov.sg")
    render_email_quote(
        "source/scene08_pdpc_publication_delay.png", "Publication Delay", EMAIL_EXPORTS,
        quote="We are unable to commit to a fixed date at this point.",
        verify_phrase="unable to commit to a fixed date",
        citation="Email from PDPC, 23 June 2025",
        sender_must_contain="pdpc.gov.sg")
    render_email_quote(
        "source/scene08_pdpc_guidelines_prevail.png", "PDPC's Guideline-Conflict Reply", EMAIL_EXPORTS,
        quote="the guidelines do not constitute legal advice, and do not modify or supplement the PDPA, which shall prevail over the guidelines in the event of any inconsistency.",
        verify_phrase="shall prevail over the guidelines in the event of any inconsistency",
        citation="Email from Boon Pin Goh (PDPC), reply to feedback, 2025",
        sender_must_contain="pdpc.gov.sg")
    image_frame(
        "source/scene04_pdpc_s22a_admission.png", "PDPC Admits The s.22A Preservation Gap",
        ROOT / "PDPC Complain/Follow Up/3) PDPC claim own guideline wrong and loophole in PDPA.png",
        "Email from Boon Pin Goh (PDPC), reply to feedback (2025), paras 12-13")
    render_email_quote(
        "source/scene09_imda_iau_finding.png", "IAU Finding", EMAIL_EXPORTS,
        quote="the PDPC and its officers did not commit any wrongful practices.",
        verify_phrase="did not commit any wrongful practices",
        citation="Email from Wan Ling Yeong, IMDA Internal Audit Unit, 20 August 2025",
        sender_must_contain="imda.gov.sg")
    render_email_quote(
        "source/scene09_imda_protocols.png", "IAU: Acted In Accordance With Protocols", EMAIL_EXPORTS,
        quote="PDPC acted in accordance with its protocols in its engagements with you on the matter.",
        verify_phrase="acted in accordance with its protocols",
        citation="Email from Wan Ling Yeong, IMDA Internal Audit Unit, 20 August 2025",
        sender_must_contain="imda.gov.sg")
```

This last frame is the source-disciplined **replacement for the dropped `scene09_letter_to_imda_ceo`** (which was the Complainant's own letter). It is a verbatim IMDA finding, so it keeps Scene 9's coverage while honouring the "official sources only" rule.

- [ ] **Step 3: Render the 4 verbatim frames and confirm the sender guard passes**

From site root:
```bash
python - <<'PY'
import sys; sys.path.insert(0, "scripts")
import generate_supplemental_frames as g
g.ensure_dirs()
print(g.render_email_quote("source/scene03_suites_dpo_reply.png", "The DPO's Written Refusal", g.EMAIL_EXPORTS,
    "Only by police direct/order the MCST to disclose the footage that MCST is obliged to do so.",
    "police direct", "Email, Property Facility Services (MCST 3615 managing agent), 21 May 2024", "pfspl.com.sg"))
print(g.render_email_quote("source/scene05_pdpc_not_channel.png", "PDPC's Channel Reasoning", g.EMAIL_EXPORTS,
    "An access request made under section 21 of the PDPA is not the appropriate channel.",
    "not the appropriate channel", "Email from PDPC, 2024", "pdpc.gov.sg"))
print(g.render_email_quote("source/scene08_pdpc_publication_delay.png", "Publication Delay", g.EMAIL_EXPORTS,
    "We are unable to commit to a fixed date at this point.",
    "unable to commit to a fixed date", "Email from PDPC, 23 June 2025", "pdpc.gov.sg"))
print(g.render_email_quote("source/scene09_imda_iau_finding.png", "IAU Finding", g.EMAIL_EXPORTS,
    "the PDPC and its officers did not commit any wrongful practices.",
    "did not commit any wrongful practices", "Email from Wan Ling Yeong, IMDA Internal Audit Unit, 20 August 2025", "imda.gov.sg"))
print(g.render_email_quote("source/scene09_imda_protocols.png", "IAU: Acted In Accordance With Protocols", g.EMAIL_EXPORTS,
    "PDPC acted in accordance with its protocols in its engagements with you on the matter.",
    "acted in accordance with its protocols", "Email from Wan Ling Yeong, IMDA Internal Audit Unit, 20 August 2025", "imda.gov.sg"))
print(g.render_email_quote("source/scene08_pdpc_guidelines_prevail.png", "PDPC's Guideline-Conflict Reply", g.EMAIL_EXPORTS,
    "the guidelines do not constitute legal advice, and do not modify or supplement the PDPA, which shall prevail over the guidelines in the event of any inconsistency.",
    "shall prevail over the guidelines in the event of any inconsistency", "Email from Boon Pin Goh (PDPC), reply to feedback, 2025", "pdpc.gov.sg"))
g.image_frame("source/scene04_pdpc_s22a_admission.png", "PDPC Admits The s.22A Preservation Gap",
    g.ROOT / "PDPC Complain/Follow Up/3) PDPC claim own guideline wrong and loophole in PDPA.png",
    "Email from Boon Pin Goh (PDPC), reply to feedback (2025), paras 12-13")
print("OK: s22a admission image frame rendered")
PY
```
Expected: six printed export filenames (verbatim frames), then `OK: s22a admission image frame rendered`, no `SystemExit`.

If a call raises "no export … from sender": the displayed `quote` or `verify_phrase` differs from the email wording, or the sender domain is wrong. Recovery: `grep -rl "<verify_phrase>" "C:/Users/limzi/Documents/AntiGravity/PDPC Emails/output"`, open the matching file, copy the exact sentence into `quote` and the real `### From:` domain into `sender_must_contain`, then re-run. Do NOT relax the guard to match a file authored by `limzirui@gmail.com`.

- [ ] **Step 4: Spot-check the 4 quote frames** render with the correct citation footer and readable quote.

- [ ] **Step 5: Commit**

```bash
git add scripts/generate_supplemental_frames.py "Screenshots Video/source/scene03_suites_dpo_reply.png" "Screenshots Video/source/scene05_pdpc_not_channel.png" "Screenshots Video/source/scene08_pdpc_publication_delay.png" "Screenshots Video/source/scene08_pdpc_guidelines_prevail.png" "Screenshots Video/source/scene04_pdpc_s22a_admission.png" "Screenshots Video/source/scene09_imda_iau_finding.png" "Screenshots Video/source/scene09_imda_protocols.png"
git commit -m "frames: add verbatim official-reply frames (DPO, PDPC channel/guideline/publication, s.22A admission, IMDA IAU x2) with sender guard"
```

---

## Task 5: Repoint Gemini frames and remove superseded placeholders

**Files:**
- Modify: `scripts/generate_supplemental_frames.py` — remove 3 `save_simple_generated()` calls.
- Modify: `scripts/video_visuals.py` — `VISUAL_SCHEDULE` Gemini remaps (done fully in Task 6; this task only removes the dead generator calls).

**Interfaces:**
- Consumes: the 5 user-generated Gemini PNGs already present in `Screenshots Video/generated/` (`scene02_memory_gap.png`, `scene03_office_refusal.png`, `scene06_clarity_machine.png`, `scene11_citizen_pattern.png`, `scene13_evidence_wall.png`).
- Produces: generator no longer emits the 3 superseded crude placeholders.

- [ ] **Step 1: Remove the 3 superseded `save_simple_generated` calls**

In `main()`, delete these three lines (the Gemini frames replace them):
```python
    save_simple_generated("generated/scene02_hospital_memory_gap.png", "Memory Gap", "Prompt: hospital bed, 05:06, quiet memory loss, no detailed face.", "hospital")
    save_simple_generated("generated/scene03_management_office_refusal.png", "Management Office Refusal", "Prompt: figure at tall management counter, no company name, no DPO, no escalation.", "office")
    save_simple_generated("generated/scene06_evidence_to_clarity_test.png", "Evidence Turned Into Clarity Test", "Prompt: handphone video fed into institutional machine labelled clarity test.", "machine")
```
Also delete the now-unused `generated/scene02_cairnhill_cctv_corridor.png` call (its schedule slot becomes the real Street View frame in Task 6):
```python
    save_simple_generated("generated/scene02_cairnhill_cctv_corridor.png", "Cairnhill Road CCTV Corridor", "Prompt: pre-dawn road flanked by condominiums, CCTV cameras, motorcycle helmet.", "road")
```
Keep the two remaining `save_simple_generated` calls (`scene03_management_office_refusal` is removed; `generated/scene13_citizen_evidence_wall.png` — see note). Note: the existing script also emits `generated/scene13_citizen_evidence_wall.png`; the user's Gemini file is `scene13_evidence_wall.png`. Leave the old `scene13_citizen_evidence_wall` call in place only if still scheduled; Task 6 repoints Scene 13 to `scene13_evidence_wall.png`, so also remove the `scene13_citizen_evidence_wall` call. Confirm by grepping which `generated/*` names remain referenced after Task 6.

- [ ] **Step 2: Confirm the 5 Gemini files exist**

Run:
```bash
ls "Screenshots Video/generated/" | grep -E "scene02_memory_gap|scene03_office_refusal|scene06_clarity_machine|scene11_citizen_pattern|scene13_evidence_wall"
```
Expected: all 5 filenames listed.

- [ ] **Step 3: Commit**

```bash
git add scripts/generate_supplemental_frames.py
git commit -m "frames: drop crude placeholder generators superseded by Gemini frames"
```

---

## Task 6: Wire everything into VISUAL_SCHEDULE and run the full generator

**Files:**
- Modify: `scripts/video_visuals.py` — `VISUAL_SCHEDULE`.
- Run: `scripts/generate_supplemental_frames.py`.

**Interfaces:**
- Consumes: all frames from Tasks 1–5.
- Produces: a schedule where every new frame appears at its `at` position and `find_missing_visual_assets` passes.

- [ ] **Step 1: Apply the 3 Gemini filename remaps**

In `scripts/video_visuals.py`, in `VISUAL_SCHEDULE`, change the frame strings:
- Scene 2 `at 0.00`: `generated/scene02_hospital_memory_gap.png` → `generated/scene02_memory_gap.png`
- Scene 3 `at 0.26`: `generated/scene03_management_office_refusal.png` → `generated/scene03_office_refusal.png`
- Scene 6 `at 0.15`: `generated/scene06_evidence_to_clarity_test.png` → `generated/scene06_clarity_machine.png`

- [ ] **Step 2: Replace the Scene 2 corridor slot and add the Street View + reflow**

Scene 2 entries become (replace the existing scene-2 block):
```python
    {"scene": 2, "frame": "generated/scene02_memory_gap.png", "at": 0.00},
    {"scene": 2, "frame": "source/scene02_tst_streetview_cameras.png", "at": 0.20},
    {"scene": 2, "frame": "Scene 2.png", "at": 0.40},
    {"scene": 2, "frame": "source/scene02_tst_cctv_location.png", "at": 0.58},
    {"scene": 2, "frame": "source/scene02_tst_accident_location.png", "at": 0.70},
    {"scene": 2, "frame": "source/scene02_suites_cctv_location.png", "at": 0.85},
```

- [ ] **Step 3: Update Scene 3 (verbatim DPO reply, guideline insert)**

Replace the Scene 3 block with:
```python
    {"scene": 3, "frame": "recreated/scene03_tst_refusal.png", "at": 0.00},
    {"scene": 3, "frame": "recreated/scene03_no_company_dpo_escalation.png", "at": 0.13},
    {"scene": 3, "frame": "generated/scene03_office_refusal.png", "at": 0.26},
    {"scene": 3, "frame": "source/scene03_suites_dpo_reply.png", "at": 0.40},
    {"scene": 3, "frame": "Scene 3.png", "at": 0.55},
    {"scene": 3, "frame": "recreated/scene03_difficulty_understanding.png", "at": 0.68},
    {"scene": 3, "frame": "source/scene03_mcst_guideline_police.png", "at": 0.80},
    {"scene": 3, "frame": "source/scene03_pdpa_s21_fifth_schedule.png", "at": 0.90},
```

- [ ] **Step 4: Add s.22A statute + PDPC admission to Scene 4**

Replace the Scene 4 block so it reads (adds the statute frame and the PDPC s.22A-gap admission as a one-two at the "s.22A became useless" beat; `scene04_s22a_no_finding.png` moves 0.78 → 0.68):
```python
    {"scene": 4, "frame": "source/scene04_cctv_captured_not_downloaded.png", "at": 0.00},
    {"scene": 4, "frame": "Scene 4.png", "at": 0.25},
    {"scene": 4, "frame": "source/scene04_17_day_overwrite.png", "at": 0.50},
    {"scene": 4, "frame": "source/scene04_s22a_no_finding.png", "at": 0.68},
    {"scene": 4, "frame": "source/scene04_pdpa_s22a.png", "at": 0.80},
    {"scene": 4, "frame": "source/scene04_pdpc_s22a_admission.png", "at": 0.92},
```

- [ ] **Step 5: Update Scene 6 (masking insert, Key Concepts replace)**

Replace the Scene 6 block's tail so it reads:
```python
    {"scene": 6, "frame": "source/scene06_mcst3615_silhouette.png", "at": 0.00},
    {"scene": 6, "frame": "generated/scene06_clarity_machine.png", "at": 0.15},
    {"scene": 6, "frame": "source/scene06_pdpa_personal_data_definition.png", "at": 0.32},
    {"scene": 6, "frame": "source/scene06_no_minimum_resolution.png", "at": 0.48},
    {"scene": 6, "frame": "source/scene06_still_frames_actual_footage.png", "at": 0.62},
    {"scene": 6, "frame": "source/scene06_masking_still_identifiable.png", "at": 0.72},
    {"scene": 6, "frame": "scene 6.jpg", "at": 0.82},
    {"scene": 6, "frame": "source/scene06_key_concepts_identifiability.png", "at": 0.92},
```
(Removes the `recreated/scene06_identifiability_not_clarity.png` slot, replaced by the real Key Concepts guideline.)

- [ ] **Step 6: Update Scene 8 (s.4 insert, two verbatim replaces)**

In the Scene 8 block:
- Insert after the `at 0.21` entry: `{"scene": 8, "frame": "source/scene08_pdpa_s4_2_4_3.png", "at": 0.28},`
- Replace `recreated/scene08_repeated_one_line_response.png` (`at 0.45`) with `source/scene08_pdpc_guidelines_prevail.png` (the recovered verbatim para-12 reply).
- Replace `recreated/scene08_publication_delay.png` (`at 0.62`) with `source/scene08_pdpc_publication_delay.png`.

- [ ] **Step 7: Update Scene 9 (IAU finding + protocols replacements)**

- Replace `recreated/scene09_no_wrongful_practices.png` (`at 0.60`) with `source/scene09_imda_iau_finding.png`.
- Replace `recreated/scene09_final_conclusive.png` (`at 0.90`) with `source/scene09_imda_protocols.png` (the dropped-frame replacement).
- Leave `recreated/scene09_imda_escalation.png` at 0.00 unchanged (the escalation letter is the Complainant's own and stays a recreated card).

- [ ] **Step 8: Add s.24 / s.25 to Scene 10 and reflow**

In the Scene 10 block, after `source/scene10_protection_204_crop.png` (`at 0.73`), set:
```python
    {"scene": 10, "frame": "source/scene10_pdpa_s24_protection.png", "at": 0.80},
    {"scene": 10, "frame": "source/scene10_pdpa_s25_retention.png", "at": 0.86},
    {"scene": 10, "frame": "recreated/scene10_two_cctv_cases.png", "at": 0.93},
```
(The last line moves `two_cctv_cases` from 0.88 to 0.93.)

- [ ] **Step 9: Add Gemini frames to Scenes 11 and 13**

- Scene 11: insert `{"scene": 11, "frame": "generated/scene11_citizen_pattern.png", "at": 0.20},` after the `at 0.00` entry.
- Scene 13: open the Scene 13 block, note its existing entries and hero position, then insert `{"scene": 13, "frame": "generated/scene13_evidence_wall.png", "at": <before the closing text-card hero>},`. If Scene 13's hero `scene 13.png` is at some `at` value H, place the evidence wall at `H - 0.15` (clamped ≥ 0.0). Remove any lingering `generated/scene13_citizen_evidence_wall.png` schedule entry.

- [ ] **Step 10: Run the full generator (must pass find_missing_visual_assets)**

From site root:
```bash
python scripts/generate_supplemental_frames.py
```
Expected final line: `Generated supplemental assets. Scheduled visuals: <N>` and **no** `SystemExit("Missing scheduled assets: …")`. If it lists missing assets, the schedule references a frame name that no generator call produces (or vice versa) — reconcile the name exactly between `video_visuals.py` and the generator call.

- [ ] **Step 11: Sanity-check the schedule has no duplicate `at` collisions per scene**

Run:
```bash
python - <<'PY'
import sys; sys.path.insert(0, "scripts")
from video_visuals import VISUAL_SCHEDULE
from collections import defaultdict
seen = defaultdict(list)
for e in VISUAL_SCHEDULE:
    seen[e["scene"]].append(e["at"])
for scene, ats in sorted(seen.items()):
    dupes = [a for a in ats if ats.count(a) > 1]
    assert not dupes, f"scene {scene} duplicate at: {sorted(set(dupes))}"
    assert ats == sorted(ats), f"scene {scene} not in ascending at order: {ats}"
print("OK: schedule ordered, no per-scene at collisions")
PY
```
Expected: `OK: schedule ordered, no per-scene at collisions`. Fix any reported scene by nudging an `at` by 0.02.

- [ ] **Step 12: Commit**

```bash
git add scripts/video_visuals.py scripts/generate_supplemental_frames.py "Screenshots Video/source" "Screenshots Video/generated"
git commit -m "schedule: wire supplemental frames into VISUAL_SCHEDULE (statute, verbatim, guideline, streetview, Gemini)"
```

---

## Task 7: Re-render via /script-to-video (burned + non-burned outputs)

**Files:**
- Run: `scripts/finalize_with_script_subs.py` (existing Path E assembler: ASR-timed, script-words subtitle text).
- Produces: `video_export/PDPC_grievance_video.mp4` (burned subtitles), `video_export/PDPC_grievance_video_nosubs.mp4` (clean), `video_export/subtitles.srt` (sidecar).

**Interfaces:**
- Consumes: the updated `VISUAL_SCHEDULE`, all frames from Tasks 1–6, the existing cleaned audio WAV and corrected-SRT source the finalize script already references (`video_export/subtitles_corrected.srt`).
- Produces: two MP4 variants + one SRT.

**Context:** This is the `/script-to-video` Path E workflow (own_voice, pre-cleaned audio, ASR-aligned subtitles, script-text substitution). The audio and scene/ASR alignment are unchanged by this plan — only *which frames show at which times* changed via `VISUAL_SCHEDULE`. So re-running the assembler regenerates the per-scene clips against the new schedule; whisper does not need to re-run if the segments JSON is cached. Do not re-transcribe unless the audio changed.

- [ ] **Step 1: Confirm audio + corrected-SRT inputs still exist**

Run (from site root):
```bash
ls -la video_export/subtitles_corrected.srt 2>/dev/null; python - <<'PY'
import sys; sys.path.insert(0,"scripts")
import finalize_with_script_subs as f
print("audio:", f.AUDIO if hasattr(f,"AUDIO") else "see script constants")
PY
```
Expected: the corrected-SRT deliverable source is present. If missing, the audio pipeline must be run first (out of scope for this plan — coordinate with the user; the script-to-video skill Path E Steps 1–4 cover producing it).

- [ ] **Step 2: Run the burned-subtitle assembly**

```bash
python -u scripts/finalize_with_script_subs.py
```
Expected: `[SRT-ASR] N cues parsed`, per-scene clip logs, and `video_export/PDPC_grievance_video.mp4` written, plus the deliverable `video_export/subtitles.srt`. Spot-check that the new frames appear at their scenes (e.g. the masking page mid-Scene 6, the s.24/s.25 statute pages late Scene 10, the IMDA protocols frame at the end of Scene 9).

- [ ] **Step 3: Produce the non-burned (clean) variant**

The finalize build leaves a pre-subtitle concat (`video_no_audio.mp4`) in its build directory. Mux that with the audio, *without* the `subtitles=` filter, to make the clean version. Run:
```bash
python - <<'PY'
import sys, subprocess; sys.path.insert(0,"scripts")
import finalize_with_script_subs as f
build = f.BUILD_DIR
video_no_audio = build / "video_no_audio.mp4"
audio = f.AUDIO  # the cleaned WAV constant used by the finalize script
out = f.ROOT / "video_export" / "PDPC_grievance_video_nosubs.mp4"
assert video_no_audio.exists(), f"missing {video_no_audio} — run Step 2 first"
cmd = ["ffmpeg","-y","-i",str(video_no_audio),"-i",str(audio),
       "-map","0:v:0","-map","1:a:0",
       "-c:v","libx264","-pix_fmt","yuv420p","-preset","fast","-crf","20",
       "-c:a","aac","-b:a","192k","-shortest", str(out)]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stderr[-600:] if r.returncode else f"OK: {out}")
PY
```
Expected: `OK: …/PDPC_grievance_video_nosubs.mp4`. If `f.AUDIO` / `f.BUILD_DIR` are named differently in the script, open `scripts/finalize_with_script_subs.py`, read the constants block (near the `SRT_SRC`/`FINAL_OUT` definitions), and substitute the correct names.

- [ ] **Step 4: Verify both outputs**

```bash
ls -la video_export/PDPC_grievance_video.mp4 video_export/PDPC_grievance_video_nosubs.mp4 video_export/subtitles.srt
```
Expected: all three present, both MP4s non-trivial size. Open the clean variant and confirm it has audio but no burned subtitles; open the burned variant and confirm subtitles are visible and word-synced; load `subtitles.srt` against the clean variant in a player to confirm the sidecar aligns.

- [ ] **Step 5: Commit the deliverables**

```bash
git add video_export/PDPC_grievance_video.mp4 video_export/PDPC_grievance_video_nosubs.mp4 video_export/subtitles.srt
git commit -m "video: re-render with supplemental frames; burned + non-burned outputs + SRT sidecar"
```

Note: MP4s are large. If the repo should not carry binaries, skip the commit and hand the files to the user directly, or add `video_export/*.mp4` to `.gitignore` and commit only `subtitles.srt`.

---

## Self-Review Notes

- **Spec coverage:** Tier A (Task 2), Tier B verbatim replies (Task 4), Tier C guideline + masking (Task 3), Tier C2 Street View (Task 3), Gemini remaps + Scene 11/13 (Tasks 5–6), TST photo copy (Task 1), VISUAL_SCHEDULE integration (Task 6). Covered.
- **Deviation from spec (intentional, source-discipline):** `scene09_letter_to_imda_ceo` dropped (Complainant's own letter) and **replaced** by verbatim `source/scene09_imda_protocols.png` from the official IAU email.
- **Correction to an earlier finding:** the Scene 8 one-line reply IS sourceable. The script paraphrases it as "Guidelines are not determinative; the PDPA takes precedence," but PDPC's actual words (from Boon Pin Goh, `pdpc.gov.sg`) are "the guidelines do not constitute legal advice, and do not modify or supplement the PDPA, which shall prevail over the guidelines in the event of any inconsistency." Rendered verbatim as `source/scene08_pdpc_guidelines_prevail.png` (Scene 8 · 0.45). The same email's next paragraph is PDPC's written **admission of the s.22A preservation gap** ("s 22A of the PDPA as worded does not require Organisations to preserve personal data … we are aware and presently reviewing this issue, which we will raise to the Ministry"), added as `source/scene04_pdpc_s22a_admission.png` (Scene 4 · 0.92) from the real screenshot `PDPC Complain/Follow Up/3) PDPC claim own guideline wrong and loophole in PDPA.png` (Failure #3 primary source).
- **New requirement — dual outputs (Task 7):** burned (`PDPC_grievance_video.mp4`) and non-burned (`PDPC_grievance_video_nosubs.mp4`) plus `subtitles.srt` sidecar, produced through the `/script-to-video` Path E finalize workflow. The frame changes flow automatically because `finalize_with_script_subs.py` reads `VISUAL_SCHEDULE`.
- **Type consistency:** `render_email_quote(path, title, output_dir, quote, verify_phrase, citation, sender_must_contain)` signature is identical in the helper definition (Task 4 Step 1) and all call sites (Task 4 Step 2). `render_pdf_source(path, title, pdf_path, search_terms, footer)` and `image_frame(path, title, src, footer)` unchanged from the existing module.
- **Fail-loud:** statute frames raise on unmatched terms (Task 2); verbatim frames raise unless the quote is present verbatim from an official sender domain (Task 4).
