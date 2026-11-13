import tomllib
d = tomllib.load(open("src/gs/lang/english.toml", "rb"))
for k, v in d.items():
    if isinstance(v, dict):
        print(f"{k}\t{v.get('base','')}")
