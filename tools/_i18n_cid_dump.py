import json, re, tomllib, subprocess, os, glob, sys
sys.path.insert(0,"tools")
import _i18n_pipeline as p
R=p.R
cid=[]
for f in glob.glob("tools/_4x_ref/*.lng"):
    lang=os.path.basename(f)[:-4]
    tf=R/("src/grf/lang/"+lang+".toml")
    if not tf.exists(): continue
    ents={}
    for ln in open(f,encoding="utf-8",errors="replace").read().split("\n"):
        m=re.match(r"\s*STR_CID_([A-Z0-9_]+)\s*:\s*(.*?)\s*$",ln)
        if m: ents[m.group(1)]=m.group(2)
    if sum(1 for v in ents.values() if any(ord(c)>127 for c in v))<5: continue
    cur=p.leaves(p.load(tf))
    for stem,h in ents.items():
        k="STR_CARGO_"+stem+".cid"
        v=cur.get(k)
        if v and v!=h and any(ord(c)>127 for c in v):
            cid.append((lang,k,h,v))
print("DIVERGENCES",len(cid))
for x in cid: print("  ",x)
