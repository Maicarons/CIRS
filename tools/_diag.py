import sys, os
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import _ai_translate as A

KEYS = list(A.FR.keys())

def load(suffix):
    p = os.path.join("tools", f"_lang_{suffix}.txt")
    if not os.path.exists(p):
        return None
    return [l.rstrip("\n") for l in open(p, encoding="utf-8") if l.strip() != ""]

def compat(key, de):
    # strong, structural checks only (avoids false positives on plain words)
    if key.startswith("{WEIGHT} of ") or key.startswith("{VOLUME} of "):
        tok = key.split(" of ")[0] + " de "
        return de.startswith(tok)
    if key.startswith("{SIGNED_WORD} bale"):
        return de.startswith("{SIGNED_WORD} fardo") or de.startswith("{SIGNED_WORD} bal")
    if key.startswith("{SIGNED_WORD} crate"):
        return de.startswith("{SIGNED_WORD} caja")
    for tok in ("{BLACK}", "{WHITE}", "{YELLOW}", "{ORANGE}", "{BLUE}",
               "{INDUSTRY}", "{RAW_STRING}"):
        if key.startswith(tok):
            return de.startswith(tok)
    return True  # plain word: assume ok

def find_gaps(suffix):
    de = load(suffix)
    if de is None:
        print(f"no _lang_{suffix}.txt"); return
    print(f"{suffix}: {len(de)} lines vs {len(KEYS)} keys")
    if len(de) != len(KEYS):
        print("  COUNT MISMATCH -- find gaps below and insert missing line(s)")
    n = min(len(KEYS), len(de))
    prev_bad = False
    for i in range(n):
        ok = compat(KEYS[i], de[i])
        if not ok and not prev_bad:
            print(f"  GAP likely at index {i}: key={KEYS[i][:45]!r}  de={de[i][:40]!r}")
        prev_bad = not ok
    print("done.")

if __name__ == "__main__":
    for s in ("de", "es", "pt", "ko", "ar"):
        find_gaps(s)
