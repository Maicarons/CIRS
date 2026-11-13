#!/usr/bin/env python3
"""Temporary CIRS i18n completion pipeline.

Commands:
  gen     -> build tools/_i18n_work/<lang>.json work lists
  apply   -> read tools/_i18n_out/<lang>.jsonl and patch TOML values
  report  -> print untranslated counts before/after
  gaps    -> list missing indices per language
"""
from __future__ import annotations
import ast, json, re, sys, tomllib
from collections import Counter
from pathlib import Path

R = Path(__file__).resolve().parents[1]
WORK = R / "tools" / "_i18n_work"
OUT = R / "tools" / "_i18n_out"
PH = re.compile(r"\{([A-Za-z_0-9]*)\}")
ASSIGN = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
SKIP_KEY = re.compile(r'^(DOC_TRANS_LANG_|DOC_NAV_SWITCH_LANGUAGE$)')

DISPLAY = {
 "afrikaans":"Afrikaans","arabic":"Arabic (العربية)","belarusian":"Belarusian (Беларуская)",
 "catalan":"Catalan (Català)","croatian":"Croatian (Hrvatski)","czech":"Czech (Čeština)",
 "danish":"Danish (Dansk)","dutch":"Dutch (Nederlands)","esperanto":"Esperanto",
 "estonian":"Estonian (Eesti)","finnish":"Finnish (Suomi)","french":"French (Français)",
 "gaelic":"Scottish Gaelic (Gàidhlig)","galician":"Galician (Galego)","german":"German (Deutsch)",
 "hungarian":"Hungarian (Magyar)","indonesian":"Indonesian (Bahasa Indonesia)",
 "italian":"Italian (Italiano)","japanese":"Japanese (日本語)","korean":"Korean (한국어)",
 "latin":"Latin (Latina)","luxembourgish":"Luxembourgish (Lëtzebuergesch)",
 "norwegian_bokmal":"Norwegian Bokmål (Norsk bokmål)","polish":"Polish (Polski)",
 "portuguese":"Portuguese (Português)","portuguese_BR":"Brazilian Portuguese (Português do Brasil)",
 "romanian":"Romanian (Română)","russian":"Russian (Русский)","serbian":"Serbian (Српски)",
 "simplified_chinese":"Simplified Chinese (简体中文)","slovak":"Slovak (Slovenčina)",
 "spanish":"Spanish (Español)","spanish_MX":"Mexican Spanish (Español de México)",
 "swedish":"Swedish (Svenska)","tamil":"Tamil (தமிழ்)",
 "traditional_chinese":"Traditional Chinese (繁體中文)","turkish":"Turkish (Türkçe)",
 "welsh":"Welsh (Cymraeg)",
}

def load(p):
    with p.open("rb") as f:
        return tomllib.load(f)

def leaves(data):
    out = {}
    for k, v in data.items():
        if k == "GLOBAL_PRAGMA":
            continue
        if isinstance(v, dict):
            for a, b in v.items():
                if isinstance(b, str):
                    out[f"{k}.{a}"] = b
        elif isinstance(v, str):
            out[k] = v
    return out

def ph(v):
    return Counter(PH.findall(v))

def placeholder_only(v):
    s = v.strip()
    return s == "" or (bool(PH.search(s)) and PH.sub("", s).strip() == "")

def lang_map():
    src = (R / "src/render_site.py").read_text(encoding="utf-8")
    i = src.index("_LANG_MAP")
    j = src.index("\n}", i)
    return ast.literal_eval(src[src.index("{", i):j + 2])

def extra_files(lm):
    """Map every src/docs/extra_strings_*.toml to a language id."""
    code2lang = {v[0]: k for k, v in lm.items()}
    out = {}
    for p in sorted((R / "src/docs").glob("extra_strings_*.toml")):
        stem = p.name[len("extra_strings_"):-5]
        lang = code2lang.get(stem) or (stem if stem in lm else None)
        if lang and lang != "english":
            out.setdefault(lang, []).append(f"src/docs/{p.name}")
    return out

def targets(l, lm, extras):
    t = [
        ("grf", f"src/grf/lang/{l}.toml", "src/grf/lang/english.toml"),
        ("gs", f"src/gs/lang/{l}.toml", "src/gs/lang/english.toml"),
        ("docs", f"src/docs/lang/{l}.toml", "src/docs/lang/english.toml"),
    ]
    for f in extras.get(l, []):
        t.append(("extra", f, "src/docs/extra_strings.toml"))
    return t

def cmd_gen():
    lm = lang_map()
    extras = extra_files(lm)
    langs = sorted(k for k in lm if k != "english")
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for l in langs:
        entries = {}
        for grp, tgt, ref in targets(l, lm, extras):
            en = leaves(load(R / ref))
            tv = leaves(load(R / tgt))
            for k, ev in en.items():
                if SKIP_KEY.match(k) or placeholder_only(ev):
                    continue
                if tv.get(k) == ev:
                    e = entries.setdefault(ev, {"ph": sorted(set(PH.findall(ev))), "refs": []})
                    e["refs"].append([tgt, k])
        items = [{"en": en, "ph": info["ph"], "refs": info["refs"]}
                 for en, info in sorted(entries.items())]
        data = {"lang": l, "display": DISPLAY.get(l, l), "count": len(items),
                "refs": sum(len(i["refs"]) for i in items), "entries": items}
        (WORK / f"{l}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        manifest[l] = {"display": DISPLAY.get(l, l), "unique": len(items), "refs": data["refs"]}
    (WORK / "_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    total_u = sum(v["unique"] for v in manifest.values())
    total_r = sum(v["refs"] for v in manifest.values())
    print(f"gen: {len(langs)} languages, {total_u} unique (lang,string) translations, {total_r} value slots")
    for l, v in manifest.items():
        print(f"  {l:<24} unique={v['unique']:<5} slots={v['refs']}")

def unescape_toml(s):
    out, i = [], 0
    mp = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "b": "\b", "f": "\f"}
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s) and s[i + 1] in mp:
            out.append(mp[s[i + 1]])
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)

def escape_toml(s):
    return (s.replace("\\", "\\\\").replace('"', '\\"')
             .replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r"))

def cmd_apply():
    lm = lang_map()
    extras = extra_files(lm)
    langs = sorted(k for k in lm if k != "english")
    grand = Counter()
    for l in langs:
        wf = WORK / f"{l}.json"
        if not wf.exists():
            continue
        work = json.loads(wf.read_text(encoding="utf-8"))
        trs = {}
        of = OUT / f"{l}.jsonl"
        if of.exists():
            for line in of.read_text(encoding="utf-8").splitlines():
                try:
                    o = json.loads(line)
                    if isinstance(o.get("i"), int) and isinstance(o.get("tr"), str) and o["tr"].strip():
                        trs[o["i"]] = o["tr"]
                except Exception:
                    pass
        patches = {}
        missing = badph = same = 0
        for idx, item in enumerate(work["entries"]):
            en = item["en"]
            tr = trs.get(idx)
            if tr is None:
                missing += 1
                continue
            if ph(tr) != ph(en):
                badph += 1
                continue
            if tr == en:
                same += 1
            for tgt, key in item["refs"]:
                patches.setdefault(tgt, {})[key] = (en, tr)
        changed = 0
        for tgt, pm in patches.items():
            p = R / tgt
            lines = p.read_text(encoding="utf-8").split("\n")
            section = ""
            for idx, line in enumerate(lines):
                ms = SECTION.match(line)
                if ms:
                    section = ms.group(1)
                    continue
                m = ASSIGN.match(line)
                if not m:
                    continue
                attr = m.group(2)
                fk = (section + "." + attr) if section else attr
                if section == "GLOBAL_PRAGMA" or fk not in pm:
                    continue
                en, tr = pm[fk]
                # Work-list slots were English at gen time; patch unconditionally so
                # re-apply after polishing is idempotent and can overwrite earlier output.
                lines[idx] = f'{m.group(1)}{m.group(2)}{m.group(3)}"{escape_toml(tr)}"{m.group(5)}'
                changed += 1
            p.write_text("\n".join(lines), encoding="utf-8", newline="")
        grand["translated"] += changed
        grand["missing"] += missing
        grand["badph"] += badph
        grand["same"] += same
        print(f"  {l:<24} patched={changed:<5} missing={missing:<4} bad_ph={badph:<3} kept_english={same}")
    print("TOTAL:", dict(grand))

def cmd_report():
    lm = lang_map()
    extras = extra_files(lm)
    langs = sorted(k for k in lm if k != "english")
    rows = []
    for l in langs:
        tot = unt = 0
        for grp, tgt, ref in targets(l, lm, extras):
            en = leaves(load(R / ref))
            tv = leaves(load(R / tgt))
            for k, ev in en.items():
                if SKIP_KEY.match(k) or placeholder_only(ev):
                    continue
                tot += 1
                if tv.get(k) == ev:
                    unt += 1
        rows.append((unt, tot, l))
    rows.sort(reverse=True)
    print("language | untranslated/total")
    for unt, tot, l in rows:
        print(f"  {l:<24} {unt:>4}/{tot}")
    print(f"TOTAL untranslated = {sum(r[0] for r in rows)} / {sum(r[1] for r in rows)}")

def cmd_gaps():
    langs = sorted(p.stem for p in WORK.glob("*.json") if not p.stem.startswith("_"))
    for l in langs:
        work = json.loads((WORK / f"{l}.json").read_text(encoding="utf-8"))
        have = set()
        of = OUT / f"{l}.jsonl"
        if of.exists():
            for line in of.read_text(encoding="utf-8").splitlines():
                try:
                    o = json.loads(line)
                    if isinstance(o.get("i"), int):
                        have.add(o["i"])
                except Exception:
                    pass
        miss = [i for i in range(work["count"]) if i not in have]
        if miss:
            print(f"{l}: {len(miss)} missing (first 20: {miss[:20]})")

if __name__ == "__main__":
    {"gen": cmd_gen, "apply": cmd_apply, "report": cmd_report, "gaps": cmd_gaps}[sys.argv[1]]()
