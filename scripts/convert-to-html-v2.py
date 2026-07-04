import re, os
from pathlib import Path

dir = Path('data/personalised-emails')

# ============= SHARED SECTIONS (identical across all 109) =============

MARADONA = """<h2>The Maradona analogy</h2>
<p>To borrow an analogy from football, this is the &ldquo;Hand of God&rdquo; moment. I asked the referee, PDPC, to review the play. It refused to examine the evidence and let the goal stand. Today&rsquo;s game has VAR, cameras, and replay. Even with all that evidence available, the <strong>referee still looked away.</strong> Worse, in football, that referee can be reviewed and held to account. <strong>Here, the enforcer sits in judgment of itself, and nothing happens.</strong></p>
<p>A referee has discretion over marginal fouls in a fast game. But when a clear foul is committed and the offending player scores, the referee cannot simply wave play on and invent a reason. That is not discretion. <strong>That is a failure of duty.</strong> PDPC effectively told me that the rulebook itself was wrong, that its own Advisory Guidelines were not determinative and that the PDPA takes precedence, while refusing to identify which guideline, which clause, or which conflict was meant. At the same time, PDPC continues to enforce the Protection Obligation against data leaks at major organisations. It cannot tell one player the rules do not apply while continuing to referee the rest of the tournament under them.</p>"""

WHY = """<h2>Why this matters</h2>
<p>My original complaint arose because CCTV footage that would have shown what happened to me was denied, then destroyed.</p>
<p>The footage is gone. I am not asking for it to be restored. That is impossible.</p>
<p>The larger issue is whether the PDPA&rsquo;s Access Obligation is being enforced in practice at all, especially where CCTV footage is denied, delayed, or deleted before access can be meaningfully reviewed.</p>
<p>Across more than a decade of published enforcement decisions, PDPC has found <strong>204 breaches of the Protection Obligation</strong>, but <strong>0 breaches of the Access Obligation</strong> across the published record I reviewed.</p>
<p>This is not a minor statistical point. It suggests that one side of the PDPA is enforced actively, while the individual&rsquo;s right of access has effectively never resulted in a published breach finding.</p>
<p>I accept that any enforcement body, whether police, civil defence, or a statutory regulator, must <strong>exercise judgment</strong> in deciding the level and priority of active enforcement based on the circumstances of the day. But discretion over enforcement priority is not the same as <strong>permission to disregard the law.</strong> An enforcement body may decide how best to allocate resources, but it cannot <strong>ignore a statutory right, deny meaningful review,</strong> and leave the <strong>affected individual without justice</strong> while protecting the very conduct the law was meant to prevent.</p>"""

FACTS = """<h2>Where the full facts are documented</h2>
<p>I have set out the full account, supporting documents, enforcement matrix, and timeline at:</p>
<p><a href="https://pdpaaccessrights.sg">pdpaaccessrights.sg</a></p>
<p>In particular, the rebuilt enforcement matrix is here:</p>
<p><a href="https://pdpaaccessrights.sg/enforcement-index.html">https://pdpaaccessrights.sg/enforcement-index.html</a></p>
<p>The purpose of the website is not to personalise the issue. It is to preserve the record and allow others to verify whether the Access Obligation is being enforced in practice.</p>"""

SITES = """<h2>Sites for verification</h2>
<ol>
<li><p><a href="https://pdpaaccessrights.sg">pdpaaccessrights.sg</a></p><p>Full account of the documented pattern, rebuilt enforcement filter, and primary record.</p></li>
<li><p><a href="https://pdpaaccessrights.sg/enforcement-index.html">Rebuilt enforcement matrix</a></p><p>Shows <strong>0 Access Obligation breach findings</strong> across <strong>374 published decisions</strong> reviewed.</p></li>
<li><p><a href="https://www.pdpc.gov.sg/organisations/regulations-decisions/enforcement-decisions?type=Commission%27s+Decisions&page=1&sort=latest">Official PDPC enforcement decisions page</a></p><p>The official PDPC page, now filterable by enforcement type and year, but no longer by obligation type.</p></li>
<li><p><a href="https://sprs.parl.gov.sg/search/#/sprs3topic?reportid=written-answer-19596">Parliament Written Answer 19596</a></p><p>Minister Josephine Teo&rsquo;s Parliamentary assurance of 22 September 2025 on data preservation and criminal penalties for intentional concealment.</p></li>
</ol>"""

ATTACHMENTS = """<h2>Attachments</h2>
<ol>
<li><p><strong>BreachBreakdown.jpg</strong></p><p>PDPC breach by obligation chart, showing <strong>204 Protection Obligation breaches</strong> versus <strong>0 Access Obligation breaches</strong>.</p></li>
<li><p><strong>entry-gate-overlay.jpg</strong></p><p>Entry overlay from pdpaaccessrights.sg.</p></li>
<li><p><strong>pdpa-masking-42.png</strong></p><p>PDPC Advisory Guidelines, page 42, paragraph 4.59, stating that blurred or pixelated masking may not be foolproof.</p></li>
<li><p><strong>hansard.jpg</strong></p><p>Parliament Written Answer 19596, 22 September 2025, on preservation and criminal penalties.</p></li>
</ol>"""

# ============= PER-FILE PARSING =============

def parse_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return None

    # Parse frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None
    fm_text = parts[1]
    body = parts[2].strip()
    # Strip **Subject:** prefix line if present (old Tier 2 format)
    if body.startswith('**Subject:'):
        body = body.split('
', 1)[-1].strip()
', 1)[-1].strip()

    fm = {}
    for line in fm_text.split('\n'):
        m = re.match(r'^(\w+):\s*(.*)', line)
        if m: fm[m.group(1)] = m.group(2).strip()

    tier = fm.get('tier', '3')
    name = fm.get('name', '')
    slug = fm.get('slug', '')
    email = fm.get('email', '')
    designation = fm.get('designation', '')
    subject = fm.get('subject', 'Follow-up on the PDPC grievance')

    # Extract greeting name
    greeting_match = re.match(r'Dear\s+(.+?)(?:,|\.)\s*(.*)', body, re.DOTALL)
    if not greeting_match:
        return None
    greeting_name = greeting_match.group(1).strip()
    body_text = greeting_match.group(2).strip()

    # Extract CC
    cc_match = re.search(r'(?:^|\n)CC:\s*(.+?)(?:\n\n|$)', body_text)
    cc = cc_match.group(1).strip() if cc_match else None
    if cc:
        body_text = body_text.replace(cc_match.group(0), '').strip()

    # Find bespoke opening: everything until the first shared-paragraph indicator
    shared_starts = [
        'PDPC recently redesigned', 'Across over a decade', 'The Personal Data Protection Commission',
        'To borrow an analogy', 'In March 2025, PDPC', 'PDPC responded to my complaint',
        'The Maradona Hand-of-God', 'The Maradona analogy', 'I am writing to update you',
        'Recently I discovered', 'I still do not know',
    ]
    opening_end = len(body_text)
    for keyword in shared_starts:
        idx = body_text.find(keyword)
        if idx >= 0 and idx < opening_end:
            opening_end = idx
    opening = body_text[:opening_end].strip()
    remainder = body_text[opening_end:].strip()

    # Find the closing question: the last bespoke paragraph before "Four sites to verify", "CC:", or "Yours sincerely,"
    # The closing question is a sentence or two asking the recipient to act
    # Find the earliest of these markers from the END of `remainder`
    end_markers = ['Four sites to verify:', 'CC:', 'Yours sincerely,']
    closing_cut = len(remainder)
    for marker in end_markers:
        idx = remainder.find(marker)
        if idx >= 0 and idx < closing_cut:
            closing_cut = idx

    # Everything after `opening_end` and before `closing_cut` is the shared body
    # The closing question is the text just before `closing_cut` in `remainder`
    # Actually, the closing question might be embedded in the body. Let me take a different approach:
    # Find "Yours sincerely," and work backwards to get the last non-shared paragraph
    ys_idx = remainder.find('Yours sincerely,')
    if ys_idx >= 0:
        remainder = remainder[:ys_idx].strip()

    # The closing question is the last meaningful sentence(s) in remainder
    # that aren't part of the shared body
    # Strategy: split remainder by newline paragraphs, find the last non-empty non-shared paragraph
    paras = [p.strip() for p in remainder.split('\n\n') if p.strip()]

    closing_question = ''
    if paras:
        # Last paragraph is usually the bespoke closing question
        last = paras[-1]
        # Check if last paragraph is definitely bespoke (not shared)
        if not any(last.startswith(s) for s in [
            'Four sites', 'In March', 'PDPC recently', 'Across over',
            'To borrow', 'The worst part', 'The Maradona', 'I still do not know',
            'I am writing', 'Recently I discovered', 'The PDPA',
            'Section 21', 'The footage', 'I rebuilt', 'But here',
            'And here', 'The referee', 'The consequence',
        ]):
            closing_question = last

    return {
        'tier': tier, 'name': name, 'slug': slug, 'email': email,
        'designation': designation, 'subject': subject,
        'greeting_name': greeting_name, 'opening': opening,
        'closing_question': closing_question, 'cc': cc,
    }

def build_html(data):
    d = data
    tier = str(d['tier'])
    parts = []

    # Greeting line
    parts.append(f'<p>Dear <strong>{d["greeting_name"]}</strong>,</p>')

    # Bespoke opening
    if d['opening']:
        parts.append(f'<p>{d["opening"]}</p>')

    # Maradona analogy (Tier 1 + 2 only; skipped for Tier 3)
    if tier in ('1', '2'):
        parts.append(MARADONA)

    # For Tier 3: brief context before the "Why this matters" section
    if tier == '3':
        parts.append('<p>I rebuilt the missing enforcement filter at <a href="https://pdpaaccessrights.sg">pdpaaccessrights.sg</a>. The issue is larger than my own case.</p>')

    # Why this matters
    parts.append(WHY)

    # Where facts are documented
    parts.append(FACTS)

    # What I am asking (bespoke closing question)
    if d['closing_question']:
        parts.append('<h2>What I am asking</h2>')
        parts.append(f'<p>{d["closing_question"]}</p>')

    # Sites for verification
    parts.append(SITES)

    # Attachments
    parts.append(ATTACHMENTS)

    # CC
    if d['cc']:
        parts.append(f'<p>CC: {d["cc"]}</p>')

    # Signature
    parts.append('<p>Yours sincerely,<br>Ray Lim</p>')

    body_html = '\n\n'.join(parts)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; max-width: 640px; margin: 0 auto; padding: 20px; color: #222; line-height: 1.7;">

{body_html}

</body>
</html>"""

    return html

# ============= MAIN =============

count = 0
skipped = 0
for f in sorted(dir.glob('*.md')):
    if f.stem == 'gpc-digital-development-and-information':
        continue  # GPC email is different — handled separately

    data = parse_file(f)
    if data is None:
        skipped += 1
        continue

    html = build_html(data)

    new_content = f"""---
tier: {data['tier']}
name: {data['name']}
slug: {data['slug']}
email: {data['email']}
designation: {data['designation']}
subject: {data['subject']}
---

{html}"""
    f.write_text(new_content, encoding='utf-8')
    count += 1
    if count <= 5:
        print(f'OK {data["slug"]} ({data["tier"]}): greeting="{data["greeting_name"]}", opening_len={len(data["opening"])}, closing_q="{data["closing_question"][:60]}"')

print(f'\nConverted {count} files, skipped {skipped}')
