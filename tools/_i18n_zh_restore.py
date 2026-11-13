# Idempotent restore of pre-session HUMAN simplified-Chinese translations from git HEAD.
# APPLY=1 writes. Guards: keep 8 website rewrites, CIRS rebrand, nav label, deliberate polish,
# conflict/mixed work indices. Mirrors restored values into out-JSONL so pipeline apply is stable.
import subprocess, tomllib, re, json, os, collections
APPLY = os.environ.get("APPLY") == "1"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def sh(*a): return subprocess.check_output(list(a), cwd=ROOT).decode("utf-8")
def leaves(txt):
    d = tomllib.loads(txt); out = {}
    for sec, v in d.items():
        if sec == "GLOBAL_PRAGMA": continue
        if isinstance(v, dict):
            for k, vv in v.items(): out[sec + "." + k] = vv if isinstance(vv, str) else str(vv)
        elif isinstance(v, str): out[sec] = v
    return out
def head(p): return sh("git", "show", "HEAD:" + p)
def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
REWRITES = {"DOC_HOME_TAGLINE", "DOC_HOME_WHY_1_DESC", "DOC_HOME_WHY_2_DESC", "DOC_HOME_WHY_3_DESC",
            "DOC_CR_COMPILING_P1", "DOC_CR_FRAX_P1", "DOC_CR_FRAX_P2", "DOC_CR_TOWN_GROWTH_NOTE"}
PROTECT = REWRITES | {"DOC_NAV_SWITCH_LANGUAGE",
              "STR_CARGO_EDIBLE_OIL.cid", "STR_CARGO_QUICKLIME.cid", "STR_CARGO_VEHICLE_BODIES.cid"}
PAIRS = [("src/grf/lang/simplified_chinese.toml", "src/grf/lang/english.toml"),
         ("src/gs/lang/simplified_chinese.toml", "src/gs/lang/english.toml"),
         ("src/docs/lang/simplified_chinese.toml", "src/docs/lang/english.toml")]
ASSIGN = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
PH = re.compile(r"\{([A-Za-z_0-9]*)\}")
def esc(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")
def line_pos(txt):
    out = {}; sec = ""
    for i, ln in enumerate(txt.split("\n")):
        ms = SECTION.match(ln)
        if ms: sec = ms.group(1); continue
        m = ASSIGN.match(ln)
        if not m: continue
        out[(sec + "." + m.group(2)) if sec else m.group(2)] = i
    return out
# ---- restore candidates ----
restore = []
for f, ef in PAIRS:
    H = leaves(head(f)); E = leaves(rd(ef)); C = leaves(rd(f))
    for k, en in E.items():
        if k.lstrip(".") in PROTECT: continue
        h = H.get(k); c = C.get(k)
        if h is None or h == en or c is None or c == h: continue
        if sorted(PH.findall(h)) != sorted(PH.findall(en)): continue
        # brand guard: do not re-introduce stale FIRS where current already rebranded to CIRS
        if h.count("FIRS") > c.count("FIRS") and c.count("CIRS") >= h.count("CIRS"): continue
        restore.append((f, k, h, c, en))
# ---- work index map ----
W = json.loads(rd("tools/_i18n_work/simplified_chinese.json")); ENTS = W["entries"] if isinstance(W, dict) else W
ref2i = {}; i2refs = collections.defaultdict(list)
for i, e in enumerate(ENTS):
    for rf in e.get("refs", []):
        key = (rf[0].replace("\\", "/").lstrip("./"), rf[1]); ref2i[key] = i; i2refs[i].append(key)
restset = {(f, k) for f, k, h, c, en in restore}
POLS = set(json.loads(rd("tools/_i18n_zh_polished_idx.json")))
want = {}
for f, k, h, c, en in restore:
    i = ref2i.get((f, k))
    if i is not None: want.setdefault(i, set()).add(h)
conflict = {i for i, v in want.items() if len(v) > 1}
mixed = {i for i, v in want.items() if len(v) == 1 and not all(r in restset for r in i2refs[i])}
skip_idx = conflict | mixed | POLS
keep_idx = {i: next(iter(v)) for i, v in want.items() if i not in skip_idx}
skip_keys = {(f, k) for f, k, h, c, en in restore if ref2i.get((f, k)) in skip_idx}
# ---- keep current rebranded GRF description ----
cur_desc = leaves(rd(PAIRS[0][0])).get("STR_GRF_DESC.base")
KEEP_DESC = ("src/grf/lang/simplified_chinese.toml", "STR_GRF_DESC.base", cur_desc)
# ---- direct TOML patches ----
byfile = collections.defaultdict(dict)
for f, k, h, c, en in restore:
    if (f, k) in skip_keys: continue
    if f == KEEP_DESC[0] and k == KEEP_DESC[1]:
        byfile[f][k] = KEEP_DESC[2]; continue
    byfile[f][k] = h
# ---- out-JSONL appends (last value per index) ----
out_path = "tools/_i18n_out/simplified_chinese.jsonl"
last = {}
for ln in rd(out_path).splitlines():
    try:
        o = json.loads(ln); last[o["i"]] = o["tr"]
    except: pass
appends = [(i, v) for i, v in sorted(keep_idx.items()) if last.get(i) != v]
# ---- report ----
L = []
L.append("APPLY %s RESTORE %d SKIP_KEYS %d OUT_APPENDS %d" % (APPLY, len(restore), len(skip_keys), len(appends)))
L.append("CONFLICT %s MIXED %s POLISHED_SKIP %s" % (sorted(conflict), sorted(mixed), len(POLS & set(want))))
L.append("ECON i=164 -> %r" % keep_idx.get(164))
L.append("STR_GRF_DESC kept = %r" % cur_desc[:80])
L.append("BRAND_GUARD excluded %d keys" % sum(1 for f,ef in PAIRS for k,en in leaves(rd(ef)).items() if k.lstrip('.') not in PROTECT and (lambda H,C: H.get(k) and C.get(k) and H[k]!=en and C[k]!=H[k] and H[k].count('FIRS')>C[k].count('FIRS') and C[k].count('CIRS')>=H[k].count('CIRS'))(leaves(head(f)),leaves(rd(f)))))
if APPLY:
    for f, pm in byfile.items():
        p = os.path.join(ROOT, f); txt = rd(f); lines = txt.split("\n"); pos = line_pos(txt)
        for k, v in pm.items():
            if k not in pos: L.append("MISSING_LINE %s %s" % (f, k)); continue
            i = pos[k]; m = ASSIGN.match(lines[i])
            lines[i] = "%s%s%s\"%s\"%s" % (m.group(1), m.group(2), m.group(3), esc(v), m.group(5))
        open(p, "w", encoding="utf-8", newline="").write("\n".join(lines))
    with open(os.path.join(ROOT, out_path), "a", encoding="utf-8") as fo:
        for i, v in appends: fo.write(json.dumps({"i": i, "tr": v}, ensure_ascii=False) + "\n")
    L.append("WROTE files=%d appends=%d" % (len(byfile), len(appends)))
else:
    L.append("DRY RUN - no files written")
open(os.path.join(ROOT, "tools/_i18n_zh_restore.log"), "w", encoding="utf-8").write("\n".join(L))
print(L[0]); print(L[1]); print(L[2]); print(L[5] if len(L)>5 else "")
