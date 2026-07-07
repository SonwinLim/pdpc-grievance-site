"""Convert number words to digits in SRT files, handling years, dates, times, ordinals."""
import re
from pathlib import Path

ROOT = Path(r"D:/Driving Legal Issue/pdpc-grievance-site")
SRT_IN = ROOT / "video_export" / "subtitles_corrected.srt"

# Ordered: longest/most-specific first to avoid partial matches
NUMBER_MAP = [
    # Ordinals
    ("twenty-second", "22nd"), ("twenty-first", "21st"), ("twentieth", "20th"),
    ("nineteenth", "19th"), ("eighteenth", "18th"), ("seventeenth", "17th"),
    ("sixteenth", "16th"), ("fifteenth", "15th"), ("fourteenth", "14th"),
    ("thirteenth", "13th"), ("twelfth", "12th"), ("eleventh", "11th"),
    ("tenth", "10th"), ("ninth", "9th"), ("eighth", "8th"),
    ("seventh", "7th"), ("sixth", "6th"), ("fifth", "5th"),
    ("fourth", "4th"), ("third", "3rd"), ("second", "2nd"), ("first", "1st"),
    # Year-like patterns (keep these before single-number words)
    ("twenty twenty-five", "2025"), ("twenty twenty-four", "2024"),
    ("twenty twenty-six", "2026"),
    # Time-like: "five oh six" → "5:06 AM"
    ("five oh six", "5:06"), ("five o six", "5:06"),
    # Decades
    ("nineteen eighty-six", "1986"),
    # Counts / clauses
    ("three hundred and eighty-four", "384"),
    ("three hundred eighty-four", "384"),
    # Multi-word numbers (before singles)
    ("thirty-first", "31st"), ("thirty", "30"),
    ("twenty-nine", "29"), ("twenty-eight", "28"), ("twenty-seven", "27"),
    ("twenty-six", "26"), ("twenty-five", "25"), ("twenty-four", "24"),
    ("twenty-three", "23"), ("twenty-two", "22"), ("twenty-one", "21"),
    ("twenty", "20"),
    ("nineteen", "19"), ("eighteen", "18"), ("seventeen", "17"),
    ("sixteen", "16"), ("fifteen", "15"), ("fourteen", "14"),
    ("thirteen", "13"), ("twelve", "12"), ("eleven", "11"),
    ("ten", "10"), ("nine", "9"), ("eight", "8"), ("seven", "7"),
    ("six", "6"), ("five", "5"), ("four", "4"), ("three", "3"),
    ("two", "2"), ("one", "1"), ("zero", "0"),
    # Ordinal short forms in text
    *[(f"{m}th", f"{d}th") for m, d in [
        ("thirtieth","30"),("twenty-ninth","29"),("twenty-eighth","28"),
        ("twenty-seventh","27"),("twenty-sixth","26"),("twenty-fifth","25"),
        ("twenty-fourth","24"),("twenty-third","23"),("twenty-second","22"),
        ("twenty-first","21")]],
]

def convert_numbers(text):
    """Replace number words with digits. Case-insensitive but preserves surrounding context."""
    result = text
    # Sort by longest phrase first to avoid partial matches
    for word, digit in sorted(NUMBER_MAP, key=lambda x: -len(x[0])):
        # Match whole word/phrase only (word boundaries or numbers)
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        result = pattern.sub(digit, result)
    return result

def process_srt(input_path, output_path):
    content = input_path.read_text(encoding="utf-8")
    # Split into blocks (separated by blank lines)
    blocks = content.strip().split("\n\n")
    out_blocks = []
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            out_blocks.append(block)
            continue
        # Lines 0 = index, 1 = timestamp, 2+ = text
        text_lines = lines[2:]
        text = "\n".join(text_lines)
        converted = convert_numbers(text)
        if converted != text:
            lines[2:] = converted.split("\n")
        out_blocks.append("\n".join(lines))

    out_text = "\n\n".join(out_blocks) + "\n"
    output_path.write_text(out_text, encoding="utf-8")
    return len(out_blocks) - 1  # cue count

if __name__ == "__main__":
    n = process_srt(SRT_IN, SRT_IN)
    print(f"[DIGITS] {n} cues processed in {SRT_IN.name}")
    deliver = ROOT / "video_export" / "subtitles.srt"
    process_srt(SRT_IN, deliver)
    print(f"[DIGITS] wrote {deliver.name}")
    offset = ROOT / "video_export" / "subtitles_cover_offset.srt"
    process_srt(offset, offset)
    print(f"[DIGITS] wrote {offset.name}")
