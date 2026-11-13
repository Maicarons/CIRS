#!/usr/bin/env python3
import json, io
p = json.load(open("tools/_i18n_partial_en.json", encoding="utf-8"))
o = io.StringIO()
n = 0
for lang in p.get("languages", []):
    for s in lang.get("samples", []):
        if s.get("flag") == "en_stopwords":
            n += 1
            o.write(lang["lang"] + " | " + s.get("key","") + " | stops=" + str(s.get("stops")) + "\n")
            o.write("  EN: " + str(s.get("en",""))[:200] + "\n")
            o.write("  TR: " + str(s.get("tr",""))[:200] + "\n")
o.write("TOTAL en_stopwords samples " + str(n) + "\n")
# also high_overlap with non-technical keys
o.write("\n=== HIGH_OVERLAP samples (all 25) ===\n")
for lang in p.get("languages", []):
    for s in lang.get("samples", []):
        if s.get("flag") == "high_overlap":
            o.write(lang["lang"] + " | " + s.get("key","") + "\n  EN: " + str(s.get("en",""))[:180] + "\n  TR: " + str(s.get("tr",""))[:180] + "\n")
open("tools/_i18n_en_stops.txt","w",encoding="utf-8").write(o.getvalue())
print("wrote", len(o.getvalue()), "chars")
