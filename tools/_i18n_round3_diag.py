#!/usr/bin/env python3
"""Round-3 independent diagnostics over FINAL TOML values. All reports are
   written as UTF-8 files; stdout is ASCII-only."""
import importlib.util, json, re, glob, os, collections
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
PH = re.compile(r"\{[^}]*\}")
BRAND = re.compile(r"FIRS|CIRS|OpenTTD|FRAX|NewGRF|GRFID|GPL|Python|Windows|macOS|Linux|Unix|Xcode|GitHub|Issue|pull request|NML|JSON|TOML|makefile|OpenGFX|Total Town Replacement Set|BaNaNas|Mild Mild West|STSW|CABBAGE", re.I)
STOP = set("the and of to in is are for with on at by from as that this it its be can not no or will may if then than into out up down over under more most some any all each other new use using used available only also via per set".split())
WORD = re.compile(r"[A-Za-z]+")
def rg(*pairs): return re.compile("[" + "".join(chr(a)+"-"+chr(b) for a,b in pairs) + "]")
SCRIPTS = {
 "cjk": rg((0x4e00,0x9fff),(0x3400,0x4dbf)),
 "kana": rg((0x3040,0x30ff)),
 "hangul": rg((0xac00,0xd7af),(0x1100,0x11ff)),
 "cyrillic": rg((0x0400,0x04ff)),
 "arabic": rg((0x0600,0x06ff)),
 "tamil": rg((0x0b80,0x0bff)),
 "greek": rg((0x0370,0x03ff)),
 "devanagari": rg((0x0900,0x097f)),
 "hebrew": rg((0x0590,0x05ff)),
 "thai": rg((0x0e00,0x0e7f)),
}
ALLOW = {"japanese":{"cjk","kana"},"simplified_chinese":{"cjk"},
         "traditional_chinese":{"cjk"},"korean":{"hangul","cjk"},
         "russian":{"cyrillic"},"belarusian":{"cyrillic"},
         "serbian":{"cyrillic"},"arabic":{"arabic"},"tamil":{"tamil"}}
REQUIRED = {"japanese":{"cjk","kana"},"simplified_chinese":{"cjk"},
            "traditional_chinese":{"cjk"},"korean":{"hangul"},
            "russian":{"cyrillic"},"belarusian":{"cyrillic"},
            "arabic":{"arabic"},"tamil":{"tamil"}}
META = re.compile(r"[\u4e00-\u9fff]|[\u3010\u3011]|[\uff08\uff09]")
def clean(s): return BRAND.sub(" ", PH.sub(" ", s))
def content_words(s): return [w.lower() for w in WORD.findall(clean(s)) if len(w) > 2]
def scripts_in(s):
    return {n for n,r in SCRIPTS.items() if r.search(s)}
def dump(path, obj):
    json.dump(obj, open(path,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

def main():
    lm = p.lang_map(); extras = p.extra_files(lm)
    langs = sorted(k for k in lm if k != "english")
    case_only=[]; high=[]; dup_src=collections.defaultdict(lambda: collections.defaultdict(set))
    bad_script=[]; no_script=[]; meta=[]; same_real=[]
    for l in langs:
        for grp, tgt, ref in p.targets(l, lm, extras):
            en = p.leaves(p.load(R / ref)); tv = p.leaves(p.load(R / tgt))
            for k, ev in en.items():
                if p.SKIP_KEY.match(k) or p.placeholder_only(ev): continue
                v = tv.get(k)
                if v is None: continue
                fname = str(tgt).replace("\\","/")
                # (1) case-only fake translation
                if v != ev and v.lower() == ev.lower():
                    case_only.append({"lang":l,"file":fname,"key":k,"en":ev,"tr":v})
                # values identical to English with real text -> same_real candidates
                if v == ev and len(content_words(ev)) >= 1 and not re.match(r"^[\W_]+$", ev):
                    same_real.append({"lang":l,"file":fname,"key":k,"en":ev})
                if v == ev or p.ph(v) != p.ph(ev): continue
                cw = content_words(v); ew = content_words(ev)
                # (2) high overlap with English on long strings (full text)
                if len(ew) >= 5:
                    inter = sum((collections.Counter(ew) & collections.Counter(cw)).values())
                    ov = inter/len(ew)
                    if ov >= 0.6:
                        high.append({"lang":l,"file":fname,"key":k,"en":ev,"tr":v,"overlap":round(ov,2)})
                # (3) duplicate collapse: >=3 distinct long English strings -> same normalized translation
                if len(ew) >= 4:
                    norm = " ".join(v.lower().split())
                    if len(norm) >= 8: dup_src[l][norm].add(ev)
                # (4) unexpected script characters
                det = scripts_in(v)
                unexpected = det - ALLOW.get(l, set())
                if unexpected:
                    bad_script.append({"lang":l,"file":fname,"key":k,"en":ev,"tr":v,"scripts":sorted(unexpected)})
                # (5) missing required script on substantial translated strings
                req = REQUIRED.get(l)
                if req and len(ew) >= 4 and not (det & req):
                    no_script.append({"lang":l,"file":fname,"key":k,"en":ev,"tr":v,"scripts":sorted(det)})
                # (6) CJK / fullwidth meta leak
                if l not in ("japanese","simplified_chinese","traditional_chinese","korean") and META.search(v):
                    meta.append({"lang":l,"file":fname,"key":k,"en":ev,"tr":v})
    dup=[]
    for l, groups in dup_src.items():
        for norm, ens in groups.items():
            if len(ens) >= 3:
                dup.append({"lang":l,"tr":norm,"count":len(ens),"english":sorted(ens)})
    # (7) short-code vs long-name extra_strings consistency
    SHORT = {"zh":"simplified_chinese","fr":"french","de":"german","es":"spanish",
             "pt":"portuguese","ko":"korean","ar":"arabic"}
    groups = collections.defaultdict(list)
    for f in sorted(glob.glob("src/docs/extra_strings_*.toml")):
        stem = os.path.basename(f)[len("extra_strings_"):-len(".toml")]
        if stem == "": continue
        lang = SHORT.get(stem, stem if stem in lm else None)
        if lang and lang != "english": groups[lang].append((stem, f))
    xs=[]
    for l, files in sorted(groups.items()):
        if len(files) < 2: continue
        data = {stem: p.leaves(p.load(R / f)) for stem,f in files}
        stems = list(data)
        for i in range(len(stems)):
            for j in range(i+1,len(stems)):
                a,b = data[stems[i]], data[stems[j]]
                diff = [k for k in a if k in b and a[k] != b[k]]
                xs.append({"lang":l,"a":stems[i],"b":stems[j],"keys":len(a),"diff":len(diff),"sample":[{"key":k,"a":a[k],"b":b[k]} for k in diff[:5]]})
    dump("tools/_i18n_round3_caseonly.json", case_only)
    dump("tools/_i18n_round3_high.json", high)
    dump("tools/_i18n_round3_dup.json", dup)
    dump("tools/_i18n_round3_badscript.json", bad_script)
    dump("tools/_i18n_round3_noscript.json", no_script)
    dump("tools/_i18n_round3_meta.json", meta)
    dump("tools/_i18n_round3_samereal.json", same_real)
    dump("tools/_i18n_round3_xs.json", xs)
    print("case_only", len(case_only), "high_overlap", len(high), "dup_groups", len(dup),
          "bad_script", len(bad_script), "no_script", len(no_script), "meta", len(meta),
          "same_real", len(same_real), "xs_pairs", len(xs))
    print("case_only_by_lang", json.dumps(dict(collections.Counter(x["lang"] for x in case_only))))
    print("high_by_lang", json.dumps(dict(collections.Counter(x["lang"] for x in high))))
    print("dup_by_lang", json.dumps(dict(collections.Counter(x["lang"] for x in dup))))
    print("badscript_by_lang", json.dumps(dict(collections.Counter(x["lang"] for x in bad_script))))
    print("meta_by_lang", json.dumps(dict(collections.Counter(x["lang"] for x in meta))))
    print("xs_diff", json.dumps([(x["lang"],x["a"],x["b"],x["diff"]) for x in xs]))
if __name__ == "__main__": main()
