"""Convert a scene script .md to yt-intake plan.json format.

Usage:
  python script_to_plan.py <script.md> --out-json <plan.json> --project-id <slug>
"""

import json
import re
import sys
from pathlib import Path


STYLE_PREFIXES = {
    "hand-drawn": "Hand-drawn ink-wash illustration, loose linework, muted palette. ",
    "clean/systemic": "Clean systemic editorial infographic, flat vector, black-white-red. ",
    "mixed": "",  # prompt already describes the transition
}


def parse_timestamp(ts_str):
    """Parse 'M:SS' or 'MM:SS' to total seconds."""
    parts = ts_str.strip().split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    return 0


def extract_field(text, field_name):
    """Extract content of a **Field:** block."""
    pattern = rf"\*\*{field_name}:\*\*\s*\n(.*?)(?=\n\*\*|$)"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def parse_scenes(content):
    """Parse the script markdown into a list of scene dicts."""
    scenes = []

    # Split on scene headers: ---\n## Scene N — Title [start–end] · Ns · style\n---
    scene_pattern = re.compile(
        r'---\s*\n## Scene (\d+)\s*[—–-]\s*(.+?)\s*\[(\d+:\d+)[–-](\d+:\d+)\]\s*·\s*(\d+)s\s*·\s*(.+?)\s*\n---\s*\n(.*?)(?=\n---\s*\n## Scene|\Z)',
        re.DOTALL,
    )

    for match in scene_pattern.finditer(content):
        num, title, start_ts, end_ts, duration, style, body = match.groups()
        scenes.append({
            "number": int(num),
            "title": title.strip(),
            "start_ts": start_ts.strip(),
            "end_ts": end_ts.strip(),
            "start_s": parse_timestamp(start_ts),
            "end_s": parse_timestamp(end_ts),
            "duration_s": int(duration),
            "style": style.strip().split()[0].rstrip(","),
            "what_happened": extract_field(body, "What happened"),
            "narration": extract_field(body, "Narration"),
            "image_prompt": extract_field(body, "Image prompt"),
        })

    return sorted(scenes, key=lambda s: s["number"])


def parse_frontmatter(content):
    """Extract YAML frontmatter fields."""
    fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return {}
    fm = {}
    for line in fm_match.group(1).split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip().strip('"')
    return fm


def build_hook(scenes):
    """Extract first 1-2 sentences of Scene 1 narration as the hook."""
    if not scenes:
        return ""
    narration = scenes[0]["narration"]
    # Take first 2 sentences (split on . ! ?)
    sentences = re.split(r'(?<=[.!?])\s+', narration)
    hook = " ".join(sentences[:2])
    if len(hook) > 200:
        hook = sentences[0] if sentences else hook[:200]
    return hook


def build_plan(script_path, project_id):
    """Build a plan.json dict from a scene script."""
    content = Path(script_path).read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    scenes = parse_scenes(content)

    if not scenes:
        raise ValueError("No scenes found in script")

    target_duration_s = scenes[-1]["end_s"]

    hook = build_hook(scenes)

    beats = []
    for i, scene in enumerate(scenes):
        style_prefix = STYLE_PREFIXES.get(scene["style"], "")
        prompt = style_prefix + scene["image_prompt"] if style_prefix else scene["image_prompt"]

        body = scene["narration"]
        # Scene 1's body starts with the same sentences build_hook() extracted;
        # since _project_script_text() narrates hook + all beat bodies in
        # sequence, leaving them in beats[0] would speak the opening twice.
        if i == 0 and hook and body.startswith(hook):
            body = body[len(hook):].lstrip()

        beats.append({
            "title": f"Scene {scene['number']} — {scene['title']}",
            "body": body,
            "per_frame_prompts": [prompt],
        })

    plan = {
        "title": fm.get("title", project_id),
        "format": "long",
        "platform": "youtube_long",
        "aspect": "16:9",
        "style": "documentary",
        "narration": "ai_voice",
        "target_duration_s": target_duration_s,
        "hook": hook,
        "beats": beats,
    }

    return plan


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert scene script to plan.json")
    parser.add_argument("script", help="Path to scene script .md")
    parser.add_argument("--out-json", required=True, help="Output plan.json path")
    parser.add_argument("--project-id", required=True, help="Project slug/id")
    args = parser.parse_args()

    plan = build_plan(args.script, args.project_id)

    out_path = Path(args.out_json)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"plan.json written to {out_path}")
    print(f"  {len(plan['beats'])} beats, target {plan['target_duration_s']}s")


if __name__ == "__main__":
    main()
