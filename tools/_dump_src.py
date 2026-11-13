import sys, tomllib
sys.stdout.reconfigure(encoding="utf-8")
grf = tomllib.load(open("src/grf/lang/english.toml", "rb"))
gs = tomllib.load(open("src/gs/lang/english.toml", "rb"))
out = []
out.append("[grf]  # %d strings" % len(grf))
for k, v in grf.items():
    out.append('%s\t%s' % (k, v.get("base", "")))
out.append("[gs]  # %d strings" % len(gs))
for k, v in gs.items():
    out.append('%s\t%s' % (k, v.get("base", "")))
open("tools/_src_mod.txt", "w", encoding="utf-8").write("\n".join(out))
print("wrote tools/_src_mod.txt with", len(grf) + len(gs), "source strings")
