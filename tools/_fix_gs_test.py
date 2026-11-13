import sys
import tomllib

sys.stdout.reconfigure(encoding="utf-8")
en = tomllib.load(open("src/gs/lang/english.toml", "rb"))
es = tomllib.load(open("src/gs/lang/spanish.toml", "rb"))
ks = [
    "STR_TOWN_STORY_PAGE_TEST",
    "STR_TOWN_STORY_PAGE_REQUIRED_CARGO_STATS",
    "STR_TOWN_STORY_INDUSTRY_REPORT_ACCEPTED_TITLE",
    "STR_MANUFACTURERS_STORY_PAGE_TEST",
    "STR_MANUFACTURERS_STORY_PAGE_VALID_TOWNS",
    "STR_CABBAGE_CLICKABLE_TEST",
]
for k in ks:
    print("EN", k, "=>", repr(en.get(k, {}).get("base")))
    print("ES", k, "=>", repr(es.get(k, {}).get("base")))
    print()
