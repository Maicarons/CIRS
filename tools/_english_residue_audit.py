import os, re, io, json, glob, collections

LANG_DIR = "generated/lang"
# languages whose native script is non-Latin; a value with zero native chars but >=2 ASCII words is almost surely untranslated English
NATIVE = {
 "korean": lambda c: '\uac00' <= c <= '\ud7a3' or '\u3130' <= c <= '\u318f',
 "japanese": lambda c: ('\u3040' <= c <= '\u30ff') or ('\u4e00' <= c <= '\u9fff'),
 "simplified_chinese": lambda c: '\u4e00' <= c <= '\u9fff',
 "traditional_chinese": lambda c: '\u4e00' <= c <= '\u9fff',
 "russian": lambda c: '\u0400' <= c <= '\u04ff',
 "belarusian": lambda c: '\u0400' <= c <= '\u04ff',
 "serbian": lambda c: '\u0400' <= c <= '\u04ff',
 "arabic": lambda c: '\u0600' <= c <= '\u06ff',
 "tamil": lambda c: '\u0b80' <= c <= '\u0bff',
}
EN_STOP = set("the and of to in a an is are for with on by from that this it as be or at not you your we will can use used using each other more less than when if into out up all per del la le el los las der die das une des et en de du pour sur dans il un una uno i e o os ao da do em no na ni od za si s a k v z do je to su se na a".split())
PLACE = re.compile(r"\{[A-Za-z_0-9]*\}")
WORD2 = re.compile(r"[A-Za-z][A-Za-z'’-]{1,}\s+[A-Za-z][A-Za-z'’-]{1,}")
URLPATH = re.compile(r"(https?://|www\.|src/|docs/|generated/|\.toml|\.md|\.png|\.py|\.lng|\.nut|/CIRS/)")
BRANDY = re.compile(r"(?i)^(cirs|firs|newgrf|openttd|github|bananas|python|gpl|lgpl|md5|sha|svg|html|css|api|url|nml|grf|gs|id|ai|ttf|png|jpg|gif|tt|cc|utf-?8|ascii|todo|ok)\b")

def strip(s):
    return PLACE.sub(" ", s)

def analyze(path, lang):
    lines = io.open(path, encoding="utf-8").read().splitlines()
    native = NATIVE.get(lang)
    flags = []
    total = 0
    for ln in lines:
        if ln.startswith("#") or ":" not in ln: continue
        key, val = ln.split(":", 1)
        key = key.strip(); val = val.strip()
        if key in ("STR_GRF_NAME",): pass
        total += 1
        s = strip(val)
        letters = re.findall(r"[A-Za-z]+", s)
        if len(letters) < 2: continue
        # skip obvious brand / code / URL / technical-only lines
        if URLPATH.search(s) or BRANDY.match(s.strip()): continue
        has_native = (not native) or any(native(c) for c in s)
        words = [w.lower() for w in letters]
        en_hits = sum(1 for w in words if w in EN_STOP)
        two_words = bool(WORD2.search(s))
        if native is not None and not has_native and (two_words or en_hits >= 1):
            flags.append((key, val[:140], "no_native_script", en_hits, two_words))
        elif native is None:
            # Latin-script languages: strong English residue = >=3 ASCII words incl. >=2 stopwords, no accented/special chars
            special = any(ord(c) > 127 and c.isalpha() for c in s)
            if not special and en_hits >= 2 and len(words) >= 4 and two_words:
                flags.append((key, val[:140], "english_sentence", en_hits, two_words))
    return total, flags

results = {}
allflags = collections.defaultdict(list)
for p in sorted(glob.glob(LANG_DIR + "/*.lng")):
    lang = os.path.basename(p)[:-4]
    total, flags = analyze(p, lang)
    results[lang] = dict(total=total, flags=len(flags))
    for f in flags: allflags[lang].append(f)

print("=== per-language English-residue counts (game-facing .lng) ===")
for lang in sorted(results, key=lambda l: -results[l]["flags"]):
    r = results[lang]
    print("  %-22s strings=%4d  flagged=%4d" % (lang, r["total"], r["flags"]))

with io.open("tools/_english_residue_audit.txt", "w", encoding="utf-8") as f:
    f.write("ENGLISH-RESIDUE AUDIT on generated/lang/*.lng (the strings the GAME shows)\n")
    f.write("Non-Latin-script languages: flag when a value has ZERO native-script chars but contains English words.\n")
    f.write("Latin-script languages: flag when a value looks like an English sentence (>=2 stopwords, >=4 words, no accented chars).\n\n")
    for lang in sorted(allflags, key=lambda l: -len(allflags[l])):
        f.write("### %s  (%d flagged of %d)\n" % (lang, len(allflags[lang]), results[lang]["total"]))
        for key, val, why, hits, two in allflags[lang][:60]:
            f.write("  %s | %s | %s | en_hits=%s two_words=%s\n" % (key, why, val.replace("\n","\\n"), hits, two))
        f.write("\n")
with io.open("tools/_english_residue_audit.json", "w", encoding="utf-8") as f:
    json.dump({"per": results, "flags": {k:v[:200] for k,v in allflags.items()}}, f, ensure_ascii=False, indent=1)
print("WROTE tools/_english_residue_audit.txt / .json")
print("=== KOREAN sample (first 20 flags) ===")
for f in allflags.get("korean", [])[:20]: print("  ", f[0], "|", f[1][:120], "|", f[2], "en_hits", f[3])
