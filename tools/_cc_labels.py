
import io, glob, os, re
root = "G:/GitHub/CIRS/src/docs/lang"
for f in sorted(glob.glob(root + "/*.toml")):
    lang = os.path.basename(f)[:-5]
    d = {}
    for line in io.open(f, encoding="utf-8").read().splitlines():
        m = re.match(r'^(DOC_CC_(?:POTABLE|NON_POTABLE|WEIRD))\s*=\s*"(.*)"\s*$', line)
        if m: d[m.group(1)] = m.group(2)
    print("%-22s POTABLE=%-22s NON_POTABLE=%-26s WEIRD=%s" % (lang, d.get("DOC_CC_POTABLE","-"), d.get("DOC_CC_NON_POTABLE","-"), d.get("DOC_CC_WEIRD","-")))
