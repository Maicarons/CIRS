#!/usr/bin/env python3
"""Cross-language consistency + consensus analysis for same-form English leftovers."""
import importlib.util, json, re
from collections import Counter, defaultdict
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
CARGO_CODE = re.compile(r"^{[A-Za-z_0-9]*}[A-Z0-9]{1,5}$")
BRAND = re.compile(r"^(FIRS|CIRS|OpenTTD|FRAX|NewGRF|GRFID|GPL\(v2\)|Python 3\.11\+|ID|LAND|STSW|CB|CABBAGE|Mild Mild West|BaNaNas|NML|JSON|TOML|makefile|GitHub|Issue|pull request|Total Town Replacement Set|OpenGFX|Windows|macOS|Linux|Unix|Xcode|git|fork|ports tree)([ .]?)$", re.I)
WORDY = re.compile(r"[A-Za-z]{3,}")
def eligible(en):
    s = en.strip()
    if p.placeholder_only(s): return False
    if CARGO_CODE.match(s): return False
    if BRAND.match(s): return False
    if not WORDY.search(s): return False
    return True
lm = p.lang_map(); extras = p.extra_files(lm)
langs = sorted(k for k in lm if k != "english")
slots = defaultdict(lambda: defaultdict(list))
for l in langs:
    for grp, tgt, ref in p.targets(l, lm, extras):
        en = p.leaves(p.load(R / ref)); tv = p.leaves(p.load(R / tgt))
        for k, ev in en.items():
            if p.SKIP_KEY.match(k) or not eligible(ev): continue
            v = tv.get(k)
            if v is None: continue
            slots[l][ev].append((tgt, k, v))
incons = []
for l in langs:
    for ev, items in slots[l].items():
        same = [(f,k) for f,k,v in items if v == ev]
        diff = [v for f,k,v in items if v != ev and p.ph(v) == p.ph(ev)]
        if same and diff:
            best = Counter(diff).most_common(1)[0][0]
            for f,k in same: incons.append({"lang":l,"file":f,"key":k,"en":ev,"tr":best})
cons = []
for l in langs:
    for ev, items in slots[l].items():
        if not all(v == ev for f,k,v in items): continue
        others = []; total = 0
        for l2 in langs:
            if l2 == l or ev not in slots[l2]: continue
            total += 1
            for f,k,v in slots[l2][ev]:
                if v != ev and p.ph(v) == p.ph(ev):
                    others.append((l2, v)); break
        if total and len(others)/total >= 0.6:
            cons.append({"lang":l,"en":ev,"others":len(others),"total":total,
                         "refs":[{"file":f,"key":k} for f,k,v in items],
                         "examples":[{"lang":a,"tr":b} for a,b in others[:4]]})
out = {"inconsistency": incons, "consensus": cons,
       "stats": {"languages":len(langs), "unique_en":len(set(e for l in langs for e in slots[l])),
                 "inconsistency_count":len(incons), "consensus_count":len(cons),
                 "consensus_langs":len(set(c["lang"] for c in cons))}}
open("tools/_i18n_consensus.json","w",encoding="utf-8").write(json.dumps(out,ensure_ascii=False,indent=1))
print(json.dumps(out["stats"],ensure_ascii=False))
print("INCONS_SAMPLE",json.dumps(incons[:8],ensure_ascii=False)[:1200])
print("CONS_SAMPLE",json.dumps(cons[:6],ensure_ascii=False)[:1600])
