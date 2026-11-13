import tomllib, re, glob, os, sys
sys.path.insert(0,"tools")
import _i18n_pipeline as p
R=p.R
d=tomllib.load(open(R/"src/grf/lang/simplified_chinese.toml","rb"))
for sec in ["STR_CARGO_EDIBLE_OIL","STR_CARGO_QUICKLIME","STR_CARGO_VEHICLE_BODIES"]:
    print(sec,"cid=",repr(d[sec]["cid"]))
print("=== report dashboard cid line ===")
for ln in open(R/"TRANSLATION_COMPLETION_REPORT.md",encoding="utf-8"):
    if "人工语料分歧" in ln or "文字体系污染" in ln or "独立 QA" in ln: print(ln.strip())
