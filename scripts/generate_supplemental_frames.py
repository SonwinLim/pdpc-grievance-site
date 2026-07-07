from pathlib import Path
import shutil
import textwrap

import fitz
from PIL import Image, ImageDraw, ImageFont, ImageOps

from video_visuals import FRAMES_DIR, VISUAL_SCHEDULE, find_missing_visual_assets


ROOT = Path(r"D:/Driving Legal Issue")
SITE_ROOT = Path(r"D:/Driving Legal Issue/pdpc-grievance-site")
W, H = 1920, 1080
RED = "#C41230"
INK = "#111111"
MUTED = "#5b6470"
PAPER = "#f7f4ee"
NAVY = "#111827"


def font(size, bold=False):
    names = ["arialbd.ttf" if bold else "arial.ttf", "segoeuib.ttf" if bold else "segoeui.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


F_TITLE = font(56, True)
F_SUB = font(30)
F_BODY = font(38)
F_BODY_BOLD = font(38, True)
F_SMALL = font(24)
F_TINY = font(18)


def ensure_dirs():
    for name in ("source", "recreated", "generated"):
        (FRAMES_DIR / name).mkdir(parents=True, exist_ok=True)


def wrap(text, width):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph.strip():
            lines.append("")
            continue
        lines.extend(textwrap.wrap(paragraph, width=width))
    return lines


def draw_wrapped(draw, xy, text, width, fill=INK, body_font=F_BODY, line_gap=10):
    x, y = xy
    for line in wrap(text, width):
        draw.text((x, y), line, fill=fill, font=body_font)
        y += body_font.size + line_gap
    return y


def title_bar(draw, title, subtitle=None, dark=False):
    bg = NAVY if dark else "#ffffff"
    fg = "#ffffff" if dark else INK
    draw.rectangle([0, 0, W, 118], fill=bg)
    draw.rectangle([0, 112, W, 118], fill=RED)
    draw.text((70, 28), title, fill=fg, font=F_TITLE)
    if subtitle:
        draw.text((70, 82), subtitle, fill=fg if dark else MUTED, font=F_SMALL)


def save_card(path, title, blocks, subtitle=None, footer=None, dark=False):
    img = Image.new("RGB", (W, H), NAVY if dark else PAPER)
    draw = ImageDraw.Draw(img)
    title_bar(draw, title, subtitle, dark=dark)
    y = 170
    for block in blocks:
        kind = block.get("kind", "body")
        text = block["text"]
        if kind == "quote":
            draw.rounded_rectangle([95, y, W - 95, y + 170], radius=16, fill="#ffffff", outline="#d1d5db", width=2)
            draw.rectangle([95, y, 108, y + 170], fill=RED)
            draw_wrapped(draw, (135, y + 34), text, 66, body_font=F_BODY_BOLD)
            y += 205
        elif kind == "label":
            draw.text((100, y), text, fill=RED, font=F_BODY_BOLD)
            y += 60
        else:
            y = draw_wrapped(draw, (100, y), text, 76, fill="#ffffff" if dark else INK, body_font=F_BODY)
            y += 36
    if footer:
        draw.rectangle([0, H - 80, W, H], fill="#ffffff" if not dark else "#0b1220")
        draw.text((70, H - 52), footer, fill=MUTED if not dark else "#cbd5e1", font=F_SMALL)
    out = FRAMES_DIR / path
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=95)


def save_simple_generated(path, title, prompt_summary, motif):
    img = Image.new("RGB", (W, H), "#e9ecef")
    draw = ImageDraw.Draw(img)
    title_bar(draw, title, "Generated storyboard frame, subtitle-safe composition")
    if motif == "hospital":
        draw.rounded_rectangle([260, 420, 1080, 680], radius=30, fill="#dbe7f3", outline="#9aaabd", width=3)
        draw.rectangle([320, 515, 980, 620], fill="#f8fafc")
        draw.ellipse([520, 450, 650, 575], fill="#cbd5e1")
        draw.line([850, 320, 1120, 250], fill="#f59e0b", width=8)
        draw.text((1220, 360), "05:06", fill=RED, font=font(76, True))
    elif motif == "road":
        draw.polygon([(360, 820), (760, 260), (1160, 260), (1560, 820)], fill="#d7dee5")
        draw.rectangle([270, 220, 520, 820], fill="#6b7280")
        draw.rectangle([1400, 220, 1650, 820], fill="#6b7280")
        draw.ellipse([760, 740, 900, 860], fill="#111827")
        draw.arc([250, 160, 410, 320], 200, 340, fill=RED, width=8)
        draw.arc([1510, 160, 1670, 320], 200, 340, fill=RED, width=8)
    elif motif == "office":
        draw.rectangle([220, 420, 1550, 620], fill="#cbd5e1")
        draw.rectangle([1120, 250, 1450, 620], fill="#64748b")
        draw.ellipse([480, 300, 620, 440], fill="#94a3b8")
        for i, label in enumerate(["no company name", "no DPO contact", "no escalation path"]):
            draw.rounded_rectangle([760, 270 + i * 90, 1200, 330 + i * 90], radius=10, fill="#ffffff")
            draw.text((790, 285 + i * 90), label, fill=RED, font=F_SMALL)
    elif motif == "machine":
        draw.rectangle([780, 280, 1440, 760], fill="#ffffff", outline="#111827", width=5)
        draw.text((890, 330), "clarity test", fill=RED, font=font(54, True))
        draw.rectangle([280, 430, 640, 650], fill="#111827")
        draw.rectangle([320, 470, 600, 610], fill="#94a3b8")
        draw.line([640, 540, 780, 540], fill=RED, width=10)
        draw.rounded_rectangle([1120, 610, 1660, 760], radius=18, fill="#fee2e2")
        draw.text((1160, 650), "identifiability + other information", fill=INK, font=F_BODY_BOLD)
    else:
        for i in range(7):
            x = 360 + i * 170
            draw.rectangle([x, 250, x + 110, 780], fill="#ffffff", outline="#d1d5db", width=2)
        draw.ellipse([180, 690, 310, 820], fill="#64748b")
        draw.line([310, 730, 1420, 490], fill=RED, width=7)
    draw_wrapped(draw, (100, 880), prompt_summary, 86, fill=MUTED, body_font=F_SMALL, line_gap=8)
    out = FRAMES_DIR / path
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=95)


def render_pdf_source(path, title, pdf_path, search_terms, footer):
    doc = fitz.open(pdf_path)
    page_index = None
    highlights = []
    for i, page in enumerate(doc):
        for term in search_terms:
            found = page.search_for(term)
            if found:
                page_index = i
                highlights.extend(found[:3])
        if highlights:
            break
    if page_index is None:
        doc.close()
        raise SystemExit(
            f"[render_pdf_source] no search term matched in {Path(pdf_path).name} "
            f"for {path} (terms: {search_terms})"
        )
    page = doc[page_index]
    for rect in highlights:
        annot = page.add_highlight_annot(rect)
        annot.set_colors(stroke=(1, 0.86, 0.2))
        annot.update()
    pix = page.get_pixmap(matrix=fitz.Matrix(1.8, 1.8), alpha=False)
    page_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    title_bar(draw, title, f"Source page {page_index + 1}: {Path(pdf_path).name}")
    page_img.thumbnail((W - 180, H - 230), Image.Resampling.LANCZOS)
    x = (W - page_img.width) // 2
    y = 150
    canvas.paste(page_img, (x, y))
    draw.rectangle([0, H - 72, W, H], fill="#ffffff")
    draw.text((70, H - 48), footer, fill=MUTED, font=F_SMALL)
    out = FRAMES_DIR / path
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=95)
    doc.close()


def image_frame(path, title, src, footer):
    img = Image.open(src).convert("RGB")
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    title_bar(draw, title, Path(src).name)
    img = ImageOps.contain(img, (W - 180, H - 230), Image.Resampling.LANCZOS)
    canvas.paste(img, ((W - img.width) // 2, 150))
    draw.rectangle([0, H - 72, W, H], fill="#ffffff")
    draw.text((70, H - 48), footer, fill=MUTED, font=F_SMALL)
    out = FRAMES_DIR / path
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=95)


def copy_existing(path, src):
    out = FRAMES_DIR / path
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, out)


def main():
    ensure_dirs()

    pdpa = ROOT / "PDPA ACT and Advisory/Personal Data Protection Act 2012.pdf"
    selected = ROOT / "PDPA ACT and Advisory/Advisory Guidelines on the PDPA for Selected Topics 17 May 2022.pdf"
    mcst_guideline = ROOT / "PDPA ACT and Advisory/Advisory Guidelines for Management Corporations 17 May 2022.pdf"
    mcst4599 = ROOT / "PDPC Rulings/Decision MCST 4599 DP-2405-C2318.pdf"
    mcst3615 = ROOT / "PDPC Rulings/Summary of Commission's Findings - MCST 3615 DP-2405-C2445.pdf"

    render_pdf_source("source/scene01_parliament_question.png", "Parliament Asked The Preservation Question", ROOT / "PDPC Complain/To Parliament/Annex A Parliamentary Question CAA20251108 1504.pdf", ["preserve", "CCTV"], "Parliamentary question package")
    copy_existing("source/scene01_preservation_penalties.png", SITE_ROOT / "hansard.jpg")
    image_frame("source/scene02_tst_cctv_location.png", "The Scotts Tower CCTV Location", ROOT / "Certification/TST CCTV Location.JPG", "Contemporaneous CCTV-location evidence")
    image_frame("source/scene02_suites_cctv_location.png", "Suites@Cairnhill CCTV Location", ROOT / "Certification/Suites CCTV Location.JPG", "Contemporaneous CCTV-location evidence")

    render_pdf_source("source/scene03_pdpa_s21_fifth_schedule.png", "Only Statutory Refusal Grounds Count", pdpa, ["FIFTH SCHEDULE", "Exceptions from access requirement"], "PDPA 2012, s.21 and Fifth Schedule")
    render_pdf_source("source/scene04_cctv_captured_not_downloaded.png", "CCTV Captured The Accident", mcst4599, ["did capture the CCTV Footage", "unable to download"], "PDPC Decision MCST 4599")
    render_pdf_source("source/scene04_17_day_overwrite.png", "The 17-Day Overwrite Window", mcst4599, ["only retained footage for 17 days", "overwritten on 30 April 2024"], "PDPC Decision MCST 4599")
    render_pdf_source("source/scene04_s22a_no_finding.png", "s.22A No-Finding Reasoning", mcst4599, ["no longer existed on the date", "does not make this finding"], "PDPC Decision MCST 4599")
    render_pdf_source("source/scene05_pdpc_complaint_form.png", "PDPC Complaint Filed", ROOT / "Emails with TST/PDPC - Data Protection Complaint Form.pdf", ["complaint", "CCTV"], "Official PDPC complaint form")
    render_pdf_source("source/scene06_mcst3615_silhouette.png", "MCST 3615: Silhouette Reasoning", mcst3615, ["silhouette", "facial features", "license plate"], "PDPC Summary MCST 3615")
    render_pdf_source("source/scene06_pdpa_personal_data_definition.png", "PDPA Personal Data Definition", pdpa, ["from that data and other information", "is likely to have access"], "PDPA 2012, s.2(1)")
    render_pdf_source("source/scene06_no_minimum_resolution.png", "No Minimum Resolution Requirement", selected, ["The PDPA does not prescribe any minimum resolution"], "Selected Topics Guidelines, para 4.57")
    render_pdf_source("source/scene06_still_frames_actual_footage.png", "Still Frames Or Actual Footage", selected, ["providing either still frames", "actual footage itself"], "Selected Topics Guidelines, para 4.58")
    render_pdf_source("source/scene07_mcst3615_reason_shift.png", "MCST 3615: Actual Reason vs PDPC Reason", mcst3615, ["MA refused the request on 21", "Access Obligation"], "PDPC Summary MCST 3615")
    render_pdf_source("source/scene07_mcst4599_timeline.png", "MCST 4599 Timeline Shift", mcst4599, ["29 April", "30 April", "2 May"], "PDPC Decision MCST 4599")
    render_pdf_source("source/scene07_pdpa_s21_3.png", "PDPA s.21(3)", pdpa, ["Subject to subsection (3A)", "must not provide"], "PDPA 2012, s.21(3)")
    render_pdf_source("source/scene07_fifth_schedule.png", "Fifth Schedule", pdpa, ["EXCEPTIONS FROM ACCESS REQUIREMENT"], "PDPA 2012, Fifth Schedule")
    render_pdf_source("source/scene04_pdpa_s22a.png", "s.22A Preservation Duty", pdpa,
                      ["the organisation must preserve, for not less than the prescribed period", "is a complete and accurate copy of the personal data"],
                      "PDPA 2012, s.22A")
    render_pdf_source("source/scene08_pdpa_s4_2_4_3.png", "Data Intermediary vs Organisation", pdpa,
                      ["as if the personal data were processed by the organisation", "other than the obligations under sections 24"],
                      "PDPA 2012, s.4(2) and s.4(3)")
    render_pdf_source("source/scene10_pdpa_s24_protection.png", "s.24 Protection Obligation", pdpa,
                      ["by making reasonable security arrangements to prevent"],
                      "PDPA 2012, s.24")
    render_pdf_source("source/scene10_pdpa_s25_retention.png", "s.25 Retention Limitation", pdpa,
                      ["or remove the means by which the personal data can be associated", "is no longer being served by retention of the personal data"],
                      "PDPA 2012, s.25")
    copy_existing("source/scene10_access_zero_crop.png", SITE_ROOT / "BreachBreakdown.jpg")
    copy_existing("source/scene10_protection_204_crop.png", SITE_ROOT / "BreachBreakdown.jpg")

    save_card("source/scene10_pdpc_register.png", "PDPC Enforcement Register", [{"text": "Published enforcement decisions were manually enumerated after the obligation-type filter disappeared from the public page."}], footer="Source: PDPC public register and site enforcement-index.html")
    save_card("source/scene12_site_story.png", "pdpaaccessrights.sg: Story Section", [{"text": "The site explains the case in five acts before sending readers into the detailed evidence."}], footer="Live site section: #story")
    save_card("source/scene12_site_cases_narrative.png", "Cases And Narrative Sections", [{"text": "The site places MCST 3615 and MCST 4599 side by side, then contrasts PDPC’s narrative against the documentary record."}], footer="Live site sections: #cases and #narrative")
    save_card("source/scene12_site_enforcement_index.png", "Enforcement Index", [{"text": "The enforcement index documents the 384-case obligation matrix and the zero Access Obligation breach pattern."}], footer="Live site page: enforcement-index.html")
    save_card("source/scene12_site_failures.png", "Documented Failures", [{"text": "The failures section compiles the procedural and statutory issues with source links."}], footer="Live site section: #failures")

    cards = {
        "recreated/scene03_tst_refusal.png": ("The Scotts Tower Refusal", ["17 Apr 2024: access refused on privacy grounds.", "No company name. No DPO contact. No escalation path."]),
        "recreated/scene03_no_company_dpo_escalation.png": ("No Route To Escalate", ["The request stalled before the Complainant could even identify the responsible organisation."]),
        "recreated/scene03_suites_police_only.png": ("Suites DPO Reply", ["“Only by police direct/order the MCST to disclose the footage that MCST is obliged to do so.”"]),
        "recreated/scene03_difficulty_understanding.png": ("DPO Follow-Up", ["“It seems to me you are having difficulty understanding our position.”"]),
        "recreated/scene05_10may_reply.png": ("PDPC Reply, 10 May 2024", ["“We regret that we are unable to assist you on the matter.”"]),
        "recreated/scene05_not_appropriate_channel.png": ("PDPC’s Channel Reasoning", ["“An access request made under section 21 of the PDPA is not the appropriate channel.”"]),
        "recreated/scene05_inform_investigation_officer.png": ("PDPC’s Practical Deflection", ["“Please consider informing the Investigation Officer on the possible existence of the CCTV footage.”"]),
        "recreated/scene05_will_not_look_further.png": ("PDPC Closed The Complaint", ["“We will not be looking into your complaint further.”", "“We will not be responding to further correspondence.”"]),
        "recreated/scene05_mp_appeal_timeline.png": ("Intervention Did Not Move The Position", ["MP intervention, twice.", "Appeal.", "No change on privacy, police-only access, or deletion."]),
        "recreated/scene05_deletion_investigated_access_not.png": ("The Pattern", ["The right to retrieve the data was treated as not worth investigating.", "The deletion of that same data, after it was gone, was treated as worth investigating."]),
        "recreated/scene06_identifiability_not_clarity.png": ("The Legal Test", ["Identifiability.", "Not clarity.", "The PDPA definition does not require a visible face or licence plate."]),
        "recreated/scene07_actual_reasons_not_tested.png": ("Actual Reasons Never Tested", ["The Scotts Tower: privacy, then no footage.", "Suites@Cairnhill: police-only access.", "Neither was tested against s.21(3) or the Fifth Schedule."]),
        "recreated/scene07_missing_dates.png": ("Dates That Disappeared", ["17 Apr verbal refusal.", "25 Apr written request.", "Both disappear from PDPC’s preservation analysis."]),
        "recreated/scene08_question_cluster_clarity.png": ("Nine Questions, Cluster 1", ["Which section authorises the clarity test?", "Why were the actual reasons never tested against the Fifth Schedule?"]),
        "recreated/scene08_question_authority.png": ("Question: Authority", ["Where in the PDPA is the clarity test found?", "Which section allows face-or-plate visibility to replace identifiability?"]),
        "recreated/scene08_question_cluster_timeline.png": ("Nine Questions, Cluster 2", ["Why did 17 Apr not matter?", "Why did 25 Apr not trigger preservation?", "Why did “many months” become 17 days?"]),
        "recreated/scene08_question_preservation.png": ("Question: Preservation", ["Why did a live access process not preserve the footage?", "Why did deletion before formal refusal defeat s.22A?"]),
        "recreated/scene08_question_reasonableness.png": ("Shifted Reasoning", ["personal data → reasonableness?", "A new gloss appeared without explaining the original reasoning gap."]),
        "recreated/scene08_repeated_one_line_response.png": ("One Repeated Response", ["“The Guidelines are not determinative; the PDPA takes precedence.”", "No guideline named. No PDPA section identified. No conflict explained."]),
        "recreated/scene08_no_guideline_named.png": ("What The Reply Did Not Say", ["Which guideline?", "Which clause?", "Which PDPA section?", "What conflict?"]),
        "recreated/scene08_publication_delay.png": ("Publication Delay", ["23 Jun 2025: “published on the microsite within the year”", "“unable to commit to a fixed date.”"]),
        "recreated/scene08_public_record_delay.png": ("Reasoning Not Promptly Public", ["The public could not see the reasoning.", "Questions on the reasoning were not answered on the merits."]),
        "recreated/scene08_closed_no_merits_answer.png": ("Closed Without Merits Answer", ["Questions on the reasoning were treated as closed rather than answered on the merits."]),
        "recreated/scene08_wrong_decision_similarity.png": ("Similarity To A Wrong Decision", ["TST was wrong.", "Saying Suites was similar to TST was not a reason at all."]),
        "recreated/scene09_imda_escalation.png": ("Escalation To IMDA", ["Complaint sent to IMDA Chief Executive, copied to PDPC Commissioner, with three IMDA branches included."]),
        "recreated/scene09_12_emails_11_months.png": ("12 Emails, 11 Months", ["Sept 2024 to Aug 2025.", "Sustained escalation before the final outcome."]),
        "recreated/scene09_complaint_leaked_back.png": ("Complaint Returned To Reviewed Body", ["During the review, complaint materials were leaked back to the PDPC officers under review."]),
        "recreated/scene09_no_wrongful_practices.png": ("IAU Finding", ["PDPC and its officers “did not commit any wrongful practices.”"]),
        "recreated/scene09_active_police_not_listed.png": ("Not A Listed Refusal Ground", ["“Active police investigation” is not listed in s.21(3) or the Fifth Schedule."]),
        "recreated/scene09_final_conclusive.png": ("Final And Conclusive", ["“acted in accordance with its protocols”", "“certain areas of improvement”", "“final and conclusive”"]),
        "recreated/scene10_filter_removed.png": ("Filter Removed", ["The public register no longer offered the obligation-type filter that would show the Access Obligation pattern directly."]),
        "recreated/scene10_zero_not_one.png": ("Zero", ["Access Obligation breach findings across 384 published enforcement actions.", "Not one."]),
        "recreated/scene10_two_cctv_cases.png": ("Only Two CCTV-Access Refusal Cases", ["Across the 384-case register, the only two CCTV-access-refusal complaints identified are both from this accident."]),
        "recreated/scene11_ordinary_vs_same_direction.png": ("Ordinary Failure vs Same Direction", ["Ordinary failure is uneven.", "This record points every decision in the same direction."]),
        "recreated/scene11_invented_reasoning_chain.png": ("Invented Reasoning Chain", ["MCST refusals → PDPC invented reasoning → IMDA endorsed outcome → one-line non-answers."]),
        "recreated/scene11_zero_breach_outcome.png": ("Outcome", ["384 published enforcement actions.", "Zero Access Obligation breach findings."]),
        "recreated/scene11_discretion_vs_denial.png": ("Discretion vs Denial", ["A regulator may choose how actively to enforce.", "It cannot actively deny a citizen’s right and reinterpret the law to justify that denial."]),
        "recreated/scene13_statutory_right_question.png": ("The Final Question", ["If a statutory right has never been enforced, not once, is it being enforced at all?", "And if not, by what mechanism, and by whom?"]),
    }
    for rel, (title, quotes) in cards.items():
        save_card(rel, title, [{"kind": "quote", "text": q} for q in quotes], subtitle="Recreated excerpt card", footer="Recreated from source correspondence or compiled record")

    save_simple_generated("generated/scene02_hospital_memory_gap.png", "Memory Gap", "Prompt: hospital bed, 05:06, quiet memory loss, no detailed face.", "hospital")
    save_simple_generated("generated/scene02_cairnhill_cctv_corridor.png", "Cairnhill Road CCTV Corridor", "Prompt: pre-dawn road flanked by condominiums, CCTV cameras, motorcycle helmet.", "road")
    save_simple_generated("generated/scene03_management_office_refusal.png", "Management Office Refusal", "Prompt: figure at tall management counter, no company name, no DPO, no escalation.", "office")
    save_simple_generated("generated/scene06_evidence_to_clarity_test.png", "Evidence Turned Into Clarity Test", "Prompt: handphone video fed into institutional machine labelled clarity test.", "machine")
    save_simple_generated("generated/scene13_citizen_evidence_wall.png", "Citizen Facing The Public Record", "Prompt: small figure before a wall of statute pages, decisions, and website screenshots.", "wall")

    missing = find_missing_visual_assets(VISUAL_SCHEDULE)
    if missing:
        raise SystemExit("Missing scheduled assets:\n" + "\n".join(missing))
    print(f"Generated supplemental assets. Scheduled visuals: {len(VISUAL_SCHEDULE)}")


if __name__ == "__main__":
    main()
