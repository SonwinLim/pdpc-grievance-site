"""Re-transcribe audio with word-level timestamps, align script words to ASR timing, write corrected SRT."""
import json, re, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(r"D:/Driving Legal Issue/pdpc-grievance-site")
AUDIO = Path(r"C:/Users/limzi/Downloads/pdp finalc.wav")
SCRIPT_MD = ROOT / "docs/superpowers/specs/2026-07-04-video-script.md"
OUT_JSON = ROOT / "video_export" / "transcript_word_aligned.json"
OUT_SRT = ROOT / "video_export" / "subtitles_corrected.srt"
OUT_SRT_DELIVER = ROOT / "video_export" / "subtitles.srt"
COVER_OFFSET = ROOT / "video_export" / "subtitles_cover_offset.srt"
COVER_DURATION = 5.0

def norm(w):
    return re.sub(r'[^a-z0-9]', '', w.lower())

def srt_time(s):
    h = int(s // 3600); m = int((s % 3600) // 60); sec = s % 60
    ss = int(sec); ms = int((sec - ss) * 1000)
    return f"{h:02d}:{m:02d}:{ss:02d},{ms:03d}"

# 1. Run whisper (word-level)
print("[1] Running faster-whisper with word timestamps...")
from faster_whisper import WhisperModel
model = WhisperModel("mobiuslabsgmbh/faster-whisper-large-v3-turbo",
                     device="cpu", compute_type="int8")
segments_raw, info = model.transcribe(
    str(AUDIO), word_timestamps=True, vad_filter=True,
    vad_parameters={"min_silence_duration_ms": 400}
)
segments = list(segments_raw)
print(f"[1] {len(segments)} segments, language={info.language}")

# Collect all words with timestamps
all_words = []
for seg in segments:
    if seg.words:
        for w in seg.words:
            all_words.append({"word": w.word.strip(), "start": w.start, "end": w.end, "prob": w.probability})
print(f"[1] {len(all_words)} words with timestamps")

# 2. Extract script narration (all scenes in order, full text with word list)
print("[2] Extracting script narration...")
script_text = SCRIPT_MD.read_text(encoding="utf-8")
scene_blocks = re.split(r'\n(?=## Scene \d+)', script_text)
all_script_words = []
scene_word_ranges = {}  # scene_num -> (start_idx, end_idx) in all_script_words
word_idx = 0

for block in scene_blocks:
    m = re.search(r'## Scene (\d+)[^\n]*\n+', block)
    if not m: continue
    scene_num = int(m.group(1))
    if scene_num == 0: continue  # skip cover
    n_start = block.find("**Narration:**")
    if n_start < 0: continue
    n_end = block.find("**Image prompt:**", n_start)
    if n_end < 0: n_end = len(block)
    narration = block[n_start:n_end].replace("**Narration:**", "").strip()
    narration = re.sub(r'\*\*.*?\*\*', '', narration)
    # Split into words, keeping punctuation attached to the word
    # This is important: we split on whitespace but track position
    raw_words = narration.split()
    start_idx = word_idx
    for rw in raw_words:
        all_script_words.append({"word": rw, "norm": norm(rw)})
        word_idx += 1
    scene_word_ranges[scene_num] = (start_idx, word_idx)

print(f"[2] {len(all_script_words)} script words across {len(scene_word_ranges)} scenes")

# 3. Align script words to ASR words using DP-like greedy + windowed matching
# For each script word, find the best ASR word match, using sequential constraint
print("[3] Aligning script words to ASR timing...")

STOP_WORDS = {"the","a","an","and","of","in","on","to","at","for","is","it","was","were",
    "be","been","being","have","has","had","do","does","did","will","would","shall","should",
    "may","might","must","can","could","i","me","my","we","our","you","your","he","she","they",
    "them","his","her","its","their","this","that","these","those","not","no","nor","or","but",
    "if","then","else","when","where","how","what","which","who","whom","are","am","so","as",
    "by","from","with","about","into","through","during","before","after","above","below",
    "between","out","off","over","under","again","further","each","all","both","few","more",
    "most","other","some","such","only","own","same","than","too","very","just","also","now",
    "here","there","up","down","okay","ok","oh","um","uh","ah","er","hmm","mmm","yeah","yes","no"}

# Pre-filter ASR words: remove very low-prob and filler
asr_content = []
for w in all_words:
    n = norm(w["word"])
    if n and n not in STOP_WORDS and w["prob"] > 0.3:
        asr_content.append(w)

# Build a mapping: for each script word, find best-matching ASR word
# Use a sliding window with sequential constraint
script_timing = []  # (script_word_text, start_s, end_s)
asr_ptr = 0
window_size = 15  # look ahead/behind this many ASR words

for i, sw in enumerate(all_script_words):
    sn = sw["norm"]
    if not sn or sn in STOP_WORDS:
        # Stop words: use timing from nearest timed word, or interpolate
        if script_timing:
            script_timing.append((sw["word"], script_timing[-1][2], script_timing[-1][2] + 0.01))
        else:
            script_timing.append((sw["word"], 0.0, 0.01))
        continue

    # Search window around asr_ptr
    best_score = -1
    best_j = asr_ptr
    search_start = max(0, asr_ptr - 5)
    search_end = min(len(asr_content), asr_ptr + window_size)
    for j in range(search_start, search_end):
        an = norm(asr_content[j]["word"])
        if sn == an:
            best_score = 10.0
            best_j = j
            break
        # Partial match for longer words
        if len(sn) > 3 and len(an) > 3 and (sn in an or an in sn):
            score = min(len(sn), len(an)) / max(len(sn), len(an))
            if score > best_score and score > 0.6:
                best_score = score
                best_j = j

    if best_score >= 0:
        asr_ptr = best_j + 1
        script_timing.append((sw["word"], asr_content[best_j]["start"], asr_content[best_j]["end"]))
    else:
        # No match found in window — use previous timing or interpolate
        if script_timing:
            script_timing.append((sw["word"], script_timing[-1][2], script_timing[-1][2] + 0.01))
        else:
            script_timing.append((sw["word"], 0.0, 0.01))

print(f"[3] {len(script_timing)} script words timed")

# 4. Build SRT — group words into cues of reasonable length
# Merge consecutive script words whose ASR gap is < 0.5s into same cue
# Max cue duration ~5s, max chars ~80 per cue
print("[4] Building SRT...")
cues = []
current_words = []
current_start = None
current_end = None

for text, start, end in script_timing:
    gap = start - current_end if current_end is not None else 0
    current_line = " ".join(current_words)

    if (current_words and (gap > 0.8 or len(current_line) > 70 or end - (current_start or 0) > 5.5)):
        # Flush current cue
        cues.append((current_start, current_end, " ".join(current_words).strip()))
        current_words = []
        current_start = None
        current_end = None

    if current_start is None:
        current_start = start
    current_words.append(text)
    current_end = max(end, current_end or 0)

# Flush last cue
if current_words:
    cues.append((current_start or 0, current_end or 0, " ".join(current_words).strip()))

# Post-process: smooth cue boundaries (don't let a cue end before it starts)
for i in range(len(cues)):
    s, e, t = cues[i]
    if e <= s:
        e = s + 0.5
        cues[i] = (s, e, t)

# Clean up text: remove double spaces, leading/trailing punctuation issues
def clean_text(t):
    t = re.sub(r'\s+', ' ', t).strip()
    # Fix spacing around punctuation
    t = re.sub(r'\s+([,.;:?!])', r'\1', t)
    t = re.sub(r'\(\s+', '(', t)
    t = re.sub(r'\s+\)', ')', t)
    return t

# Write SRT
lines = []
for i, (s, e, t) in enumerate(cues, 1):
    lines.append(f"{i}")
    lines.append(f"{srt_time(s)} --> {srt_time(e)}")
    lines.append(clean_text(t))
    lines.append("")

srt_content = "\n".join(lines)
OUT_SRT.write_text(srt_content, encoding="utf-8")
OUT_SRT_DELIVER.write_text(srt_content, encoding="utf-8")
print(f"[4] {len(cues)} cues written to {OUT_SRT}")

# 5. Write cover-offset SRT
print("[5] Writing cover-offset SRT...")
offset_lines = []
for i, (s, e, t) in enumerate(cues, 1):
    offset_lines.append(f"{i}")
    offset_lines.append(f"{srt_time(s + COVER_DURATION)} --> {srt_time(e + COVER_DURATION)}")
    offset_lines.append(clean_text(t))
    offset_lines.append("")
COVER_OFFSET.write_text("\n".join(offset_lines), encoding="utf-8")
print(f"[5] Cover-offset SRT written: {COVER_OFFSET}")

# 6. Save word-alignment data for future use
json.dump({
    "cues": [{"start_s": s, "end_s": e, "text": clean_text(t)} for s, e, t in cues],
    "whisper_segments": [{"start": s.start, "end": s.end, "text": s.text} for s in segments],
}, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"[6] Alignment data saved to {OUT_JSON}")
print("DONE")
