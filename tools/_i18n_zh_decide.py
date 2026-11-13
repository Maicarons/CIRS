import subprocess, tomllib, re, json, os, io, collections, hashlib
def sh(*a): return subprocess.check_output(list(a)).decode("utf-8","replace")
def leaves(txt):
    d=tomllib.loads(txt); out={}
    for sec,v in d.items():
        if sec=="GLOBAL_PRAGMA": continue
        if isinstance(v,dict):
            for k,vv in v.items(): out[sec+"."+k]=vv if isinstance(vv,str) else str(vv)
        elif isinstance(v,str): out[sec]=v
    return out
L=[]
tracked=sh("git","ls-files","src/grf/lang/","src/gs/lang/","src/docs/lang/").splitlines()
L.append("TRACKED LANG FILES: %r"%[p for p in tracked if p.endswith(".toml")])
# DOC_NAV_SWITCH_LANGUAGE convention
nav={}
for f in sorted(__import__("glob").glob("src/docs/lang/*.toml")):
    d=tomllib.load(open(f,"rb"))
    nav[os.path.basename(f)[:-5]]=d.get("DOC_NAV_SWITCH_LANGUAGE")
L.append("DOC_NAV_SWITCH_LANGUAGE values (first 20): %r"%list(nav.items())[:20])
L.append("  counts: %r"%collections.Counter(nav.values()).most_common(12))
# rebrand outputs mentioning simplified_chinese
for name in ["tools/_i18n_rebrand_model_out.json","tools/_i18n_rebrand_tasks.json","tools/_i18n_rebrand_candidates.json"]:
    try: d=json.load(open(name,encoding="utf-8"))
    except Exception as e: L.append("DATA %s err %s"%(name,e)); continue
    s=json.dumps(d,ensure_ascii=False)
    zh=[x for x in (d if isinstance(d,list) else []) if isinstance(x,dict) and x.get("lang")=="simplified_chinese"]
    L.append("DATA %s zh_entries=%d"%(name,len(zh)))
    for x in zh[:12]: L.append("   %r"%x)
# git HEAD grf/gs/docs zh existence
for p in ["src/grf/lang/simplified_chinese.toml","src/gs/lang/simplified_chinese.toml","src/docs/lang/simplified_chinese.toml","src/grf/lang/traditional_chinese.toml"]:
    try:
        t=sh("git","show","HEAD:"+p); L.append("HEAD %s OK lines=%d"%(p,len(t.splitlines())))
    except Exception as e: L.append("HEAD %s MISSING (%s)"%(p,str(e)[:80]))
# current file encodings / newline style
for p in ["src/grf/lang/simplified_chinese.toml","src/gs/lang/simplified_chinese.toml","src/docs/lang/simplified_chinese.toml"]:
    b=open(p,"rb").read(); L.append("CUR %s bytes=%d crlf=%d lf=%d"%(p,len(b),b.count(b"\r\n"),b.count(b"\n")))
open("tools/_i18n_zh_decide.txt","w",encoding="utf-8").write("\n".join(L))
print("OK")
