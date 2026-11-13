#!/usr/bin/env python3
import importlib.util, json, re, glob, os, io, collections
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
out = io.StringIO()
# (1) checker regex
chk = open("tools/check_translations.py", encoding="utf-8").read()
out.write("=== check_translations.py placeholder-related lines ===\n")
for i,ln in enumerate(chk.split("\n"),1):
    if re.search(r"placeholder|findall|Counter|\{", ln): out.write(str(i) + ": " + ln.strip()[:170] + "\n")
# (2) 4x corpora
for lang, pats in [("indonesian", [r"STATION", r"FACTORY", r"MILL", r"WORKS", r"PLANT"]), ("korean",[r"CID_",r"CHEMICALS",r"SULPHUR",r"SALT"])]:
    f = "tools/_4x_ref/" + lang + ".lng"
    out.write("\n=== 4x_ref/" + lang + ".lng matching lines ===\n")
    if not os.path.exists(f): out.write("MISSING\n"); continue
    for ln in open(f, encoding="utf-8", errors="replace").read().split("\n"):
        if any(re.search(pa, ln, re.I) for pa in pats): out.write("  " + ln.strip()[:170] + "\n")
# (3) Korean cid census
lm = p.lang_map(); extras = p.extra_files(lm)
CIDK = ["STR_CARGO_CHEMICALS.cid","STR_CARGO_CHLORINE.cid","STR_CARGO_PHOSPHATE.cid","STR_CARGO_SALT.cid","STR_CARGO_PYRITE_ORE.cid","STR_CARGO_SULPHUR.cid","STR_CARGO_SULPHURIC_ACID.cid"]
en = p.leaves(p.load(R/"src/grf/lang/english.toml"))
out.write("\n=== Korean cid values vs English + how many langs keep English ===\n")
for k in CIDK:
    ev = en.get(k,"?"); kv = ""
    f = "src/grf/lang/korean.toml"
    kv = p.leaves(p.load(R/f)).get(k,"?")
    keep = 0; tot = 0
    for g in sorted(glob.glob("src/grf/lang/*.toml")):
        if "english" in g: continue
        v = p.leaves(p.load(R/g)).get(k)
        if v is not None: tot += 1; keep += (v == ev)
    out.write("  " + k + " | EN=" + ev + " | KO=" + kv + " | keepEnglish " + str(keep) + "/" + str(tot) + "\n")
# (4) Indonesian station census
STK = ["STR_STATION_FACTORY.base","STR_STATION_HEAVY_INDUSTRY_2.base","STR_STATION_MILL.base","STR_STATION_PLANT.base","STR_STATION_WORKS.base"]
out.write("\n=== Indonesian station keys vs English + sibling distribution ===\n")
for k in STK:
    ev = en.get(k,"?"); cnt = collections.Counter()
    for g in sorted(glob.glob("src/grf/lang/*.toml")):
        if "english" in g: continue
        v = p.leaves(p.load(R/g)).get(k)
        if v is not None: cnt[v] += 1
    out.write("  " + k + " | EN=" + ev + " | ID=" + p.leaves(p.load(R/"src/grf/lang/indonesian.toml")).get(k,"?") + " | top " + json.dumps(cnt.most_common(4), ensure_ascii=False) + "\n")
# (5) dual diff key lists
SHORT = {"fr":"french","de":"german","es":"spanish","zh":"simplified_chinese"}
out.write("\n=== dual-file differing keys (short->long) ===\n")
for code,lang in SHORT.items():
    short = p.leaves(p.load(R/("src/docs/extra_strings_"+code+".toml")))
    long = p.leaves(p.load(R/("src/docs/extra_strings_"+lang+".toml")))
    diff = [k for k in short if k in long and short[k] != long[k]]
    out.write("  " + code + "->" + lang + " diff=" + str(len(diff)) + "\n")
    json.dump(diff, open("tools/_i18n_round3_diff_"+code+".json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    for k in diff[:6]: out.write("    " + k + " | short: " + short[k][:90] + " | long: " + long[k][:90] + "\n")
open("tools/_i18n_round3_evidence.txt","w",encoding="utf-8").write(out.getvalue())
print("wrote", len(out.getvalue()), "chars")
