#!/usr/bin/env python3
"""Compare current STR_CARGO_*.cid values against FIRS 4.x human corpus STR_CID_*."""
import importlib.util, json, re, glob, os, io, collections
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
CYR = re.compile("[\u0400-\u04ff]"); CJK = re.compile("[\u4e00-\u9fff]")
KANA = re.compile("[\u3040-\u30ff]"); HANG = re.compile("[\uac00-\ud7af]")
NONLAT = re.compile("[^\x00-\x7f]")
out = io.StringIO()
census=[]
for f in sorted(glob.glob("tools/_4x_ref/*.lng")):
    lang = os.path.basename(f)[:-4]
    ents={}
    for ln in open(f, encoding="utf-8", errors="replace").read().split("\n"):
        m = re.match(r"\s*(STR_CID_[A-Z0-9_]+)\s*:\s*(.*?)\s*$", ln)
        if m: ents[m.group(1)] = m.group(2)
    nonlat = sum(1 for v in ents.values() if NONLAT.search(v))
    census.append((lang, len(ents), nonlat))
out.write("=== 4x corpus STR_CID_ census (lang, total, non-Latin values) ===\n")
for l,t,n in census: out.write("  " + l + " " + str(t) + " " + str(n) + "\n")
CAND = [l for l,t,n in census if n >= 5 and os.path.exists(R/("src/grf/lang/"+l+".toml"))]
out.write("candidates with non-Latin cid corpus: " + json.dumps(CAND) + "\n")
divergences=[]
for lang in CAND:
    ents={}
    for ln in open("tools/_4x_ref/"+lang+".lng", encoding="utf-8", errors="replace").read().split("\n"):
        m = re.match(r"\s*STR_CID_([A-Z0-9_]+)\s*:\s*(.*?)\s*$", ln)
        if m: ents[m.group(1)] = m.group(2)
    cur = p.leaves(p.load(R/("src/grf/lang/"+lang+".toml")))
    hit=0; same=0; diff=[]; absent=0
    for stem, human in ents.items():
        key = "STR_CARGO_"+stem+".cid"
        if key not in cur: absent+=1; continue
        hit+=1
        if cur[key] == human: same+=1
        else: diff.append((key, human, cur[key]))
    out.write("\n=== " + lang + " mapped " + str(hit) + " same " + str(same) + " diff " + str(len(diff)) + " absent_key " + str(absent) + " ===\n")
    for k,h,c in diff[:80]:
        out.write("  " + k + " | 4x: " + h + " | now: " + c + "\n")
        divergences.append({"lang":lang,"key":k,"human":h,"current":c})
json.dump(divergences, open("tools/_i18n_round3_cid.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
open("tools/_i18n_round3_cid.txt","w",encoding="utf-8").write(out.getvalue())
print("wrote", len(out.getvalue()), "chars; candidates", len(CAND), "divergences", len(divergences))
for lang in CAND:
    ds=[d for d in divergences if d["lang"]==lang]
    print("  " + lang + " divergences " + str(len(ds)))
