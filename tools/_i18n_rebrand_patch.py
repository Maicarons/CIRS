#!/usr/bin/env python3
"""Unified rebrand patcher.
   Applies deterministic brand fixes, cargo-code restores, the manual French fix,
   and all model retranslations to the final TOMLs. Also appends corrected lines
   to tools/_i18n_out/<lang>.jsonl for any task that maps to a work-list index,
   so a later 'pipeline.py apply' cannot overwrite the fixes.
   Usage: python tools/_i18n_rebrand_patch.py [--dry]
"""
import json, re, sys, collections, os
ROOT = "."
T = json.load(open("tools/_i18n_rebrand_model_tasks.json", encoding="utf-8"))
ASSIGN = re.compile(r'^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)("(?:[^"\\]|\\.)*")(\s*(?:#.*)?)$')
SECTION = re.compile(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$')
PH = re.compile(r'\{([A-Za-z_0-9]*)\}')
def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")
def ph(s): return collections.Counter(PH.findall(s or ""))
def patch_file(file, key, tr, dry=False):
    with open(file, "r", encoding="utf-8") as f: lines = f.read().split("\n")
    sec = None; out = []; hit = 0; old_raw = ""
    for ln in lines:
        m = SECTION.match(ln)
        if m: sec = m.group(1)
        a = ASSIGN.match(ln)
        if a:
            full = (sec + "." + a.group(2)) if sec else a.group(2)
            if full == key:
                old_raw = a.group(4)[1:-1]
                if ph(old_raw) != ph(tr):
                    return ("PH_MISMATCH", old_raw, sorted(ph(old_raw).items()), sorted(ph(tr).items()))
                out.append(a.group(1)+a.group(2)+a.group(3)+'"'+esc(tr)+'"'+a.group(5)); hit += 1; continue
        out.append(ln)
    if hit != 1: return ("HIT_"+str(hit), old_raw, [], [])
    if not dry:
        with open(file, "w", encoding="utf-8", newline="\n") as f: f.write("\n".join(out))
    return ("OK", old_raw, [], [])
def main():
    dry = "--dry" in sys.argv
    todo = []
    for x in T["deterministic"]:
        tr = re.sub(r'(?<![A-Za-z])FIRS(?![A-Za-z])', 'CIRS', x["tr"])
        todo.append((x, tr, "deterministic"))
    for x in T["restore"]:
        todo.append((x, x["en"], "restore"))
    for x in T["manual"]:
        todo.append((x, x["tr"], "manual"))
    try: mo = json.load(open("tools/_i18n_rebrand_model_out.json", encoding="utf-8"))
    except FileNotFoundError: mo = []
    for x in mo:
        todo.append((x, x["tr"], "model"))
    # duplicate detection
    seen = {}
    dups = []
    for x, tr, kind in todo:
        k = (x["lang"], x["file"], x["key"])
        if k in seen: dups.append((k, seen[k], kind))
        seen[k] = kind
    print("TOTAL", len(todo), "DUPLICATES", len(dups))
    for d in dups[:10]: print("  DUP", d)
    stats = collections.Counter(); errs = []; append = collections.defaultdict(list)
    for x, tr, kind in todo:
        st, old, a, b = patch_file(x["file"], x["key"], tr, dry)
        stats[kind+"_"+st] += 1
        if st != "OK": errs.append((x["lang"], x["file"], x["key"], st, old[:120], a, b))
        if st == "OK" and x.get("in_work") and isinstance(x.get("work_index"), int):
            append[x["lang"]].append((x["work_index"], tr))
    print("PATCH", json.dumps(dict(stats)))
    for e in errs[:20]: print("ERR", e)
    print("OUT_JSONL_APPENDS", sum(len(v) for v in append.values()), "langs", len(append))
    if dry: print("DRY RUN — nothing written"); return
    for lang, pairs in append.items():
        p = os.path.join("tools", "_i18n_out", lang + ".jsonl")
        with open(p, "a", encoding="utf-8") as f:
            for i, tr in pairs: f.write(json.dumps({"i":i,"tr":tr}, ensure_ascii=False) + "\n")
    print("WROTE out-JSONL appends")
main()
