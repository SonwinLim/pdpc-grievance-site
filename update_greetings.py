import os

ROOT = 'H:/My Drive/Driving Legal Issue/pdpc-grievance-site/data/personalised-emails'
REPLACEMENTS = [
    # Tier 1A
    ('lawrence-wong',           'Dear Mr Lawrence Wong,',           'Dear Prime Minister Lawrence Wong,'),
    ('lee-hsien-loong',         'Dear Mr Lee Hsien Loong,',         'Dear Senior Minister Lee Hsien Loong,'),
    ('gan-kim-yong',            'Dear Mr Gan Kim Yong,',            'Dear Deputy Prime Minister Gan Kim Yong,'),
    ('chan-chun-sing',          'Dear Mr Chan Chun Sing,',          'Dear Coordinating Minister Chan Chun Sing,'),
    ('k-shanmugam',             'Dear Mr K Shanmugam,',             'Dear Coordinating Minister K Shanmugam,'),
    ('josephine-teo',           'Dear Madam Josephine Teo,',         'Dear Minister Josephine Teo,'),
    ('edwin-tong-chun-fai',     'Dear Mr Edwin Tong Chun Fai,',     'Dear Minister Edwin Tong,'),
    ('indranee-rajah',          'Dear Madam Indranee Rajah,',        'Dear Minister Indranee Rajah,'),
    ('seah-kian-peng',          'Dear Mr Seah Kian Peng,',          'Dear Speaker Seah Kian Peng,'),
    ('zhulkarnain-abdul-rahim', 'Dear Mr Zhulkarnain Abdul Rahim,', 'Dear Minister of State Zhulkarnain Abdul Rahim,'),
    # Tier 2
    ('alex-yam-ziming',                       'Dear Mr Alex Yam Ziming,',                       'Dear Mayor Alex Yam Ziming,'),
    ('denise-phua-lay-peng',                  'Dear Ms Denise Phua Lay Peng,',                  'Dear Mayor Denise Phua Lay Peng,'),
    ('christopher-de-souza',                  'Dear Mr Christopher de Souza,',                  'Dear Deputy Speaker Christopher de Souza,'),
    ('xie-yao-quan',                          'Dear Mr Xie Yao Quan,',                          'Dear Deputy Speaker Xie Yao Quan,'),
    ('ong-ye-kung',                           'Dear Mr Ong Ye Kung,',                           'Dear Coordinating Minister Ong Ye Kung,'),
    ('chee-hong-tat',                         'Dear Mr Chee Hong Tat,',                         'Dear Minister Chee Hong Tat,'),
    ('desmond-lee',                           'Dear Mr Desmond Lee,',                           'Dear Minister Desmond Lee,'),
    ('grace-fu-hai-yien',                     'Dear Ms Grace Fu Hai Yien,',                     'Dear Minister Grace Fu Hai Yien,'),
    ('masagos-zulkifli-bin-masagos-mohamad',  'Dear Mr Masagos Zulkifli Bin Masagos Mohamad,',  'Dear Minister Masagos Zulkifli,'),
    ('tan-see-leng',                          'Dear Dr Tan See Leng,',                          'Dear Minister Tan See Leng,'),
    ('vivian-balakrishnan',                   'Dear Dr Vivian Balakrishnan,',                   'Dear Minister Vivian Balakrishnan,'),
    ('david-neo',                             'Dear Mr David Neo,',                             'Dear Acting Minister David Neo,'),
    ('muhammad-faishal-ibrahim',              'Dear Assoc Prof Dr Muhammad Faishal Ibrahim,',  'Dear Acting Minister Muhammad Faishal Ibrahim,'),
    ('jeffrey-siow',                          'Dear Mr Jeffrey Siow,',                          'Dear Acting Minister Jeffrey Siow,'),
    ('alvin-tan-sheng-hui',                   'Dear Mr Alvin Tan,',                             'Dear Minister of State Alvin Tan,'),
    ('baey-yam-keng',                         'Dear Ms Baey Yam Keng,',                         'Dear Minister of State Baey Yam Keng,'),
    ('desmond-choo',                          'Dear Mr Desmond Choo,',                          'Dear Minister of State Desmond Choo,'),
    ('gan-siow-huang',                        'Dear Ms Gan Siow Huang,',                        'Dear Minister of State Gan Siow Huang,'),
    ('goh-pei-ming',                          'Dear Mr Goh Pei Ming,',                          'Dear Minister of State Goh Pei Ming,'),
    ('jasmin-lau',                            'Dear Ms Jasmin Lau,',                            'Dear Minister of State Jasmin Lau,'),
    ('rahayu-mahzam',                         'Dear Ms Rahayu Mahzam,',                         'Dear Minister of State Rahayu Mahzam,'),
    ('desmond-tan-kok-ming',                  'Dear Mr Desmond Tan,',                           'Dear Senior Minister of State Desmond Tan,'),
    ('janil-puthucheary',                     'Dear Dr Janil Puthucheary,',                     'Dear Senior Minister of State Janil Puthucheary,'),
    ('low-yen-ling',                          'Dear Ms Low Yen Ling,',                          'Dear Senior Minister of State Low Yen Ling,'),
    ('murali-pillai',                         'Dear Mr Murali Pillai,',                         'Dear Senior Minister of State Murali Pillai,'),
    ('sim-ann',                               'Dear Ms Sim Ann,',                               'Dear Senior Minister of State Sim Ann,'),
    ('sun-xueling',                           'Dear Ms Sun Xueling,',                           'Dear Senior Minister of State Sun Xueling,'),
    ('tan-kiat-how',                          'Dear Mr Tan Kiat How,',                          'Dear Senior Minister of State Tan Kiat How,'),
    ('zaqy-mohamad',                          'Dear Mr Zaqy Mohamad,',                          'Dear Senior Minister of State Zaqy Mohamad,'),
    ('eric-chua-swee-leong',                  'Dear Mr Eric Chua,',                             'Dear Senior Parliamentary Secretary Eric Chua,'),
    ('goh-han-yan',                           'Dear Ms Goh Hanyan,',                            'Dear Senior Parliamentary Secretary Goh Hanyan,'),
    ('shawn-huang-wei-zhong',                 'Dear Mr Shawn Huang Wei Zhong,',                 'Dear Senior Parliamentary Secretary Shawn Huang Wei Zhong,'),
    ('syed-harun-alhabsyi',                   'Dear Mr Syed Harun Alhabsyi,',                   'Dear Senior Parliamentary Secretary Syed Harun Alhabsyi,'),
    ('kuah-boon-theng',                       'Dear Ms Kuah Boon Theng,',                       'Dear Nominated Member of Parliament Kuah Boon Theng,'),
]

not_found = []
old_not_found = []
count = 0

for slug, old, new in REPLACEMENTS:
    path = os.path.join(ROOT, slug + '.md')
    if not os.path.exists(path):
        not_found.append(slug)
        print(f"NOT FOUND: {slug}")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if old not in content:
        old_not_found.append((slug, old))
        print(f"OLD NOT FOUND in {slug}: {old!r}")
        continue
    new_content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    count += 1
    print(f"OK: {slug}")

print(f"\nUpdated {count} files")
if not_found:
    print(f"NOT FOUND: {not_found}")
if old_not_found:
    print(f"OLD NOT FOUND: {old_not_found}")
