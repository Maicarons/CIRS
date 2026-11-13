"""Carry over ALL 4.x (FIRS) language translations into the new CIRS mod + docs.

Strategy: match by STRING ID first (CIRS shares 171 grf string IDs with 4.x),
falling back to English-text matching. This carries over real 4.x translations
instead of leaving every string in English.

Strings that did not exist in 4.x stay in English (to be AI-translated later);
the 6 primary languages are later overridden with full AI translations by
_apply_rest.py / _ai_translate.py.
"""
from __future__ import annotations

import os
import re
import sys
import tomllib

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "tools", "_4x_ref")

PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_0-9]*)\}")
ASSIGN_RE = re.compile(r'^(\s*)(\w+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*)$')
DOC_TRANS_RE = re.compile(r'^\s*(DOC_TRANS_LANG_\w+)\s*=\s*".*"\s*$')

# All 4.x languages (the full set, not a subset).
ALL_LANGS = [
    "afrikaans", "belarusian", "catalan", "croatian", "czech", "danish",
    "dutch", "english", "english_au", "english_us", "esperanto", "estonian",
    "finnish", "french", "gaelic", "galician", "german", "hungarian",
    "indonesian", "italian", "japanese", "korean", "latin", "luxembourgish",
    "norwegian_bokmal", "polish", "portuguese", "portuguese_BR", "romanian",
    "russian", "serbian", "simplified_chinese", "slovak", "spanish",
    "spanish_MX", "swedish", "tamil", "traditional_chinese", "turkish", "welsh",
    "arabic",
]

# Languages with no 4.x .lng reference: supply grflangid/plural directly.
KNOWN_IDS = {"arabic": ("0x3C", "0")}

# Languages we fully AI-translate ourselves (overridden later by _apply_rest).
PRIMARY = {"french", "german", "spanish", "portuguese", "korean", "arabic"}

# Native names for the docs language switcher (shown in every language file).
NATIVE_NAMES = {
    "afrikaans": "Afrikaans", "belarusian": "Беларуская", "catalan": "Català",
    "croatian": "Hrvatski", "czech": "Čeština", "danish": "Dansk",
    "dutch": "Nederlands", "english": "English", "english_au": "English (AU)",
    "english_us": "English (US)", "esperanto": "Esperanto", "estonian": "Eesti",
    "finnish": "Suomi", "french": "Français", "gaelic": "Gàidhlig",
    "galician": "Galego", "german": "Deutsch", "hungarian": "Magyar",
    "indonesian": "Indonesia", "italian": "Italiano", "japanese": "日本語",
    "korean": "한국어", "latin": "Latina", "luxembourgish": "Lëtzebuergesch",
    "norwegian_bokmal": "Norsk (Bokmål)", "polish": "Polski",
    "portuguese": "Português", "portuguese_BR": "Português (BR)",
    "romanian": "Română", "russian": "Русский", "serbian": "Српски",
    "simplified_chinese": "简体中文", "slovak": "Slovenčina",
    "spanish": "Español", "spanish_MX": "Español (MX)", "swedish": "Svenska",
    "tamil": "தமிழ்", "traditional_chinese": "繁體中文", "turkish": "Türkçe",
    "welsh": "Cymraeg", "arabic": "العربية",
}

SWITCHER_CODES = [c.upper() for c in ALL_LANGS]


def fix_mojibake(s: str) -> str:
    s = "".join(
        ch for ch in s
        if not (0xE000 <= ord(ch) <= 0xF8FF) and (ord(ch) >= 0x20 or ch in "\t")
    )
    try:
        repaired = s.encode("latin1").decode("utf-8")
        if repaired != s and "\ufffd" not in repaired and any(ord(c) > 127 for c in repaired):
            return repaired
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return s


def parse_pragma(path: str):
    gid = plural = None
    if not os.path.exists(path):
        return gid, plural
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            if gid and plural:
                break
            m = re.match(r"##grflangid\s+(\S+)", line)
            if m:
                gid = m.group(1)
            m = re.match(r"##plural\s+(\S+)", line)
            if m:
                plural = m.group(1)
    return gid, plural


def load_lng(path: str) -> dict:
    data = {}
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("##"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip()
    return data


_EN4 = None


def en4_lng() -> dict:
    global _EN4
    if _EN4 is None:
        _EN4 = load_lng(os.path.join(REF, "english.lng"))
    return _EN4


def build_ref(lang: str):
    """Return (by_id, by_text) maps of the 4.x translation for `lang`.

    by_id:   {4.x string id -> translated text}   (primary, robust)
    by_text: {4.x english text -> translated text} (fallback)
    """
    tr_path = os.path.join(REF, f"{lang}.lng")
    if not os.path.exists(tr_path):
        return {}, {}
    tr = load_lng(tr_path)
    by_id = {k: fix_mojibake(v) for k, v in tr.items() if v}
    by_text = {}
    for k, ev in en4_lng().items():
        if k in tr and tr[k]:
            by_text[ev] = fix_mojibake(tr[k])
    return by_id, by_text


def placeholders(value: str) -> dict:
    return dict(__import__("collections").Counter(PLACEHOLDER_RE.findall(value)))


def unescape_toml(s: str) -> str:
    out, i = [], 0
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


def translate_value(inner: str, key: str, by_id: dict, by_text: dict) -> str:
    if not inner:
        return inner
    cand = by_id.get(key) or by_text.get(inner)
    if cand is None:
        low = inner.strip().lower()
        cand = next((v for k, v in by_text.items() if k.strip().lower() == low), None)
    if cand is None:
        return inner
    if placeholders(inner) != placeholders(cand):
        return inner
    return cand


def process_text(text: str, by_id: dict, by_text: dict, lang_id=None, plural=None,
                 doc_names=None) -> str:
    out = []
    in_pragma = False
    current_key = None
    for line in text.split("\n"):
        msec = re.match(r'^\[(\w+)\]\s*$', line)
        if msec:
            in_pragma = (msec.group(1) == "GLOBAL_PRAGMA")
            current_key = msec.group(1)
            out.append(line)
            continue
        if in_pragma:
            if re.match(r'\s*grflangid\s*=', line):
                out.append(f'grflangid = "{lang_id}"')
                continue
            if re.match(r'\s*plural\s*=', line):
                out.append(f'plural = "{plural}"')
                continue
            out.append(line)
            continue
        if doc_names is not None:
            m = DOC_TRANS_RE.match(line)
            if m:
                key = m.group(1)
                code = key[len("DOC_TRANS_LANG_"):].lower()
                newval = doc_names.get(code, NATIVE_NAMES.get(code, ""))
                out.append(f'{key} = "{escape_toml(newval)}"')
                continue
        m = ASSIGN_RE.match(line)
        if m:
            inner = unescape_toml(m.group(4)[1:-1])
            new_inner = translate_value(inner, current_key, by_id, by_text)
            out.append(f'{m.group(1)}{m.group(2)}{m.group(3)}"{escape_toml(new_inner)}"{m.group(5)}')
            continue
        out.append(line)
    return "\n".join(out)


def generate() -> None:
    grf_en = tomllib.load(open(os.path.join(ROOT, "src", "grf", "lang", "english.toml"), "rb"))

    for lang in ALL_LANGS:
        if lang in ("english", "english_au", "english_us"):
            continue  # english is the base; variants are english text
        gid, plural = parse_pragma(os.path.join(REF, f"{lang}.lng"))
        if gid is None:
            gid, plural = KNOWN_IDS.get(lang, (None, None))
        if gid is None:
            print(f"skip {lang}: no grflangid available")
            continue
        by_id, by_text = build_ref(lang)
        doc_names = {c.lower(): NATIVE_NAMES.get(c.lower(), "") for c in SWITCHER_CODES}

        # grf
        grf_src = os.path.join(ROOT, "src", "grf", "lang", "english.toml")
        grf_out = process_text(open(grf_src, encoding="utf-8").read(), by_id, by_text,
                               lang_id=gid, plural=str(plural))
        open(os.path.join(ROOT, "src", "grf", "lang", f"{lang}.toml"),
             "w", encoding="utf-8", newline="").write(grf_out)

        # gs
        gs_src = os.path.join(ROOT, "src", "gs", "lang", "english.toml")
        gs_out = process_text(open(gs_src, encoding="utf-8").read(), by_id, by_text)
        open(os.path.join(ROOT, "src", "gs", "lang", f"{lang}.toml"),
             "w", encoding="utf-8", newline="").write(gs_out)

        # docs lang
        docs_src = os.path.join(ROOT, "src", "docs", "lang", "english.toml")
        docs_text = open(docs_src, encoding="utf-8").read()
        docs_out = process_text(docs_text, by_id, by_text, doc_names=doc_names)
        already = set(re.findall(r'DOC_TRANS_LANG_\w+', docs_out))
        missing = [c for c in SWITCHER_CODES if f'DOC_TRANS_LANG_{c}' not in already]
        if missing:
            docs_out += "\n" + "\n".join(
                f'DOC_TRANS_LANG_{c} = "{escape_toml(NATIVE_NAMES.get(c.lower(), ""))}"'
                for c in missing
            ) + "\n"
        open(os.path.join(ROOT, "src", "docs", "lang", f"{lang}.toml"),
             "w", encoding="utf-8", newline="").write(docs_out)

        # extra strings
        extra_src = os.path.join(ROOT, "src", "docs", "extra_strings.toml")
        extra_out = process_text(open(extra_src, encoding="utf-8").read(), by_id, by_text)
        open(os.path.join(ROOT, "src", "docs", f"extra_strings_{lang}.toml"),
             "w", encoding="utf-8", newline="").write(extra_out)

        carried = sum(1 for k in grf_en if k in by_id)
        print(f"{lang:20s} gid={gid} grf_carried={carried}/{len(grf_en)} ({carried / len(grf_en):.0%})")


if __name__ == "__main__":
    generate()
