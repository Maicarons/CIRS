
import io, os, re, sys
ROOT = "G:/GitHub/CIRS"
LANGS = ["belarusian","croatian","czech","gaelic","indonesian","japanese","polish","russian","serbian","slovak","traditional_chinese","turkish"]
CARGOS = ["COFFEE","ENGINEERING_SUPPLIES","FARM_SUPPLIES","WOOL"]
def read(p):
    return io.open(os.path.join(ROOT,p),encoding="utf-8").read()

def corpus(lang):
    t = read("tools/_4x_ref/%s.lng" % lang)
    pl = re.search(r"##plural\s+(\d+)", t)
    out = {}
    for c in CARGOS:
        m = re.search(r"^STR_CARGO_UNIT_%s\s*:(.*)$" % c, t, re.M)
        if m: out[c] = m.group(1).strip()
    return (pl.group(1) if pl else "?"), out

def toml_block(t, key):
    # return the cargo_unit value inside [key] section
    m = re.search(r"\[" + re.escape(key) + r"\](.*?)(?=\n\[|\Z)", t, re.S)
    if not m: return None
    b = m.group(1)
    mm = re.search(r"^cargo_unit\s*=\s*\"(.*)\"\s*$", b, re.M)
    return mm.group(1) if mm else None

def toml_plural(t):
    m = re.search(r"^plural\s*=\s*\"(\d+)\"", t, re.M)
    return m.group(1) if m else "?"

out = io.open(os.path.join(ROOT,"tools/_plural_restore.txt"),"w",encoding="utf-8")
eng = read("src/grf/lang/english.toml")
print("ENGLISH:")
for c in CARGOS:
    print("  %-22s %s" % (c, toml_block(eng, "STR_CARGO_"+c)))
for lang in LANGS:
    t = read("src/grf/lang/%s.toml" % lang)
    pl = toml_plural(t)
    cpl, cvals = corpus(lang)
    print("\n== %s  our_plural=%s  corpus_plural=%s" % (lang, pl, cpl))
    for c in CARGOS:
        key = "STR_CARGO_"+c
        ours = toml_block(t, key)
        theirs = cvals.get(c)
        if ours is None and theirs is None: continue
        print("   %-22s OURS=%s" % (c, ours))
        print("   %-22s CORP=%s" % ("", theirs))
out.close()
