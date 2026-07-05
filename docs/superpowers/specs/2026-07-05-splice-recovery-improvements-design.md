# Splice Recovery Improvements — Design

**Date:** 2026-07-05
**Context:** `/splicing-own-voice-recordings` skill leaves 215 MISSING words (6.4%) on a 3,337-word legal narration script. Content words like "subarachnoid", "cairnhill", "thirtieth" are MISSING, breaking meaning. The user's recording discipline guarantees every script word is in the audio (last take always complete).

**Root causes identified:**
1. Script tokenization structurally mismatches Whisper's output (possessive `'s` split as separate token, digit-to-word gap, hyphenated terms)
2. Single phonetic threshold (0.55) is too tight for long content words with distinctive phonetics
3. Non-standard terms (medical, legal, proper names) aren't primed in Whisper's vocabulary before transcription
4. No feedback loop from MISSING words back to the overrides YAML

---

## Section 1: Script Tokenization Fixes

Three structural bugs in `clean()` and token processing. Fixes apply retroactively to already-recorded audio — re-running the splice immediately recovers words.

### 1a. Possessive/contraction token join

**Problem:** `clean()` produces `["knight", "frank", "s"]` for "Knight Frank's". Whisper transcribes "Frank's" as one token. The isolated `"s"` token has no ASR match and becomes MISSING (~20 occurrences in this run).

**Fix:** In `get_kept_tokens()`, after `clean()` produces `script_tokens`, add a post-processing pass:
- If token is exactly `"s"` and the preceding token is ≥3 chars, merge: `["frank", "s"]` → `["frank's"]`
- Same for `"t"` following `"wouldn"` → `"wouldn't"`, `"don"` → `"don't"`, etc.
- The `TokenMatch` already carries `asr_text` which may contain punctuation; the merged script token now matches.

**Estimated recovery:** ~25 words.

### 1b. Digit-to-word expansion

**Problem:** `clean()` preserves digits via `[a-z0-9']+` but script digit tokens like `"2025"` never match spoken word-number tokens like `"twenty"` `"twenty"` `"five"`.

**Fix:** Before `clean()`, scan the script text for digit sequences and expand them:
- `"2025"` → `"twenty twenty five"`
- `"30"` → `"thirty"`
- `"17th"` → `"seventeenth"`
- `"21,"` → `"twenty one"` (already partially handled by phonetic override — make it structural)

Apply the `num2words` library or a hand-rolled lookup for common date/number patterns. The expansion happens to the script text string before tokenization, so downstream code is unchanged.

**Estimated recovery:** ~15 words (mostly date components).

### 1c. Hyphenated compound join

**Problem:** `"twenty-second"` → `["twenty", "second"]`. Whisper may output `"twenty-second"` as one token (regex keeps it). Only "twenty" matches; "second" MISSING.

**Fix:** Post-tokenization: detect consecutive number-words that form common compounds (`"twenty" + "second"`, `"thirty" + "first"`, etc.) and create a joined variant token. Try matching against both the split and joined forms.

**Estimated recovery:** ~10 words.

### Total Section 1: ~50 MISSING words recovered

---

## Section 2: Content-Word Tiered Recovery

### 2a. Tiered phonetic threshold

**Problem:** Single `PHONETIC_MIN_RATIO = 0.55` for all words. Loose enough to occasionally false-match short words, tight enough to miss long content words with real phonetic similarity.

**Fix:** Two-tier threshold in `compute_phonetic_claims` and `recover_missing_phrase_bridges`:

| Tier | Criteria | Threshold |
|---|---|---|
| Content word | ≥5 chars OR in `script_overrides.yaml` OR capitalized in original | **0.45** |
| Function word | <5 chars AND not in overrides | **0.60** (raised from 0.55) |

The 3-char length guard (anti-noise) remains — it applies to the ASR token, not the script word. A 2-char ASR token like `"oh"` still can't claim anything. A 5-char script word like `"subarachnoid"` can be claimed by a 4+ char ASR token at 0.45+.

**Configuration:** Thresholds are tunables in the splice script, not hardcoded. Existing behavior preserved if user sets both to 0.55.

### 2b. Content-word forced bridge

**Problem:** `recover_missing_phrase_bridges` walks the suffix of the preceding span, tries phonetic match at the standard threshold. If no match, the gap's unmatched tokens are left unused — even when a content word clearly corresponds to one of them.

**Fix:** After the first-pass bridge recovery, for any gap that still contains MISSING content words (≥5 chars):
1. Collect all unmatched ASR tokens in the gap's time window
2. Try phonetic match at **0.40** threshold
3. If one claims a content word, label it `selected_bridge` with reason `"Recovered bridge (content-word low-confidence)"`
4. These appear in `summary.json["phonetic_overrides_used"]` with a distinct marker for review

The 0.40 threshold is aggressive but safe: it only fires for ≥5 char script words with a nearby ASR token, and the review surface flags it explicitly.

### Total Section 2: ~30-40 MISSING words recovered

---

## Section 3: Pre-Recording Script Audit Tool

New module: `intake/script_audit.py`. Run once before recording. Retroactively applicable — generates YAML entries and vocab hints that feed the existing pipeline for re-transcription.

### 3a. Non-standard term extraction

Given script text, identify every word Whisper is likely to struggle with:
- Proper names (capitalized words not in a common-words dictionary)
- Medical/legal terms (≥8 chars, low frequency)
- Non-English words (Pali, Chinese, Malay — already covered by YAML but audit surfaces new ones)
- Number-word phrases (dates, times, section references)

### 3b. Auto-generated mishearing variants

For each flagged term, use `pronunciation.normalize_phonetic` plus common Whisper confusion patterns to generate likely mishearings:
- Vowel substitution (ə→a, ɒ→o)
- Consonant cluster simplification (bn→b, gm→m)
- Syllable boundary shifts
- Common digit confusions

Output as `script_overrides.yaml` entries. Merge with existing entries (never overwrite manually-curated lines).

### 3c. initial_prompt generation

Feeds all flagged terms into `build_initial_prompt()` so Whisper is primed. Already wired — audit tool just provides the complete list automatically.

### 3d. Pronunciation guide

Prints a human-readable guide grouping terms by difficulty, flagging >3 syllable words and non-English phonemes. Optional: suggests which words to articulate most carefully.

### CLI

```bash
python -m intake audit-script <script.txt|script.md> \
  --project <pid> \
  --out-yaml intake/script_overrides.yaml \
  --out-hints
```

`--out-yaml` merges into existing overrides. `--out-hints` prints the pronunciation guide.

---

## Section 4: YAML Auto-Suggestion in Diagnostics

**Problem:** After the splice runs, content words that couldn't be recovered (ratio below even the content-word threshold) are just reported as MISSING with no actionable path.

**Fix:** At the end of the splice run, print a new block:

```
=== SUGGESTED YAML ENTRIES (MISSING content words with nearby unmatched ASR tokens) ===
  subarachnoid ← "super rack noid" @ 94.2s (ratio 0.42)
  thirtieth ← "30th" @ 782.1s (ratio 0.38)
```

These are pairs where:
- Script word is ≥5 chars AND MISSING
- An unmatched ASR token exists in the same time region
- The phonetic ratio is 0.30–0.45 (below even the content-word threshold)

The user can add these to `script_overrides.yaml` and re-run. The diagnostic doesn't auto-apply — it surfaces the information.

---

## Implementation Order

| Step | Module(s) | Tests existing audio? | Est. MISSING → |
|---|---|---|---|
| 1 | Tokenization fixes (`_splice_alignment_merged.py`, token processing) | Yes — re-run splice | ~165 |
| 2 | Content-word tiered thresholds + forced bridge (`backward_selector.py`, `phrase_selector.py`) | Yes — re-run splice | ~125-135 |
| 3 | Script audit tool (`intake/script_audit.py` — new) | Requires re-transcription | ~105-115 |
| 4 | YAML auto-suggestion diagnostics (`_splice_alignment_merged.py`) | Informational only | surfaces gaps |

After steps 1-2 alone (same audio, same words.json, just better matching): ~80-90 MISSING words recovered. Content-word MISSING should approach zero.

## Non-Goals

- No changes to Whisper model or VAD parameters
- No changes to the recording discipline or workflow
- No real-time transcription feedback
- No patch-recording / re-recording workflow (deferred to separate design)
- No removal of existing recovery mechanisms

## Testing

- All 347 existing tests must continue passing
- New unit tests for: possessive join, digit expansion, hyphen join, tiered threshold selection, content-word forced bridge
- Re-run on the PDPC audio (pdpc.wav) and verify MISSING count drops
- Ear-check: listen to the spliced mp3, verify no false claims in recovered content words
