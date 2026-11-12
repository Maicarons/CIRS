# CIRS — 社区产业替换集（Community Industry Replacement Set）

[English](README.md) | **简体中文**

[![CI](https://github.com/Maicarons/CIRS/actions/workflows/ci.yml/badge.svg)](https://github.com/Maicarons/CIRS/actions/workflows/ci.yml)
[![文档](https://github.com/Maicarons/CIRS/actions/workflows/pages.yml/badge.svg)](https://maicarons.github.io/CIRS/)
[![许可证: GPL v2](https://img.shields.io/badge/license-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/gpl-2.0.html)

CIRS 是 OpenTTD 产业 NewGRF [FIRS（Industry Replacement Set）](https://github.com/andythenorth/firs) 的社区维护分支。它保留了玩家熟悉的产业、货物与经济模式，同时重新开放社区支持和社区翻译。

上游 FIRS 项目已不再接受建议和翻译贡献。CIRS 的目标就是改变这一点：问题反馈、平衡建议、新图形和翻译都欢迎提交到本仓库。

## 为什么选择 CIRS？

- **开放的社区支持** —— 本仓库会审查并合并 issue 与 pull request。
- **开放的翻译** —— 游戏文本和网页文本都通过纯 TOML 文件翻译，像代码一样审查。
- **跟踪上游** —— 完整保留 FIRS 的 git 历史，未来上游更新可以直接合并，而不是彻底分叉。
- **可直接替换** —— CIRS 保留 FIRS 的 NewGRF ID，已有存档和场景会把它识别为同一套产业。

> CIRS 与 FIRS 使用相同的 NewGRF ID，请不要在同一局游戏中同时启用两者。

## 特性

- 多种经济模式下共 100 多个产业、60 多种货物。
- 为新手准备的简单经济模式，以及为老玩家准备的复杂经济模式。
- 初级产业永不关闭；二级产业是否关闭可选。
- 货物产量会响应供应品，也会响应多种收货货物的持续运输。
- 雪线以上建筑拥有雪景图形。
- 可选的景观对象和大量参数。

## 安装

1. 从 [最新发布](https://github.com/Maicarons/CIRS/releases) 下载 `cirs.grf`。
2. 把它放进 OpenTTD 的 `newgrf` 目录。
3. 在 NewGRF 设置窗口中启用，并在参数中选择经济模式。

需要 OpenTTD 1.7.0 或更新版本。

## 从源码构建

依赖：

- Python 3.11+
- NML 0.7.5+（`nmlc`）
- Chameleon、Pillow、Markdown（见 `requirements.txt`）
- Node.js 20+（VitePress 文档站）
- GNU Make
- Graphviz（可选，仅用于生成网页中的货物流向图）

```bash
python -m pip install -r requirements.txt
make            # 构建 generated/cirs.grf 和 generated/gs
make grf        # 只构建 NewGRF
make gs         # 只构建 GameScript
make text_docs  # 只生成 readme/license/changelog 文本
make site       # 生成 Markdown 并构建 VitePress 文档站
```

Windows 上没有 `make` 时，可以直接运行 Python 脚本：

```powershell
python src/render_docs.py dummy dummy
python src/render_site.py dummy dummy
python src/render_nml.py dummy dummy
nmlc -c -l generated/lang --grf=generated/cirs.grf generated/cirs.nml
cd docs-site; npm install; npm run dev
```

## 文档站

网站是 `docs-site/` 下的 VitePress 项目。页面内容由 `src/render_site.py` 从与 NewGRF 相同的游戏数据生成，因此货物、产业、经济模式不会与游戏内脱节。

```bash
make site                 # 生成 docs-site/src 并构建静态站点
cd docs-site
npm run dev               # 本地预览 http://localhost:5173/CIRS/
```

英文站点位于 `/`，简体中文位于 `/zh/`。两种语言共用一套模板，通过下文的 TOML 文件翻译。

## 翻译

CIRS 首发即支持英文和简体中文。

- 游戏文本：`src/grf/lang/*.toml` 与 `src/gs/lang/*.toml`
- 网页文本：`src/docs/lang/*.toml` 与 `src/docs/extra_strings*.toml`
- 校验：`python tools/check_translations.py`

完整流程以及 FIRS 3.x/4.x 时期的翻译历史见 [TRANSLATING.md](TRANSLATING.md)。

## 跟踪 FIRS 上游

仓库保留了上游历史，并配置了 `upstream` 远程：

```bash
git remote add upstream https://github.com/andythenorth/firs.git
git fetch upstream --tags
git merge upstream/main
```

`tools/sync_upstream.sh` 会自动完成拉取、合并和翻译校验。CIRS 的品牌化改动会放在独立提交中，方便上游合并。

## 仓库结构

```
src/grf/            NewGRF 源码（产业、货物、经济模式、语言）
src/gs/             GameScript 源码
src/docs/           文档生成器、数据与网页翻译
docs-site/          VitePress 项目（配置、主题、生成的页面）
src/render_*.py     构建入口
tools/              翻译校验与上游同步工具
.github/workflows/  CI、发布与 GitHub Pages 部署
```

## CI 与发布

- 每次 push 和 pull request 都会构建 NewGRF、GameScript 和文档站，并运行翻译校验。
- 发布标签与 FIRS 的版本号一致，只加 `cirs-` 前缀（例如 `cirs-5.2.0`），便于看出对应哪个上游版本。推送这类标签会创建 GitHub Release，附带 `cirs.grf`、GameScript 压缩包和构建好的文档站。
- 文档网站部署到 GitHub Pages。

## 致谢

CIRS 基于 andythenorth、FooBar、planetmaker、Terkhen、Yexo 以及十多年来众多贡献者共同完成的 FIRS。中文翻译建立在 FIRS 3.x/4.x 译者工作的基础之上。

## 许可证

GPL v2。完整许可证与素材例外说明见 `license.pt`。
