#!/usr/bin/env python3
"""Build a unified rebrand/residue fix candidate list with work-index mapping."""
import importlib.util, json, glob, os, re
from collections import Counter
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
lm = p.lang_map(); extras = p.extra_files(lm)
# English values map: file::key -> (en, ph)
EN = {}
for l in ["french"]:
    for grp, tgt, ref in p.targets(l, lm, extras):
        e = p.leaves(p.load(R/ref))
        for k, ev in e.items(): EN[tgt+"::"+k] = ev
# work index map: lang::file::key -> index
WIDX = {}
for f in glob.glob("tools/_i18n_work/*.json"):
    l = os.path.basename(f)[:-5]
    w = json.load(open(f, encoding="utf-8"))
    for i, e in enumerate(w.get("entries", [])):
        for rf in e.get("refs", []):
            WIDX[l+"::"+rf[0]+"::"+rf[1]] = i
reb = json.load(open("tools/_i18n_rebrand.json", encoding="utf-8"))
res = json.load(open("tools/_i18n_residue_all.json", encoding="utf-8"))
cand = {}
def add(l, file, key, reasons):
    kk = l+"::"+file+"::"+key
    if kk in cand:
        cand[kk]["reasons"] = sorted(set(cand[kk]["reasons"] + reasons))
        return
    ev = EN.get(file+"::"+key)
    if ev is None: return
    tv = None
    for grp, tgt, ref in p.targets(l, lm, extras):
        if tgt == file: tv = p.leaves(p.load(R/tgt)).get(key); break
    if tv is None: return
    cand[kk] = {"lang":l,"file":file,"key":key,"en":ev,"tr":tv,"reasons":sorted(set(reasons)),
                "work_index":WIDX.get(kk),"in_work":kk in WIDX}
for s in reb["stale"]: add(s["lang"], s["file"], s["key"], s["reasons"])
for s in reb["case_only"]: add(s["lang"], s["file"], s["key"], ["english_case_only"])
for t in res["targeted"]:
    if t["pattern"] in ("upstream","old_firs_name","na_city_param","conflicting_newgrfs"):
        add(t["lang"], t["file"], t["key"], [t["pattern"]])
out = sorted(cand.values(), key=lambda x:(x["lang"], x["file"], x["key"]))
json.dump(out, open("tools/_i18n_rebrand_candidates.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("candidates", len(out), "in_work", sum(1 for c in out if c["in_work"]), "not_in_work", sum(1 for c in out if not c["in_work"]))
print("langs", json.dumps(dict(Counter(c["lang"] for c in out))))
print("reasons", json.dumps(dict(Counter(r for c in out for r in c["reasons"]))))
print("keys", json.dumps(dict(Counter(c["key"] for c in out))))
