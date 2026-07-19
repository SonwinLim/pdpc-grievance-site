# Hero Video Repositioning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Embed the new 18-minute YouTube video (`aV-i5ts7zFo`) as the site's hero explainer in `#hook`, with a clickable 14-chapter list, plus pointer lines in `#summary` and `#verify`.

**Architecture:** Static HTML/CSS site, no build step. All markup edits in `index.html`; new styles appended to the hook block in `css/style.css`. Verification via puppeteer (installed at `../PDPC Rulings/Other Rulings/node_modules/`) and grep style audits.

**Tech Stack:** Plain HTML/CSS, GitHub Pages deploy on push to `main`.

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-19-hero-video-design.md` (approved).
- Curly quotes/apostrophes only in visible text; audits `grep -cE "[a-z]'[a-z]" index.html` and `grep -cE '[a-z]"[a-z]' index.html` must both return 0.
- No em-dashes anywhere in site text. The count `grep -c "—" index.html` must not increase.
- "the Complainant" voice rules do not apply here (hero is first-person testimony, which is allowed).
- Entry gate, old `#verify` embeds, and NotebookLM item must remain untouched.
- Working dir: `D:/Driving Legal Issue/pdpc-grievance-site`.

---

### Task 1: Hero video block (HTML + CSS)

**Files:**
- Modify: `index.html` (insert after the `</figure>` closing the `hook__diagram`, currently line 111, before the `hook__irony` paragraph)
- Modify: `css/style.css` (insert after line 199, the `@media (max-width: 600px)` hook rule)

**Interfaces:**
- Produces: classes `hook__video-block`, `hook__video-lead`, `hook__video-row`, `hook__video`, `hook__chapters`, `hook__chapter-time` used only within this task. Task 3's puppeteer check selects `#hook .video-frame iframe` and `#hook .hook__chapters a`.

- [ ] **Step 1: Insert the hero video HTML**

In `index.html`, immediately after the `</figure>` of `hook__diagram` (line 111), insert:

```html
        <div class="hook__video-block">
          <p class="hook__video-lead">
            The full account, from the accident to the questions now before Parliament, in one
            18-minute video. This video and this site were produced after PDPC revamped its
            enforcement decisions page without a filter by obligation, a change that removed the
            public’s ability to see the zero-breach pattern the video documents. Everything it
            states is sourced on this page below.
          </p>
          <div class="hook__video-row">
            <div class="hook__video">
              <div class="video-frame">
                <iframe
                  src="https://www.youtube-nocookie.com/embed/aV-i5ts7zFo"
                  title="Denied CCTV After Brain Injury: Why Zero PDPA Access Breach Findings on Record Despite Two Refusals?"
                  loading="lazy"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  referrerpolicy="strict-origin-when-cross-origin"
                  allowfullscreen></iframe>
              </div>
              <p class="meta"><a href="https://youtu.be/aV-i5ts7zFo" target="_blank" rel="noopener">Open on YouTube</a></p>
            </div>
            <nav class="hook__chapters" aria-label="Video chapters">
              <p class="hook__chapters-title">Chapters</p>
              <ol>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=0" target="_blank" rel="noopener"><span class="hook__chapter-time">0:00</span> Parliament’s assurance that requested data must be preserved</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=41" target="_blank" rel="noopener"><span class="hook__chapter-time">0:41</span> The accident, brain injury, and need for CCTV evidence</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=111" target="_blank" rel="noopener"><span class="hook__chapter-time">1:51</span> Two CCTV access requests and two refusals</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=227" target="_blank" rel="noopener"><span class="hook__chapter-time">3:47</span> The deletion window and section 22A preservation gap</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=292" target="_blank" rel="noopener"><span class="hook__chapter-time">4:52</span> Formal complaints filed with PDPC</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=413" target="_blank" rel="noopener"><span class="hook__chapter-time">6:53</span> PDPC’s “clarity” reasoning and the definition of personal data</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=518" target="_blank" rel="noopener"><span class="hook__chapter-time">8:38</span> The condominiums’ stated refusal grounds were not tested as stated</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=616" target="_blank" rel="noopener"><span class="hook__chapter-time">10:16</span> Nine legal questions across six PDPA provisions</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=768" target="_blank" rel="noopener"><span class="hook__chapter-time">12:48</span> Escalation to IMDA and the PDPC Commissioner</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=835" target="_blank" rel="noopener"><span class="hook__chapter-time">13:55</span> Reconstructing the enforcement filter by obligation</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=860" target="_blank" rel="noopener"><span class="hook__chapter-time">14:20</span> Zero adjudicated Access Obligation breach findings in the reconstructed index</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=946" target="_blank" rel="noopener"><span class="hook__chapter-time">15:46</span> Why ordinary regulatory error may not explain the pattern</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=1017" target="_blank" rel="noopener"><span class="hook__chapter-time">16:57</span> Source documents at pdpaaccessrights.sg</a></li>
                <li><a href="https://youtu.be/aV-i5ts7zFo?t=1065" target="_blank" rel="noopener"><span class="hook__chapter-time">17:45</span> Questions for Parliament</a></li>
              </ol>
            </nav>
          </div>
        </div>
```

Note: every apostrophe and quote in visible text above is already curly (`’`, `“ ”`). Do not retype them as straight.

- [ ] **Step 2: Add the CSS**

In `css/style.css`, after line 199 (`@media (max-width: 600px) { .hook__statement ... }`), insert:

```css
.hook__video-block { margin: var(--sp-4) auto var(--sp-5); max-width: 88rem; }
.hook__video-lead { font-size: var(--fs-md); max-width: var(--measure); margin: 0 0 var(--sp-3); }
.hook__video-row { display: grid; gap: var(--sp-3); }
.hook__chapters-title { font-weight: 600; margin: 0 0 0.5rem; }
.hook__chapters ol { list-style: none; margin: 0; padding: 0; }
.hook__chapters li + li { margin-top: 0.4rem; }
.hook__chapter-time { font-variant-numeric: tabular-nums; color: var(--accent); margin-right: 0.5em; }
@media (min-width: 820px) {
  .hook__video-row { grid-template-columns: 62fr 38fr; align-items: start; }
  .hook__chapters { max-height: 30rem; overflow-y: auto; padding-right: var(--sp-2); }
}
```

Before committing, confirm the variables used exist in `:root` of `css/style.css` (`--sp-2`, `--sp-3`, `--sp-4`, `--sp-5`, `--fs-md`, `--measure`, `--accent`); if a spacing var is missing, use the nearest existing one rather than inventing a new variable.

- [ ] **Step 3: Verify locally with puppeteer**

Save as `scratchpad/check-hero.js` (session scratchpad or repo `scratchpad/`), run with `node`:

```javascript
const path = require('path');
const puppeteer = require(path.resolve('../PDPC Rulings/Other Rulings/node_modules/puppeteer'));
(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve('index.html'));
  const src = await page.$eval('#hook .video-frame iframe', el => el.getAttribute('src'));
  const chapters = await page.$$eval('#hook .hook__chapters a', as => as.map(a => a.href));
  console.log('iframe src:', src);
  console.log('chapter count:', chapters.length);
  console.log('first/last:', chapters[0], chapters[chapters.length - 1]);
  await page.setViewport({ width: 1280, height: 900 });
  await page.screenshot({ path: 'scratchpad/hero-desktop.png' });
  await page.setViewport({ width: 400, height: 900 });
  await page.screenshot({ path: 'scratchpad/hero-mobile.png' });
  await browser.close();
})();
```

Expected: `iframe src: https://www.youtube-nocookie.com/embed/aV-i5ts7zFo`, `chapter count: 14`, first link ends `?t=0`, last ends `?t=1065`. Inspect both screenshots: two-column at 1280px, stacked at 400px, no overflow.

- [ ] **Step 4: Run style audits**

```bash
grep -cE "[a-z]'[a-z]" index.html
grep -cE '[a-z]"[a-z]' index.html
grep -c "—" index.html
```

Expected: first two return `0`; em-dash count equals the pre-change count (record it before editing).

- [ ] **Step 5: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: hero video embed with 14-chapter list in #hook (aV-i5ts7zFo)"
```

---

### Task 2: Pointer lines in #summary and #verify

**Files:**
- Modify: `index.html` `#summary` lede area (currently lines 133–139) and `#verify` intro (currently lines 1545–1548)

**Interfaces:**
- Consumes: `#hook` anchor from Task 1.
- Produces: nothing downstream.

- [ ] **Step 1: Add the #summary pointer**

Immediately after the closing `</p>` of the `lede` paragraph in `#summary` (the one ending "found no breach of the Access Obligation."), insert:

```html
        <p class="meta">
          If you prefer to watch rather than read, <a href="#hook">the video above</a> covers
          the full account; each section below documents the sources behind it.
        </p>
```

- [ ] **Step 2: Add the #verify pointer**

In `#verify`, immediately after the intro paragraph ("A six-minute overview, and the full underlying research notebook, both public.") and before `<div class="verify-grid grid grid--3">`, insert:

```html
        <p class="meta">
          The current full account is the 18-minute video at the top of this page. The items
          below are earlier summaries, kept as part of the record.
        </p>
```

- [ ] **Step 3: Re-run style audits**

```bash
grep -cE "[a-z]'[a-z]" index.html
grep -cE '[a-z]"[a-z]' index.html
```

Expected: both `0`.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: pointer lines to hero video in #summary and #verify"
```

---

### Task 3: Deploy and verify live

**Files:** none (git push + live check only)

**Interfaces:**
- Consumes: commits from Tasks 1–2.

- [ ] **Step 1: Push**

```bash
git push
```

- [ ] **Step 2: Wait for GitHub Pages deploy, then check the live page**

Wait for the Actions run to finish (`gh run watch` or ~2 minutes), then:

```bash
curl -s https://pdpaaccessrights.sg/ | grep -c "aV-i5ts7zFo"
```

Expected: `16` (1 iframe src + 1 "Open on YouTube" + 14 chapter links). Any non-zero value confirms deploy; if `0`, the deploy has not landed yet or failed — check `gh run list --limit 3`.

- [ ] **Step 3: Report**

Confirm to Ray: hero video live, chapter links working, old #verify embeds untouched.
