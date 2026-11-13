import os, re, io, glob, collections
SECTION=re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
ASSIGN=re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
ESC={"n":"\n","t":"\t","r":"\r","b":"\b","f":"\f","\\":"\\","\"":"\""}
def unesc(s):
    out=[];i=1
    while i<len(s)-1:
        c=s[i]
        if c=="\\" and i+1<len(s)-1: out.append(ESC.get(s[i+1],s[i+1]));i+=2
        else: out.append(c);i+=1
    return "".join(out)
def parse(p):
    d={};sec=""
    for ln in io.open(p,encoding="utf-8").read().splitlines():
        m=SECTION.match(ln)
        if m: sec=m.group(1);continue
        m=ASSIGN.match(ln)
        if m: d[sec+"."+m.group(2)]=unesc(m.group(4))
    return d
PH=re.compile(r"\{[A-Za-z_0-9]*\}")
def words(s): return set(w.lower() for w in re.findall(r"[A-Za-z]{2,}",PH.sub(" ",s)))
out=io.open("tools/_strict_en_match.txt","w",encoding="utf-8")
def W(s=""): out.write(s+"\n")
GROUPS={"grf":"src/grf/lang/","gs":"src/gs/lang/","docs":"src/docs/lang/"}
main=collections.defaultdict(list)
for g,d in GROUPS.items():
    en=parse(d+"english.toml")
    files=sorted(glob.glob(d+"*.toml"))
    W("=== "+g+" : EXACT English matches on STR_* keys with >=2 English words ===")
    for p in files:
        lang=os.path.basename(p)[:-5]
        if lang=="english": continue
        tr=parse(p); hits=[]; near=[]
        for k,ev in en.items():
            if not k.upper().startswith("STR_"): continue
            ew=words(ev)
            if len(ew)<2: continue
            v=tr.get(k,"")
            if v==ev: hits.append((k,ev,v))
            else:
                tw=words(v); inter=len(ew&tw)
                if len(ew)>=4 and inter/len(ew)>=0.75: near.append((k,ev,v,inter/len(ew)))
        if hits or near:
            W("  "+lang+" exact="+str(len(hits))+" near="+str(len(near)))
            for k,ev,v in hits[:25]: W("    EXACT "+k+" = "+ev[:100].replace("\n","\\n"))
            for k,ev,v,r in near[:15]: W("    NEAR%.2f "%r+k+" | EN="+ev[:90].replace("\n","\\n")+" | TR="+v[:90].replace("\n","\\n"))
            main[g].append((lang,len(hits),len(near)))
W(""); W("=== totals by group ===")
for g,rows in main.items(): W("  "+g+" languages affected="+str(len(rows))+" exact="+str(sum(r[1] for r in rows))+" near="+str(sum(r[2] for r in rows)))
out.close(); print("WROTE tools/_strict_en_match.txt")
print("affected", {g:len(rows) for g,rows in main.items()}, "exact", {g:sum(r[1] for r in rows) for g,rows in main.items()}, "near", {g:sum(r[2] for r in rows) for g,rows in main.items()})
