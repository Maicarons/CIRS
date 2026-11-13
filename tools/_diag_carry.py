"""Check whether the 4.x carry-over actually maps any CIRS grf/gs keys."""
import os
import tomllib


def load_lng(path):
    d = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("##") or not line.strip():
                continue
            if ":" in line:
                k, _, v = line.partition(":")
                d[k.strip()] = v.strip().strip('"')
    return d


REF = "tools/_4x_ref"
en4 = load_lng(os.path.join(REF, "english.lng"))

for mod in ("grf", "gs"):
    ce = tomllib.load(open(f"src/{mod}/lang/english.toml", "rb"))
    keys = list(ce.keys())
    print(f"\n=== {mod}: CIRS english has {len(keys)} keys ===")
    for lang in ["italian", "french", "german", "spanish", "russian", "japanese"]:
        tr4 = load_lng(os.path.join(REF, f"{lang}.lng"))
        ref_map = {en4[k]: tr4.get(k, "") for k in en4 if tr4.get(k)}
        mapped = sum(
            1 for k in keys
            if str(ce[k]).strip() in ref_map and ref_map[str(ce[k]).strip()]
        )
        print(f"  {lang:10s} mapped {mapped:3d}/{len(keys)}  (4.x en strings: {len(en4)})")
