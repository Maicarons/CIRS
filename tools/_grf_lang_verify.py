import os, io, re, glob, struct, collections
GRF="generated/cirs.grf"
b=open(GRF,"rb").read()
out=io.open("tools/_grf_lang_verify.txt","w",encoding="utf-8")
def W(s=""): out.write(s+"\n")
W("=== GRF header hex (first 48 bytes) ===")
W(" ".join("%02X"%x for x in b[:48]))
PH=re.compile(r"\{[^}]*\}")
def read_lng(p):
    prag={}; ss=[]
    for ln in io.open(p,encoding="utf-8").read().splitlines():
        if ln.startswith("##"):
            q=ln[2:].split(None,1); prag[q[0]]=q[1] if len(q)>1 else ""
        elif ":" in ln and not ln.startswith("#"):
            k,v=ln.split(":",1); ss.append((k.strip(),v.strip()))
    return prag,ss
langs={os.path.basename(p)[:-4]:read_lng(p) for p in sorted(glob.glob("generated/lang/*.lng"))}
def probes(ss,n=80):
    res=[]
    for k,v in ss:
        frags=[f.strip() for f in PH.split(v)]
        frags=[f for f in frags if len(f.encode("utf-8"))>=12]
        if not frags: continue
        f=max(frags,key=lambda x:len(x.encode("utf-8")))
        res.append((k,f))
    return res[:n]
W(""); W("=== Are translated string fragments physically present in cirs.grf? ===")
W("%-24s %-10s %9s  %s"%("lang","grflangid","present","note"))
presence={}
for l in sorted(langs):
    prag,ss=langs[l]; pr=probes(ss); hit=0; miss=[]
    for k,f in pr:
        if b.count(f.encode("utf-8"))>0: hit+=1
        else: miss.append((k,f[:40]))
    presence[l]=(hit,len(pr))
    W("%-24s %-10s %4d/%-3d  %s"%(l,prag.get("grflangid","?"),hit,len(pr),("MISS e.g. "+miss[0][0]) if miss else "all present"))
W(""); W("=== Adaptive GRF container walk ===")
bests=[]
for start in range(8,16):
  for mode in ("A","B"):
    i=start; n=0; acts=collections.Counter(); lang=collections.Counter(); err=""
    while i+5<=len(b) and n<600000:
        size=struct.unpack_from("<I",b,i)[0]
        if size<2 or size>4_000_000: err="bad size @%d"%i; break
        step=4+size if mode=="A" else 5+size
        if i+step>len(b): err="truncated @%d"%i; break
        info=b[i+4]
        data=b[i+5:i+4+size] if mode=="A" else b[i+5:i+5+size]
        if info==0 and data:
            acts[data[0]]+=1
            if data[0]==0x04 and len(data)>=4: lang[data[2]&0x7f]+=1
        i+=step; n+=1
    bests.append((i,n,len(lang),sum(lang.values()),start,mode,err,acts,lang))
bests.sort(key=lambda x:-x[0])
W("top candidates by bytes covered:")
for x in bests[:4]: W("  covered=%d recs=%d distinct=%d a4=%d start=%d mode=%s %s"%(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
i,n,dl,na,start,mode,err,acts,lang=bests[0]
W("chosen start=%d mode=%s covered=%d/%d"%(start,mode,i,len(b)))
W("action first bytes: %s"%repr(acts.most_common(10)))
W("Action4 language-id census (%d distinct, %d records):"%(len(lang),sum(lang.values())))
for k,v in sorted(lang.items()): W("  0x%02X : %d"%(k,v))
W(""); W("=== .lng grflangid -> Action4 count ===")
for l in sorted(langs):
    m=re.search(r"0x([0-9A-Fa-f]+)",langs[l][0].get("grflangid",""))
    lid=int(m.group(1),16) if m else -1
    W("  %-24s 0x%02X  action4=%d  fragments=%d/%d"%(l,lid,lang.get(lid,0),presence[l][0],presence[l][1]))
out.close()
print("WROTE tools/_grf_lang_verify.txt")
print("top", [(x[4],x[5],x[0],x[2],x[3]) for x in bests[:3]])
print("presence", {l:presence[l] for l in ("korean","english","japanese","simplified_chinese","german","welsh")})
