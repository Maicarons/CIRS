# -*- coding: utf-8 -*-
"""Generate full VitePress locale themeConfig blocks for the 31 short locales.
Idempotent: replaces the short-locale section between the first 'af' locale key
and the line that closes the locales object (followed by '})')."""
import json, re, tomllib
from pathlib import Path

ROOT = Path(".")
CFG = ROOT / "docs-site/.vitepress/config.mts"
CHROME = json.loads((ROOT / "tools/_i18n_chrome.json").read_text("utf-8"))

# code -> (lang toml id, native label)
LOCALES = [
    ("af",      "afrikaans",        "Afrikaans"),
    ("be",      "belarusian",       "Беларуская"),
    ("ca",      "catalan",          "Català"),
    ("cs",      "czech",            "Čeština"),
    ("cy",      "welsh",            "Cymraeg"),
    ("da",      "danish",           "Dansk"),
    ("eo",      "esperanto",        "Esperanto"),
    ("es-mx",   "spanish_MX",       "Español (MX)"),
    ("et",      "estonian",         "Eesti"),
    ("fi",      "finnish",          "Suomi"),
    ("gd",      "gaelic",           "Gàidhlig"),
    ("gl",      "galician",         "Galego"),
    ("hr",      "croatian",         "Hrvatski"),
    ("hu",      "hungarian",        "Magyar"),
    ("id",      "indonesian",       "Indonesia"),
    ("it",      "italian",          "Italiano"),
    ("ja",      "japanese",         "日本語"),
    ("la",      "latin",            "Latina"),
    ("lb",      "luxembourgish",    "Lëtzebuergesch"),
    ("nb",      "norwegian_bokmal", "Norsk (Bokmål)"),
    ("nl",      "dutch",            "Nederlands"),
    ("pl",      "polish",           "Polski"),
    ("pt-br",   "portuguese_BR",    "Português (BR)"),
    ("ro",      "romanian",         "Română"),
    ("ru",      "russian",          "Русский"),
    ("sk",      "slovak",           "Slovenčina"),
    ("sr",      "serbian",          "Српски"),
    ("sv",      "swedish",          "Svenska"),
    ("ta",      "tamil",            "தமிழ்"),
    ("tr",      "turkish",          "Türkçe"),
    ("zh-hant", "traditional_chinese", "繁體中文"),
]

def js(s):
    # JSON string literal is valid TS/JS and escapes quotes/backslashes safely.
    return json.dumps(s, ensure_ascii=False)

def docs_nav(lang_id):
    with open(ROOT / "src/docs/lang" / (lang_id + ".toml"), "rb") as f:
        d = tomllib.load(f)
    return d

def block(code, lang_id, label):
    c = CHROME[code]
    d = docs_nav(lang_id)
    P = "/" + code + "/"
    def L(page): return P + page
    guide        = c["guide"]
    get_started  = c["get_started"]
    reference    = c["reference"]
    economies    = d["DOC_NAV_ECONOMIES"]
    cargos       = d["DOC_NAV_CARGOS"]
    industries   = d["DOC_NAV_INDUSTRIES"]
    code_ref     = d["DOC_NAV_CODE_REFERENCE"]
    changelog    = d["DOC_NAV_CHANGELOG"]
    translations = d["DOC_NAV_TRANSLATIONS"]
    b = []
    a = b.append
    a("    '" + code + "': {")
    a("      label: " + js(label) + ",")
    a("      lang: " + js(code) + ",")
    a("      link: " + js(P) + ",")
    a("      themeConfig: {")
    a("        nav: [")
    a("          { text: " + js(guide)      + ", link: " + js(L("get-started.html"))  + " },")
    a("          { text: " + js(economies)  + ", link: " + js(L("economies.html"))    + " },")
    a("          { text: " + js(cargos)     + ", link: " + js(L("cargos.html"))       + " },")
    a("          { text: " + js(industries) + ", link: " + js(L("industries.html"))   + " },")
    a("          {")
    a("            text: " + js(reference) + ",")
    a("            items: [")
    a("              { text: " + js(code_ref)     + ", link: " + js(L("code-reference.html")) + " },")
    a("              { text: " + js(changelog)    + ", link: " + js(L("changelog.html"))      + " },")
    a("              { text: " + js(translations) + ", link: " + js(L("translations.html"))   + " }")
    a("            ]")
    a("          }")
    a("        ],")
    a("        sidebar: [")
    a("          {")
    a("            text: " + js(guide) + ",")
    a("            items: [")
    a("              { text: " + js(get_started) + ", link: " + js(L("get-started.html")) + " },")
    a("              { text: " + js(economies)  + ", link: " + js(L("economies.html"))   + " },")
    a("              { text: " + js(cargos)     + ", link: " + js(L("cargos.html"))      + " },")
    a("              { text: " + js(industries) + ", link: " + js(L("industries.html"))  + " }")
    a("            ]")
    a("          },")
    a("          {")
    a("            text: " + js(reference) + ",")
    a("            items: [")
    a("              { text: " + js(code_ref)     + ", link: " + js(L("code-reference.html")) + " },")
    a("              { text: " + js(changelog)    + ", link: " + js(L("changelog.html"))      + " },")
    a("              { text: " + js(translations) + ", link: " + js(L("translations.html"))   + " }")
    a("            ]")
    a("          }")
    a("        ],")
    a("        outline: { label: " + js(c["on_this_page"]) + " },")
    a("        docFooter: { prev: " + js(c["prev"]) + ", next: " + js(c["next"]) + " },")
    a("        darkModeSwitchLabel: " + js(c["appearance"]) + ",")
    a("        lightModeSwitchTitle: " + js(c["switch_light"]) + ",")
    a("        darkModeSwitchTitle: " + js(c["switch_dark"]) + ",")
    a("        sidebarMenuLabel: " + js(c["menu"]) + ",")
    a("        returnToTopLabel: " + js(c["return_to_top"]) + ",")
    a("        langMenuLabel: " + js(c["change_language"]) + ",")
    a("        externalLinkIcon: true")
    a("      }")
    a("    }")
    return "\n".join(b)

def main():
    raw = CFG.read_text("utf-8")
    lines = raw.replace("\r\n", "\n").split("\n")
    start = next(i for i, l in enumerate(lines) if re.match(r"^\s*'?af'?\s*:\s*\{", l))
    close = next(i for i in range(start, len(lines) - 1)
                 if lines[i].strip() == "}" and lines[i + 1].strip().startswith("})"))
    blocks = [block(c, i, l) for c, i, l in LOCALES]
    new_section = ",\n".join(blocks)
    lines[start:close] = new_section.split("\n")
    CFG.write_text("\n".join(lines), "utf-8")
    print("WROTE", CFG, "locales=", len(blocks),
          "start_line=", start + 1, "old_end_line=", close,
          "new_lines=", len(lines))

main()
