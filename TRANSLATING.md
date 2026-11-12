# Translating CIRS / CIRS 翻译指南

[English](#english) | [简体中文](#简体中文)

## English

### A short history of FIRS translations

- **FIRS 3.x and 4.x** shipped translations as `.lng` files under `src/lang/`, generated from `src/lang_templates/english.pylng`. Translations were managed outside the repository with the #openttdcoop Web Translator, and files such as `simplified_chinese.lng` were committed back. The Chinese files from that era are still in git history and remain the reference for cargo and industry names.
- **FIRS 5.x** removed translations entirely. Only `src/grf/lang/english.toml` and `src/gs/lang/english.toml` remain.
- **CIRS** restores translations with a workflow that lives in the repository: one TOML file per language, reviewed through normal pull requests.

### Game text

| File | Purpose |
| --- | --- |
| `src/grf/lang/english.toml` | NewGRF strings (reference language) |
| `src/grf/lang/simplified_chinese.toml` | Simplified Chinese NewGRF strings |
| `src/gs/lang/english.toml` | GameScript strings (reference language) |
| `src/gs/lang/simplified_chinese.toml` | Simplified Chinese GameScript strings |

Rules:

1. Every language file must contain **exactly the same keys, in the same order**, as the English file.
2. Keep every placeholder unchanged: `{ORANGE}`, `{BLACK}`, `{}{}`, `{SIGNED_WORD}`, `{STRING}`, `{COMPANY}`, `{NUM}`, `{CARGO_LONG}`, `{TOWN}`, `{INDUSTRY}` and so on. `{}` is a line break, so the number of `{}` markers matters.
3. NewGRF language files need a `[GLOBAL_PRAGMA]` block. Simplified Chinese uses `grflangid = "0x56"` and `plural = "1"`.
4. Do not translate key names, cargo labels or NewGRF identifiers.
5. Run `python tools/check_translations.py` before opening a pull request.

### Website text

| File | Purpose |
| --- | --- |
| `src/docs/lang/english.toml` | English website strings (navigation, headings, notes) |
| `src/docs/lang/simplified_chinese.toml` | Simplified Chinese website strings |
| `src/docs/extra_strings.toml` | English docs-only descriptions and TTD industry names |
| `src/docs/extra_strings_zh.toml` | Simplified Chinese docs-only descriptions |

The website is a VitePress project in `docs-site/`. Page Markdown is generated from the game data and the TOML files above, then VitePress renders it. English is served from `/`, Chinese from `/zh/`; both locales share one page generator, so a new page only has to be added once in `src/render_site.py`. Cargo flow SVG charts are generated once in English and shared by every language.

### Adding a new language

1. Copy `src/grf/lang/english.toml` to `<language>.toml`, translate the values, and set the correct `grflangid` from the OpenTTD language table.
2. Do the same for `src/gs/lang/`.
3. Copy `src/docs/lang/english.toml` to `<language>.toml` and `src/docs/extra_strings.toml` to `extra_strings_<code>.toml`.
4. Add an entry to `SITE_LANGS` in `src/render_site.py` with a unique `code` (for example `zh`), output `dir`, and `display` key, then add the matching locale to `docs-site/.vitepress/config.mts`.
5. Run `python tools/check_translations.py` and `make site`, then open a pull request.

You do not need to translate everything perfectly in the first pull request; partial work is welcome, but the automated check requires key and placeholder parity, so use the English text as a temporary value for strings you have not translated yet.

## 简体中文

### FIRS 翻译简史

- **FIRS 3.x 与 4.x** 使用 `src/lang/` 下的 `.lng` 文件发布翻译，由 `src/lang_templates/english.pylng` 生成。翻译在仓库外通过 #openttdcoop Web Translator 协作，完成后提交 `simplified_chinese.lng` 等文件。那个时期的中文文件仍保留在 git 历史中，是货物名和产业名的重要参考。
- **FIRS 5.x** 完全移除了翻译，只保留 `src/grf/lang/english.toml` 和 `src/gs/lang/english.toml`。
- **CIRS** 恢复了翻译，并把流程放回仓库：每种语言一个 TOML 文件，通过普通 pull request 审查。

### 游戏文本

| 文件 | 用途 |
| --- | --- |
| `src/grf/lang/english.toml` | NewGRF 文本（基准语言） |
| `src/grf/lang/simplified_chinese.toml` | 简体中文 NewGRF 文本 |
| `src/gs/lang/english.toml` | GameScript 文本（基准语言） |
| `src/gs/lang/simplified_chinese.toml` | 简体中文 GameScript 文本 |

规则：

1. 每个语言文件必须与英文文件拥有**完全相同的键，且顺序一致**。
2. 原样保留所有占位符：`{ORANGE}`、`{BLACK}`、`{}{}`、`{SIGNED_WORD}`、`{STRING}`、`{COMPANY}`、`{NUM}`、`{CARGO_LONG}`、`{TOWN}`、`{INDUSTRY}` 等。`{}` 表示换行，所以 `{}` 的数量不能变。
3. NewGRF 语言文件需要 `[GLOBAL_PRAGMA]`。简体中文使用 `grflangid = "0x56"`、`plural = "1"`。
4. 不要翻译键名、货物 label 或 NewGRF 标识符。
5. 提交 pull request 前运行 `python tools/check_translations.py`。

### 网页文本

| 文件 | 用途 |
| --- | --- |
| `src/docs/lang/english.toml` | 英文网页文本（导航、标题、说明） |
| `src/docs/lang/simplified_chinese.toml` | 简体中文网页文本 |
| `src/docs/extra_strings.toml` | 英文文档专用描述与 TTD 产业名 |
| `src/docs/extra_strings_zh.toml` | 简体中文文档专用描述 |

网站是 `docs-site/` 下的 VitePress 项目。页面 Markdown 由上面的 TOML 与游戏数据生成，再交给 VitePress 渲染。英文位于 `/`，中文位于 `/zh/`；两种语言共用同一套页面生成器，因此新增页面只需在 `src/render_site.py` 中写一次。货物流向图 SVG 只生成一份英文版本，由所有语言共用。

### 新增一种语言

1. 复制 `src/grf/lang/english.toml` 为 `<language>.toml`，翻译所有值，并按 OpenTTD 语言表填写正确的 `grflangid`。
2. 对 `src/gs/lang/` 做同样处理。
3. 复制 `src/docs/lang/english.toml` 为 `<language>.toml`，复制 `src/docs/extra_strings.toml` 为 `extra_strings_<code>.toml`。
4. 在 `src/render_site.py` 的 `SITE_LANGS` 中增加一项，填写唯一的 `code`（例如 `zh`）、输出目录 `dir` 与 `display` 键，并在 `docs-site/.vitepress/config.mts` 中添加对应的 locale。
5. 运行 `python tools/check_translations.py` 和 `make site`，然后提交 pull request。

不要求第一次就翻译完美；欢迎分阶段提交。但自动校验要求键和占位符完全对齐，尚未翻译的条目可以先临时保留英文。
