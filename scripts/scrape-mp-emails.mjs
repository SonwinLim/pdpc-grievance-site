#!/usr/bin/env node
/**
 * scrape-mp-emails.mjs — Collect contact info for every current Singapore
 * Member of Parliament and Cabinet Minister.
 *
 * Sources (verified static HTML, no JS client needed):
 *   - https://www.parliament.gov.sg/mps/list-of-current-mps
 *       Single page lists all 108 MPs. The page server-renders 108 JSON
 *       records (one per MP) inline as part of the Next.js RSC stream. Each
 *       record includes: slug, full_name, designation (ministerial role for
 *       Cabinet), party_affliation, constituency, social links, etc.
 *   - https://www.parliament.gov.sg/mps/list-of-current-mps/mp/details/{slug}
 *       Each bio page contains a <a href="mailto:..."> in the
 *       "Meet the People Session" accordion — the MP's personal/constituency
 *       contact email (may be @gmail.com or a constituency-domain email).
 *   - https://www.sgdi.gov.sg/organs-of-state/parl
 *       Singapore Government Directory. Single page lists ~109 MPs/secretariat
 *       with their contact emails (often ministry-domain for Cabinet, e.g.
 *       david_neo@mccy.gov.sg). Used as FALLBACK for MPs whose Parliament
 *       bio had no email; primary source for newer MPs whose Parliament page
 *       is not yet populated.
 *
 * Outputs (in data/):
 *   - mp-contact-list.csv    (mail-merge ready)
 *   - mp-contact-list.json   (programmatic)
 *   - mp-contact-list.md     (human-readable table)
 *   - scrape-log.txt         (per-fetch log with timestamps)
 *   - missing-emails.txt     (MPs still missing after sgdi fallback)
 *
 * Usage:
 *   node scripts/scrape-mp-emails.mjs
 *
 * No dependencies. Uses Node 18+ built-in fetch.
 * Runtime: ~1 minute (108 bio fetches fast, plus 1 sgdi fetch).
 */

import fs from 'node:fs';
import path from 'node:path';

// Run from project root: `node scripts/scrape-mp-emails.mjs`
const DATA = path.join(process.cwd(), 'data');

const LIST_URL = 'https://www.parliament.gov.sg/mps/list-of-current-mps';
const BIO_URL_BASE =
  'https://www.parliament.gov.sg/mps/list-of-current-mps/mp/details';
const SGDI_URL = 'https://www.sgdi.gov.sg/organs-of-state/parl';
const UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
const DELAY_MS = 1500;
const RETRY_DELAY_MS = 3000;

// --- Logging -----------------------------------------------------------------

const logPath = path.join(DATA, 'scrape-log.txt');
function log(line) {
  const ts = new Date().toISOString();
  const out = `[${ts}] ${line}`;
  console.log(out);
  fs.appendFileSync(logPath, out + '\n', 'utf8');
}

// --- HTTP --------------------------------------------------------------------

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function fetchWithRetry(url) {
  for (let attempt = 1; attempt <= 2; attempt++) {
    try {
      const res = await fetch(url, {
        headers: {
          'User-Agent': UA,
          Accept: 'text/html,application/xhtml+xml',
          'Accept-Language': 'en-SG,en;q=0.9',
        },
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.text();
    } catch (err) {
      log(
        `fetch FAIL attempt ${attempt} ${url}: ${err.message}`,
      );
      if (attempt < 2) await sleep(RETRY_DELAY_MS);
      else throw err;
    }
  }
}

// --- Step 1: fetch MP list and parse 108 records ----------------------------

async function fetchMpList() {
  log(`Fetching list: ${LIST_URL}`);
  const html = await fetchWithRetry(LIST_URL);
  // Unescape Next.js's RSC double-escaped quotes (\" → ")
  const unescaped = html.replace(/\\"/g, '"');
  // Walk every 'party_affliation' occurrence back to its containing '{...}'.
  // The records are JSON objects with curly-quoted values (’) intact.
  const records = [];
  let searchFrom = 0;
  while (true) {
    const idx = unescaped.indexOf('party_affliation', searchFrom);
    if (idx === -1) break;

    // Walk back to the opening '{' at depth 0.
    let depth = 0;
    let start = idx;
    while (start > 0) {
      if (unescaped[start] === '}') depth++;
      else if (unescaped[start] === '{') {
        if (depth === 0) break;
        depth--;
      }
      start--;
    }
    // Walk forward to the matching '}' at depth 0.
    depth = 0;
    let end = idx;
    while (end < unescaped.length) {
      if (unescaped[end] === '{') depth++;
      else if (unescaped[end] === '}') {
        if (depth === 0) {
          end++;
          break;
        }
        depth--;
      }
      end++;
    }

    try {
      const obj = JSON.parse(unescaped.slice(start, end));
      if (obj && obj.url && obj.full_name) records.push(obj);
    } catch (err) {
      log(`  parse FAIL at offset ${start}: ${err.message.slice(0, 120)}`);
    }
    searchFrom = end;
  }
  return records;
}

// --- Step 2: fetch each bio page and extract mailto links -------------------

async function fetchEmails(slug) {
  const url = `${BIO_URL_BASE}/${slug}`;
  const html = await fetchWithRetry(url);
  // Find all mailto: links; primary email is the first one.
  const re = /mailto:([A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,})/g;
  const found = [];
  for (const m of html.matchAll(re)) found.push(m[1]);
  if (found.length === 0) return { email: null, additional: [] };
  // Dedupe while preserving order.
  const seen = new Set();
  const unique = [];
  for (const e of found) {
    if (!seen.has(e)) {
      seen.add(e);
      unique.push(e);
    }
  }
  return { email: unique[0], additional: unique.slice(1) };
}

// --- Step 3: build rows -----------------------------------------------------

function buildRows(records, emailMap) {
  return records.map((r) => {
    const slug = r.url;
    const { email, additional, source } = emailMap[slug] || {};
    // Normalise party: "People's Action Party" (both ’ and ') collapse to
    // straight ASCII apostrophe for spreadsheet compatibility.
    const partyRaw = r.party_affliation || 'Nominated Member of Parliament';
    const party = partyRaw.replace(/[’‘]/g, "'");
    return {
      name: r.full_name,
      slug,
      role: r.designation || '',
      constituency: (r.constituency && r.constituency.constituency) || '',
      party,
      email: email || '',
      additionalEmails: (additional || []).join('; '),
      sourceUrl: `${BIO_URL_BASE}/${slug}`,
      emailSource: source || '',
    };
  });
}

// --- Step 2b: sgdi fallback -------------------------------------------------

// Strip honorifics + punctuation, lowercase, return sorted unique tokens.
// Two equivalent names ("Andre Low Wu Yang" vs "LOW Wu Yang Andre") collapse
// to the same token set.
function nameTokens(name) {
  const cleaned = name
    .replace(/\b(Dr|Mr|Mrs|Ms|Assoc Prof Dr|Prof Dr|Professor|Prof|Asst Prof|Assistant Professor)\b\.?/gi, '')
    .replace(/[^a-zA-Z\s]/g, ' ')
    .trim()
    .toLowerCase();
  return [...new Set(cleaned.split(/\s+/).filter(Boolean))].sort();
}

// Subset match: all tokens of the shorter name appear in the longer.
// Catches "Kenneth Tiong" matching "Kenneth TIONG Boon Kiat".
// Requires ≥2 tokens on the smaller side to avoid single-name false positives.
function namesMatch(a, b) {
  const ta = nameTokens(a);
  const tb = nameTokens(b);
  if (ta.length < 2 || tb.length < 2) return false;
  const shorter = ta.length <= tb.length ? ta : tb;
  const longer = ta.length <= tb.length ? new Set(tb) : new Set(ta);
  return shorter.every((t) => longer.has(t));
}

async function fetchSgdi() {
  log(`Fetching sgdi fallback: ${SGDI_URL}`);
  const html = await fetchWithRetry(SGDI_URL);
  const liMatches = html.match(/<li id="[^"]+">[\s\S]*?<\/li>/g) || [];
  const mpLi = liMatches.filter((li) => /class="name"/.test(li));
  const records = [];
  for (const li of mpLi) {
    const nameMatch = li.match(/<div class="name"[^>]*>([\s\S]{0,300}?)<\/div>/);
    if (!nameMatch) continue;
    const name = nameMatch[1].replace(/<[^>]+>/g, '').trim();
    const emailMatch = li.match(/color:#d11212">([^<]+)<\/span>/);
    const emails = emailMatch
      ? emailMatch[1].split(',').map((e) => e.trim()).filter(Boolean)
      : [];
    records.push({ name, emails });
  }
  return records;
}

function findSgdiMatch(parliamentName, sgdiRecords) {
  return sgdiRecords.find((r) => namesMatch(parliamentName, r.name)) || null;
}

// --- Step 4: write outputs ---------------------------------------------------

function csvEscape(v) {
  const s = v == null ? '' : String(v);
  return `"${s.replace(/"/g, '""')}"`;
}

function writeCsv(rows) {
  const columnMap = [
    ['name', 'name'],
    ['slug', 'slug'],
    ['role', 'role'],
    ['constituency', 'constituency'],
    ['party', 'party'],
    ['email', 'email'],
    ['email_source', 'emailSource'],
    ['additional_emails', 'additionalEmails'],
    ['source_url', 'sourceUrl'],
  ];
  const lines = [columnMap.map((c) => c[0]).join(',')];
  for (const r of rows) lines.push(columnMap.map((c) => csvEscape(r[c[1]])).join(','));
  fs.writeFileSync(path.join(DATA, 'mp-contact-list.csv'), lines.join('\n') + '\n', 'utf8');
}

function writeJson(rows) {
  fs.writeFileSync(
    path.join(DATA, 'mp-contact-list.json'),
    JSON.stringify(rows, null, 2) + '\n',
    'utf8',
  );
}

function writeMarkdown(rows) {
  const lines = [];
  lines.push('# Singapore MPs & Cabinet Ministers — Contact List');
  lines.push('');
  lines.push(`Generated: ${new Date().toISOString()}`);
  lines.push(`Total entries: ${rows.length}`);
  const withEmail = rows.filter((r) => r.email).length;
  const fromParliament = rows.filter((r) => r.emailSource === 'parliament').length;
  const fromSgdi = rows.filter((r) => r.emailSource === 'sgdi').length;
  lines.push(`With email: ${withEmail} (${Math.round((withEmail / rows.length) * 100)}%) — parliament: ${fromParliament}, sgdi fallback: ${fromSgdi}`);
  lines.push('');
  lines.push('Sources:');
  lines.push('- https://www.parliament.gov.sg/mps/list-of-current-mps');
  lines.push('- https://www.sgdi.gov.sg/organs-of-state/parl');
  lines.push('');
  lines.push('| Name | Role | Party | Constituency | Email | Source |');
  lines.push('|------|------|-------|--------------|-------|--------|');
  for (const r of rows) {
    lines.push(
      `| ${r.name.replace(/\|/g, '\\|')} | ${r.role.replace(/\|/g, '\\|')} | ${r.party} | ${r.constituency} | ${r.email || '_(none)_'} | ${r.emailSource || ''} |`,
    );
  }
  fs.writeFileSync(path.join(DATA, 'mp-contact-list.md'), lines.join('\n') + '\n', 'utf8');
}

function writeMissing(missing) {
  if (missing.length === 0) {
    fs.writeFileSync(path.join(DATA, 'missing-emails.txt'), '', 'utf8');
    return;
  }
  const lines = ['slug\tname\tsource_url\terror'];
  for (const m of missing) {
    lines.push(
      [m.slug, m.name, m.sourceUrl, m.error || ''].join('\t'),
    );
  }
  fs.writeFileSync(path.join(DATA, 'missing-emails.txt'), lines.join('\n') + '\n', 'utf8');
}

// --- Main --------------------------------------------------------------------

async function main() {
  fs.mkdirSync(DATA, { recursive: true });
  fs.writeFileSync(
    logPath,
    `[${new Date().toISOString()}] === scrape started ===\n`,
    'utf8',
  );

  // 1. List page
  const records = await fetchMpList();
  log(`Found ${records.length} MP records on list page`);
  if (records.length === 0) {
    log('FATAL: no records parsed; aborting');
    process.exit(2);
  }

  // 2. Bio pages
  const emailMap = {};
  const missing = [];
  for (let i = 0; i < records.length; i++) {
    const r = records[i];
    const tag = `[${i + 1}/${records.length}]`;
    log(`${tag} ${r.full_name} (${r.url})`);
    try {
      const { email, additional } = await fetchEmails(r.url);
      emailMap[r.url] = { email, additional, source: email ? 'parliament' : '' };
      if (!email) {
        log(`  no parliament email; will try sgdi`);
        missing.push({ slug: r.url, name: r.full_name, sourceUrl: `${BIO_URL_BASE}/${r.url}` });
      } else if (additional.length) {
        log(`  ${email} (+${additional.length} additional)`);
      } else {
        log(`  ${email}`);
      }
    } catch (err) {
      log(`  ERROR: ${err.message}`);
      emailMap[r.url] = { email: null, additional: [], source: '' };
      missing.push({
        slug: r.url,
        name: r.full_name,
        sourceUrl: `${BIO_URL_BASE}/${r.url}`,
        error: err.message,
      });
    }
    if (i < records.length - 1) await sleep(DELAY_MS);
  }

  // 2b. sgdi fallback for any MP still missing an email
  let sgdiRecords = [];
  try {
    sgdiRecords = await fetchSgdi();
    log(`sgdi: ${sgdiRecords.length} records (incl. secretariat)`);
    let filled = 0;
    for (const r of records) {
      if (emailMap[r.url].email) continue;
      const match = findSgdiMatch(r.full_name, sgdiRecords);
      if (match && match.emails.length > 0) {
        emailMap[r.url] = {
          email: match.emails[0],
          additional: match.emails.slice(1),
          source: 'sgdi',
        };
        log(`  ${r.full_name}: filled from sgdi → ${match.emails[0]}`);
        filled++;
        const idx = missing.findIndex((m) => m.slug === r.url);
        if (idx >= 0) missing.splice(idx, 1);
      }
    }
    log(`Filled ${filled} missing emails from sgdi`);
  } catch (err) {
    log(`sgdi fallback FAILED: ${err.message}`);
  }

  // 3. Build rows
  const rows = buildRows(records, emailMap);

  // 4. Write outputs
  log('Writing outputs...');
  writeCsv(rows);
  writeJson(rows);
  writeMarkdown(rows);
  writeMissing(missing);

  // 5. Summary
  const withEmail = rows.filter((r) => r.email).length;
  const withGmail = rows.filter((r) => /@gmail\.com$/i.test(r.email)).length;
  const fromParliament = rows.filter((r) => r.emailSource === 'parliament').length;
  const fromSgdi = rows.filter((r) => r.emailSource === 'sgdi').length;
  const cabinet = rows.filter((r) => /(Minister|Speaker|Deputy Speaker|Mayor)/i.test(r.role)).length;
  log(`=== Done ===`);
  log(`Total: ${rows.length} | Emails: ${withEmail} (parliament: ${fromParliament}, sgdi: ${fromSgdi}) | @gmail: ${withGmail} | Cabinet/Mayor/Speaker: ${cabinet} | Missing: ${missing.length}`);
  log(`Outputs: data/mp-contact-list.{csv,json,md}`);
  log(`Log: data/scrape-log.txt`);
  log(`Missing list: data/missing-emails.txt`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});