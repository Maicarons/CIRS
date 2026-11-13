#!/usr/bin/env python3
"""Detect stale rebrand + case-only-English translations across all 4 groups."""
import importlib.util, json, re
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
def scan():
    lm = p.lang_map(); extras = p.extra_files(lm)
    langs = sorted(k for k in lm if k != "english")
    stale = []; grf_desc = []; case_only = []
    for l in langs:
        for grp, tgt, ref in p.targets(l, lm, extras):
            en = p.leaves(p.load(R / ref)); tv = p.leaves(p.load(R / tgt))
            for k, ev in en.items():
                if p.SKIP_KEY.match(k) or p.placeholder_only(ev): continue
                v = tv.get(k)
                if v is None: continue
                ef, tf = len(re.findall(r"FIRS", ev)), len(re.findall(r"FIRS", v))
                ec, tc = len(re.findall(r"CIRS", ev)), len(re.findall(r"CIRS", v))
                reasons = []
                if tf > ef: reasons.append("firs_overuse(+%d)" % (tf-ef))
                if ec > 0 and tc == 0: reasons.append("cirs_missing")
                if v != ev and v.strip().lower() == ev.strip().lower(): reasons.append("english_case_only")
                if reasons:
                    stale.append({"lang":l,"file":tgt,"key":k,"en":ev,"tr":v,"reasons":reasons,"efirs":ef,"tfirs":tf,"ecirs":ec,"tcirs":tc})
                if k == "STR_GRF_DESC.base": grf_desc.append({"lang":l,"tr":v,"en":ev})
                if v != ev and v.strip().lower() == ev.strip().lower(): case_only.append({"lang":l,"file":tgt,"key":k,"en":ev,"tr":v})
    json.dump({"stale":stale,"grf_desc":grf_desc,"case_only":case_only}, open("tools/_i18n_rebrand.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("stale", len(stale), "grf_desc", len(grf_desc), "case_only", len(case_only))
    from collections import Counter
    print("reasons", json.dumps(dict(Counter(r for s in stale for r in s["reasons"]))))
    print("langs", json.dumps(dict(Counter(s["lang"] for s in stale))))
if __name__ == "__main__": scan()
