# -*- coding: utf-8 -*-
# Fix the root cause of 19 languages being silently dropped by nmlc.
# (1) add ##gender pragma (via [GLOBAL_PRAGMA] gender=...) for the 11 langs using {G=...}
# (2) remove the machine-copied English {P ...} commands whose argument count != lang.get_num_plurals()
# (3) mirror (2) into tools/_i18n_out/<lang>.jsonl (last-wins) so pipeline apply cannot revert it
# Idempotent. APPLY=1 writes. Authoritative gender labels come from tools/_4x_ref/*.lng headers.
import os, re, io, glob, json, collections

APPLY = os.environ.get("APPLY") == "1"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# nml/grfstrings.py:842-859  Language.get_num_plurals()
NUM = {0:2,1:1,2:2,3:3,4:5,5:3,6:3,7:3,8:4,9:2,10:3,11:2,12:4,13:4,14:3}
PCMD = re.compile(r"\{P\s+([^}]*)\}")
GCMD = re.compile(r"\{G=([^}]*)\}")
ASSIGN = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
PLURAL_LINE = re.compile(r'^\s*plural\s*=\s*"([^"]*)"')
GENDER_LINE = re.compile(r'^\s*gender\s*=')

def toks(body):
    b = body.replace('\\"', '"')
    t = re.findall(r'"[^"]*"|\S+', b)
    if t and re.fullmatch(r"\d+", t[0]):
        t = t[1:]
    return t

def unescape(s):
    out = []; i = 0
    mp = {"n":"\n","t":"\t","r":"\r","\\":"\\",'"':'"',"b":"\b","f":"\f"}
    while i < len(s):
        if s[i] == "\\" and i+1 < len(s):
            out.append(mp.get(s[i+1], s[i+1])); i += 2
        else:
            out.append(s[i]); i += 1
    return "".join(out)

# authoritative 4.x gender pragma values
G4 = {}
for p in glob.glob("tools/_4x_ref/*.lng"):
    lang = os.path.basename(p)[:-4]
    for ln in io.open(p, encoding="utf-8", errors="replace"):
        if ln.startswith("##gender"):
            G4[lang] = ln.strip().split(" ", 1)[1]
            break

LOG = []
LOG.append("APPLY=%s" % APPLY)
total_gender = 0
total_premove = 0
total_appends = 0
errors = []

for path in sorted(glob.glob("src/grf/lang/*.toml")):
    lang = os.path.basename(path)[:-5]
    raw = io.open(path, encoding="utf-8", newline="").read()
    sep = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(sep)

    # --- plural form for this language ---
    txt_flat = raw
    pm = PLURAL_LINE.search(txt_flat)
    plural = int(re.search(r"plural\s*=\s*\"(\d+)\"", txt_flat).group(1)) if re.search(r"plural\s*=\s*\"(\d+)\"", txt_flat) else 0
    N = NUM[plural]

    # --- gender needed? ---
    glabels = sorted(set(GCMD.findall(txt_flat)))
    gender_to_add = None
    if glabels:
        gstr = G4.get(lang)
        if not gstr:
            errors.append("%s: no 4x ##gender header but uses {G=} %r" % (lang, glabels)); gstr = " ".join(glabels)
        gset = gstr.split()
        missing = [g for g in glabels if g not in gset]
        if missing:
            errors.append("%s: {G=} labels %r not in 4x gender %r" % (lang, missing, gstr))
        if not any(GENDER_LINE.match(l) for l in lines):
            gender_to_add = gstr
        else:
            LOG.append("GENDER already present: %s" % lang)

    # --- find lines with bad {P} commands, keyed by TOML key ---
    bad = {}          # key -> (old_inner, new_inner)
    def fix(mo):
        b = mo.group(1)
        return "" if len(toks(b)) != N else mo.group(0)
    sec = ""
    for ln in lines:
        ms = SECTION.match(ln)
        if ms:
            sec = ms.group(1); continue
        m = ASSIGN.match(ln)
        if not m:
            continue
        val = m.group(4)                       # includes surrounding quotes
        inner = val[1:-1]
        newinner = PCMD.sub(fix, inner)
        if newinner != inner:
            key = (sec + "." + m.group(2)) if sec else m.group(2)
            bad[key] = (inner, newinner)

    if not gender_to_add and not bad:
        continue

    # --- rebuild file (single pass; avoids index shifting) ---
    make_fix = lambda v: PCMD.sub(fix, v)
    new_lines = []
    in_pragma = False
    gender_added = False
    sec = ""
    for ln in lines:
        ms = SECTION.match(ln)
        if ms:
            sec = ms.group(1)
            in_pragma = (sec == "GLOBAL_PRAGMA")
        m = ASSIGN.match(ln)
        outln = ln
        if m:
            key = (sec + "." + m.group(2)) if sec else m.group(2)
            if key in bad:
                v = m.group(4)
                nv = '"' + make_fix(v[1:-1]) + '"'
                outln = m.group(1) + m.group(2) + m.group(3) + nv + m.group(5)
        new_lines.append(outln)
        if in_pragma and gender_to_add and not gender_added and PLURAL_LINE.match(ln):
            new_lines.append('gender = "' + gender_to_add + '"')
            gender_added = True
    if gender_to_add and not gender_added:
        errors.append("%s: could not find plural line to insert ##gender after" % lang)

    # --- work-ref mirroring for the {P} changes ---
    appends = []
    wp = "tools/_i18n_work/" + lang + ".json"
    if bad and os.path.exists(wp):
        W = json.load(io.open(wp, encoding="utf-8")); ents = W["entries"]
        ref2i = {}; i2refs = collections.defaultdict(list)
        for i, e in enumerate(ents):
            for rf in e.get("refs", []):
                k = (rf[0].replace("\\", "/").lstrip("./"), rf[1])
                ref2i[k] = i; i2refs[i].append(k)
        myfile = "src/grf/lang/" + lang + ".toml"
        want = collections.defaultdict(set)
        noref = []
        for key, (old, new) in bad.items():
            i = ref2i.get((myfile, key))
            if i is None:
                noref.append(key); continue
            want[i].add(unescape(new))
        conflict = set()
        for i, vals in want.items():
            ok = len(vals) == 1
            for (f, k2) in i2refs[i]:
                f2 = f.replace("\\", "/").lstrip("./")
                if f2 != myfile or k2 not in bad:
                    ok = False; break
            if not ok:
                conflict.add(i)
        outp = "tools/_i18n_out/" + lang + ".jsonl"
        last = {}
        if os.path.exists(outp):
            for line in io.open(outp, encoding="utf-8"):
                try:
                    o = json.loads(line); last[o["i"]] = o["tr"]
                except Exception:
                    pass
        for i, vals in sorted(want.items()):
            if i in conflict:
                continue
            v = next(iter(vals))
            if last.get(i) != v:
                appends.append((i, v))
        if noref:
            LOG.append("NO_WORK_REF %s %r" % (lang, noref))
        if conflict:
            LOG.append("MIXED_INDEX %s %r" % (lang, sorted(conflict)))
    elif bad:
        errors.append("%s: no work file %s" % (lang, wp))

    LOG.append("LANG %-20s plural=%-2d N=%d gender=%-28s premove=%d appends=%d" % (
        lang, plural, N, repr(gender_to_add)[:28], len(bad), len(appends)))
    for key, (old, new) in sorted(bad.items()):
        LOG.append("   - %s" % key)
        LOG.append("       OLD %r" % old[:120])
        LOG.append("       NEW %r" % new[:120])
    total_gender += 1 if gender_to_add else 0
    total_premove += len(bad)
    total_appends += len(appends)

    if APPLY:
        io.open(path, "w", encoding="utf-8", newline="").write(sep.join(new_lines))
        if appends:
            with io.open("tools/_i18n_out/" + lang + ".jsonl", "a", encoding="utf-8") as fo:
                for i, v in appends:
                    fo.write(json.dumps({"i": i, "tr": v}, ensure_ascii=False) + "\n")

LOG.append("TOTAL gender=%d premove=%d appends=%d" % (total_gender, total_premove, total_appends))
LOG.append("ERRORS %d" % len(errors))
for e in errors:
    LOG.append("  ERR " + e)
LOG.append("DRY RUN - no files written" if not APPLY else "WROTE (APPLY=1)")
io.open("tools/_nml_grf_lang_fix.log", "w", encoding="utf-8").write("\n".join(LOG))
print(LOG[-3]); print(LOG[-2]); print("TOTAL gender=%d premove=%d appends=%d" % (total_gender, total_premove, total_appends))
for e in errors[:6]: print("ERR", e[:150])
