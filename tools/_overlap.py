import tomllib

def load(p):
    return tomllib.load(open(p, "rb"))

g = load("src/grf/lang/english.toml")
d = load("src/docs/lang/english.toml")
ge = {v.get("base", "") for k, v in g.items() if isinstance(v, dict)}
de = {v for k, v in d.items() if isinstance(v, str)}
ov = ge & de
print("grf_keys", len(g), "docs_keys", len(d))
print("docs_values_appearing_in_grf", len(ov))
print("docs_values_fresh_needed", len(de - ov))
import sys
sys.stdout.flush()
