import sys, os, io, traceback
sys.path.insert(0, r"C:\Users\Maicarons\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages")
import nml.grfstrings as g
print("nml file:", g.__file__)
print("has read_lang_files:", hasattr(g,"read_lang_files"), "has read_lang:", hasattr(g,"read_lang"))
import inspect
for n in dir(g):
    if "lang" in n.lower() and ("read" in n.lower() or "load" in n.lower() or "parse" in n.lower()):
        o=getattr(g,n)
        if callable(o):
            try: print("  ",n, inspect.signature(o))
            except Exception: print("  ",n)
print()
print("=== try read_lang_files('generated/lang') ===")
try:
    res=g.read_lang_files("generated/lang")
    print("returned:", type(res), len(res) if hasattr(res,"__len__") else "?")
    try:
        for x in res: print("  ",x[:2] if isinstance(x,tuple) else x)
    except Exception as e: print("  iterate err",e)
except Exception as e:
    print("ERR",repr(e)); traceback.print_exc()
print()
print("=== langs global after call ===")
try:
    print("len(g.langs)=",len(g.langs))
    for lid,lang in g.langs:
        print("  0x%02X"%lid, "n_strings=", len(lang.strings), "gender=",getattr(lang,"genders",None), "case=",getattr(lang,"cases",None))
except Exception as e:
    print("ERR",repr(e)); traceback.print_exc()
