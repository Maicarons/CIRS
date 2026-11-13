import os, re, io, json, glob, collections

ROOT = "src"
GROUPS = {
    "grf":  ("src/grf/lang/english.toml",  "src/grf/lang/{}.toml",  "src/grf/lang/*.toml"),
    "gs":   ("src/gs/lang/english.toml",   "src/gs/lang/{}.toml",   "src/gs/lang/*.toml"),
    "docs": ("src/docs/lang/english.toml", "src/docs/lang/{}.toml", "src/docs/lang/*.toml"),
}
XS = {  # 7 rendered short-code files vs long-name files
    "ar": "arabic", "de": "german", "es": "spanish", "fr": "french",
    "ko": "korean", "pt": "portuguese", "zh": "simplified_chinese",
}

SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
ASSIGN  = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
PH = re.compile(r"\{[A-Za-z_0-9]*\}")
ESC = {"n":"\n","t":"\t","r":"\r","b":"\b","f":"\f","\\":"\\","\"":"\""}
def unesc(s):
    out = []; i = 1
    while i < len(s) - 1:
        c = s[i]
        if c == "\\" and i + 1 < len(s) - 1:
            out.append(ESC.get(s[i+1], s[i+1])); i += 2
        else:
            out.append(c); i += 1
    return "".join(out)
def parse(p):
    d = {}; sec = ""; cur = None
    for ln in io.open(p, encoding="utf-8").read().splitlines():
        m = SECTION.match(ln)
        if m: sec = m.group(1); cur = None; continue
        m = ASSIGN.match(ln)
        if m:
            k = sec + "." + m.group(2) if m.group(2) == "base" else m.group(2)
            # keep fully qualified for uniqueness
            k = sec + "." + m.group(2)
            d[k] = unesc(m.group(4))
    return d

def langs(globpat):
    out = []
    for p in sorted(glob.glob(globpat)):
        b = os.path.basename(p)[:-5]
        if b in ("english",) or b in XS: continue
        out.append((b, p))
    return out

def real_text(s):
    return bool(re.search(r"[A-Za-z\u00c0-\u02af\u0370-\u1fff\u2c00-\ud7ff]|[^\x00-\x7f]", s)) and len(s.strip()) > 2

def is_brand_or_code(en, tr):
    # legitimate to keep English: pure placeholders/codes, CIRS/FIRS/NewGRF names, URLs, numbers/punct
    if PH.sub("", en).strip() == PH.sub("", tr).strip() == "": return True
    if not real_text(en): return True
    bare = PH.sub("", en).strip()
    if re.fullmatch(r"[A-Za-z0-9_./#\-+&'()\[\]{},:;% ]*", tr) is None: return False
    # allow if English is a single technical token / proper noun with no spaces (e.g. "NewGRF", "CIRS")
    if " " not in bare and re.fullmatch(r"[A-Za-z0-9_./\-+&']+", bare): return True
    if bare.lower() in ("cirs", "firs", "newgrf", "openttd", "github", "bananas", "mild mild west", "steeltown", "in a hot country"): return True
    if re.fullmatch(r"(?i)(cirs|firs|newgrf|openttd).*", bare) and bare.count(" ") <= 2: return True
    if re.match(r"^(https?://|www\.|src/|docs/|\{)", bare): return True
    return False

def main():
    total = collections.Counter()
    per = {}
    details = collections.defaultdict(list)
    for grp, (engp, tmpl, gpat) in GROUPS.items():
        en = parse(engp)
        ls = langs(gpat)
        print("GROUP", grp, "english_keys", len(en), "langs", len(ls))
        for b, p in ls:
            tr = parse(p)
            miss = [k for k in en if k not in tr]
            empty = [k for k in en if k in tr and not tr[k].strip()]
            badph = [k for k in en if k in tr and sorted(PH.findall(en[k])) != sorted(PH.findall(tr[k]))]
            same = []
            for k in en:
                if k not in tr or not tr[k].strip(): continue
                if tr[k] == en[k] and real_text(en[k]) and not is_brand_or_code(en[k], tr[k]):
                    same.append(k)
            # extra strings (same language, short-code file)
            xsmiss = []; xssame = []
            if grp == "docs" and b in XS.values():
                short = {v:k2 for k2,v in XS.items()}
                xp = "src/docs/extra_strings_" + short[b] + ".toml"
                if os.path.exists(xp):
                    xe = parse(xp); xl = parse("src/docs/extra_strings_" + b + ".toml") if os.path.exists("src/docs/extra_strings_" + b + ".toml") else {}
                    xsmiss = [k for k in xe if k not in xl]
                    xssame = [k for k in xe if k in xl and xl[k] == xe[k] and real_text(xe[k]) and not is_brand_or_code(xe[k], xl[k])]
            rec = dict(lang=b, group=grp, en=len(en), keys=len(tr), missing=len(miss), empty=len(empty), badph=len(badph), same_real=len(same),
                       xs_missing=len(xsmiss), xs_same=len(xssame))
            per[grp + "/" + b] = rec
            for k in miss: details[grp + "/" + b].append(("missing", k, en.get(k,"")[:80], ""))
            for k in empty: details[grp + "/" + b].append(("empty", k, en.get(k,"")[:80], ""))
            for k in badph: details[grp + "/" + b].append(("badph", k, en.get(k,"")[:80], tr.get(k,"")[:80]))
            for k in same: details[grp + "/" + b].append(("same_real", k, en.get(k,"")[:100], tr.get(k,"")[:100]))
            total[grp + "_missing"] += len(miss); total[grp + "_empty"] += len(empty)
            total[grp + "_badph"] += len(badph); total[grp + "_same_real"] += len(same)
            total[grp + "_xs_missing"] += len(xsmiss); total[grp + "_xs_same"] += len(xssame)
    print("TOTAL", dict(total))
    print("=== worst 25 by same_real ===")
    for key, rec in sorted(per.items(), key=lambda kv: -kv[1]["same_real"])[:25]:
        print("  ", key, "same_real", rec["same_real"], "missing", rec["missing"], "empty", rec["empty"], "badph", rec["badph"], "keys", rec["keys"], "/", rec["en"])
    with io.open("tools/_strict_audit_report.json", "w", encoding="utf-8") as f:
        json.dump({"per": per, "total": dict(total), "details": {k:v[:400] for k,v in details.items()}}, f, ensure_ascii=False, indent=1)
    # full text for human review
    with io.open("tools/_strict_audit_report.txt", "w", encoding="utf-8") as f:
        f.write("STRICT AUDIT — every English key vs every non-English TOML\n")
        f.write("Legend: same_real = value byte-identical to English real text (untranslated) after excluding brands/codes/URLs\n\n")
        for key in sorted(details):
            if details[key]:
                f.write("### " + key + "  (" + str(len(details[key])) + ")\n")
                for typ, k, ev, tv in details[key]:
                    f.write("  " + typ + " | " + k + " | EN=" + ev.replace("\n","\\n") + " | TR=" + tv.replace("\n","\\n") + "\n")
        f.write("\n=== PER-LANGUAGE COUNTS ===\n")
        for key in sorted(per):
            r = per[key]
            f.write(key + " " + json.dumps(r, ensure_ascii=False) + "\n")
    print("WROTE tools/_strict_audit_report.json / .txt")
main()
