import json, re, subprocess, tomllib, collections
W=json.load(open("tools/_i18n_work/simplified_chinese.json",encoding="utf-8")); E=W["entries"] if isinstance(W,dict) else W
def refs(i): return [tuple(r) for r in E[i].get("refs",[])]
def en(i): return E[i]["en"]
# 1) ref format for docs keys
for i,e in enumerate(E):
    rs=[tuple(r) for r in e.get("refs",[])]
    if any("docs/lang" in r[0] for r in rs):
        print("DOCS_REF_SAMPLE i=%d en=%r refs=%r"%(i,e["en"][:50],rs[:3])); break
for i,e in enumerate(E):
    rs=[tuple(r) for r in e.get("refs",[])]
    if any(r[1] in ("DOC_TITLE","DOC_NAV_ECONOMIES","DOC_HOME_TAGLINE","DOC_CC_PASSENGERS") for r in rs):
        print("DOCKEY i=%d en=%r refs=%r"%(i,e["en"][:50],rs[:4]))
# 2) conflict groups
for i in (337,191,69):
    print("CONFLICT i=%d en=%r refs=%r"%(i,en(i),refs(i)))
# 3) english cid values of the 3 cid keys
eng=tomllib.load(open("src/grf/lang/english.toml","rb"))
for sec in ["STR_CARGO_INDUSTRIAL_CARBONS","STR_CARGO_PAINTS_AND_COATINGS","STR_CARGO_PROCESS_CHEMICALS","STR_CARGO_CHEMICALS","STR_CARGO_PACKAGING"]:
    d=eng.get(sec)
    if d: print("EN CID %s cid=%r name=%r"%(sec,d.get("cid"),d.get("name")))
cur=tomllib.load(open("src/grf/lang/simplified_chinese.toml","rb"))
for sec in ["STR_CARGO_INDUSTRIAL_CARBONS","STR_CARGO_PAINTS_AND_COATINGS","STR_CARGO_PROCESS_CHEMICALS","STR_CARGO_CHEMICALS","STR_CARGO_PACKAGING"]:
    d=cur.get(sec)
    if d: print("ZH CID %s cid=%r name=%r"%(sec,d.get("cid"),d.get("name")))
# 4) round3 cid fix keys
try:
    c=json.load(open("tools/_i18n_round3_cid.json",encoding="utf-8"))
    print("CID JSON type",type(c).__name__,"len",len(c))
    s=json.dumps(c,ensure_ascii=False)
    print("CID JSON mentions simplified_chinese?", "simplified_chinese" in s)
    print(s[:900])
except Exception as ex: print("CID JSON err",ex)
