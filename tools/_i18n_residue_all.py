#!/usr/bin/env python3
"""Dump ALL partial-English flags + targeted residue scans to JSON (no console unicode)."""
import importlib.util, json, re
from collections import Counter
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
PH = re.compile(r"\{[^}]*\}")
BRAND = re.compile(r"FIRS|CIRS|OpenTTD|FRAX|NewGRF|GRFID|GPL|Python|Windows|macOS|Linux|Unix|Xcode|GitHub|Issue|pull request|NML|JSON|TOML|makefile|OpenGFX|Total Town Replacement Set|BaNaNas|Mild Mild West|STSW|CABBAGE", re.I)
STOP = set("the and of to in is are for with on at by from as that this it its be can not no or will may if then than into out up down over under more most some any all each other new use using used available only also via per set".split())
WORD = re.compile(r"[A-Za-z]+")
NONLATIN = {"arabic","russian","belarusian","japanese","korean","tamil","simplified_chinese","traditional_chinese"}
def clean(s):
    return BRAND.sub(" ", PH.sub(" ", s))
def words(s):
    return [w.lower() for w in WORD.findall(clean(s)) if len(w) > 2]
def scan():
    lm = p.lang_map(); extras = p.extra_files(lm)
    langs = sorted(k for k in lm if k != "english")
    flags = []; targeted = []
    for l in langs:
        for grp, tgt, ref in p.targets(l, lm, extras):
            en = p.leaves(p.load(R / ref)); tv = p.leaves(p.load(R / tgt))
            for k, ev in en.items():
                if p.SKIP_KEY.match(k) or p.placeholder_only(ev): continue
                v = tv.get(k)
                if v is None or v == ev: continue
                if p.ph(v) != p.ph(ev): continue
                c = clean(v); ws = words(v)
                latin = len(re.findall(r"[A-Za-z]", c)); na = len(re.findall(r"[^\x00-\x7F]", c))
                ratio = latin / (latin + na) if (latin + na) else 0
                ew = words(ev); overlap = 0
                if len(ew) >= 5:
                    overlap = sum((Counter(ew) & Counter(ws)).values()) / len(ew)
                stops = [w for w in ws if w in STOP]
                fl = []
                if l in NONLATIN and ratio > 0.35 and len(c.strip()) >= 8: fl.append("latin_ratio")
                if len(stops) >= 2 and len(ws) >= 4: fl.append("en_stopwords")
                if overlap >= 0.6: fl.append("high_overlap")
                if fl: flags.append({"lang":l,"file":tgt,"key":k,"en":ev,"tr":v,"flags":fl,"ratio":round(ratio,2),"overlap":round(overlap,2),"stops":stops})
                # targeted residue patterns
                tl = v.lower()
                if "firs industry replacement set" in tl: targeted.append({"lang":l,"file":tgt,"key":k,"en":ev,"tr":v,"pattern":"old_firs_name"})
                if "conflicting new" in tl and ("newgrf" in tl or "newgrfs" in tl): targeted.append({"lang":l,"file":tgt,"key":k,"en":ev,"tr":v,"pattern":"conflicting_newgrfs"})
                if "na city set parameter" in tl: targeted.append({"lang":l,"file":tgt,"key":k,"en":ev,"tr":v,"pattern":"na_city_param"})
                if re.search(r"\bupstream\b", v, re.I) and l not in ("english",): targeted.append({"lang":l,"file":tgt,"key":k,"en":ev,"tr":v,"pattern":"upstream"})
    json.dump({"flags":flags,"targeted":targeted}, open("tools/_i18n_residue_all.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("flags", len(flags), "targeted", len(targeted))
    tc = Counter(t["pattern"] for t in targeted)
    print("targeted patterns", json.dumps(dict(tc)))
if __name__ == "__main__": scan()
