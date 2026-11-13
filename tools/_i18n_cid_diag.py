import json, re, tomllib, subprocess, os
# report helper's cid logic
t=open("tools/_i18n_make_report.py",encoding="utf-8").read()
i=t.find("def round3_quality")
print("=== round3_quality source ===")
print(t[i:i+3000])
