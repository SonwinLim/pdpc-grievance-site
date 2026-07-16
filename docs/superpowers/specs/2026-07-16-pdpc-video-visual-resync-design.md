# PDPC Video Visual Resync Design

**Date:** 16 July 2026

**Status:** Approved in conversation, pending written-spec review

**Primary video:** `video_export/PDPC_grievance_video_nosubs.mp4`

**Current mapping:** `video_export/frame_mapping_actual.xlsx`

**Narration:** `docs/superpowers/specs/2026-07-05-video-narration-only.md`

**Current visual schedule:** `scripts/video_visuals.py`

## Goal

Resynchronise every visual in the 23-minute PDPC grievance video to an exact narration cue, retain strong existing evidence and hero frames, and add script-specific documentary visuals where the current sequence leaves narration unsupported.

The goal is not to reduce the number of frames. The goal is to make each visual appear on the narration beat it explains and to add coverage where a long or conceptually distinct passage needs another visual.

## Locked inputs

- Keep the existing own-voice narration.
- Keep the existing audio timing and scene order.
- Keep the current 1920 by 1080, 30 fps output format.
- Keep the current no-subtitles video duration as the assembly target. `ffprobe` reports 1387.666667 seconds.
- Review every scene and every current frame assignment. No opening or previously reviewed section is exempt.
- Preserve strong primary-source and hero assets unless retiming or replacement is required for script relevance.

## Confirmed creative decisions

- **Approach:** evidence-led documentary hybrid.
- **Generated-frame style:** documentary photojournalism.
- **Pacing:** narration beats, normally 10 to 18 seconds per visual, with longer holds for readable evidence.
- **Narrator presence:** selective, at the human and analytical pivots rather than throughout the video.
- **Evidence discipline:** real documents, correspondence, legislation, CCTV/location images, charts, and site captures prove claims. Generated visuals carry personal experience, transitions, and concepts that lack a direct visual record.

## Root cause of the current synchronisation problem

`scripts/video_visuals.py` places frames at normalised percentages within each scene, for example `at: 0.35`. The narration is timed by 319 real subtitle cues in `frame_mapping_actual.xlsx`. A percentage-based transition can therefore land during the wrong sentence even when the frame order is broadly correct.

The audit found concrete mismatches:

- Scene 2's Street View frame enters during the brain-injury diagnosis rather than the CCTV/location discussion.
- Scene 6's masking/identifiability material remains on screen when the narration introduces Maradona.
- Scene 10's Protection and Retention statute frames appear during the Maradona and repeated-response passage.
- Scene 5 has two distinct visuals across approximately 152 seconds.
- Scene 8 has five distinct visuals across approximately 191 seconds.
- Scene 11 has two distinct visuals across approximately 97 seconds.

## Timing architecture

`video_export/frame_mapping_actual.xlsx` becomes the visual timing source of truth. Each of its 319 cue rows has an exact start time, end time, scene number, narration text, and assigned frame.

A frame assignment applies from the first cue on which it appears until the next cue assigned a different frame. The compiler collapses consecutive cues using the same frame into one explicit visual segment.

Each cue-level assignment has one review status:

- **Keep:** the visual and entry cue are correct.
- **Retime:** the visual is correct but must enter on another cue.
- **Replace:** the visual does not explain the assigned narration.
- **Add:** the narration needs a new visual beat.
- **Hold:** intentionally retain the previous frame through the cue.

The compiled schedule records explicit cue numbers and timestamps. It does not use scene percentages.

## Workbook schema

Retain the existing `Frames` and `Reference` sheets and their current formatting. Add these columns to `Frames`:

| Column | Purpose |
|---|---|
| Status | Keep, Retime, Replace, Add, or Hold |
| Anchor phrase | Exact narration words that trigger the visual |
| Visual type | Primary source, documentary reconstruction, narrator, diagram, hero, or site capture |
| Source/reference path | Primary source or identity reference used to make the asset |
| Review rationale | Why this visual belongs on this cue |
| Approved | Review gate before full assembly |

The `Reference` sheet lists every retained and proposed asset, its scene, explicit start cue, exact timestamp, type, path, and generation status.

## Visual system

### Primary-source evidence

Use real correspondence, statutory provisions, CCTV/location images, enforcement charts, and site captures when the narration discusses that source. Keep the existing navy, white, and statutory-red presentation. Highlight only the relevant passage and preserve sufficient reading time.

Never use an image-generated quotation, official document, logo, legal provision, statistic, or email. Reconstructed evidence cards are allowed only when they reproduce verbatim source text and identify the sender, date, and document subject.

### Documentary reconstruction

Use Codex image generation for events with no direct visual record, including waking in hospital without memory, approaching the management office, waiting through institutional silence, reviewing the enforcement register, and confronting the documented pattern.

Generated frames must:

- Use a restrained documentary photojournalistic look.
- Avoid invented documentary details that imply photographic proof.
- Avoid readable generated text, logos, legal citations, and quotations.
- Place focal action in the upper 88 percent of the frame.
- Keep the lower subtitle band visually quiet even though the current target video is unburned.
- Use 16:9 composition suitable for 1920 by 1080 output.

### Selective narrator frames

Use the stylised portraits in `C:/Users/limzi/Documents/Linkedin Articles/Reference_images/` to preserve identity. Prefer the already stylised portraits over the raw reference photographs.

Proposed narrator appearances:

| Scene | Narrative pivot | Reference direction |
|---:|---|---|
| 2 | Hospital, brain injury, and missing memory | `Contemplative.png` or `Sadness.png` |
| 3 | Requesting footage at the management office | `tensed.png` |
| 5 | Waiting while the complaint produces no meaningful action | `Contemplative.png` |
| 10 or 11 | Discovering the zero-breach pattern | `resolved.png` |
| 13 | Citizen appeal and invitation to verify | `resolved.png` |

Do not default to `Fear.png`. Its expression is stronger than the approved documentary tone unless a specific narration beat supports that intensity.

## Scene review decisions

### Scene 1: Parliament

Retain the parliamentary question, Scene 1 hero, and preservation/penalties assets. Move the preservation/penalties frame to the first cue that mentions criminal penalties.

### Scene 2: The accident

Retain the location, Street View, CCTV, and hero evidence. Move each asset to the cue naming its location or evidential purpose. Add a documentary hospital frame with the narrator's likeness for the memory-loss passage.

### Scene 3: The denials

Retain the DPO reply, hero comparison, guideline, and Fifth Schedule. Add a selective narrator frame for the in-person management-office request. Anchor each condominium's evidence to its own narration.

### Scene 4: The deletion window

Retain the six current evidence assets. Correct the entry cues so the captured-footage, 17-day overwrite, s.22A, no-finding, and PDPC admission visuals enter on their exact propositions.

### Scene 5: Filing with PDPC

Expand substantially from the current two-frame treatment. Add source-grounded beats for:

- The complaint submission.
- The 10 May reply.
- The statement that PDPC was not the appropriate channel.
- The instruction to contact the investigation officer.
- MP intervention.
- The refusal to look further.
- The deletion-versus-access distinction.
- The period of institutional silence, using one selective narrator documentary frame.

### Scene 6: The clarity test

Retain the silhouette, personal-data definition, actual-footage stills, masking precedent, hero, and Maradona material. Move masking and identifiability evidence before the football analogy. Use the Maradona asset when the analogy begins.

### Scene 7: Two invented reasonings

Retain the principal decision and statute assets. Add distinct beats for the disappearing request date and PDPC's failure to test either condominium's stated refusal ground.

### Scene 8: Nine questions

Expand from five assets. Show question clusters when the relevant questions are spoken, then show the repeated one-line response, missing legal analysis, publication delay, and closure. Clearly label question cards as questions submitted by the Complainant, not official quotations.

### Scene 9: IMDA

Retain the IAU finding, protocols reply, and hero. Add the escalation path, `12 emails · 11 months`, and complaint-returned-to-reviewed-body beats.

### Scene 10: 384 cases

Retain the enforcement register and breach charts. Do not display Protection or Retention statute frames during the Maradona passage. Use the Maradona analogy and PDPC's repeated one-line reply at that point.

### Scene 11: The explanation

Expand from two visuals. Add a sequence for uneven error versus one-directional decisions, the reasoning chain, discretion versus active denial, and legal mechanism to zero-breach outcome to non-engagement. Include one resolved narrator frame at the pattern-recognition pivot.

### Scene 12: The website

Retain the five site captures. Retime each capture to the feature named in the narration. Do not add generated imagery.

### Scene 13: Call to action

Open with a resolved documentary narrator frame, transition to the evidence wall, and finish on the existing statutory-right question card.

## Image-generation proof gate

Generate two proof frames before any full batch:

1. Scene 2 hospital memory-loss frame using `Contemplative.png`.
2. Scene 11 pattern-discovery frame using `resolved.png`.

Both proofs must demonstrate:

- Recognisable identity without a close-up reaction portrait.
- Documentary environment and lighting.
- Restrained emotion.
- Visual continuity with the evidence-led frames.
- No generated legal text or quotation.
- A clear lower subtitle zone.

The full generation batch begins only after both proof frames are reviewed and approved.

## Compilation and assembly flow

1. Audit all 319 workbook cues and assign review statuses.
2. Add proposed assets and generation prompts to the workbook.
3. Generate and review the two proof frames.
4. Generate only approved missing documentary frames.
5. Verify frame count, filenames, dimensions, and reference provenance.
6. Compile consecutive cue assignments into explicit visual segments.
7. Produce a short review render around both proof frames.
8. Assemble the complete no-subtitles video after review approval.
9. Verify duration, audio stream, frame coverage, and transition timing.

## Validation and failure conditions

Fail the schedule validation if:

- Any cue has no effective visual.
- Any referenced asset is missing.
- A transition occurs outside a cue boundary.
- A generated asset is not 16:9 or cannot fill 1920 by 1080 safely.
- A generated asset contains fabricated official text or a purported quotation.
- A visual's anchor phrase is absent from its assigned cue.
- A static hold exceeds 25 seconds without an explicit evidence-readability justification.
- The compiled video duration differs materially from the locked target.
- The final video loses or changes the existing audio stream.

The review report must state:

- Total visual segments.
- Retained, retimed, replaced, and added counts.
- New generated and new source-grounded asset counts.
- Average and maximum hold length.
- Every hold longer than 25 seconds and its justification.
- Missing-file and cue-boundary validation results.
- Every generated frame's prompt and reference image.

## Acceptance criteria

- Every one of the 319 narration cues resolves to a visual.
- Every visual transition occurs on an exact narration cue start.
- All 13 scenes have been reviewed.
- Primary-source visuals appear on the claims they support.
- Scene 5, Scene 8, Scene 10, and Scene 11 no longer contain the identified long or mismatched passages.
- Selective narrator appearances are limited to approved human and analytical pivots.
- The two proof frames are approved before bulk image generation.
- The final no-subtitles video retains the existing narration, scene order, output dimensions, frame rate, and target duration.
