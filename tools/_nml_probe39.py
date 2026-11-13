# -*- coding: utf-8 -*-
import sys, io, os, glob
os.chdir(r"G:\GitHub\CIRS")
import nml.grfstrings as g
# capture warnings
import nml.generic as gen
warn = []
orig = gen.print_warning
def cap(*a, **k):
    warn.append(" ".join(str(x) for x in a))
    return None
gen.print_warning = cap
g.langs[:] = []
g.read_lang_files("generated/lang", "english.lng")
gen.print_warning = orig
print("LANGS", len(g.langs))
print("LANGIDS", " ".join("%02X" % x[0] for x in g.langs))
print("WARNINGS", len(warn))
for w in warn[:30]: print("  W:", w[:170])
