import re
from pathlib import Path

# Load shared sections from existing email
sample = Path('data/personalised-emails/josephine-teo.md').read_text(encoding='utf-8')

def extract_section(content, name):
    m = re.search(r'<h2>' + re.escape(name) + r'</h2>(.*?)(?=<h2>|</body)', content, re.DOTALL)
    return '<h2>' + name + '</h2>' + m.group(1) if m else ''

REVISITED = extract_section(sample, 'What caused me to revisit this issue')
MARADONA = extract_section(sample, 'The Maradona &ldquo;Hand of God&rdquo; analogy')
WHY = extract_section(sample, 'Why this matters')
FACTS = extract_section(sample, 'Where the full facts are documented')
SITES = extract_section(sample, 'Sites for verification')
ATTACHMENTS = extract_section(sample, 'Attachments')

# Also extract the PDPC/IMDA no-reply sentence
# It's a standalone p after the revisited section. We'll keep it in REVISITED.

CLOSING = (
    '<p>My complaints were the only ones where PDPC were compelled to investigate, '
    'after considerable effort including reading the laws and guidelines myself and filing appeals, '
    'and still no Access Obligation breaches were found. Imagine how many Singaporeans and residents '
    'in Singapore were told by PDPC, in effect, that their rights under the PDPA could not be exercised. '
    'After all the pain I have been through, it is my mission to make sure that other Singaporeans and '
    'residents will not suffer what I went through.</p>\n\n'
    '<p>Yours sincerely,<br>Ray Lim</p>'
)

CSS = (
    '<body style="font-family: Arial, Helvetica, sans-serif; font-size: 16px; max-width: 640px; '
    'margin: 0 auto; padding: 20px; color: #222; line-height: 1.5;">\n'
    '<style>\n'
    'p { margin-bottom: 0.9em; }\n'
    'h2 { font-size: 1.15em; margin-top: 1.6em; margin-bottom: 0.6em; }\n'
    'li { margin-bottom: 0.6em; }\n'
    'ol { margin-bottom: 1em; }\n'
    '</style>'
)

WRAPPER_OPEN = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n</head>\n' + CSS + '\n'
WRAPPER_CLOSE = '\n</body>\n</html>'

servants = [
    ('mddi-ps-chng', 'CHNG Kai Fong', 'Permanent Secretary (MDDI)', 'CHNG_Kai_Fong@mddi.gov.sg',
     'As Permanent Secretary at the Ministry of Digital Development and Information, you are the most senior civil servant in the ministry that directly oversees the Personal Data Protection Commission. I am writing to you because the internal and regulatory channels have not produced a substantive response, and the public record itself has been made harder to scrutinise.',
     'I am asking whether your office will review the documented pattern and consider what internal steps are available to ensure that the Access Obligation is enforced as Parliament intended.'),
    ('mddi-2ps-foo', 'FOO Chi Hsia', 'Second Permanent Secretary (Digital Development), MDDI', 'FOO_Chi_Hsia@mfa.gov.sg',
     'As Second Permanent Secretary for Digital Development at MDDI, your portfolio covers the policy and regulatory space in which PDPC operates. I am writing to you because the documented pattern raises questions that cut across policy and enforcement.',
     'I am asking whether the policy implications of the documented zero-Access-Obligation-enforcement record warrant review within the Ministry.'),
    ('mddi-2ps-wong', 'WONG Kang Jet', 'Second Permanent Secretary (Information), MDDI', 'WONG_Kang_Jet@mddi.gov.sg',
     'As Second Permanent Secretary for Information at MDDI, your portfolio includes the information and media policy space. The public\'s ability to verify enforcement data is an information-access issue as much as a data-protection one. I am writing because the obligation-type filter was removed from the public enforcement decisions page after I raised the zero-Access-Obligation pattern.',
     'I am asking whether the removal of the obligation-type filter from the public enforcement-decisions page is consistent with the Ministry\'s information-access objectives.'),
    ('pmo-ps-chan', 'CHAN Heng Kee', 'Permanent Secretary (PMO)', 'Chan_Heng_Kee@pmo.gov.sg',
     'As Permanent Secretary at the Prime Minister\'s Office, you serve at the centre of government. I am writing to you because this matter has been escalated through every available channel without a substantive reply, and the pattern now documented at pdpaaccessrights.sg warrants review at the centre.',
     'I am asking whether this matter warrants internal review at the PMO level, given that every other channel has been exhausted.'),
    ('istana-pps', 'Zed TEO', 'Principal Private Secretary to the President', 'zed_teo@istana.gov.sg',
     'As Principal Private Secretary to the President, you serve in the office that holds the constitutional reserve powers. I am writing to you because the documented pattern raises questions about whether a statutory right has been rendered ineffective in practice, and the executive channels have not produced a substantive response.',
     'I am asking that the President\'s office be aware of the documented pattern, in the event that constitutional questions arise regarding the enforcement of statutory rights under the PDPA.'),
    # Add PDPC Commissioner
    ('pdpc-commissioner', 'Commissioner, PDPC', 'Commissioner, Personal Data Protection Commission', 'info@pdpc.gov.sg',
     'I am writing to you in your capacity as Commissioner of the Personal Data Protection Commission. Your office is the subject of the documented pattern at pdpaaccessrights.sg. I write not to relitigate my individual case, which is closed, but to flag three systemic findings that I believe warrant the Commission\'s own internal review.',
     'I am asking whether the Commission will conduct its own review of the documented pattern, and whether it will address the question of why zero Access Obligation breach findings have been recorded across the entirety of its published enforcement history.'),
]

dir = Path('data/personalised-emails-civil-servants')
dir.mkdir(exist_ok=True)

for slug, name, title, email, opening, closing in servants:
    html_parts = []
    html_parts.append(f'<h2 style="font-weight: normal; margin-bottom: 1.2em;">Dear <strong>{title} {name}</strong>,</h2>')
    html_parts.append(f'<p>{opening}</p>')
    html_parts.append(REVISITED)
    html_parts.append(MARADONA)
    html_parts.append(WHY)
    html_parts.append(FACTS)
    html_parts.append('<h2>What I am asking</h2>')
    html_parts.append(f'<p>{closing}</p>')
    html_parts.append(SITES)
    html_parts.append(ATTACHMENTS)
    html_parts.append(CLOSING)

    full_html = WRAPPER_OPEN + '\n\n'.join(html_parts) + WRAPPER_CLOSE

    frontmatter = f'---\ntier: cs\nname: {name}\nslug: {slug}\nemail: {email}\ndesignation: {title}\nsubject: Follow-up on the PDPC grievance, an update and a request for your attention\n---\n\n'
    (dir / f'{slug}.md').write_text(frontmatter + full_html, encoding='utf-8')

print(f'Created {len(servants)} civil servant emails in {dir}')
for slug, name, title, email, opening, closing in servants:
    print(f'  {slug} -> {email}')
