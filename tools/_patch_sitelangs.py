"""Expand SITE_LANGS in src/render_site.py to cover every 4.x language.

Replaces the hardcoded 8-entry SITE_LANGS list with a generated one built from
a compact mapping. Each entry: id -> (code, extra_strings file, display key, dir).
"""
import re

PATH = "src/render_site.py"

# id -> (short site code, extra_strings TOML, DOC_TRANS_LANG_* label key, dir)
_LANG_MAP = {
    "english":            ("en",    "extra_strings.toml",            "DOC_TRANS_LANG_EN",            ""),
    "simplified_chinese": ("zh",    "extra_strings_zh.toml",         "DOC_TRANS_LANG_ZH",            "zh"),
    "french":             ("fr",    "extra_strings_fr.toml",         "DOC_TRANS_LANG_FR",            "fr"),
    "german":             ("de",    "extra_strings_de.toml",         "DOC_TRANS_LANG_DE",            "de"),
    "spanish":            ("es",    "extra_strings_es.toml",         "DOC_TRANS_LANG_ES",            "es"),
    "portuguese":         ("pt",    "extra_strings_pt.toml",         "DOC_TRANS_LANG_PT",            "pt"),
    "korean":             ("ko",    "extra_strings_ko.toml",         "DOC_TRANS_LANG_KO",            "ko"),
    "arabic":             ("ar",    "extra_strings_ar.toml",         "DOC_TRANS_LANG_AR",            "ar"),
    "afrikaans":          ("af",    "extra_strings_afrikaans.toml",  "DOC_TRANS_LANG_AFRIKAANS",     "af"),
    "belarusian":         ("be",    "extra_strings_belarusian.toml", "DOC_TRANS_LANG_BELARUSIAN",    "be"),
    "catalan":            ("ca",    "extra_strings_catalan.toml",    "DOC_TRANS_LANG_CATALAN",       "ca"),
    "croatian":           ("hr",    "extra_strings_croatian.toml",   "DOC_TRANS_LANG_CROATIAN",      "hr"),
    "czech":              ("cs",    "extra_strings_czech.toml",      "DOC_TRANS_LANG_CZECH",         "cs"),
    "danish":             ("da",    "extra_strings_danish.toml",     "DOC_TRANS_LANG_DANISH",        "da"),
    "dutch":              ("nl",    "extra_strings_dutch.toml",      "DOC_TRANS_LANG_DUTCH",         "nl"),
    "esperanto":          ("eo",    "extra_strings_esperanto.toml",  "DOC_TRANS_LANG_ESPERANTO",     "eo"),
    "estonian":           ("et",    "extra_strings_estonian.toml",   "DOC_TRANS_LANG_ESTONIAN",      "et"),
    "finnish":            ("fi",    "extra_strings_finnish.toml",    "DOC_TRANS_LANG_FINNISH",       "fi"),
    "gaelic":             ("gd",    "extra_strings_gaelic.toml",     "DOC_TRANS_LANG_GAELIC",        "gd"),
    "galician":           ("gl",    "extra_strings_galician.toml",   "DOC_TRANS_LANG_GALICIAN",      "gl"),
    "hungarian":          ("hu",    "extra_strings_hungarian.toml",  "DOC_TRANS_LANG_HUNGARIAN",     "hu"),
    "indonesian":         ("id",    "extra_strings_indonesian.toml", "DOC_TRANS_LANG_INDONESIAN",   "id"),
    "italian":            ("it",    "extra_strings_italian.toml",    "DOC_TRANS_LANG_ITALIAN",       "it"),
    "japanese":           ("ja",    "extra_strings_japanese.toml",   "DOC_TRANS_LANG_JAPANESE",      "ja"),
    "latin":              ("la",    "extra_strings_latin.toml",      "DOC_TRANS_LANG_LATIN",         "la"),
    "luxembourgish":      ("lb",    "extra_strings_luxembourgish.toml","DOC_TRANS_LANG_LUXEMBOURGISH","lb"),
    "norwegian_bokmal":   ("nb",    "extra_strings_norwegian_bokmal.toml","DOC_TRANS_LANG_NORWEGIAN_BOKMAL","nb"),
    "polish":             ("pl",    "extra_strings_polish.toml",     "DOC_TRANS_LANG_POLISH",        "pl"),
    "portuguese_BR":      ("pt-br", "extra_strings_portuguese_BR.toml","DOC_TRANS_LANG_PORTUGUESE_BR","pt-br"),
    "romanian":           ("ro",    "extra_strings_romanian.toml",    "DOC_TRANS_LANG_ROMANIAN",      "ro"),
    "russian":            ("ru",    "extra_strings_russian.toml",     "DOC_TRANS_LANG_RUSSIAN",       "ru"),
    "serbian":            ("sr",    "extra_strings_serbian.toml",     "DOC_TRANS_LANG_SERBIAN",       "sr"),
    "traditional_chinese":("zh-hant", "extra_strings_traditional_chinese.toml","DOC_TRANS_LANG_TRADITIONAL_CHINESE","zh-hant"),
    "slovak":             ("sk",    "extra_strings_slovak.toml",     "DOC_TRANS_LANG_SLOVAK",        "sk"),
    "spanish_MX":         ("es-mx", "extra_strings_spanish_MX.toml",  "DOC_TRANS_LANG_SPANISH_MX",    "es-mx"),
    "swedish":            ("sv",    "extra_strings_swedish.toml",     "DOC_TRANS_LANG_SWEDISH",       "sv"),
    "tamil":              ("ta",    "extra_strings_tamil.toml",       "DOC_TRANS_LANG_TAMIL",         "ta"),
    "turkish":            ("tr",    "extra_strings_turkish.toml",     "DOC_TRANS_LANG_TURKISH",       "tr"),
    "welsh":              ("cy",    "extra_strings_welsh.toml",      "DOC_TRANS_LANG_WELSH",         "cy"),
}

lines = []
lines.append("# site languages; the first entry is the default (English, served from the site root).")
lines.append("# Keys are grf/gs/docs lang filenames; values give the short site `code`, the")
lines.append("# extra_strings TOML file, the DOC_TRANS_LANG_* key for the switcher label, and dir.")
lines.append("_LANG_MAP = {")
for _id, (_code, _extra, _display, _dir) in _LANG_MAP.items():
    lines.append(f'    "{_id}": ("{_code}", "{_extra}", "{_display}", "{_dir}"),')
lines.append("}")
lines.append("")
lines.append("SITE_LANGS = []")
lines.append('for _id, (_code, _extra, _display, _dir) in _LANG_MAP.items():')
lines.append("    if _id == \"english\":")
lines.append('        SITE_LANGS.append({')
lines.append('            "id": _id, "code": _code, "dir": _dir, "prefix": SITE_BASE,')
lines.append('            "route_prefix": "/", "extra_strings": _extra, "display": _display,')
lines.append("        })")
lines.append("    else:")
lines.append('        SITE_LANGS.append({')
lines.append('            "id": _id, "code": _code, "dir": _dir,')
lines.append('            "prefix": SITE_BASE + _code + "/",')
lines.append('            "route_prefix": "/" + _code + "/",')
lines.append('            "extra_strings": _extra, "display": _display,')
lines.append("        })")

new_block = "\n".join(lines)

with open(PATH, encoding="utf-8") as fp:
    src = fp.read()

new_src = re.sub(r"SITE_LANGS = \[.*?\n\]", new_block, src, count=1, flags=re.DOTALL)
if new_src == src:
    raise SystemExit("SITE_LANGS replacement failed")

with open(PATH, "w", encoding="utf-8", newline="") as fp:
    fp.write(new_src)
print(f"patched render_site.py: {len(_LANG_MAP)} languages")
