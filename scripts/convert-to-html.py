import re, os, json
from pathlib import Path

dir = Path('data/personalised-emails')
files = sorted(dir.glob('*.md'))

# ====================================================================
# SHARED HTML SECTIONS (from the user's approved template: Template Email PM.md)
# ====================================================================

def maradona_section():
    """Shared Maradona analogy — same for all Tier 1 + 2, dropped for Tier 3"""
    return """<h2>The Maradona analogy</h2>

<p>To borrow an analogy from football, this is the &ldquo;Hand of God&rdquo; moment. I asked the referee, PDPC, to review the play. It refused to examine the evidence and let the goal stand. Today&rsquo;s game has VAR, cameras, and replay. Even with all that evidence available, the <strong>referee still looked away.</strong> Worse, in football, that referee can be reviewed and held to account. <strong>Here, the enforcer sits in judgment of itself, and nothing happens.</strong></p>

<p>A referee has discretion over marginal fouls in a fast game. But when a clear foul is committed and the offending player scores, the referee cannot simply wave play on and invent a reason. That is not discretion. <strong>That is a failure of duty.</strong> PDPC effectively told me that the rulebook itself was wrong, that its own Advisory Guidelines were not determinative and that the PDPA takes precedence, while refusing to identify which guideline, which clause, or which conflict was meant. At the same time, PDPC continues to enforce the Protection Obligation against data leaks at major organisations. It cannot tell one player the rules do not apply while continuing to referee the rest of the tournament under them.</p>
"""

def why_this_matters():
    return """<h2>Why this matters</h2>

<p>My original complaint arose because CCTV footage that would have shown what happened to me was denied, then destroyed.</p>

<p>The footage is gone. I am not asking for it to be restored. That is impossible.</p>

<p>The larger issue is whether the PDPA&rsquo;s Access Obligation is being enforced in practice at all, especially where CCTV footage is denied, delayed, or deleted before access can be meaningfully reviewed.</p>

<p>Across more than a decade of published enforcement decisions, PDPC has found <strong>204 breaches of the Protection Obligation</strong>, but <strong>0 breaches of the Access Obligation</strong> across the published record I reviewed.</p>

<p>This is not a minor statistical point. It suggests that one side of the PDPA is enforced actively, while the individual&rsquo;s right of access has effectively never resulted in a published breach finding.</p>

<p>I accept that any enforcement body, whether police, civil defence, or a statutory regulator, must <strong>exercise judgment</strong> in deciding the level and priority of active enforcement based on the circumstances of the day. But discretion over enforcement priority is not the same as <strong>permission to disregard the law.</strong> An enforcement body may decide how best to allocate resources, but it cannot <strong>ignore a statutory right, deny meaningful review,</strong> and leave the <strong>affected individual without justice</strong> while protecting the very conduct the law was meant to prevent.</p>
"""

def where_facts_are():
    return """<h2>Where the full facts are documented</h2>

<p>I have set out the full account, supporting documents, enforcement matrix, and timeline at:</p>

<p><a href="https://pdpaaccessrights.sg">pdpaaccessrights.sg</a></p>

<p>In particular, the rebuilt enforcement matrix is here:</p>

<p><a href="https://pdpaaccessrights.sg/enforcement-index.html">https://pdpaaccessrights.sg/enforcement-index.html</a></p>

<p>The purpose of the website is not to personalise the issue. It is to preserve the record and allow others to verify whether the Access Obligation is being enforced in practice.</p>
"""

def sites_for_verification():
    return """<h2>Sites for verification</h2>

<ol>
<li><p><a href="https://pdpaaccessrights.sg">pdpaaccessrights.sg</a></p>
<p>Full account of the documented pattern, rebuilt enforcement filter, and primary record.</p></li>
<li><p><a href="https://pdpaaccessrights.sg/enforcement-index.html">Rebuilt enforcement matrix</a></p>
<p>Shows <strong>0 Access Obligation breach findings</strong> across <strong>374 published decisions</strong> reviewed.</p></li>
<li><p><a href="https://www.pdpc.gov.sg/organisations/regulations-decisions/enforcement-decisions?type=Commission%27s+Decisions&page=1&sort=latest">Official PDPC enforcement decisions page</a></p>
<p>The official PDPC page, now filterable by enforcement type and year, but no longer by obligation type.</p></li>
<li><p><a href="https://sprs.parl.gov.sg/search/#/sprs3topic?reportid=written-answer-19596">Parliament Written Answer 19596</a></p>
<p>Minister Josephine Teo&rsquo;s Parliamentary assurance of 22 September 2025 on data preservation and criminal penalties for intentional concealment.</p></li>
</ol>
"""

def attachments():
    return """<h2>Attachments</h2>

<ol>
<li><p><strong>BreachBreakdown.jpg</strong></p>
<p>PDPC breach by obligation chart, showing <strong>204 Protection Obligation breaches</strong> versus <strong>0 Access Obligation breaches</strong>.</p></li>
<li><p><strong>entry-gate-overlay.jpg</strong></p>
<p>Entry overlay from pdpaaccessrights.sg.</p></li>
<li><p><strong>pdpa-masking-42.png</strong></p>
<p>PDPC Advisory Guidelines, page 42, paragraph 4.59, stating that blurred or pixelated masking may not be foolproof.</p></li>
<li><p><strong>hansard.jpg</strong></p>
<p>Parliament Written Answer 19596, 22 September 2025, on preservation and criminal penalties.</p></li>
</ol>
"""

# ====================================================================
# PER-RECIPIENT CONTENT EXTRACTION
# ====================================================================

def extract_personalisation(content):
    """Extract bespoke opening and closing from existing .md file."""
    # Strip frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        body = parts[2].strip() if len(parts) >= 3 else content
    else:
        body = content.strip()

    # Find the bespoke opening: everything after the greeting until the first shared paragraph
    # The greeting is "Dear X," — we need the text after that
    greeting_m = re.match(r'Dear\s+([^,]+),?\s*(.*)', body, re.DOTALL)
    if not greeting_m:
        return None, None, None

    greeting_name = greeting_m.group(1).strip()
    rest = greeting_m.group(2).strip()

    # The opening is everything before the first shared section
    # Look for indicators of shared content
    shared_indicators = [
        'PDPC recently redesigned',
        'Across over a decade',
        'The Personal Data Protection Commission has never',
        'To borrow an analogy',
        'In March 2025, PDPC',
        'PDPC responded to my complaint',
        'The Maradona Hand-of-God',
        'The Maradona analogy',
    ]

    opening_end = len(rest)
    for indicator in shared_indicators:
        idx = rest.find(indicator)
        if idx >= 0 and idx < opening_end:
            opening_end = idx

    opening = rest[:opening_end].strip()
    remainder = rest[opening_end:].strip()

    # Find the closing question — it's the last bespoke paragraph before "Four sites to verify" or "CC:" or "Yours sincerely,"
    closing_markers = ['Four sites to verify:', 'CC:', 'Yours sincerely,']
    closing_start = len(remainder)
    for marker in closing_markers:
        idx = remainder.rfind(marker)
        if idx >= 0 and idx < closing_start:
            closing_start = idx

    closing = remainder[closing_start:].strip() if closing_start < len(remainder) else ''
    middle = remainder[:closing_start].strip()

    return greeting_name, opening, closing

def extract_closing_question(closing_text):
    """Extract the bespoke closing question line from the text before sites/CC/sign-off."""
    # The closing question is usually one sentence asking the recipient to take action
    # It's between the shared body and the "Four sites to verify" / "CC:" / "Yours sincerely,"
    lines = closing_text.split('\n')
    question_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('Four sites') or stripped.startswith('CC:') or stripped.startswith('Yours'):
            break
        question_lines.append(stripped)
    return ' '.join(question_lines).strip()

def extract_cc(content):
    """Extract CC line if present."""
    m = re.search(r'^CC:\s*(.+)$', content, re.MULTILINE)
    return m.group(1).strip() if m else None

# ====================================================================
# BUILD EACH EMAIL
# ====================================================================

def build_email(slug, tier, name, email_addr, subject, greeting_name, bespoke_opening, closing_question, cc, designation):
    """Build a complete HTML email for one recipient."""
    parts = []

    # Greeting
    parts.append(f'<p>Dear <strong>{greeting_name}</strong>,</p>')

    # Bespoke opening paragraph
    if bespoke_opening:
        parts.append(f'<p>{bespoke_opening}</p>')

    # Maradona section (Tier 1 + 2 only; dropped for Tier 3)
    if tier in ('1', '2') or tier == 1 or tier == 2:
        parts.append(maradona_section())

    # Why this matters (Tier 3: include the rebuilding/CCTV context first)
    if tier == '3' or tier == 3:
        parts.append("""<p>I rebuilt the missing enforcement filter at <a href="https://pdpaaccessrights.sg">pdpaaccessrights.sg</a>. The issue is larger than my own case.</p>""")

    parts.append(why_this_matters())

    # Where facts are documented
    parts.append(where_facts_are())

    # What I am asking
    if closing_question:
        parts.append('<h2>What I am asking</h2>')
        parts.append(f'<p>{closing_question}</p>')

    # Sites for verification
    parts.append(sites_for_verification())

    # Attachments
    parts.append(attachments())

    # CC
    if cc:
        parts.append(f'<p>CC: {cc}</p>')

    # Signature
    parts.append('<p>Yours sincerely,<br>Ray Lim</p>')

    body_html = '\n\n'.join(parts)

    # Build the full HTML document
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

def extract_tier(content):
    """Extract tier from frontmatter or body."""
    m = re.search(r'^tier:\s*(\d+)', content, re.MULTILINE)
    if m:
        return m.group(1)
    # Fallback: if file has "CC:" it's probably tier 1
    if 'CC:' in content:
        return '1'
    # If it has the Maradona analogy, it's tier 1 or 2
    if 'Hand of God' in content or 'Maradona' in content:
        return '2'
    return '3'

# ====================================================================
# MAIN
# ====================================================================

def main():
    count = 0
    for f in files:
        slug = f.stem
        if slug == 'gpc-digital-development-and-information':
            continue  # Skip GPC — handled separately

        content = f.read_text(encoding='utf-8')
        tier = extract_tier(content)

        # Extract frontmatter
        fm = {}
        name = ''
        email_addr = ''
        subject = ''
        designation = ''
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                fm_text = parts[1]
                for line in fm_text.split('\n'):
                    m = re.match(r'^(\w+):\s*(.*)', line)
                    if m:
                        fm[m.group(1)] = m.group(2).strip()
                name = fm.get('name', '')
                email_addr = fm.get('email', '')
                subject = fm.get('subject', '')
                designation = fm.get('designation', '')

        # Extract greeting and personalisation
        result = extract_personalisation(content)
        if result is None:
            print(f'SKIP {slug}: could not parse')
            continue
        greeting_name, bespoke_opening, closing_text = result

        # Extract closing question from closing text
        closing_question = extract_closing_question(closing_text)

        # Extract CC
        cc = extract_cc(content)

        # Build HTML
        html = build_email(slug, tier, name, email_addr, subject, greeting_name, bespoke_opening, closing_question, cc, designation)

        # Write back as .md with HTML content
        new_content = f"""---
tier: {tier}
name: {name}
slug: {slug}
email: {email_addr}
designation: {designation}
subject: {subject}
---

{html}"""
        f.write_text(new_content, encoding='utf-8')
        count += 1

        if count <= 3:
            print(f'OK {slug} ({tier})')

    print(f'\nConverted {count} files to HTML')

if __name__ == '__main__':
    main()
