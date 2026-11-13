#!/usr/bin/env python3
import importlib.util, json
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
lm = p.lang_map(); extras = p.extra_files(lm)
out = {}
keys = ["DOC_GS_SETUP_B1_PREFIX","DOC_GS_SETUP_B1_LINK","DOC_GS_SETUP_B1_SUFFIX","DOC_HOME_WHY_3_TITLE","DOC_HOME_WHY_3_DESC","STR_GRF_NAME.base","STR_PARAM_DESC_ECONOMIES.base"]
for l in sorted(lm):
    vals = {}
    for grp, tgt, ref in p.targets(l, lm, extras) if l != "english" else p.targets("french", lm, extras):
        tv = p.leaves(p.load(R/tgt))
        for k in keys:
            if k in tv: vals[k] = tv[k]
    out[l] = vals
json.dump(out, open("tools/_i18n_edge_survey.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("survey langs", len(out))
# ascii-safe summaries
print("=== CHINESE TRIO ===")
for l in ["english","simplified_chinese","traditional_chinese"]:
    v=out[l]
    print(l, json.dumps({k:v.get(k) for k in keys[:3]}, ensure_ascii=False))
print("=== UPSTREAM TITLE (all) ===")
for l,v in out.items():
    t=v.get("DOC_HOME_WHY_3_TITLE","")
    print("  "+l.ljust(22)+" | "+t.encode("ascii","backslashreplace").decode())
print("=== GRF NAME (all) ===")
for l,v in out.items():
    t=v.get("STR_GRF_NAME.base","")
    print("  "+l.ljust(22)+" | "+t.encode("ascii","backslashreplace").decode())
