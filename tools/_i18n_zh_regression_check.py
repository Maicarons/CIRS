import subprocess, tomllib, io, json, re
def head(p):
    try:
        return subprocess.check_output(["git","show","HEAD:"+p]).decode("utf-8")
    except Exception as e:
        return None
def leaves(txt):
    out={}; sec=None
    for ln in txt.splitlines():
        m=re.match(r'^\s*\[([^\]]+)\]\s*(?:#.*)?$',ln)
        if m: sec=m.group(1); continue
        m=re.match(r'^\s*([A-Za-z0-9_-]+)\s*=\s*"(.*)"\s*$',ln)
        if m: out[(sec or "")+"."+m.group(1)]=m.group(2)
    return out
files=["src/grf/lang/simplified_chinese.toml","src/gs/lang/simplified_chinese.toml","src/docs/lang/simplified_chinese.toml"]
en_files=["src/grf/lang/english.toml","src/gs/lang/english.toml","src/docs/lang/english.toml"]
for f,ef in zip(files,en_files):
    h=head(f); e=leaves(open(ef,encoding="utf-8").read()); c=leaves(open(f,encoding="utf-8").read())
    H=leaves(h) if h else {}
    keys=list(e.keys())
    human_over=[k for k in keys if k in H and H[k]!=e[k] and c.get(k)!=H[k]]
    head_en=[k for k in keys if k in H and H[k]==e[k]]
    print("FILE",f,"keys",len(keys),"human_overwritten",len(human_over),"head_untranslated",len(head_en))
    for k in human_over[:14]:
        print("  KEY",k)
        print("    HEAD:",H[k][:150])
        print("    CUR :",c.get(k,"")[:150])
print("=== THREE MONTHS OCCURRENCES ===")
txt=open(files[0],encoding="utf-8").read()
for i,ln in enumerate(txt.splitlines(),1):
    if "三个月" in ln or "次水准" in ln:
        print(i, ln.strip()[:220])
