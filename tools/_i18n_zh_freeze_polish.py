import json, collections, os
out_path="tools/_i18n_out/simplified_chinese.jsonl"
byi=collections.defaultdict(list)
for ln in open(out_path,encoding="utf-8").read().splitlines():
    if not ln.strip(): continue
    try: o=json.loads(ln); byi[o["i"]].append(o["tr"])
    except: pass
polished=sorted(i for i,v in byi.items() if len(v)>1)
json.dump(polished,open("tools/_i18n_zh_polished_idx.json","w",encoding="utf-8"))
print("POLISHED_IDX",len(polished),"includes 224?",224 in polished)
