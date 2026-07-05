---
name: script-to-video
description: Use when turning a pre-written scene script (with Narration, Image prompt, timestamps, and visual style per scene) into an MP4 video via the yt-intake pipeline. The script format has "## Scene N" blocks with **Narration:**, **Image prompt:**, and **What happened:** fields per scene. NOT for LinkedIn articles — use yt-intake for those.
---

# Script-to-Video

Convert a pre-written video script (scene blocks with narration + image prompts) into an MP4 video using the MiniMax intake pipeline (TTS + image generation + ffmpeg assemble).

## Overview

yt-intake expects a LinkedIn article and runs `intake convert` to parse it into beats. This skill bridges pre-written scene scripts into the same pipeline by building `plan.json` directly — skipping article parsing, polishing, and the convert step.

## When to Use

- You have a markdown script file with `## Scene N` blocks containing `**Narration:**`, `**Image prompt:**`, and `**What happened:**` fields
- The script has explicit timestamps like `[M:SS–M:SS]` in scene headers
- Scenes have per-scene visual style tags (`hand-drawn`, `clean/systemic`, `mixed`)
- You want to produce an MP4 with TTS voiceover + generated images + burned-in subtitles

Do NOT use for LinkedIn articles — use the yt-intake skill directly for those.

## Pipeline

Scene script → script_to_plan.py → plan.json → intake tts/timestamps → intake frames → intake assemble → .mp4

## Core Pattern

### Step 1 — Parse the script into plan.json

Run the conversion script:
```bash
cd <project-dir>
python .claude/skills/script-to-video/script_to_plan.py \
  docs/superpowers/specs/<script>.md \
  --out-json <scratchpad>/plan.json \
  --project-id <slug>
```

This extracts:
- **Hook** — first 2 sentences of Scene 1 narration
- **Beats** — one per scene, with body = narration text, title = scene title
- **per_frame_prompts** — image prompts, style-prefixed based on the scene's visual style tag
- **beat_timestamps** — from the script's [M:SS–M:SS] headers
- **target_duration_s** — from the last scene's end timestamp

**Style mapping** (yt-intake only has 6 global presets; we use `documentary` as base and prefix prompts):

| Script tag | Prompt prefix |
|---|---|
| `hand-drawn` | "Hand-drawn ink-wash illustration, loose linework, muted palette. " |
| `clean/systemic` | "Clean systemic editorial infographic, flat vector, black-white-red. " |
| `mixed` | No prefix — prompt already describes the transition |

### Step 2 — Commit the plan

Two-stage commit, same as yt-intake Step 3:
```bash
# Stage A: Create project
PYTHONPATH=E:/Bespoke/Minimax_Hub E:/Bespoke/Minimax_Hub/.venv/Scripts/python.exe \
  -m intake convert <script>.md \
  --format long --platform youtube_long --aspect 16:9 \
  --style documentary --narration ai_voice \
  --voice-id <voice_id> --target-duration <seconds> \
  --project-id <slug> --apply

# Stage B: Overwrite with our plan.json
cp <scratchpad>/plan.json <projects_dir>/<slug>/plan.json
# Then recompute plan.sha256 (see yt-intake Step 3)
```

### Step 3 — Voiceover

Three paths. Choose based on how the narration will be produced:

#### Path A: ai_voice (fastest — MiniMax TTS)

```
PYTHONPATH=E:/Bespoke/Minimax_Hub E:/Bespoke/Minimax_Hub/.venv/Scripts/python.exe \
  -m intake tts <slug> --voice-id <voice_id>
```

Then run timestamps + resync (see yt-intake Step 4, steps 2-4).

#### Path B: own_voice with prep-recording (recommended — single clean take)

For a recording done in one take, no false starts or retakes:
1. Record the script narration with phone voice memo (m4a/wav/mp3)
2. Clean: `intake prep-recording --input "<recording.m4a>" --project <slug>`
3. Listen to `voiceover.mp3` — re-run with `--denoise-prop-decrease 0.5` if too processed
4. Run timestamps: `intake timestamps <slug> --audio .../voiceover.mp3`
5. Resync ASR text to script (see yt-intake Step 4.5)
6. Verify coverage: `intake check-recording-coverage <slug>`

#### Path C: own_voice with manual splice (for multi-take recordings)

When your recording has retakes, false starts, or off-script remarks, use yt-intake's manual splice workflow (Step 4c). **Do NOT use `intake edit-recording`** — the auto-pick splices fragments from different takes producing a disconnected patchwork.

**REQUIRED REFERENCE:** Read yt-intake Step 4c for the full manual workflow. In brief:
1. Transcribe with faster-whisper (word-level timestamps)
2. Identify retake regions — find sentences spoken multiple times, pick the best take
3. Build splice regions — mark start_s/end_s for each kept segment
4. Splice with ffmpeg concat filter on body segments
5. Concat hook + body if separate, run `prep-recording` ONCE on the full WAV
6. Adjust per-segment volume if re-recorded parts are at different levels

See yt-intake Step 4c.5 for why single-pass prep-recording matters (multiple passes on short clips create artifacts).

#### Path D: text_only (frames only, no audio)

Skip TTS and timestamps. Manually create a synthetic `timestamps.json` with proportional times. Then run frames + assemble (no voiceover).

### Step 4 — Frames + Assemble

Follow yt-intake Steps 5–6. These are identical to the standard pipeline:
```
intake frames <slug>
intake assemble <slug> [--font-name "..."] [--font-size N]
```

### Step 5 — Export

Copy mp4 + srt to export directory per yt-intake Step 6.5.

## What This Skill Does NOT Do

- Polish narration or image prompts (they're already finished in the script)
- Parse LinkedIn articles (use yt-intake for that)
- Support the `intake convert` path (the script IS the plan)
- Change visual styles globally — style direction comes from per-scene tags
- Auto-pick takes with `intake edit-recording` (produces disconnected patchwork — use manual splice)

## Key Differences From yt-intake

| yt-intake | script-to-video |
|---|---|
| Input: LinkedIn article .md | Input: scene script .md |
| `intake convert` parses article | `script_to_plan.py` builds plan.json directly |
| One global style preset | Per-scene style tags mapped to prompt prefixes |
| Polish hook + prompts (LLM) | No polishing needed — script is finished |
| Beats from article sections | Beats from scene blocks |
| Narration from article body | Narration from `**Narration:**` blocks |
| "What happened" included | "What happened" skipped (source-anchors, not voice-over) |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Feeding script to `intake convert` | Run `script_to_plan.py` instead |
| Including "What happened" in TTS | The conversion script skips these |
| Using one global style | Style tags are mapped to per-prompt prefixes |
| Polishing finished prompts | Skip polish — script prompts are final |
| Using `intake edit-recording` for multi-take recordings | Use manual splice workflow (Path C) |
| Running prep-recording on individual clips | Concat first, prep-recording ONCE on full WAV |
| Trusting `intake timestamps` drift check on own_voice | ASR segment counts may coincidentally match and trigger false-positive drift errors — bypass CLI for own_voice (see yt-intake Step 4c.7) |

## Red Flags

- "I'll just feed it to intake convert" → It will parse scene headers as section titles. Don't.
- "Let me pick one style preset" → You'll lose the hand-drawn/systemic contrast.
- "I'll include What happened blocks for context" → They're metadata. Narration blocks are the voice-over.
- "The narration needs polishing" → It's already written. Don't rewrite it.
- "I'll use intake edit-recording" → Don't. Manual splice workflow only for multi-take recordings.
