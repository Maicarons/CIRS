#!/usr/bin/env python3
"""Restore 16 STR_CARGO_*.cid values to the authoritative FIRS 4.x human corpus.
   Idempotent; APPLY=1 writes. Mirrors into out-JSONL so pipeline apply keeps them."""
import json, re, glob, os, collections, io
ASSIGN = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
PH = re.compile(r'\{([A-Za-z_0-9]*)\}')
APPLY = os.environ.get("APPLY","0")=="1"
def esc(s): return s.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n").replace("\t","\\t").replace("\r","\\r")
def unesc(s):
    out=[];i=0;mp={"n":"\n","t":"\t","r":"\r","b":"\b","f":"\f","\\":"\\",'"':'"'}
    while i<len(s):
        if s[i]=="\\" and i+1<len(s): out.append(mp.get(s[i+1],s[i+1])); i+=2
        else: out.append(s[i]); i+=1
    return "".join(out)
def ph(s): return collections.Counter(PH.findall(s or ""))
def read_raw(f):
    sec=None;cur={}
    for ln in open(f,encoding="utf-8").read().split("\n"):
        m=SECTION.match(ln)
        if m: sec=m.group(1);continue
        a=ASSIGN.match(ln)
        if a: cur[(sec+"."+a.group(2)) if sec else a.group(2)]=unesc(a.group(4)[1:-1])
    return cur
def patch(f,ch):
    lines=open(f,encoding="utf-8").read().split("\n");sec=None;out=[];hits=collections.Counter()
    for ln in lines:
        m=SECTION.match(ln)
        if m: sec=m.group(1);out.append(ln);continue
        a=ASSIGN.match(ln)
        if a:
            full=(sec+"."+a.group(2)) if sec else a.group(2)
            if full in ch:
                old=unesc(a.group(4)[1:-1]);new=ch[full]
                if ph(old)!=ph(new): return "PH_MISMATCH "+full
                out.append(a.group(1)+a.group(2)+a.group(3)+'"'+esc(new)+'"'+a.group(5));hits[full]+=1;continue
        out.append(ln)
    for k in ch:
        if hits[k]!=1: return "HIT_"+str(hits[k])+" "+k
    if APPLY: open(f,"w",encoding="utf-8",newline="\n").write("\n".join(out))
    return "OK"
D = json.load(open("tools/_i18n_round3_cid.json",encoding="utf-8"))
log=io.StringIO()
# ---- evidence: English names/cids + collision check for CHEMICALS ----
en = read_raw("src/grf/lang/english.toml")
log.write("=== EVIDENCE: English cids/names for the 8 diverging keys ===\n")
for k in sorted({d["key"] for d in D}):
    stem=k.split(".")[0]
    log.write("  "+k+" EN_cid="+en.get(k,"?")+" EN_name="+en.get(stem+".name","?")+"\n")
log.write("=== EVIDENCE: CHEMICALS vs CHLORINE cid collision (before fix) ===\n")
for lang in sorted({d["lang"] for d in D}):
    f="src/grf/lang/"+lang+".toml"; v=read_raw(f)
    log.write("  "+lang+" CHEMICALS="+v.get("STR_CARGO_CHEMICALS.cid","?")+" CHLORINE="+v.get("STR_CARGO_CHLORINE.cid","?")+"\n")
# ---- build change set ----
ALL=collections.defaultdict(dict)
for d in D:
    f="src/grf/lang/"+d["lang"]+".toml"
    ALL[f][d["key"]]=d["human"]
# ---- validate ----
bad=[]
for f,ch in ALL.items():
    cur=read_raw(f)
    for k,new in ch.items():
        if k not in cur: bad.append((f,k,"ABSENT"))
        elif ph(cur[k])!=ph(new): bad.append((f,k,"PH"))
if bad:
    print("VALIDATION_ERRORS",len(bad));[print(" ",*b) for b in bad];raise SystemExit(1)
# ---- out-JSONL mirror ----
REF2WORK={}
for wf in sorted(glob.glob("tools/_i18n_work/*.json")):
    lang=os.path.basename(wf)[:-5];w=json.load(open(wf,encoding="utf-8"))
    for i,e in enumerate(w.get("entries",[])):
        for ref in e.get("refs",[]):
            if isinstance(ref,(list,tuple)) and len(ref)>=2:
                REF2WORK.setdefault((str(ref[0]).replace("\\","/"),str(ref[1])),[]).append((lang,i))
byidx=collections.defaultdict(lambda:collections.defaultdict(set));noref=[]
for f,ch in ALL.items():
    fk=f.replace("\\","/")
    for k,new in ch.items():
        t=REF2WORK.get((fk,k),[])
        if not t: noref.append((f,k));continue
        for lang,i in t: byidx[(lang,i)][new].add((fk,k))
app=collections.defaultdict(list);conf=0
for (lang,i),vals in sorted(byidx.items()):
    if len(vals)>1: conf+=1
    app[lang].append((i,sorted(vals)[0]))
log.write("CHANGES "+str(sum(len(c) for c in ALL.values()))+" files "+str(len(ALL))+" noref "+str(len(noref))+" conflicts "+str(conf)+" appends "+str(sum(len(x) for x in app.values()))+"\n")
for f,ch in sorted(ALL.items()):
    for k,v in sorted(ch.items()): log.write("  "+os.path.basename(f)+" "+k+" -> "+v+"\n")
if APPLY:
    for f,ch in ALL.items(): log.write("PATCH "+f+" "+patch(f,ch)+"\n")
    for lang,pairs in app.items():
        with open("tools/_i18n_out/"+lang+".jsonl","a",encoding="utf-8") as fp:
            for i,v in pairs: fp.write(json.dumps({"i":i,"tr":v},ensure_ascii=False)+"\n")
    log.write("WROTE (APPLY=1)\n")
else: log.write("DRY RUN\n")
open("tools/_i18n_round3_cidfix.log","w",encoding="utf-8").write(log.getvalue())
print("changes",sum(len(c) for c in ALL.values()),"noref",len(noref),"appends",sum(len(x) for x in app.values()),"APPLY",APPLY)
