#!/usr/bin/env python3
"""Scan ALL final TOML values for specific untranslated English content words."""
import tomllib, glob, io, os, re
BAD = re.compile(r"\b(billets|blooms|ingots|slabs|Parameter name|Locations:|Supply crates required|Current production|Normal production|Enhanced production|increase production|deliver|Landscaping objects|Glassworks|Kaolin|Lye|Bales|Wool|Engineering Supplies|Farm Supplies)\b", re.I)
o = io.StringIO()
hits = 0
for f in sorted(glob.glob("src/grf/lang/*.toml") + glob.glob("src/gs/lang/*.toml") + glob.glob("src/docs/lang/*.toml") + glob.glob("src/docs/extra_strings_*.toml")):
    if "english" in os.path.basename(f) or f.endswith("extra_strings.toml"): continue
    d = tomllib.load(open(f, "rb"))
    def leaves(x, pre=""):
        out = []
        if isinstance(x, dict):
            for k,v in x.items(): out += leaves(v, pre + ("." if pre else "") + k)
        elif isinstance(x, str): out.append((pre, x))
        return out
    for k, v in leaves(d):
        m = BAD.search(v)
        if m and k != "GLOBAL_PRAGMA":
            hits += 1
            o.write(os.path.basename(f) + " | " + k + " | " + m.group(0) + " | " + v[:150] + "\n")
o.write("TOTAL " + str(hits) + "\n")
open("tools/_i18n_english_word_residue.txt","w",encoding="utf-8").write(o.getvalue())
print("wrote", hits, "hits")
