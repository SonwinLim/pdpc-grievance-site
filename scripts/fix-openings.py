import re, json, subprocess
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

openings = {
    'josephine-teo': ('Minister Josephine Teo',
        'Your Written Answer 19596, delivered in Parliament on 22 September 2025, stated that organisations must preserve data while access requests are being processed, and that criminal penalties apply for intentional concealment. That assurance is on the Parliamentary record. The documentary record now shows that PDPC has not once found a breach of the Access Obligation across its published enforcement history. I am writing to ask whether your office still stands by those assurances.'
    ),
    'lawrence-wong': ('Prime Minister Lawrence Wong',
        'I respectfully request a Prime Ministerial review of PDPC\'s non-enforcement of the PDPA Access Obligation.'
    ),
    'chan-chun-sing': ('Coordinating Minister Chan Chun Sing',
        'As Coordinating Minister for Public Services, your office oversees the public service institutions involved in this matter. When I approached the Public Service Commission, IMDA represented to PSC that the issues had been addressed at a time when no substantive reply had been provided to me. PSC relied on that representation. I am writing to flag a documented pattern that warrants your attention.'
    ),
    'edwin-tong-chun-fai': ('Minister Edwin Tong',
        'As Minister for Law, your portfolio includes the statutory interpretation of Acts of Parliament. PDPC wrote to me that its Advisory Guidelines are not determinative and that the PDPA takes precedence, while refusing to identify which guideline, which clause, or which conflict was meant. It then used those same Guidelines as the basis for a finding against me. I am writing to ask whether the Law Ministry will review this.'
    ),
    'gan-kim-yong': ('Deputy Prime Minister Gan Kim Yong',
        'As Deputy Prime Minister, your office has visibility over the whole of government. The documented pattern at pdpaaccessrights.sg concerns whether a statutory right given to all Singaporeans is being enforced in practice. I am writing because every internal channel has been exhausted without a substantive reply.'
    ),
    'indranee-rajah': ('Minister Indranee Rajah',
        'As Minister in the Prime Minister\'s Office and Leader of the House, you hold both Cabinet rank and procedural authority over parliamentary business. The documented pattern at pdpaaccessrights.sg concerns whether the PDPA\'s Access Obligation is being enforced. I am writing to ask whether this matter can be raised through Parliamentary channels.'
    ),
    'k-shanmugam': ('Coordinating Minister K Shanmugam',
        'As Coordinating Minister for National Security and Minister for Home Affairs, your portfolio engages both the public safety dimension of CCTV evidence and the legal framework under which that evidence is governed. The documented pattern at pdpaaccessrights.sg reveals a regulatory posture that effectively excludes CCTV footage from the Access Obligation. I am writing to flag this for your attention.'
    ),
    'lee-hsien-loong': ('Senior Minister Lee Hsien Loong',
        'The PDPA was enacted in 2012 under your Government. Its plain text grants a right of access to personal data. The documented pattern at pdpaaccessrights.sg shows that right has never produced a published breach finding across PDPC\'s entire enforcement record. I am writing to ask whether the statute as enforced still matches the statute as enacted.'
    ),
    'seah-kian-peng': ('Speaker Seah Kian Peng',
        'As Speaker of Parliament, you hold the procedural authority over what matters are raised in the House. The documented pattern at pdpaaccessrights.sg concerns whether a statutory right granted by Parliament is being enforced. I am writing to ask whether the procedural channels of the House can accommodate this question.'
    ),
    'zhulkarnain-abdul-rahim': ('Minister of State Zhulkarnain Abdul Rahim',
        'You have been my constituency MP for Chua Chu Kang. My first email to you on this matter was on 27 May 2024. The PDPC\'s own records, in their replies to me that copied you in, refer to that email. Since then I have written to you many more times, all on the same subject. The record of those emails is verifiable.'
    ),
}

for slug, (greeting, opening_text) in openings.items():
    src = f'data/personalised-emails/{slug}.md'
    content = Path(src).read_text(encoding='utf-8')
    m = re.search(r'Dear <strong>([^<]+)</strong>', content)
    if m:
        content = content.replace(f'Dear <strong>{m.group(1)}</strong>', f'Dear <strong>{greeting}</strong>', 1)
    target = '</h2>\n\n<h2>Why this is a public issue</h2>'
    if target in content and opening_text:
        content = content.replace(target, f'</h2>\n\n<p>{opening_text}</p>\n\n<h2>Why this is a public issue</h2>', 1)
    Path(src).write_text(content, encoding='utf-8')
    print(f'Fixed {slug}: {greeting}')

# Tier 1C: first-name-only
for slug, fname in {'kenneth-goh':'Kenneth','dinesh-vasu-dash':'Dinesh','cai-yinzhou':'Yinzhou'}.items():
    src = f'data/personalised-emails/{slug}.md'
    content = Path(src).read_text(encoding='utf-8')
    m = re.search(r'Dear <strong>([^<]+)</strong>', content)
    if m:
        content = content.replace(f'Dear <strong>{m.group(1)}</strong>', f'Dear <strong>{fname}</strong>', 1)
        Path(src).write_text(content, encoding='utf-8')
        print(f'Fixed {slug} -> {fname}')

# Send 4 samples
print('\nSending...')
GWS = r'C:\Users\limzi\AppData\Roaming\npm\node_modules\@googleworkspace\cli\bin\gws.exe'
img_data = Path('conclusion-flow.jpeg').read_bytes()

for slug, label in [('josephine-teo','MINISTER'),('lawrence-wong','PM'),('zhulkarnain-abdul-rahim','MY-MP'),('kenneth-goh','TIER1C')]:
    parts = Path(f'data/personalised-emails/{slug}.md').read_text(encoding='utf-8').split('---\n', 2)
    html_body = parts[2].strip()

    outer = MIMEMultipart('mixed')
    outer['From'] = 'limzirui@gmail.com'; outer['To'] = 'limzirui@gmail.com'
    outer['Subject'] = f'SAMPLE v4 final: {label}'

    inner = MIMEMultipart('related')
    alt = MIMEMultipart('alternative')
    alt.attach(MIMEText(html_body, 'html', 'utf-8'))
    inner.attach(alt)

    img = MIMEImage(img_data)
    img.add_header('Content-ID', '<conclusion-flow>')
    img.add_header('Content-Disposition', 'inline', filename='conclusion-flow.jpeg')
    inner.attach(img)
    outer.attach(inner)

    for fn in ['BreachBreakdown.jpg','entry-gate-overlay.jpg','pdpa-masking-42.png','hansard.jpg']:
        if Path(fn).exists():
            with open(fn,'rb') as fp:
                a = MIMEImage(fp.read())
            a.add_header('Content-Disposition','attachment',filename=fn)
            outer.attach(a)

    outpath = Path(f'data/v4-{slug}.eml')
    outpath.write_bytes(outer.as_bytes())
    r = subprocess.run([GWS,'gmail','users','messages','send','--params',json.dumps({'userId':'me'}),'--upload',str(outpath.resolve()),'--upload-content-type','message/rfc822'],capture_output=True,text=True,timeout=120)
    print(f'{slug}: id={json.loads(r.stdout).get("id","?")}')

print('done')
