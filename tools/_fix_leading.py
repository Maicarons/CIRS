import sys
sys.stdout.reconfigure(encoding="utf-8")
p = "tools/_lang_pt.txt"
L = open(p, encoding="utf-8").read().split("\n")
while L and L[0].strip() == "":
    L.pop(0)
L.insert(0, "")
open(p, "w", encoding="utf-8").write("\n".join(L))
gs = next(i for i, l in enumerate(L) if l.startswith("{COMPANY}"))
print("grf block lines:", gs, "first3:", [repr(x) for x in L[:3]])
