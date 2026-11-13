import os, sys, traceback
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import _build_i18n as b

lines = []
try:
    for lang in ["french", "german", "spanish", "portuguese", "korean"]:
        m = b.load_lng(os.path.join(b.REF, lang + ".lng"))
        lines.append(f"{lang} parsed pairs: {len(m)}")
        for k, v in list(m.items())[:3]:
            lines.append("    " + repr(k) + " -> " + repr(v[:40]))
    open(os.path.join(b.REF, "_dbg_out.txt"), "w", encoding="utf-8").write("\n".join(lines))
except Exception:
    open(os.path.join(b.REF, "_dbg_out.txt"), "w", encoding="utf-8").write(traceback.format_exc())
