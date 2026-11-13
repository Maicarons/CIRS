#!/usr/bin/env python3
import json
T = json.load(open("tools/_i18n_rebrand_model_tasks.json", encoding="utf-8"))
try: mo = json.load(open("tools/_i18n_rebrand_model_out.json", encoding="utf-8"))
except FileNotFoundError: mo = []
for name, arr in [("deterministic", T["deterministic"]), ("restore", T["restore"]), ("manual", T["manual"]), ("model_desc", mo), ("remaining", [x for x in T["retranslate"] if x["key"]!="STR_GRF_DESC.base"])]:
    inw = [x for x in arr if x.get("in_work")]
    print(name, "total", len(arr), "in_work", len(inw))
    for x in inw[:12]: print("   ", x["lang"], x["key"], "wi", x.get("work_index"))
