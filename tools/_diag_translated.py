"""Diagnose how much of each translation is actually non-English.

For every non-english language file in grf/lang, gs/lang, docs/lang,
count string values that are byte-identical to the English source.
A high identical-ratio means the file is effectively untranslated
(structure passes the validator but values are still English).
"""
import os
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict:
    with path.open("rb") as fp:
        return tomllib.load(fp)


def values(node):
    """Yield (value) for every string leaf. grf/gs use nested {key: {base: str}};
    docs use flat {key: str}."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        if "base" in node and isinstance(node["base"], str):
            yield node["base"]
        else:
            for v in node.values():
                yield from values(v)


def compare(ref_path: Path, lang_path: Path):
    ref = load(ref_path)
    tgt = load(lang_path)
    ref_vals = list(values(ref))
    tgt_vals = list(values(tgt))
    total = len(tgt_vals)
    if total == 0:
        return 0, 0
    identical = sum(1 for a, b in zip(ref_vals, tgt_vals) if a == b)
    return identical, total


def scan(kind: str, rel_dir: str):
    d = ROOT / rel_dir
    ref = d / "english.toml"
    if not ref.exists():
        print(f"[skip] {rel_dir}: no english.toml")
        return
    print(f"=== {kind} ({rel_dir}) ===")
    for p in sorted(d.glob("*.toml")):
        if p.name == "english.toml":
            continue
        ident, total = compare(ref, p)
        ratio = ident / total if total else 0
        flag = "  <-- CHECK (likely untranslated)" if ratio >= 0.5 and total > 0 else ""
        print(f"  {p.stem:20s} identical={ident:4d}/{total:4d}  ({ratio:5.1%}){flag}")


scan("GRF", "src/grf/lang")
scan("GS", "src/gs/lang")
scan("DOCS", "src/docs/lang")
