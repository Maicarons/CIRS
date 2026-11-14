# CIRS Growth

CIRS Growth is a companion [OpenTTD](https://www.openttd.org/) Game Script that makes town growth depend on varied cargo deliveries and sustained passenger and mail transport. It is an adaptation of Firrel's [Renewed Village Growth](https://github.com/F1rrel/RenewedVillageGrowth), extended to support **all six economies** of the [CIRS](https://github.com/Maicarons/CIRS) industry NewGRF set.

> CIRS Growth is a **separate download** from the CIRS NewGRF. It is a Game Script (GS), enabled from *Game Script settings* in OpenTTD, not a NewGRF.

## Why a dedicated adaptation is needed

The original RVG discovers the active industry set by comparing the in-game cargo-label list against a set of hard-coded, position-sensitive arrays (`DiscoverEconomyType()` / `CompareCargoLists()` in `cargo.nut`). CIRS ships its own cargo lists for each economy, so none of the original arrays match. RVG then falls back to `::Economy = NONE` and `CreateDefaultCargoCat()`, which assumes passengers and mail occupy cargo slots 0 and 2. In CIRS those slots differ in every economy (13/11, 11/9, 16/13, 22/17, 28/24 and 41/34 for PASS/MAIL), so town growth and the passenger/mail limiter are driven by the wrong cargos.

CIRS Growth fixes this by:

- Adding exact cargo-label arrays for the six CIRS economies, so economy detection succeeds.
- Looking up passenger and mail slots by cargo label (`GetPassengerMailSlots()`), so the limiter works regardless of slot order or randomization mode.
- Providing hand-tuned cargo categories for each CIRS economy (5 categories by default, with an optional 6th for Steeltown).

## Supported CIRS economies

| Economy | Cargos | PASS / MAIL slots |
| --- | ---: | ---: |
| Temperate Basic | 17 | 13 / 11 |
| Arctic Basic | 19 | 11 / 9 |
| Tropic Basic | 18 | 16 / 13 |
| In A Hot Country | 28 | 22 / 17 |
| Steeltown | 62 | 28 / 24 |
| Mild Mild West | 66 | 41 / 34 |

CIRS Growth also keeps the original RVG support for Baseset, FIRS, ECS, YETI, NAIS and many other industry sets; unsupported sets fall back to procedurally generated categories.

## How it works

- Each monitored town receives **monthly requirements in 3-6 cargo categories**. Delivering any cargo in a category counts toward it; surplus is stockpiled (up to 10x the monthly requirement).
- Categories **unlock as the town grows** (population thresholds such as 500, 1500, 4000, 8000). Passengers and mail are required at every size.
- Only towns that **exchange passengers** are monitored; a town is dropped after six months without passenger deliveries.
- Growth rate is an exponential function of the supplied fraction, smoothed with an 8-month moving average, and is stopped when the required passenger/mail percentage is not met.
- A **Contributor** is chosen each month by summed category contribution and earns growth points; town signs, town windows (Largest population / Contributor / Limiter / Categories), five town-info modes, a StoryBook and the Goals window expose the details in game.

## Requirements

- OpenTTD **14.x or newer**.
- GS libraries from BaNaNaS / *Online Content*: **SuperLib v40**, **ToyLib v2**, **Script Communication for GS v45**.
- Any industry NewGRF; CIRS (all six economies), Baseset (all climates), FIRS 1.4/2/3/4.3/5, ECS 1.2, YETI 0.1.6, NAIS 1.0.6, ITI 1.6/2.14, XIS 0.6, AXIS 2.2, OTIS 05, IOTC 0.1, LJI 0.1, WRBI 1200, Real Beta, Minimalist and PIRS 2022 are specifically supported.

## Installation

1. Download `CIRS_Growth-13.0.tar` from the [repository](https://github.com/Maicarons/CIRS-Growth), or subscribe to it through *Online Content* (BaNaNaS).
2. Install the three GS libraries listed above.
3. In OpenTTD, start a new game and enable **CIRS Growth** in the Game Script settings, then configure its settings before starting.
4. Enable the **CIRS** NewGRF (do not enable FIRS at the same time - the two share a NewGRF ID).

## Settings

CIRS Growth exposes a wide range of Game Script settings, including town-info display mode, difficulty / goal scaling, growth-rate text under town names, *Eternal love*, **cargo randomization** (type, nearby probability, show cargos from start), an optional **6th cargo category** for supported economies (Steeltown), per-category minimum population, town growth factor, supply impact, exponentiality, lowest growth rate, subsidy behaviour, industry density and log level. The in-game StoryBook documents every category used under the current settings.

### Settings menu translations

OpenTTD reads Game Script setting descriptions and drop-down labels as **plain strings when it scans the script**, before any language is loaded. A running game therefore cannot translate them, and a single `.tar` cannot switch the settings menu language at runtime. CIRS Growth solves this at **build time**: all 25 descriptions and 37 label values live as `STR_SETTINGS_*` keys in `lang/*.txt`, and `tools/gen_settings.py` turns one language file into `settings_text.nut`, which `info.nut` loads with `require()`.

`python make_tar.py --lang <language>` builds a `.tar` whose settings menu is in that language; `--all-langs` builds all 12. The default `CIRS_Growth-13.0.tar` uses English, and localized builds are named `CIRS_Growth-13.0-<language>.tar` (for example `CIRS_Growth-13.0-simplified_chinese.tar`). Pick the build matching your OpenTTD language; the same 12 languages as the in-game translations are available.

Every `.tar` still ships all 12 language files, so the in-game StoryBook, town signs, town windows and other `GSText` strings follow the game's language as usual. The settings menu is the only part that is fixed when the archive is built.

## Version, translations and license

- Version **13.0** (2026-11-14), Game Script API 14, up to 2000 towns.
- 12 in-game translations: English, French, Slovak, Czech, Simplified Chinese, Polish, Galician, German, Japanese, Traditional Chinese, Russian, Ukrainian.
- GPL-2.0. Original author **Firrel**; CIRS adaptation **Maicarons**; the original RVG also combines keoz's *Renewed City Growth GS* and Sylf's *City Growth Limiter GS*.

> **Save compatibility:** 13.0 raises `SELF_MINLOADVERSION` to 130, so savegames started with RVG 12.1 or older will not load this version. Start a new game.

## Links

- [CIRS Growth repository](https://github.com/Maicarons/CIRS-Growth)
- [Upstream: Renewed Village Growth](https://github.com/F1rrel/RenewedVillageGrowth)
- [CIRS NewGRF](https://github.com/Maicarons/CIRS) - [CIRS documentation](https://maicarons.github.io/CIRS/)
