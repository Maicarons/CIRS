
import os, re
ROOT = "G:/GitHub/CIRS"
DOCS = ROOT + "/src/docs/lang"
# endonym per language-key
END = {
 "DOC_TRANS_LANG_EN":"English","DOC_TRANS_LANG_ZH":"简体中文","DOC_TRANS_LANG_FR":"Français","DOC_TRANS_LANG_DE":"Deutsch","DOC_TRANS_LANG_ES":"Español","DOC_TRANS_LANG_PT":"Português","DOC_TRANS_LANG_KO":"한국어","DOC_TRANS_LANG_AR":"العربية",
 "DOC_TRANS_LANG_AFRIKAANS":"Afrikaans","DOC_TRANS_LANG_BELARUSIAN":"Беларуская","DOC_TRANS_LANG_CATALAN":"Català","DOC_TRANS_LANG_CROATIAN":"Hrvatski","DOC_TRANS_LANG_CZECH":"Čeština","DOC_TRANS_LANG_DANISH":"Dansk","DOC_TRANS_LANG_DUTCH":"Nederlands","DOC_TRANS_LANG_ENGLISH":"English",
 "DOC_TRANS_LANG_ENGLISH_AU":"English (AU)","DOC_TRANS_LANG_ENGLISH_US":"English (US)","DOC_TRANS_LANG_ESPERANTO":"Esperanto","DOC_TRANS_LANG_ESTONIAN":"Eesti","DOC_TRANS_LANG_FINNISH":"Suomi","DOC_TRANS_LANG_FRENCH":"Français","DOC_TRANS_LANG_GAELIC":"Gàidhlig","DOC_TRANS_LANG_GALICIAN":"Galego",
 "DOC_TRANS_LANG_GERMAN":"Deutsch","DOC_TRANS_LANG_HUNGARIAN":"Magyar","DOC_TRANS_LANG_INDONESIAN":"Indonesia","DOC_TRANS_LANG_ITALIAN":"Italiano","DOC_TRANS_LANG_JAPANESE":"日本語","DOC_TRANS_LANG_KOREAN":"한국어","DOC_TRANS_LANG_LATIN":"Latina","DOC_TRANS_LANG_LUXEMBOURGISH":"Lëtzebuergesch",
 "DOC_TRANS_LANG_NORWEGIAN_BOKMAL":"Norsk (Bokmål)","DOC_TRANS_LANG_POLISH":"Polski","DOC_TRANS_LANG_PORTUGUESE":"Português","DOC_TRANS_LANG_PORTUGUESE_BR":"Português (BR)","DOC_TRANS_LANG_ROMANIAN":"Română","DOC_TRANS_LANG_RUSSIAN":"Русский","DOC_TRANS_LANG_SERBIAN":"Српски","DOC_TRANS_LANG_SIMPLIFIED_CHINESE":"简体中文",
 "DOC_TRANS_LANG_SLOVAK":"Slovenčina","DOC_TRANS_LANG_SPANISH":"Español","DOC_TRANS_LANG_SPANISH_MX":"Español (MX)","DOC_TRANS_LANG_SWEDISH":"Svenska","DOC_TRANS_LANG_TAMIL":"தமிழ்","DOC_TRANS_LANG_TRADITIONAL_CHINESE":"繁體中文","DOC_TRANS_LANG_TURKISH":"Türkçe","DOC_TRANS_LANG_WELSH":"Cymraeg",
}
def apply_file(path):
    with open(path,"rb") as f: text=f.read().decode("utf-8")
    lines=text.split("\n"); changed=0
    for i,l in enumerate(lines):
        s=l.rstrip("\r")
        m=re.match(r'^(DOC_TRANS_LANG_[A-Z_0-9]+)\s*=\s*"(.*)"\s*$', s)
        if m and m.group(1) in END:
            new = '%s = "%s"' % (m.group(1), END[m.group(1)])
            if new != s: lines[i]=new; changed+=1
    out="\n".join(lines)
    if out!=text:
        with open(path,"wb") as f: f.write(out.encode("utf-8"))
    return changed
total=0
for f in sorted(os.listdir(DOCS)):
    if not f.endswith(".toml") or f=="english.toml": continue
    c=apply_file(DOCS+"/"+f)
    if c: total+=c; print("  %-22s %d"%(f[:-5],c))
print("TOTAL docs changes:",total)
