import subprocess, re, json, collections, tomllib
REWRITES = {".DOC_HOME_TAGLINE",".DOC_HOME_WHY_1_DESC",".DOC_HOME_WHY_2_DESC",".DOC_HOME_WHY_3_DESC",".DOC_CR_COMPILING_P1",".DOC_CR_FRAX_P1",".DOC_CR_FRAX_P2",".DOC_CR_TOWN_GROWTH_NOTE"}
def leaves(txt):
    d=tomllib.loads(txt); out={}
    for sec,v in d.items():
        if isinstance(v,dict):
            for k,vv in v.items(): out[sec+"."+k]=vv if isinstance(vv,str) else str(vv)
        elif isinstance(v,str): out["."+sec]=v
    return out
def head(p): return subprocess.check_output(["git","show","HEAD:"+p]).decode("utf-8")
def cnt(s,t): return len(re.findall(r"(?<![A-Za-z])"+t+r"(?![A-Za-z])",s))
PAIRS=[("src/grf/lang/simplified_chinese.toml","src/grf/lang/english.toml"),("src/gs/lang/simplified_chinese.toml","src/gs/lang/english.toml"),("src/docs/lang/simplified_chinese.toml","src/docs/lang/english.toml")]
restore=[]
for f,ef in PAIRS:
    H=leaves(head(f)); E=leaves(open(ef,encoding="utf-8").read()); C=leaves(open(f,encoding="utf-8").read())
    for k,en in E.items():
        if k in REWRITES: continue
        h=H.get(k); c=C.get(k)
        if h is None or h==en or c is None or c==h: continue
        restore.append((f,k,h,c,en))
L=[]
L.append("RESTORE %d"%len(restore))
# brand/rebrand regression check
brand=[]
for f,k,h,c,en in restore:
    hf,ef,cf=cnt(h,"FIRS"),cnt(en,"FIRS"),cnt(c,"FIRS")
    hc,ec,cc=cnt(h,"CIRS"),cnt(en,"CIRS"),cnt(c,"CIRS")
    if hf>ef or (cc>hc and hf>0): brand.append((f,k,hf,ef,cf,hc,ec,cc,h,c,en))
L.append("BRAND_REGRESSION %d"%len(brand))
for f,k,hf,ef,cf,hc,ec,cc,h,c,en in brand[:30]:
    L.append("  %s %s | FIRS h/e/c=%d/%d/%d CIRS h/e/c=%d/%d/%d"%(f,k,hf,ef,cf,hc,ec,cc))
    L.append("    HEAD: %s"%h[:130]); L.append("    CUR : %s"%c[:130]); L.append("    EN  : %s"%en[:130])
# placeholder parity
PH=re.compile(r"\{([A-Za-z_0-9]*)\}")
badph=[(f,k) for f,k,h,c,en in restore if sorted(PH.findall(h))!=sorted(PH.findall(en))]
L.append("PH_MISMATCH %d %s"%(len(badph),badph[:8]))
# work index mapping
work=json.load(open("tools/_i18n_work/simplified_chinese.json",encoding="utf-8"))
entries=work["entries"] if isinstance(work,dict) else work
ref2i={}; i2refs=collections.defaultdict(list)
for i,e in enumerate(entries):
    for rf in e.get("refs",[]):
        key=(rf[0].replace("\\","/").lstrip("./"),rf[1])
        ref2i[key]=i; i2refs[i].append(key)
rest_keys={(f,k) for f,k,h,c,en in restore}
mapped={}; noref=[]; conflicts=[]; mixed=[]
for f,k,h,c,en in restore:
    i=ref2i.get((f,k))
    if i is None: noref.append((f,k)); continue
    mapped.setdefault(i,[]).append((f,k,h,c))
for i,vals in mapped.items():
    hs={v[2] for v in vals}
    if len(hs)>1: conflicts.append((i,vals))
    others=[r for r in i2refs[i] if r not in rest_keys]
    if others: mixed.append((i,others,vals))
L.append("MAPPED %d NOREF %d CONFLICT_IDX %d MIXED_IDX %d"%(len(mapped),len(noref),len(conflicts),len(mixed)))
for i,vals in conflicts[:10]:
    L.append("  CONFLICT i=%d"%i)
    for f,k,h,c in vals: L.append("    %s %s HEAD=%s CUR=%s"%(f,k,h[:60],c[:60]))
for i,others,vals in mixed[:10]:
    L.append("  MIXED i=%d other_refs=%s"%(i,[(a,b) for a,b in others][:4]))
# out jsonl last wins
out={}
for ln in open("tools/_i18n_out/simplified_chinese.jsonl",encoding="utf-8"):
    ln=ln.strip()
    if not ln: continue
    try: o=json.loads(ln); out[o["i"]]=o["tr"]
    except: pass
L.append("OUT_LINES %d"%len(out))
L.append("=== ENGLISH SEMANTIC SAMPLES ===")
want=["STR_PARAM_VALUE_ECONOMIES_MILD_MILD_WEST.base","STR_PARAM_NAME_PRIMARY_LEVEL1_REQUIREMENT.base","STR_PARAM_NAME_PRIMARY_LEVEL2_REQUIREMENT.base","STR_IND_PRODUCTION_LEVEL_NORMAL.base"]
for f,k,h,c,en in restore:
    if k in want or "THREE" in k or "MINUTES" in k:
        L.append("KEY %s"%k); L.append("  EN  : %s"%en[:200]); L.append("  HEAD: %s"%h[:200]); L.append("  CUR : %s"%c[:200])
# three months keys
L.append("=== KEYS WITH 三个月 OR 次水准 IN CURRENT ===")
for f,k,h,c,en in restore:
    if "三个月" in c or "次水准" in c:
        L.append("  %s %s"%(f,k)); L.append("    HEAD: %s"%h[:170]); L.append("    CUR : %s"%c[:170])
open("tools/_i18n_zh_restore_plan.txt","w",encoding="utf-8").write("\n".join(L))
print("OK lines",len(L),"restore",len(restore),"brand",len(brand),"mapped",len(mapped),"noref",len(noref),"conflicts",len(conflicts),"mixed",len(mixed))
