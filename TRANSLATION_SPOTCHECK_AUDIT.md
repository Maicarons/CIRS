# CIRS 模组文本翻译抽测审计（m02131 之后）

## 抽测方法
- 解析 src/grf/lang、src/gs/lang、src/docs/lang 下每个语言的 TOML，逐键与 english.toml 比对：
  - present：键存在；missing：键缺失（nmlc 回退英文）；identical：值与英文逐字节相同（游戏内显示英文）。
- 已剔除 {STRING}、(optional) 这类占位/格式串（不计为"未翻译内容"）。

## 结论：游戏文本（grf）其实翻译得相当完整
- grf 英文总键数 358；每个非英文语言"已存在"键 247；其中与英文逐字相同（含拉丁）仅 2–11 个（占 247 的 1%–4%）。
- 即：每语言游戏文本已本地化 236–245 / 247 ≈ 95%–99%。
- 完全缺失的键（回退英文）：0。
- gs 域 44 键全 present，16 键 identical（多为 {RAW_STRING}/{STRING1} 占位串，非内容）。

## 真正的"显示英文"来源：专有名词（by design）
grf 里英文/仍英文的键，绝大多数是行业名、站点名、经济模式名这类专有名词，按上游惯例保留英文：
- 经济模式：Mild Mild West、Arctic Basic、Tropic Basic、Steeltown
- 行业/站点名：Hotel、Ranch、Port、Silo、Plantation、Mines、Base、Plant、Bakery、Components、Shorefront、Slab yard、Steelmasters、Flowline、Precast、Manor、Reinder Pens …
- 出现面最广的 34 个 distinct 键（STR_TOWN/STR_STATION 占位串已剔除）：Silo 16 语言、Hotel 13、Base 8、LAND 5、Ranch 4…（full union 可见上一轮脚本输出）。
- 这些在游戏内表现为"行业名/站点名是英文"，容易被误判为没翻译。

## docs 站点的真实缺口
- docs 真实可译正文 130 键（剔除 49 个 DOC_TRANS_LANG_* 语言名），每语言仅 0–6 个仍英文（多为 DOC_CR_DEP_PYTHON = "Python 3.11+"）。
- 真正未本地化的是 49 个语言切换器名称键：36–38 个语言仍把 DOC_TRANS_LANG_ZH 等显示为英文（如简体中文页仍写 "Chinese, Simplified" 而非"简体中文"）。

## 建议下一步（等你拍板）
1. 把 grf 的 34 个专有名词键逐语言本地化（至少经济模式名 + 高频站点/行业名：Silo/Hotel/Ranch/Port/Plantation/Mines/Steeltown 等）——可明显消除游戏内英文观感。
2. 修掉 docs 的 49 个 DOC_TRANS_LANG_* 语言名（每个语言填自己语言对该语言的称呼）。
3. 其余逐字相同的占位串（{STRING}、(optional)、{RAW_STRING}）保留英文，无需处理。

要不要我先把第 1 + 2 项做掉？这两项体量可控（约 34×少量 + 49×38），做完会重编译 cirs.grf 并重新部署。
