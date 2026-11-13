# -*- coding: utf-8 -*-
import os, re, io, glob, json, collections
NUM = {0:2,1:1,2:2,3:3,4:5,5:3,6:3,7:3,8:4,9:2,10:3,11:2,12:4,13:4,14:3}
PCMD = re.compile(r"\{P\s+([^}]*)\}")
GCMD = re.compile(r"\{G=([^}]*)\}")
ASSIGN = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')

def toks(body):
    b = body.replace('\\"', '"')
    t = re.findall(r'"[^"]*"|\S+', b)
    if t and re.fullmatch(r"\d+", t[0]): t = t[1:]
    return t

# authoritative 4x gender headers
G4 = {}
for p in glob.glob("tools/_4x_ref/*.lng"):
    for l in io.open(p, encoding="utf-8", errors="replace"):
        if l.startswith("##gender"):
            G4[os.path.basename(p)[:-4]] = l.strip().split(" ",1)[1].split()
            break

changes = collections.defaultdict(dict)   # lang -> key -> newvalue
genders = {}
for p in sorted(glob.glob("src/grf/lang/*.toml")):
    lang = os.path.basename(p)[:-5]
    txt = io.open(p, encoding="utf-8").read()
    lines = txt.split("\n")
    m = re.search(r"\[GLOBAL_PRAGMA\]([\s\S]*?)(?=\n\[|\Z)", txt)
    pm = re.search(r'plural\s*=\s*"([^"]*)"', m.group(1) if m else "")
    N = NUM[int(pm.group(1))] if pm else 2
    glabels = sorted(set(GCMD.findall(txt)))
    if glabels:
        hdr = G4.get(lang, [])
        missing = [g for g in glabels if g not in hdr]
        genders[lang] = (glabels, hdr, missing)
    sec = ""
    for i, ln in enumerate(lines):
        ms = SECTION.match(ln)
        if ms: sec = ms.group(1); continue
        a = ASSIGN.match(ln)
        if not a: continue
        val = a.group(4)
        def fix(mo):
            b = mo.group(1)
            return "" if len(toks(b)) != N else mo.group(0)
        new = PCMD.sub(fix, val)
        if new != val:
            raw = val[1:-1].replace('\\"','"').replace('\\\\','\\')
            newraw = new[1:-1].replace('\\"','"').replace('\\\\','\\')
            key = (sec + "." + a.group(2)) if sec else a.group(2)
            changes[lang][key] = (raw, newraw)

print("=== GENDER label validation ===")
for l,(g,h,m) in sorted(genders.items()):
    print(l, "used="+repr(g), "4x="+repr(h), "MISSING="+repr(m))
print()
print("=== P changes per lang ===")
tot=0
for l,d in sorted(changes.items()):
    print(l, len(d), list(d)[:4]); tot+=len(d)
print("TOTAL", tot)

print()
print("=== work-ref coverage for changed keys ===")
conflict=[]; nref=0; mixed=[]; safe=0
for l,d in sorted(changes.items()):
    wp = "tools/_i18n_work/" + l + ".json"
    if not os.path.exists(wp):
        print(l, "NO_WORK_FILE"); continue
    W = json.load(io.open(wp, encoding="utf-8")); ents = W["entries"]
    ref2i = {}
    for i,e in enumerate(ents):
        for rf in e.get("refs",[]):
            ref2i[(rf[0].replace("\\","/").lstrip("./"), rf[1])] = i
    for k,(old,new) in d.items():
        f = "src/grf/lang/" + l + ".toml"
        i = ref2i.get((f,k))
        if i is None: nref+=1; continue
        refs = ents[i].get("refs",[])
        desired = []
        for rf in refs:
            rk = (rf[0].replace("\\","/").lstrip("./"), rf[1])
            desired.append(d.get(rk[1], (None,None))[1] if rk in [(f,x) for x in d] else None)
        if len(refs)==1: safe+=1
        else:
            # all refs must be changed keys with same new value
            allc = all((f, r[1]) in [(f,x) for x in d] for r in refs)
            vals = [d[r[1]][1] for r in refs if r[1] in d]
            if allc and len(set(vals))==1: safe+=1
            else: mixed.append((l,k,i,[r[1] for r in refs]))
print("NO_WORK_REF", nref, "SAFE", safe, "MIXED", len(mixed))
for x in mixed[:15]: print("  MIXED", x)
