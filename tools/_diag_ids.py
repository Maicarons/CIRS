import os
import tomllib


def load_lng(p):
    d = {}
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("##") or not line.strip() or ":" not in line:
                continue
            k, _, v = line.partition(":")
            d[k.strip()] = v.strip().strip('"')
    return d


REF = "tools/_4x_ref"
en4 = set(load_lng(os.path.join(REF, "english.lng")).keys())
print("4.x english string IDs:", len(en4))

for mod in ("grf", "gs"):
    ce = set(tomllib.load(open(f"src/{mod}/lang/english.toml", "rb")).keys())
    print(f"CIRS {mod} string IDs: {len(ce)}  OVERLAP by ID with 4.x: {len(en4 & ce)}")
