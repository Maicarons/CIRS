#!/usr/bin/env python3
"""Round-3 triage: precise zh-Hant simplified chars, rendered short-code health, work coverage."""
import importlib.util, json, re, glob, os, collections, io
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
lm = p.lang_map(); extras = p.extra_files(lm)
out = io.StringIO()

# --- precise unambiguous simplified-only char map (never valid in Traditional) ---
S = "检简温鲁馏装压状带构块盖设细圆铜胶灵处与广结长园杂单热浓进种来为电学机筑铸属输运气产钢业类铁炼纤浆经划发几没还对开关问间东车马鸟门风无爱边节术叶虽归务办华极众体邮纸张标场陈迟冲虫触传创辞达当导岛敌递点垫钓调叠顶订动独断队吨顿夺鹅儿尔访纺飞坟奋丰凤肤负赶冈刚纲个给巩贡沟购顾观馆贯龟规贵滚国过汉号壶护怀坏欢环缓换汇会浑获击积鸡际继纪夹见将奖讲较阶届紧尽劲径镜纠旧举据决军凯课恳垦夸况亏扩兰拦览滥劳乐厘离礼丽厉联连练俩脸凉辆疗临铃领刘龙楼卢陆录吕乱论罗骆妈码骂买麦卖蛮满闷们梦弥庙灭鸣铭纳难脑闹拟宁纽农欧盘贫评凭铺朴齐骑启弃牵签钱浅枪强抢桥亲轻倾请庆穷区劝却让饶认荣软锐润伞扫纱筛删闪陕伤绍时识实试视书树双谁顺说苏诉肃随岁孙态摊谈汤讨题条贴听统头图团弯万网围维伟卫闻吴误雾习显现线项销晓协写兴许续选寻讯严盐验扬阳养样约药页医仪遗义艺忆议异译阴银饮应拥优犹鱼语预员缘远愿云载则择泽责赠战这针诊阵争征证织职执质终钟专砖转壮准浊资综总纵组检简温鲁馏装压状带构块盖设细圆铜胶灵处与广结长园杂单热浓进种来为电学机筑铸属输运气产钢业类铁炼纤浆经划"
T = "檢簡溫魯餾裝壓狀帶構塊蓋設細圓銅膠靈處與廣結長園雜單熱濃進種來為電學機築鑄屬輸運氣產鋼業類鐵煉纖漿經劃發幾沒還對開關問間東車馬鳥門風無愛邊節術葉雖歸務辦華極眾體郵紙張標場陳遲衝蟲觸傳創辭達當導島敵遞點墊釣調疊頂訂動獨斷隊噸頓奪鵝兒爾訪紡飛墳奮豐鳳膚負趕岡剛綱個給鞏貢溝購顧觀館貫龜規貴滾國過漢號壺護懷壞歡環緩換匯會渾獲擊積雞際繼紀夾見將獎講較階屆緊盡勁徑鏡糾舊舉據決軍凱課懇墾誇況虧擴蘭攔覽濫勞樂釐離禮麗厲聯連練倆臉涼輛療臨鈴領劉龍樓盧陸錄呂亂論羅駱媽碼罵買麥賣蠻滿悶們夢彌廟滅鳴銘納難腦鬧擬寧紐農歐盤貧評憑鋪樸齊騎啟棄牽簽錢淺槍強搶橋親輕傾請慶窮區勸卻讓饒認榮軟銳潤傘掃紗篩刪閃陝傷紹時識實試視書樹雙誰順說蘇訴肅隨歲孫態攤談湯討題條貼聽統頭圖團彎萬網圍維偉衛聞吳誤霧習顯現線項銷曉協寫興許續選尋訊嚴鹽驗揚陽養樣約藥頁醫儀遺義藝憶議異譯陰銀飲應擁優猶魚語預員緣遠願雲載則擇澤責贈戰這針診陣爭徵證織職執質終鐘專磚轉壯準濁資綜總縱組檢簡溫魯餾裝壓狀帶構塊蓋設細圓銅膠靈處與廣結長園雜單熱濃進種來為電學機築鑄屬輸運氣產鋼業類鐵煉纖漿經劃"
assert len(S) == len(T), (len(S), len(T))
MAP = dict(zip(S, T))
ZHANT = ["src/docs/lang/traditional_chinese.toml","src/grf/lang/traditional_chinese.toml","src/gs/lang/traditional_chinese.toml","src/docs/extra_strings_traditional_chinese.toml"]
out.write("=== PRECISE zh-Hant simplified-char lines (unambiguous map " + str(len(MAP)) + " chars) ===\n")
lines=[]
for f in ZHANT:
    for i, ln in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
        if "=" not in ln or ln.lstrip().startswith("#"): continue
        chars = sorted({c for c in ln if c in MAP})
        if chars: lines.append((f, i, "".join(chars), ln.strip()))
out.write("TOTAL lines " + str(len(lines)) + "\n")
for f,i,cs,ln in lines: out.write(f.replace("\\","/") + ":" + str(i) + " | " + cs + " | " + ln[:180] + "\n")
json.dump([{"file":f,"line":i,"chars":cs,"text":ln} for f,i,cs,ln in lines], open("tools/_i18n_round3_zhant.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

# --- rendered short-code files health ---
SHORT = {"zh":"extra_strings_zh.toml","fr":"extra_strings_fr.toml","de":"extra_strings_de.toml","es":"extra_strings_es.toml","pt":"extra_strings_pt.toml","ko":"extra_strings_ko.toml","ar":"extra_strings_ar.toml"}
en_ref = p.leaves(p.load(R/"src/docs/extra_strings.toml"))
CYR = re.compile("[\u0400-\u04ff]"); KANA = re.compile("[\u3040-\u30ff]")
out.write("\n=== RENDERED short-code extra_strings health ===\n")
for code, fn in SHORT.items():
    f = "src/docs/" + fn
    tv = p.leaves(p.load(R/f))
    eng = [k for k,v in tv.items() if v == en_ref.get(k)]
    firs = [(k,v) for k,v in tv.items() if re.search(r"(?<![A-Za-z])FIRS(?![A-Za-z])", v)]
    cyr = [(k,v) for k,v in tv.items() if CYR.search(v)]
    kana = [(k,v) for k,v in tv.items() if KANA.search(v)]
    out.write(fn + " keys=" + str(len(tv)) + " english=" + str(len(eng)) + " FIRS=" + str(len(firs)) + " cyr=" + str(len(cyr)) + " kana=" + str(len(kana)) + "\n")
    for k,v in (firs[:4]+cyr[:2]+kana[:2]): out.write("    " + k + " | " + v[:150] + "\n")

# --- work-list coverage for dual files + contaminated strings ---
out.write("\n=== WORK-LIST COVERAGE ===\n")
work = {}
for f in sorted(glob.glob("tools/_i18n_work/*.json")):
    lang = os.path.basename(f)[:-5]
    work[lang] = json.load(open(f, encoding="utf-8"))
def has_ref(lang, filefrag, key):
    w = work.get(lang)
    if not w: return False
    for e in w.get("entries", w if isinstance(w,list) else []):
        refs = e.get("refs", [])
        for r in refs:
            rr = r[0] if isinstance(r,(list,tuple)) else r
            kk = r[1] if isinstance(r,(list,tuple)) and len(r)>1 else ""
            if filefrag in str(rr).replace("\\","/") and key in str(kk): return True
    return False
pairs = [("croatian","extra_strings_croatian.toml","CARGO_INFO_PLANT_AND_MACHINERY.base"),
         ("danish","grf/lang/danish.toml","STR_CARGO_AMMONIA_AND_NITRIC_PRODUCTS.name"),
         ("norwegian_bokmal","grf/lang/norwegian_bokmal.toml","STR_CARGO_AMMONIA_AND_NITRIC_PRODUCTS.name"),
         ("traditional_chinese","extra_strings_traditional_chinese.toml","CARGO_INFO_WOOD_PULP.base")]
for l,f,k in pairs: out.write("contam " + l + " " + k + " in_work=" + str(has_ref(l,f,k)) + "\n")
for l in ["french","german","spanish","simplified_chinese","korean","arabic","portuguese"]:
    w = work.get(l, {}); ents = w.get("entries", w if isinstance(w,list) else [])
    cnt = collections.Counter()
    for e in ents:
        for r in e.get("refs", []):
            rr = str(r[0]).replace("\\","/") if isinstance(r,(list,tuple)) else str(r)
            if "extra_strings_" in rr: cnt[rr.split("/")[-1]] += 1
    out.write("dual " + l + " extra refs " + json.dumps(dict(cnt)) + "\n")

open("tools/_i18n_round3_triage.txt","w",encoding="utf-8").write(out.getvalue())
print("wrote", len(out.getvalue()), "chars; zhant lines", len(lines))
