# Final Review — PDPC Grievance Site

**Date:** 2026-06-21
**Reviewers:** Three parallel agents across MP/journalist, public, and lawyer/DPO lenses
**Scope:** index.html (15 sections), 8 evidence subpages, enforcement-index.html

---

## RED: Must Fix Now (credibility-threatening or factually wrong)

### 1. Arithmetic error: "17 days after the access request" (should be 13)

- **Where:** `#why` lines 421 and 267
- **Text:** "My CCTV footage was deleted on 30 April 2024, 17 days after I made my access request"
- **Problem:** First verbal access request was 17 April 2024. 17 Apr to 30 Apr = 13 days, not 17. The 17-day figure matches the accident date (13 April), not the request date. Any reader doing basic arithmetic catches this.
- **Fix:** "13 days after my first verbal access request" or "17 days after the accident"

### 2. Internal contradiction: investigation start date

- **Where:** `#why` line 267 vs `#narrative` line 614
- **Text A:** "5 days before PDPC began investigating" (implies investigation started ~5 May 2024)
- **Text B:** "PDPC only began investigating in August 2024, about four months after the 4 May 2024 complaint"
- **Problem:** These two statements cannot both be true. PDPC either started investigating in early May or in August. This is the single most damaging inconsistency on the site — a hostile reader would present both quotes side by side.
- **Fix:** Determine correct date. PDPC acknowledged the complaint in May (computer-generated acknowledgment) but opened substantive investigation in August. Say: "PDPC acknowledged the complaint in early May but did not open a substantive investigation until August 2024."

### 3. "Five" vs "Six" challenges in narrative section header

- **Where:** `#narrative` line 600
- **Text:** "Five documented challenges, presented claim by claim"
- **Problem:** There are six numbered contrasts (1 through 6). The header says five.
- **Fix:** Change "Five" to "Six".

### 4. "Seven" vs "Ten" contradictions in source citations page

- **Where:** `evidence/contradictions-source-citations.html` lines 6, 33, 35, 37
- **Text:** `<title>`, `<meta>`, `<h1>`, and nav breadcrumb all say "Seven Contradictions"
- **Problem:** The main page says "Ten Contradictions" and the page has 10 sections. The source page title was never updated.
- **Fix:** Change all "Seven" to "Ten" in that file.

### 5. s.4(6) "required" vs "could provide" — mischaracterises PDPC precedent

- **Where:** `#narrative` line 699
- **Text:** "PDPC concluded in MCST 4436 that s.4(6) PDPA required the footage to be provided"
- **Problem:** The actual MCST 4436 decision says the organisation "can provide inspection" — permitted, not compelled. The distinction between permission and obligation is legally significant. PDPC's lawyers would immediately point this out. Note: contradiction card #8 already correctly says "could provide" — so this is also an internal inconsistency within the same page.
- **Fix:** "could provide the footage" or "was permitted to provide inspection"

---

## AMBER: Should Fix (weakens credibility or persuasion)

### 6. #why subsection 4: "Street View of the building is gone too"

- **Problem:** Purely speculative. "The cause is unknown. It may have been incidental." This is the most credibility-damaging paragraph on the entire site. Every reviewer flagged it. An MP or journalist reading this will immediately question the author's judgment.
- **Fix:** Remove this subsection entirely. It adds nothing and actively undercuts everything around it.

### 7. #hook: the injury is absent from the opening

- **Problem:** The hook says "I asked for my own CCTV footage" but never says "I was injured." The word "accident" appears zero times. The hook reads as a dispute about footage, not the story of a person with a traumatic brain injury who cannot remember what happened to them.
- **Fix:** Add: "I was injured in a road accident and suffered a traumatic brain injury. I asked for my own CCTV footage to understand what happened to me. I was refused. The footage was deleted. The regulator found no breach."

### 8. "Both cannot be true" false dichotomy

- **Where:** `#story` line 289 equivalent
- **Text:** "Both cannot be true at the same time. So who is correct, Parliament and the Minister, or PDPC?"
- **Problem:** The Minister described general legal requirements in a parliamentary answer. PDPC applied the law to specific facts. There's no necessary contradiction — both could be correct within their contexts. The false-dichotomy framing invites PDPC to easily rebut it.
- **Fix:** "The Minister's assurance describes what the law intends. PDPC's rulings describe what happened. The gap between them — 13 days from request to deletion with no preservation — raises the question of whether the law as applied achieves what Parliament was told it guarantees."

### 9. "De facto policy" claim needs stronger caveating

- **Where:** `#story` lines 212-216
- **Text:** "PDPC operates a de facto policy of non-enforcement of the Access Obligation for CCTV footage."
- **Problem:** Accusing a Singapore statutory board of operating a "de facto policy" of non-enforcement is a serious allegation. The hedging follows the claim rather than preceding it. MPCs will ask "can you prove a policy, or are you inferring from a pattern?"
- **Fix:** "The documented record is consistent with a pattern of systematic non-enforcement. This site does not assert an explicit policy — only that the evidence points consistently in this direction. [List the facts that support the inference.]"

### 10. #reform: no prioritization across 12 items

- **Problem:** 4 legislative asks + 8 parliamentary questions = 12 items. An MP can table one PQ per session. They need to know which to lead with.
- **Fix:** Star or bold the single most impactful question in each category.

### 11. #timeline: four entries with only "2025" as the date

- **Problem:** "2025" spanning an entire year looks incomplete. These are critical entries — they show even parliamentary intervention failed.
- **Fix:** Every entry must have at least a month. "Mar 2025", "Sep 2025", etc.

### 12. "about four months" is imprecise

- **Where:** `#narrative` line 614
- **Text:** "about four months after the 4 May 2024 complaint"
- **Problem:** 4 May to 4 August is three months. Stretching to "about four" hurts credibility.
- **Fix:** "over three months after" or use exact month: "August 2024, over three months later"

### 13. Contradiction 3.2: §5.1(b) quoted out of context

- **Where:** `#contradictions` card #2, and `contradictions-source-citations.html` §2
- **Problem:** §5.1(b) is about excluded categories of personal data (public agencies, employment), not identifiability. The combination test comes from §5.7, which is correctly quoted second. Quoting the wrong guideline section weakens the argument.
- **Fix:** Remove the §5.1(b) quote or replace with one that actually addresses the combination/identifiability test.

### 14. Failure #5: security guard statements unsourced

- **Problem:** "The MCST's own security guards said footage was kept for many months" — no source citation. Important factual claim without verification.
- **Fix:** Add source citation to the correspondence or statement recording this claim.

### 15. MCST 3615 "unnamed" claim needs verification

- **Where:** `#cases` line 314
- **Text:** "Property Facility Services Pte Ltd (PFS), unnamed in the published summary"
- **Problem:** If PFS is named anywhere in the published Summary, this claim is false and PDPC can use it.
- **Fix:** Verify against the actual PDF. If the summary does not name PFS, cite the specific paragraph where the omission occurs.

### 16. Enforcement count needs a specific verification date

- **Problem:** "at the time of this compilation" appears multiple times without a date.
- **Fix:** Add: "compiled June 2026, verified 21 June 2026" or similar specific timestamp.

### 17. #why: "The enforcer became the damager" heading

- **Problem:** Emotionally charged language. May trigger defensiveness in MPs. Content is solid but heading undermines it.
- **Fix:** "When enforcement defeats the right" or "When the regulator invalidates the statute."

### 18. #process h2 is three sentences crammed into one heading

- **Problem:** "PDPC ceased communication. External agencies were told the issues were addressed. The published-decisions filter has no obligation-type filter." — three separate claims in one h2. Hard to scan.
- **Fix:** Single heading: "Three patterns across 19 months." Use subheadings for details.

---

## GREEN: Nice to Have (polish, not urgent)

### 19. Expand acronyms on first use in each section (DPO, MCST, IAU, QSM)
- The nav allows direct jumps to any section. Acronyms should be re-expanded on first use in each section.

### 20. #hook: "willing to be corrected" placed too early
- Appears before the reader has seen any evidence. Reads as lack of conviction. Move to footer only.

### 21. #summary: no recommended reading path for MPs
- Three CTA cards but no guidance on sequence. A busy MP doesn't know where to click first.

### 22. "subarachnoid haemorrhage" needs layperson gloss
- Add "(bleeding around the brain)" or "(bleeding on the brain)"

### 23. ComfortDelGro listed in cases note but never discussed
- Line 343-344 names ComfortDelGro without context. Either explain relevance or remove.

### 24. #verify: NotebookLM needs explanation
- Most readers won't know what NotebookLM is. Add one sentence explaining it.

### 25. "The ask" → "What is being asked of Parliament"
- Business jargon in a Parliament-facing document.

### 26. "Free society" language
- "the mechanism by which a free society supervises private power" — may trigger framing debate. Use "how the public holds private power to account."

### 27. #why subsection titles could be more descriptive
- "The enforcer became the damager" → "When enforcement defeats the right"
- "Who guards the guards?" → keep, it's strong

### 28. Failure #12: MBS comparison acknowledges different data types
- A casino membership database and CCTV footage are different identification mechanisms. Acknowledge this explicitly before making the comparison.

---

## Priority Implementation Order

1. Fix the arithmetic error (13 days, not 17) — **5 minutes**
2. Reconcile investigation start date contradiction — **5 minutes**
3. Fix "Five" → "Six" in narrative header — **1 minute**
4. Fix "Seven" → "Ten" in contradictions source page — **1 minute**
5. Fix s.4(6) "required" → "could provide" — **1 minute**
6. Remove Street View subsection — **1 minute**
7. Add injury to the hook — **2 minutes**
8. Fix "Both cannot be true" false dichotomy — **2 minutes**
9. Add caveat to "de facto policy" claim — **3 minutes**
10. Fix timeline dates — **5 minutes**
11-28. Remaining AMBER and GREEN items — **30 minutes**
