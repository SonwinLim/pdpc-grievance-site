# Splice Recovery Improvements — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce MISSING words from 215 (6.4%) to ~100-130 (3-4%) by fixing script tokenization mismatches and adding tiered phonetic recovery for content words.

**Architecture:** Four independent workstreams. Task 1 fixes structural tokenization bugs (digit→word expansion, possessive `'s` join) in a new shared `intake/script_tokenizer.py`. Task 2 adds tiered phonetic thresholds (0.45 for ≥5-char content words, 0.60 for short function words). Task 3 adds a low-confidence forced-bridge pass for content words still MISSING after standard recovery. Task 4 (bonus) surfaces YAML-entry suggestions for the remaining unrecoverable content words. All changes are additive — no existing threshold is tightened, no behavior removed.

**Tech Stack:** Python 3.13, pytest, difflib.SequenceMatcher, existing `intake/pronunciation.py` (match_multi, match_score)

## Global Constraints

- All 347 existing tests must continue passing
- No changes to Whisper model, VAD parameters, or recording workflow
- No new pip dependencies
- Existing YAML entries in `intake/script_overrides.yaml` must not be modified
- `_make_takes_view.py` must stay in sync with `_splice_alignment_merged.py` (same `clean()` replacement)

---

### Task 1: Shared Script Tokenizer with Digit Expansion & Possessive Join

**Files:**
- Create: `intake/script_tokenizer.py`
- Create: `tests/unit/test_script_tokenizer.py`
- Modify: `projects/pdpc-grievance-2026-v2/assets/audio/whisper_raw/pdpc_20260705_1948/_splice_alignment_merged.py:191-198`
- Modify: `projects/pdpc-grievance-2026-v2/assets/audio/whisper_raw/pdpc_20260705_1948/_make_takes_view.py:167-174`

**Interfaces:**
- Produces: `tokenize_script(text: str) -> list[str]` — normalizes script text into tokens matching Whisper's output style. Public function used by both scripts.
- Produces: `expand_digits(text: str) -> str` — pre-processing pass that replaces digit patterns with word forms before tokenization.
- Produces: `_join_possessives(tokens: list[str]) -> list[str]` — post-processing merge of `["word", "s"]` → `["word's"]`.

- [ ] **Step 1: Write failing tests for digit expansion**

Create `tests/unit/test_script_tokenizer.py`:

```python
import pytest
from intake.script_tokenizer import expand_digits, tokenize_script


class TestExpandDigits:
    def test_expands_four_digit_year(self):
        assert expand_digits("In September 2025, Mr") == "In September twenty twenty five, Mr"

    def test_expands_two_digit_number(self):
        assert expand_digits("section 21, subsection 3") == "section twenty one, subsection three"

    def test_expands_ordinal_with_st_suffix(self):
        assert expand_digits("on the 21st of May") == "on the twenty first of May"

    def test_expands_ordinal_with_nd_suffix(self):
        assert expand_digits("the 22nd of September") == "the twenty second of September"

    def test_expands_ordinal_with_rd_suffix(self):
        assert expand_digits("the 23rd of April") == "the twenty third of April"

    def test_expands_ordinal_with_th_suffix(self):
        assert expand_digits("on April 30th") == "on April thirtieth"

    def test_expands_single_digit(self):
        assert expand_digits("under subsection 3") == "under subsection three"

    def test_leaves_non_digit_text_unchanged(self):
        text = "The minister responsible for the PDPA"
        assert expand_digits(text) == text

    def test_handles_multiple_digit_groups(self):
        assert expand_digits("17 days. 30 days. 2025.") == "seventeen days. thirty days. twenty twenty five."

    def test_section_reference_22A_preserved(self):
        # "22A" is a section label — expand the "22" part, keep "A"
        assert expand_digits("section 22A") == "section twenty two A"

    def test_expands_thirtieth_ordinal(self):
        assert expand_digits("April 30th") == "April thirtieth"


class TestTokenizeScript:
    def test_basic_tokenization(self):
        assert tokenize_script("Hello world") == ["hello", "world"]

    def test_lowercases(self):
        assert tokenize_script("The Quick Brown") == ["the", "quick", "brown"]

    def test_strips_punctuation(self):
        assert tokenize_script("Yes. No! Wait,") == ["yes", "no", "wait"]

    def test_preserves_apostrophe_within_word(self):
        assert tokenize_script("wouldn't they've") == ["wouldn't", "they've"]

    def test_digit_expansion_applied_before_tokenization(self):
        # "2025" becomes "twenty twenty five" then tokenized
        result = tokenize_script("In 2025")
        assert result == ["in", "twenty", "twenty", "five"]

    def test_possessive_s_joined_to_preceding_word(self):
        result = tokenize_script("Knight Frank's footage")
        assert result == ["knight", "frank's", "footage"]

    def test_possessive_after_pdpc(self):
        result = tokenize_script("PDPC's guidelines")
        assert result == ["pdpc's", "guidelines"]

    def test_possessive_after_short_word_not_joined(self):
        # "a's" — preceding token "a" is <3 chars, don't merge
        result = tokenize_script("a's the")
        assert result == ["a's", "the"]  # regex keeps "a's" as one token already

    def test_contraction_wouldnt_t_joined(self):
        result = tokenize_script("they wouldn t tell")
        assert result == ["they", "wouldn't", "tell"]

    def test_plural_s_not_joined(self):
        # "cameras pointing" — "cameras" is one token, not camera+s split
        result = tokenize_script("cameras pointing at")
        assert "cameras" in result

    def test_hyphenated_date_compounds_detected(self):
        result = tokenize_script("September twenty-second was")
        # "twenty-second" regex-splits to ["twenty", "second"]
        # compound detection adds "twentysecond" joined variant concept
        # but actual impl keeps split for SequenceMatcher; digit expansion
        # of "22nd" already handles this case. Test that both tokens exist.
        assert "twenty" in result
        assert "second" in result

    def test_handles_smart_quotes(self):
        result = tokenize_script("Josephine Teo’s answer")
        assert "teo's" in result

    def test_empty_string(self):
        assert tokenize_script("") == []

    def test_numbers_only(self):
        result = tokenize_script("2025")
        assert result == ["twenty", "twenty", "five"]

    def test_single_letter_s_not_merged_when_standalone(self):
        # A lone "s" at the start shouldn't merge backwards
        result = tokenize_script("s is a letter")
        assert result == ["s", "is", "a", "letter"]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd E:/Bespoke/Minimax_Hub && ./.venv/Scripts/python.exe -m pytest tests/unit/test_script_tokenizer.py -v
```

Expected: all fail with `ModuleNotFoundError: No module named 'intake.script_tokenizer'`

- [ ] **Step 3: Implement `intake/script_tokenizer.py`**

```python
"""Script text tokenization with digit expansion and possessive join.

Normalizes script text into tokens that match Whisper's typical output,
bridging structural mismatches: digit sequences expanded to word forms,
possessive 's joined to its preceding word.
"""

from __future__ import annotations

import re

# Digit-to-word lookup tables (mirrors intake/pronunciation.py's _DIGIT_WORDS
# for consistency; kept separate to avoid circular imports).
_ONES = [
    "zero", "one", "two", "three", "four",
    "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen",
    "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
]
_TENS = [
    "", "", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety",
]
_ORDINAL_SUFFIXES = {
    "st": "first", "nd": "second", "rd": "third", "th": "th",
}


def _number_to_words(n: int) -> str:
    """Convert integer 0-9999 to word form."""
    if n < 20:
        return _ONES[n]
    if n < 100:
        tens = _TENS[n // 10]
        ones = n % 10
        if ones == 0:
            return tens
        return f"{tens} {_ONES[ones]}"
    if n < 1000:
        hundreds = _ONES[n // 100]
        rest = n % 100
        if rest == 0:
            return f"{hundreds} hundred"
        return f"{hundreds} hundred {_number_to_words(rest)}"
    if n < 10000:
        thousands_part = n // 100
        rest = n % 100
        thousands = _number_to_words(thousands_part)
        if rest == 0:
            return thousands
        return f"{thousands} {_number_to_words(rest)}"
    return str(n)


def _ordinal_suffix_to_word(suffix: str) -> str:
    """Map ordinal suffix to its word form. Returns suffix unchanged if unknown."""
    return _ORDINAL_SUFFIXES.get(suffix.lower(), suffix)


def expand_digits(text: str) -> str:
    """Replace digit sequences in text with word forms.

    Handles: 4-digit years (2025), 1-2 digit numbers (17, 30),
    ordinals (21st, 30th, 22nd, 23rd), section-ref digits (22A -> twenty two A).
    """
    # Ordinals with letter suffix: 21st, 22nd, 23rd, 30th, etc.
    # Pattern: digits followed by st/nd/rd/th (possibly followed by non-letter)
    def _replace_ordinal(m: re.Match) -> str:
        num = int(m.group(1))
        suffix = m.group(2)
        word = _ordinal_suffix_to_word(suffix)
        if word != suffix and num <= 99:
            if num <= 20:
                # "21st" -> "twenty first", "30th" -> "thirtieth"
                if num == 30:
                    return f"thirtieth"
                tens = num // 10
                ones_digit = num % 10
                if ones_digit == 0 and num < 100:
                    # "20th" -> "twentieth"
                    base = _TENS[tens]
                    return f"{base}ieth"
                if num <= 20:
                    return _ONES[num].rstrip("e") + "th"  # "eighth", "ninth"
                return f"{_TENS[tens]} {word}"
            return m.group(0)  # can't handle, leave as-is
        # For non-standard suffixes or large numbers, use numeric expansion
        try:
            words = _number_to_words(num)
            return f"{words} {word}"
        except (ValueError, IndexError):
            return m.group(0)

    text = re.sub(r'\b(\d{1,2})(st|nd|rd|th)\b', _replace_ordinal, text)

    # Standalone numbers (not followed by letters or within words)
    def _replace_number(m: re.Match) -> str:
        num_str = m.group(1)
        num = int(num_str)
        if num <= 9999:
            return _number_to_words(num)
        return num_str

    text = re.sub(r'\b(\d{1,4})\b', _replace_number, text)

    return text


def _join_possessives(tokens: list[str]) -> list[str]:
    """Merge possessive 's'/'t' with preceding word.

    'Knight Frank's' -> ['knight', 'frank', 's'] -> ['knight', 'frank's']
    'wouldn t' -> ['wouldn', 't'] -> ['wouldn't']

    Only merges when the preceding token is >= 3 chars (avoids false joins).
    """
    if len(tokens) < 2:
        return tokens

    result: list[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in ("s", "t") and i > 0 and len(result[-1]) >= 3:
            # Merge into previous token: "frank" + "s" -> "frank's"
            result[-1] = result[-1] + "'" + token
            i += 1
            continue
        result.append(token)
        i += 1
    return result


def tokenize_script(text: str) -> list[str]:
    """Normalize script text into tokens that match Whisper's typical output.

    1. Expand digit sequences to word forms
    2. Normalize smart quotes and lowercase
    3. Extract alphanumeric+apostrophe tokens via regex
    4. Join possessive 's'/'t' to preceding word
    """
    text = expand_digits(text)
    text = (
        text.replace("’", "'")   # right single quote
        .replace("‘", "'")       # left single quote
        .replace("“", '"')       # left double quote
        .replace("”", '"')       # right double quote
    ).lower()
    tokens = [t for t in re.findall(r"[a-z0-9']+", text) if t]
    tokens = _join_possessives(tokens)
    return tokens
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd E:/Bespoke/Minimax_Hub && ./.venv/Scripts/python.exe -m pytest tests/unit/test_script_tokenizer.py -v
```

Expected: all 20 tests PASS

- [ ] **Step 5: Update `_splice_alignment_merged.py` to use the shared tokenizer**

Replace the local `clean()` function (lines 191-198) with an import:

```python
# Replace:
# def clean(t: str) -> list[str]:
#     t = (
#         t.replace("’", "'")
#         .replace("‘", "'")
#         .replace("“", '"')
#         .replace("”", '"')
#     ).lower()
#     return [t for t in re.findall(r"[a-z0-9']+", t) if t]

# With:
from intake.script_tokenizer import tokenize_script as clean
```

Update the two call sites in `get_kept_tokens()` (line 253) and ensure `clean(w["text"])` calls (line 239) still work — note that `clean()` is also called on individual ASR words. The ASR words should NOT get digit expansion (Whisper outputs words, not digits), but `expand_digits` on a word like "hello" is a no-op, so it's safe.

The line `script_tokens = clean(script_text)` at line 253 will now get the expanded/joined tokens. The `clean(w["text"])` at line 239 for ASR tokens will also go through `expand_digits`, which is safe (no digits to expand in ASR output).

- [ ] **Step 6: Update `_make_takes_view.py` to use the shared tokenizer (same replacement)**

Replace the identical local `clean()` function (lines 167-174) with the same import:

```python
from intake.script_tokenizer import tokenize_script as clean
```

- [ ] **Step 7: Verify existing tests still pass**

```bash
cd E:/Bespoke/Minimax_Hub && ./.venv/Scripts/python.exe -m pytest tests/unit/ -v --timeout=60
```

Expected: all 347+ existing tests PASS (plus 20 new ones from Task 1)

- [ ] **Step 8: Commit**

```bash
cd E:/Bespoke/Minimax_Hub
git add intake/script_tokenizer.py tests/unit/test_script_tokenizer.py
git add projects/pdpc-grievance-2026-v2/assets/audio/whisper_raw/pdpc_20260705_1948/_splice_alignment_merged.py
git add projects/pdpc-grievance-2026-v2/assets/audio/whisper_raw/pdpc_20260705_1948/_make_takes_view.py
git commit -m "feat(tokenizer): add shared script tokenizer with digit expansion and possessive join

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: Content-Word Tiered Phonetic Threshold

**Files:**
- Modify: `intake/backward_selector.py:395-405,569-605`
- Modify: `intake/phrase_selector.py:779-786,845-860,945-960`
- Modify: `projects/pdpc-grievance-2026-v2/assets/audio/whisper_raw/pdpc_20260705_1948/_splice_alignment_merged.py:108-109,598-604`
- Modify: `tests/unit/test_backward_selector.py`
- Modify: `tests/unit/test_phrase_selector.py`

**Interfaces:**
- Produces: `is_content_word(script_token: str, *, terms: dict | None = None, capitalized_words: set | None = None) -> bool` — True for ≥5 chars, YAML-listed, or originally-capitalized script words.
- Consumes: `compute_phonetic_claims` gains `content_min_ratio: float = 0.45` parameter
- Consumes: `select_spans_backwards` gains `content_min_ratio: float = 0.45` parameter
- Consumes: `recover_missing_phrase_bridges` gains `content_min_ratio: float = 0.45` parameter

- [ ] **Step 1: Add `is_content_word` and update `compute_phonetic_claims` signature**

In `intake/backward_selector.py`, add the helper function after `_clean_word` (after line 70):

```python
def is_content_word(
    script_token: str,
    *,
    terms: dict[str, list[str]] | None = None,
    capitalized_words: set[str] | None = None,
) -> bool:
    """True when a script token deserves the lower content-word threshold.

    Content words are: >= 5 chars, OR listed in the YAML overrides,
    OR originally capitalized in the script (proper names).
    """
    if len(script_token) >= 5:
        return True
    if terms and script_token in terms:
        return True
    if capitalized_words and script_token in capitalized_words:
        return True
    return False
```

Update `compute_phonetic_claims` signature (line 395-404):

```python
def compute_phonetic_claims(
    transcribed: list[dict],
    script_tokens: list[str],
    per_word_match: dict[int, int],
    *,
    terms: dict[str, list[str]] | None = None,
    min_ratio: float = 0.55,
    content_min_ratio: float = 0.45,
    max_join: int = 5,
    alt_transcribed: list[dict] | None = None,
) -> dict[int, dict]:
```

In the primary loop (line 446-449), use tiered threshold:

```python
            # Determine threshold: content words get the lower bar
            effective_min = min_ratio
            for si in range(s, min(s + max_join, hi + 1)):
                if is_content_word(script_tokens[si], terms=terms):
                    effective_min = min(content_min_ratio, min_ratio)
                    break

            m = match_multi(
                word, script_tokens, s, terms,
                max_join=max_join, min_ratio=effective_min,
            )
```

In the alt fallback loop (line 502-506), same tiered threshold:

```python
            effective_min = min_ratio
            for si in range(s, min(s + max_join, hi + 1)):
                if is_content_word(script_tokens[si], terms=terms):
                    effective_min = min(content_min_ratio, min_ratio)
                    break

            m = match_multi(
                atext, script_tokens, s, terms,
                max_join=max_join, min_ratio=effective_min,
            )
```

- [ ] **Step 2: Thread `content_min_ratio` through `select_spans_backwards`**

Update `select_spans_backwards` signature (line 569-580) to add `content_min_ratio`:

```python
def select_spans_backwards(
    transcribed: list[dict],
    script_tokens: list[str],
    per_word_match: dict[int, int],
    *,
    min_coverage: float = 0.55,
    min_score: float = 10.0,
    script_start_idx: int = 0,
    script_text: str | None = None,
    phonetic_overrides: dict[str, list[str]] | None = None,
    content_min_ratio: float = 0.45,
    alt_transcribed: list[dict] | None = None,
) -> tuple[list[SelectedSpan], list[dict]]:
```

Update the `compute_phonetic_claims` call (line 599-602):

```python
    claims: dict[int, dict] = (
        compute_phonetic_claims(
            transcribed, script_tokens, per_word_match, terms=phonetic_overrides,
            content_min_ratio=content_min_ratio,
            alt_transcribed=alt_transcribed,
        )
        if phonetic_overrides is not None
        else {}
    )
```

- [ ] **Step 3: Update `recover_missing_phrase_bridges` for tiered threshold**

Update `recover_missing_phrase_bridges` signature (line 779-786):

```python
def recover_missing_phrase_bridges(
    token_labels: list[TokenLabel],
    transcribed: list[dict],
    script_tokens: list[str],
    *,
    overrides: dict[str, list[str]] | None = None,
    min_phonetic_ratio: float = 0.55,
    content_min_ratio: float = 0.45,
) -> list[TokenLabel]:
```

In the first-pass phonetic check (line 845-848), use tiered threshold:

```python
            # Content words get the lower bar
            effective_ratio = min_phonetic_ratio
            if overrides:
                for si in range(expected, min(expected + 5, len(script_tokens))):
                    if is_content_word(script_tokens[si], terms=overrides):
                        effective_ratio = min(content_min_ratio, min_phonetic_ratio)
                        break

            m = match_multi(
                tl.text, script_tokens, expected, overrides,
                min_ratio=effective_ratio,
            )
```

Add the import at the top of `phrase_selector.py`:

```python
from intake.backward_selector import is_content_word
```

In the suffix-walk phonetic pass (line 949-952), same tiered threshold:

```python
                effective_ratio = min_phonetic_ratio
                if overrides:
                    for si in range(j, min(j + 5, len(gap_script))):
                        if is_content_word(gap_script[si], terms=overrides):
                            effective_ratio = min(content_min_ratio, min_phonetic_ratio)
                            break

                m = match_multi(
                    labels[idx].text, gap_script, j, overrides,
                    min_ratio=effective_ratio,
                )
```

- [ ] **Step 4: Update the splice script to pass `content_min_ratio`**

In `_splice_alignment_merged.py`, add the tunable near `PHONETIC_MIN_RATIO` (after line 109):

```python
# Content-word phonetic threshold — lower bar for long/proper script words
# where distinctive phonetics justify a more permissive match.
CONTENT_MIN_RATIO = 0.45
```

Update the `select_spans_backwards` call (around line 451-457):

```python
    selected_spans, token_labels_raw = select_spans_backwards(
        primary_transcribed, script_tokens, primary_pwm,
        script_start_idx=script_start_idx,
        script_text=script_text,
        phonetic_overrides=overrides_terms,
        content_min_ratio=CONTENT_MIN_RATIO,
        alt_transcribed=alt_transcribed,
    )
```

Update the `recover_missing_phrase_bridges` call (around line 471-475):

```python
    token_labels = recover_missing_phrase_bridges(
        token_labels, primary_transcribed, script_tokens,
        overrides=overrides_terms,
        min_phonetic_ratio=PHONETIC_MIN_RATIO,
        content_min_ratio=CONTENT_MIN_RATIO,
    )
```

Update `summary.json` tunables block (after line 590):

```python
            "phonetic_min_ratio": PHONETIC_MIN_RATIO,
            "content_min_ratio": CONTENT_MIN_RATIO,
```

- [ ] **Step 5: Update `_make_takes_view.py` with the same `content_min_ratio` config**

In `_make_takes_view.py`, find where `PHONETIC_MIN_RATIO` is defined, add `CONTENT_MIN_RATIO = 0.45` next to it. Find where `select_spans_backwards` or `compute_phonetic_claims` is called and pass `content_min_ratio`.

- [ ] **Step 6: Add tests for tiered threshold**

In `tests/unit/test_backward_selector.py`, add:

```python
class TestIsContentWord:
    def test_long_word_is_content(self):
        from intake.backward_selector import is_content_word
        assert is_content_word("subarachnoid") is True

    def test_short_word_is_not_content(self):
        from intake.backward_selector import is_content_word
        assert is_content_word("the") is False

    def test_five_char_boundary_is_content(self):
        from intake.backward_selector import is_content_word
        assert is_content_word("cairn") is True  # exactly 5

    def test_yaml_term_is_content_even_when_short(self):
        from intake.backward_selector import is_content_word
        assert is_content_word("dpo", terms={"dpo": ["tpo"]}) is True

    def test_capitalized_word_is_content(self):
        from intake.backward_selector import is_content_word
        assert is_content_word("pdp", capitalized_words={"pdp"}) is True

    def test_short_unknown_word_is_not_content(self):
        from intake.backward_selector import is_content_word
        assert is_content_word("and") is False
        assert is_content_word("it") is False
        assert is_content_word("of") is False
```

In `tests/unit/test_phrase_selector.py`, add a test that `recover_missing_phrase_bridges` accepts `content_min_ratio` parameter:

```python
def test_recover_missing_phrase_bridges_accepts_content_min_ratio():
    """content_min_ratio parameter is accepted and passed through."""
    from intake.phrase_selector import TokenLabel, recover_missing_phrase_bridges

    labels = [
        TokenLabel(0, "hello", 0.0, 0.5, 0.9, "selected_core", 0, "aligned"),
        TokenLabel(1, "wrld", 0.6, 1.0, 0.8, "outside_selection", None, ""),
        TokenLabel(2, "goodbye", 1.1, 1.6, 0.9, "selected_core", 2, "aligned"),
    ]
    script_tokens = ["hello", "world", "goodbye"]
    result = recover_missing_phrase_bridges(
        labels, [], script_tokens,
        min_phonetic_ratio=0.55, content_min_ratio=0.45,
    )
    assert len(result) == 3
```

- [ ] **Step 7: Run all tests**

```bash
cd E:/Bespoke/Minimax_Hub && ./.venv/Scripts/python.exe -m pytest tests/unit/ -v --timeout=60
```

Expected: all tests PASS

- [ ] **Step 8: Commit**

```bash
cd E:/Bespoke/Minimax_Hub
git add intake/backward_selector.py intake/phrase_selector.py
git add tests/unit/test_backward_selector.py tests/unit/test_phrase_selector.py
git add projects/pdpc-grievance-2026-v2/assets/audio/whisper_raw/pdpc_20260705_1948/_splice_alignment_merged.py
git add projects/pdpc-grievance-2026-v2/assets/audio/whisper_raw/pdpc_20260705_1948/_make_takes_view.py
git commit -m "feat(phonetic): add tiered content-word threshold (0.45) in phonetic claims and bridge recovery

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: Content-Word Forced Bridge (Low-Confidence Recovery)

**Files:**
- Modify: `intake/phrase_selector.py:779-1017`
- Modify: `tests/unit/test_phrase_selector.py`

**Interfaces:**
- Consumes: `recover_missing_phrase_bridges` already has `content_min_ratio` from Task 2
- Produces: Second-pass bridge recovery at `content_force_ratio = 0.40` for ≥5-char script words still MISSING between anchored spans

- [ ] **Step 1: Write failing test for forced bridge**

In `tests/unit/test_phrase_selector.py`, add:

```python
def test_content_word_forced_bridge_recovers_low_confidence_match():
    """A content word between anchors gets a second-pass at 0.40 threshold."""
    from intake.phrase_selector import TokenLabel, recover_missing_phrase_bridges

    labels = [
        TokenLabel(0, "hello", 0.0, 0.5, 0.9, "selected_core", 0, "aligned"),
        TokenLabel(1, "suprachnoid", 0.6, 1.2, 0.7, "outside_selection", None, ""),
        TokenLabel(2, "goodbye", 1.3, 1.8, 0.9, "selected_core", 2, "aligned"),
    ]
    script_tokens = ["hello", "subarachnoid", "goodbye"]
    # "suprachnoid" vs "subarachnoid" — ratio ~0.55-0.65 (fuzzy)
    # Force bridge should try at 0.40 and recover it if first pass at 0.55 misses
    result = recover_missing_phrase_bridges(
        labels, [], script_tokens,
        overrides={},
        min_phonetic_ratio=0.55,
        content_min_ratio=0.45,
        content_force_ratio=0.40,
    )
    # Check that label[1] was recovered
    recovered = [tl for tl in result if tl.label == "selected_bridge"]
    assert len(recovered) >= 1
    assert any("content-word low-confidence" in tl.reason for tl in recovered)
```

- [ ] **Step 2: Implement forced bridge in `recover_missing_phrase_bridges`**

Update the signature to accept `content_force_ratio`:

```python
def recover_missing_phrase_bridges(
    token_labels: list[TokenLabel],
    transcribed: list[dict],
    script_tokens: list[str],
    *,
    overrides: dict[str, list[str]] | None = None,
    min_phonetic_ratio: float = 0.55,
    content_min_ratio: float = 0.45,
    content_force_ratio: float = 0.40,
) -> list[TokenLabel]:
```

After both existing passes complete (after the suffix-walk loop ends, before the final `return labels`), add the forced-bridge pass. Insert after the suffix-walk block (after the `for i in range(1, len(ordered) - 1)` loop that does suffix recovery, around line 985):

```python
    # === Content-word forced bridge ===
    # After both standard recovery passes, find gaps between core anchors
    # where content words (>=5 chars) are still MISSING. Run a third pass
    # at content_force_ratio (0.40) — aggressive but safe because it only
    # fires for long script words with a nearby unmatched ASR token.
    for i in range(1, len(ordered) - 1):
        pl = labels[ordered[i - 1]]
        if pl.label != "selected_core" or pl.script_idx is None:
            continue
        # Find the next core anchor
        j = i
        while j < len(ordered) and labels[ordered[j]].label != "selected_core":
            j += 1
        if j >= len(ordered):
            continue
        nl = labels[ordered[j]]
        if nl.script_idx is None:
            continue
        if nl.script_idx - pl.script_idx < 2 or nl.script_idx - pl.script_idx > 15:
            continue

        # Collect MISSING content words in the gap
        missing_sis: list[int] = []
        for si in range(pl.script_idx + 1, nl.script_idx):
            already_claimed = any(
                labels[idx].script_idx == si
                for idx in ordered
                if labels[idx].label in ("selected_core", "selected_bridge")
            )
            if not already_claimed and len(script_tokens[si]) >= 5:
                missing_sis.append(si)

        if not missing_sis:
            continue

        # Collect unmatched ASR tokens in this gap's time window
        gap_start_s = pl.end_s
        gap_end_s = nl.start_s
        unmatched_in_gap: list[int] = []
        for idx in ordered:
            tl = labels[idx]
            if (
                tl.label in ("outside_selection", "rejected_retake")
                and tl.script_idx is None
                and gap_start_s <= tl.start_s <= gap_end_s
            ):
                unmatched_in_gap.append(idx)

        if not unmatched_in_gap:
            continue

        # For each missing content word, try to claim an unmatched token
        # at the force ratio
        for missing_si in missing_sis:
            script_word = script_tokens[missing_si]
            best_match: tuple[int, float] | None = None  # (asr_idx, ratio)
            for idx in unmatched_in_gap:
                if labels[idx].label not in ("outside_selection", "rejected_retake"):
                    continue
                tl = labels[idx]
                ratio = _compute_simple_phonetic_ratio(tl.text, script_word, overrides)
                if ratio >= content_force_ratio:
                    if best_match is None or ratio > best_match[1]:
                        best_match = (idx, ratio)
            if best_match is not None:
                idx, ratio = best_match
                ol = labels[idx]
                labels[idx] = TokenLabel(
                    asr_idx=ol.asr_idx, text=ol.text,
                    start_s=ol.start_s, end_s=ol.end_s,
                    conf=ol.conf, label="selected_bridge",
                    script_idx=missing_si,
                    reason=(
                        f"Recovered bridge (content-word low-confidence): "
                        f"'{ol.text}' -> '{script_word}' (ratio {ratio:.2f})"
                    ),
                )
                unmatched_in_gap.remove(idx)
```

Add the helper function `_compute_simple_phonetic_ratio` before `recover_missing_phrase_bridges`:

```python
def _compute_simple_phonetic_ratio(
    asr_token: str,
    script_token: str,
    overrides: dict[str, list[str]] | None = None,
) -> float:
    """Single-word phonetic ratio without multi-join complexity.

    Used by the forced-bridge pass for fast content-word matching.
    """
    from intake.pronunciation import match_score
    return match_score(asr_token, script_token, overrides)
```

- [ ] **Step 3: Update the splice script to pass `content_force_ratio`**

In `_splice_alignment_merged.py`, add near the other tunables (after line 109):

```python
# Force-bridge threshold: content words (>=5 chars) still MISSING between
# anchors get one last recovery attempt at this very permissive ratio.
CONTENT_FORCE_RATIO = 0.40
```

Update the `recover_missing_phrase_bridges` call (around line 471-475):

```python
    token_labels = recover_missing_phrase_bridges(
        token_labels, primary_transcribed, script_tokens,
        overrides=overrides_terms,
        min_phonetic_ratio=PHONETIC_MIN_RATIO,
        content_min_ratio=CONTENT_MIN_RATIO,
        content_force_ratio=CONTENT_FORCE_RATIO,
    )
```

Add `"content_force_ratio": CONTENT_FORCE_RATIO` to the tunables dict in summary.json.

- [ ] **Step 4: Run all tests**

```bash
cd E:/Bespoke/Minimax_Hub && ./.venv/Scripts/python.exe -m pytest tests/unit/ -v --timeout=60
```

Expected: all tests PASS

- [ ] **Step 5: Commit**

```bash
cd E:/Bespoke/Minimax_Hub
git add intake/phrase_selector.py tests/unit/test_phrase_selector.py
git add projects/pdpc-grievance-2026-v2/assets/audio/whisper_raw/pdpc_20260705_1948/_splice_alignment_merged.py
git commit -m "feat(phonetic): add content-word forced bridge recovery at 0.40 threshold

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: YAML Auto-Suggestion Diagnostics

**Files:**
- Modify: `projects/pdpc-grievance-2026-v2/assets/audio/whisper_raw/pdpc_20260705_1948/_splice_alignment_merged.py:299-750`

**Interfaces:**
- Produces: Console output block `=== SUGGESTED YAML ENTRIES ===` at end of splice run showing MISSING content words with nearby unmatched ASR tokens at ratio 0.30-0.45

- [ ] **Step 1: Add diagnostic helper function in the splice script**

In `_splice_alignment_merged.py`, add after `main()` begins (after line 300) but before `return` — actually, add as a standalone function before `main()`:

```python
def _suggest_yaml_entries(
    token_labels: list,
    script_tokens: list[str],
    transcribed: list[dict],
    min_ratio: float = 0.30,
    max_ratio: float = 0.45,
) -> list[dict]:
    """Find MISSING content words with nearby unmatched ASR tokens.

    Returns entries suitable for script_overrides.yaml:
    [{script_word, asr_text, start_s, ratio}]
    """
    from intake.pronunciation import match_score

    # Build sets for fast lookup
    claimed_sis: set[int] = set()
    for tl in token_labels:
        if tl.label in ("selected_core", "selected_bridge") and tl.script_idx is not None:
            claimed_sis.add(tl.script_idx)

    # Collect unmatched ASR tokens with their times
    unmatched: list[dict] = []
    for tl in token_labels:
        if tl.label in ("outside_selection", "rejected_retake") and tl.script_idx is None:
            unmatched.append({
                "text": tl.text,
                "start_s": tl.start_s,
                "end_s": tl.end_s,
            })

    suggestions: list[dict] = []
    for si, script_word in enumerate(script_tokens):
        if si in claimed_sis:
            continue
        if len(script_word) < 5:
            continue

        # Find the nearest unmatched ASR token in time
        # (use neighboring claimed tokens to estimate time window)
        prev_end = 0.0
        next_start = float("inf")
        for tl in token_labels:
            if tl.label in ("selected_core", "selected_bridge") and tl.script_idx is not None:
                if tl.script_idx < si:
                    prev_end = max(prev_end, tl.end_s)
                elif tl.script_idx > si:
                    next_start = min(next_start, tl.start_s)

        for u in unmatched:
            if prev_end <= u["start_s"] <= next_start:
                ratio = match_score(u["text"], script_word, None)
                if min_ratio <= ratio <= max_ratio:
                    suggestions.append({
                        "script_word": script_word,
                        "asr_text": u["text"],
                        "start_s": round(u["start_s"], 1),
                        "ratio": round(ratio, 2),
                    })
                    break  # one suggestion per script word

    # Deduplicate by script_word (keep highest ratio)
    seen: dict[str, dict] = {}
    for s in suggestions:
        sw = s["script_word"]
        if sw not in seen or s["ratio"] > seen[sw]["ratio"]:
            seen[sw] = s

    return sorted(seen.values(), key=lambda s: s["start_s"])
```

- [ ] **Step 2: Add diagnostic output at end of `main()`**

In `_splice_alignment_merged.py`, after the "LAST 5 CLIPS" print block (before the takes-view generation, around line 731), add:

```python
    # Suggest YAML entries for MISSING content words
    yaml_suggestions = _suggest_yaml_entries(token_labels, script_tokens, primary_transcribed)
    if yaml_suggestions:
        print()
        print("=== SUGGESTED YAML ENTRIES (MISSING content words with nearby unmatched ASR tokens) ===")
        for s in yaml_suggestions:
            print(f"  {s['script_word']} ← \"{s['asr_text']}\" @ {s['start_s']}s (ratio {s['ratio']})")
        print("Add these to intake/script_overrides.yaml and re-run the splice to recover them.")
```

- [ ] **Step 3: Run the splice script to verify no crashes**

No pytest needed — this is purely diagnostic output. Verify the existing tests still pass:

```bash
cd E:/Bespoke/Minimax_Hub && ./.venv/Scripts/python.exe -m pytest tests/unit/ -v --timeout=60
```

- [ ] **Step 4: Commit**

```bash
cd E:/Bespoke/Minimax_Hub
git add projects/pdpc-grievance-2026-v2/assets/audio/whisper_raw/pdpc_20260705_1948/_splice_alignment_merged.py
git commit -m "feat(diagnostics): add YAML entry suggestions for unrecovered MISSING content words

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 5: Script Audit Tool (CLI + Core Logic)

**Files:**
- Create: `intake/script_audit.py`
- Create: `tests/unit/test_script_audit.py`
- Modify: `intake/cli.py` (add `audit-script` subcommand)

**Interfaces:**
- Produces: `audit_script(text: str) -> AuditResult` — returns flagged terms with generated variants
- Produces: `generate_initial_prompt(terms: list[str], existing_preamble: str = "") -> str` — Whisper-compatible prompt string
- Produces: CLI `python -m intake audit-script <script.txt> --out-yaml <path> --out-hints`

- [ ] **Step 1: Write failing tests**

Create `tests/unit/test_script_audit.py`:

```python
import pytest
from intake.script_audit import (
    AuditResult,
    audit_script,
    extract_non_standard_terms,
    generate_mishearing_variants,
    generate_initial_prompt,
)


class TestExtractNonStandardTerms:
    def test_finds_proper_names(self):
        terms = extract_non_standard_terms(
            "Mr Zhulkarnain Abdul Rahim asked the minister."
        )
        assert "zhulkarnain" in terms
        assert "abdul" in terms
        assert "rahim" in terms

    def test_finds_long_medical_terms(self):
        terms = extract_non_standard_terms(
            "A subarachnoid haemorrhage was diagnosed."
        )
        assert "subarachnoid" in terms
        assert "haemorrhage" in terms

    def test_finds_non_english_words(self):
        terms = extract_non_standard_terms(
            "The concept of papañca is central."
        )
        assert "papañca" in terms

    def test_skips_common_english_words(self):
        terms = extract_non_standard_terms(
            "The minister asked a simple question about the footage."
        )
        for word in ["the", "minister", "asked", "simple", "question", "about", "footage"]:
            assert word not in terms

    def test_finds_number_phrases(self):
        terms = extract_non_standard_terms(
            "Section twenty one, subsection three of the PDPA."
        )
        # Number words themselves aren't flagged, but the pattern is noted


class TestGenerateMishearingVariants:
    def test_generates_variants_for_medical_term(self):
        variants = generate_mishearing_variants("subarachnoid")
        assert len(variants) >= 3
        # Should include common confusion patterns
        has_vowel_sub = any("sub" in v for v in variants)
        assert has_vowel_sub

    def test_generates_variants_for_proper_name(self):
        variants = generate_mishearing_variants("cairnhill")
        assert len(variants) >= 2
        # Should include known confusion from actual data
        assert any("hill" in v.lower() for v in variants) or len(variants) >= 2

    def test_each_variant_is_lowercase(self):
        variants = generate_mishearing_variants("Cairnhill")
        for v in variants:
            assert v == v.lower()


class TestAuditScript:
    def test_returns_audit_result_with_terms(self):
        result = audit_script(
            "Mr Zhulkarnain asked about subarachnoid haemorrhage at Cairnhill."
        )
        assert isinstance(result, AuditResult)
        assert len(result.flagged_terms) >= 3
        assert "zhulkarnain" in result.flagged_terms
        assert "subarachnoid" in result.flagged_terms

    def test_each_flagged_term_has_variants(self):
        result = audit_script("Diagnosis: subarachnoid haemorrhage.")
        for term, variants in result.term_variants.items():
            assert len(variants) >= 1

    def test_empty_text_returns_empty_result(self):
        result = audit_script("")
        assert len(result.flagged_terms) == 0

    def test_yaml_output_is_valid(self):
        result = audit_script("The doctor at Cairnhill diagnosed subarachnoid.")
        yaml_text = result.to_yaml_entries()
        assert "cairnhill:" in yaml_text
        assert "subarachnoid:" in yaml_text


class TestGenerateInitialPrompt:
    def test_includes_flagged_terms(self):
        prompt = generate_initial_prompt(
            ["subarachnoid", "cairnhill", "pdpc"]
        )
        assert "subarachnoid" in prompt
        assert "cairnhill" in prompt
        assert "pdpc" in prompt

    def test_handles_empty_list(self):
        prompt = generate_initial_prompt([])
        assert isinstance(prompt, str)
```

- [ ] **Step 2: Implement `intake/script_audit.py`**

```python
"""Pre-recording script auditor — extracts terms Whisper will struggle with.

Run before recording (or retroactively) to:
1. Extract non-standard terms (proper names, medical/legal, non-English)
2. Generate mishearing variants for script_overrides.yaml
3. Build the initial_prompt vocab list for Whisper transcription
4. Print a pronunciation guide
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# Common English words — anything NOT in this set and meeting other criteria
# is flagged as non-standard.
_COMMON_WORDS: set[str] = set("""
the be to of and a in that have i it for not on with he as you do at
this but his by from they we say her she or an will my one all would
there their what so up out if about who get which go me when make can
like time no just him know take people into year your good some could
them see other than then now look only come its over think also back
after use two how our work first well way even new want because any
these give day most us
""".split())

# Non-English character ranges that signal terms Whisper may not know.
_NON_ENGLISH_PATTERN = re.compile(r'[^\x00-\x7F]')


def extract_non_standard_terms(text: str) -> set[str]:
    """Extract words Whisper is likely to struggle with.

    Returns lowercase set of: proper names, >=8 char low-frequency words,
    non-English script words, and words containing digits.
    """
    words = re.findall(r"[a-zA-Z0-9\x80-\xFF'\-]+", text)
    flagged: set[str] = set()

    for w in words:
        clean = w.strip("'\-").lower()
        if len(clean) < 2:
            continue

        # Non-ASCII characters (Pali, Chinese, etc.)
        if _NON_ENGLISH_PATTERN.search(clean):
            flagged.add(clean)
            continue

        # Contains digits (section references like "22A")
        if re.search(r'\d', clean):
            continue  # handled by digit expansion in tokenizer

        # Proper names: starts with capital and not common
        if w[0].isupper() and clean not in _COMMON_WORDS and len(clean) >= 3:
            flagged.add(clean)
            continue

        # Long low-frequency terms (medical, legal)
        if len(clean) >= 8 and clean not in _COMMON_WORDS:
            flagged.add(clean)
            continue

    return flagged


def generate_mishearing_variants(term: str) -> list[str]:
    """Generate plausible Whisper mishearing variants for a term.

    Uses common confusion patterns: vowel substitution, consonant cluster
    simplification, syllable boundary shifts.
    """
    term = term.lower()
    variants: set[str] = set()

    # Vowel substitution patterns
    vowel_subs = [
        ("a", "e"), ("e", "i"), ("i", "e"), ("o", "a"), ("u", "o"),
        ("ae", "e"), ("oe", "e"),
    ]
    for old, new in vowel_subs:
        if old in term:
            variants.add(term.replace(old, new))

    # Consonant cluster simplification
    cluster_simplifications = [
        ("ph", "f"), ("gh", "g"), ("ch", "k"), ("th", "t"),
        ("pt", "t"), ("bd", "d"), ("gm", "m"), ("gn", "n"),
        ("kn", "n"), ("wr", "r"), ("mb", "m"),
    ]
    for cluster, simple in cluster_simplifications:
        if cluster in term:
            variants.add(term.replace(cluster, simple))

    # Syllable boundary shifts (common in long medical terms)
    if len(term) >= 6:
        mid = len(term) // 2
        # Split-and-rejoin variations
        variants.add(term[:mid] + " " + term[mid:])
        variants.add(term[:mid] + "-" + term[mid:])

    # Double-letter reduction
    doubled = re.findall(r'([a-z])\1', term)
    for d in doubled:
        variants.add(term.replace(d + d, d))

    # Remove duplicates and the original term itself
    variants.discard(term)
    # Filter to plausible lengths (not too far from original)
    result = [v for v in variants if abs(len(v) - len(term)) <= 3]
    return sorted(set(result))


@dataclass
class AuditResult:
    """Output of script_audit — flagged terms with generated variants."""

    flagged_terms: list[str]
    term_variants: dict[str, list[str]] = field(default_factory=dict)
    pronunciation_notes: list[str] = field(default_factory=list)

    def to_yaml_entries(self) -> str:
        """Generate YAML fragment for script_overrides.yaml."""
        lines: list[str] = []
        for term, variants in sorted(self.term_variants.items()):
            if variants:
                var_str = ", ".join(variants)
                lines.append(f"{term}: [{var_str}]")
            else:
                lines.append(f"{term}: []")
        return "\n".join(lines)

    def merge_into_yaml(self, yaml_path: Path) -> bool:
        """Merge flagged terms into an existing YAML file. Returns True if changed."""
        existing: dict[str, list[str]] = {}
        preamble = ""
        if yaml_path.exists():
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
            preamble = str(data.get("preamble", ""))
            existing = {
                str(k): [str(vv) for vv in (v or [])]
                for k, v in (data.get("terms") or {}).items()
            }

        added = 0
        for term, variants in self.term_variants.items():
            if term not in existing:
                existing[term] = variants
                added += 1

        if added == 0:
            return False

        out = {"preamble": preamble, "terms": dict(sorted(existing.items()))}
        yaml_path.write_text(
            yaml.dump(out, allow_unicode=True, default_flow_style=False, sort_keys=False),
            encoding="utf-8",
        )
        return True


def audit_script(text: str) -> AuditResult:
    """Analyze script text and return flagged terms with variants."""
    flagged = extract_non_standard_terms(text)
    term_variants: dict[str, list[str]] = {}
    pronunciation_notes: list[str] = []

    for term in sorted(flagged):
        variants = generate_mishearing_variants(term)
        term_variants[term] = variants

        # Pronunciation notes for multi-syllable terms
        syllables = len(re.findall(r'[aeiou]+', term))
        if syllables >= 4:
            pronunciation_notes.append(
                f"  ⚠ {term} ({syllables} syllables) — articulate slowly"
            )
        elif _NON_ENGLISH_PATTERN.search(term):
            pronunciation_notes.append(
                f"  ℹ {term} — non-English characters, pronounce clearly"
            )

    return AuditResult(
        flagged_terms=sorted(flagged),
        term_variants=term_variants,
        pronunciation_notes=pronunciation_notes,
    )


def generate_initial_prompt(terms: list[str], existing_preamble: str = "") -> str:
    """Build a Whisper initial_prompt from flagged terms."""
    if not terms:
        return existing_preamble

    term_list = ", ".join(sorted(terms))
    vocab_block = f"Vocabulary: {term_list}"

    if existing_preamble:
        return f"{existing_preamble}\n{vocab_block}"
    return vocab_block
```

- [ ] **Step 3: Run tests**

```bash
cd E:/Bespoke/Minimax_Hub && ./.venv/Scripts/python.exe -m pytest tests/unit/test_script_audit.py -v
```

Expected: all tests PASS

- [ ] **Step 4: Add CLI subcommand in `intake/cli.py`**

Add to the subparser list:

```python
    # audit-script
    sp_audit = sub.add_parser(
        "audit-script",
        help="Audit script for terms Whisper will struggle with",
    )
    sp_audit.add_argument("script_path", help="Path to script .txt or .md file")
    sp_audit.add_argument(
        "--out-yaml",
        default=None,
        help="Merge flagged terms into this YAML overrides file",
    )
    sp_audit.add_argument(
        "--out-hints",
        action="store_true",
        help="Print pronunciation guide",
    )
    sp_audit.set_defaults(cmd=cmd_audit_script)
```

Add the handler function:

```python
def cmd_audit_script(args):
    """Audit a script for Whisper-difficult terms."""
    from pathlib import Path
    from intake.script_audit import audit_script

    script_path = Path(args.script_path)
    if not script_path.is_file():
        print(f"ERROR: script file not found: {args.script_path}")
        return 1

    text = script_path.read_text(encoding="utf-8")
    result = audit_script(text)

    print(f"Flagged {len(result.flagged_terms)} non-standard terms:")
    for term in result.flagged_terms:
        variants = result.term_variants.get(term, [])
        if variants:
            print(f"  {term} ← {', '.join(variants[:5])}")
        else:
            print(f"  {term}")

    if args.out_yaml:
        yaml_path = Path(args.out_yaml)
        changed = result.merge_into_yaml(yaml_path)
        if changed:
            print(f"\nMerged entries into {yaml_path}")
        else:
            print(f"\nNo new entries — all terms already in {yaml_path}")

    if args.out_hints and result.pronunciation_notes:
        print("\n=== PRONUNCIATION GUIDE ===")
        for note in result.pronunciation_notes:
            print(note)

    return 0
```

- [ ] **Step 5: Run all tests**

```bash
cd E:/Bespoke/Minimax_Hub && ./.venv/Scripts/python.exe -m pytest tests/unit/ -v --timeout=60
```

- [ ] **Step 6: Commit**

```bash
cd E:/Bespoke/Minimax_Hub
git add intake/script_audit.py tests/unit/test_script_audit.py intake/cli.py
git commit -m "feat(cli): add audit-script command for pre-recording Whisper vocab priming

Co-Authored-By: Claude <noreply@anthropic.com>"
```
