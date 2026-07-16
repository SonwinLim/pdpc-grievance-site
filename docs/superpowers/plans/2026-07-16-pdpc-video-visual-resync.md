# PDPC Video Visual Resync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace percentage-based frame timing with a reviewed cue-anchored schedule, add approved documentary visuals, and assemble a fully resynchronised no-subtitles PDPC grievance video without changing its narration.

**Architecture:** Preserve `frame_mapping_actual.xlsx` as the baseline and create `frame_mapping_resync.xlsx` as the reviewed source of truth. A focused cue compiler reads the workbook, validates all 318 narration cues, collapses consecutive identical assignments into explicit segments, and feeds the existing FFmpeg renderer. Primary-source assets remain real; Codex image generation is limited to approved documentary and narrator frames.

**Tech Stack:** Python 3.13, `openpyxl`, `dataclasses`, `unittest`, FFmpeg/ffprobe, Codex image generation, MP4/H.264/AAC.

---

## File structure

- Create `scripts/cue_visuals.py`: workbook parsing, cue assignment validation, segment compilation, and audit metrics.
- Create `scripts/prepare_visual_resync_workbook.py`: copy the baseline workbook, add review columns, validations, and corrected scene boundaries.
- Create `scripts/render_cue_video.py`: render cue-anchored segments, proof clips, and final no-subtitles output.
- Create `scripts/report_visual_resync.py`: write the final Markdown audit report from the reviewed workbook.
- Create `tests/test_cue_visuals.py`: compiler and validation intent tests.
- Create `tests/test_prepare_visual_resync_workbook.py`: workbook preservation and schema tests.
- Create `tests/test_render_cue_video.py`: command construction and locked-output tests.
- Create `video_export/frame_mapping_resync.xlsx`: reviewed visual source of truth.
- Create `Screenshots Video/codex_generated/`: approved documentary frame outputs.
- Create `video_export/PDPC_grievance_visual_review.mp4`: proof-frame review excerpt.
- Create `video_export/PDPC_grievance_video_resynced_nosubs.mp4`: final clean video.
- Create `docs/superpowers/plans/2026-07-16-pdpc-video-visual-resync-report.md`: acceptance report.
- Modify `scripts/prepare_review_frames.py`: read the reviewed workbook instead of `VISUAL_SCHEDULE`.
- Leave `scripts/video_visuals.py` and its legacy percentage schedule intact for recovery and comparison.

## Locked constants

```python
ROOT = Path(r"D:/Driving Legal Issue/pdpc-grievance-site")
BASELINE_XLSX = ROOT / "video_export/frame_mapping_actual.xlsx"
REVIEWED_XLSX = ROOT / "video_export/frame_mapping_resync.xlsx"
FRAMES_ROOT = ROOT / "Screenshots Video"
AUDIO_SOURCE = ROOT / "video_export/PDPC_grievance_video_nosubs.mp4"
FINAL_OUT = ROOT / "video_export/PDPC_grievance_video_resynced_nosubs.mp4"
LOCKED_DURATION_S = 1387.666667
WIDTH, HEIGHT, FPS = 1920, 1080, 30
```

### Task 1: Specify cue compiler behaviour with failing tests

**Files:**
- Create: `tests/test_cue_visuals.py`
- Create later: `scripts/cue_visuals.py`

- [ ] **Step 1: Write the failing unit tests**

```python
import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from scripts.cue_visuals import (
    CueScheduleError,
    compile_segments,
    load_assignments,
    validate_assignments,
)


HEADERS = [
    "Cue #", "Start", "End", "Duration (s)", "Scene #", "Frame", "URL",
    "Narrative", "Status", "Anchor phrase", "Visual type",
    "Source/reference path", "Review rationale", "Approved",
]


def workbook(rows):
    tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    tmp.close()
    wb = Workbook()
    ws = wb.active
    ws.title = "Frames"
    ws.append(HEADERS)
    for row in rows:
        ws.append(row)
    wb.save(tmp.name)
    return Path(tmp.name)


class CueVisualsTest(unittest.TestCase):
    def test_consecutive_cues_using_same_frame_collapse_at_cue_boundaries(self):
        path = workbook([
            [1, "00:00:03.000", "00:00:08.000", 5, 1, "a.png", "", "alpha words", "Keep", "alpha", "hero", "a.png", "correct", True],
            [2, "00:00:08.000", "00:00:12.000", 4, 1, "a.png", "", "more alpha", "Hold", "", "hero", "a.png", "intentional", True],
            [3, "00:00:12.000", "00:00:18.000", 6, 1, "b.png", "", "beta words", "Add", "beta", "primary source", "b.png", "new subject", True],
        ])
        segments = compile_segments(load_assignments(path), cover_frame="cover page.png")
        self.assertEqual([s.frame for s in segments], ["cover page.png", "a.png", "b.png"])
        self.assertEqual(segments[1].start_s, 3.0)
        self.assertEqual(segments[1].end_s, 12.0)
        self.assertEqual(segments[2].start_s, 12.0)

    def test_anchor_phrase_must_exist_on_transition_cue(self):
        path = workbook([
            [1, "00:00:03.000", "00:00:08.000", 5, 1, "a.png", "", "alpha words", "Keep", "missing", "hero", "a.png", "correct", True],
        ])
        with self.assertRaisesRegex(CueScheduleError, "anchor phrase"):
            validate_assignments(load_assignments(path), frames_root=Path("."), check_files=False)

    def test_all_rows_must_be_approved(self):
        path = workbook([
            [1, "00:00:03.000", "00:00:08.000", 5, 1, "a.png", "", "alpha words", "Keep", "alpha", "hero", "a.png", "correct", False],
        ])
        with self.assertRaisesRegex(CueScheduleError, "not approved"):
            validate_assignments(load_assignments(path), frames_root=Path("."), check_files=False)

    def test_long_hold_requires_written_justification(self):
        path = workbook([
            [1, "00:00:03.000", "00:00:33.500", 30.5, 1, "a.png", "", "alpha words", "Keep", "alpha", "primary source", "a.png", "", True],
        ])
        with self.assertRaisesRegex(CueScheduleError, "long hold"):
            validate_assignments(load_assignments(path), frames_root=Path("."), check_files=False)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify the module is missing**

Run:

```powershell
python -m unittest tests.test_cue_visuals -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.cue_visuals'`.

- [ ] **Step 3: Commit the intent tests**

```powershell
git add tests/test_cue_visuals.py
git commit -m "test: specify cue-anchored visual schedule"
```

### Task 2: Implement cue parsing, validation, and segment compilation

**Files:**
- Create: `scripts/cue_visuals.py`
- Test: `tests/test_cue_visuals.py`

- [ ] **Step 1: Implement the focused compiler**

```python
from dataclasses import dataclass
from pathlib import Path

from openpyxl import load_workbook


REQUIRED_HEADERS = {
    "Cue #", "Start", "End", "Scene #", "Frame", "Narrative", "Status",
    "Anchor phrase", "Visual type", "Source/reference path",
    "Review rationale", "Approved",
}
VALID_STATUS = {"Keep", "Retime", "Replace", "Add", "Hold"}


class CueScheduleError(ValueError):
    pass


@dataclass(frozen=True)
class CueAssignment:
    cue: int
    start_s: float
    end_s: float
    scene: int
    frame: str
    narrative: str
    status: str
    anchor: str
    visual_type: str
    source_path: str
    rationale: str
    approved: bool


@dataclass(frozen=True)
class VisualSegment:
    scene: int
    frame: str
    start_s: float
    end_s: float
    start_cue: int
    end_cue: int
    visual_type: str
    rationale: str


def time_s(value):
    text = str(value)
    h, m, s = text.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def load_assignments(path):
    ws = load_workbook(path, data_only=True, read_only=True)["Frames"]
    headers = {cell.value: i for i, cell in enumerate(ws[1])}
    missing = REQUIRED_HEADERS - headers.keys()
    if missing:
        raise CueScheduleError(f"missing columns: {sorted(missing)}")
    out = []
    for values in ws.iter_rows(min_row=2, values_only=True):
        get = lambda name: values[headers[name]]
        out.append(CueAssignment(
            cue=int(get("Cue #")), start_s=time_s(get("Start")), end_s=time_s(get("End")),
            scene=int(get("Scene #")), frame=str(get("Frame") or "").strip(),
            narrative=str(get("Narrative") or "").strip(), status=str(get("Status") or "").strip(),
            anchor=str(get("Anchor phrase") or "").strip(), visual_type=str(get("Visual type") or "").strip(),
            source_path=str(get("Source/reference path") or "").strip(),
            rationale=str(get("Review rationale") or "").strip(), approved=bool(get("Approved")),
        ))
    return out


def validate_assignments(items, frames_root, check_files=True):
    if not items or items[0].cue != 1:
        raise CueScheduleError("cue 1 must be present")
    current = ""
    transition_start = None
    for i, item in enumerate(items):
        if item.cue != i + 1:
            raise CueScheduleError(f"cue sequence breaks at {item.cue}")
        if not item.approved:
            raise CueScheduleError(f"cue {item.cue} is not approved")
        if item.status not in VALID_STATUS:
            raise CueScheduleError(f"cue {item.cue} has invalid status {item.status!r}")
        frame = item.frame or current
        if not frame:
            raise CueScheduleError(f"cue {item.cue} has no effective frame")
        if frame != current:
            if item.anchor and item.anchor.casefold() not in item.narrative.casefold():
                raise CueScheduleError(f"cue {item.cue} anchor phrase is absent")
            if check_files and not (frames_root / frame).exists():
                raise CueScheduleError(f"cue {item.cue} frame missing: {frame}")
            current, transition_start = frame, item.start_s
        if item.end_s - transition_start > 25 and not item.rationale:
            raise CueScheduleError(f"cue {item.cue} long hold lacks justification")


def compile_segments(items, cover_frame=None):
    segments = []
    if cover_frame and items[0].start_s > 0:
        segments.append(VisualSegment(0, cover_frame, 0.0, items[0].start_s, 0, 0, "cover", "pre-roll"))
    current = None
    start = None
    start_cue = None
    meta = None
    for item in items:
        frame = item.frame or current
        if frame != current:
            if current is not None:
                segments.append(VisualSegment(meta.scene, current, start, item.start_s, start_cue, item.cue - 1, meta.visual_type, meta.rationale))
            current, start, start_cue, meta = frame, item.start_s, item.cue, item
    last = items[-1]
    segments.append(VisualSegment(meta.scene, current, start, last.end_s, start_cue, last.cue, meta.visual_type, meta.rationale))
    return segments
```

- [ ] **Step 2: Run the compiler tests**

Run:

```powershell
python -m unittest tests.test_cue_visuals -v
```

Expected: four tests PASS.

- [ ] **Step 3: Commit the compiler**

```powershell
git add scripts/cue_visuals.py tests/test_cue_visuals.py
git commit -m "feat: compile visuals from narration cues"
```

### Task 3: Create the reviewed workbook without altering the baseline

**Files:**
- Create: `scripts/prepare_visual_resync_workbook.py`
- Create: `tests/test_prepare_visual_resync_workbook.py`
- Create: `video_export/frame_mapping_resync.xlsx`
- Preserve: `video_export/frame_mapping_actual.xlsx`

- [ ] **Step 1: Write the failing workbook migration test**

```python
import tempfile
import unittest
from pathlib import Path

from openpyxl import load_workbook

from scripts.prepare_visual_resync_workbook import prepare_workbook


class PrepareWorkbookTest(unittest.TestCase):
    def test_preserves_318_cues_and_adds_review_schema(self):
        root = Path(__file__).parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "review.xlsx"
            prepare_workbook(root / "video_export/frame_mapping_actual.xlsx", out)
            wb = load_workbook(out, data_only=False)
            self.assertEqual(wb["Frames"].max_row, 319)
            headers = [c.value for c in wb["Frames"][1]]
            self.assertEqual(headers[-6:], [
                "Status", "Anchor phrase", "Visual type", "Source/reference path",
                "Review rationale", "Approved",
            ])
            self.assertEqual(wb["Frames"][296 + 1][4].value, 12)
            self.assertEqual(wb["Frames"][310 + 1][4].value, 13)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the migration test and verify failure**

Run:

```powershell
python -m unittest tests.test_prepare_visual_resync_workbook -v
```

Expected: FAIL because `prepare_visual_resync_workbook` does not exist.

- [ ] **Step 3: Implement the migration script**

```python
from copy import copy
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation


REVIEW_HEADERS = [
    "Status", "Anchor phrase", "Visual type", "Source/reference path",
    "Review rationale", "Approved",
]


def prepare_workbook(source, output):
    wb = load_workbook(source)
    ws = wb["Frames"]
    start_col = ws.max_column + 1
    for offset, header in enumerate(REVIEW_HEADERS):
        cell = ws.cell(1, start_col + offset, header)
        cell.font = copy(ws.cell(1, 8).font)
        cell.fill = copy(ws.cell(1, 8).fill)
        cell.alignment = copy(ws.cell(1, 8).alignment)
    for row in range(2, ws.max_row + 1):
        cue = int(ws.cell(row, 1).value)
        ws.cell(row, start_col, "Keep")
        ws.cell(row, start_col + 1, "")
        ws.cell(row, start_col + 2, "hero" if "Scene " in str(ws.cell(row, 6).value) else "primary source")
        ws.cell(row, start_col + 3, str(ws.cell(row, 6).value or ""))
        ws.cell(row, start_col + 4, "")
        ws.cell(row, start_col + 5, False)
        if 296 <= cue <= 309:
            ws.cell(row, 5, 12)
        if cue >= 310:
            ws.cell(row, 5, 13)
    status = DataValidation(type="list", formula1='"Keep,Retime,Replace,Add,Hold"')
    ws.add_data_validation(status)
    status.add(f"I2:I{ws.max_row}")
    output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output)


if __name__ == "__main__":
    root = Path(__file__).parents[1]
    prepare_workbook(
        root / "video_export/frame_mapping_actual.xlsx",
        root / "video_export/frame_mapping_resync.xlsx",
    )
```

- [ ] **Step 4: Run tests and create the workbook**

Run:

```powershell
python -m unittest tests.test_prepare_visual_resync_workbook -v
python scripts/prepare_visual_resync_workbook.py
```

Expected: test PASS; `frame_mapping_resync.xlsx` contains 318 cue rows and 14 columns.

- [ ] **Step 5: Open with LibreOffice only for visual verification**

Verify the original columns, hyperlinks, fonts, widths, and both existing sheets remain intact. Do not save from a `data_only=True` workbook.

- [ ] **Step 6: Commit the migration and workbook**

```powershell
git add scripts/prepare_visual_resync_workbook.py tests/test_prepare_visual_resync_workbook.py video_export/frame_mapping_resync.xlsx
git commit -m "feat: prepare reviewed cue mapping workbook"
```

### Task 4: Review and assign every cue

**Files:**
- Modify: `video_export/frame_mapping_resync.xlsx`
- Reference: `docs/superpowers/specs/2026-07-16-pdpc-video-visual-resync-design.md`

- [ ] **Step 1: Apply the mandatory cue transitions**

Use these exact minimum anchors. Existing assignments between transition cues inherit the preceding frame.

| Cue | Frame | Required reason |
|---:|---|---|
| 1 | `source/scene01_parliament_question.png` | Parliament question begins |
| 5 | `Scene 1.jpg` | Minister's answer |
| 7 | `source/scene01_preservation_penalties.png` | Criminal penalties |
| 12 | `codex_generated/scene02_hospital_memory_documentary.png` | Accident and memory loss |
| 19 | `source/scene02_tst_streetview_cameras.png` | Condominiums and cameras |
| 21 | `Scene 2.png` | Guards identify footage |
| 24 | `source/scene02_tst_cctv_location.png` | The Scotts Tower request |
| 25 | `source/scene02_tst_accident_location.png` | Direct accident view |
| 28 | `source/scene02_suites_cctv_location.png` | Evidential purpose and second angle |
| 31 | `codex_generated/scene03_management_request_documentary.png` | In-person office request |
| 39 | `Scene 3.png` | Suites begins differently |
| 48 | `source/scene03_suites_dpo_reply.png` | Written DPO refusal |
| 51 | `source/scene03_mcst_guideline_police.png` | PDPC guideline contradiction |
| 56 | `source/scene03_pdpa_s21_fifth_schedule.png` | Only statutory grounds |
| 63 | `source/scene04_cctv_captured_not_downloaded.png` | Deletion clock begins |
| 66 | `Scene 4.png` | False no-footage claim |
| 72 | `source/scene04_17_day_overwrite.png` | Retention-window dispute |
| 75 | `source/scene04_s22a_no_finding.png` | PDPC's chosen request date |
| 77 | `source/scene04_pdpa_s22a.png` | s.22A becomes useless |
| 79 | `source/scene04_pdpc_s22a_admission.png` | No breach despite deletion |
| 82 | `source/scene05_pdpc_complaint_form.png` | Complaint filed |
| 88 | `scene 5.png` | Footage was identified |
| 93 | `recreated/scene05_not_appropriate_channel.png` | Directed to police |
| 96 | `codex_generated/scene05_institutional_wait_documentary.png` | Nothing meaningful follows |
| 104 | `recreated/scene05_mp_appeal_timeline.png` | MP intervention twice |
| 107 | `recreated/scene05_will_not_look_further.png` | Deflection exhausted |
| 110 | `recreated/scene05_deletion_investigated_access_not.png` | Deletion investigation opens |
| 113 | `recreated/scene05_deletion_investigated_access_not.png` | Access right not investigated |
| 118 | `source/scene06_mcst3615_silhouette.png` | No-personal-data finding |
| 126 | `generated/scene06_clarity_machine.png` | Silhouette, face, and plate test |
| 128 | `source/scene06_pdpa_personal_data_definition.png` | Statutory definition |
| 133 | `source/scene06_key_concepts_identifiability.png` | Other information and real-world identification |
| 137 | `source/scene06_still_frames_actual_footage.png` | Evidence used against the Complainant |
| 140 | `scene 6.jpg` | Maradona analogy begins |
| 144 | `source/scene06_masking_still_identifiable.png` | Identifiability versus clarity conclusion |
| 148 | `source/scene07_mcst3615_reason_shift.png` | First substituted reasoning |
| 151 | `source/scene07_mcst4599_timeline.png` | Second condominium timeline |
| 162 | `recreated/scene07_missing_dates.png` | Earlier requests disappear |
| 168 | `recreated/scene07_actual_reasons_not_tested.png` | Stated grounds not tested |
| 171 | `source/scene07_pdpa_s21_3.png` | s.21(3) |
| 173 | `source/scene07_fifth_schedule.png` | Fifth Schedule and unlisted grounds |
| 175 | `scene 8.png` | Nine-question overview |
| 176 | `recreated/scene08_question_cluster_clarity.png` | Clarity-test question |
| 177 | `recreated/scene07_actual_reasons_not_tested.png` | Actual grounds question |
| 179 | `recreated/scene08_question_preservation.png` | Preservation questions |
| 182 | `source/scene08_pdpa_s4_2_4_3.png` | Data-intermediary authority question |
| 187 | `recreated/scene08_repeated_one_line_response.png` | Repeated response begins |
| 189 | `recreated/scene08_no_guideline_named.png` | Missing guideline and conflict |
| 193 | `source/scene08_pdpc_reasonableness.png` | Reasonableness gloss |
| 199 | `recreated/scene08_public_record_delay.png` | Findings and public record |
| 205 | `source/scene08_pdpc_publication_delay.png` | Verbatim publication reply |
| 210 | `recreated/scene08_closed_no_merits_answer.png` | Matter treated as closed |
| 213 | `recreated/scene08_wrong_decision_similarity.png` | Similarity to wrong decision |
| 222 | `recreated/scene09_imda_escalation.png` | IMDA escalation path |
| 225 | `recreated/scene09_12_emails_11_months.png` | Twelve emails and eleven months |
| 227 | `recreated/scene09_complaint_leaked_back.png` | Complaint returned to reviewed officers |
| 229 | `source/scene09_imda_iau_finding.png` | IAU finding |
| 235 | `recreated/scene09_active_police_not_listed.png` | Police investigation not a refusal ground |
| 239 | `source/scene09_imda_protocols.png` | Protocols and unnamed improvements |
| 241 | `recreated/scene09_final_conclusive.png` | Final and conclusive closure |
| 242 | `source/scene10_pdpc_register.png` | Register question begins |
| 245 | `recreated/scene10_filter_removed.png` | Obligation filter disappears |
| 247 | `codex_generated/scene11_pattern_discovery_documentary.png` | Manual review of every decision |
| 249 | `source/scene10_access_zero_crop.png` | Zero Access findings |
| 253 | `source/scene10_protection_204_crop.png` | Dominant Protection findings |
| 257 | `recreated/scene10_two_cctv_cases.png` | Only two refused-CCTV cases |
| 261 | `generated/scene06_clarity_machine.png` | Clarity test explains the pattern |
| 266 | `scene 6.jpg` | Maradona passage |
| 269 | `recreated/scene08_repeated_one_line_response.png` | PDPC one-line response |
| 275 | `recreated/scene11_ordinary_vs_same_direction.png` | Uneven error comparison |
| 277 | `generated/scene11_citizen_pattern.png` | Documented pattern |
| 280 | `Scene 11.png` | Every decision in the same direction |
| 284 | `codex_generated/scene11_pattern_discovery_documentary.png` | Shape of a policy |
| 286 | `recreated/scene11_discretion_vs_denial.png` | Discretion principle |
| 292 | `recreated/scene11_invented_reasoning_chain.png` | Active denial and invented grounds |
| 294 | `recreated/scene11_zero_breach_outcome.png` | Mechanism, outcome, non-engagement |
| 296 | `scene 12.jpg` | Website begins |
| 298 | `source/scene12_site_story.png` | Decisions and story |
| 302 | `source/scene12_site_cases_narrative.png` | Questions and narrative |
| 303 | `source/scene12_site_enforcement_index.png` | Enforcement analysis |
| 305 | `source/scene12_site_failures.png` | Timeline, contradictions, failures |
| 310 | `codex_generated/scene13_citizen_appeal_documentary.png` | Final citizen appeal begins |
| 313 | `generated/scene13_evidence_wall.png` | Public evidence and zero findings |
| 315 | `scene 13.png` | Final statutory-right question |

- [ ] **Step 2: Review every non-transition cue**

For cues 1 through 318, set `Status`, `Visual type`, `Source/reference path`, `Review rationale`, and `Approved`. Use `Hold` when the prior frame intentionally continues. Set `Anchor phrase` only on transition rows, using exact words from that row's `Narrative` cell. Do not approve a source frame unless the visual's cited content matches the narration.

- [ ] **Step 3: Validate complete coverage before generation**

Run:

```powershell
python -c "from pathlib import Path; from scripts.cue_visuals import load_assignments,validate_assignments; p=Path('video_export/frame_mapping_resync.xlsx'); a=load_assignments(p); print(len(a)); validate_assignments(a,Path('Screenshots Video'),check_files=False)"
```

Expected: `318`; no approval, anchor, status, or long-hold errors. Missing new generated assets are intentionally deferred by `check_files=False`.

- [ ] **Step 4: Commit the reviewed mapping before spending generation calls**

```powershell
git add video_export/frame_mapping_resync.xlsx
git commit -m "schedule: review all PDPC narration cues"
```

### Task 5: Generate and approve two documentary proof frames

**Files:**
- Create: `Screenshots Video/codex_generated/scene02_hospital_memory_documentary.png`
- Create: `Screenshots Video/codex_generated/scene11_pattern_discovery_documentary.png`
- Modify after review: `video_export/frame_mapping_resync.xlsx`

- [ ] **Step 1: Generate the Scene 2 proof with `$imagegen`**

Reference: `C:/Users/limzi/Documents/Linkedin Articles/Reference_images/Contemplative.png`.

Prompt:

```text
16:9 restrained documentary photojournalism. Preserve the identity, facial structure, hairstyle, and build of the illustrated reference subject, but place him in a realistic Singapore hospital room shortly after a serious road accident. Medium-wide side composition, the subject awake in bed and looking toward an empty visitor chair, subdued and disoriented rather than theatrical. A dim pre-dawn window, muted clinical light, an out-of-focus IV stand, no visible wounds, no readable monitor text, no clock, no logos. The negative space around him suggests missing memory. Keep the subject and all meaningful detail in the upper 88 percent; the bottom 12 percent is simple dark floor and bedding for subtitles. Natural 35mm documentary grain, neutral slate and warm skin palette, no typography.
```

- [ ] **Step 2: Generate the Scene 11 proof with `$imagegen`**

Reference: `C:/Users/limzi/Documents/Linkedin Articles/Reference_images/resolved.png`.

Prompt:

```text
16:9 restrained investigative documentary photojournalism. Preserve the identity, facial structure, hairstyle, and build of the illustrated reference subject. Show him at a desk in a modest Singapore home office, seen three-quarter profile, calmly reviewing a large spread of printed regulatory decisions and a laptop displaying an abstract bar-chart shape with no readable text. Several document stacks form a visible repeated pattern leading toward one empty highlighted space. The expression is resolved and analytical, not angry. Practical desk lamp, dark navy shadows, statutory-red accents only on folder tabs, realistic paper texture, subtle 35mm grain. No readable generated text, no logos, no evidence-board conspiracy strings. Keep all meaningful content in the upper 88 percent and leave the lower 12 percent visually quiet.
```

- [ ] **Step 3: Verify proof assets before user review**

Run:

```powershell
ffprobe -v error -show_entries stream=width,height -of csv=p=0 "Screenshots Video/codex_generated/scene02_hospital_memory_documentary.png"
ffprobe -v error -show_entries stream=width,height -of csv=p=0 "Screenshots Video/codex_generated/scene11_pattern_discovery_documentary.png"
```

Expected: both images report a 16:9 resolution. Visually verify identity, restraint, no fabricated text, and the bottom-clear zone.

- [ ] **Step 4: Pause for proof approval**

Present both images side by side. Do not generate the remaining narrator frames until the user approves both or requests a revision.

- [ ] **Step 5: Mark the two proof assets approved and commit**

```powershell
git add "Screenshots Video/codex_generated/scene02_hospital_memory_documentary.png" "Screenshots Video/codex_generated/scene11_pattern_discovery_documentary.png" video_export/frame_mapping_resync.xlsx
git commit -m "frames: add approved documentary proof visuals"
```

### Task 6: Generate the remaining selective narrator frames

**Files:**
- Create: `Screenshots Video/codex_generated/scene03_management_request_documentary.png`
- Create: `Screenshots Video/codex_generated/scene05_institutional_wait_documentary.png`
- Create: `Screenshots Video/codex_generated/scene13_citizen_appeal_documentary.png`

- [ ] **Step 1: Generate Scene 3 using `tensed.png`**

```text
16:9 Singapore documentary photojournalism. Preserve the reference subject's identity from tensed.png. Medium-wide view from behind the reception counter of a modern condominium management office. The subject stands calmly but tensely with a small folder in hand, asking for help; an anonymous staff silhouette is visible without identifiable features. No readable forms, logos, signage, or invented quotations. Cool office lighting, realistic glass and stone surfaces, restrained composition, subtle 35mm grain. Keep faces and action in the upper 88 percent and the lower subtitle band quiet.
```

- [ ] **Step 2: Generate Scene 5 using `Contemplative.png`**

```text
16:9 restrained documentary photojournalism. Preserve the reference subject's identity from Contemplative.png. Show him alone at a dining table at night, laptop closed, several dated envelopes and printed correspondence arranged in a small unanswered stack. A phone lies face down. The mood is institutional waiting and exhaustion, not melodrama. No readable text, no agency logos, no red-string evidence wall. Warm desk lamp against dark navy room shadows, natural 35mm grain. Keep all meaningful content in the upper 88 percent; leave the bottom 12 percent simple and dark.
```

- [ ] **Step 3: Generate Scene 13 using `resolved.png`**

```text
16:9 civic documentary portrait. Preserve the reference subject's identity from resolved.png. Medium-wide view of the subject standing at a public-library or civic-building table with an organised folder of source documents and an open laptop turned slightly toward the viewer. His expression is calm, resolved, and inviting verification, not accusatory. Background architecture is generic Singapore civic modernism with no logos or readable signs. Natural daylight, restrained navy-white-red palette, subtle 35mm grain. No readable generated text. Keep the subject and evidence in the upper 88 percent and leave the lower subtitle band quiet.
```

- [ ] **Step 4: Validate all five generated assets and full file coverage**

Run:

```powershell
python -c "from pathlib import Path; from scripts.cue_visuals import load_assignments,validate_assignments; a=load_assignments(Path('video_export/frame_mapping_resync.xlsx')); validate_assignments(a,Path('Screenshots Video'),check_files=True); print('318 cues and all assets valid')"
```

Expected: `318 cues and all assets valid`.

- [ ] **Step 5: Commit the remaining approved visuals**

```powershell
git add "Screenshots Video/codex_generated" video_export/frame_mapping_resync.xlsx
git commit -m "frames: add selective documentary narrator visuals"
```

### Task 7: Render cue-anchored video instead of scene-percentage timing

**Files:**
- Create: `tests/test_render_cue_video.py`
- Create: `scripts/render_cue_video.py`
- Modify: `scripts/prepare_review_frames.py`

- [ ] **Step 1: Write the failing renderer tests**

```python
import unittest
from pathlib import Path

from scripts.render_cue_video import build_clip_command, output_paths


class RenderCueVideoTest(unittest.TestCase):
    def test_clip_uses_locked_resolution_rate_and_exact_duration(self):
        cmd = build_clip_command(Path("frame.png"), Path("clip.mp4"), 12.345)
        joined = " ".join(map(str, cmd))
        self.assertIn("-t 12.345", joined)
        self.assertIn("-r 30", joined)
        self.assertIn("scale=1920:950", joined)
        self.assertIn("pad=1920:1080", joined)

    def test_output_does_not_overwrite_baseline(self):
        final, review = output_paths(Path("video_export"))
        self.assertEqual(final.name, "PDPC_grievance_video_resynced_nosubs.mp4")
        self.assertEqual(review.name, "PDPC_grievance_visual_review.mp4")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify failure**

Run:

```powershell
python -m unittest tests.test_render_cue_video -v
```

Expected: FAIL because `render_cue_video` does not exist.

- [ ] **Step 3: Implement the cue renderer**

Implement these public functions in `scripts/render_cue_video.py`:

```python
def output_paths(export_dir):
    return (
        export_dir / "PDPC_grievance_video_resynced_nosubs.mp4",
        export_dir / "PDPC_grievance_visual_review.mp4",
    )


def build_clip_command(frame, output, duration):
    return [
        "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(frame),
        "-t", f"{duration:.3f}", "-r", "30", "-vf",
        "scale=1920:950:force_original_aspect_ratio=decrease,"
        "pad=1920:1080:(ow-iw)/2:0:black,setsar=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
        str(output),
    ]
```

In `main()`:

1. Load `frame_mapping_resync.xlsx` with `load_assignments()`.
2. Call `validate_assignments(..., check_files=True)`.
3. Compile segments with `cover_frame="cover page.png"`.
4. Render one clip per segment using its exact `end_s - start_s`.
5. Concatenate with the FFmpeg concat demuxer.
6. Mux the existing audio stream from `PDPC_grievance_video_nosubs.mp4` using `-map 0:v:0 -map 1:a:0 -c:a copy`.
7. Write only `PDPC_grievance_video_resynced_nosubs.mp4`.
8. Support `--from-cue` and `--to-cue` to produce the review excerpt. For a cue slice, subtract the selected cue's absolute start time from every rendered segment, and mux only the matching source-audio window with FFmpeg `-ss` and `-t`. The resulting excerpt must start at timestamp zero and remain sample-aligned with its narration.

- [ ] **Step 4: Modify review-frame preparation**

Replace the `VISUAL_SCHEDULE` import in `scripts/prepare_review_frames.py` with:

```python
from cue_visuals import compile_segments, load_assignments

assignments = load_assignments(ROOT / "video_export/frame_mapping_resync.xlsx")
segments = compile_segments(assignments, cover_frame="cover page.png")
all_frames = list(dict.fromkeys(segment.frame for segment in segments))
```

Keep its label-copy and reduction behaviour unchanged.

- [ ] **Step 5: Run renderer and legacy tests**

Run:

```powershell
python -m unittest tests.test_render_cue_video tests.test_cue_visuals tests.test_prepare_visual_resync_workbook tests.test_supplemental_frames -v
```

Expected: all tests PASS. The legacy percentage-schedule tests continue to pass because `video_visuals.py` remains intact.

- [ ] **Step 6: Commit the renderer migration**

```powershell
git add scripts/render_cue_video.py scripts/prepare_review_frames.py tests/test_render_cue_video.py
git commit -m "video: render visuals on exact narration cues"
```

### Task 8: Build the proof review render and obtain approval

**Files:**
- Create: `video_export/PDPC_grievance_visual_review.mp4`

- [ ] **Step 1: Render the two proof windows**

Run Scene 2 and Scene 10/11 windows separately, then concatenate them:

```powershell
python scripts/render_cue_video.py --from-cue 12 --to-cue 30 --out "video_export/review_scene02.mp4"
python scripts/render_cue_video.py --from-cue 242 --to-cue 296 --out "video_export/review_scene10_11.mp4"
```

Create `video_export/review_concat.txt` containing:

```text
file 'review_scene02.mp4'
file 'review_scene10_11.mp4'
```

Run:

```powershell
ffmpeg -y -f concat -safe 0 -i video_export/review_concat.txt -c copy video_export/PDPC_grievance_visual_review.mp4
```

- [ ] **Step 2: Verify the review render**

Run:

```powershell
ffprobe -v error -show_entries stream=codec_type,codec_name,width,height -show_entries format=duration -of default=noprint_wrappers=1 video_export/PDPC_grievance_visual_review.mp4
```

Expected: H.264 1920 by 1080 video, AAC audio, and both proof windows present.

- [ ] **Step 3: Pause for user review**

Ask the user to review identity consistency, documentary tone, transition timing, evidence readability, and whether any passage still lacks a relevant visual. Apply requested mapping or prompt changes before full assembly.

- [ ] **Step 4: Commit the approved review state**

```powershell
git add video_export/frame_mapping_resync.xlsx video_export/PDPC_grievance_visual_review.mp4
git commit -m "review: approve cue-anchored visual sequence"
```

### Task 9: Assemble and verify the final no-subtitles video

**Files:**
- Create: `video_export/PDPC_grievance_video_resynced_nosubs.mp4`
- Create: `scripts/report_visual_resync.py`
- Create: `docs/superpowers/plans/2026-07-16-pdpc-video-visual-resync-report.md`

- [ ] **Step 1: Render the full approved workbook**

Run:

```powershell
python scripts/render_cue_video.py
```

Expected: one clip per compiled visual segment and final output at `video_export/PDPC_grievance_video_resynced_nosubs.mp4`.

- [ ] **Step 2: Verify locked media properties**

Run:

```powershell
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type,codec_name,width,height,r_frame_rate -of default=noprint_wrappers=1 video_export/PDPC_grievance_video_resynced_nosubs.mp4
```

Expected:

- Duration within 0.10 seconds of 1387.666667.
- H.264 video, 1920 by 1080, 30 fps.
- AAC audio present.

- [ ] **Step 3: Implement and run the audit report**

`scripts/report_visual_resync.py` must load assignments and compiled segments. It must use `collections.Counter` for cue statuses, calculate hold durations from the compiled segment boundaries, validate asset paths with `validate_assignments(..., check_files=True)`, and probe the final video with JSON output from:

```powershell
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type -of json video_export/PDPC_grievance_video_resynced_nosubs.mp4
```

It must write `docs/superpowers/plans/2026-07-16-pdpc-video-visual-resync-report.md` with: cue and scene counts; total visual segments; retained, retimed, replaced, and added cue counts; average and maximum segment duration; every hold over 25 seconds with its frame and workbook rationale; missing-asset and off-cue-transition counts; final duration; and whether an audio stream is present. Every value must be derived at runtime. A validation failure must stop the script instead of producing a successful report.

Run:

```powershell
python scripts/report_visual_resync.py
rg -n "Missing assets: 0|Off-cue transitions: 0|Cue rows: 318|Scenes reviewed: 13" docs/superpowers/plans/2026-07-16-pdpc-video-visual-resync-report.md
```

Expected: all four acceptance lines are present.

- [ ] **Step 4: Perform the final visual spot-check**

Review at least these exact cue transitions in the final MP4:

- Cue 7, Parliament penalties.
- Cue 19, CCTV/location passage.
- Cue 93, police-channel deflection.
- Cue 140, first Maradona analogy.
- Cue 187, repeated one-line response.
- Cue 227, complaint returned to reviewed officers.
- Cue 266, second Maradona passage.
- Cue 284, pattern recognition.
- Cue 296, website opening.
- Cue 310, final citizen appeal.

Expected: every frame begins on the first word of its anchor cue and remains relevant through its hold.

- [ ] **Step 5: Run the full test suite**

Run:

```powershell
python -m unittest discover -s tests -v
```

Expected: all tests PASS; no skipped tests.

- [ ] **Step 6: Commit the final deliverables intentionally**

```powershell
git add scripts/report_visual_resync.py docs/superpowers/plans/2026-07-16-pdpc-video-visual-resync-report.md video_export/frame_mapping_resync.xlsx video_export/PDPC_grievance_video_resynced_nosubs.mp4
git commit -m "video: complete cue-anchored PDPC visual resync"
```

## Self-review results

- **Spec coverage:** All 13 scenes, all 318 cues, exact cue timing, selective narrator use, documentary style, proof generation gate, source discipline, workbook review, short review render, full assembly, and media verification are covered.
- **Scope:** The plan changes only the visual schedule, its reviewed workbook, generated visuals, review tooling, and final clean render. It does not change narration, audio, subtitles, case text, or the public website.
- **Compatibility:** The legacy percentage schedule remains intact so prior tooling and tests continue to work. The new renderer consumes only `frame_mapping_resync.xlsx`.
- **No silent skips:** Full-file validation, approval flags, missing-asset checks, anchor checks, long-hold checks, exact transition spot-checks, and an audit report all fail loudly.
