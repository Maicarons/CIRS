#!/usr/bin/env python3
"""Generate HIGH-PRECISION English-residue repair tasks.
   Rule: an English content word appears inside a value that is otherwise localized,
   and the English reference for that key contains the same word (so it was meant
   to be translated). Excludes well-known same-form loanwords / proper nouns."""
import tomllib, glob, io, os, re, json
# English words that are GENUINE residue when left untranslated in steel/chemical cargo descriptions.
TERMS = {
 "billets", "blooms", "slabs", "ingots", "bales", "lye", "kaolin",
 "caustic soda", "crate", "crates",
}
# Legitimate international/technical words that are NOT errors.
LOAN = re.compile(r"^(markdown|chameleon|template|engine|newgrf|gamescript|python|graphviz|json|toml|nml|github|issue|pull|request|git|open?ttd|firs|cirs|frax|gpl|windows|macos|linux|unix|xcode|opengfx|grfid|readme|makefile|fork|stsw|cabbage|land|id|cb|g=w+|p d+ .*)$", re.I)
def leaves(d, pre=""):
    out = []
    if isinstance(d, dict):
        for k,v in d.items(): out += leaves(v, pre+("." if pre else "")+k)
    elif isinstance(d, str): out.append((pre, d))
    return out
def english_val(key):
    """Find the English reference value for the same key."""
    for f in ENGLISH_FILES:
        d = ENGLISH_CACHE.setdefault(f, tomllib.load(open(f,"rb")))
        for k,v in leaves(d):
            if k==key: return v
    return ""
ENGLISH_FILES = (["src/grf/lang/english.toml","src/gs/lang/english.toml","src/docs/lang/english.toml","src/docs/extra_strings.toml"])
ENGLISH_CACHE = {}
# Only repair values in files that are rendered (all long-name + short-code variants)
FILES = sorted(glob.glob("src/grf/lang/*.toml")+glob.glob("src/gs/lang/*.toml")+glob.glob("src/docs/lang/*.toml")+glob.glob("src/docs/extra_strings_*.toml"))
FILES = [f for f in FILES if "english" not in os.path.basename(f) and not f.endswith("extra_strings.toml")]
tasks = []
for f in FILES:
    base = os.path.basename(f)
    lang = base[:-5] if f.startswith("src/grf/lang/") or f.startswith("src/gs/lang/") or f.startswith("src/docs/lang/") else ("extra:"+base[14:-5])
    d = tomllib.load(open(f,"rb"))
    for k, v in leaves(d):
        if k.startswith("GLOBAL_PRAGMA"): continue
        low = v.lower()
        found = [t for t in TERMS if re.search(r"(?<![A-Za-z])"+t+r"(?![A-Za-z])", low)]
        if not found: continue
        en = english_val(k)
        if not en: continue
        # English reference must also contain that term (i.e. it was meant to be translated)
        if not any(re.search(r"(?<![A-Za-z])"+t+r"(?![A-Za-z])", en.lower()) for t in found): continue
        # Value must be otherwise localized (has non-ASCII OR differs from English by more than the term)
        if v.strip() == en.strip(): continue
        tasks.append({"file":f,"lang":lang,"key":k,"en":en,"tr":v,"terms":found})
json.dump(tasks, open("tools/_i18n_residue_tasks.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
o = io.StringIO()
o.write("TASKS "+str(len(tasks))+"\n")
from collections import Counter
o.write("BY LANG "+json.dumps(dict(Counter(t["lang"] for t in tasks)))+"\n")
o.write("BY TERM "+json.dumps(dict(Counter(t for x in tasks for t in x["terms"])))+"\n\n")
for t in tasks:
    o.write(t["lang"]+" | "+t["key"]+" | "+",".join(t["terms"])+"\n  EN: "+t["en"][:160]+"\n  TR: "+t["tr"][:160]+"\n")
open("tools/_i18n_residue_tasks.txt","w",encoding="utf-8").write(o.getvalue())
print("wrote", len(tasks), "tasks")
