# PDPC Grievance Story — Video Production Handoff

**Date:** 2026-07-04
**For:** Codex execution
**Status:** Plan ready, awaiting voiceover + frames + assemble

---

## What's already done

1. **Script written** — 13-scene, ~10:45 YouTube video, first-person narration by Ray Lim
2. **plan.json built** — converted from scene script via `script_to_plan.py`, SHA-256 verified
3. **Voice selected** — `ray-en-rec-003` (Ray's cloned voice, latest recording-based)

## What needs to be done (in order)

1. Commit plan to yt-intake project directory
2. Generate TTS voiceover
3. Run timestamps + resync ASR to script
4. Generate frames via MiniMax image API
5. Assemble MP4 with subtitles
6. Export

---

## Key paths

```
Script:        H:\My Drive\Driving Legal Issue\pdpc-grievance-site\docs\superpowers\specs\2026-07-04-video-script.md
Plan JSON:     H:\My Drive\Driving Legal Issue\pdpc-grievance-site\docs\superpowers\specs\2026-07-04-video-plan.json
Plan SHA-256:  e88669281be7d42e5f907c2c422486d07dae49ead9b3ff215e3a7e6f3af9e703
Project slug:  pdpc-grievance-story
Voice ID:      ray-en-rec-003
Target:        645s (~10:45)

Working dir:   E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\
Python:        E:/Bespoke/Minimax_Hub/.venv/Scripts/python.exe
PYTHONPATH:    E:/Bespoke/Minimax_Hub
MINIMAX_KEY:   In E:/Bespoke/Minimax_Hub/.env as MINIMAX_API_KEY
FFmpeg:        On PATH (installed 2026-06-30)
```

## Plan summary

| # | Scene | Duration | Style | Narration chars |
|---|---|---|---|---|
| 1 | The Hook — Parliament vs PDPC | 30s | clean/systemic | 599ch |
| 2 | The Accident | 60s | hand-drawn | 866ch |
| 3 | The Denials | 105s | hand-drawn | 1391ch |
| 4 | The Deletion Window | 45s | hand-drawn | 585ch |
| 5 | Filing With PDPC | 45s | hand-drawn | 551ch |
| 6 | The Clarity Test (Maradona Beat 1) | 60s | mixed | 1450ch |
| 7 | Two Cases, Two Invented Reasonings | 75s | clean/systemic | 1086ch |
| 8 | Nine Questions, One Response | 60s | clean/systemic | 1131ch |
| 9 | IMDA — The Oversight | 45s | clean/systemic | 858ch |
| 10 | 384 Cases (Maradona Beat 2) | 60s | clean/systemic | 1864ch |
| 11 | The Only Explanation | 30s | clean/systemic | 1176ch |
| 12 | pdpaaccessrights.sg | 20s | mixed | 847ch |
| 13 | Call to Action | 10s | clean/systemic | 576ch |
| **Total** | | **645s** | | **~13,000ch** |

All 13 image prompts in `per_frame_prompts` are style-prefixed:
- `hand-drawn` → "Hand-drawn ink-wash illustration, loose linework, muted palette. "
- `clean/systemic` → "Clean systemic editorial infographic, flat vector, black-white-red. "
- `mixed` → no prefix (prompt already describes the transition)

---

## Step-by-step execution

### Step 1: Create the yt-intake project directory

```bash
mkdir -p "E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\assets\audio"
mkdir -p "E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\assets\frames"
```

### Step 2: Commit plan.json + plan.sha256

Copy the plan and write the hash file:

```bash
copy "H:\My Drive\Driving Legal Issue\pdpc-grievance-site\docs\superpowers\specs\2026-07-04-video-plan.json" "E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\plan.json"
```

Write `plan.sha256` — create a file at `E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\plan.sha256` containing exactly:
```
e88669281be7d42e5f907c2c422486d07dae49ead9b3ff215e3a7e6f3af9e703
```
(no newline at end — use `echo -n` or Write tool)

Verify:
```bash
PYTHONPATH=E:/Bespoke/Minimax_Hub E:/Bespoke/Minimax_Hub/.venv/Scripts/python.exe -c "
from intake.plan import sha256
from pathlib import Path
import json
t = Path('E:/Bespoke/Minimax_Hub/projects/pdpc-grievance-story/plan.json').read_text(encoding='utf-8')
stored = Path('E:/Bespoke/Minimax_Hub/projects/pdpc-grievance-story/plan.sha256').read_text(encoding='utf-8').strip()
computed = sha256(t)
assert stored == computed, f'Mismatch: stored={stored} computed={computed}'
print(f'Plan verified: {len(json.loads(t)[\"beats\"])} beats, {json.loads(t)[\"target_duration_s\"]}s')
"
```

### Step 3: Generate voiceover (ai_voice with cloned voice)

```bash
PYTHONPATH=E:/Bespoke/Minimax_Hub E:/Bespoke/Minimax_Hub/.venv/Scripts/python.exe -m intake tts pdpc-grievance-story --voice-id ray-en-rec-003
```

This reads `plan.json`, cleans the script via `_clean_for_tts()` (strips markdown, separators, "What happened" blocks are already excluded), inserts pause markers `<#0.35#>` after sentences and `<#0.15#>` after commas, calls MiniMax TTS at `https://api.minimax.io/v1/t2a_v2`, writes `assets/audio/voiceover.mp3`.

**Expected output:** `E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\assets\audio\voiceover.mp3`

**Verify:** File exists and is > 1MB (645s of speech should be several MB).

### Step 4: Run timestamps (ASR-anchored)

```bash
PYTHONPATH=E:/Bespoke/Minimax_Hub E:/Bespoke/Minimax_Hub/.venv/Scripts/python.exe -m intake timestamps pdpc-grievance-story --audio "E:/Bespoke/Minimax_Hub/projects/pdpc-grievance-story/assets/audio/voiceover.mp3"
```

This transcribes with faster-whisper (`language="en"` forced), writes `assets/timestamps.json`.

**Expected:** May show a warning "sentence count mismatch — drift skipped" (normal for long-form narration). This is NOT a failure.

### Step 5: Resync ASR text to the real script

ASR WILL mishear words phonetically. Run this Python to replace ASR text with the correct script text while keeping ASR's segment boundaries:

```python
from intake.timestamps import TimestampedSentence, resync_to_script
from intake.voice import _project_script_text
import json
from pathlib import Path

PROJECT = "pdpc-grievance-story"
BASE = Path("E:/Bespoke/Minimax_Hub/projects") / PROJECT

raw = json.loads((BASE / "assets/timestamps.json").read_text(encoding="utf-8"))
entries = [TimestampedSentence(**e) for e in raw]
resynced = resync_to_script(entries, _project_script_text(PROJECT))
out = [{"start_s": e.start_s, "end_s": e.end_s, "text": e.text} for e in resynced]
(BASE / "assets/asr_segments.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Resynced {len(out)} segments to asr_segments.json")
```

### Step 6: Generate frames

```bash
PYTHONPATH=E:/Bespoke/Minimax_Hub E:/Bespoke/Minimax_Hub/.venv/Scripts/python.exe -m intake frames pdpc-grievance-story
```

This reads `plan.json` per_frame_prompts (one per beat = 13 frames), generates via MiniMax image API at `https://api.minimax.io/v1/image_generation`, writes timestamp-named `.jpg` files to `assets/frames/`.

**Expected:** 13 frames generated (or 13 attempted). Report: `succeeded / failed / skipped` counts.

**If any frames fail:** re-run with `--retry-failed` (not `--fresh` — that regenerates all and burns extra credits):
```bash
PYTHONPATH=E:/Bespoke/Minimax_Hub E:/Bespoke/Minimax_Hub/.venv/Scripts/python.exe -m intake frames pdpc-grievance-story --retry-failed
```

**Known issue:** The CLI has a state truncation bug where `_build_initial_state` creates N entries but only some survive after `_generate_one` loop. If you get fewer frames than expected, report how many succeeded and we'll regenerate the missing ones via direct MiniMax API calls.

### Step 7: Assemble MP4

```bash
PYTHONPATH=E:/Bespoke/Minimax_Hub E:/Bespoke/Minimax_Hub/.venv/Scripts/python.exe -m intake assemble pdpc-grievance-story
```

This reads `timestamps.json` for frame entries, loops each frame for its duration, scales to 1920x1080 with letterboxing, concats all frames, muxes voiceover as audio, burns in subtitles from `asr_segments.json` (white text, dark outline, bottom-aligned), writes the MP4.

**Output:** `E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\pdpc-grievance-story.mp4`

**Subtitle line-breaking:** Auto-detected: Latin font → MAX_LINE=52, max 2 lines. Text with explicit `\n` is used as-is.

**If assemble command errors with "invalid choice: 'assemble'":** The CLI registration was lost. Re-add to `E:/Bespoke/Minimax_Hub/intake/cli.py`:
```python
from intake.assemble import assemble as assemble_project
# In cmd_assemble function, then register:
sub.add_parser("assemble", ...)
```
Verify with:
```bash
PYTHONPATH=E:/Bespoke/Minimax_Hub E:/Bespoke/Minimax_Hub/.venv/Scripts/python.exe -c "import intake.cli; print(sorted(intake.cli.build_parser()._subparsers._group_actions[0].choices.keys()))"
```
Must include `'assemble'`.

### Step 8: Verify output

```bash
# Check file exists and size
dir "E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\pdpc-grievance-story.mp4"

# Check duration with ffprobe (should be ~645s)
ffprobe -v error -show_entries format=duration -of csv=p=0 "E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\pdpc-grievance-story.mp4"

# Check frame count
dir "E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\assets\frames\*.jpg" | find /c ".jpg"
```

---

## Known issues to watch for

| # | Issue | Symptom | Fix |
|---|---|---|---|
| 1 | TTS returns HTTP 404 or 2013 | Error in TTS output | Host must be `api.minimax.io`, path `/t2a_v2`. Payload must have nested `voice_setting`/`audio_setting` objects. Verify MINIMAX_API_KEY in `.env`. |
| 2 | Timestamps hard-fails on sentence count | "cannot compute drift" error | This was fixed 2026-07-02 — tolerant path now skips drift on count mismatch. If it still fails, the CLI may have reverted; check `cli.py:cmd_timestamps` for the `drift_skipped` flag. |
| 3 | Frames generates fewer than 13 images | CLI state truncation bug | Regenerate missing frames via direct MiniMax API: `build_image_payload` → `post_json` → `download_to`. |
| 4 | `assemble` command missing | "invalid choice: 'assemble'" | Re-register in `intake/cli.py` (see Step 7 fix). |
| 5 | ASR transcribes cloned voice as gibberish | Subtitles show non-English text | `language="en"` is forced in `align()`. If still garbled, sanity-check by re-running faster-whisper manually with `language="en"`. Do not assume the audio is broken. |
| 6 | Multiple frames render as near-identical | 3+ consecutive pale/empty compositions | Spot-check frames after generation. If they look the same, regenerate those specific frames with bolder contrast cues in the prompt, then reassemble. Don't `--fresh` the whole batch (burns credits). |
| 7 | Windows FFmpeg subtitles filter fails | "Unable to parse original_size" | Fixed: `assemble.py` backslash-escapes drive-letter colons. If it reappears, manually escape `E\:/path/to/subtitles.srt`. |
| 8 | Subtitle bottom-clear zone | Subtitles cover faces/action | All our image prompts were written with the subtitle-safe zone in mind (subjects in upper 88%, bottom 12% clear for 2-line subtitles). If a frame has content in the bottom band, regenerate that frame with the subject moved up. |

---

## Voice info

- **Voice ID:** `ray-en-rec-003`
- **Type:** Cloned voice (recording-based, latest)
- **Alternatives available if this one has issues:**
  - `ray-en-rec-002` (v2)
  - `ray-en-rec-001` (v1)
  - `ray-en-yt-001` (YouTube-optimized)
- **TTS endpoint:** `POST https://api.minimax.io/v1/t2a_v2`
- **No GroupId required** with current API key format

---

## If anything goes wrong

1. **Check the plan is intact:** Verify `plan.json` has 13 beats and `target_duration_s: 645`
2. **Check the voice works:** Test with `mcp__MiniMax__text_to_audio` with a single sentence using `ray-en-rec-003`
3. **Check the API key:** `E:/Bespoke/Minimax_Hub/.env` must have `MINIMAX_API_KEY`
4. **Check FFmpeg:** `ffmpeg -version` must work
5. **Regenerate from scratch:** Delete `E:\Bespoke\Minimax_Hub\projects\pdpc-grievance-story\` and restart from Step 1

---

## Reference files in pdpc-grievance-site

| File | Purpose |
|---|---|
| `docs/superpowers/specs/2026-07-04-video-script.md` | The 13-scene script (source of truth for narration) |
| `docs/superpowers/specs/2026-07-04-video-script-design.md` | Design spec with scene breakdown + source map |
| `docs/superpowers/specs/2026-07-04-video-plan.json` | Generated plan.json (13 beats, style-prefixed prompts) |
| `docs/superpowers/plans/2026-07-04-video-script-plan.md` | Implementation plan (how the script was built) |
| `.claude/skills/script-to-video/SKILL.md` | Skill documentation |
| `.claude/skills/script-to-video/script_to_plan.py` | Conversion script (script.md → plan.json) |
