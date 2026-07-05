"""Strip Scene 0 (non-narrated cover frame) from the video script.
Scene 0's [thumbnail / pre-roll] brackets confuse the script_to_plan.py
regex which expects [M:SS-M:SS] timestamps, so Scene 0 is excluded
from the plan. This script produces a temp copy without Scene 0.
"""
from pathlib import Path
import re

src = Path("docs/superpowers/specs/2026-07-04-video-script.md")
content = src.read_text(encoding="utf-8")

# Match from the divider before "## Scene 0" up to (but not including) "## Scene 1"
pattern = re.compile(
    r"^---[^\n]*\n## Scene 0\b.*?(?=^---[^\n]*\n## Scene 1\b)",
    re.DOTALL | re.MULTILINE,
)
stripped = pattern.sub("", content)

out = Path("scratchpad/script-no-scene0.md")
out.write_text(stripped, encoding="utf-8")
print(f"Source length: {len(content)}")
print(f"Stripped length: {len(stripped)}")
print(f"First 200 chars of stripped:")
print(stripped[:200])
print(f"...")
print(f"First 200 chars of body around Scene 1:")
idx = stripped.find("## Scene 1")
print(stripped[idx:idx + 200])