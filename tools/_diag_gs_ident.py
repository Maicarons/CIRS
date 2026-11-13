"""List which GS strings are identical-to-English across ALL languages
(i.e. untranslatable strings), to confirm GS completeness is real."""
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
d = ROOT / "src" / "gs" / "lang"
ref = tomllib.load((d / "english.toml").open("rb"))


def vals(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        if "base" in node and isinstance(node["base"], str):
            yield node["base"]
        else:
            for v in node.values():
                yield from vals(v)


ref_pairs = list(ref.items())
identical_keys = []
for key, rv in ref_pairs:
    if not isinstance(rv, dict) or "base" not in rv:
        continue
    rvb = rv["base"]
    is_ident = True
    for p in sorted(d.glob("*.toml")):
        if p.name == "english.toml":
            continue
        t = tomllib.load(p.open("rb"))
        tb = t.get(key, {})
        if isinstance(tb, dict) and tb.get("base") != rvb:
            is_ident = False
            break
    if is_ident:
        identical_keys.append((key, rvb))

print(f"GS strings identical across ALL languages: {len(identical_keys)}")
for k, v in identical_keys:
    print(f"  {k} = {v!r}")
