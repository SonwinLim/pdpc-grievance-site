from pathlib import Path


ROOT = Path(r"D:/Driving Legal Issue/pdpc-grievance-site")
FRAMES_DIR = ROOT / "Screenshots Video"

SCENE_FRAME = {
    1: "Scene 1.jpg",
    2: "Scene 2.png",
    3: "Scene 3.png",
    4: "Scene 4.png",
    5: "scene 5.png",
    6: "scene 6.jpg",
    7: "scene 7.png",
    8: "scene 8.png",
    9: "scene 9.png",
    10: "Scene 10.jpg",
    11: "Scene 11.png",
    12: "scene 12.jpg",
    13: "scene 13.png",
}


VISUAL_SCHEDULE = [
    {"scene": 1, "frame": "source/scene01_parliament_question.png", "at": 0.00},
    {"scene": 1, "frame": "Scene 1.jpg", "at": 0.36},
    {"scene": 1, "frame": "source/scene01_preservation_penalties.png", "at": 0.68},

    {"scene": 2, "frame": "generated/scene02_memory_gap.png", "at": 0.00},
    {"scene": 2, "frame": "source/scene02_tst_streetview_cameras.png", "at": 0.20},
    {"scene": 2, "frame": "Scene 2.png", "at": 0.40},
    {"scene": 2, "frame": "source/scene02_tst_cctv_location.png", "at": 0.58},
    {"scene": 2, "frame": "source/scene02_tst_accident_location.png", "at": 0.70},
    {"scene": 2, "frame": "source/scene02_suites_cctv_location.png", "at": 0.85},

    {"scene": 3, "frame": "recreated/scene03_tst_refusal.png", "at": 0.00},
    {"scene": 3, "frame": "recreated/scene03_no_company_dpo_escalation.png", "at": 0.13},
    {"scene": 3, "frame": "generated/scene03_office_refusal.png", "at": 0.26},
    {"scene": 3, "frame": "source/scene03_suites_dpo_reply.png", "at": 0.40},
    {"scene": 3, "frame": "Scene 3.png", "at": 0.55},
    {"scene": 3, "frame": "recreated/scene03_difficulty_understanding.png", "at": 0.68},
    {"scene": 3, "frame": "source/scene03_mcst_guideline_police.png", "at": 0.80},
    {"scene": 3, "frame": "source/scene03_pdpa_s21_fifth_schedule.png", "at": 0.90},

    {"scene": 4, "frame": "source/scene04_cctv_captured_not_downloaded.png", "at": 0.00},
    {"scene": 4, "frame": "Scene 4.png", "at": 0.25},
    {"scene": 4, "frame": "source/scene04_17_day_overwrite.png", "at": 0.50},
    {"scene": 4, "frame": "source/scene04_s22a_no_finding.png", "at": 0.68},
    {"scene": 4, "frame": "source/scene04_pdpa_s22a.png", "at": 0.80},
    {"scene": 4, "frame": "source/scene04_pdpc_s22a_admission.png", "at": 0.92},

    {"scene": 5, "frame": "source/scene05_pdpc_complaint_form.png", "at": 0.00},
    {"scene": 5, "frame": "recreated/scene05_10may_reply.png", "at": 0.13},
    {"scene": 5, "frame": "recreated/scene05_not_appropriate_channel.png", "at": 0.25},
    {"scene": 5, "frame": "scene 5.png", "at": 0.40},
    {"scene": 5, "frame": "recreated/scene05_inform_investigation_officer.png", "at": 0.55},
    {"scene": 5, "frame": "recreated/scene05_will_not_look_further.png", "at": 0.68},
    {"scene": 5, "frame": "recreated/scene05_mp_appeal_timeline.png", "at": 0.82},
    {"scene": 5, "frame": "recreated/scene05_deletion_investigated_access_not.png", "at": 0.91},

    {"scene": 6, "frame": "source/scene06_mcst3615_silhouette.png", "at": 0.00},
    {"scene": 6, "frame": "generated/scene06_clarity_machine.png", "at": 0.15},
    {"scene": 6, "frame": "source/scene06_pdpa_personal_data_definition.png", "at": 0.32},
    {"scene": 6, "frame": "source/scene06_no_minimum_resolution.png", "at": 0.48},
    {"scene": 6, "frame": "source/scene06_still_frames_actual_footage.png", "at": 0.62},
    {"scene": 6, "frame": "source/scene06_masking_still_identifiable.png", "at": 0.72},
    {"scene": 6, "frame": "scene 6.jpg", "at": 0.82},
    {"scene": 6, "frame": "source/scene06_key_concepts_identifiability.png", "at": 0.92},

    {"scene": 7, "frame": "source/scene07_mcst3615_reason_shift.png", "at": 0.00},
    {"scene": 7, "frame": "source/scene07_mcst4599_timeline.png", "at": 0.18},
    {"scene": 7, "frame": "scene 7.png", "at": 0.36},
    {"scene": 7, "frame": "recreated/scene07_missing_dates.png", "at": 0.47},
    {"scene": 7, "frame": "source/scene07_pdpa_s21_3.png", "at": 0.58},
    {"scene": 7, "frame": "source/scene07_fifth_schedule.png", "at": 0.76},
    {"scene": 7, "frame": "recreated/scene07_actual_reasons_not_tested.png", "at": 0.88},

    {"scene": 8, "frame": "recreated/scene08_question_cluster_clarity.png", "at": 0.00},
    {"scene": 8, "frame": "recreated/scene08_question_authority.png", "at": 0.07},
    {"scene": 8, "frame": "recreated/scene08_question_cluster_timeline.png", "at": 0.14},
    {"scene": 8, "frame": "recreated/scene08_question_preservation.png", "at": 0.21},
    {"scene": 8, "frame": "source/scene08_pdpa_s4_2_4_3.png", "at": 0.26},
    {"scene": 8, "frame": "scene 8.png", "at": 0.28},
    {"scene": 8, "frame": "source/scene08_pdpc_reasonableness.png", "at": 0.365},
    {"scene": 8, "frame": "source/scene08_pdpc_guidelines_prevail.png", "at": 0.45},
    {"scene": 8, "frame": "recreated/scene08_no_guideline_named.png", "at": 0.535},
    {"scene": 8, "frame": "source/scene08_pdpc_publication_delay.png", "at": 0.62},
    {"scene": 8, "frame": "recreated/scene08_public_record_delay.png", "at": 0.71},
    {"scene": 8, "frame": "recreated/scene08_closed_no_merits_answer.png", "at": 0.80},
    {"scene": 8, "frame": "recreated/scene08_wrong_decision_similarity.png", "at": 0.90},

    {"scene": 9, "frame": "recreated/scene09_imda_escalation.png", "at": 0.00},
    {"scene": 9, "frame": "recreated/scene09_12_emails_11_months.png", "at": 0.15},
    {"scene": 9, "frame": "scene 9.png", "at": 0.30},
    {"scene": 9, "frame": "recreated/scene09_complaint_leaked_back.png", "at": 0.45},
    {"scene": 9, "frame": "source/scene09_imda_iau_finding.png", "at": 0.60},
    {"scene": 9, "frame": "recreated/scene09_active_police_not_listed.png", "at": 0.76},
    {"scene": 9, "frame": "source/scene09_imda_protocols.png", "at": 0.90},

    {"scene": 10, "frame": "source/scene10_pdpc_register.png", "at": 0.00},
    {"scene": 10, "frame": "recreated/scene10_filter_removed.png", "at": 0.18},
    {"scene": 10, "frame": "Scene 10.jpg", "at": 0.35},
    {"scene": 10, "frame": "recreated/scene10_zero_not_one.png", "at": 0.45},
    {"scene": 10, "frame": "source/scene10_access_zero_crop.png", "at": 0.55},
    {"scene": 10, "frame": "source/scene10_protection_204_crop.png", "at": 0.73},
    {"scene": 10, "frame": "source/scene10_pdpa_s24_protection.png", "at": 0.80},
    {"scene": 10, "frame": "source/scene10_pdpa_s25_retention.png", "at": 0.86},
    {"scene": 10, "frame": "recreated/scene10_two_cctv_cases.png", "at": 0.93},

    {"scene": 11, "frame": "recreated/scene11_ordinary_vs_same_direction.png", "at": 0.00},
    {"scene": 11, "frame": "generated/scene11_citizen_pattern.png", "at": 0.18},
    {"scene": 11, "frame": "Scene 11.png", "at": 0.20},
    {"scene": 11, "frame": "recreated/scene11_invented_reasoning_chain.png", "at": 0.40},
    {"scene": 11, "frame": "recreated/scene11_zero_breach_outcome.png", "at": 0.60},
    {"scene": 11, "frame": "recreated/scene11_discretion_vs_denial.png", "at": 0.80},

    {"scene": 12, "frame": "scene 12.jpg", "at": 0.00},
    {"scene": 12, "frame": "source/scene12_site_story.png", "at": 0.22},
    {"scene": 12, "frame": "source/scene12_site_cases_narrative.png", "at": 0.45},
    {"scene": 12, "frame": "source/scene12_site_enforcement_index.png", "at": 0.68},
    {"scene": 12, "frame": "source/scene12_site_failures.png", "at": 0.85},

    {"scene": 13, "frame": "recreated/scene13_statutory_right_question.png", "at": 0.28},
    {"scene": 13, "frame": "generated/scene13_evidence_wall.png", "at": 0.40},
    {"scene": 13, "frame": "scene 13.png", "at": 0.55},
]


def visual_path(frame):
    path = Path(frame)
    if path.is_absolute():
        return path
    return FRAMES_DIR / path


def find_missing_visual_assets(schedule=VISUAL_SCHEDULE):
    return [
        item["frame"] for item in schedule
        if not visual_path(item["frame"]).exists()
    ]


def build_visual_segments(timeline, schedule=VISUAL_SCHEDULE):
    segments = []
    for scene in timeline:
        scene_num = scene["num"]
        scene_start = float(scene["start_s"])
        scene_end = float(scene["end_s"])
        scene_dur = max(scene_end - scene_start, 0.5)
        items = [
            item for item in schedule
            if item["scene"] == scene_num
        ]
        if not items:
            items = [{"scene": scene_num, "frame": SCENE_FRAME[scene_num], "at": 0.0}]
        items = sorted(items, key=lambda item: item["at"])
        for i, item in enumerate(items):
            start_s = scene_start + scene_dur * float(item["at"])
            if i + 1 < len(items):
                end_s = scene_start + scene_dur * float(items[i + 1]["at"])
            else:
                end_s = scene_end
            if end_s <= start_s:
                end_s = min(scene_end, start_s + 0.5)
            segments.append({
                "scene": scene_num,
                "title": scene.get("title", ""),
                "frame": item["frame"],
                "start_s": start_s,
                "end_s": end_s,
            })
    return segments


def extend_last_scene_to_duration(timeline, duration_s):
    if not timeline:
        return timeline
    out = [dict(item) for item in timeline]
    if duration_s > out[-1]["end_s"]:
        out[-1]["end_s"] = float(duration_s)
    return out
