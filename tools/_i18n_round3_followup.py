#!/usr/bin/env python3
"""Round-3 follow-up: exact duplicate collapse, dual-file diff samples, render target, zh-Hant census."""
import importlib.util, json, glob, os, collections, io
spec = importlib.util.spec_from_file_location("p", "tools/_i18n_pipeline.py")
p = importlib.util.module_from_spec(spec); spec.loader.exec_module(p)
R = p.R
lm = p.lang_map(); extras = p.extra_files(lm)
langs = sorted(k for k in lm if k != "english")
out = io.StringIO()

# --- (1) EXACT (Unicode-preserving) duplicate collapse ---
out.write("=== EXACT DUPLICATE COLLAPSE (>=3 distinct English -> same exact translation) ===\n")
dups = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
for l in langs:
    for grp, tgt, ref in p.targets(l, lm, extras):
        en = p.leaves(p.load(R/ref)); tv = p.leaves(p.load(R/tgt))
        for k, ev in en.items():
            if p.SKIP_KEY.match(k) or p.placeholder_only(ev): continue
            v = tv.get(k)
            if v is None or v == ev or p.ph(v) != p.ph(ev): continue
            norm = " ".join(v.lower().split())
            if len(norm) < 6: continue
            dups[l][norm][tgt].append((k, ev, v))
n = 0
for l, groups in sorted(dups.items()):
    for norm, byfile in groups.items():
        pairs = [(k,ev,v) for arr in byfile.values() for k,ev,v in arr]
        uniq_en = set(ev for k,ev,v in pairs)
        if len(uniq_en) >= 3:
            n += 1
            out.write(l + " | tr=" + norm[:110] + " | distinct_en=" + str(len(uniq_en)) + " | slots=" + str(len(pairs)) + "\n")
            for k,ev,v in pairs[:8]: out.write("    " + k + " | EN: " + ev[:110] + " | TR: " + v[:110] + "\n")
out.write("TOTAL exact dup groups " + str(n) + "\n")

# --- (2) dual extra_strings short/long diffs ---
SHORT = {"zh":"simplified_chinese","fr":"french","de":"german","es":"spanish","pt":"portuguese","ko":"korean","ar":"arabic"}
groups = collections.defaultdict(list)
for f in sorted(glob.glob("src/docs/extra_strings_*.toml")):
    stem = os.path.basename(f)[len("extra_strings_"):-5]
    lang = SHORT.get(stem, stem if stem in lm else None)
    if lang and lang != "english": groups[lang].append((stem,f))
en_ref = p.leaves(p.load(R/"src/docs/extra_strings.toml"))
out.write("\n=== DUAL extra_strings DIFF SAMPLES ===\n")
for l, files in sorted(groups.items()):
    if len(files) < 2: continue
    data = {s: p.leaves(p.load(R/f)) for s,f in files}
    stems = list(data)
    a,b = data[stems[0]], data[stems[1]]
    diff = [k for k in a if k in b and a[k] != b[k]]
    eng_a = sum(1 for k in diff if a[k] == en_ref.get(k)); eng_b = sum(1 for k in diff if b[k] == en_ref.get(k))
    out.write(l + " | " + stems[0] + " vs " + stems[1] + " | diff=" + str(len(diff)) + "/" + str(len(a)) + " | english_on_" + stems[0] + "=" + str(eng_a) + " english_on_" + stems[1] + "=" + str(eng_b) + "\n")
    for k in diff[:10]:
        out.write("    " + k + " | " + stems[0] + ": " + a[k][:130] + " | " + stems[1] + ": " + b[k][:130] + "\n")

# --- (3) render target proof (plain line scan) ---
out.write("\n=== render_site.py lines mentioning extra_strings_ ===\n")
rs = open("src/render_site.py", encoding="utf-8").read()
for ln in rs.split("\n"):
    if "extra_strings_" in ln: out.write("    " + ln.strip()[:200] + "\n")

# --- (4) Traditional-Chinese simplified-char census (compact unambiguous set) ---
BAD = set("装馏纤浆气与产浓两须筑属铸细运输状颗盖广处炼经划后里只发几没还来为从对开关问间东车马鸟长门风热无爱边节术叶虽归务办华毕币标别参场陈迟冲虫丑触传创辞窜达带单当导岛邓敌递点电垫钓调叠顶订动斗独断队吨顿夺鹅儿尔访纺飞坟奋丰凤肤负复赶冈刚钢纲个给巩贡沟构购谷顾刮观馆贯龟规贵滚国过汉号壶护怀坏欢环缓换回汇会浑获击机积鸡极际继纪夹检简见将奖讲胶较阶结届紧进尽劲径镜纠旧举据卷决军凯课恳垦夸块况亏扩兰拦览滥劳乐类厘离礼丽厉联连练俩脸凉辆疗临灵铃领刘龙楼卢鲁陆录吕乱论罗骆妈码骂买麦卖蛮满闷们梦弥庙灭鸣铭纳难脑闹拟宁纽农欧盘贫评凭铺朴齐骑启弃牵签钱浅枪强抢桥亲轻倾请庆穷区劝却让饶认荣软锐润伞扫纱筛删闪陕伤绍设时识实试视书树双谁顺说苏诉肃随岁孙态摊谈汤讨题条贴铁听铜统头图团托弯万网围维伟卫温闻吴误雾习系显现线项销晓协写兴许续选学寻讯压烟严盐验扬阳养样约药页业叶医仪移遗义艺忆议异译阴银饮应拥优犹邮鱼语育预园员圆缘远愿云运杂载则择泽责赠战张折这针诊阵争征证织职执质终钟众种专砖转壮准浊资综总纵组")
TRAD_FILES = ["src/docs/lang/traditional_chinese.toml","src/grf/lang/traditional_chinese.toml","src/gs/lang/traditional_chinese.toml","src/docs/extra_strings_traditional_chinese.toml"]
out.write("\n=== TRADITIONAL-CHINESE simplified-char census ===\n")
hits=collections.Counter(); details=[]
for f in TRAD_FILES:
    if not os.path.exists(f): continue
    for ln in open(f, encoding="utf-8").read().split("\n"):
        if "=" not in ln or ln.lstrip().startswith("#") or "DOC_TRANS_LANG_" in ln: continue
        bad=[c for c in ln if c in BAD]
        if bad:
            hits.update(bad); details.append((f, "".join(sorted(set(bad))), ln.strip()[:170]))
out.write("total_lines " + str(len(details)) + " chars " + json.dumps(dict(hits.most_common(50)), ensure_ascii=False) + "\n")
for d in details[:50]: out.write("  " + d[0].replace("\\","/") + " | " + d[1] + " | " + d[2] + "\n")

open("tools/_i18n_round3_followup.txt","w",encoding="utf-8").write(out.getvalue())
print("wrote", len(out.getvalue()), "chars; exact dup groups", n, "trad_lines", len(details))
