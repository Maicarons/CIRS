import subprocess, tomllib, re, json, collections, io
REWRITES={"DOC_HOME_TAGLINE","DOC_HOME_WHY_1_DESC","DOC_HOME_WHY_2_DESC","DOC_HOME_WHY_3_DESC","DOC_CR_COMPILING_P1","DOC_CR_FRAX_P1","DOC_CR_FRAX_P2","DOC_CR_TOWN_GROWTH_NOTE"}
def leaves(txt):
    d=tomllib.loads(txt); out={}
    for sec,v in d.items():
        if isinstance(v,dict):
            for k,vv in v.items():
                if sec=="GLOBAL_PRAGMA": continue
                out[sec+"."+k]=vv if isinstance(vv,str) else str(vv)
        elif isinstance(v,str): out[sec]=v
    return out
def head(p): return subprocess.check_output(["git","show","HEAD:"+p]).decode("utf-8")
FILES=["src/grf/lang/simplified_chinese.toml","src/gs/lang/simplified_chinese.toml","src/docs/lang/simplified_chinese.toml"]
ENF=["src/grf/lang/english.toml","src/gs/lang/english.toml","src/docs/lang/english.toml"]
restore=[]
for f,ef in zip(FILES,ENF):
    H=leaves(head(f)); E=leaves(open(ef,encoding="utf-8").read()); C=leaves(open(f,encoding="utf-8").read())
    for k,en in E.items():
        if k.lstrip(".") in REWRITES or k in ("DOC_NAV_SWITCH_LANGUAGE",): continue
        h=H.get(k); c=C.get(k)
        if h is None or h==en or c is None or c==h: continue
        restore.append((f,k,h,c,en))
W=json.load(open("tools/_i18n_work/simplified_chinese.json",encoding="utf-8")); E2=W["entries"] if isinstance(W,dict) else W
ref2i={}; i2refs=collections.defaultdict(list)
for i,e in enumerate(E2):
    for rf in e.get("refs",[]):
        key=(rf[0].replace("\\","/").lstrip("./"),rf[1]); ref2i[key]=i; i2refs[i].append(key)
restset={(f,k) for f,k,h,c,en in restore}
byidx=collections.defaultdict(list); noref=[]
for f,k,h,c,en in restore:
    i=ref2i.get((f,k))
    if i is None: noref.append((f,k,h))
    else: byidx[i].append((f,k,h,c))
conf={i:v for i,v in byidx.items() if len({x[2] for x in v})>1}
mixed={i:(v,[r for r in i2refs[i] if r not in restset]) for i,v in byidx.items() if any(r not in restset for r in i2refs[i])}
L=[]
L.append("RESTORE %d MAPPED_IDX %d NOREF %d CONFLICT_IDX %d MIXED_IDX %d"%(len(restore),len(byidx),len(noref),len(conf),len(mixed)))
L.append("=== CONFLICTS ===")
for i,v in conf.items():
    L.append("i=%d en=%r"%(i,E2[i]["en"]))
    for f,k,h,c in v: L.append("  %s %s HEAD=%r CUR=%r"%(f,k,h,c))
L.append("=== MIXED (index has refs outside restore set) ===")
for i,(v,others) in mixed.items():
    L.append("i=%d en=%r"%(i,E2[i]["en"]))
    for f,k,h,c in v: L.append("  REST %s %s HEAD=%r CUR=%r"%(f,k,h,c))
    for a,b in others: L.append("  OTHER %s %s"%(a,b))
L.append("=== NOREF (first 12) ===")
for f,k,h in noref[:12]: L.append("  %s %s HEAD=%r"%(f,k,h))
L.append("=== DOC_NAV_SWITCH_LANGUAGE ===")
for f in FILES:
    H=leaves(head(f)); C=leaves(open(f,encoding="utf-8").read())
    if "DOC_NAV_SWITCH_LANGUAGE" in C: L.append("  %s HEAD=%r CUR=%r EN=%r"%(f,H.get("DOC_NAV_SWITCH_LANGUAGE"),C["DOC_NAV_SWITCH_LANGUAGE"],leaves(open(ENF[FILES.index(f)],encoding="utf-8").read()).get("DOC_NAV_SWITCH_LANGUAGE")))
L.append("=== 8 REWRITES current values ===")
C=leaves(open(FILES[2],encoding="utf-8").read())
for k in sorted(REWRITES): L.append("  %s = %r"%(k,C.get(k)))
open("tools/_i18n_zh_restore_map.txt","w",encoding="utf-8").write("\n".join(L))
# also save machine-readable restore data
json.dump({"restore":restore,"conflict_idx":list(conf.keys()),"mixed_idx":list(mixed.keys())},open("tools/_i18n_zh_restore_data.json","w",encoding="utf-8"),ensure_ascii=False)
print("OK", "restore",len(restore),"conflict",len(conf),"mixed",len(mixed),"noref",len(noref))
