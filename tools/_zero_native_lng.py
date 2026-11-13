import os, re, io, glob, collections
PH=re.compile(r"\{[A-Za-z_0-9]*\}")
NATIVE={
 "korean": lambda c:'\uac00'<=c<='\ud7a3' or '\u3130'<=c<='\u318f',
 "japanese": lambda c:('\u3040'<=c<='\u30ff') or ('\u4e00'<=c<='\u9fff'),
 "simplified_chinese": lambda c:'\u4e00'<=c<='\u9fff',
 "traditional_chinese": lambda c:'\u4e00'<=c<='\u9fff',
 "russian": lambda c:'\u0400'<=c<='\u04ff',
 "belarusian": lambda c:'\u0400'<=c<='\u04ff',
 "serbian": lambda c:'\u0400'<=c<='\u04ff',
 "arabic": lambda c:'\u0600'<=c<='\u06ff',
 "tamil": lambda c:'\u0b80'<=c<='\u0bff',
}
def strip(s): return PH.sub("",s)
def has_letter(s): return bool(re.search(r"[A-Za-z]",s))
def main():
  print("=== RAW zero-native-script values in generated/lang/*.lng (game strings) ===")
  for lang,n in sorted(NATIVE.items()):
    p="generated/lang/"+lang+".lng"
    if not os.path.exists(p): continue
    rows=[]
    for ln in io.open(p,encoding="utf-8").read().splitlines():
      if ln.startswith("#") or ":" not in ln: continue
      k,v=ln.split(":",1); k=k.strip(); v=strip(v.strip())
      if not has_letter(v): continue
      if any(n(c) for c in v): continue
      rows.append((k,v[:130]))
    print("  %-22s zero_native=%3d" % (lang,len(rows)))
    if lang in ("korean","japanese","tamil"):
      for k,v in rows[:25]: print("      ",k,"|",v)
  with io.open("tools/_zero_native_lng.txt","w",encoding="utf-8") as f:
    for lang,n in sorted(NATIVE.items()):
      p="generated/lang/"+lang+".lng"
      if not os.path.exists(p): continue
      f.write("### "+lang+"\n")
      for ln in io.open(p,encoding="utf-8").read().splitlines():
        if ln.startswith("#") or ":" not in ln: continue
        k,v=ln.split(":",1); k=k.strip(); v=strip(v.strip())
        if not has_letter(v): continue
        if any(n(c) for c in v): continue
        f.write("  "+k+" | "+v[:160].replace("\n","\\n")+"\n")
      f.write("\n")
  print("WROTE tools/_zero_native_lng.txt")
main()
