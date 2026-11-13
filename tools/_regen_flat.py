"""Regenerate a mod translation flat file so it contains exactly one line per
NON-EMPTY English key (in order). Empty-base template keys (e.g. STR_STATION)
are dropped from the flat file, so the applier's skip-version build_map aligns
perfectly. Usage: python tools/_regen_flat.py <suffix>"""
import os
import sys
import tomllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def align(en, lines):
    out, p = [], 0
    for k, v in en.items():
        base = v.get("base", "") if isinstance(v, dict) else ""
        if base == "":
            continue
        if p < len(lines):
            out.append(lines[p])
            p += 1
    return out


if __name__ == "__main__":
    suffix = sys.argv[1]
    L = [l.rstrip("\n") for l in open(os.path.join(ROOT, "tools", f"_lang_{suffix}.txt"), encoding="utf-8")]
    gs_start = next(i for i, l in enumerate(L) if l.startswith("{COMPANY}"))
    grf_lines, gs_lines = L[:gs_start], L[gs_start:]
    grf_en = tomllib.load(open(os.path.join(ROOT, "src", "grf", "lang", "english.toml"), "rb"))
    gs_en = tomllib.load(open(os.path.join(ROOT, "src", "gs", "lang", "english.toml"), "rb"))
    grf_a = align(grf_en, grf_lines)
    gs_a = align(gs_en, gs_lines)
    open(os.path.join(ROOT, "tools", f"_lang_{suffix}.txt"), "w", encoding="utf-8").write("\n".join(grf_a + gs_a))
    print(f"{suffix}: grf {len(grf_a)} (was {len(grf_lines)}), gs {len(gs_a)} (was {len(gs_lines)})")
