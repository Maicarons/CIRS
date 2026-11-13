# -*- coding: utf-8 -*-
import os, re, io, glob, json

print("=== work JSON format ===")
w = sorted(glob.glob("tools/_i18n_work/*.json"))
print("count", len(w), "sample", w[0] if w else None)
if w:
    d = json.load(io.open(w[0], encoding="utf-8"))
    print("type", type(d).__name__, "len", len(d))
    print("first", json.dumps(d[0] if isinstance(d, list) else list(d.items())[0], ensure_ascii=False)[:400])

print()
print("=== out-JSONL format ===")
o = sorted(glob.glob("tools/_i18n_out/*.jsonl"))
print("count", len(o), "sample", o[0] if o else None)
if o:
    lines = io.open(o[0], encoding="utf-8").read().splitlines()
    print("first2", [x[:300] for x in lines[:2]])

NUM = {0:2,1:1,2:2,3:3,4:5,5:3,6:3,7:3,8:4,9:2,10:3,11:2,12:4,13:4,14:3}
PCMD = re.compile(r"\{P\s+([^}]*)\}")

def toks(body):
    b = body.replace('\\"', '"')
    t = re.findall(r'"[^"]*"|\S+', b)
    if t and re.fullmatch(r"\d+", t[0]):
        t = t[1:]
    return t

print()
print("=== {P} bodies per language (N = required arg count) ===")
for p in sorted(glob.glob("src/grf/lang/*.toml")):
    t = io.open(p, encoding="utf-8").read()
    m = re.search(r"\[GLOBAL_PRAGMA\]([\s\S]*?)(?=\n\[|\Z)", t)
    pm = re.search(r'plural\s*=\s*"([^"]*)"', m.group(1) if m else "")
    plural = int(pm.group(1)) if pm else 0
    N = NUM[plural]
    bodies = PCMD.findall(t)
    if not bodies:
        continue
    lang = os.path.basename(p)[:-5]
    info = [(b.strip(), len(toks(b))) for b in bodies]
    bad = [(b, n) for b, n in info if n != N]
    print(lang, "plural=" + str(plural), "N=" + str(N), "P=" + str(len(bodies)),
          "keep=" + str(len(info) - len(bad)), "remove=" + str(len(bad)),
          "samples=" + repr([x[0][:52] for x in bad[:3]]))

print()
print("=== {G=} position check in generated .lng (must be at start of value) ===")
for p in sorted(glob.glob("generated/lang/*.lng")):
    lines = io.open(p, encoding="utf-8").read().splitlines()
    bad = []
    for i, l in enumerate(lines, 1):
        if "{G=" in l and ":" in l:
            val = l.split(":", 1)[1].lstrip()
            if not val.startswith("{G="):
                bad.append((i, val[:70]))
    if bad:
        print(os.path.basename(p), "NOT_AT_START", len(bad), repr(bad[:3]))
print("done")
