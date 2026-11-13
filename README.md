# CIRS — Community Industry Replacement Set

**English** | [简体中文](README_zh.md)

[![CI](https://github.com/Maicarons/CIRS/actions/workflows/ci.yml/badge.svg)](https://github.com/Maicarons/CIRS/actions/workflows/ci.yml)
[![Docs](https://github.com/Maicarons/CIRS/actions/workflows/pages.yml/badge.svg)](https://maicarons.github.io/CIRS/)
[![License: GPL v2](https://img.shields.io/badge/license-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/gpl-2.0.html)

CIRS is a community-maintained fork of [FIRS (Industry Replacement Set)](https://github.com/andythenorth/firs) for OpenTTD. It keeps the industries, cargos and economies that players know, while reopening the project to community support and community translations.

The upstream FIRS project no longer accepts suggestions or translation contributions. CIRS exists to change that: bug reports, balance suggestions, new graphics and translations are welcome here.

## Why CIRS?

- **Open community support** — issues and pull requests are reviewed and merged in this repository.
- **Open translations** — game text and website text are translated through plain TOML files, reviewed like code.
- **Upstream tracking** — the full FIRS git history is preserved, so future upstream changes can be merged instead of forked away.
- **Drop-in gameplay** — CIRS keeps the FIRS NewGRF ID, so existing savegames and scenarios load it as the same industry set.

> CIRS and FIRS share the same NewGRF ID. Do not enable both at the same time in one game.

## Features

- 100+ industries and 60+ cargos across multiple economies.
- Simple economies for new players and complex economies for veterans.
- Primary industries never close; secondary industry closure is optional.
- Cargo production responds to supplies and to delivering multiple accepted cargos.
- Snow-aware graphics for buildings above the snowline.
- Optional landscaping objects and a large set of parameters.

## Installation

1. Download `cirs.grf` from the [latest release](https://github.com/Maicarons/CIRS/releases).
2. Put it in your OpenTTD `newgrf` folder.
3. Enable it in the NewGRF settings window and choose an economy in the parameters.

OpenTTD 1.7.0 or newer is required.

## Building from source

Requirements:

- Python 3.11+
- NML 0.7.5+ (`nmlc`)
- Chameleon, Pillow and Markdown (see `requirements.txt`)
- Node.js 20+ (VitePress documentation site)
- GNU Make
- Graphviz (optional, only for cargo flow charts)

```bash
python -m pip install -r requirements.txt
make            # builds generated/cirs.grf and generated/gs
make grf        # only the NewGRF
make gs         # only the GameScript
make text_docs  # only the readme/license/changelog text files
make site       # generate Markdown and build the VitePress docs site
```

On Windows, run the same Python scripts directly if `make` is unavailable:

```powershell
python src/render_docs.py dummy dummy
python src/render_site.py dummy dummy
python src/render_nml.py dummy dummy
nmlc -c -l generated/lang --grf=generated/cirs.grf generated/cirs.nml
cd docs-site; npm install; npm run dev
```

## Documentation site

The website is a VitePress project in `docs-site/`. Page content is generated from the same game data as the NewGRF by `src/render_site.py`, so cargos, industries and economies never drift between the game and the docs.

```bash
make site                 # generate docs-site/src and build the static site
cd docs-site
npm run dev               # local preview at http://localhost:5173/CIRS/
```

English lives at `/`, Chinese at `/zh/`. Both locales share one template set and are translated through the TOML files below.

## Translations

CIRS ships with **39 languages** out of the box: English plus 38 community translations. All game text is fully localizable and the website is available in English and Chinese.

**Supported languages:** English · Simplified Chinese (简体中文) · Traditional Chinese (繁體中文) · Japanese (日本語) · Korean (한국어) · Arabic (العربية) · Russian (Русский) · German · French · Spanish · Spanish (Mexico) · Portuguese · Portuguese (Brazil) · Italian · Dutch · Catalan · Galician · Romanian · Polish · Czech · Slovak · Hungarian · Finnish · Swedish · Danish · Norwegian Bokmål · Afrikaans · Belarusian · Croatian · Esperanto · Estonian · Gaelic · Indonesian · Latin · Luxembourgish · Serbian · Tamil · Turkish · Welsh

- Game text: `src/grf/lang/*.toml` and `src/gs/lang/*.toml`
- Website text: `src/docs/lang/*.toml` and `src/docs/extra_strings*.toml`
- Validation: `python tools/check_translations.py`

See [TRANSLATING.md](TRANSLATING.md) for the full workflow and for the history of FIRS 3.x/4.x translations.

## Keeping up with FIRS

The repository keeps the upstream history and an `upstream` remote:

```bash
git remote add upstream https://github.com/andythenorth/firs.git
git fetch upstream --tags
git merge upstream/main
```

`tools/sync_upstream.sh` automates the fetch, merge and translation check. CIRS-specific branding is kept in separate commits so upstream merges stay small.

## Repository layout

```
src/grf/            NewGRF source (industries, cargos, economies, lang)
src/gs/             GameScript source
src/docs/           Documentation generator, templates data and website translations
docs-site/          VitePress project (config, theme, generated pages)
src/render_*.py     Build entry points
tools/              Translation checks and upstream sync helpers
.github/workflows/  CI, release and GitHub Pages deployment
```

## CI and releases

- Every push and pull request builds the NewGRF, the GameScript and the docs site, and runs translation checks.
- Release tags carry the FIRS version number, prefixed with `cirs-` (for example `cirs-5.2.0`), so it is obvious which upstream release a build corresponds to. Pushing such a tag creates a GitHub release with `cirs.grf`, the GameScript archive and the built documentation.
- The docs website is deployed to GitHub Pages.

## Credits

CIRS is based on FIRS by andythenorth, FooBar, planetmaker, Terkhen and Yexo, with help from many others over more than a decade. The Chinese translation builds on the work of the FIRS 3.x/4.x translators.

## License

GPL v2. See `license.pt` for the full license and the asset license exceptions.
