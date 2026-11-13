import os, io, re, struct, collections
b=open("generated/cirs.grf","rb").read()
out=io.open("tools/_grf_lang_census.txt","w",encoding="utf-8")
out.write("GRF bytes %d\n\n"%len(b))
def hits(s): return b.count(s.encode("utf-8"))
probes={
 "korean":["CIRS 커뮤니티 산업 교체 세트","커뮤니티에서 유지 관리하는","가구 공장","마일드 마일드 웨스트"],
 "japanese":["CIRS コミュニティ産業置換セット","マイルド・マイルド・ウェスト"],
 "simplified_chinese":["CIRS 社区产业替换集","温和西部"],
 "traditional_chinese":["CIRS 社區產業替換套組","溫和的西部"],
 "russian":["Набор CIRS для замены"],
 "arabic":["مجموعة استبدال الصناعة المجتمعية"],
 "tamil":["CIRS சமூகத் தொழில் மாற்றுத் தொகுப்பு"],
 "welsh":["Set Disodli Diwydiant Cymunedol CIRS"],
 "german":["CIRS - Community Industry Replacement Set"],
}
out.write("=== exact .lng values present in GRF (UTF-8 byte count) ===\n")
for lang,ss in probes.items():
    out.write(" "+lang+" "+repr([(s[:20],hits(s)) for s in ss])+"\n")
out.write("\n=== UTF-8 lead-byte ranges in GRF ===\n")
for name,pat in [("Hangul EA..ED 3-byte", rb"[\xea-\xed][\x80-\xbf][\x80-\xbf]"),
                ("Cyrillic D0/D1", rb"\xd0[\x80-\xbf]|\xd1[\x80-\xbf]"),
                ("CJK E4..E9", rb"[\xe4-\xe9][\x80-\xbf][\x80-\xbf]"),
                ("Arabic D8..DB", rb"[\xd8-\xdb][\x80-\xbf]"),
                ("Kana E3 81..83", rb"\xe3[\x81-\x83][\x80-\xbf]")]:
    out.write("  %-26s %d\n"%(name,len(re.findall(pat,b))))
# GRF container: sprite records. Action4 chunks have first byte 0x04, then langid byte.
out.write("\n=== GRF container sprite scan (action-byte census) ===\n")
# Standard GRF: 2 bytes '00 00' marker, then repeated [4-byte size][1-byte info][data][4-byte sprite-size + sprite data]
i=8; acts=collections.Counter(); langcounts=collections.Counter(); total=0
try:
  while i+5<=len(b):
    size=struct.unpack_from("<I",b,i)[0]; i+=4
    info=b[i]; i+=1
    if size==0: break
    data=b[i:i+size]; i+=size
    total+=1
    if data: acts[data[0]]+=1
    # pseudo-sprite: action4 = 0x04, next byte langid
    if data and data[0]==0x04 and len(data)>=2:
      langcounts[data[1]]+=1
    spr=struct.unpack_from("<I",b,i)[0]; i+=4
    if spr==0: break
    i+=spr
except Exception as e:
  out.write("scan stopped: "+repr(e)+" at "+str(i)+"\n")
out.write("  pseudo-sprites seen: %d\n"%total)
out.write("  action first-bytes: %s\n"%repr(acts.most_common(12)))
out.write("  Action4 langid census (%d distinct):\n"%len(langcounts))
for k,v in sorted(langcounts.items()): out.write("    0x%02X : %d\n"%(k,v))
out.write("\n=== .lng grflangid -> expected Action4 count ===\n")
import glob
for p in sorted(glob.glob("generated/lang/*.lng")):
  first=io.open(p,encoding="utf-8").readline().strip()
  m=re.search(r"0x([0-9A-Fa-f]+)",first)
  lid=int(m.group(1),16) if m else -1
  out.write("  %-26s 0x%02X  action4=%d\n"%(os.path.basename(p),lid,langcounts.get(lid,0)))
out.close()
print("WROTE tools/_grf_lang_census.txt")
print("action4 distinct langs",len(langcounts),"total action4",sum(langcounts.values()))
