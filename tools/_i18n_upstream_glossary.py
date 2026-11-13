#!/usr/bin/env python3
"""Dump DOC_HOME_WHY_3_TITLE/_DESC from every language TOML as glossary hints."""
import tomllib, glob, io, os
o = io.StringIO()
for f in sorted(glob.glob('src/docs/lang/*.toml')):
    lang = os.path.basename(f)[:-5]
    d = tomllib.load(open(f,'rb'))
    o.write(lang+'\n')
    o.write('  TITLE: '+str(d.get('DOC_HOME_WHY_3_TITLE',''))+'\n')
    o.write('  DESC : '+str(d.get('DOC_HOME_WHY_3_DESC',''))+'\n')
open('tools/_i18n_upstream_glossary.txt','w',encoding='utf-8').write(o.getvalue())
print('wrote', len(o.getvalue()))
