"""Idempotent translation applier.

Replaces English source values in a target TOML (grf/gs/docs/extra) with
translations from a {english_value: translation} dict. The target is first
RESET to its English source (preserving [GLOBAL_PRAGMA] / grflangid), then the
dict is applied. Re-running is safe: it always resets first.

Placeholders ({BLACK}, {RAW_STRING}, {COMPANY}, {} etc.) are preserved verbatim
because they live inside the value text that we look up by its English form.
"""
from __future__ import annotations

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ASSIGN_RE = re.compile(r'^(\s*)(\w+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*)$')
STRING_RE = re.compile(r'"((?:[^"\\]|\\.)*)"')


def unescape_toml(s: str) -> str:
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            out.append({"n": "\n", "t": "\t", "\\": "\\", '"': '"'}.get(nxt, c + nxt))
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def escape_toml(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


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


def apply_translations(path: str, lang_map: dict) -> int:
    text = open(path, encoding="utf-8").read()
    changed = 0
    out = []
    in_pragma = False
    for line in text.split("\n"):
        if re.match(r'^\[GLOBAL_PRAGMA\]\s*$', line):
            in_pragma = True
            out.append(line)
            continue
        if re.match(r'^\[\w+\]\s*$', line):
            in_pragma = False
            out.append(line)
            continue
        if in_pragma:
            out.append(line)
            continue
        m = ASSIGN_RE.match(line)
        if m:
            inner = unescape_toml(m.group(4)[1:-1])
            if inner in lang_map:
                out.append(f'{m.group(1)}{m.group(2)}{m.group(3)}"{escape_toml(lang_map[inner])}"{m.group(5)}')
                changed += 1
            else:
                out.append(line)
        else:
            out.append(line)
    open(path, "w", encoding="utf-8", newline="").write("\n".join(out))
    return changed


def translate_file(path: str, lang_map: dict, english_path: str) -> int:
    reset_to_english(path, english_path)
    return apply_translations(path, lang_map)


def apply_file_by_key(path: str, tr: dict) -> int:
    """Replace values by TOML KEY NAME (section name for grf/gs, top-level key
    for docs/lang). Safer than value-matching: no trailing-space pitfalls. Keys
    absent from `tr` are left untouched (e.g. placeholder-only or native names).
    """
    text = open(path, encoding="utf-8").read()
    changed = 0
    out = []
    in_pragma = False
    cur = None
    for line in text.split("\n"):
        if re.match(r'^\[GLOBAL_PRAGMA\]\s*$', line):
            in_pragma = True
            out.append(line)
            continue
        msec = re.match(r'^\[(\w+)\]\s*$', line)
        if msec:
            in_pragma = False
            cur = msec.group(1)
            out.append(line)
            continue
        if in_pragma:
            out.append(line)
            continue
        m = ASSIGN_RE.match(line)
        if m:
            lookup = cur if cur is not None else m.group(2)
            if lookup in tr:
                out.append(f'{m.group(1)}{m.group(2)}{m.group(3)}"{escape_toml(tr[lookup])}"{m.group(5)}')
                changed += 1
            else:
                out.append(line)
        else:
            out.append(line)
    open(path, "w", encoding="utf-8", newline="").write("\n".join(out))
    return changed


def translate_file_by_key(path: str, tr: dict, english_path: str) -> int:
    reset_to_english(path, english_path)
    return apply_file_by_key(path, tr)


if __name__ == "__main__":
    # quick self-test / usage example
    print("use translate_file(path, lang_map, english_path)")
