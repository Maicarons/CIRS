import os, re, io, glob, collections, json
SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
ASSIGN  = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
PH = re.compile(r"\{[A-Za-z_0-9]*\}")
ESC = {"n":"\n","t":"\t","r":"\r","b":"\b","f":"\f","\\":"\\","\"":"\""}
def unesc(s):
    out=[]; i=1
    while i<len(s)-1:
        c=s[i]
        if c=="\\" and i+1<len(s)-1: out.append(ESC.get(s[i+1],s[i+1])); i+=2
        else: out.append(c); i+=1
    return "".join(out)
def parse(p):
    d={}; sec=""
    for ln in io.open(p,encoding="utf-8").read().splitlines():
        m=SECTION.match(ln)
        if m: sec=m.group(1); continue
        m=ASSIGN.match(ln)
        if m: d[sec+"."+m.group(2)]=unesc(m.group(4))
    return d
def realtext(s):
    t=PH.sub(" ",s)
    words=re.findall(r"[A-Za-z]{2,}",t)
    return len(words)>=2, set(w.lower() for w in words)
GROUPS={
 "grf": ("src/grf/lang/english.toml", sorted(glob.glob("src/grf/lang/*.toml"))),
 "gs":  ("src/gs/lang/english.toml",  sorted(glob.glob("src/gs/lang/*.toml"))),
 "docs":("src/docs/lang/english.toml",sorted(glob.glob("src/docs/lang/*.toml"))),
 "extra":("src/docs/extra_strings.toml",sorted(glob.glob("src/docs/extra_strings_*.toml"))),
}
NATIVE={
 "korean": lambda c:'\uac00'<=c<='\ud7a3' or '\u3130'<=c<='\u318f',
 "japanese": lambda c:('\u3040'<=c<='\u30ff') or ('\u4e00'<=c<='\u9fff'),
 "simplified_chinese": lambda c:'\u4e00'<=c<='\u9fff',
 "traditional_chinese": lambda c:'\u4e00'<=c<='\u9fff',
 "russian": lambda c:'\u0400'<=c<='\u04ff',
 "belarusian": lambda c:'\u0400'<=c<='\u04ff',
 "arabic": lambda c:'\u0600'<=c<='\u06ff',
 "tamil": lambda c:'\u0b80'<=c<='\u0bff',
}
SHORT2LONG={"ar":"arabic","de":"german","es":"spanish","fr":"french","ko":"korean","pt":"portuguese","zh":"simplified_chinese"}
ENSTOP=set("the and of to in a an is are for with on by from that this it as be or at not you your we will can use used using each other more less than when if into out up all per about which what who how make made have has had do does did been being their its over under also only same such very much many some any no yes via then once every most after before between during new set sets default value values game games player players town towns industry industries cargo cargos parameter parameters including include includes available rate rates level levels required supply supplied produced amount units unit distance maximum minimum number open close switch see website information including".split())
URLCODE=re.compile(r"(https?://|www\.|src/|docs/|generated/|\.toml|\.md|\.png|\.py|\.lng|\.nut|/CIRS/|\{\}|[{}])")
def langof(base,g):
    b=os.path.basename(base)
    if g=="extra":
        x=b[len("extra_strings_"):-5] if b.startswith("extra_strings_") else "english"
        return SHORT2LONG.get(x,x)
    return b[:-5]
def collect():
    out={}
    for g,(enbase,files) in GROUPS.items():
        en=parse(enbase); langs={}
        for p in files:
            l=langof(p,g)
            if l=="english": continue
            langs[l]=parse(p)
        out[g]=(en,langs)
    return out
def main():
    data=collect()
    perlang=collections.defaultdict(lambda: collections.Counter())
    detail=collections.defaultdict(list)
    keybad=collections.defaultdict(lambda: collections.Counter())
    keyexamples={}
    for g,(en,langs) in data.items():
        alllangs=list(langs.keys())
        for k,ev in en.items():
            ok, ewords = realtext(ev)
            if not ok: continue
            # global constant = byte-identical across every single language -> proper noun / code
            vals=[langs[l].get(k) for l in alllangs]
            if all(v==ev for v in vals): continue
            for l in alllangs:
                v=langs[l].get(k,"")
                if v is None: continue
                ok2,twords=realtext(v)
                if not ok2: continue
                reasons=[]
                if v==ev: reasons.append("IDENTICAL_EN")
                else:
                    inter=len(ewords&twords); ratio=inter/max(1,len(ewords))
                    if ratio>=0.8 and len(ewords)>=4: reasons.append("OVERLAP_%.2f"%ratio)
                n=NATIVE.get(l)
                if n is not None and not any(n(c) for c in v):
                    if len(twords)>=3 and not URLCODE.search(v): reasons.append("NO_NATIVE_SCRIPT")
                if reasons:
                    perlang[l][g]+=1
                    detail[l].append((g,k,",".join(reasons),ev[:120].replace("\n","\\n"),v[:120].replace("\n","\\n")))
                    keybad[g+"::"+k][l]+=1
                    keyexamples.setdefault(g+"::"+k,(ev[:120],v[:120]))
    print("=== HONEST AUDIT: values that are English / untranslated (no brand whitelist) ===")
    print("lang                 grf   gs docs extra  TOTAL")
    for l in sorted(perlang,key=lambda x:-sum(perlang[x].values())):
        c=perlang[l]; tot=sum(c.values())
        print("  %-22s %4d %4d %4d %5d  %5d" % (l,c["grf"],c["gs"],c["docs"],c["extra"],tot))
    print("TOTAL flagged slots", sum(sum(c.values()) for c in perlang.values()))
    print()
    print("=== WORST KEYS (untranslated in the most languages) ===")
    for kk,c in sorted(keybad.items(),key=lambda x:-len(x[1]))[:40]:
        en,ex=keyexamples[kk]
        print("  %3d langs | %s | EN=%s | EX=%s" % (len(c),kk,en[:80],ex[:80]))
    with io.open("tools/_honest_audit.txt","w",encoding="utf-8") as f:
        f.write("HONEST AUDIT — no brand/proper-noun whitelist; global constants excluded\n\n")
        for l in sorted(detail,key=lambda x:-len(detail[x])):
            f.write("### "+l+" ("+str(len(detail[l]))+")\n")
            for g,k,r,ev,v in detail[l]:
                f.write("  ["+g+"] "+r+" | "+k+" | EN="+ev+" | TR="+v+"\n")
            f.write("\n")
    print("WROTE tools/_honest_audit.txt")

def grfbytes():
    p="generated/cirs.grf"
    if not os.path.exists(p): print("GRF MISSING"); return
    b=open(p,"rb").read()
    def count(seq): return b.count(seq.encode("utf-8"))
    probes={"korean_hangul":"커뮤니티","korean_ga":"가","japanese_kana":"の","cjk":"产业","cyrillic":"п","arabic":"ا","tamil":"அ",
            "zh_wenhe":"温和西部","en_mild":"Mild Mild West","grfid":None}
    print("\n=== GRF byte embedding check (generated/cirs.grf, %d bytes) ===" % len(b))
    for name,s in probes.items():
        if s is None: continue
        print("  %-16s %6d hits" % (name,count(s)))
    print("  Hangul syllable-range EA B0.. occurrences:", len(re.findall(b"\xea[\xb0-\xbf][\x80-\xbf]",b)))
    # lng header comparison
    print("\n=== .lng headers: generated vs FIRS 4.x corpus ===")
    for l in ("korean","japanese","russian","serbian","simplified_chinese","tamil","arabic"):
        gp="generated/lang/"+l+".lng"; rp="tools/_4x_ref/"+l+".lng"
        gh=[x for x in io.open(gp,encoding="utf-8").read().splitlines()[:8] if x.startswith("##")] if os.path.exists(gp) else []
        rh=[x for x in io.open(rp,encoding="utf-8").read().splitlines()[:8] if x.startswith("##")] if os.path.exists(rp) else []
        print("  %-22s generated=%s" % (l," | ".join(gh)))
        if rh: print("  %-22s 4x       =%s" % (""," | ".join(rh)))
def main2():
    main(); grfbytes()
main2()
