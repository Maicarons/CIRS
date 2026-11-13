#!/usr/bin/env python3
"""Round-3 polish (idempotent; dry-run by default, APPLY=1 writes).
   A) repair 4 script-contaminated values
   B) Traditional Chinese: convert unambiguous simplified chars, skip DOC_TRANS_LANG_ autonyms
   C) sync unrendered long-name extra_strings files to the rendered short-code files
   D) mirror every change into tools/_i18n_out/<lang>.jsonl via work ref index (last-wins)
"""
import json, re, glob, os, collections, io, importlib.util
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
APPLY = os.environ.get("APPLY", "0") == "1"

ASSIGN = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
PH = re.compile(r'\{([A-Za-z_0-9]*)\}')
def esc(s): return s.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n").replace("\t","\\t").replace("\r","\\r")
def unesc(s):
    out=[]; i=0
    mp={"n":"\n","t":"\t","r":"\r","b":"\b","f":"\f","\\":"\\",'"':'"'}
    while i<len(s):
        if s[i]=="\\" and i+1<len(s): out.append(mp.get(s[i+1],s[i+1])); i+=2
        else: out.append(s[i]); i+=1
    return "".join(out)
def ph(s): return collections.Counter(PH.findall(s or ""))

def read_raw(file):
    sec=None; cur={}
    for ln in open(file,encoding="utf-8").read().split("\n"):
        m=SECTION.match(ln)
        if m: sec=m.group(1); continue
        a=ASSIGN.match(ln)
        if a:
            k=(sec+"."+a.group(2)) if sec else a.group(2)
            cur[k]=unesc(a.group(4)[1:-1])
    return cur
def write_patch(file, changes):
    lines=open(file,encoding="utf-8").read().split("\n"); sec=None; out=[]; hits=collections.Counter()
    for ln in lines:
        m=SECTION.match(ln)
        if m: sec=m.group(1); out.append(ln); continue
        a=ASSIGN.match(ln)
        if a:
            full=(sec+"."+a.group(2)) if sec else a.group(2)
            if full in changes:
                old=unesc(a.group(4)[1:-1]); new=changes[full]
                if ph(old)!=ph(new): return "PH_MISMATCH "+full
                out.append(a.group(1)+a.group(2)+a.group(3)+'"'+esc(new)+'"'+a.group(5)); hits[full]+=1; continue
        out.append(ln)
    for k in changes:
        if hits[k]!=1: return "HIT_"+str(hits[k])+" "+k
    if APPLY: open(file,"w",encoding="utf-8",newline="\n").write("\n".join(out))
    return "OK"

ALL = collections.defaultdict(dict)
log = io.StringIO()

# ---------- A) 4 curated script-contamination repairs ----------
A = [
 ("src/docs/extra_strings_croatian.toml","CARGO_INFO_PLANT_AND_MACHINERY.base",
  "Oprema s pogonom i mehanički sustavi koji se koriste u zgradama, industriji i na farmama. Prevoze se kao cjelovite jedinice ili kao veliki podsklopovi."),
 ("src/grf/lang/danish.toml","STR_CARGO_AMMONIA_AND_NITRIC_PRODUCTS.name","Ammoniak- og salpetersyreprodukter"),
 ("src/grf/lang/norwegian_bokmal.toml","STR_CARGO_AMMONIA_AND_NITRIC_PRODUCTS.name","Ammoniak- og salpetersyreprodukter"),
 ("src/docs/extra_strings_traditional_chinese.toml","CARGO_INFO_WOOD_PULP.base",
  "經加工後的木纖維，主要用於紙張生產，以捆包或散裝紙漿形式運輸。"),
]
for f,k,v in A: ALL[f][k]=v
log.write("A curated repairs "+str(len(A))+"\n")

# ---------- B) zh-Hant simplified-char conversion ----------
S2T = {"检":"檢","简":"簡","温":"溫","鲁":"魯","馏":"餾","装":"裝","体":"體"}
ZHANT = ["src/docs/lang/traditional_chinese.toml","src/grf/lang/traditional_chinese.toml",
         "src/gs/lang/traditional_chinese.toml","src/docs/extra_strings_traditional_chinese.toml"]
bcount=0
for f in ZHANT:
    for k,old in read_raw(f).items():
        if k.startswith("DOC_TRANS_LANG_"): continue
        if k in ALL[f]: continue          # curated repair wins
        new = "".join(S2T.get(c,c) for c in old)
        if new != old: ALL[f][k]=new; bcount+=1
log.write("B zh-Hant char conversions "+str(bcount)+"\n")

# ---------- C) sync unrendered long-name extra_strings to rendered short-code files ----------
PAIRS = [("extra_strings_fr.toml","extra_strings_french.toml"),
         ("extra_strings_de.toml","extra_strings_german.toml"),
         ("extra_strings_es.toml","extra_strings_spanish.toml"),
         ("extra_strings_zh.toml","extra_strings_simplified_chinese.toml"),
         ("extra_strings_ko.toml","extra_strings_korean.toml"),
         ("extra_strings_ar.toml","extra_strings_arabic.toml"),
         ("extra_strings_pt.toml","extra_strings_portuguese.toml")]
ccount=0
for short,long in PAIRS:
    sf = "src/docs/"+short; lf = "src/docs/"+long
    sv = read_raw(sf); lv = read_raw(lf)
    diff=0
    for k,v in sv.items():
        if k in lv and lv[k] != v:
            ALL[lf][k] = v; diff+=1
    ccount+=diff
    log.write("C SYNC "+short+" -> "+long+" diff="+str(diff)+"\n")

# ---------- validate placeholder parity ----------
bad=[]
for f,ch in ALL.items():
    cur = read_raw(f)
    for k,new in ch.items():
        if k not in cur: bad.append((f,k,"ABSENT")); continue
        if ph(cur[k]) != ph(new): bad.append((f,k,"PH "+cur[k][:60]+" => "+new[:60]))
if bad:
    log.write("VALIDATION ERRORS "+str(len(bad))+"\n")
    for b in bad: log.write("  "+" | ".join(b)+"\n")
    open("tools/_i18n_round3_fix.log","w",encoding="utf-8").write(log.getvalue())
    print("VALIDATION_ERRORS",len(bad),"ABORT")
    raise SystemExit(1)

# ---------- D) mirror into out-JSONL by work index ----------
REF2WORK = {}
for wf in sorted(glob.glob("tools/_i18n_work/*.json")):
    lang = os.path.basename(wf)[:-5]
    w = json.load(open(wf, encoding="utf-8"))
    for i,e in enumerate(w.get("entries",[])):
        for ref in e.get("refs",[]):
            if isinstance(ref,(list,tuple)) and len(ref)>=2:
                REF2WORK.setdefault((str(ref[0]).replace("\\","/"),str(ref[1])),[]).append((lang,i))
byidx = collections.defaultdict(lambda: collections.defaultdict(set))
noref=[]
for f,ch in ALL.items():
    fk = f.replace("\\","/")
    for k,new in ch.items():
        targets = REF2WORK.get((fk,k),[])
        if not targets: noref.append((f,k)); continue
        for lang,i in targets: byidx[(lang,i)][new].add((fk,k))
appends = collections.defaultdict(list); conflicts=[]
for (lang,i), vals in sorted(byidx.items()):
    if len(vals)==1: appends[lang].append((i,next(iter(vals))))
    else:
        conflicts.append((lang,i))
        appends[lang].append((i,sorted(vals)[0]))
log.write("CHANGES_TOTAL "+str(sum(len(c) for c in ALL.values()))+" files "+str(len(ALL))+"\n")
for f,ch in sorted(ALL.items()): log.write("  "+f.replace("\\","/")+" "+str(len(ch))+"\n")
log.write("NO_WORK_REF "+str(len(noref))+" (safe: apply never touches keys outside work list)\n")
for n in noref[:8]: log.write("  NOREF "+n[0]+" "+n[1]+"\n")
log.write("OUT_JSONL_CONFLICTS "+str(len(conflicts))+"\n")
log.write("OUT_JSONL_APPENDS "+str(sum(len(x) for x in appends.values()))+" langs "+str(len(appends))+"\n")
if APPLY:
    for f,ch in ALL.items():
        s = write_patch(f,ch)
        log.write("PATCH "+f.replace("\\","/")+" "+s+"\n")
    for lang,pairs in appends.items():
        with open("tools/_i18n_out/"+lang+".jsonl","a",encoding="utf-8") as fp:
            for i,v in pairs: fp.write(json.dumps({"i":i,"tr":v},ensure_ascii=False)+"\n")
    log.write("WROTE (APPLY=1)\n")
else:
    log.write("DRY RUN\n")
open("tools/_i18n_round3_fix.log","w",encoding="utf-8").write(log.getvalue())
print("changes",sum(len(c) for c in ALL.values()),"A",len(A),"B",bcount,"C",ccount,
      "appends",sum(len(x) for x in appends.values()),"conflicts",len(conflicts),
      "noref",len(noref),"APPLY",APPLY)
