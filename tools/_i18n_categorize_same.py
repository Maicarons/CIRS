import re, collections
lines = [l.strip() for l in open('tools/_i18n_same_real.txt', encoding='utf-8') if l.strip()]
PH = re.compile(r'\{[A-Za-z_0-9]*\}')
tmpl, wordy = [], []
for l in lines:
    lang, grp, key, en = l.split('|', 3)
    residue = PH.sub('', en).strip()
    (tmpl if not re.search(r'[A-Za-z]{3,}', residue) else wordy).append((lang, grp, key, en))
print('TOTAL', len(lines), 'pure_template_no_words=', len(tmpl), 'has_translatable_words=', len(wordy))
c = collections.Counter(en for _,_,_,en in wordy)
print('UNIQUE wordy values:', len(c))
for v, n in c.most_common(): print(f'{n:3d}  {v}')
