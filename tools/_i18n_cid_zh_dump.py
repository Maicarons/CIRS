import json, re, tomllib, subprocess, os, glob, collections, sys
sys.path.insert(0,"tools")
import _i18n_pipeline as p
R=p.R
def leaves(txt): return p.leaves(p.load(R/txt))
cur=leaves("src/grf/lang/simplified_chinese.toml")
head=p.leaves(p.load(R/"src/grf/lang/simplified_chinese.toml").__class__(subprocess.check_output(["git","show","HEAD:src/grf/lang/simplified_chinese.toml"]).decode("utf-8"))) if False else None
# proper HEAD parse
def parse(txt):
    d=tomllib.loads(txt); out={}
    for sec,v in d.items():
        if isinstance(v,dict):
            for k,vv in v.items(): out[sec+"."+k]=vv if isinstance(vv,str) else str(vv)
        elif isinstance(v,str): out[sec]=v
    return out
H=parse(subprocess.check_output(["git","show","HEAD:src/grf/lang/simplified_chinese.toml"]).decode("utf-8"))
EN=parse(open(R/"src/grf/lang/english.toml",encoding="utf-8").read())
corpus={}
for ln in open("tools/_4x_ref/simplified_chinese.lng",encoding="utf-8",errors="replace").read().split("\n"):
    m=re.match(r"\s*STR_CID_([A-Z0-9_]+)\s*:\s*(.*?)\s*$",ln)
    if m: corpus[m.group(1)]=m.group(2)
L=[]
L.append("=== 3 DIVERGENCES (HEAD / FIRS4x corpus / CURRENT / English name) ===")
for stem in ["EDIBLE_OIL","QUICKLIME","VEHICLE_BODIES"]:
    k="STR_CARGO_"+stem+".cid"; nk="STR_CARGO_"+stem+".name"
    L.append("%s:"%k)
    L.append("  HEAD    = %r"%H.get(k))
    L.append("  CORPUS  = %r"%corpus.get(stem))
    L.append("  CURRENT = %r"%cur.get(k))
    L.append("  EN name = %r  EN cid = %r"%(EN.get(nk),EN.get(k)))
# all .cid values: collisions
cids=collections.defaultdict(list)
for k,v in cur.items():
    if k.endswith(".cid"): cids[v].append(k)
dups={v:ks for v,ks in cids.items() if len(ks)>1}
L.append("=== CID COLLISIONS in simplified_chinese: %d groups ==="%len(dups))
for v,ks in dups.items(): L.append("  %r -> %s"%(v,ks))
# count cid keys
L.append("CID KEYS %d"%len(cids))
# HEAD collisions too
hc=collections.defaultdict(list)
for k,v in H.items():
    if k.endswith(".cid"): hc[v].append(k)
hd={v:ks for v,ks in hc.items() if len(ks)>1}
L.append("=== HEAD CID COLLISIONS: %d groups ==="%len(hd))
for v,ks in hd.items(): L.append("  %r -> %s"%(v,ks))
# divergent keys not in dups?
L.append("=== divergent keys colliding? ===")
for stem in ["EDIBLE_OIL","QUICKLIME","VEHICLE_BODIES"]:
    k="STR_CARGO_"+stem+".cid"; v=cur.get(k)
    L.append("  %s current=%r group_size=%d"%(k,v,len(cids.get(v,[]))))
open("tools/_i18n_cid_zh_dump.txt","w",encoding="utf-8").write("\n".join(L))
print("OK divergences dumped, current_collisions=%d head_collisions=%d"%(len(dups),len(hd)))
