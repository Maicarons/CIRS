#!/usr/bin/env python3
"""Prepare HIGH-PRECISION steel-term repair tasks with semantic hints.
   Excludes legitimate international mineral/chemical names (kaolin, lye, caustic soda, bales)."""
import tomllib, glob, os, re, json, io, collections
SHORT = {"zh":"simplified_chinese","fr":"french","de":"german","es":"spanish","pt":"portuguese","ko":"korean","ar":"arabic"}
KEEP_TERMS = {"billets","blooms","ingots","slabs","crate","crates"}
def lang_of(f):
    b = os.path.basename(f)[:-5]
    if f.startswith(("src/grf/lang/","src/gs/lang/","src/docs/lang/")): return b
    if b.startswith("extra_strings_"):
        c = b[len("extra_strings_"):]
        return SHORT.get(c, c)
    return b
def leaves(d, pre=""):
    out=[]
    if isinstance(d,dict):
        for k,v in d.items(): out += leaves(v, pre+("." if pre else "")+k)
    elif isinstance(d,str): out.append((pre,d))
    return out
T = json.load(open("tools/_i18n_residue_tasks.json", encoding="utf-8"))
tasks = []
for t in T:
    fl = [x for x in t["terms"] if x in KEEP_TERMS]
    if not fl: continue
    t["lang"] = lang_of(t["file"])
    t["fix_terms"] = fl
    tasks.append(t)
# attach sibling examples (same key, other languages, translation != English, no flagged English term)
ALLF = sorted(glob.glob("src/grf/lang/*.toml")+glob.glob("src/gs/lang/*.toml")+glob.glob("src/docs/lang/*.toml")+glob.glob("src/docs/extra_strings_*.toml"))
cache = {}
def val(f,k):
    if f not in cache: cache[f] = dict(leaves(tomllib.load(open(f,"rb"))))
    return cache[f].get(k,"")
for t in tasks:
    ex = []
    for f in ALLF:
        if f == t["file"]: continue
        v = val(f, t["key"])
        if not v or v == t["en"]: continue
        if any(re.search(r"(?<![A-Za-z])"+x+r"(?![A-Za-z])", v.lower()) for x in t["fix_terms"]): continue
        ex.append({"lang":lang_of(f), "tr":v})
        if len(ex) >= 4: break
    t["examples"] = ex
json.dump(tasks, open("tools/_i18n_residue_model_tasks.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
o = io.StringIO()
o.write("TASKS "+str(len(tasks))+"\n")
o.write("BY LANG "+json.dumps(dict(collections.Counter(t["lang"] for t in tasks)))+"\n\n")
for t in tasks:
    o.write(t["lang"]+" | "+os.path.basename(t["file"])+" | "+t["key"]+" | "+",".join(t["fix_terms"])+"\n")
    o.write("  EN: "+t["en"][:170]+"\n  TR: "+t["tr"][:170]+"\n")
    for e in t["examples"]: o.write("  EG["+e["lang"]+"]: "+e["tr"][:150]+"\n")
open("tools/_i18n_residue_model_tasks.txt","w",encoding="utf-8").write(o.getvalue())
print("wrote", len(tasks), "tasks")
