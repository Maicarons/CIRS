# CIRS 全语言翻译完成情况报告

生成时间：2026-11-14 01:07 UTC+08:00

## 1. 范围与方法

- 语言范围：`src/render_site.py` `_LANG_MAP` 中的 39 种语言（含 English 作为基准），其余 38 种为翻译目标。
- 四组文本：`src/grf/lang/*.toml`（NewGRF 模组文本）、`src/gs/lang/*.toml`（GameScript 文本）、`src/docs/lang/*.toml`（网站文档文本）、`src/docs/extra_strings*.toml`（网站补充文本，含长短文件名双份变体）。
- 翻译引擎：Bilibili Index-Translate 免费 API（`Index-Translate-9B`，OpenAI 兼容 `/v1/chat/completions`），JSON 批量 12 条 / 并发 8 / 4 次重试。
- 保障：占位符多重集校验（含 `{}`）、U+FFFD / 控制字符检查、非 ASCII 占位符体检查、恢复单句重译、软问题（拉丁残留 / 未译长句 / 元信息泄漏 / 错字体系 / 同形）定向润色、独立 QA 复核。
- 校验：`tools/check_translations.py`（键集合 / 顺序 / NML 占位符 / grflangid 唯一性）。

## 2. 总体结果

- 全库可翻译字符串槽位（逐语言逐文件计）：**35401**。
- 已译为非英文文本：**31738**（89.7%）。
- 与英文完全相同但属于**合法不译**内容：货物两字母代码 3005、占位符模板 0、专有名词/品牌 216、纯标点 200。
- 与英文完全相同且属于**疑似未译的普通文本**：**242**。
- 缺键：**0**；占位符不匹配：**0**。
- 翻译工作量：38 种语言共 **19198** 条唯一 (语言, 字符串) 对，覆盖 **20277** 个 TOML 值槽位。

## 3. 逐语言明细

| 语言 | 唯一待译 | 已译槽位 | 合法同形 | 疑似未译普通文本 | 槽位总数 |
|---|---:|---:|---:|---:|---:|
| afrikaans | 610 | 777 | 118 | 11 | 906 |
| arabic | 692 | 929 | 115 | 1 | 1045 |
| belarusian | 432 | 839 | 66 | 1 | 906 |
| catalan | 597 | 792 | 100 | 14 | 906 |
| croatian | 440 | 826 | 75 | 5 | 906 |
| czech | 452 | 815 | 86 | 5 | 906 |
| danish | 613 | 783 | 107 | 16 | 906 |
| dutch | 454 | 801 | 88 | 17 | 906 |
| esperanto | 633 | 800 | 105 | 1 | 906 |
| estonian | 615 | 788 | 117 | 1 | 906 |
| finnish | 443 | 830 | 75 | 1 | 906 |
| french | 234 | 949 | 79 | 17 | 1045 |
| gaelic | 663 | 777 | 116 | 13 | 906 |
| galician | 363 | 852 | 50 | 4 | 906 |
| german | 263 | 914 | 118 | 13 | 1045 |
| hungarian | 433 | 835 | 66 | 5 | 906 |
| indonesian | 604 | 792 | 102 | 12 | 906 |
| italian | 355 | 856 | 49 | 1 | 906 |
| japanese | 643 | 795 | 109 | 2 | 906 |
| korean | 345 | 1007 | 37 | 1 | 1045 |
| latin | 560 | 803 | 97 | 6 | 906 |
| luxembourgish | 498 | 803 | 89 | 14 | 906 |
| norwegian_bokmal | 479 | 777 | 115 | 14 | 906 |
| polish | 352 | 861 | 43 | 2 | 906 |
| portuguese | 408 | 939 | 101 | 5 | 1045 |
| portuguese_BR | 605 | 799 | 102 | 5 | 906 |
| romanian | 632 | 792 | 106 | 8 | 906 |
| russian | 601 | 805 | 100 | 1 | 906 |
| serbian | 565 | 804 | 101 | 1 | 906 |
| simplified_chinese | 429 | 1037 | 8 | 0 | 1045 |
| slovak | 552 | 791 | 111 | 4 | 906 |
| spanish | 255 | 924 | 117 | 4 | 1045 |
| spanish_MX | 439 | 827 | 72 | 7 | 906 |
| swedish | 456 | 809 | 86 | 11 | 906 |
| tamil | 676 | 792 | 113 | 1 | 906 |
| traditional_chinese | 551 | 822 | 83 | 1 | 906 |
| turkish | 631 | 805 | 97 | 4 | 906 |
| welsh | 625 | 791 | 102 | 13 | 906 |

## 4. 官方校验

见 `tools/check_translations.py` 运行结果（应输出 `[TRANSLATIONS] OK`，退出码 0）。

## 5. 中文网站文案润色

`src/docs/lang/simplified_chinese.toml` 中 8 条首页/代码参考页文案改写保留（含弯引号 “ ” 与全角斜杠 ／）：

| 键 | 新文案 |
|---|---|
| `DOC_HOME_TAGLINE` | OpenTTD 版 FIRS 的社区分支，提供开放的翻译与社区支持。 |
| `DOC_HOME_WHY_1_DESC` | Issue 与 pull request 都会在本仓库中审阅并合并。 |
| `DOC_HOME_WHY_2_DESC` | 游戏文本与网站文本都以简单的 TOML 文件翻译，并像代码一样接受审阅。 |
| `DOC_HOME_WHY_3_DESC` | FIRS 完整的 git 历史被保留，未来的上游改动可以直接合并，而不必另起 fork。 |
| `DOC_CR_COMPILING_P1` | CIRS 源代码附带一个便于构建的 makefile，构建需要“Make”工具，它通常由 Linux/Unix 的 ports tree、macOS 的 Xcode 或 Windows 下的其他构建系统提供。 |
| `DOC_CR_FRAX_P1` | 在货物类别的命名上，FIRS 4 及更新版本采用 FRAX——一套更完善的货物类别标准。 |
| `DOC_CR_FRAX_P2` | FRAX 类别是让车辆支持改装的首选方式。但在某些细节场景下，作者可能会发现改用货物标签来设置车辆改装更为方便。 |
| `DOC_CR_TOWN_GROWTH_NOTE` | ** 城镇成长效果：除 TOWNGROWTH_PASSENGERS 与 TOWNGROWTH_MAIL 外，CIRS 不设置任何城镇成长效果；这正是预期行为，用于取消沙漠及雪线以上城镇对食物／水的需求。 |

## 6. 备注

- 机器翻译后经过自动 QA 与定向润色；专有名词、NML 颜色/字体标签、货物代码与模板占位符按项目惯例保留英文。
- 与英文同形的短词（如 Aluminium、Silo、Port）由审校提示确认为目标语言同形借词，故计为“合法同形”。
- `src/polar_fox/cargo_classes/cargo_classes_FIRS.toml` 中的英文描述用于生成 NML/内部数据，网站显示名走 `DOC_CC_*` 键（已随 `src/docs/lang/*.toml` 翻译），不构成第五组翻译文本。

## 7. 多轮检查与润色记录

| 轮次 | 内容与规模 |
|---|---|
| 翻译 | 通过 Bilibili Index-Translate 免费 API 完成 38 种语言共 19,198 条唯一 (语言, 字符串) 对；JSON 批量 12 条 / 并发 8 / 4 次重试，缺口由单句重译补齐。 |
| 首轮润色 | 独立 QA（占位符多重集、U+FFFD、控制字符、占位符体、错字体系、拉丁残留、元信息泄漏）；身份串/同形词审校与跨语言一致性共识；钢材术语人工校正 30 处。 |
| 第二轮润色 | 部分英文残留检测器 + 品牌回归扫描：FIRS/CIRS 误用、upstream 未译、STR_GRF_DESC 旧简介等共 98 处重译或替换。 |
| 第三轮润色 | 文字体系污染 4 处（西里尔字母、日文假名混入）修复；繁体中文简体字 14 处转换（保留「简体中文」自名）；7 组短码/长名 extra_strings 双份文件统一 400 处；货物短码对照 FIRS 4.x 人工语料修复 16 处（消除 Chemicals 与 Chlorine 短码撞码）。 |
| 第四轮润色 | 人工检查发现简体中文原有人工译文被批量机翻覆盖：从 git HEAD 恢复 465 条人工译文（含 `温和温和西部`→`温和西部`、6 条「每三分钟」误译为「三个月内」等），GameScript 文件回到人工译文基线；另将 3 条货物短码对照 FIRS 4.x 人工语料校正（食/石/身→脂/生/车）。保留 CIRS 品牌更新、8 条网站文案改写与既有润色成果；文档站改名 zh-tw→zh-hant，补齐 39 个语言区域导航栏与侧边栏，修复生产构建图片路径。 |
| 第五轮润色 | 严格复审发现 19 门语言的译文根本没有进入模组：nmlc 对非默认语言 .lng 里的 {G=}（缺 `##gender` pragma）与参数个数不符的 `{P ...}` 只打印 warning，并整门丢弃该语言。已为 11 门语言补 `##gender`（取自 FIRS 4.x 语料头）、删除 19 处错误 `{P}`；重编译后 nmlc warning 由 20 条降到 1 条，39 门语言全部写入 cirs.grf（体积 10,704,891 → 11,114,286 字节）。 |
| 第六轮润色 | 人工核查文档站代码参考页发现货物类别标签语义错误：FRAX 的 `CC_POTABLE` / `CC_NON_POTABLE` 是**食品级 / 可食用**（edible / food-grade）之分，不是「可饮用」，中文却把牲畜、煤炭、水泥、化肥标成「不能喝」。已按各语言改写这两个标签（38 个文件 77 处，中文「食品级 / 非食品级」），并把繁体中文 `DOC_CC_WEIRD`「其他」对齐为「特殊」；该组标签只出现在文档站，不进入 GRF / GameScript，故无需重编模组。 |

## 8. 复检看板（生成时实时计算）

- 文字体系污染：**0**
- 短码 / 长名双份文件差异：**0**
- 与 FIRS 4.x 人工语料分歧的货物短码：**0**
- 繁体中文残留简体字（不含自名）：**0**
- 独立 QA：node tools/_i18n_qa.mjs → 19,198 / 19,198，零硬错误。
- 官方校验：python tools/check_translations.py → [TRANSLATIONS] OK（39 种语言 × 4 组文本）。
- 缺键 **0**、占位符不匹配 **0**；render_lang.py / render_site.py 构建产物已重新生成（39 个 .lng、39 个 .txt、39 个站点目录）。
- 文档站 @siteData：39 个语言区域，全部具备导航栏与侧边栏（config.mts 中 nav=39、sidebar=39）；繁体中文路由为 zh-hant（True），旧 zh-tw / zh_tw 残留 **0**。

- 模组内置语言普查（解析 generated/cirs.grf 的 Action 4 语言 ID）：源文件声明 **39** 门，实际写入 **39** 门，缺失 **0** 门。

## 9. 文档站（供人工检查翻译）

- 开发服务器：`docs-site` 目录下 `npm run dev`（VitePress 1.6.4，绑定 `127.0.0.1:5173`，站点基础路径 `/CIRS/`）。
- 入口：根 `http://127.0.0.1:5173/CIRS/`；简体中文 `/CIRS/zh/`；繁体中文 `/CIRS/zh-hant/`；其余 36 个语言用两位代码，如 `/CIRS/af/`、`/CIRS/es-mx/`、`/CIRS/pt-br/`。
- 页面：`get-started.html / economies.html / cargos.html / industries.html / code-reference.html / changelog.html / translations.html`。
- 繁体中文标识统一为 `zh-hant`：`src/render_site.py` `_LANG_MAP`、`tools/_patch_sitelangs.py`、`docs-site/.vitepress/config.mts` 区域键 / `lang` / `link`、生成目录 `docs-site/src/zh-hant/` 与 39 份 translations.md 语言链接已全部同步，仓库内 `zh-tw` / `zh_tw` 残留为 0。
- 侧边栏：之前仅 8 个语言（root/zh/fr/de/es/pt/ko/ar）手写 `themeConfig`，VitePress 对 locale themeConfig 采用浅合并，其余 31 个语言因根配置无 sidebar 而没有侧边栏。现由 `tools/_gen_locales.py` 为 31 个短区域生成完整 `themeConfig`：导航/侧边栏标签取自各语言 `src/docs/lang/*.toml` 的 `DOC_NAV_*`（已翻译），12 条通用界面文案（Guide / On this page / Previous / …）经 Bilibili Index-Translate 免费 API 翻译，带英文回退；39/39 区域均有 nav 与 sidebar。
- 图片与生产构建：产业图片 `src` 恢复为 Vite 可解析的 `/img/industries/*.png`（`helper.asset()`），VitePress 在构建时自动补 `/CIRS/` 基路径；`npm run build` 成功，313 个 HTML、38 个语言目录各 8 页、4,864 处图片 URL 带 `/CIRS/` 前缀，273 个页面含 VPSidebar。
- 下载条目加粗修复：`src/render_site.py:286` 的下载列表模板原为 `- **%s**[%s](...)`，加粗标记与译文末尾空格/句号组合后 Markdown 解析异常（`- **…推荐）。 **[安装说明]`）。已去掉模板里的 `**`，39 个语言的 get-started 页面与生产构建 HTML 中的 `- **` 残留均为 0；翻译值未改动，仅调整渲染模板。


## 10. 模组多语言失效的根因与修复

- 现象：文档站与源文件的翻译都在，但 19 门语言（belarusian / catalan / croatian / czech / gaelic / galician / indonesian / italian / japanese / korean / latin / norwegian_bokmal / polish / russian / serbian / slovak / traditional_chinese / turkish）在游戏里完全没有译文。`nmlc` 依旧 exit 0，只留 20 条 warning。
- 根因（nml/grfstrings.py）：`parse_file(filename, default)` 捕获 `generic.ScriptError` 后，若不是默认语言，只 `print_warning` 就跳过整个文件，语言不会进入 `langs`。触发点是 `StringCommand.validate_arguments`：`{G=}` 需要 `##gender` pragma，`{P ...}` 的参数个数必须等于该语言的复数形数量（`get_num_plurals()`）。机翻把英文 `{P 0 "" s}` 这种 2 参数形式照抄进需要 1/3/4 形的语言，于是整门语言被丢。
- 修复（tools/_nml_grf_lang_fix.py，幂等）：① 从 FIRS 4.x 语料头的 `##gender` 取权威性别名，为 11 门使用 `{G=}` 的语言在 `[GLOBAL_PRAGMA]` 中补 `gender = "..."`；② 删除参数个数不符的 19 处 `{P}`（日文 `コーヒー{P 0 "" s}袋の{WEIGHT}` → `コーヒー袋の{WEIGHT}`）；③ 把改动镜像进 `tools/_i18n_out/<lang>.jsonl`，保证 `pipeline apply` 不会回退。
- 验证：`tools/_nml_probe39.py` 直接调用 nml → 39 门语言、0 warning；`tools/_grf_lang_verify.py` 对最终 cirs.grf 做每语言 80 条最长文本片段的精确字节搜索 → 39/39 全部 80/80 命中（修复前 19 门为 0–23/80）；GRF 字符串普查由 hangul/kana/cyrillic 全为 0 变为 hangul 575 / kana 359 / cyrillic 1319；Action 4 语言 ID 普查 39 个 ID 全部出现。
- 结论：源文件校验全绿不代表模组里有译文，**发布前必须普查最终 .grf**。重建命令见 `tools/_build_grf.sh`（Makefile 在 MSYS 下因 `bin/find-files` 路径引号无法直接使用）。

## 11. 发布信息

- 版本标签：**cirs-5.2.0**（构建产物内嵌 rev 计数 7543）。
- 产物：`generated/cirs.grf` 11,113,790 字节，SHA-256 `79ba8edce22818c99d7d592f01d65dd1a88215f40000e1c615b6c32d13e06599`。

## 12. 货物类别标签的语义修正

- 用户在文档站简体中文代码参考页「货物」表（编号 122 牲畜 LVST）发现类别列写着「不可饮用」，指出翻译有误。
- 权威语义（`src/polar_fox/docs/frax.html`）：`CC_POTABLE` = "Cargo that is edible / food-grade (safe for human consumption and with hygienic transport requirements)."（示例 BEANS / FISH / FLOUR / FOOD / GRAIN / MILK）；`CC_NON_POTABLE` = "Cargo that is inedible / non-food-grade (unsafe for human consumption and incompatible with hygienic transport requirements)."（示例含 LIVESTOCK / COAL / CEMENT / OIL / FERTILISER / AMMONIA）；`CC_WEIRD` = "Unique cargos that don't really fit any standard classes"。即该分类是食品级属性，而非能否饮用。`src/polar_fox/constants.py` 的 food_grade 车厢改装规则同样使用 food-grade 语义。
- 渲染链路：`src/docs/doc_helper.py` 的 `pretty_print_cargo_classes()` 按映射表取 `DOC_CC_*` 译文；`src/cargos/livestock.py` 把牲畜归入 `CC_PIECE_GOODS` / `CC_WEIRD` / `CC_NON_POTABLE`，所以「不可饮用」会被套到牲畜身上。
- 修复（`tools/_cc_foodgrade_fix.py`，幂等）：按各语言改写 `DOC_CC_POTABLE` / `DOC_CC_NON_POTABLE`（中文「食品级 / 非食品级」、繁中「食品級 / 非食品級」、日「食品級」、韩「식품 등급」、德「Lebensmitteleignung」、法「Alimentaire」、俄「Пищевой」等），英文保留 FRAX 原名 Potable / Non-Potable；繁体中文 `DOC_CC_WEIRD` 由「其他」对齐为「特殊」。
- 影响面：`DOC_CC_*` 只在 `src/docs/lang/*.toml` 中定义、只被文档站两个 code-reference 页面使用，`src/grf/lang` 与 `src/gs/lang` 无同名键 → 不进入 cirs.grf / GameScript，无需重编模组，只需重新渲染站点。
- 复验：重渲染后简体中文代码参考页牲畜行显示「件货, 特殊, 非食品级」，全站旧词「不可饮用 / 不可飲用」残留 0；`check_translations.py` → [TRANSLATIONS] OK，`tools/_i18n_qa.mjs` → 19,198 / 19,198，缺键与占位符不匹配均为 0，`npm run build` 成功。
