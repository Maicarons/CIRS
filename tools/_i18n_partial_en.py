#!/usr/bin/env python3
"""Independent partial-English detector over FINAL TOML values (not the out JSONL)."""
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
    s = PH.sub(" ", s)
    s = BRAND.sub(" ", s)
    return s
def content_words(s):
    return [w.lower() for w in WORD.findall(clean(s)) if len(w) > 2]
def main():
    lm = p.lang_map(); extras = p.extra_files(lm)
    langs = sorted(k for k in lm if k != "english")
    out = []
    for l in langs:
        cnt = Counter(); samples = []
        for grp, tgt, ref in p.targets(l, lm, extras):
            en = p.leaves(p.load(R / ref)); tv = p.leaves(p.load(R / tgt))
            for k, ev in en.items():
                if p.SKIP_KEY.match(k) or p.placeholder_only(ev): continue
                v = tv.get(k)
                if v is None or v == ev: continue
                if p.ph(v) != p.ph(ev): continue
                c = clean(v); words = content_words(v)
                # (a) standalone English function words in a translated string
                stops = [w for w in words if w in STOP]
                # (b) Latin residue in non-Latin-script languages
                latin = len(re.findall(r"[A-Za-z]", c)); nonascii = len(re.findall(r"[^\x00-\x7F]", c))
                ratio = latin / (latin + nonascii) if (latin + nonascii) else 0
                # (c) high overlap with English content words on long strings
                ew = content_words(ev); overlap = 0
                if len(ew) >= 5:
                    inter = sum((Counter(ew) & Counter(words)).values())
                    overlap = inter / len(ew)
                flag = None
                if l in NONLATIN and ratio > 0.35 and len(c.strip()) >= 8: flag = "latin_ratio"
                elif stops and len(stops) >= 2 and len(words) >= 4: flag = "en_stopwords"
                elif overlap >= 0.6: flag = "high_overlap"
                if flag:
                    cnt[flag] += 1
                    if len(samples) < 6: samples.append({"file":tgt,"key":k,"en":ev[:90],"tr":v[:90],"flag":flag,"ratio":round(ratio,2),"overlap":round(overlap,2),"stops":stops[:6]})
        if cnt:
            out.append({"lang":l,"counts":dict(cnt),"samples":samples})
    total = Counter()
    for o in out: total.update(o["counts"])
    json.dump({"total":dict(total),"languages":out}, open("tools/_i18n_partial_en.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("TOTAL", json.dumps(dict(total), ensure_ascii=False), "languages", len(out))
    for o in out[:20]:
        print(o["lang"].ljust(22), json.dumps(o["counts"], ensure_ascii=False))
        for s in o["samples"][:2]:
            try: print("    ", s["flag"], "|", s["en"], "=>", s["tr"])
            except UnicodeEncodeError: print("    ", s["flag"])
if __name__ == "__main__": main()
