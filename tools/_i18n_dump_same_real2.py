#!/usr/bin/env python3
import importlib.util, re
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
CARGO_CODE = re.compile(r"^\{[A-Za-z_0-9]*\}[A-Z0-9]{1,5}$")
BRAND = re.compile(r"^(FIRS|CIRS|OpenTTD|FRAX|NewGRF|GRFID|GPL\(v2\)|Python 3\.11\+|ID|LAND|STSW|CB|CABBAGE|Mild Mild West|BaNaNas|NML|JSON|TOML|makefile|GitHub|Issue|pull request|Total Town Replacement Set|OpenGFX|Windows|macOS|Linux|Unix|Xcode|git|fork|ports tree)([ .]?)$", re.I)
WORDY = re.compile(r"[A-Za-z]{3,}")
def classify(en):
    s = en.strip()
    if p.placeholder_only(s): return "template"
    if CARGO_CODE.match(s): return "code"
    if BRAND.match(s): return "brand"
    if not WORDY.search(s): return "punct"
    return "real"
lm = p.lang_map(); extras = p.extra_files(lm)
lines = []
for l in sorted(k for k in lm if k != 'english'):
    for grp, tgt, ref in p.targets(l, lm, extras):
        en = p.leaves(p.load(R / ref)); tv = p.leaves(p.load(R / tgt))
        for k, ev in en.items():
            if p.SKIP_KEY.match(k) or p.placeholder_only(ev): continue
            if tv.get(k) == ev and classify(ev) == 'real':
                lines.append(f"{l}|{tgt}|{k}|{ev}")
open("tools/_i18n_same_real_files.txt", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("slots", len(lines))
