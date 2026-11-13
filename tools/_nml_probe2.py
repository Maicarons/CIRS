import sys, os, io, traceback, contextlib
sys.path.insert(0, r"C:\Users\Maicarons\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages")
import nml.grfstrings as g, nml.generic as gen
print("=== calling read_lang_files('generated/lang','english.lng') ===")
buf=io.StringIO()
try:
    with contextlib.redirect_stderr(buf), contextlib.redirect_stdout(buf):
        g.read_lang_files("generated/lang","english.lng")
    print("call returned OK")
except Exception as e:
    print("CALL ERR",repr(e)); traceback.print_exc()
print("captured output:")
print(buf.getvalue()[:6000])
print("=== g.langs after call: %d ==="%len(g.langs))
for lid,lang in g.langs:
    print("  0x%02X strings=%-4d genders=%-5s cases=%-5s plural=%s"%(lid,len(lang.strings),str(getattr(lang,"genders",None))[:40],str(getattr(lang,"cases",None))[:40],getattr(lang,"plural",None)))
print("=== NEWGRF language ids present ===")
have=set(x[0] for x in g.langs)
for l in ("english","korean","japanese","russian","serbian","traditional_chinese","welsh","simplified_chinese","czech","croatian","polish"):
    import re
    first=open("generated/lang/"+l+".lng",encoding="utf-8").readline()
    m=re.search(r"0x([0-9A-Fa-f]+)",first); lid=int(m.group(1),16)
    print("  %-24s 0x%02X  loaded=%s"%(l,lid,lid in have))
