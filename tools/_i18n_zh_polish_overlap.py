import json, collections, re, os, io, subprocess, tomllib
L=[]
# out jsonl multi-line indices
lines=[l for l in open("tools/_i18n_out/simplified_chinese.jsonl",encoding="utf-8").read().splitlines() if l.strip()]
byi=collections.defaultdict(list)
for n,l in enumerate(lines,1):
    o=json.loads(l); byi[o["i"]].append((n,o["tr"]))
W=json.load(open("tools/_i18n_work/simplified_chinese.json",encoding="utf-8")); E=W["entries"] if isinstance(W,dict) else W
multi={i:v for i,v in byi.items() if len(v)>1}
L.append("OUT_LINES %d UNIQUE_IDX %d MULTI_IDX %d"%(len(lines),len(byi),len(multi)))
L.append("=== MULTI (deliberate polish appended) ===")
for i,v in sorted(multi.items()):
    en=E[i]["en"]; refs=[tuple(r) for r in E[i].get("refs",[])]
    L.append("i=%d en=%r first=%r last=%r refs=%r"%(i,en[:80],v[0][1][:80],v[-1][1][:80],refs[:3]))
# direct TOML polish key sets from data files
def load(p):
    try: return json.load(open(p,encoding="utf-8"))
    except: return None
for name in ["tools/_i18n_rebrand_tasks.json","tools/_i18n_rebrand_candidates.json","tools/_i18n_rebrand_model_out.json","tools/_i18n_sameform_v4_candidates.json","tools/_i18n_consensus.json","tools/_i18n_rebrand.json","tools/_i18n_round3_cid.json"]:
    d=load(name)
    if d is None: L.append("DATA %s MISSING"%name); continue
    s=json.dumps(d,ensure_ascii=False)
    zh = "simplified_chinese" in s
    L.append("DATA %s type=%s len=%s mentions_zh=%s"%(name,type(d).__name__,len(d),zh))
# rebrand patch program: find keys by reading its source for zh entries
for name in ["tools/_i18n_rebrand_patch.py","tools/_i18n_round3_cidfix.py","tools/_i18n_steel_fix.py","tools/_i18n_round3_fix.py"]:
    if os.path.exists(name):
        t=open(name,encoding="utf-8").read()
        L.append("SRC %s len=%d mentions_zh=%s"%(name,len(t),"simplified_chinese" in t))
# English DOC_NAV_SWITCH_LANGUAGE
for f in ["src/docs/lang/english.toml","src/docs/lang/simplified_chinese.toml"]:
    d=tomllib.load(open(f,"rb"))
    L.append("NAV %s = %r"%(f,d.get("DOC_NAV_SWITCH_LANGUAGE")))
# HEAD vs CUR FIRS/CIRS for NOREF restore keys
def leaves(txt):
    d=tomllib.loads(txt); out={}
    for sec,v in d.items():
        if isinstance(v,dict):
            for k,vv in v.items(): out[sec+"."+k]=vv if isinstance(vv,str) else str(vv)
        elif isinstance(v,str): out[sec]=v
    return out
def head(p): return subprocess.check_output(["git","show","HEAD:"+p]).decode("utf-8")
F="src/grf/lang/simplified_chinese.toml"; EF="src/grf/lang/english.toml"
H=leaves(head(F)); C=leaves(open(F,encoding="utf-8").read()); EN=leaves(open(EF,encoding="utf-8").read())
noref=[]
for k,en in EN.items():
    h=H.get(k); c=C.get(k)
    if h is None or h==en or c is None or c==h: continue
    noref.append((k,h,c,en))
br=[(k,h,c,en) for k,h,c,en in noref if ("FIRS" in h)!=( "FIRS" in c) or ("CIRS" in h)!=( "CIRS" in c)]
L.append("GRF NOREF restore=%d brand_diff=%d"%(len(noref),len(br)))
for k,h,c,en in br[:30]:
    L.append("  %s | HEAD_FIRS=%d CUR_FIRS=%d HEAD_CIRS=%d CUR_CIRS=%d"%(k,h.count("FIRS"),c.count("FIRS"),h.count("CIRS"),c.count("CIRS")))
    L.append("    HEAD: %s"%h[:120]); L.append("    CUR : %s"%c[:120])
open("tools/_i18n_zh_polish_overlap.txt","w",encoding="utf-8").write("\n".join(L))
print("OK lines",len(L))
