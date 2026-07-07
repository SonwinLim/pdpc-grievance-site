"""Produce the final PDPC grievance video with script-words subtitle text.

Steps:
  1. Reuse the scene alignment from prior runs (saved-as-printed in transcripts)
     by recomputing it deterministically from the existing SRT cues.
  2. For each scene, split the script body into sentences and distribute them
     across the scene's cues by char count proportional to cue duration.
     Each cue keeps its exact ASR start/end time, but its text is rebuilt
     from the script.
  3. Save the corrected SRT into video_export/ as a deliverable.
  4. Regenerate per-scene video clips at scene-boundary durations
     (cue-anchored: each scene runs from first cue start to next scene's
     first cue start).
  5. Concat, burn corrected SRT, mux audio, write the final MP4.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    from video_visuals import (
        SCENE_FRAME,
        VISUAL_SCHEDULE,
        build_visual_segments,
        extend_last_scene_to_duration,
        find_missing_visual_assets,
        visual_path,
    )
except ModuleNotFoundError:
    from scripts.video_visuals import (
        SCENE_FRAME,
        VISUAL_SCHEDULE,
        build_visual_segments,
        extend_last_scene_to_duration,
        find_missing_visual_assets,
        visual_path,
    )

ROOT = Path(r"D:/Driving Legal Issue/pdpc-grievance-site")
FRAMES_DIR = ROOT / "Screenshots Video"
NARRATION_MD = ROOT / "docs/superpowers/specs/2026-07-05-video-narration-only.md"
AUDIO_PATH = Path(r"C:/Users/limzi/Downloads/pdp finalc.wav")
BUILD_DIR = Path(r"D:/temp/pdp_video_build")
SRT_SRC = ROOT / "video_export" / "subtitles_corrected.srt"  # corrected timing source
FINAL_OUT = ROOT / "video_export" / "PDPC_grievance_video.mp4"
FINAL_SRT = ROOT / "video_export" / "subtitles.srt"   # deliverable
FINAL_OUT.parent.mkdir(exist_ok=True)

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "of", "in", "on", "at", "to", "for",
    "with", "from", "by", "when", "where", "why", "how", "who", "what", "which",
    "this", "that", "these", "those", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "can", "could", "must", "ought", "i", "you", "he",
    "she", "it", "we", "they", "them", "their", "his", "her", "my", "your", "our",
    "its", "as", "if", "so", "than", "then", "there", "here", "into", "out", "up",
    "down", "about", "above", "below", "between", "through", "during", "before",
    "after", "until", "while", "also", "just", "only", "very", "too", "more",
    "most", "some", "any", "all", "no", "not", "nor", "own", "same", "such", "am",
}


def norm(w):
    return re.sub(r"[^\w']", "", w.lower())


def run(cmd, label):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] {label}: rc={res.returncode}", file=sys.stderr)
        print(res.stderr[-1500:], file=sys.stderr)
        raise SystemExit(1)
    return res


def srt_time_to_seconds(t):
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def seconds_to_srt_time(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s_int = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        ms = 0
        s_int += 1
        if s_int == 60:
            s_int = 0
            m += 1
    return f"{h:02d}:{m:02d}:{s_int:02d},{ms:03d}"


def parse_srt(path):
    cues = []
    with open(path, encoding="utf-8") as f:
        content = f.read()
    blocks = content.strip().split("\n\n")
    for b in blocks:
        lines = b.strip().split("\n")
        if len(lines) < 3:
            continue
        try:
            idx = int(lines[0].strip())
        except ValueError:
            continue
        time_line = lines[1].strip()
        if " --> " not in time_line:
            continue
        start_t, _, end_t = time_line.partition(" --> ")
        text = " ".join(lines[2:]).strip()
        cues.append({
            "idx": idx,
            "start_s": srt_time_to_seconds(start_t),
            "end_s": srt_time_to_seconds(end_t),
            "text": text,
        })
    return cues


def parse_script_scenes(text):
    header_re = re.compile(
        r'^## Scene (\d+)\s*[-—–]\s*([^\[]+?)\s*\[(\d+):(\d+)[-–](\d+):(\d+)\]\s*·\s*(\d+)s',
        re.MULTILINE,
    )
    body_re = re.compile(
        r'^## Scene (\d+)[^\n]*\n+(.*?)(?=^##|\Z)',
        re.MULTILINE | re.DOTALL,
    )
    headers = {}
    for m in header_re.finditer(text):
        n = int(m.group(1))
        headers[n] = {"num": n, "title": m.group(2).strip()}
    bodies = {}
    for m in body_re.finditer(text):
        n = int(m.group(1))
        bodies[n] = m.group(2).strip()
    scenes = []
    for n in sorted(headers.keys()):
        sc = headers[n]
        sc["body"] = bodies.get(n, "")
        scenes.append(sc)
    return scenes


def align_scenes_to_cues(scenes, cues):
    """For each scene, find the cue range that best matches its first 18 content words.

    Returns timeline dicts that include the script body so the distributor can
    split it into sentences.
    """
    out = []
    last_cue = 0
    for sc in scenes:
        body_words = [
            norm(w) for w in sc["body"].split()
            if norm(w) and norm(w) not in STOP_WORDS
        ]
        anchor_words = body_words[:18]
        sent_set = set(anchor_words)
        if not sent_set:
            continue
        best_i = last_cue
        best_score = 0
        best_overlap = set()
        end_search = min(len(cues), last_cue + 100)
        for i in range(last_cue, end_search):
            cue_words = set(
                norm(w) for w in cues[i]["text"].split()
                if norm(w) and norm(w) not in STOP_WORDS
            )
            if not cue_words:
                continue
            overlap = sent_set & cue_words
            if not overlap:
                continue
            recall = len(overlap) / len(sent_set)
            score = recall + 0.05 * len(overlap)
            if score > best_score:
                best_score = score
                best_i = i
                best_overlap = overlap
        out.append({
            "num": sc["num"],
            "title": sc["title"],
            "body": sc["body"],
            "cue_idx": best_i,
            "start_s": cues[best_i]["start_s"],
            "match_score": best_score,
            "overlap_words": sorted(best_overlap),
        })
        last_cue = max(last_cue, best_i)
    # End = next scene's start, or last cue's end
    for i, sc in enumerate(out):
        if i + 1 < len(out):
            sc["end_s"] = out[i + 1]["start_s"]
        else:
            sc["end_s"] = cues[-1]["end_s"]
    return out


def split_sentences(text):
    """Split narration into sentence-level chunks. Try to keep reasonable length.

    Markdown separators ('---' lines) are stripped before tokenizing so they
    don't leak into subtitle text.
    """
    # Strip markdown separator lines (---) and standalone dashes
    cleaned_lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        # Drop lines that are just dashes (---)
        if stripped and all(c in "-—" for c in stripped):
            continue
        cleaned_lines.append(line)
    text = " ".join(ln.strip() for ln in cleaned_lines if ln.strip())

    # First split on sentence-ending punctuation with whitespace
    parts = re.split(r'(?<=[.!?])\s+(?=[A-Z“"\'‘—–-])', text.strip())
    parts = [p.strip() for p in parts if p.strip()]
    # If any part is too long (>200 chars), split on em-dash break points
    out = []
    for p in parts:
        if len(p) > 200:
            sub = re.split(r'\s+(?:[—–])\s+', p)
            out.extend([s.strip() for s in sub if s.strip()])
        else:
            out.append(p)
    return out


def distribute_script_to_cues(cues, sentences, scene_start, scene_end):
    """Distribute script sentences across cues by char count proportional to cue duration.

    Returns list of strings, one per cue.
    """
    if not cues or not sentences:
        return [""] * len(cues)

    scene_cues = cues
    total_dur = sum(c["end_s"] - c["start_s"] for c in scene_cues)
    total_chars = sum(len(s) for s in sentences)

    cue_texts = []
    sent_idx = 0
    sent_pos = 0
    n = len(sentences)

    for cue in scene_cues:
        cue_dur = cue["end_s"] - cue["start_s"]
        target_chars = max(1, (cue_dur / total_dur) * total_chars)

        collected = ""
        while sent_idx < n:
            sent = sentences[sent_idx]
            remaining = sent[sent_pos:]
            if not remaining:
                sent_idx += 1
                sent_pos = 0
                continue
            # If adding whole sentence still under target, take it
            if len(collected) + len(remaining) <= target_chars + 5:
                collected += remaining + " "
                sent_idx += 1
                sent_pos = 0
                if len(collected) >= target_chars and sent_idx < n:
                    # We have enough; but only stop if there's no immediate next sentence
                    if not sentences[sent_idx]:
                        break
                    # Otherwise peek: if next sentence alone fits, keep taking
                    if len(collected) + len(sentences[sent_idx]) <= target_chars + 20:
                        continue
                    break
            else:
                # Take partial — try to end at word boundary
                take = max(0, int(target_chars - len(collected)))
                if take <= 0:
                    # No room left; drop what's here into next cue
                    break
                # Look for last space within [take-3, take+5]
                best_end = min(take, len(remaining))
                window_lo = max(0, take - 5)
                window_hi = min(len(remaining), take + 8)
                # Find nearest space in that window
                end_at = best_end
                for j in range(window_hi, window_lo - 1, -1):
                    if j < len(remaining) and remaining[j] == ' ':
                        end_at = j
                        break
                if end_at < len(remaining) and end_at > 0 and remaining[end_at] == ' ':
                    collected += remaining[:end_at] + " "
                    sent_pos += end_at + 1
                else:
                    # Hard cut at char boundary
                    collected += remaining[:take]
                    sent_pos += take
                break
        cue_texts.append(collected.strip())

    # If anything left in queue, append to last cue
    leftover_parts = []
    while sent_idx < n:
        leftover_parts.append(sentences[sent_idx][sent_pos:])
        sent_idx += 1
        sent_pos = 0
    if leftover_parts and cue_texts:
        cue_texts[-1] = (cue_texts[-1] + " " + " ".join(leftover_parts)).strip()

    return cue_texts


def build_corrected_srt(cues_with_text):
    """Build SRT from list of (start_s, end_s, text) tuples."""
    lines = []
    for i, cue in enumerate(cues_with_text, 1):
        text = cue["text"].strip()
        if not text:
            continue
        lines.append(
            f"{i}\n{seconds_to_srt_time(cue['start_s'])} --> "
            f"{seconds_to_srt_time(cue['end_s'])}\n{text}\n"
        )
    return "\n".join(lines) + "\n"


def main():
    # ---- Parse SRT --------------------------------------------------------
    cues = parse_srt(SRT_SRC)
    print(f"[SRT-ASR] {len(cues)} cues parsed")

    # ---- Parse script -----------------------------------------------------
    md = NARRATION_MD.read_text(encoding="utf-8")
    scenes = parse_script_scenes(md)
    print(f"[SCRIPT] {len(scenes)} scenes parsed")

    # ---- Align scenes to cues ---------------------------------------------
    timeline = align_scenes_to_cues(scenes, cues)
    audio_dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(AUDIO_PATH)],
        capture_output=True, text=True,
    ).stdout.strip())
    timeline = extend_last_scene_to_duration(timeline, audio_dur)
    print("\n[ALIGNMENT]")
    for sc in timeline:
        dur = sc["end_s"] - sc["start_s"]
        print(f"  scene {sc['num']:>2}  {sc['start_s']:7.2f}s  ->  {sc['end_s']:7.2f}s"
              f"   ({dur:6.2f}s)   match={sc['match_score']:.2f}"
              f"   overlap={sc['overlap_words'][:5]}")

    # ---- For each scene, distribute its script sentences to its cues -----
    cues_with_text = []
    for sc in timeline:
        scene_num = sc["num"]
        scene_start = sc["start_s"]
        scene_end = sc["end_s"]

        # Cues for this scene (start within scene window).
        # Exclusive upper bound so a cue at scene_end belongs to NEXT scene.
        scene_cues = [c for c in cues if scene_start - 1 <= c["start_s"] < scene_end]
        if not scene_cues:
            print(f"  WARNING scene {scene_num}: no cues found in [{scene_start}, {scene_end}]")
            continue

        # Split script body into sentences
        sentences = split_sentences(sc["body"])
        if not sentences:
            print(f"  WARNING scene {scene_num}: no sentences")
            continue

        # Distribute sentences across scene cues
        cue_texts = distribute_script_to_cues(scene_cues, sentences, scene_start, scene_end)

        for cue, text in zip(scene_cues, cue_texts):
            cues_with_text.append({
                "idx": cue["idx"],
                "start_s": cue["start_s"],
                "end_s": cue["end_s"],
                "text": text,
            })

        # Diagnostic: how many chars assigned vs source
        assigned_chars = sum(len(t) for t in cue_texts)
        source_chars = sum(len(s) for s in sentences)
        print(f"  scene {scene_num:>2}: {len(scene_cues)} cues, "
              f"{len(sentences)} sentences, "
              f"{source_chars} source chars -> {assigned_chars} assigned chars "
              f"({100*assigned_chars/max(source_chars,1):.0f}%)")

    # ---- Sort by start time and de-collide ---------------------------------
    cues_with_text.sort(key=lambda c: c["start_s"])

    # ---- Build corrected SRT and save -------------------------------------
    srt_text = build_corrected_srt(cues_with_text)
    (BUILD_DIR / "subs_corrected.srt").write_text(srt_text, encoding="utf-8")
    FINAL_SRT.write_text(srt_text, encoding="utf-8")
    print(f"\n[SRT-OUT] corrected SRT saved to:")
    print(f"  - {FINAL_SRT}")
    print(f"  - {BUILD_DIR}/subs_corrected.srt")

    missing = find_missing_visual_assets(VISUAL_SCHEDULE)
    if missing:
        raise SystemExit(
            "Missing scheduled visual assets:\n" + "\n".join(f"  - {m}" for m in missing)
        )

    # ---- Clean old clips BEFORE generating any new ones --------------------
    for old in BUILD_DIR.glob("scene_*.mp4"):
        old.unlink()

    # ---- Cover page (pre-roll, silent) ----------------------------------
    COVER_DURATION = 5.0
    cover_clip = None
    cover_path = visual_path("cover page.png")
    if cover_path.exists():
        cover_clip = BUILD_DIR / "scene_00_cover.mp4"
        run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-loop", "1", "-i", str(cover_path),
            "-t", f"{COVER_DURATION:.3f}",
            "-r", "30",
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,"
                   "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,setsar=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            str(cover_clip),
        ], "cover page clip")
        # Write an offset SRT so subtitles appear after the cover
        from datetime import timedelta as _td
        def _add_offset(ts_str, secs):
            h, m, rest = ts_str.split(":")
            s, ms = rest.split(",")
            t = int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000 + secs
            dt = str(_td(seconds=t))
            if "." in dt:
                base, frac = dt.split(".")
            else:
                base, frac = dt, "000000"
            frac = frac[:3].ljust(3, "0")
            return f"{base.replace(':', ':').zfill(8)},{frac}"
        import re as _re
        srt_text = (BUILD_DIR / "subs_corrected.srt").read_text(encoding="utf-8")
        def _shift_block(m):
            ts1, ts2 = m.group(1), m.group(2)
            return f"{_add_offset(ts1, COVER_DURATION)} --> {_add_offset(ts2, COVER_DURATION)}"
        srt_shifted = _re.sub(
            r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})',
            _shift_block, srt_text,
        )
        srt_offset_path = BUILD_DIR / "subs_cover_offset.srt"
        srt_offset_path.write_text(srt_shifted, encoding="utf-8")
        print(f"[COVER] offset SRT written: {srt_offset_path}")

    # ---- Generate per-visual video clips (scene durations preserved) -------
    visual_segments = build_visual_segments(timeline, VISUAL_SCHEDULE)
    print(f"\n[CLIPS] generating {len(visual_segments)} visual clips at 1920x1080 30fps...")
    clip_paths = []
    if cover_clip is not None and cover_clip.exists():
        clip_paths.append(cover_clip)
    for idx, sc in enumerate(visual_segments, 1):
        frame_path = visual_path(sc["frame"])
        if not frame_path.exists():
            raise SystemExit(f"Frame not found: {frame_path}")
        dur = max(sc["end_s"] - sc["start_s"], 0.5)
        clip_out = BUILD_DIR / f"scene_{sc['scene']:02d}_{idx:03d}.mp4"
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-loop", "1", "-i", str(frame_path),
            "-t", f"{dur:.3f}",
            "-r", "30",
            "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,"
                   "pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,setsar=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
            str(clip_out),
        ]
        run(cmd, f"scene {sc['scene']} visual clip {idx}")
        clip_paths.append(clip_out)

    # ---- Concat ----------------------------------------------------------
    concat_list = BUILD_DIR / "concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{p.resolve()}'" for p in clip_paths) + "\n",
        encoding="utf-8",
    )
    video_no_audio = BUILD_DIR / "video_no_audio.mp4"
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c", "copy",
        str(video_no_audio),
    ], "concat")
    vd = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(video_no_audio)],
        capture_output=True, text=True,
    ).stdout.strip())
    print(f"[INTER] video-only duration: {vd:.2f}s ({vd/60:.2f} min)")

    # ---- Final mux --------------------------------------------------------
    force_style = (
        "FontName=Arial,"
        "FontSize=22,"
        "PrimaryColour=&H00FFFFFF&,"
        "OutlineColour=&H00000000&,"
        "BorderStyle=1,"
        "Outline=3,"
        "Shadow=1,"
        "Alignment=2,"
        "MarginV=40"
    )

    has_cover = cover_clip is not None and cover_clip.exists()
    srt_for_burn = "subs_cover_offset.srt" if has_cover else "subs_corrected.srt"

    cmd = [
        "ffmpeg", "-y", "-loglevel", "info",
        "-i", str(video_no_audio),
    ]
    if has_cover:
        cmd += ["-itsoffset", f"{COVER_DURATION:.3f}"]
    cmd += [
        "-i", str(AUDIO_PATH),
        "-vf", f"subtitles={srt_for_burn}:force_style='{force_style}'",
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{(audio_dur + COVER_DURATION if has_cover else audio_dur):.3f}",
        str(FINAL_OUT),
    ]
    print("\n[FFMPEG] running final mux…")
    res = subprocess.run(cmd, capture_output=True, text=True, cwd=str(BUILD_DIR))
    err_lines = res.stderr.splitlines()
    print("--- last 15 lines of stderr ---")
    print("\n".join(err_lines[-15:]))

    if res.returncode != 0:
        print(f"\n[ERROR] rc={res.returncode}", file=sys.stderr)
        sys.exit(1)

    sz = FINAL_OUT.stat().st_size
    fdur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(FINAL_OUT)],
        capture_output=True, text=True,
    ).stdout.strip())
    print(f"\n[DONE] {FINAL_OUT}")
    print(f"[DONE] SRT deliverable: {FINAL_SRT}")
    print(f"[DONE] SRT for non-burned (original word timings): {FINAL_SRT}")
    if has_cover:
        offset_srt = FINAL_OUT.parent / "subtitles_cover_offset.srt"
        shutil.copy2(str(srt_offset_path), str(offset_srt))
        print(f"[DONE] SRT for burned (offset {COVER_DURATION}s): {offset_srt}")
    print(f"[DONE] size={sz/1024/1024:.1f} MB, duration={fdur:.2f}s ({fdur/60:.2f} min)")


if __name__ == "__main__":
    main()
