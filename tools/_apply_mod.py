"""Apply a mod (grf+gs) translation flat file to a language's TOML files.

Aligns by KEY NAME (not by line count), skipping empty-base English keys, so
blank lines in the flat file don't cause shifts. Usage:
    python tools/_apply_mod.py <lang> <suffix>
e.g. python tools/_apply_mod.py portuguese pt
"""
import os
import re
import sys
import tomllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSIGN_RE = re.compile(r'^(\s*)(\w+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*)$')


def build_map(mod: str, flat_lines: list):
    """Consume exactly ONE flat line per English key (1:1 alignment). Empty-base
    template keys consume a flat line but are not assigned. The flat file must
    have one line per English key in order (incl. a blank line for empty-base
    keys / GLOBAL_PRAGMA)."""
    en = tomllib.load(open(os.path.join(ROOT, "src", mod, "lang", "english.toml"), "rb"))
    p = 0
    tmap = {}
    for k, v in en.items():
        base = v.get("base", "") if isinstance(v, dict) else ""
        if p >= len(flat_lines):
            break
        line = flat_lines[p]
        p += 1
        if base != "" and line.strip() != "":
            tmap[k] = line
    return tmap


def apply(mod: str, lang: str, tmap: dict):
    tgt = os.path.join(ROOT, "src", mod, "lang", f"{lang}.toml")
    raw = open(tgt, encoding="utf-8").read().split("\n")
    cur = None
    in_pragma = False
    out = []
    for line in raw:
        if re.match(r"^\[GLOBAL_PRAGMA\]\s*$", line):
            in_pragma = True
            out.append(line)
            continue
        m = re.match(r"^\[(\w+)\]\s*$", line)
        if m:
            in_pragma = False
            cur = m.group(1)
            out.append(line)
            continue
        if in_pragma:
            out.append(line)
            continue
        mm = ASSIGN_RE.match(line)
        if mm and cur in tmap:
            out.append(f'{mm.group(1)}{mm.group(2)}{mm.group(3)}"{tmap[cur]}"{mm.group(5)}')
            continue
        out.append(line)
    open(tgt, "w", encoding="utf-8", newline="").write("\n".join(out))
    print(f"{lang} {mod}: {len(tmap)} strings applied")


if __name__ == "__main__":
    lang, suffix = sys.argv[1], sys.argv[2]
    lines = [l.rstrip("\n") for l in open(os.path.join(ROOT, "tools", f"_lang_{suffix}.txt"), encoding="utf-8")]
    grf_n = len(tomllib.load(open(os.path.join(ROOT, "src", "grf", "lang", "english.toml"), "rb")))
    gm = build_map("grf", lines[:grf_n])
    gs = build_map("gs", lines[grf_n:])
    apply("grf", lang, gm)
    apply("gs", lang, gs)
