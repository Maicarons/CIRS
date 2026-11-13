import os, traceback
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "_4x_ref")
results = []
try:
    for f in ["english", "german", "french", "spanish", "portuguese", "portuguese_br", "korean"]:
        p = os.path.join(OUT, f + ".lng")
        with open(p, encoding="utf-8") as fp:
            lines = fp.read().splitlines()[:3]
        results.append("::".join([f] + lines))
    with open(os.path.join(OUT, "_hdr_out.txt"), "w", encoding="utf-8") as out:
        out.write("\n".join(results))
    print("WROTE OK")
except Exception:
    with open(os.path.join(OUT, "_hdr_out.txt"), "w", encoding="utf-8") as out:
        out.write(traceback.format_exc())
    print("ERROR")
