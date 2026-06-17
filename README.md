# PDPC / PDPA Grievance Site

A static website presenting documented grievances with Singapore's Personal Data Protection
Commission (PDPC) and IMDA over the handling of CCTV access requests under the Personal Data
Protection Act (PDPA).

**Audiences:** Members of Parliament (primary), the Singapore public (primary), and the
legal / data-protection community (secondary).

## Structure

Single-page site plus a set of recreated source pages:

- `index.html` — the main page
- `css/style.css` — styles
- `js/main.js` — collapsibles, smooth scroll, scrollspy
- `evidence/` — the author's own documents, recreated as readable web pages

Official documents (the PDPA, PDPC advisory guidelines, and the two PDPC decisions) are linked
to their authoritative pages on the AGC and PDPC websites rather than reproduced here.

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
