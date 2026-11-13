"""Append the full set of DOC_TRANS_LANG_* switcher keys to the english.toml
reference so every generated docs/lang file (which carries all language names)
matches the reference key set exactly.

The 8 core codes (EN, ZH, FR, DE, ES, PT, KO, AR) already exist; we add the
40 long-name codes (AFRIKAANS ... WELSH) in the same order the generator uses.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALL_LANGS = [
    "afrikaans", "belarusian", "catalan", "croatian", "czech", "danish",
    "dutch", "english", "english_au", "english_us", "esperanto", "estonian",
    "finnish", "french", "gaelic", "galician", "german", "hungarian",
    "indonesian", "italian", "japanese", "korean", "latin", "luxembourgish",
    "norwegian_bokmal", "polish", "portuguese", "portuguese_BR", "romanian",
    "russian", "serbian",     "simplified_chinese", "slovak", "spanish",
    "spanish_MX", "swedish", "tamil", "traditional_chinese", "turkish", "welsh",
    "arabic",
]

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

path = os.path.join(ROOT, "src", "docs", "lang", "english.toml")
with open(path, encoding="utf-8") as fp:
    content = fp.read()

existing = {f"DOC_TRANS_LANG_{l.upper()}" for l in ALL_LANGS}
lines = []
for lang in ALL_LANGS:
    key = f"DOC_TRANS_LANG_{lang.upper()}"
    if key in content:
        continue
    lines.append(f'{key} = "{NATIVE_NAMES.get(lang, "")}"')

if lines:
    sep = "" if content.endswith("\n") else "\n"
    with open(path, "a", encoding="utf-8", newline="") as fp:
        fp.write(sep + "\n".join(lines) + "\n")
    print(f"appended {len(lines)} DOC_TRANS_LANG_* keys to english.toml")
else:
    print("no new keys needed")
