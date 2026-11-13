# -*- coding: utf-8 -*-
import re, io, glob, os

def read(p):
    return io.open(p, encoding='utf-8').read()

def global_pragma(path):
    t = read(path)
    m = re.search(r'\[GLOBAL_PRAGMA\]([\s\S]*?)(?=\n\[|\Z)', t)
    return (m.group(1).strip().replace('\n', ' | ') if m else '(none)')

def nforms(body):
    tk = re.findall(r'"[^"]*"|\S+', body)
    return len(tk) - (1 if tk and re.fullmatch(r'\d+', tk[0]) else 0)

print('=== TOML census (files containing {G=} / {G } / {P }) ===')
for p in sorted(glob.glob('src/grf/lang/*.toml')):
    t = read(p)
    gequal = sorted(set(re.findall(r'\{G=([^}]*)\}', t)))
    gcons = re.findall(r'\{G\s+([^}]*)\}', t)
    pbodies = re.findall(r'\{P\s+([^}]*)\}', t)
    if not (gequal or gcons or pbodies):
        continue
    gp = global_pragma(p)
    pm = re.search(r'plural\s*=\s*"([^"]*)"', gp)
    print(os.path.basename(p)[:-5], 'plural=' + (pm.group(1) if pm else '?'),
          'G=labels=' + repr(gequal),
          'Gcons=' + repr(gcons[:3]),
          'Pbodies=' + str(len(pbodies)),
          'Pforms=' + repr(sorted(set(nforms(b) for b in pbodies))),
          'pragma=' + repr(gp[:150]))

print()
print('=== generated/lang/*.lng : {G } consumers? ===')
any_cons = False
for p in sorted(glob.glob('generated/lang/*.lng')):
    gcons = re.findall(r'\{G\s+([^}]*)\}', read(p))
    if gcons:
        any_cons = True
        print(os.path.basename(p), repr(gcons[:5]))
print('ANY_CONSUMER', any_cons)

print()
print('=== {P } command samples in the 8 plural-warning languages ===')
bad = ['croatian','czech','gaelic','indonesian','japanese','slovak','traditional_chinese','turkish']
for lang in bad:
    p = 'src/grf/lang/' + lang + '.toml'
    if not os.path.exists(p):
        print(lang, 'NO TOML'); continue
    lines = [l.rstrip('\n') for l in io.open(p, encoding='utf-8') if '{P ' in l]
    gp = global_pragma(p)
    pm = re.search(r'plural\s*=\s*"([^"]*)"', gp)
    print('--- ' + lang + ' plural=' + (pm.group(1) if pm else '?') + ' lines=' + str(len(lines)))
    for l in lines[:7]:
        print('   ', l[:190])
