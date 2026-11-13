#!/usr/bin/env python3
"""Final diagnostic: remaining rebrand flags + all partial-English flags + stale substring scan."""
import json, io, tomllib, glob, os, re
o = io.StringIO()
# --- rebrand leftovers ---
try:
    rb = json.load(open("tools/_i18n_rebrand.json", encoding="utf-8"))
    o.write("=== REBRAND LEFTOVERS ===\n")
    o.write(json.dumps(rb, ensure_ascii=False, indent=1)[:6000] + "\n")
except Exception as e:
    o.write("rebrand read fail " + str(e) + "\n")
# --- partial english flags (all) ---
try:
    pe = json.load(open("tools/_i18n_partial_en.json", encoding="utf-8"))
    o.write("\n=== PARTIAL ENGLISH: all flags ===\n")
    if isinstance(pe, dict):
        for lang, d in sorted(pe.items()):
            if not isinstance(d, dict): continue
            for kind, arr in d.items():
                if not isinstance(arr, list): continue
                for it in arr:
                    if isinstance(it, dict):
                        o.write(lang + " | " + kind + " | " + str(it.get("key", "")) + " | EN: " + str(it.get("en", ""))[:160] + " | TR: " + str(it.get("tr", ""))[:160] + "\n")
                    else:
                        o.write(lang + " | " + kind + " | " + str(it)[:200] + "\n")
    else:
        o.write(str(type(pe)) + " " + str(pe)[:500] + "\n")
except Exception as e:
    o.write("partial read fail " + str(e) + "\n")
# --- targeted stale substring scan over all lang TOMLs ---
o.write("\n=== TARGETED STALE SUBSTRING SCAN ===\n")
PATS = ["FIRS Industry Replacement Set", "See readme", "readme for more", "conflicting new",
        "upstream", "NA City Set parameter 2", "fork of FIRS", "how to use FIRS",
        "with FIRS", "FIRS economies", "web site of FIRS"]
hits = 0
for f in sorted(glob.glob("src/*/lang/*.toml") + glob.glob("src/docs/extra_strings_*.toml")):
    txt = open(f, encoding="utf-8").read()
    for p in PATS:
        if p.lower() in txt.lower():
            # report count and first line
            for ln in txt.split("\n"):
                if p.lower() in ln.lower():
                    o.write(f + " | " + p + " | " + ln.strip()[:200] + "\n"); hits += 1; break
o.write("targeted hits " + str(hits) + "\n")
# --- STR_GRF_DESC.base headers across languages ---
o.write("\n=== STR_GRF_DESC.base HEADER (first 90 chars) ===\n")
for f in sorted(glob.glob("src/grf/lang/*.toml")):
    d = tomllib.load(open(f, "rb"))
    v = d.get("STR_GRF_DESC", {}).get("base", "")
    o.write(os.path.basename(f) + " | " + v[:95] + "\n")
open("tools/_i18n_final_diag.txt", "w", encoding="utf-8").write(o.getvalue())
print("wrote", len(o.getvalue()), "chars")
