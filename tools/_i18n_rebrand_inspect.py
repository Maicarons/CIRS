#!/usr/bin/env python3
import json, re, io
T = json.load(open("tools/_i18n_rebrand_model_tasks.json", encoding="utf-8"))
try: mo = json.load(open("tools/_i18n_rebrand_model_out.json", encoding="utf-8"))
except FileNotFoundError: mo = []
o = io.StringIO()
o.write("=== DESC RETRANSLATIONS "+str(len(mo))+" ===\n")
for x in mo:
    o.write(x["lang"]+" | CIRS:"+str(x["tr"].count("CIRS"))+" FIRS:"+str(x["tr"].count("FIRS"))+" | len:"+str(len(x["tr"]))+"\n")
    o.write("   "+x["tr"][:320].replace("\n"," ")+"\n")
rem = [x for x in T["retranslate"] if x["key"]!="STR_GRF_DESC.base"]
o.write("\n=== REMAINING RETRANSLATE (non-desc) "+str(len(rem))+" ===\n")
for x in rem:
    o.write(x["lang"]+" "+x["file"]+" "+x["key"]+"\n")
    o.write("   EN: "+x["en"][:220]+"\n")
    o.write("   TR: "+x["tr"][:220]+"\n")
    o.write("   NOTE: "+x.get("note","")[:150]+"\n")
o.write("\n=== DETERMINISTIC sample (first 8) ===\n")
for x in T["deterministic"][:8]:
    tr = re.sub(r'(?<![A-Za-z])FIRS(?![A-Za-z])', 'CIRS', x["tr"])
    o.write(x["lang"]+" "+x["key"]+" | "+x["tr"][:110]+" => "+tr[:110]+"\n")
o.write("\n=== RESTORE ===\n")
for x in T["restore"]: o.write(x["lang"]+" "+x["file"]+" "+x["key"]+" "+repr(x["tr"])+" => "+repr(x["en"])+"\n")
o.write("\n=== MANUAL ===\n")
for x in T["manual"]: o.write(json.dumps(x, ensure_ascii=False)+"\n")
o.write("\n=== IN_WORK non-desc ===\n")
for x in rem: o.write(x["lang"]+" "+x["key"]+" wi="+str(x.get("work_index"))+" in_work="+str(x.get("in_work"))+"\n")
open("tools/_i18n_rebrand_inspect.txt","w",encoding="utf-8").write(o.getvalue())
print("wrote", len(o.getvalue()), "chars")
