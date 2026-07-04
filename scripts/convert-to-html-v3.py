import re, os
from pathlib import Path

DIR = Path('data/personalised-emails')

# ============= SHARED HTML SECTIONS =============

MARADONA = "<h2>The Maradona analogy</h2>\n" + \
"<p>To borrow an analogy from football, this is the &ldquo;Hand of God&rdquo; moment. I asked the referee, PDPC, to review the play. It refused to examine the evidence and let the goal stand. Today&rsquo;s game has VAR, cameras, and replay. Even with all that evidence available, the <strong>referee still looked away.</strong> Worse, in football, that referee can be reviewed and held to account. <strong>Here, the enforcer sits in judgment of itself, and nothing happens.</strong></p>\n" + \
"<p>A referee has discretion over marginal fouls in a fast game. But when a clear foul is committed and the offending player scores, the referee cannot simply wave play on and invent a reason. That is not discretion. <strong>That is a failure of duty.</strong> PDPC effectively told me that the rulebook itself was wrong, that its own Advisory Guidelines were not determinative and that the PDPA takes precedence, while refusing to identify which guideline, which clause, or which conflict was meant. At the same time, PDPC continues to enforce the Protection Obligation against data leaks at major organisations. It cannot tell one player the rules do not apply while continuing to referee the rest of the tournament under them.</p>"

WHY = "<h2>Why this matters</h2>\n" + \
"<p>My original complaint arose because CCTV footage that would have shown what happened to me was denied, then destroyed.</p>\n" + \
"<p>The footage is gone. I am not asking for it to be restored. That is impossible.</p>\n" + \
"<p>The larger issue is whether the PDPA&rsquo;s Access Obligation is being enforced in practice at all, especially where CCTV footage is denied, delayed, or deleted before access can be meaningfully reviewed.</p>\n" + \
"<p>Across more than a decade of published enforcement decisions, PDPC has found <strong>204 breaches of the Protection Obligation</strong>, but <strong>0 breaches of the Access Obligation</strong> across the published record I reviewed.</p>\n" + \
"<p>This is not a minor statistical point. It suggests that one side of the PDPA is enforced actively, while the individual&rsquo;s right of access has effectively never resulted in a published breach finding.</p>\n" + \
"<p>I accept that any enforcement body, whether police, civil defence, or a statutory regulator, must <strong>exercise judgment</strong> in deciding the level and priority of active enforcement based on the circumstances of the day. But discretion over enforcement priority is not the same as <strong>permission to disregard the law.</strong> An enforcement body may decide how best to allocate resources, but it cannot <strong>ignore a statutory right, deny meaningful review,</strong> and leave the <strong>affected individual without justice</strong> while protecting the very conduct the law was meant to prevent.</p>"

FACTS = "<h2>Where the full facts are documented</h2>\n" + \
"<p>I have set out the full account, supporting documents, enforcement matrix, and timeline at:</p>\n" + \
'<p><a href="https://pdpaaccessrights.sg">pdpaaccessrights.sg</a></p>\n' + \
"<p>In particular, the rebuilt enforcement matrix is here:</p>\n" + \
'<p><a href="https://pdpaaccessrights.sg/enforcement-index.html">https://pdpaaccessrights.sg/enforcement-index.html</a></p>\n' + \
"<p>The purpose of the website is not to personalise the issue. It is to preserve the record and allow others to verify whether the Access Obligation is being enforced in practice.</p>"

SITES = "<h2>Sites for verification</h2>\n" + \
"<ol>\n" + \
'<li><p><a href="https://pdpaaccessrights.sg">pdpaaccessrights.sg</a></p><p>Full account of the documented pattern, rebuilt enforcement filter, and primary record.</p></li>\n' + \
'<li><p><a href="https://pdpaaccessrights.sg/enforcement-index.html">Rebuilt enforcement matrix</a></p><p>Shows <strong>0 Access Obligation breach findings</strong> across <strong>374 published decisions</strong> reviewed.</p></li>\n' + \
'<li><p><a href="https://www.pdpc.gov.sg/organisations/regulations-decisions/enforcement-decisions?type=Commission%27s+Decisions&page=1&sort=latest">Official PDPC enforcement decisions page</a></p><p>The official PDPC page, now filterable by enforcement type and year, but no longer by obligation type.</p></li>\n' + \
'<li><p><a href="https://sprs.parl.gov.sg/search/#/sprs3topic?reportid=written-answer-19596">Parliament Written Answer 19596</a></p><p>Minister Josephine Teo&rsquo;s Parliamentary assurance of 22 September 2025 on data preservation and criminal penalties for intentional concealment.</p></li>\n' + \
"</ol>"

ATTACHMENTS = "<h2>Attachments</h2>\n" + \
"<ol>\n" + \
"<li><p><strong>BreachBreakdown.jpg</strong></p><p>PDPC breach by obligation chart, showing <strong>204 Protection Obligation breaches</strong> versus <strong>0 Access Obligation breaches</strong>.</p></li>\n" + \
"<li><p><strong>entry-gate-overlay.jpg</strong></p><p>Entry overlay from pdpaaccessrights.sg.</p></li>\n" + \
"<li><p><strong>pdpa-masking-42.png</strong></p><p>PDPC Advisory Guidelines, page 42, paragraph 4.59, stating that blurred or pixelated masking may not be foolproof.</p></li>\n" + \
"<li><p><strong>hansard.jpg</strong></p><p>Parliament Written Answer 19596, 22 September 2025, on preservation and criminal penalties.</p></li>\n" + \
"</ol>"

WRAPPER_OPEN = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n</head>\n<body style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; max-width: 640px; margin: 0 auto; padding: 20px; color: #222; line-height: 1.7;">\n\n'
WRAPPER_CLOSE = '\n\n</body>\n</html>'

# ============= MAIN =============

def extract_opening(body_text):
    """Everything before the first shared-paragraph indicator is the bespoke opening."""
    markers = [
        'PDPC recently redesigned',
        'Across over a decade',
        'The Personal Data Protection Commission',
        'To borrow an analogy',
        'In March 2025, PDPC',
        'PDPC responded to my complaint',
        'The Maradona Hand-of-God',
        'The Maradona analogy',
        'I am writing to update you',
        'Recently I discovered',
        'I still do not know',
        'The picture is this.',
        'PDPC responded to my complaint',
    ]
    cut = len(body_text)
    for m in markers:
        idx = body_text.find(m)
        if 0 <= idx < cut:
            cut = idx
    return body_text[:cut].strip()

def extract_closing(body_text):
    """The last non-shared paragraph(s) before signature plates."""
    # Find "Yours sincerely," or "CC:" or "Four sites to verify:"
    cut = len(body_text)
    for m in ['Four sites to verify:', 'CC:', 'Yours sincerely,']:
        idx = body_text.rfind(m)
        if 0 <= idx < cut:
            cut = idx
    after = body_text[cut:].strip()
    # The closing is everything from this cut point to the end
    return after

count = 0
for f in sorted(DIR.glob('*.md')):
    if f.stem == 'gpc-digital-development-and-information':
        continue

    content = f.read_text(encoding='utf-8')
    if not content.startswith('---'):
        continue
    parts = content.split('---', 2)
    if len(parts) < 3:
        continue

    # Parse frontmatter
    fm = {}
    for line in parts[1].split('\n'):
        m = re.match(r'^(\w+):\s*(.*)', line)
        if m:
            fm[m.group(1)] = m.group(2).strip()

    tier = fm.get('tier', '3')
    name = fm.get('name', '')
    slug = fm.get('slug', '')
    email = fm.get('email', '')
    designation = fm.get('designation', '')
    subject = fm.get('subject', 'Follow-up on the PDPC grievance')

    # Parse body
    body = parts[2].strip()
    # Skip any **Subject:** or blank lines
    body = re.sub(r'^\*\*Subject:.*?\*\*\s*\n+', '', body)

    # Find greeting
    gm = re.match(r'Dear\s+(.+?)(?:,|\.)\s*\n*(.*)', body, re.DOTALL)
    if not gm:
        print(f'SKIP {f.name}: no greeting')
        continue
    greeting_name = gm.group(1).strip()
    body_text = gm.group(2).strip()

    # Extract CC
    cc = None
    ccm = re.search(r'(?:^|\n)CC:\s*(.+?)(?:\n\n|$)', body_text)
    if ccm:
        cc = ccm.group(1).strip()
        body_text = body_text.replace(ccm.group(0), '').strip()

    # Extract opening
    opening = extract_opening(body_text)

    # Extract closing (removing sites and attachments from it)
    full_closing = extract_closing(body_text)
    # Strip "Four sites to verify:" section and "Yours sincerely," from closing
    closing_clean = re.sub(r'Four sites to verify:.*?(?=CC:|Yours sincerely,|$)', '', full_closing, flags=re.DOTALL).strip()
    closing_clean = re.sub(r'CC:.*?(?=\n\n|$)', '', closing_clean, flags=re.DOTALL).strip()
    closing_clean = re.sub(r'Yours sincerely,.*$', '', closing_clean, flags=re.DOTALL).strip()
    # Remove "Attachments:" section too
    closing_clean = re.sub(r'Attachments:.*$', '', closing_clean, flags=re.DOTALL).strip()

    # Build HTML body
    html_parts = []
    html_parts.append(f'<p>Dear <strong>{greeting_name}</strong>,</p>')

    if opening:
        html_parts.append(f'<p>{opening}</p>')

    if tier in ('1', '2'):
        html_parts.append(MARADONA)
    else:
        html_parts.append('<p>I rebuilt the missing enforcement filter at <a href="https://pdpaaccessrights.sg">pdpaaccessrights.sg</a>. The issue is larger than my own case.</p>')

    html_parts.append(WHY)
    html_parts.append(FACTS)

    if closing_clean:
        html_parts.append('<h2>What I am asking</h2>')
        html_parts.append(f'<p>{closing_clean}</p>')

    html_parts.append(SITES)
    html_parts.append(ATTACHMENTS)

    if cc:
        html_parts.append(f'<p>CC: {cc}</p>')

    html_parts.append('<p>Yours sincerely,<br>Ray Lim</p>')

    body_html = '\n\n'.join(html_parts)
    full_html = WRAPPER_OPEN + body_html + WRAPPER_CLOSE

    # Write back
    new_content = f"---\ntier: {tier}\nname: {name}\nslug: {slug}\nemail: {email}\ndesignation: {designation}\nsubject: {subject}\n---\n\n{full_html}"
    f.write_text(new_content, encoding='utf-8')
    count += 1
    if count <= 5:
        print(f'OK {slug} ({tier}): greeting="{greeting_name}", opening={len(opening)}chars, closing={len(closing_clean)}chars')

print(f'\nConverted {count} files to HTML format')
