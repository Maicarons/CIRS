# -*- coding: utf-8 -*-
# Verify every language's .lng strings physically exist inside the compiled GRF.
import os, re, io, glob, json
os.chdir(r"G:\GitHub\CIRS")
data = open("generated/cirs.grf", "rb").read()
print("GRF bytes", len(data), "sha", __import__("hashlib").sha256(data).hexdigest()[:16])

def clean(v):
    # strip string commands + placeholders; keep natural text
    v = re.sub(r"\{[^}]*\}", " ", v)
    v = re.sub(r"\s+", " ", v).strip()
    return v

rows = []
for p in sorted(glob.glob("generated/lang/*.lng")):
    lang = os.path.basename(p)[:-4]
    cands = []
    for ln in io.open(p, encoding="utf-8"):
        if ":" not in ln or ln.startswith("#"): continue
        v = ln.split(":", 1)[1].strip()
        c = clean(v)
        # longest natural fragments with real letters (>=4 chars, non-ASCII preferred)
        if len(c) >= 6 and re.search(r"[^\x00-\x7F]", c):
            cands.append(c)
        elif len(c) >= 12:
            cands.append(c)
    cands = sorted(set(cands), key=lambda s: -len(s))[:80]
    hit = sum(1 for c in cands if c.encode("utf-8") in data)
    rows.append((lang, hit, len(cands)))

bad = [(l,h,t) for l,h,t in rows if h < t - 0 or (t and h < t)]
print("LANGS", len(rows))
print("FULL_HIT", sum(1 for l,h,t in rows if t and h == t))
print("ZERO_HIT", sum(1 for l,h,t in rows if h == 0))
print("PER_LANG")
for l,h,t in rows:
    flag = "OK" if t and h == t else ("PARTIAL" if h else "MISSING")
    print("  %-22s %3d/%3d %s" % (l,h,t,flag))
# script census
import collections
cnt = collections.Counter()
for m in re.finditer(rb"\xc3\x9e([^\x00]{1,400})", data):
    s = m.group(1)
    try: t = s.decode("utf-8")
    except: continue
    if re.search(r"[\uac00-\ud7af]", t): cnt["hangul"] += 1
    elif re.search(r"[\u3040-\u30ff]", t): cnt["kana"] += 1
    elif re.search(r"[\u0400-\u04ff]", t): cnt["cyrillic"] += 1
    elif re.search(r"[\u4e00-\u9fff]", t): cnt["cjk"] += 1
    elif re.search(r"[\u0b80-\u0bff]", t): cnt["tamil"] += 1
    elif re.search(r"[\u0600-\u06ff]", t): cnt["arabic"] += 1
    else: cnt["latin_or_ascii"] += 1
print("STRING_CENSUS", dict(cnt))
