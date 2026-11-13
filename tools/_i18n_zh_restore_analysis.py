import subprocess, tomllib, re, json, io, os
REWRITES = {".DOC_HOME_TAGLINE",".DOC_HOME_WHY_1_DESC",".DOC_HOME_WHY_2_DESC",".DOC_HOME_WHY_3_DESC",".DOC_CR_COMPILING_P1",".DOC_CR_FRAX_P1",".DOC_CR_FRAX_P2",".DOC_CR_TOWN_GROWTH_NOTE"}
PH = re.compile(r"\{([A-Za-z_0-9]*)\}")
def parse(txt):
    out={}; sec=None
    for ln in txt.splitlines():
        m=re.match(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$',ln)
        if m: sec=m.group(1); continue
        m=re.match(r'^\s*([A-Za-z0-9_-]+)\s*=\s*"(.*)"\s*$',ln)
        if m: out[(sec or "")+"."+m.group(1)]=m.group(2)
    return out
def head(p): return subprocess.check_output(["git","show","HEAD:"+p]).decode("utf-8")
PAIRS=[("src/grf/lang/simplified_chinese.toml","src/grf/lang/english.toml"),("src/gs/lang/simplified_chinese.toml","src/gs/lang/english.toml"),("src/docs/lang/simplified_chinese.toml","src/docs/lang/english.toml")]
report=[]
restore=[]
for f,ef in PAIRS:
    H=parse(head(f)); E=parse(open(ef,encoding="utf-8").read()); C=parse(open(f,encoding="utf-8").read())
    R=[k for k in E if k in H and H[k]!=E[k] and k not in REWRITES and k in C and H[k]!=C[k]]
    report.append("FILE %s keys=%d restore=%d"%(f,len(E),len(R)))
    for k in R: restore.append((f,k,H[k],C[k],E[k]))
    # FIRS/CIRS staleness in HEAD
    firs=[k for k in R if "FIRS" in H[k] and "FIRS" not in E[k]]
    report.append("  HEAD with FIRS but English no FIRS: %d %s"%(len(firs),firs[:8]))
    # placeholder parity HEAD vs English
    badph=[k for k in R if sorted(PH.findall(H[k]))!=sorted(PH.findall(E[k]))]
    report.append("  placeholder mismatch HEAD vs English: %d %s"%(len(badph),badph[:8]))
    # keys HEAD==English (keep current machine)
    keep=[k for k in E if k in H and H[k]==E[k] and k in C and C[k]!=E[k]]
    report.append("  HEAD was English, keep current translation: %d"%len(keep))
    report.append("  samples of restore:")
    for k in R[:6]:
        report.append("    %s"%k)
        report.append("      HEAD: %s"%H[k][:160])
        report.append("      CUR : %s"%C[k][:160])
# out-jsonl ref conflict check
work=json.load(open("tools/_i18n_work/simplified_chinese.json",encoding="utf-8"))
entries=work["entries"] if isinstance(work,dict) else work
ref2i={}
for i,e in enumerate(entries):
    for rf in e.get("refs",[]): ref2i[(rf[0].replace("\\","/"),rf[1])]=i
want={}
conf=[]
for f,k,h,c,en in restore:
    key=(f,k)
    if key in ref2i:
        i=ref2i[key]
        want.setdefault(i,{}).setdefault(h,[]).append(key)
    else:
        conf.append(("NO_WORK_REF",f,k))
multi=[(i,list(d.keys())) for i,d in want.items() if len(d)>1]
report.append("RESTORE total=%d mapped_indices=%d no_work_ref=%d index_conflicts=%d"%(len(restore),len(want),len(conf),len(multi)))
for i,vs in multi[:10]:
    report.append("  CONFLICT i=%d values=%s"%(i,[v[:80] for v in vs]))
for c in conf[:10]: report.append("  NO_WORK_REF %s %s"%(c[1],c[2]))
open("tools/_i18n_zh_restore_analysis.txt","w",encoding="utf-8").write("\n".join(report))
print("report lines",len(report))
