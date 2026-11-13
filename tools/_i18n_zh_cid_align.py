# Align 3 simplified-Chinese cargo cid values to the FIRS 4.x HUMAN corpus.
# Reason: HEAD human values 食/石/身 diverge from corpus 脂/生/车; corpus is the
# authoritative legacy 2-letter code set and is semantically better (生石灰/车身/油脂).
import json, re, tomllib, subprocess, os, collections, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(os.path.join(ROOT,p),encoding="utf-8").read()
ASSIGN=re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
SECTION=re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
def esc(s): return s.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n").replace("\t","\\t").replace("\r","\\r")
# corpus
corpus={}
for ln in rd("tools/_4x_ref/simplified_chinese.lng").split("\n"):
    m=re.match(r"\s*STR_CID_([A-Z0-9_]+)\s*:\s*(.*?)\s*$",ln)
    if m: corpus[m.group(1)]=m.group(2)
FIX={"STR_CARGO_EDIBLE_OIL.cid":corpus["EDIBLE_OIL"],
     "STR_CARGO_QUICKLIME.cid":corpus["QUICKLIME"],
     "STR_CARGO_VEHICLE_BODIES.cid":corpus["VEHICLE_BODIES"]}
print("FIX",FIX)
# patch TOML
p=os.path.join(ROOT,"src/grf/lang/simplified_chinese.toml")
txt=rd("src/grf/lang/simplified_chinese.toml"); lines=txt.split("\n"); sec=""
changed=[]
for i,ln in enumerate(lines):
    ms=SECTION.match(ln)
    if ms: sec=ms.group(1); continue
    m=ASSIGN.match(ln)
    if not m: continue
    fk=(sec+"."+m.group(2)) if sec else m.group(2)
    if fk in FIX:
        lines[i]="%s%s%s\"%s\"%s"%(m.group(1),m.group(2),m.group(3),esc(FIX[fk]),m.group(5))
        changed.append(fk)
open(p,"w",encoding="utf-8",newline="").write("\n".join(lines))
print("TOML changed",changed)
# mirror into out-JSONL so pipeline apply cannot overwrite
W=json.loads(rd("tools/_i18n_work/simplified_chinese.json")); E=W["entries"] if isinstance(W,dict) else W
ref2i={}
for j,e in enumerate(E):
    for rf in e.get("refs",[]): ref2i[(rf[0].replace("\\","/").lstrip("./"),rf[1])]=j
out_path=os.path.join(ROOT,"tools/_i18n_out/simplified_chinese.jsonl")
app=[]
for fk,v in FIX.items():
    j=ref2i.get(("src/grf/lang/simplified_chinese.toml",fk))
    if j is not None: app.append({"i":j,"tr":v})
    else: print("NO_WORK_REF",fk)
with open(out_path,"a",encoding="utf-8") as fo:
    for o in app: fo.write(json.dumps(o,ensure_ascii=False)+"\n")
print("OUT_APPENDS",app)
