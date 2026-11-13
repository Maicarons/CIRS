"""Coverage analysis: how many strings per language are still identical to the
English reference (i.e. untranslated). This surfaces genuinely missing
translations that check_translations.py (key-set only) cannot see."""
import os
import tomllib

ROOT = "src"


def load(p):
    with open(p, "rb") as f:
        return tomllib.load(f)


LANGS = sorted(
    l[:-5] for l in os.listdir(f"{ROOT}/grf/lang")
    if l.endswith(".toml") and l != "english.toml"
)


def report(mod):
    en = load(f"{ROOT}/{mod}/lang/english.toml")
    total = len(en)
    print(f"\n=== {mod} (vs english.toml, {total} keys) ===")
    rows = []
    for lang in LANGS:
        p = f"{ROOT}/{mod}/lang/{lang}.toml"
        if not os.path.exists(p):
            rows.append((lang, "MISSING FILE", 0, 0.0))
            continue
        d = load(p)
        same = sum(
            1 for k in en
            if k in d and str(d[k]).strip() == str(en[k]).strip()
        )
        translated = total - same
        rows.append((lang, total, translated, translated / total * 100 if total else 0))
    rows.sort(key=lambda r: r[3])
    for lang, total, translated, pct in rows:
        if isinstance(total, str):
            print(f"  {lang:22s} {total}")
        else:
            print(f"  {lang:22s} {translated:4d}/{total:4d}  {pct:5.1f}%")


report("grf")
report("gs")
report("docs")
