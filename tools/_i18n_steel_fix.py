#!/usr/bin/env python3
"""Curated steel-term repair (idempotent). Replaces only unambiguous
   'tickets/flowers/invented-word' mistranslations with the English technical
   term, which this project already keeps as a loanword. Syncs to out-JSONL."""
import json, re, glob, os, collections, sys, io
REPL = [
    ("Billetes","Billets"),("billetes","Billets"),
    ("Bilhetes","Billets"),("bilhetes","Billets"),
    ("flors","blooms"),("Flors","blooms"),
    ("flores","blooms"),("Flores","blooms"),
    ("Blöme","Blooms"),("blöme","Blooms"),
    ("bloeiings","blooms"),("Bloeiings","blooms"),
    ("bloemorum","blooms"),
]
WRONG = re.compile(r"Billetes|billetes|Bilhetes|bilhetes|flors|Flors|flores|Flores|Blöme|blöme|bloeiings|Bloeiings|bloemorum")
KEYS = {"CARGO_INFO_CARBON_STEEL.base","CARGO_INFO_CAST_IRON.base",
        "STR_CARGO_STEEL_BILLETS_AND_BLOOMS.name","STR_CARGO_STEEL_BILLETS_AND_BLOOMS.cargo_unit"}
FILES = sorted(glob.glob("src/grf/lang/*.toml")+glob.glob("src/gs/lang/*.toml")+
               glob.glob("src/docs/lang/*.toml")+glob.glob("src/docs/extra_strings_*.toml"))
FILES = [f for f in FILES if "english" not in os.path.basename(f) and not f.endswith("extra_strings.toml")]
REF2WORK = {}
for wf in sorted(glob.glob("tools/_i18n_work/*.json")):
    lang = os.path.basename(wf)[:-5]
    w = json.load(open(wf, encoding="utf-8"))
    for i,e in enumerate(w.get("entries",[])):
        for ref in e.get("refs",[]):
            if isinstance(ref,(list,tuple)) and len(ref)>=2:
                REF2WORK.setdefault((str(ref[0]),str(ref[1])),[]).append((lang,i))
ASSIGN = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
PH = re.compile(r'\{([A-Za-z_0-9]*)\}')
def esc(s): return s.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n").replace("\t","\\t").replace("\r","\\r")
def ph(s): return collections.Counter(PH.findall(s or ""))
def read_keys(file):
    sec=None; cur={}
    for ln in open(file,encoding="utf-8").read().split("\n"):
        m=SECTION.match(ln)
        if m: sec=m.group(1); continue
        a=ASSIGN.match(ln)
        if a:
            k=(sec+"."+a.group(2)) if sec else a.group(2)
            if k in KEYS: cur[k]=a.group(4)[1:-1]
    return cur
def patch(file,key,tr):
    lines=open(file,encoding="utf-8").read().split("\n"); sec=None; out=[]; hit=0
    for ln in lines:
        m=SECTION.match(ln)
        if m: sec=m.group(1)
        a=ASSIGN.match(ln)
        if a:
            full=(sec+"."+a.group(2)) if sec else a.group(2)
            if full==key:
                old=a.group(4)[1:-1]
                if ph(old)!=ph(tr): return "PH_MISMATCH"
                out.append(a.group(1)+a.group(2)+a.group(3)+'"'+esc(tr)+'"'+a.group(5)); hit+=1; continue
        out.append(ln)
    if hit!=1: return "HIT_"+str(hit)
    open(file,"w",encoding="utf-8",newline="\n").write("\n".join(out)); return "OK"
log=io.StringIO(); log.write("work refs indexed: "+str(len(REF2WORK))+"\n")
changes=[]; residual=[]
for f in FILES:
    for k,old in read_keys(f).items():
        new=old
        for a,b in REPL: new=new.replace(a,b)
        if WRONG.search(old): residual.append((f,k,old))
        if new!=old: changes.append((f,k,old,new))
log.write("CHANGES "+str(len(changes))+"  RESIDUAL_WRONG_BEFORE "+str(len(residual))+"\n")
for f,k,old,new in changes: log.write("  "+os.path.basename(f)+" "+k+" | "+old+" => "+new+"\n")
ok=0; append=collections.defaultdict(list)
for f,k,old,new in changes:
    s=patch(f,k,new)
    if s!="OK": log.write("  ERR "+f+" "+k+" "+s+"\n"); continue
    ok+=1
    for lang,i in REF2WORK.get((f.replace("\\","/"),k),[]): append[lang].append((i,new))
for lang,pairs in append.items():
    with open("tools/_i18n_out/"+lang+".jsonl","a",encoding="utf-8") as fp:
        for i,tr in pairs: fp.write(json.dumps({"i":i,"tr":tr},ensure_ascii=False)+"\n")
# residual census AFTER
after=[]
for f in FILES:
    for k,v in read_keys(f).items():
        if WRONG.search(v): after.append((os.path.basename(f),k,v))
log.write("RESIDUAL_WRONG_AFTER "+str(len(after))+"\n")
for f,k,v in after: log.write("  AFTER "+f+" "+k+" | "+v+"\n")
log.write("PATCHED "+str(ok)+" OUT_JSONL_APPENDS "+str(sum(len(x) for x in append.values()))+" langs "+str(len(append))+"\n")
open("tools/_i18n_steel_fix.log","w",encoding="utf-8").write(log.getvalue())
print("PATCHED",ok,"changes",len(changes),"residual_before",len(residual),"residual_after",len(after))
