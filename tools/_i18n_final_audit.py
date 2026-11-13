#!/usr/bin/env python3
"""Final completeness audit: classify exact-English-match values per language."""
from __future__ import annotations
import importlib.util, json, re, sys
from collections import Counter
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R, WORK = p.R, p.WORK
PH = re.compile(r"\{([A-Za-z_0-9]*)\}")
CARGO_CODE = re.compile(r"^\{[A-Za-z_0-9]*\}[A-Z0-9]{1,5}$")
BRAND = re.compile(r"^(FIRS|CIRS|OpenTTD|FRAX|NewGRF|GRFID|GPL\(v2\)|Python 3\.11\+|ID|LAND|STSW|CB|CABBAGE|Mild Mild West|BaNaNas|NML|JSON|TOML|makefile|GitHub|Issue|pull request|Total Town Replacement Set|OpenGFX|Windows|macOS|Linux|Unix|Xcode|git|fork|ports tree)([ .]?)$", re.I)
WORDY = re.compile(r"[A-Za-z]{3,}")
def classify(en):
    s = en.strip()
    if p.placeholder_only(s): return "placeholder_template"
    if CARGO_CODE.match(s): return "cargo_id_code"
    if BRAND.match(s): return "brand_or_proper_noun"
    if not WORDY.search(s): return "punctuation_or_symbol"
    return "REAL_TEXT_UNTRANSLATED"
def main():
    lm = p.lang_map(); extras = p.extra_files(lm)
    langs = sorted(k for k in lm if k != "english")
    grand = Counter(); rows = []
    for l in langs:
        c = Counter(); detail = []
        for grp, tgt, ref in p.targets(l, lm, extras):
            en = p.leaves(p.load(R / ref)); tv = p.leaves(p.load(R / tgt))
            for k, ev in en.items():
                if p.SKIP_KEY.match(k) or p.placeholder_only(ev): continue
                grand["total"] += 1; c["total"] += 1
                v = tv.get(k)
                if v is None: grand["missing_key"] += 1; c["missing_key"] += 1; continue
                if v == ev:
                    cls = classify(ev); grand["same_" + cls] += 1; c["same_" + cls] += 1
                    if cls == "REAL_TEXT_UNTRANSLATED": detail.append((grp, k, ev[:70]))
                elif p.ph(v) == p.ph(ev):
                    grand["translated"] += 1; c["translated"] += 1
                else:
                    grand["bad_placeholder"] += 1; c["bad_placeholder"] += 1
        rows.append((l, c, detail))
    print("GRAND:", json.dumps(dict(grand), ensure_ascii=False))
    print()
    print("language | translated | same_real_text | same_code_brand_loan | total")
    for l, c, detail in rows:
        legit = c["same_placeholder_template"] + c["same_cargo_id_code"] + c["same_brand_or_proper_noun"] + c["same_punctuation_or_symbol"]
        flag = "  <<<" if c["same_REAL_TEXT_UNTRANSLATED"] else ""
        print(f"  {l:<24} {c['translated']:>5} {c['same_REAL_TEXT_UNTRANSLATED']:>5} {legit:>5} {c['total']:>5}{flag}")
    print()
    print("=== REAL_TEXT_UNTRANSLATED detail (max 60) ===")
    n = 0
    for l, c, detail in rows:
        for grp, k, ev in detail:
            print(f"  {l:<20} {grp:<6} {k:<38} {ev}")
            n += 1
            if n >= 60: break
        if n >= 60: break
    if n == 0: print("  (none)")
    print()
    print("=== hard errors ===")
    print("  missing_key=", grand["missing_key"], " bad_placeholder=", grand["bad_placeholder"])
    sys.exit(1 if grand["missing_key"] or grand["bad_placeholder"] else 0)
if __name__ == "__main__": main()
