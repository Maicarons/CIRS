import os, re, io, json, glob, collections
SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
ASSIGN  = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
PH = re.compile(r"\{[A-Za-z_0-9]*\}")
ESC = {"n":"\n","t":"\t","r":"\r","b":"\b","f":"\f","\\":"\\","\"":"\""}
def unesc(s):
    out=[]; i=1
    while i < len(s)-1:
        c=s[i]
        if c=="\\" and i+1 < len(s)-1: out.append(ESC.get(s[i+1], s[i+1])); i+=2
        else: out.append(c); i+=1
    return "".join(out)
def parse(p):
    d={}; sec=""
    for ln in io.open(p, encoding="utf-8").read().splitlines():
        m=SECTION.match(ln)
        if m: sec=m.group(1); continue
        m=ASSIGN.match(ln)
        if m: d[sec+"."+m.group(2)]=unesc(m.group(4))
    return d
def real(s):
    return len(s.strip())>2 and bool(re.search(r"[A-Za-z\u00c0-\ud7ff]", s))
def legit(en):
    b=PH.sub("",en).strip()
    if not b or not real(b): return True
    if re.match(r"^(https?://|www\.|src/|docs/|generated/|\{)", b): return True
    if b.lower() in ("cirs","firs","newgrf","openttd","github","bananas","gpl(v2)","python 3.11+","mild mild west","steeltown"): return True
    if " " not in b and re.fullmatch(r"[A-Za-z0-9_./\-+&']+", b): return True
    return False

base = parse("src/docs/extra_strings.toml")
print("ENGLISH extra_strings keys", len(base))
# map short-code to long-name
XS = {"ar":"arabic","de":"german","es":"spanish","fr":"french","ko":"korean","pt":"portuguese","zh":"simplified_chinese"}
rows=[]; details=collections.defaultdict(list)
for p in sorted(glob.glob("src/docs/extra_strings_*.toml")):
    b=os.path.basename(p)[len("extra_strings_"):-5]
    tr=parse(p)
    miss=[k for k in base if k not in tr]
    empty=[k for k in base if k in tr and not tr[k].strip()]
    badph=[k for k in base if k in tr and sorted(PH.findall(base[k]))!=sorted(PH.findall(tr[k]))]
    same=[k for k in base if k in tr and tr[k]==base[k] and real(base[k]) and not legit(base[k])]
    rows.append((b, len(tr), len(miss), len(empty), len(badph), len(same)))
    for k in same: details[b].append((k, base[k][:110].replace("\n","\\n")))
    for k in miss: details[b].append(("MISSING:"+k, base[k][:110].replace("\n","\\n")))
print("=== per-file: file lang | keys | missing | empty | badph | SAME_AS_ENGLISH ===")
for r in rows: print("  %-24s %4d %4d %4d %4d %5d" % r)
print("=== TOTALS ===")
print("  files", len(rows), "same_english", sum(r[5] for r in rows), "missing", sum(r[2] for r in rows), "empty", sum(r[3] for r in rows))
with io.open("tools/_extra_strings_audit.txt","w",encoding="utf-8") as f:
    f.write("AUDIT src/docs/extra_strings_*.toml vs extra_strings.toml (English)\n")
    f.write("same_english = untranslated real text\n\n")
    for b in sorted(details):
        f.write("### "+b+" ("+str(len(details[b]))+")\n")
        for k,ev in details[b]: f.write("  "+k+" | EN="+ev+"\n")
    f.write("\n=== COUNTS ===\n")
    for r in rows: f.write("  %-24s keys=%4d missing=%4d empty=%4d badph=%4d same=%5d\n" % r)
print("WROTE tools/_extra_strings_audit.txt")
print("=== KOREAN same_english keys (ko + korean) ===")
for b in ("ko","korean"):
    ds=details.get(b,[])
    print(" --",b,len(ds))
    for k,ev in ds[:35]: print("    ",k,"|",ev[:100])
