import re, json
from pathlib import Path

# ============================
# NEW SHARED TEMPLATE (user-approved, 5 July 2026)
# ============================

SITES_SECTION = """## Sites for verification

1. **pdpaaccessrights.sg**
Full account of the documented pattern, rebuilt enforcement filter, and primary record.

2. **Rebuilt enforcement matrix**
Shows the Access Obligation breach findings across the published decisions reviewed.

3. **Official PDPC enforcement decisions page**
The official PDPC page, now filterable by enforcement type and year, but no longer by obligation type.

4. **Parliament Written Answer 19596**
Minister Josephine Teo&rsquo;s Parliamentary assurance of **22 September 2025** on preservation and criminal penalties."""

ATTACHMENTS_SECTION = """## Attachments

1. **BreachBreakdown.jpg**
PDPC breach-by-obligation chart, showing Protection Obligation breach findings versus no Access Obligation breach finding in the reviewed published record.

2. **entry-gate-overlay.jpg**
Entry overlay from pdpaaccessrights.sg.

3. **pdpa-masking-42.png**
PDPC Advisory Guidelines, page 42, paragraph 4.59, stating that blurred or pixelated masking may not be foolproof and that individuals may still be identifiable. In my case, I was identified on-site from the footage by security guards, yet PDPC later relied on the footage to conclude that I was not identifiable.

4. **hansard.jpg**
Parliament Written Answer 19596, **22 September 2025**, on preservation and criminal penalties.

5. **conclusion-flow.jpeg**
The conclusion flow diagram: every deviation from the PDPA, PDPC&rsquo;s own Advisory Guidelines, and PDPC&rsquo;s own prior published decisions that PDPC had to take, in sequence, to reach the conclusion it issued."""

# ============================
# THESE SECTIONS ARE THE SAME FOR ALL RECIPIENTS
# ============================

SHARED_BODY = f"""
## Why this is a public issue

Across **374 published decisions reviewed**, PDPC has found **204 Protection Obligation breaches**, but **0 Access Obligation breaches**.

My two complaints appear to be the only two cases in which PDPC investigated the **Access Obligation in relation to CCTV footage**.

Even then, after PDPC was compelled to investigate following considerable effort, including reading the laws and guidelines myself, filing appeals, and repeatedly asking for review, **no Access Obligation breach was found**.

That raises a larger public question.

If this was the result in a case where the complainant persisted, documented the timeline, cited the law, and escalated repeatedly, how many ordinary Singaporeans and residents may have been told, in effect, that their access rights under the PDPA could not be exercised?

After all the pain I have gone through, I do not want others to face the same gap between the law as described and the law as enforced.

## The core problem

My original complaint arose because CCTV footage that would have shown what happened to me was denied, then destroyed.

The footage is gone. I am not asking for it to be restored. That is impossible.

The larger issue is whether the PDPA&rsquo;s Access Obligation is being enforced in practice at all, especially where CCTV footage is denied, delayed, or deleted before access can be meaningfully reviewed.

I accept that any enforcement body, whether police, civil defence, or a statutory regulator, must exercise judgment in deciding the level and priority of active enforcement based on the circumstances of the day.

But discretion over enforcement priority is not permission to disregard the law.

An enforcement body may decide how best to allocate resources, but it cannot ignore a statutory right, deny meaningful review, and leave the affected individual without justice while shielding the very conduct the law was meant to regulate.

## The &ldquo;Hand of God&rdquo; problem

To borrow an analogy from football, this is the **&ldquo;Hand of God&rdquo; problem**.

I asked the referee, PDPC, to review the play. The evidence was available. The rulebook was available. Parliament&rsquo;s assurance was later clear. Yet the goal was allowed to stand.

A referee has discretion over marginal fouls in a fast game. But when the rule is clear, the referee cannot simply wave play on and invent a reason after the fact.

That is not discretion. That is a failure of duty.

The diagram below sets out how PDPC did not reach its conclusion by applying one rule neutrally. It had to depart from multiple rules, ignore the real chronology, and accept institutional delay.

<p><img src="cid:conclusion-flow" alt="Conclusion flow diagram" style="max-width:100%;height:auto;display:block;margin:0.9em auto;"></p>

{SITES_SECTION}

{ATTACHMENTS_SECTION}"""

# ============================
# PER-RECIPIENT CUSTOMISATIONS
# ============================

def extract_bespoke_opening(old_body):
    """Extract the bespoke opening paragraph from the old .md body."""
    # Skip greeting and blank lines, take everything until a shared-paragraph indicator
    text = old_body.strip()
    # Strip the Dear line
    m = re.match(r'Dear\s+[^,]+,\s*(.*)', text, re.DOTALL)
    if not m:
        return '', text
    rest = m.group(1).strip()
    # Find the first shared indicator
    shared_markers = [
        'I am revisiting', 'PDPC recently redesigned', 'Across over a decade',
        'The Personal Data Protection Commission', 'To borrow an analogy',
        'In March 2025, PDPC', 'I am writing to update',
        'Recently I discovered', 'I still do not know',
        'My original complaint', 'The footage that would have shown',
        'I respectfully', 'You have been my', 'I hope this note',
        'I hope you are well', 'As Permanent Secretary',
        'As Second Permanent Secretary', 'As President',
        'As Deputy Secretary', 'As Minister of State',
        'As Senior Minister of State', 'As Mayor',
        'As the GPC tasked',
    ]
    cut = len(rest)
    for k in shared_markers:
        idx = rest.find(k)
        if 0 <= idx < cut:
            cut = idx
    opening = rest[:cut].strip()
    remainder = rest[cut:].strip()
    return opening, remainder

def extract_cc(text):
    """Extract CC line if present."""
    m = re.search(r'(?:^|\n)CC:\s*(.+?)(?:\n\n|$)', text)
    return m.group(1).strip() if m else None

def build_html_body(greeting_name, subject_line, opening, closing_ask, cc, include_opening_html=True):
    """Build the complete HTML body for one recipient."""
    parts = []

    # Greeting (as h2, same styling as template)
    parts.append(f'<h2 style="font-weight: normal; margin-bottom: 1.2em;">Dear <strong>{greeting_name}</strong>,</h2>')

    # Bespoke opening
    if opening and include_opening_html:
        parts.append(f'<p>{opening}</p>')

    # Shared body (the entire template body)
    parts.append(SHARED_BODY)

    # Request section (bespoke closing ask)
    if closing_ask:
        parts.append('<h2>Request</h2>')
        parts.append(f'<p>{closing_ask}</p>')

    # CC
    if cc:
        parts.append(f'<p>CC: {cc}</p>')

    # Signature
    parts.append('<p>Yours sincerely,<br>Ray Lim</p>')

    return '\n\n'.join(parts)

CSS = """body { font-family: Arial, Helvetica, sans-serif; font-size: 16px; max-width: 640px; margin: 0 auto; padding: 20px; color: #222; line-height: 1.5; }
p { margin-bottom: 0.9em; }
h2 { font-size: 1.15em; margin-top: 1.6em; margin-bottom: 0.6em; }
li { margin-bottom: 0.6em; }
ol { margin-bottom: 1em; }
a { color: #1a0dab; }"""

WRAPPER_OPEN = f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n</head>\n<body style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; max-width: 640px; margin: 0 auto; padding: 20px; color: #222; line-height: 1.5;">\n<style>\n{CSS}\n</style>\n'
WRAPPER_CLOSE = '\n</body>\n</html>'

# ============================
# RECIPIENT-SPECIFIC DATA
# ============================

# Load CC map
cc_map = json.loads(Path('data/pa-cc-map.json').read_text()) if Path('data/pa-cc-map.json').exists() else {}

# Bespoke closing questions per slug (drawn from the original personalised content)
closing_questions = {
    'josephine-teo': 'I respectfully ask whether your office still stands by the assurances given in Written Answer 19596, and whether the Ministry of Digital Development and Information will direct an independent review of PDPC&rsquo;s enforcement record in respect of the Access Obligation.',
    'lawrence-wong': 'I respectfully ask whether the Prime Minister&rsquo;s Office will direct an independent review into: (1)&nbsp;whether PDPC&rsquo;s handling of my complaints was consistent with the PDPA, Parliament&rsquo;s assurances, and PDPC&rsquo;s published Advisory Guidelines; (2)&nbsp;whether the Access Obligation is being enforced in practice; (3)&nbsp;why no Access Obligation breach appears to have been found across the published enforcement record reviewed; (4)&nbsp;whether PDPC&rsquo;s removal of the obligation-type filter from its enforcement website reduces public transparency over enforcement patterns; and (5)&nbsp;whether further safeguards are needed where CCTV footage is denied, delayed, or deleted after an access request has been made.',
    'zhulkarnain-abdul-rahim': 'I am not asking you to act as my MP in this matter, as you are now a Minister and the rules have changed. I am asking that you stay aware of the full record, and that you consider whether a follow-up parliamentary question on the zero-Access-Obligation-enforcement record is a proper use of your colleagues&rsquo; time in the House. Your constituency residents in Chua Chu Kang will ask; I want you to know the answer before they do.',
    'kenneth-goh': 'As my former SMU professor and now a Nominated Member of Parliament, I would ask whether this documented regulatory interpretation gap warrants formal scrutiny through your NMP platform. The documentary record is publicly available, and every conclusion on the site can be verified against primary sources.',
    'dinesh-vasu-dash': 'As someone who worked under your leadership at MOH during Covid, I would ask whether the documented pattern of PDPC non-enforcement warrants review, based solely on the public record. While your current portfolio at MCCY and MOM does not directly oversee PDPC, the principles of evidence-based policy and public accountability that I saw you uphold at MOH apply across ministries.',
    'cai-yinzhou': 'As a backbencher and a friend since youth, I would ask what procedural options are available to you to raise a documented systemic pattern in Parliament. I am not asking for a favour. I am asking that the record be reviewed.',
    'chan-chun-sing': 'I respectfully ask whether, as Coordinating Minister for Public Services, your office will review the accuracy of the representation made by IMDA to the Public Service Commission in this matter.',
    'edwin-tong-chun-fai': 'I respectfully ask whether the Law Ministry will review PDPC&rsquo;s stated position that its Advisory Guidelines are not determinative, when those same Guidelines appear to have been used as the sole basis for finding that my footage was not personal data.',
    'gan-kim-yong': 'I respectfully ask whether this matter warrants Cabinet-level review. The documented pattern affects the enforcement of a statutory right granted to all Singaporeans, and the internal channels have not produced a substantive response.',
    'indranee-rajah': 'I respectfully ask whether, as Leader of the House, you will consider whether this matter can be raised procedurally in Parliament through the channels available to the Government side.',
    'k-shanmugam': 'I respectfully ask whether, as Coordinating Minister for National Security and Minister for Home Affairs, your office will review whether the PDPA&rsquo;s Access Obligation is being read consistently with its purpose, particularly in cases where CCTV footage is at issue and public safety interests are engaged.',
    'lee-hsien-loong': 'I respectfully ask whether, as Senior Minister whose Government enacted the PDPA in 2012, this documented gap between the statute as written and the statute as enforced warrants your attention.',
    'seah-kian-peng': 'I respectfully ask whether the procedural channels of Parliament can accommodate a substantive motion or question on the documented enforcement pattern, and whether you would consider allowing a Member to raise it.',
}

# Civil servant closing questions
cs_closing_questions = {
    'istana-president': 'I respectfully ask that the President&rsquo;s office be aware of the documented pattern. I do not ask for intervention. I ask that the record be preserved, so that if constitutional questions arise regarding the enforcement of statutory rights under the PDPA, the facts are not lost.',
    'mddi-ps-chng': 'I respectfully ask whether your office will review the documented pattern and consider what internal steps are available to ensure that the Access Obligation is enforced as Parliament intended.',
    'mddi-2ps-foo': 'I respectfully ask whether the policy implications of the documented zero-Access-Obligation-enforcement record warrant review within the Ministry.',
    'mddi-2ps-wong': 'I respectfully ask whether the removal of the obligation-type filter from the public enforcement-decisions page is consistent with the Ministry&rsquo;s information-access objectives.',
    'pmo-ps-chan': 'I respectfully ask whether this matter warrants internal review at the PMO level, given that every other channel has been exhausted.',
    'psd-ps-tan': 'I respectfully ask whether PSD will review the accuracy of the representation made by IMDA to the Public Service Commission in this matter.',
    'psd-ds-han': 'I respectfully ask whether the conduct standards of the public service were upheld in the handling of this matter.',
    'psd-ds-jamie': 'I respectfully ask whether the enforcement gap between the Access Obligation and the Protection Obligation warrants review as a service-delivery issue.',
}

# ============================
# BUILD ALL FILES
# ============================

def process_directory(email_dir, is_civil_servant=False):
    count = 0
    for f in sorted(email_dir.glob('*.md')):
        slug = f.stem
        content = f.read_text(encoding='utf-8')

        # Parse old frontmatter
        tier = '1'
        name = ''
        email_addr = ''
        designation = ''
        old_subject = 'Follow-up on the PDPC grievance'

        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                for line in parts[1].split('\n'):
                    m = re.match(r'^(\w+):\s*(.*)', line)
                    if m:
                        k, v = m.group(1), m.group(2).strip()
                        if k == 'tier': tier = v
                        elif k == 'name': name = v
                        elif k == 'email': email_addr = v
                        elif k == 'designation': designation = v
                        elif k == 'subject': old_subject = v
                old_body = parts[2].strip()
            else:
                old_body = content.strip()
        else:
            old_body = content.strip()

        # Strip old HTML tags to get plain text for extraction
        old_text = re.sub(r'<[^>]+>', '', old_body)
        old_text = old_text.replace('&ldquo;', '"').replace('&rdquo;', '"').replace('&rsquo;', "'").replace('&ndash;', '-')

        # Extract bespoke opening and CC
        opening, _ = extract_bespoke_opening(old_text)
        cc = cc_map.get(slug, None)
        if cc:
            cc = ', '.join(cc) if isinstance(cc, list) else str(cc)

        # Determine greeting name
        greeting_name = name  # fallback
        gm = re.match(r'Dear\s+(.+?)(?:,|\.)', old_text)
        if gm:
            greeting_name = gm.group(1).strip()

        # Determine subject line (custom per tier)
        if 'Prime Minister' in greeting_name:
            subject = 'Request for Prime Ministerial Review of PDPC&rsquo;s Non-Enforcement of the PDPA Access Obligation'
        elif 'President' in greeting_name:
            subject = 'The PDPA Access Obligation: A documented pattern for the President&rsquo;s awareness'
        elif tier == 'cs':
            subject = 'The PDPA Access Obligation: A documented enforcement pattern for your attention'
        else:
            subject = 'The PDPA Access Obligation: A documented enforcement pattern for your attention'

        # Determine closing question
        closing_q = ''
        if is_civil_servant:
            closing_q = cs_closing_questions.get(slug, '')
        else:
            closing_q = closing_questions.get(slug, '')
            if not closing_q and tier in ('1', '2'):
                closing_q = 'I respectfully ask that you consider this documented pattern and what, if anything, can be done within your remit to ensure that the Access Obligation is enforced as Parliament intended.'
            elif not closing_q:
                closing_q = 'I respectfully ask that you consider this documented pattern. As a backbencher, your constituents may one day raise questions about their rights under the PDPA, and I want you to have the full picture before that happens.'

        # For Zhulkarnain: preserve full personal narrative as opening
        if slug == 'zhulkarnain-abdul-rahim':
            # The full personal narrative IS the opening
            zhul_opening = (
                'You have been my constituency MP for Chua Chu Kang. '
                'My first email to you on this matter was on 27&nbsp;May&nbsp;2024. '
                'The PDPC&rsquo;s own records, in their replies to me that copied you in, refer to that email. '
                'Since then I have written to you many more times, all on the same subject. '
                'The record of those emails is verifiable.'
            )
            opening = zhul_opening

        # For Tier 1C: first-name only, add disclosure after signature
        include_opening_html = True
        disclosure_html = ''
        if slug in ('kenneth-goh', 'dinesh-vasu-dash', 'cai-yinzhou'):
            # First-name greeting
            if slug == 'kenneth-goh':
                greeting_name = 'Kenneth'
                disclosure_html = '<p style="font-style: italic; color: #666; margin-top: 2em;">You were my SMU professor during my MBA. I want to be transparent: I am writing to you not because of that connection, but because the documented pattern of regulatory conduct speaks for itself. This case stands on its own merits and the publicly available record. I am not asking for any special treatment or favourable outcome. I am asking only that the record be reviewed.</p>'
            elif slug == 'dinesh-vasu-dash':
                greeting_name = 'Dinesh'
                disclosure_html = '<p style="font-style: italic; color: #666; margin-top: 2em;">You were my group director at MOH when I served there during Covid. I want to be clear: I am writing to you not because of that connection, but because the documented pattern speaks for itself. This case stands on its own merits and the publicly available record. I am not asking for any special treatment or favourable outcome. I am asking only that the record be reviewed.</p>'
            elif slug == 'cai-yinzhou':
                greeting_name = 'Yinzhou'
                disclosure_html = '<p style="font-style: italic; color: #666; margin-top: 2em;">We&rsquo;ve known each other since youth. I want to be transparent: I am writing to you not because of that friendship, but because the documented pattern speaks for itself. This case stands on its own merits and the publicly available record. I am not asking for any special treatment or favourable outcome. I am asking only that the record be reviewed.</p>'

        # Build HTML
        html_body = build_html_body(greeting_name, subject, opening, closing_q, cc, include_opening_html)

        # Add disclosure after signature for Tier 1C
        if disclosure_html:
            html_body += '\n\n' + disclosure_html

        full_html = WRAPPER_OPEN + '\n\n' + html_body + WRAPPER_CLOSE

        # Write
        new_content = f'---\ntier: {tier}\nname: {name}\nslug: {slug}\nemail: {email_addr}\ndesignation: {designation}\nsubject: {subject}\n---\n\n{full_html}'
        f.write_text(new_content, encoding='utf-8')
        count += 1

        if count <= 5:
            print(f'  OK {slug}: greeting="{greeting_name}", opening={len(opening)}chars, closing={len(closing_q)}chars')

    return count

# Process both directories
print('=== MP emails ===')
mp_count = process_directory(Path('data/personalised-emails'))

print('\n=== Civil servant emails ===')
cs_count = process_directory(Path('data/personalised-emails-civil-servants'), is_civil_servant=True)

print(f'\nTotal: {mp_count} MP + {cs_count} civil servant = {mp_count + cs_count} files rewritten')
