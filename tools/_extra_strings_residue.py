import os, re, io, json, glob, collections
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
base=parse("src/docs/extra_strings.toml")
NATIVE={
 "korean": lambda c:'\uac00'<=c<='\ud7a3' or '\u3130'<=c<='\u318f',
 "japanese": lambda c:('\u3040'<=c<='\u30ff') or ('\u4e00'<=c<='\u9fff'),
 "simplified_chinese": lambda c:'\u4e00'<=c<='\u9fff',
 "traditional_chinese": lambda c:'\u4e00'<=c<='\u9fff',
 "russian": lambda c:'\u0400'<=c<='\u04ff',
 "belarusian": lambda c:'\u0400'<=c<='\u04ff',
 "serbian": lambda c:'\u0400'<=c<='\u04ff',
 "arabic": lambda c:'\u0600'<=c<='\u06ff',
 "tamil": lambda c:'\u0b80'<=c<='\u0bff',
}
SHORT2LONG={"ar":"arabic","de":"german","es":"spanish","fr":"french","ko":"korean","pt":"portuguese","zh":"simplified_chinese"}
ENSTOP=set("the and of to in a an is are for with on by from that this it as be or at not you your we will can use used using each other more less than when if into out up all per from about which what who how make made have has had do does did been being their its over under also only same such very much many some any no yes via then once every most some".split())
URLPATH=re.compile(r"(https?://|www\.|src/|docs/|generated/|\.toml|\.md|\.png|\.py|\.lng|\.nut|/CIRS/)")
def strip(s): return PH.sub(" ",s)
def classify(lang, key, val, en):
    s=strip(val); es=strip(en)
    letters=re.findall(r"[A-Za-z]+",s)
    if len(letters)<2: return None
    if URLPATH.search(s): return None
    n=NATIVE.get(lang)
    if n is not None:
        if not any(n(c) for c in s):
            hits=sum(1 for w in letters if w.lower() in ENSTOP)
            if hits>=1 or len(letters)>=3: return "no_native_script"
    else:
        special=any(ord(c)>127 and c.isalpha() for c in s)
        hits=sum(1 for w in letters if w.lower() in ENSTOP)
        if not special and hits>=2 and len(letters)>=5: return "english_sentence"
    return None

rows={}; flags=collections.defaultdict(list)
for p in sorted(glob.glob("src/docs/extra_strings_*.toml")):
    b=os.path.basename(p)[len("extra_strings_"):-5]
    lang=SHORT2LONG.get(b,b)
    tr=parse(p)
    cnt=0
    for k,en in base.items():
        v=tr.get(k,"")
        w=classify(lang,k,v,en)
        if w:
            cnt+=1; flags[b].append((k,w,en[:140].replace("\n","\\n"),v[:140].replace("\n","\\n")))
    rows[b]=(len(tr),cnt)
print("=== extra_strings English-residue / missing-native-script flags ===")
for b in sorted(rows,key=lambda x:-rows[x][1]): print("  %-24s keys=%3d flagged=%3d" % (b,rows[b][0],rows[b][1]))
print("TOTAL flagged", sum(r[1] for r in rows.values()))
with io.open("tools/_extra_strings_residue.txt","w",encoding="utf-8") as f:
    f.write("EXTRA_STRINGS naturalness audit (non-Latin: zero native chars; Latin: English-sentence-like)\n\n")
    for b in sorted(flags,key=lambda x:-len(flags[x])):
        f.write("### "+b+" ("+str(len(flags[b]))+")\n")
        for k,w,en,v in flags[b][:80]: f.write("  "+w+" | "+k+" | EN="+en+" | TR="+v+"\n")
        f.write("\n")
print("WROTE tools/_extra_strings_residue.txt")
print("=== KOREAN (ko/korean) examples ===")
for b in ("ko","korean"):
    fs=flags.get(b,[]); print(" --",b,len(fs))
    for k,w,en,v in fs[:25]: print("    ",k,"|",w,"| EN=",en[:90],"| TR=",v[:90])
