import json, collections
lines=[l for l in open("tools/_i18n_out/simplified_chinese.jsonl",encoding="utf-8").read().splitlines() if l.strip()]
byi=collections.defaultdict(list)
for l in lines:
    o=json.loads(l); byi[o["i"]].append(o["tr"])
multi={i for i,v in byi.items() if len(v)>1}
D=json.load(open("tools/_i18n_zh_restore_data.json",encoding="utf-8"))
restore=D["restore"]
W=json.load(open("tools/_i18n_work/simplified_chinese.json",encoding="utf-8")); E=W["entries"] if isinstance(W,dict) else W
ref2i={}
for i,e in enumerate(E):
    for rf in e.get("refs",[]): ref2i[(rf[0].replace("\\","/").lstrip("./"),rf[1])]=i
polished_keys=[]
for f,k,h,c,en in restore:
    i=ref2i.get((f,k))
    if i is not None and i in multi:
        polished_keys.append((f,k,i,h,byi[i][-1]))
print("MULTI_IDX",len(multi),"RESTORE∩MULTI",len(polished_keys))
for f,k,i,h,last in polished_keys[:40]:
    print("  i=%d %s %s"%(i,f,k))
    print("    HEAD=%r"%h[:100]); print("    POLISHED=%r"%last[:100])
open("tools/_i18n_zh_polished_overlap.txt","w",encoding="utf-8").write("\n".join("%d %s %s HEAD=%r POLISHED=%r"%(i,f,k,h,last) for f,k,i,h,last in polished_keys))
