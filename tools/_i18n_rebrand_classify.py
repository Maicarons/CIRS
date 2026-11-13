#!/usr/bin/env python3
"""Classify rebrand candidates; compute deterministic FIRS->CIRS fixes; emit task files."""
import json, re
from collections import Counter
c = json.load(open("tools/_i18n_rebrand_candidates.json", encoding="utf-8"))
# safe brand substitution: FIRS not adjacent to a Latin letter (so FIRST / FIRSX are untouched)
BR = re.compile(r"(?<![A-Za-z])FIRS(?![A-Za-z])")
PH = re.compile(r"\{([A-Za-z_0-9]*)\}")
from collections import Counter as C
def ph(v): return C(PH.findall(v))
det, restore, retr = [], [], []
for x in c:
    en, tr = x["en"], x["tr"]
    ef, tf = len(re.findall("FIRS", en)), len(re.findall("FIRS", tr))
    ec, tc = len(re.findall("CIRS", en)), len(re.findall("CIRS", tr))
    # phase 1: English has CIRS and no FIRS -> every FIRS in target is stale brand
    if ec > 0 and ef == 0 and tf > 0:
        nv = BR.sub("CIRS", tr)
        if ph(nv) == ph(en) and "FIRS" not in nv.replace("CIRS",""):
            det.append({**x, "new_tr": nv})
            continue
    # phase 2: 2-letter cargo id codes -> restore English code (brand injection artifact)
    if x["key"].endswith(".cid") and re.match(r"^\{TINYFONT\}[A-Za-z0-9]{1,8}$", en.strip()):
        restore.append({**x, "new_tr": en})
        continue
    # phase 3: full retranslation from current English
    retr.append(x)
json.dump({"deterministic":det,"restore":restore,"retranslate":retr},
          open("tools/_i18n_rebrand_tasks.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("deterministic", len(det), "restore", len(restore), "retranslate", len(retr))
print("retr keys", json.dumps(dict(Counter(x["key"] for x in retr))))
print("retr langs", json.dumps(dict(Counter(x["lang"] for x in retr))))
print("retr in_work", sum(1 for x in retr if x["in_work"]), "not_in_work", sum(1 for x in retr if not x["in_work"]))
# duplicate work indices among all direct fixes (must be consistent)
allfix = det+restore+retr
wi = {}
for x in allfix:
    if x["work_index"] is not None: wi.setdefault(x["lang"]+"::"+str(x["work_index"]), []).append(x)
dups = {k:v for k,v in wi.items() if len(v)>1}
print("work_index_duplicates", len(dups))
for k,v in list(dups.items())[:10]: print("   ", k, [z["file"]+"::"+z["key"] for z in v])
