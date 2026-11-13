"""Apply the AI-written translations (de, es, pt, ko, ar) to the generated
language files. Driven by the authoritative FR key order in tools/_frkeys.txt,
so each language file is just one translation per line, in that order.

Each target file is first RESET to its English source (preserving the
[GLOBAL_PRAGMA] / grflangid), then the translations are applied. This makes
re-runs idempotent and safe even if a previous run wrote shifted values.
"""
from __future__ import annotations

import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import _ai_translate as A  # noqa: E402

ASSIGN_RE = re.compile(r'^(\s*)(\w+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*)$')

KEYS = [
    line
    for line in open(os.path.join(ROOT, "tools", "_frkeys.txt"), encoding="utf-8")
    .read()
    .split("\n")
    if line != ""
]

# language -> translation file suffix; target file mapping comes from A.TARGETS
LANGS = {
    "german": "de",
    "spanish": "es",
    "portuguese": "pt",
    "korean": "ko",
    "arabic": "ar",
}

# kind -> English source file (relative to ROOT)
SOURCES = {
    "grf": os.path.join("src", "grf", "lang", "english.toml"),
    "gs": os.path.join("src", "gs", "lang", "english.toml"),
    "extra": os.path.join("src", "docs", "extra_strings.toml"),
}


def reset_to_english(target: str, source: str) -> None:
    t = open(target, encoding="utf-8").read().split("\n")
    s = open(source, encoding="utf-8").read().split("\n")
    out = []
    in_pragma = False
    for i in range(max(len(t), len(s))):
        tl = t[i] if i < len(t) else ""
        sl = s[i] if i < len(s) else ""
        if re.match(r"^\[GLOBAL_PRAGMA\]\s*$", tl):
            in_pragma = True
            out.append(tl)
            continue
        if re.match(r"^\[\w+\]\s*$", tl):
            in_pragma = False
            out.append(tl)
            continue
        if in_pragma:
            out.append(tl)
            continue
        mt = ASSIGN_RE.match(tl)
        ms = ASSIGN_RE.match(sl)
        if mt and ms and mt.group(2) == ms.group(2):
            out.append(f"{mt.group(1)}{mt.group(2)}{mt.group(3)}{ms.group(4)}{mt.group(5)}")
        else:
            out.append(tl)
    open(target, "w", encoding="utf-8", newline="").write("\n".join(out))


def load_translations(suffix: str):
    path = os.path.join(ROOT, "tools", f"_lang_{suffix}.txt")
    if not os.path.exists(path):
        return None
    return [line.rstrip("\n") for line in open(path, encoding="utf-8") if line.strip() != ""]


def placeholder_check(key: str, val: str):
    for tok in ("{BLACK}", "{WHITE}", "{YELLOW}", "{ORANGE}", "{BLUE}",
               "{INDUSTRY}", "{VOLUME}", "{WEIGHT}", "{SIGNED_WORD}",
               "{RAW_STRING}"):
        if key.startswith(tok):
            if not val.startswith(tok):
                return f"placeholder mismatch: key starts {tok} but val '{val[:30]}'"
    return None


def main() -> None:
    for lang, suffix in LANGS.items():
        lines = load_translations(suffix)
        if lines is None:
            print(f"-- skip {lang}: no _lang_{suffix}.txt")
            continue
        if len(lines) != len(KEYS):
            print(f"!! {lang}: {len(lines)} lines vs {len(KEYS)} keys -- SKIP (fix the file)")
            continue
        mapping = {}
        for i in range(len(KEYS)):
            k, v = KEYS[i], lines[i]
            if v == "":
                continue
            warn = placeholder_check(k, v)
            if warn:
                print(f"   [{lang}] {warn}  (key='{k[:40]}')")
            mapping[k] = v
        for kind, fname in A.TARGETS[lang].items():
            if kind == "grf":
                tgt = os.path.join(ROOT, "src", "grf", "lang", fname)
            elif kind == "gs":
                tgt = os.path.join(ROOT, "src", "gs", "lang", fname)
            else:
                tgt = os.path.join(ROOT, "src", "docs", fname)
            reset_to_english(tgt, os.path.join(ROOT, SOURCES[kind]))
            cnt = A.apply_translations(tgt, mapping)
            print(f"{lang} {kind}: {cnt} values translated")


if __name__ == "__main__":
    main()
