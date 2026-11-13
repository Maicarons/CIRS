#!/usr/bin/env python3
"""Correct the FRAX cargo-class labels DOC_CC_POTABLE / DOC_CC_NON_POTABLE.

FRAX defines these classes as an edibility / food-grade distinction, not a
drinkability one:

  src/polar_fox/docs/frax.html
    CC_POTABLE     "Cargo that is edible / food-grade (safe for human
                    consumption and with hygienic transport requirements)."
    CC_NON_POTABLE "Cargo that is inedible / non-food-grade (unsafe for human
                    consumption and incompatible with hygienic transport
                    requirements)."

The literal readings used so far ("可饮用" / "Drinkbar" / "Potabile" ...) made
the code reference table label livestock, coal, cement, fertiliser and
chemicals as "cannot be drunk", which is nonsense and misleading.

This script rewrites the two labels (and aligns zh-hant's DOC_CC_WEIRD with
zh) in every src/docs/lang/*.toml. English keeps the upstream FRAX names
("Potable" / "Non-Potable") because that is the canonical name players look up
in the FRAX reference.

Idempotent: only writes a file whose target value differs.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANG_DIR = ROOT / "src" / "docs" / "lang"

# lang -> (Potable, Non-Potable)
FOOD_GRADE = {
    "english":            ("Potable", "Non-Potable"),
    "simplified_chinese": ("食品级", "非食品级"),
    "traditional_chinese":("食品級", "非食品級"),
    "japanese":           ("食品級", "非食品級"),
    "korean":             ("식품 등급", "비식품 등급"),
    "afrikaans":          ("Voedselgraad", "Nie-voedselgraad"),
    "arabic":             ("صالح للأكل", "غير صالح للأكل"),
    "belarusian":         ("Продовольчага класа", "Непродовольчага класа"),
    "catalan":            ("Alimentari", "No alimentari"),
    "croatian":           ("Jestivo", "Nejestivo"),
    "czech":              ("Potravinářský", "Nepotravinářský"),
    "danish":             ("Spiselig", "Ikke spiselig"),
    "dutch":              ("Eetbaar", "Niet eetbaar"),
    "esperanto":          ("Manĝebla", "Nemanĝebla"),
    "estonian":           ("Toiduaine", "Mittetoiduaine"),
    "finnish":            ("Syötävä", "Ei syötävä"),
    "french":             ("Alimentaire", "Non alimentaire"),
    "gaelic":             ("Ìre bìdh", "Neo-ìre bìdh"),
    "galician":           ("Alimentario", "Non alimentario"),
    "german":             ("Lebensmitteleignung", "Nicht lebensmitteleignend"),
    "hungarian":          ("Élelmiszer-minőségű", "Nem élelmiszer-minőségű"),
    "indonesian":         ("Layak pangan", "Tidak layak pangan"),
    "italian":            ("Alimentare", "Non alimentare"),
    "latin":              ("Edibilis", "Non edibilis"),
    "luxembourgish":      ("Liewensmëttelgeeignet", "Net Liewensmëttelgeeignet"),
    "norwegian_bokmal":   ("Matvaregod", "Ikke-matvaregod"),
    "polish":             ("Jadalne", "Niejadalne"),
    "portuguese":         ("Alimentar", "Não alimentar"),
    "portuguese_BR":      ("Alimentar", "Não alimentar"),
    "romanian":           ("Alimentar", "Nearalimentar"),
    "russian":            ("Пищевой", "Непищевой"),
    "serbian":            ("Jestivo", "Nejestivo"),
    "slovak":             ("Potravinársky", "Nepotravinársky"),
    "spanish":            ("Alimentario", "No alimentario"),
    "spanish_MX":         ("Alimentario", "No alimentario"),
    "swedish":            ("Ätbar", "Ej ätbar"),
    "tamil":              ("உணவுத் தரம்", "உணவுத் தரமற்றது"),
    "turkish":            ("Yenilebilir", "Yenilemez"),
    "welsh":              ("Bwydadwy", "An-bwydadwy"),
}

# zh-hant used "其他" for Weird while zh used "特殊"; FRAX means "does not fit
# any standard class", so keep the two Chinese variants parallel.
WEIRD_ALIGN = {"traditional_chinese": "特殊"}

KEY_RE = {
    "DOC_CC_POTABLE": re.compile(r'^(\s*DOC_CC_POTABLE\s*=\s*)"(.*)"(\s*(?:#.*)?)$', re.M),
    "DOC_CC_NON_POTABLE": re.compile(r'^(\s*DOC_CC_NON_POTABLE\s*=\s*)"(.*)"(\s*(?:#.*)?)$', re.M),
    "DOC_CC_WEIRD": re.compile(r'^(\s*DOC_CC_WEIRD\s*=\s*)"(.*)"(\s*(?:#.*)?)$', re.M),
}


def main() -> int:
    changed_files = 0
    changed_values = 0
    errors = []
    for path in sorted(LANG_DIR.glob("*.toml")):
        lang = path.stem
        if lang not in FOOD_GRADE:
            errors.append(f"{lang}: no food-grade translation defined")
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        potable, non_potable = FOOD_GRADE[lang]
        targets = {"DOC_CC_POTABLE": potable, "DOC_CC_NON_POTABLE": non_potable}
        if lang in WEIRD_ALIGN:
            targets["DOC_CC_WEIRD"] = WEIRD_ALIGN[lang]
        for key, value in targets.items():
            m = KEY_RE[key].search(text)
            if not m:
                errors.append(f"{lang}: {key} not found")
                continue
            if m.group(2) == value:
                continue
            text = text[: m.start()] + m.group(1) + '"' + value + '"' + m.group(3) + text[m.end():]
            changed_values += 1
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed_files += 1
            print(f"updated {path.relative_to(ROOT)}")
    print(f"changed_files={changed_files} changed_values={changed_values}")
    if errors:
        print("ERRORS:")
        for e in errors:
            print("  " + e)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
