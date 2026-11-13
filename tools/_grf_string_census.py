import io, re, glob, os, collections
b=open("generated/cirs.grf","rb").read()
out=io.open("tools/_grf_string_census.txt","w",encoding="utf-8")
def W(s=""): out.write(s+"\n")
W("=== C3 9E-marked UTF-8 strings physically stored in cirs.grf ===")
pos=0; rows=collections.Counter(); samples=collections.defaultdict(list)
while True:
    i=b.find(b"\xC3\x9E",pos)
    if i<0: break
    pos=i+2; j=pos
    while j<len(b) and b[j]>=0x20 and b[j]!=0x7F and b[j]!=0xFF: j+=1
    raw=b[pos:j]
    try: s=raw.decode("utf-8")
    except Exception: s=raw.decode("utf-8","replace")
    s=s.strip()
    if len(s)>=2:
        hang=sum(1 for c in s if '\uac00'<=c<='\ud7a3')
        kana=sum(1 for c in s if '\u3040'<=c<='\u30ff')
        cjk=sum(1 for c in s if '\u4e00'<=c<='\u9fff')
        cyr=sum(1 for c in s if '\u0400'<=c<='\u04ff')
        ara=sum(1 for c in s if '\u0600'<=c<='\u06ff')
        tam=sum(1 for c in s if '\u0b80'<=c<='\u0bff')
        key=max([("hangul",hang),("kana",kana),("cjk",cjk),("cyrillic",cyr),("arabic",ara),("tamil",tam),("latin",0)],key=lambda x:x[1])[0]
        if max(hang,kana,cjk,cyr,ara,tam)==0: key="latin_or_ascii"
        rows[key]+=1
        if len(samples[key])<6: samples[key].append((i,s[:100]))
    if pos>len(b)-2: break
W("total C3 9E strings: %d"%sum(rows.values()))
for k,v in rows.most_common(): W("  %-14s %d"%(k,v))
W(""); W("=== samples per script ===")
for k,ss in samples.items():
    W("  "+k+":")
    for off,s in ss: W("    @%d %s"%(off,s))
W(""); W("=== nmlc-warning lines in korean.lng / croatian.lng / czech.lng ===")
for lang,lines in [("korean",[56,57,114]),("croatian",[114,115]),("czech",[114,115]),("japanese",[114,115]),("russian",[83,84])]:
    p="generated/lang/"+lang+".lng"
    ls=io.open(p,encoding="utf-8").read().splitlines()
    W("  --- "+lang)
    for n in lines:
        if n<=len(ls): W("    %d: %s"%(n,ls[n-1][:240]))
W(""); W("=== GLOBAL_PRAGMA in src/grf/lang/*.toml (gender / case / plural / grflangid) ===")
for p in sorted(glob.glob("src/grf/lang/*.toml")):
    txt=io.open(p,encoding="utf-8").read()
    m=re.search(r"\[GLOBAL_PRAGMA\](.*?)(?=\n\[|\Z)",txt,re.S)
    line=" ".join(x.strip() for x in m.group(1).splitlines() if x.strip() and not x.strip().startswith("#")) if m else "MISSING"
    W("  %-26s %s"%(os.path.basename(p)[:-5],line[:150]))
W(""); W("=== FIRS 4.x corpus headers (gender/case/plural) for the 19 warned languages ===")
warn=["belarusian","catalan","croatian","czech","gaelic","galician","indonesian","italian","japanese","korean","latin","norwegian_bokmal","polish","russian","serbian","slovak","spanish_MX","traditional_chinese","turkish"]
for l in warn:
    p="tools/_4x_ref/"+l+".lng"
    if not os.path.exists(p): W("  %-24s (no corpus)"%l); continue
    h=[x for x in io.open(p,encoding="utf-8").read().splitlines()[:10] if x.startswith("##")]
    W("  %-24s %s"%(l," | ".join(h)))
out.close(); print("WROTE tools/_grf_string_census.txt")
print("scripts",dict(rows))
