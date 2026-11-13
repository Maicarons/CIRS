#!/usr/bin/env python3
"""Prepare the model retranslation task list (exclude confirmed false positives)."""
import json
t = json.load(open("tools/_i18n_rebrand_tasks.json", encoding="utf-8"))
survey = json.load(open("tools/_i18n_edge_survey.json", encoding="utf-8"))
# Confirmed false positives / manual cases
EXCLUDE = {
 ("simplified_chinese","DOC_GS_SETUP_B1_PREFIX"), ("traditional_chinese","DOC_GS_SETUP_B1_PREFIX"),
 ("german","STR_ERR_INCOMPATIBLE_PARAM_CITYSET.base"),
 ("dutch","DOC_CC_OPEN_BULK"), ("french","DOC_ECO_INDUSTRIES"),
}
MANUAL = [
 {"lang":"french","file":"src/docs/lang/french.toml","key":"DOC_ECO_CARGOS",
  "en":"{count} Cargos","tr":"{count} marchandises"},
]
retr = [x for x in t["retranslate"] if (x["lang"],x["key"]) not in EXCLUDE]
# attach hints
for x in retr:
    l, k = x["lang"], x["key"]
    x["name_hint"] = survey.get(l, {}).get("STR_GRF_NAME.base", "")
    x["note"] = ""
    if k == "STR_GRF_DESC.base":
        x["note"] = "这是模组简介：现在是名为 CIRS 的社区维护分支（community-maintained fork of FIRS）。标题与正文里凡英语写 CIRS 处必须用 CIRS，只有 'fork of FIRS' 里的 FIRS 指上游项目应保留；必须译出 'See website for more information, including how to use CIRS' 这层意思。"
    elif k in ("DOC_HOME_WHY_3_TITLE","DOC_HOME_WHY_3_DESC"):
        x["note"] = "git 术语 upstream（上游）请译成目标语言的地道说法，不要直接保留英文单词 upstream；保留 FIRS、git 等专有名词。"
    elif k == "STR_PARAM_DESC_ECONOMIES.base":
        x["note"] = "英语里两处 CIRS 必须译为 CIRS；不要出现英语里没有的 FIRS；保留 {SILVER}/{BLACK}/{}{} 等占位符。"
    elif k == "DOC_GS_CONFLICTS_P3_LINK":
        x["note"] = "必须译成目标语言，不要只改大小写；NewGRF 作为专有名词保留。"
    elif k.endswith(".cargo_unit"):
        x["note"] = "当前译文里混入了多余的 FIRS 一词，必须去掉；忠实译出 crate of ... supplies（……补给箱），保留 {SIGNED_WORD} 与 {P 0 "" s} 占位符。"
    elif k == "DOC_ECO_CARGOS":
        x["note"] = "若当前形式在该语言中是合法同形词可保留，否则译成地道的复数货物名。"
    elif k == "STR_ERR_INCOMPATIBLE_PARAM_CITYSET.base":
        x["note"] = "NA City Set 是参数专有名保留；'work with CIRS' 必须用 CIRS。"
json.dump({"retranslate":retr,"manual":MANUAL,"deterministic":t["deterministic"],"restore":t["restore"]},
          open("tools/_i18n_rebrand_model_tasks.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
print("model tasks", len(retr), "manual", len(MANUAL), "deterministic", len(t["deterministic"]), "restore", len(t["restore"]))
print("keys", json.dumps(dict(Counter(x["key"] for x in retr))))
