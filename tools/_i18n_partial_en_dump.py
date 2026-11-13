#!/usr/bin/env python3
import json, io
p = json.load(open("tools/_i18n_partial_en.json", encoding="utf-8"))
o = io.StringIO()
o.write("TYPE " + type(p).__name__ + "\n")
if isinstance(p, dict):
    o.write("TOP KEYS " + str(list(p.keys())[:12]) + "\n")
    o.write("SAMPLE " + json.dumps(p, ensure_ascii=False)[:1200] + "\n\n")
    def walk(x, path=""):
        if isinstance(x, dict):
            for k,v in x.items(): walk(v, path+"/"+str(k))
        elif isinstance(x, list):
            for i,v in enumerate(x[:400]): walk(v, path+"/"+str(i))
        else:
            o.write(path + " = " + str(x)[:300] + "\n")
    walk(p)
open("tools/_i18n_partial_en_all.txt","w",encoding="utf-8").write(o.getvalue())
print("wrote", len(o.getvalue()))
