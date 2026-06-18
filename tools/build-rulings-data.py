#!/usr/bin/env python3
"""
Build data/rulings.json for the PDPC enforcement index page.

Reads the public enforcement-decisions catalogue (CSV + downloaded PDFs, both kept
OUTSIDE this repo) and produces a structured JSON the static page renders.

Method (deliberately conservative, to withstand hostile scrutiny):
  * The DECISION TITLE is PDPC's authoritative statement of the obligation(s) at
    issue, so obligations for Commission's Decisions are parsed from the title.
  * Voluntary Undertakings rarely name an obligation in the title, so their
    obligations are derived from the PDF body (explicit "<X> Obligation" / section
    references tied to a breach), and flagged confidence="review" when uncertain.
  * Raw body keyword frequency is NOT used to assign obligations — bodies mention
    other obligations in passing (e.g. an Accountability decision cites "Protection"
    repeatedly in context). Frequency would mislabel cases.
  * Separately, EVERY body is scanned for any *access-obligation breach* assertion
    (section 21 tied to a breach). This is the evidence behind the headline claim
    that the Access Obligation has zero breach findings; any hit is reported.

The raw PDFs are never copied into the repo. Each row links to PDPC's own detail page.

Usage:
    python3 tools/build-rulings-data.py "/path/to/PDPC Rulings/Other Rulings"
"""
import csv
import json
import re
import sys
from pathlib import Path

import pypdf

# --- Canonical obligations (PDPA Parts III–VI + DNC) -------------------------
# Order = display order. Each: canonical name -> (section label, title aliases).
OBLIGATIONS = [
    ("Consent",             "s13–17",  ["consent"]),
    ("Purpose Limitation",  "s18",     ["purpose limitation", "purpose"]),
    ("Notification",        "s20",     ["notification", "notify"]),
    ("Access",              "s21",     ["access"]),
    ("Correction",          "s22",     ["correction"]),
    ("Accuracy",            "s23",     ["accuracy"]),
    ("Protection",          "s24",     ["protection"]),
    ("Retention Limitation","s25",     ["retention limitation", "retention"]),
    ("Transfer Limitation", "s26",     ["transfer limitation", "transfer"]),
    ("Accountability",      "s11–12",  ["accountability"]),
    ("Openness",            "s11–12",  ["openness"]),
    ("Do Not Call",         "Part IX", ["do not call", "dnc"]),
    ("Data Protection",     "Parts III–VI", ["data protection"]),  # generic
]
ALIAS_TO_CANON = []  # (alias, canon) longest-first for greedy match
for canon, _sec, aliases in OBLIGATIONS:
    for a in aliases:
        ALIAS_TO_CANON.append((a, canon))
ALIAS_TO_CANON.sort(key=lambda x: -len(x[0]))


def parse_title(title):
    """Return (breach_finding, obligations[], obligation_block_found)."""
    t = title.strip()
    low = t.lower()

    if low.startswith("no breach"):
        finding = "no breach"
    elif "outcome of a review" in low or low.startswith("outcome of"):
        finding = "review"
    elif "undertaking" in low and "breach of" not in low:
        finding = "undertaking"
    elif "breach of" in low:
        finding = "breach"
    else:
        finding = "other"

    # Do Not Call titles don't use the "X Obligation" form.
    if re.search(r"do[\s-]?not[\s-]?call|\bdnc\b", low):
        return finding, ["Do Not Call"], True
    # Part 9A offences (e.g. s48B dictionary attacks, s48C/D unauthorised use/
    # disclosure) are offences, not breaches of a data-protection obligation.
    if re.search(r"section\s*48[a-z]|dictionary attack|egregious", low):
        return finding, ["Other PDPA offence"], True

    # Obligation block: "...Breach of (the) X (and Y) Obligation(s) by..."
    m = re.search(r"breach of (?:the\s+)?(.+?)\s+obligations?\b", low)
    obls, block = [], False
    if m:
        block = True
        seg = m.group(1)
        seg = seg.replace(" and other", " and").replace("other ", "")
        # split on connectors
        for part in re.split(r"\s+and\s+|\s*&\s*|\s*,\s*", seg):
            part = part.strip(" .")
            if not part:
                continue
            for alias, canon in ALIAS_TO_CANON:
                if alias in part:
                    if canon not in obls:
                        obls.append(canon)
                    break
    return finding, obls, block


# Body patterns: an access-obligation BREACH assertion (the headline claim).
ACCESS_BREACH_PATTERNS = [
    re.compile(r"breach(?:ed|es)?[^.\n]{0,90}section\s*21\b", re.I),
    re.compile(r"section\s*21\b[^.\n]{0,90}breach(?:ed|es)?", re.I),
    re.compile(r"breach(?:ed|es)?[^.\n]{0,90}access obligation", re.I),
    re.compile(r"access obligation[^.\n]{0,90}breach(?:ed|es)?", re.I),
    re.compile(r"(?:contraven|fail[a-z]*|did not comply)[^.\n]{0,90}section\s*21\b", re.I),
]

# Body obligation cues for undertakings (explicit obligation phrase or section).
SECTION_TO_CANON = {
    "13": "Consent", "14": "Consent", "15": "Consent", "16": "Consent", "17": "Consent",
    "18": "Purpose Limitation", "20": "Notification", "21": "Access", "22": "Correction",
    "23": "Accuracy", "24": "Protection", "25": "Retention Limitation",
    "26": "Transfer Limitation", "11": "Accountability", "12": "Openness",
}
BREACH_SECTION_RE = re.compile(
    r"(?:breach|contraven|fail[a-z]*|did not comply|not compl|obligation)[^.\n]{0,120}section\s*(\d{1,2})[A-Z]?",
    re.I,
)
OBLIGATION_PHRASE_RE = re.compile(
    r"\b(consent|purpose limitation|notification|access|correction|accuracy|protection|"
    r"retention(?: limitation)?|transfer(?: limitation)?|accountability|openness)\s+obligation",
    re.I,
)

PUBLISHED_RE = re.compile(r"Published on\s+\d{1,2}\s+[A-Za-z]+\s+(20\d{2})")
CITATION_YEAR_RE = re.compile(r"\[(20\d{2})\]\s*SGPDPC", re.I)
DATE_RE = re.compile(
    r"\b(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+(20\d{2})\b"
)
UNDERTAKING_DATE_RE = re.compile(
    r"day of\s+(January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+(20\d{2})", re.I)


def extract_text(pdf_path):
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception as e:  # noqa: BLE001 — surface, don't hide
        print(f"   ! could not read {pdf_path.name}: {e}", file=sys.stderr)
        return ""


def body_obligations(text):
    found = []
    for canon in OBLIGATION_PHRASE_RE.findall(text):
        c = canon.strip().title()
        c = {"Retention": "Retention Limitation", "Transfer": "Transfer Limitation"}.get(c, c)
        if c not in found:
            found.append(c)
    for sec in BREACH_SECTION_RE.findall(text):
        c = SECTION_TO_CANON.get(sec)
        if c and c not in found:
            found.append(c)
    return found


def extract_year(text, finding):
    # "Published on <date>" is the most reliable signal on saved detail pages.
    m = PUBLISHED_RE.search(text)
    if m:
        return int(m.group(1))
    if finding == "undertaking":
        m = UNDERTAKING_DATE_RE.search(text)
        if m:
            return int(m.group(2))
    m = CITATION_YEAR_RE.search(text)
    if m:
        return int(m.group(1))
    # Fallback: latest plausible date year in the document.
    years = [int(y) for _d, _mo, y in DATE_RE.findall(text)]
    return max(years) if years else None


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: build-rulings-data.py <path-to 'Other Rulings' folder>")
    src = Path(sys.argv[1])
    csv_path = src / "pdpc_rulings.csv"
    pdf_dir = src / "PDFs"
    out_path = Path(__file__).resolve().parent.parent / "data" / "rulings.json"

    rows = list(csv.DictReader(open(csv_path, newline="")))
    print(f"Loaded {len(rows)} catalogue rows from {csv_path.name}")

    records, review, access_breach_hits, missing_pdf, missing_year = [], [], [], [], []

    for r in rows:
        title = r["Title"].strip()
        ctype = r["Type"].strip()
        detail_url = r["Detail Page URL"].strip()
        local = (r.get("Local PDF(s)") or "").split(";")[0].strip()

        finding, title_obls, block = parse_title(title)

        text = ""
        pdf_path = pdf_dir / local if local else None
        if pdf_path and pdf_path.exists():
            text = extract_text(pdf_path)
        elif local:
            missing_pdf.append(title)

        # Assign obligations. Decisions: title is authoritative. Undertakings:
        # PDPC makes no breach finding, so only tag obligations the body states
        # explicitly; otherwise "Not adjudicated".
        obls = list(title_obls)
        conf = "title" if obls else "review"
        if not obls and text:
            obls = body_obligations(text)
            conf = "body" if obls else "review"
        if "Data Protection" in obls and len(obls) > 1:
            obls = [o for o in obls if o != "Data Protection"]

        is_data_breach = bool(text) and bool(re.search(r"data breach", text, re.I))
        if not obls:
            obls = ["Not adjudicated"] if finding == "undertaking" else ["Unspecified"]

        # Headline scan: any access-obligation *breach* assertion in this body?
        access_breach = bool(text) and any(p.search(text) for p in ACCESS_BREACH_PATTERNS)
        if access_breach and finding == "breach":
            access_breach_hits.append(title)
            conf = "review"

        year = extract_year(text, finding) if text else None
        if year is None:
            missing_year.append(title)

        rec = {
            "title": title,
            "type": ctype,
            "obligations": obls,
            "finding": finding,
            "year": year,
            "detailUrl": detail_url,
            "confidence": conf,
            "dataBreachIncident": is_data_breach,
            "accessMentioned": "Access" in obls or access_breach,
        }
        records.append(rec)
        # Flag for manual review only where it matters: a Decision we could not
        # categorise, or any access mention. Undertakings with no stated
        # obligation are expected ("Not adjudicated"), not errors.
        if (conf == "review" and finding != "undertaking") or rec["accessMentioned"]:
            review.append(rec)

    records.sort(key=lambda x: (x["year"] or 0), reverse=True)
    out_path.parent.mkdir(exist_ok=True)
    payload = {
        "generated": "build-rulings-data.py",
        "source": "https://www.pdpc.gov.sg/organisations/regulations-decisions/enforcement-decisions",
        "count": len(records),
        "records": records,
    }
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

    # ---- Build report -------------------------------------------------------
    print(f"\nWrote {out_path} ({len(records)} records)")
    from collections import Counter
    by_ob_breach = Counter()
    for rec in records:
        if rec["finding"] == "breach":
            for o in rec["obligations"]:
                by_ob_breach[o] += 1
    print("\nBreach findings by obligation (Commission's Decisions + undertakings):")
    for canon, _s, _a in OBLIGATIONS:
        print(f"   {by_ob_breach.get(canon, 0):4d}  {canon}")
    print(f"   {by_ob_breach.get('Unspecified', 0):4d}  Unspecified")

    access_records = [r for r in records if "Access" in r["obligations"]]
    print(f"\nAccess Obligation cases ({len(access_records)}):")
    for rec in access_records:
        print(f"   [{rec['finding']:>10}] {rec['year']}  {rec['title']}")

    print(f"\n*** Access-obligation BREACH findings: {len(access_breach_hits)} ***")
    for t in access_breach_hits:
        print(f"   ! {t}")

    print(f"\nRows flagged confidence='review': {len(review)}")
    for rec in review[:60]:
        print(f"   - [{rec['finding']}] {rec['title']}  -> {rec['obligations']}")
    if len(review) > 60:
        print(f"   ... and {len(review) - 60} more")
    if missing_pdf:
        print(f"\nMissing local PDF for {len(missing_pdf)} rows (first 10): {missing_pdf[:10]}")
    print(f"Rows with no extractable year: {len(missing_year)}")
    for t in missing_year:
        print(f"   ? {t}")


if __name__ == "__main__":
    main()
