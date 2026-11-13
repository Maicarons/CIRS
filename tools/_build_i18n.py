"""Generate CIRS i18n TOML files for the 4.x-referenced languages.

Each output file is produced by copying the English template verbatim and
replacing every string *value* with a translation, keeping keys, attribute
names, comments and order identical (the checker requires this). Translations
are taken from the FIRS 4.x .lng references where the English text matches;
otherwise the English value is kept as a temporary placeholder, exactly as
TRANSLATING.md permits.

Languages produced (all had a 4.x reference except Arabic, which is seeded
from English):
    french, german, spanish, portuguese, korean, arabic
"""
from __future__ import annotations

import os
import re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(ROOT, "tools", "_4x_ref")

PLACEHOLDER_RE = re.compile(r"\{([A-Za-z_0-9]*)\}")


def placeholders(value: str) -> dict:
    return dict(Counter(PLACEHOLDER_RE.findall(value)))


def load_lng(path: str) -> dict[str, str]:
    data: dict[str, str] = {}
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            line = line.rstrip("\n")
            if not line.strip() or line.lstrip().startswith("##"):
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()
    return data


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


def build_ref_maps() -> dict[str, dict[str, str]]:
    maps: dict[str, dict[str, str]] = {}
    lang_files = {
        "german": ["german.lng"],
        "french": ["french.lng"],
        "spanish": ["spanish.lng"],
        "portuguese": ["portuguese.lng", "portuguese_br.lng"],
        "korean": ["korean.lng"],
    }
    for lang, files in lang_files.items():
        en = load_lng(os.path.join(REF, f"{lang}_en.lng"))
        mapping: dict[str, str] = {}
        for fname in files:
            tr = load_lng(os.path.join(REF, fname))
            for k, v in tr.items():
                if k in en:
                    mapping[en[k]] = fix_mojibake(v)
        maps[lang] = mapping
    maps["arabic"] = {}
    return maps


# ---------------------------------------------------------------------------
# target language metadata
# ---------------------------------------------------------------------------
TARGETS = {
    "french":      {"grf_id": "0x03", "plural": "0", "code": "fr", "dir": "fr", "extra": "extra_strings_fr.toml", "display": "DOC_TRANS_LANG_FR"},
    "german":      {"grf_id": "0x02", "plural": "0", "code": "de", "dir": "de", "extra": "extra_strings_de.toml", "display": "DOC_TRANS_LANG_DE"},
    "spanish":     {"grf_id": "0x04", "plural": "0", "code": "es", "dir": "es", "extra": "extra_strings_es.toml", "display": "DOC_TRANS_LANG_ES"},
    "portuguese":  {"grf_id": "0x09", "plural": "0", "code": "pt", "dir": "pt", "extra": "extra_strings_pt.toml", "display": "DOC_TRANS_LANG_PT"},
    "korean":      {"grf_id": "0x55", "plural": "0", "code": "ko", "dir": "ko", "extra": "extra_strings_ko.toml", "display": "DOC_TRANS_LANG_KO"},
    "arabic":      {"grf_id": "0x3C", "plural": "0", "code": "ar", "dir": "ar", "extra": "extra_strings_ar.toml", "display": "DOC_TRANS_LANG_AR"},
}

LANG_NAMES = {
    "english":       {"en": "English", "zh": "Chinese, Simplified", "fr": "French", "de": "German", "es": "Spanish", "pt": "Portuguese", "ko": "Korean", "ar": "Arabic"},
    "simplified_chinese": {"en": "English", "zh": "简体中文", "fr": "法语", "de": "德语", "es": "西班牙语", "pt": "葡萄牙语", "ko": "韩语", "ar": "阿拉伯语"},
    "french":        {"en": "Anglais", "zh": "Chinois simplifié", "fr": "Français", "de": "Allemand", "es": "Español", "pt": "Portugais", "ko": "Coréen", "ar": "Arabe"},
    "german":        {"en": "Englisch", "zh": "Chinesisch (Vereinfacht)", "fr": "Französisch", "de": "Deutsch", "es": "Spanisch", "pt": "Portugiesisch", "ko": "Koreanisch", "ar": "Arabisch"},
    "spanish":       {"en": "Inglés", "zh": "Chino simplificado", "fr": "Francés", "de": "Alemán", "es": "Español", "pt": "Portugués", "ko": "Coreano", "ar": "Árabe"},
    "portuguese":    {"en": "Inglês", "zh": "Chinês Simplificado", "fr": "Francês", "de": "Alemão", "es": "Espanhol", "pt": "Português", "ko": "Coreano", "ar": "Árabe"},
    "korean":        {"en": "영어", "zh": "중국어 간체", "fr": "프랑스어", "de": "독일어", "es": "스페인어", "pt": "포르투갈어", "ko": "한국어", "ar": "아랍어"},
    "arabic":        {"en": "الإنجليزية", "zh": "الصينية المبسطة", "fr": "الفرنسية", "de": "الألمانية", "es": "الإسبانية", "pt": "البرتغالية", "ko": "الكورية", "ar": "العربية"},
}

LANG_CODES = ["en", "zh", "fr", "de", "es", "pt", "ko", "ar"]
LANG_KEYS = ["EN", "ZH", "FR", "DE", "ES", "PT", "KO", "AR"]


# ---------------------------------------------------------------------------
# TOML string handling
# ---------------------------------------------------------------------------
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


def translate_value(value: str, ref_map: dict[str, str]) -> str:
    """Return a translation for `value`, or the original if none is available."""
    if not value:
        return value
    if value in ref_map:
        cand = ref_map[value]
    else:
        low = value.strip().lower()
        cand = next((v for k, v in ref_map.items() if k.strip().lower() == low), None)
    if cand is None:
        return value
    # never change placeholder counts
    if placeholders(value) != placeholders(cand):
        return value
    return cand


ASSIGN_RE = re.compile(r'^(\s*)(\w+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*)$')
DOC_TRANS_RE = re.compile(r'^\s*(DOC_TRANS_LANG_\w+)\s*=\s*".*"\s*$')


def process_text(text: str, ref_map: dict[str, str], lang_id: str | None = None,
                 plural: str | None = None, doc_names: dict[str, str] | None = None) -> str:
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
                newval = doc_names.get(code, "")
                out.append(f'{key} = "{escape_toml(newval)}"')
                continue
        m = ASSIGN_RE.match(line)
        if m:
            inner = unescape_toml(m.group(4)[1:-1])
            new_inner = translate_value(inner, ref_map)
            out.append(f'{m.group(1)}{m.group(2)}{m.group(3)}"{escape_toml(new_inner)}"{m.group(5)}')
            continue
        out.append(line)
    return "\n".join(out)


def ensure_lang_names(path: str, lang: str) -> None:
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()
    names = LANG_NAMES.get(lang, LANG_NAMES["english"])
    extra = []
    for code, key in zip(LANG_CODES, LANG_KEYS):
        name_key = f"DOC_TRANS_LANG_{key}"
        if name_key not in content:
            extra.append(f'{name_key} = "{escape_toml(names[code])}"')
    if extra:
        with open(path, "a", encoding="utf-8", newline="") as fp:
            fp.write("\n" + "\n".join(extra) + "\n")


def generate() -> None:
    ref_maps = build_ref_maps()
    # keep english + simplified_chinese docs lang files in key parity
    ensure_lang_names(os.path.join(ROOT, "src", "docs", "lang", "english.toml"), "english")
    ensure_lang_names(os.path.join(ROOT, "src", "docs", "lang", "simplified_chinese.toml"), "simplified_chinese")

    for lang, meta in TARGETS.items():
        ref_map = ref_maps[lang]
        names = LANG_NAMES.get(lang, LANG_NAMES["english"])

        # grf
        grf_src = os.path.join(ROOT, "src", "grf", "lang", "english.toml")
        grf_text = open(grf_src, encoding="utf-8").read()
        grf_out = process_text(grf_text, ref_map, lang_id=meta["grf_id"], plural=meta["plural"])
        open(os.path.join(ROOT, "src", "grf", "lang", f"{lang}.toml"), "w", encoding="utf-8", newline="").write(grf_out)

        # gs (no pragma)
        gs_src = os.path.join(ROOT, "src", "gs", "lang", "english.toml")
        gs_text = open(gs_src, encoding="utf-8").read()
        gs_out = process_text(gs_text, ref_map)
        open(os.path.join(ROOT, "src", "gs", "lang", f"{lang}.toml"), "w", encoding="utf-8", newline="").write(gs_out)

        # docs lang (flat keys + DOC_TRANS names)
        docs_src = os.path.join(ROOT, "src", "docs", "lang", "english.toml")
        docs_text = open(docs_src, encoding="utf-8").read()
        docs_out = process_text(docs_text, ref_map, doc_names=names)
        # append any DOC_TRANS_LANG_* not already present (preserve order: en,zh,...,ar)
        already = set(re.findall(r'DOC_TRANS_LANG_\w+', docs_out))
        missing = [f'DOC_TRANS_LANG_{k}' for k in LANG_KEYS if f'DOC_TRANS_LANG_{k}' not in already]
        if missing:
            docs_out += "\n" + "\n".join(
                f'DOC_TRANS_LANG_{k} = "{escape_toml(names[c])}"'
                for k, c in zip(LANG_KEYS, LANG_CODES) if f'DOC_TRANS_LANG_{k}' in missing
            ) + "\n"
        open(os.path.join(ROOT, "src", "docs", "lang", f"{lang}.toml"), "w", encoding="utf-8", newline="").write(docs_out)

        # extra strings
        extra_src = os.path.join(ROOT, "src", "docs", "extra_strings.toml")
        extra_text = open(extra_src, encoding="utf-8").read()
        extra_out = process_text(extra_text, ref_map)
        open(os.path.join(ROOT, "src", "docs", meta["extra"]), "w", encoding="utf-8", newline="").write(extra_out)

        print(f"generated {lang}: grf/gs/docs/extra  ({len(ref_map)} 4.x reference strings)")


if __name__ == "__main__":
    generate()
