import os, io, re, glob
b=open("generated/cirs.grf","rb").read()
print("GRF bytes", len(b))
def hits(s): return b.count(s.encode("utf-8"))
print("\n=== exact .lng values present in GRF (UTF-8 byte count) ===")
probes={
 "korean":["CIRS 커뮤니티 산업 교체 세트","커뮤니티에서 유지 관리하는","가구 공장","마일드 마일드 웨스트","최소 3분에 한 번씩"],
 "japanese":["CIRS コミュニティ産業置換セット","マイルド・マイルド・ウェスト","家具工場"],
 "simplified_chinese":["CIRS 社区产业替换集","温和西部","家具厂"],
 "traditional_chinese":["CIRS 社區產業替換套組","溫和的西部","家具工廠"],
 "russian":["Набор CIRS для замены","Мягкий мягкий запад"],
 "arabic":["مجموعة استبدال الصناعة المجتمعية"],
 "tamil":["CIRS சமூகத் தொழில் மாற்றுத் தொகுப்பு"],
 "serbian":["CIRS комплет за замену"],
 "welsh":["Set Disodli Diwydiant Cymunedol CIRS"],
}
for lang,ss in probes.items():
    print(" ",lang, [(s[:24],hits(s)) for s in ss])
print("\n=== count UTF-8 lead-byte ranges in GRF ===")
for name,pat in [("Hangul E1 84.. / EA..ED", rb"[\xea-\xed][\x80-\xbf][\x80-\xbf]"),
                ("Cyrillic D0..D1", rb"\xd0[\x80-\xbf]|\xd1[\x80-\xbf]"),
                ("CJK E4..E9", rb"[\xe4-\xe9][\x80-\xbf][\x80-\xbf]"),
                ("Arabic D8..DB", rb"[\xd8-\xdb][\x80-\xbf]"),
                ("Kana E3 81..83", rb"\xe3[\x81-\x83][\x80-\xbf]")]:
    print("  %-28s %d" % (name,len(re.findall(pat,b))))
print("\n=== language-name markers in GRF ===")
for s in ["korean","Korean","한국어","##grflangid","CIRS"]:
    print("  %-16s %d" % (s,hits(s)))
