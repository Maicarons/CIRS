import tomllib, json, subprocess, os, sys
sys.path.insert(0,"tools"); import _i18n_pipeline as p
R=p.R
d=tomllib.load(open(R/"src/grf/lang/simplified_chinese.toml","rb"))
geo=tomllib.load(open(R/"src/docs/lang/simplified_chinese.toml","rb"))
L=[]
for sec in ["STR_CARGO_EDIBLE_OIL","STR_CARGO_QUICKLIME","STR_CARGO_VEHICLE_BODIES"]:
    L.append("%s cid=%s"%(sec,d[sec]["cid"]))
L.append("ECONOMY MILD_MILD_WEST = %s"%d["STR_PARAM_VALUE_ECONOMIES_MILD_MILD_WEST"]["base"])
L.append("PRODUCTION 1X = %s"%d["STR_PRIMARY_PRODUCTION_1X"]["base"])
L.append("TAGLINE = %s"%geo["DOC_HOME_TAGLINE"])
L.append("FRAX_P1 = %s"%geo["DOC_CR_FRAX_P1"])
L.append("GRF_DESC = %s"%d["STR_GRF_DESC"]["base"])
# dashboard lines in UTF-8
for ln in open(R/"TRANSLATION_COMPLETION_REPORT.md",encoding="utf-8"):
    if ln.startswith("- 文字体系污染") or ln.startswith("- 与 FIRS") or ln.startswith("- 繁体中文残留") or ln.startswith("- 独立 QA") or ln.startswith("- 官方校验") or ln.startswith("- 短码 /"):
        L.append("DASH "+ln.strip())
open(R/"tools/_i18n_final_verify.txt","w",encoding="utf-8").write("\n".join(L))
print("OK")
