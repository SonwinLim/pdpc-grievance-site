# PDPC / PDPA Grievance Site

A static website presenting documented grievances with Singapore's Personal Data Protection
Commission (PDPC) and IMDA over the handling of CCTV access requests under the Personal Data
Protection Act (PDPA).

**Audiences:** Members of Parliament (primary), the Singapore public (primary), and the
legal / data-protection community (secondary).

## Structure

Single-page site plus a set of recreated source pages:

- `index.html` — the main page
- `enforcement-index.html` — every case in PDPC's public enforcement register, filterable by obligation (the filter PDPC removed)
- `data/rulings.json` — generated dataset backing the enforcement index (384 records)
- `tools/build-rulings-data.py` — one-off script that regenerates `data/rulings.json` from the public catalogue
- `css/style.css` — styles
- `js/main.js` — collapsibles, smooth scroll, scrollspy
- `js/enforcement-index.js` — loads `data/rulings.json`, renders bars and the filterable register
- `evidence/` — the author's own documents, recreated as readable web pages

Official documents (the PDPA, PDPC advisory guidelines, and the two PDPC decisions) are linked
to their authoritative pages on the AGC and PDPC websites rather than reproduced here. The
enforcement index likewise links every row to PDPC's own detail page — no documents are re-hosted.

## Rebuilding the enforcement dataset

The enforcement index is backed by `data/rulings.json`, generated from the public PDPC catalogue.
The source catalogue and downloaded PDFs live outside this repo (in
`PDPC Rulings/Other Rulings/`). To regenerate the dataset:

```
python3 tools/build-rulings-data.py "/path/to/PDPC Rulings/Other Rulings"
```

The script writes `data/rulings.json` and prints a build report covering:

- Counts of breach findings per obligation (Decisions + undertakings)
- Every case tagged with the Access Obligation
- The headline scan: any access-obligation breach assertion anywhere in the register
  (expected: **0**)
- Rows flagged for manual review (typically zero for the Decisions; Undertakings are
  categorised as "Not adjudicated" because PDPC makes no breach finding on them)

The report's "review" rows are the only ones a reader should manually confirm.

## Running locally

No build step. Serve the folder with any static server:

```
python3 -m http.server 8000
# then open http://localhost:8000/
```

## Hosting

Plain HTML / CSS / JS — no backend, no build step. Hostable on any static host (GitHub Pages,
Netlify, Cloudflare Pages). Responsive, and prints cleanly to PDF.

## A note on the evidence pages

The pages under `evidence/` are anonymized recreations of the author's own correspondence and
submissions: the emails, the letter to Parliament, and the three correspondence/record excerpts
are reproduced verbatim; the longer documents are presented as structured summaries with key
verbatim quotes. Personal identifying details have been removed.
