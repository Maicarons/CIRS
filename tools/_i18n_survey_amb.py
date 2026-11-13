#!/usr/bin/env python3
import importlib.util, json, re, glob
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
keys = ["DOC_BRAND","DOC_CC_OPEN_BULK","DOC_ECO_CARGOS","DOC_ECO_INDUSTRIES","DOC_GS_CONFLICTS_P3_LINK","STR_GRF_NAME.base","STR_CARGO_FOOD_ADDITIVES.cid"]
lm = p.lang_map(); extras = p.extra_files(lm)
res = {k:{} for k in keys}
# English values
en0 = {}
for grp, tgt, ref in p.targets("french", lm, extras):
    e = p.leaves(p.load(R/ref))
    for k in keys:
        if k in e: en0[k]=e[k]
print("ENGLISH", json.dumps(en0, ensure_ascii=False))
for l in sorted(k for k in lm if k!="english"):
    for grp, tgt, ref in p.targets(l, lm, extras):
        tv = p.leaves(p.load(R/tgt))
        for k in keys:
            if k in tv: res[k][l]=tv[k]
for k in keys:
    print("=== "+k+" ("+str(len(res[k]))+" langs) ===")
    for l,v in sorted(res[k].items()): print("   "+l.ljust(20)+" | "+v[:110])
# check work refs
workrefs = {}
for f in glob.glob("tools/_i18n_work/*.json"):
    l = f.split("\\")[-1].split("/")[-1][:-5]
    w = json.load(open(f,encoding="utf-8"))
    s = set()
    for e in w.get("entries",[]):
        for rf in e.get("refs",[]): s.add(rf[0]+"::"+rf[1])
    workrefs[l]=s
stale = json.load(open("tools/_i18n_rebrand.json",encoding="utf-8"))["stale"]
inwork = [s for s in stale if (s["file"]+"::"+s["key"]) in workrefs.get(s["lang"],set())]
print("=== STALE IN WORK REFS ===", len(inwork), "of", len(stale))
for s in inwork[:20]: print("   ", s["lang"], s["file"], s["key"])
