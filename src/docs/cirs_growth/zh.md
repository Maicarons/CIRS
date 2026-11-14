# CIRS Growth

CIRS Growth 是 [OpenTTD](https://www.openttd.org/) 的配套游戏脚本（Game Script），让城镇增长取决于多样化的货物运输以及持续稳定的乘客与邮件运输。它改编自 Firrel 的 [Renewed Village Growth](https://github.com/F1rrel/RenewedVillageGrowth)，并专门扩展以支持 [CIRS](https://github.com/Maicarons/CIRS) 产业 NewGRF 的**全部六种经济模式**。

> CIRS Growth 与 CIRS NewGRF 是**两个独立的下载项**。它是游戏脚本（GS），需在 OpenTTD 的「游戏脚本设置」中启用，而不是 NewGRF。

## 为什么需要专门适配

原版 RVG 通过把游戏内的货物标签列表与一组硬编码、与位置严格对应的数组逐一比对来识别当前产业集（`cargo.nut` 中的 `DiscoverEconomyType()` / `CompareCargoLists()`）。CIRS 为每种经济模式提供了自己的货物列表，因此原版数组无一匹配；RVG 会退回 `::Economy = NONE` 与 `CreateDefaultCargoCat()`，并假定乘客与邮件固定在 0、2 号货物槽。而 CIRS 六种经济中这两个槽位各不相同（PASS/MAIL 分别为 13/11、11/9、16/13、22/17、28/24、41/34），导致增长判定与乘客/邮件限制器作用在错误的货物上。

CIRS Growth 的修复：

- 为六种 CIRS 经济加入精确的货物标签数组，使经济识别成功。
- 通过货物标签查找乘客与邮件槽位（`GetPassengerMailSlots()`），无论槽位顺序或随机化模式如何，限制器都能正确工作。
- 为每种 CIRS 经济提供手工调优的货物分类（默认 5 类，Steeltown 可开启第 6 类）。

## 支持的 CIRS 经济模式

| 经济模式 | 货物数 | 乘客 / 邮件槽位 |
| --- | ---: | ---: |
| Temperate Basic（温带基础） | 17 | 13 / 11 |
| Arctic Basic（寒带基础） | 19 | 11 / 9 |
| Tropic Basic（热带基础） | 18 | 16 / 13 |
| In A Hot Country（炎热国度） | 28 | 22 / 17 |
| Steeltown（钢城） | 62 | 28 / 24 |
| Mild Mild West（温和西部） | 66 | 41 / 34 |

CIRS Growth 同时保留原版 RVG 对 Baseset、FIRS、ECS、YETI、NAIS 等众多产业集的支持；未专门支持的产业集会回退到程序自动生成的分类。

## 运作方式

- 每个被监控的城镇每月会收到 **3-6 个货物分类的需求**；交付该分类中任意一种货物都计入完成量，多余部分可囤积（最多为月需求的 10 倍）。
- 分类随城镇人口**逐步解锁**（如 500、1500、4000、8000）；乘客与邮件在任何规模下都必需。
- 只有**发生乘客运输**的城镇才被监控；连续六个月没有乘客运输的城镇会被移出列表。
- 增长率是已供给比例的指数函数，经 8 个月移动平均平滑；若乘客/邮件运输比例未达标，增长会停止。
- 每月按各类贡献总和选出 **Contributor（贡献者）** 并获得增长点数；城镇标牌、城镇窗口（最大人口 / 贡献者 / 限制因素 / 分类）、五种城镇信息模式、StoryBook 与 Goals 窗口会在游戏内展示这些细节。

## 运行要求

- OpenTTD **14.x 或更新版本**。
- 来自 BaNaNaS /「在线内容」的 GS 库：**SuperLib v40**、**ToyLib v2**、**Script Communication for GS v45**。
- 任意产业 NewGRF；其中 CIRS（六种经济）、Baseset（全部气候）、FIRS 1.4/2/3/4.3/5、ECS 1.2、YETI 0.1.6、NAIS 1.0.6、ITI 1.6/2.14、XIS 0.6、AXIS 2.2、OTIS 05、IOTC 0.1、LJI 0.1、WRBI 1200、Real Beta、Minimalist、PIRS 2022 为专门支持。

## 安装

1. 从 [仓库](https://github.com/Maicarons/CIRS-Growth) 下载 `CIRS_Growth-13.0.tar`，或通过「在线内容」（BaNaNaS）订阅。
2. 安装上述三个 GS 库。
3. 在 OpenTTD 中新建游戏，于「游戏脚本设置」启用 **CIRS Growth**，开始游戏前按需调整其设置。
4. 启用 **CIRS** NewGRF（不要同时启用 FIRS，两者共用同一 NewGRF ID）。

## 设置

CIRS Growth 提供大量游戏脚本设置，涵盖城镇信息显示模式、难度 / 目标缩放、城镇名下的增长率文字、*Eternal love*、**货物随机化**（类型、就近概率、开局即显示城镇货物）、为支持的经济开启可选的**第 6 个货物分类**（Steeltown）、各类最低人口、城镇增长系数、供给影响、指数系数、最低增长率、补贴行为、产业密度与日志级别等。游戏内 StoryBook 会列出当前设置下使用的全部分类。

### 设置菜单翻译

OpenTTD 在**扫描游戏脚本时**就把设置说明与下拉选项当作纯文本读取，此时尚未加载任何语言。因此运行中的游戏无法翻译它们，单个 `.tar` 也无法在运行时切换设置菜单的语言。CIRS Growth 在**构建阶段**解决：25 条说明与 37 个选项文本以 `STR_SETTINGS_*` 键保存在 `lang/*.txt` 中，`tools/gen_settings.py` 将指定语言文件转换为 `settings_text.nut`，由 `info.nut` 用 `require()` 加载。

`python make_tar.py --lang <语言>` 会生成设置菜单为该语言的 `.tar`，`--all-langs` 则一次生成全部 12 种。默认 `CIRS_Growth-13.0.tar` 为英文；本地化包命名为 `CIRS_Growth-13.0-<语言>.tar`（例如 `CIRS_Growth-13.0-simplified_chinese.tar`）。请选择与你的 OpenTTD 语言一致的构建；可用语言与游戏内翻译的 12 种相同。

BaNaNaS /「在线内容」发布的是英文默认包，因为一个包只能固定一种设置菜单语言。本地化包附在 [GitHub Releases](https://github.com/Maicarons/CIRS-Growth/releases) 上，需手动安装：把选定的 `.tar` 放进 OpenTTD 的 `game/` 文件夹，并只保留一个 `CIRS_Growth-13.0*.tar`——脚本名和版本相同的包会冲突，只有第一个会被加载。

每个 `.tar` 仍包含全部 12 个语言文件，因此游戏内 StoryBook、城镇标牌、城镇窗口等 `GSText` 文本照常跟随游戏语言。只有设置菜单的语言在打包时固定。

`settings_text.nut` 生成时带有 UTF-8 BOM。OpenTTD 的 Squirrel 加载器只对以 BOM 开头的 `.nut` 文件启用 UTF-8 词法分析；缺少 BOM 时非 ASCII 文本会被逐字节读取，显示为乱码。`lang/*.txt` 保持无 BOM，因为游戏用普通文本读取器而非 Squirrel 解析它们。

## 版本、翻译与许可

- 版本 **13.0**（2026-11-14），Game Script API 14，最多支持 2000 个城镇。
- 12 种游戏内翻译：英语、法语、斯洛伐克语、捷克语、简体中文、波兰语、加利西亚语、德语、日语、繁体中文、俄语、乌克兰语。
- GPL-2.0。原作者 **Firrel**，CIRS 适配 **Maicarons**；原版 RVG 本身还融合了 keoz 的 *Renewed City Growth GS* 与 Sylf 的 *City Growth Limiter GS*。

> **存档兼容性：** 13.0 将 `SELF_MINLOADVERSION` 提升到 130，因此用 RVG 12.1 或更早版本创建的存档无法由本版本加载，请新建游戏。

## 相关链接

- [CIRS Growth 仓库](https://github.com/Maicarons/CIRS-Growth)
- [上游：Renewed Village Growth](https://github.com/F1rrel/RenewedVillageGrowth)
- [CIRS NewGRF](https://github.com/Maicarons/CIRS) - [CIRS 文档站](https://maicarons.github.io/CIRS/)
