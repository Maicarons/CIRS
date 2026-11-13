#!/usr/bin/env python3
"""Build a unified rebrand/residue fix candidate list with work-index mapping."""
import json, glob, os
from collections import Counter
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
def add(l, file, key, en, tr, reasons):
    kk = l+"::"+file+"::"+key
    if kk in cand:
        cand[kk]["reasons"] = sorted(set(cand[kk]["reasons"] + reasons))
        return
    cand[kk] = {"lang":l,"file":file,"key":key,"en":en,"tr":tr,"reasons":sorted(set(reasons)),
                "work_index":WIDX.get(kk),"in_work":kk in WIDX}
for s in reb["stale"]: add(s["lang"], s["file"], s["key"], s["en"], s["tr"], s["reasons"])
for s in reb["case_only"]: add(s["lang"], s["file"], s["key"], s["en"], s["tr"], ["english_case_only"])
for t in res["targeted"]:
    if t["pattern"] in ("upstream","old_firs_name","na_city_param","conflicting_newgrfs"):
        add(t["lang"], t["file"], t["key"], t["en"], t["tr"], [t["pattern"]])
out = sorted(cand.values(), key=lambda x:(x["lang"], x["file"], x["key"]))
json.dump(out, open("tools/_i18n_rebrand_candidates.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("candidates", len(out), "in_work", sum(1 for c in out if c["in_work"]), "not_in_work", sum(1 for c in out if not c["in_work"]))
print("langs", json.dumps(dict(Counter(c["lang"] for c in out))))
print("reasons", json.dumps(dict(Counter(r for c in out for r in c["reasons"]))))
print("keys", json.dumps(dict(Counter(c["key"] for c in out))))
