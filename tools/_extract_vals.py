import re

files = [
    "src/grf/lang/english.toml",
    "src/gs/lang/english.toml",
    "src/docs/extra_strings.toml",
]
vals = set()
pattern = re.compile(r'=\s*"((?:[^"\\]|\\.)*)"')
for f in files:
    text = open(f, encoding="utf-8").read()
    for m in pattern.finditer(text):
        v = m.group(1)
        if v:
            vals.add(v)
with open("tools/_vals.txt", "w", encoding="utf-8") as out:
    out.write("\n".join(sorted(vals)))
print("unique values:", len(vals))
