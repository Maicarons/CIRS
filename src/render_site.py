"""Render the CIRS documentation site (VitePress) from the game data.

The site is generated as Markdown into docs-site/src, one directory per site
language. VitePress then builds the static site from those files, so the game
data (economies, cargos, industries) stays a single source of truth shared by
the NewGRF, the GameScript and the website.
"""

import html
import os
import shutil
import subprocess

currentdir = os.curdir
from time import time

from PIL import Image

import firs
import global_constants
import utils
from docs.doc_helper import DocHelper
from grf.incompatible_grfs import incompatible_grfs
from polar_fox import git_info
from chameleon import PageTemplateLoader

docs_src = os.path.join(currentdir, "src", "docs")
site_root = os.path.join(currentdir, "docs-site")
site_source = os.path.join(site_root, "src")
site_public = os.path.join(site_source, "public")
site_images = os.path.join(site_public, "img")

# must match `base` in docs-site/.vitepress/config.mts
SITE_BASE = "/CIRS/"

# site languages; the first entry is the default (English, served from the site root)
# site languages; the first entry is the default (English, served from the site root).
# Keys are grf/gs/docs lang filenames; values give the short site `code`, the
# extra_strings TOML file, the DOC_TRANS_LANG_* key for the switcher label, and dir.
_LANG_MAP = {
    "english": ("en", "extra_strings.toml", "DOC_TRANS_LANG_EN", ""),
    "simplified_chinese": ("zh", "extra_strings_zh.toml", "DOC_TRANS_LANG_ZH", "zh"),
    "french": ("fr", "extra_strings_fr.toml", "DOC_TRANS_LANG_FR", "fr"),
    "german": ("de", "extra_strings_de.toml", "DOC_TRANS_LANG_DE", "de"),
    "spanish": ("es", "extra_strings_es.toml", "DOC_TRANS_LANG_ES", "es"),
    "portuguese": ("pt", "extra_strings_pt.toml", "DOC_TRANS_LANG_PT", "pt"),
    "korean": ("ko", "extra_strings_ko.toml", "DOC_TRANS_LANG_KO", "ko"),
    "arabic": ("ar", "extra_strings_ar.toml", "DOC_TRANS_LANG_AR", "ar"),
    "afrikaans": ("af", "extra_strings_afrikaans.toml", "DOC_TRANS_LANG_AFRIKAANS", "af"),
    "belarusian": ("be", "extra_strings_belarusian.toml", "DOC_TRANS_LANG_BELARUSIAN", "be"),
    "catalan": ("ca", "extra_strings_catalan.toml", "DOC_TRANS_LANG_CATALAN", "ca"),
    "croatian": ("hr", "extra_strings_croatian.toml", "DOC_TRANS_LANG_CROATIAN", "hr"),
    "czech": ("cs", "extra_strings_czech.toml", "DOC_TRANS_LANG_CZECH", "cs"),
    "danish": ("da", "extra_strings_danish.toml", "DOC_TRANS_LANG_DANISH", "da"),
    "dutch": ("nl", "extra_strings_dutch.toml", "DOC_TRANS_LANG_DUTCH", "nl"),
    "esperanto": ("eo", "extra_strings_esperanto.toml", "DOC_TRANS_LANG_ESPERANTO", "eo"),
    "estonian": ("et", "extra_strings_estonian.toml", "DOC_TRANS_LANG_ESTONIAN", "et"),
    "finnish": ("fi", "extra_strings_finnish.toml", "DOC_TRANS_LANG_FINNISH", "fi"),
    "gaelic": ("gd", "extra_strings_gaelic.toml", "DOC_TRANS_LANG_GAELIC", "gd"),
    "galician": ("gl", "extra_strings_galician.toml", "DOC_TRANS_LANG_GALICIAN", "gl"),
    "hungarian": ("hu", "extra_strings_hungarian.toml", "DOC_TRANS_LANG_HUNGARIAN", "hu"),
    "indonesian": ("id", "extra_strings_indonesian.toml", "DOC_TRANS_LANG_INDONESIAN", "id"),
    "italian": ("it", "extra_strings_italian.toml", "DOC_TRANS_LANG_ITALIAN", "it"),
    "japanese": ("ja", "extra_strings_japanese.toml", "DOC_TRANS_LANG_JAPANESE", "ja"),
    "latin": ("la", "extra_strings_latin.toml", "DOC_TRANS_LANG_LATIN", "la"),
    "luxembourgish": ("lb", "extra_strings_luxembourgish.toml", "DOC_TRANS_LANG_LUXEMBOURGISH", "lb"),
    "norwegian_bokmal": ("nb", "extra_strings_norwegian_bokmal.toml", "DOC_TRANS_LANG_NORWEGIAN_BOKMAL", "nb"),
    "polish": ("pl", "extra_strings_polish.toml", "DOC_TRANS_LANG_POLISH", "pl"),
    "portuguese_BR": ("pt-br", "extra_strings_portuguese_BR.toml", "DOC_TRANS_LANG_PORTUGUESE_BR", "pt-br"),
    "romanian": ("ro", "extra_strings_romanian.toml", "DOC_TRANS_LANG_ROMANIAN", "ro"),
    "russian": ("ru", "extra_strings_russian.toml", "DOC_TRANS_LANG_RUSSIAN", "ru"),
    "serbian": ("sr", "extra_strings_serbian.toml", "DOC_TRANS_LANG_SERBIAN", "sr"),
    "traditional_chinese": ("zh-hant", "extra_strings_traditional_chinese.toml", "DOC_TRANS_LANG_TRADITIONAL_CHINESE", "zh-hant"),
    "slovak": ("sk", "extra_strings_slovak.toml", "DOC_TRANS_LANG_SLOVAK", "sk"),
    "spanish_MX": ("es-mx", "extra_strings_spanish_MX.toml", "DOC_TRANS_LANG_SPANISH_MX", "es-mx"),
    "swedish": ("sv", "extra_strings_swedish.toml", "DOC_TRANS_LANG_SWEDISH", "sv"),
    "tamil": ("ta", "extra_strings_tamil.toml", "DOC_TRANS_LANG_TAMIL", "ta"),
    "turkish": ("tr", "extra_strings_turkish.toml", "DOC_TRANS_LANG_TURKISH", "tr"),
    "welsh": ("cy", "extra_strings_welsh.toml", "DOC_TRANS_LANG_WELSH", "cy"),
}

SITE_LANGS = []
for _id, (_code, _extra, _display, _dir) in _LANG_MAP.items():
    if _id == "english":
        SITE_LANGS.append({
            "id": _id, "code": _code, "dir": _dir, "prefix": SITE_BASE,
            "route_prefix": "/", "extra_strings": _extra, "display": _display,
        })
    else:
        SITE_LANGS.append({
            "id": _id, "code": _code, "dir": _dir,
            "prefix": SITE_BASE + _code + "/",
            "route_prefix": "/" + _code + "/",
            "extra_strings": _extra, "display": _display,
        })


def load_site_strings(site_lang_id):
    """Load the website-only strings (navigation, headings, notes) for one language."""
    import tomllib

    with open(os.path.join(docs_src, "lang", site_lang_id + ".toml"), "rb") as fp:
        return tomllib.load(fp)


def build_doc_helper(site_lang):
    """Combine game strings (cargo/industry/economy names) with docs-only strings."""
    import tomllib

    lang_strings = utils.get_lang_data("grf", site_lang["id"])["lang_strings"]
    with open(os.path.join(docs_src, site_lang["extra_strings"]), "rb") as fp:
        extra_strings_source = tomllib.load(fp)
    for node_name, node_value in extra_strings_source.items():
        lang_strings[node_name] = node_value["base"]
    return DocHelper(
        lang_strings=lang_strings,
        site_strings=load_site_strings(site_lang["id"]),
        site_lang_code=site_lang["code"],
        site_prefix=site_lang["prefix"],
        site_route_prefix=site_lang["route_prefix"],
        site_base=SITE_BASE,
        site_langs=SITE_LANGS,
    )


def esc(value):
    """Escape a value for use in generated HTML fragments."""
    return html.escape(str(value), quote=True)


def yaml_str(value):
    """Quote a value for use in YAML frontmatter."""
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def page_link(helper, doc_name, text, anchor=None):
    """Render a link to another generated site page (and optional anchor)."""
    url = helper.link(doc_name)
    if anchor:
        url += "#" + anchor
    return '<a href="%s">%s</a>' % (esc(url), esc(text))


def cargo_icon_span(helper, cargo):
    """Render the cargo icon as a sprite taken from the shared cargo icon sheet."""
    x = 20 + 40 * cargo.icon_indices[0]
    y = 20 + 40 * cargo.icon_indices[1]
    style = (
        "display:inline-block;width:20px;height:20px;vertical-align:-4px;"
        "margin-right:6px;background-image:url('%s');background-position:-%dpx -%dpx;"
        % (helper.asset_href("img/cargoicons.png"), x, y)
    )
    return '<span class="cirs-cargo-icon" style="%s"></span>' % style


def anchor(node_id):
    """Emit an explicit anchor so old links (#cargo-id) keep working."""
    return '<a id="%s"></a>\n' % esc(node_id)


def economy_id(helper, economy):
    """Stable, URL safe id for an economy (same as the old HTML docs)."""
    return helper.get_economy_name_char_safe(economy)


def render_home(helper):
    """Render the landing page, using the VitePress home layout."""
    t = helper.t
    features = [
        (t("DOC_GS_FEATURE_CARGOS", count=len(firs.cargo_manager)), t("DOC_GS_GAMEPLAY_B2")),
        (t("DOC_GS_FEATURE_INDUSTRIES", count=len(firs.industry_manager)), t("DOC_GS_GAMEPLAY_B1")),
        (t("DOC_GS_FEATURE_ECONOMIES", count=len(firs.economy_manager)), t("DOC_ECO_INTRO")),
    ]
    lines = [
        "---",
        "layout: home",
        "hero:",
        '  name: "CIRS"',
        "  text: %s" % yaml_str(t("DOC_SUBTITLE")),
        "  tagline: %s" % yaml_str(t("DOC_HOME_TAGLINE")),
        "  image:",
        # VitePress prepends the deployment base to the hero image itself, so this
        # must stay a route without the base (unlike object data or inline CSS)
        "    src: %s" % yaml_str(helper.asset("img/industries/integrated_steel_mill.png")),
        '    alt: "CIRS"',
        "  actions:",
        "    - theme: brand",
        "      text: %s" % yaml_str(t("DOC_GS_ANCHOR_GAMEPLAY")),
        "      link: %s" % yaml_str(helper.site_route_prefix + "get-started.html"),
        "    - theme: alt",
        '      text: "GitHub"',
        '      link: "https://github.com/Maicarons/CIRS"',
        "features:",
    ]
    for title, details in features:
        lines.append("  - title: %s" % yaml_str(title))
        lines.append("    details: %s" % yaml_str(details))
    lines.append("---")
    lines.append("")

    # headline numbers, repeated here because the hero cannot show arbitrary HTML
    stats = [
        (len(firs.cargo_manager), t("DOC_NAV_CARGOS")),
        (len(firs.industry_manager), t("DOC_NAV_INDUSTRIES")),
        (len(firs.economy_manager), t("DOC_NAV_ECONOMIES")),
    ]
    lines.append('<div class="cirs-stats">')
    for count, label in stats:
        lines.append(
            '  <div class="cirs-stat"><strong>%d</strong><span>%s</span></div>'
            % (count, esc(label))
        )
    lines.append("</div>")
    lines.append("")

    lines.append("## %s" % esc(t("DOC_HOME_WHY_TITLE")))
    lines.append('<div class="cirs-cards">')
    for index in (1, 2, 3):
        lines.append('  <div class="cirs-card">')
        lines.append("    <h3>%s</h3>" % esc(t("DOC_HOME_WHY_%d_TITLE" % index)))
        lines.append("    <p>%s</p>" % esc(t("DOC_HOME_WHY_%d_DESC" % index)))
        lines.append("  </div>")
    lines.append("</div>")
    lines.append("")

    lines.append("## %s" % esc(t("DOC_HOME_EXPLORE_TITLE")))
    explore = [
        page_link(helper, "get-started", t("DOC_GS_ANCHOR_GAMEPLAY")),
        page_link(helper, "economies", t("DOC_NAV_ECONOMIES")),
        page_link(helper, "cargos", t("DOC_NAV_CARGOS")),
        page_link(helper, "industries", t("DOC_NAV_INDUSTRIES")),
        page_link(helper, "cirs-growth", "CIRS Growth"),
        page_link(helper, "code-reference", t("DOC_NAV_CODE_REFERENCE")),
        page_link(helper, "translations", t("DOC_NAV_TRANSLATIONS")),
    ]
    lines.append(" · ".join(explore))
    lines.append("")
    return "\n".join(lines)


def render_get_started(helper):
    """Render the getting started guide: gameplay, download, setup and conflicts."""
    t = helper.t
    lines = [
        "---",
        "title: %s" % yaml_str(t("DOC_GS_GAMEPLAY_TITLE")),
        "---",
        "",
        '<ul class="cirs-checks">',
    ]
    for key in (
        "DOC_GS_FEATURE_CARGOS",
        "DOC_GS_FEATURE_INDUSTRIES",
        "DOC_GS_FEATURE_PRIMARY",
        "DOC_GS_FEATURE_SECONDARY",
        "DOC_GS_FEATURE_SNOW",
        "DOC_GS_FEATURE_PIXELS",
        "DOC_GS_FEATURE_LICENSE",
    ):
        if "{count}" in t(key):
            value = t(key, count=len(firs.cargo_manager))
        else:
            value = t(key)
        lines.append("  <li>%s</li>" % esc(value))
    lines.append("</ul>")
    lines.append("")

    # gameplay
    lines.append(anchor("gameplay"))
    lines.append("## %s" % esc(t("DOC_GS_GAMEPLAY_TITLE")))
    lines.append(t("DOC_GS_GAMEPLAY_LEAD"))
    lines.append("")
    for key in ("DOC_GS_GAMEPLAY_B1", "DOC_GS_GAMEPLAY_B2", "DOC_GS_GAMEPLAY_B3", "DOC_GS_GAMEPLAY_B4"):
        lines.append("- %s" % t(key))
    lines.append("")
    lines.append("### %s" % esc(t("DOC_GS_TIPS_TITLE")))
    for index in range(1, 6):
        lines.append("- %s" % t("DOC_GS_TIPS_%d" % index))
    lines.append("")

    # download
    lines.append(anchor("download-firs"))
    lines.append("## %s" % esc(t("DOC_GS_DOWNLOAD_TITLE")))
    lines.append(t("DOC_GS_DOWNLOAD_INTRO"))
    lines.append("")
    lines.append(
        "- %s[%s](http://wiki.openttd.org/Content_downloading)%s"
        % (
            t("DOC_GS_DOWNLOAD_B1_PREFIX"),
            t("DOC_GS_DOWNLOAD_B1_LINK"),
            t("DOC_GS_DOWNLOAD_B1_SUFFIX"),
        )
    )
    lines.append(
        "- %s%s%s"
        % (
            t("DOC_GS_DOWNLOAD_B2_PREFIX"),
            page_link(helper, "code-reference", t("DOC_GS_DOWNLOAD_B2_LINK")),
            t("DOC_GS_DOWNLOAD_B2_SUFFIX"),
        )
    )
    lines.append("")

    # vehicles
    lines.append("## %s" % esc(t("DOC_GS_VEHICLES_TITLE")))
    for key in ("DOC_GS_VEHICLES_P1", "DOC_GS_VEHICLES_P2", "DOC_GS_VEHICLES_P3"):
        lines.append(t(key))
        lines.append("")

    # setup
    lines.append(anchor("choose-economy"))
    lines.append("## %s" % esc(t("DOC_GS_SETUP_TITLE")))
    lines.append(
        "%s%s%s"
        % (
            t("DOC_GS_SETUP_INTRO_PREFIX"),
            page_link(
                helper,
                "economies",
                t("DOC_GS_SETUP_INTRO_LINK", count=len(firs.economy_manager)),
            ),
            t("DOC_GS_SETUP_INTRO_SUFFIX"),
        )
    )
    lines.append("")
    lines.append(
        "- %s[%s](https://wiki.openttd.org/NewGRF#Activating_NewGRFs)%s"
        % (
            t("DOC_GS_SETUP_B1_PREFIX"),
            t("DOC_GS_SETUP_B1_LINK"),
            t("DOC_GS_SETUP_B1_SUFFIX"),
        )
    )
    for key in ("DOC_GS_SETUP_B2", "DOC_GS_SETUP_B3", "DOC_GS_SETUP_B4"):
        lines.append("- %s" % t(key))
    lines.append("")

    # advanced
    lines.append("## %s" % esc(t("DOC_GS_ADVANCED_TITLE")))
    lines.append(t("DOC_GS_ADVANCED_P1"))
    lines.append("")
    lines.append(t("DOC_GS_ADVANCED_P2"))
    lines.append("")

    # conflicts
    lines.append("## %s" % esc(t("DOC_GS_CONFLICTS_TITLE")))
    lines.append(t("DOC_GS_CONFLICTS_P1"))
    lines.append("")
    lines.append(t("DOC_GS_CONFLICTS_P2"))
    lines.append("")
    lines.append(
        "%s%s%s"
        % (
            t("DOC_GS_CONFLICTS_P3_PREFIX"),
            page_link(helper, "code-reference", t("DOC_GS_CONFLICTS_P3_LINK"), anchor="incompatible-grfs"),
            t("DOC_GS_CONFLICTS_P3_SUFFIX"),
        )
    )
    lines.append("")
    return "\n".join(lines)


def render_economies(helper):
    """Render the economy reference, including the cargo flow graph per economy."""
    t = helper.t
    lines = [
        "---",
        "title: %s" % yaml_str(t("DOC_ECO_TITLE")),
        "---",
        "",
        t("DOC_ECO_INTRO"),
        "",
        " ".join(
            '- <a href="#%s">%s</a>'
            % (
                esc(economy_id(helper, economy)),
                esc(helper.get_economy_name(economy)),
            )
            for economy in firs.economy_manager
        ),
        "",
    ]
    for economy in firs.economy_manager:
        safe_id = economy_id(helper, economy)
        lines.append(anchor(safe_id))
        lines.append("## %s" % esc(helper.get_economy_name(economy)))
        extra_info = helper.get_economy_extra_info(economy)
        if extra_info:
            lines.append("*%s*" % extra_info.replace("\n", " "))
            lines.append("")

        lines.append("### %s" % esc(t("DOC_ECO_CARGOS", count=len(economy.cargos))))
        lines.append(
            ", ".join(
                page_link(helper, "cargos", helper.get_cargo_name(cargo), anchor=cargo.id)
                for cargo in sorted(economy.cargos, key=helper.get_cargo_name)
            )
        )
        lines.append("")

        lines.append("### %s" % esc(t("DOC_ECO_INDUSTRIES", count=len(economy.industries))))
        lines.append(
            ", ".join(
                page_link(
                    helper,
                    "industries",
                    helper.get_industry_name(industry, economy),
                    anchor=industry.id,
                )
                for industry in sorted(economy.industries, key=helper.get_industry_name)
            )
        )
        lines.append("")

        graph_svg = os.path.join(site_images, "cargoflow", safe_id + ".dot.svg")
        graph_dot = os.path.join(site_images, "cargoflow", safe_id + ".dot")
        if os.path.exists(graph_svg):
            lines.append("### %s" % esc(t("DOC_ECO_CARGO_FLOW")))
            lines.append(
                '<div class="cirs-cargoflow"><object data="%s" type="image/svg+xml"></object></div>'
                % esc(helper.asset_href("img/cargoflow/" + safe_id + ".dot.svg"))
            )
            lines.append("")
            graph_links = [
                '<a href="%s" target="_blank" rel="noopener">%s</a>'
                % (
                    esc(helper.asset_href("img/cargoflow/" + safe_id + ".dot.svg")),
                    esc(t("DOC_ECO_VIEW_LARGER")),
                )
            ]
            if os.path.exists(graph_dot):
                graph_links.append(
                    '<a href="%s" download>%s</a>'
                    % (
                        esc(helper.asset_href("img/cargoflow/" + safe_id + ".dot")),
                        esc(t("DOC_ECO_DOWNLOAD_DOT")),
                    )
                )
            lines.append('<p class="cirs-cargoflow-links">%s</p>' % " | ".join(graph_links))
            lines.append("")
    return "\n".join(lines)


def render_cargos(helper):
    """Render the cargo reference: names, descriptions and per-economy producers."""
    t = helper.t
    lines = [
        "---",
        "title: %s" % yaml_str(t("DOC_CARGO_TITLE", count=len(firs.cargo_manager))),
        "---",
        "",
        '<details class="cirs-jump"><summary>%s</summary><p>%s</p></details>'
        % (
            esc(t("DOC_CARGO_JUMP_LABEL")),
            " ".join(
                page_link(helper, "cargos", helper.get_cargo_name(cargo), anchor=cargo.id)
                for _, cargo in helper.get_registered_cargo_sorted_by_name()
            ),
        ),
        "",
    ]
    for _, cargo in helper.get_registered_cargo_sorted_by_name():
        lines.append(anchor(cargo.id))
        lines.append(
            "## %s%s" % (cargo_icon_span(helper, cargo), esc(helper.get_cargo_name(cargo)))
        )
        extra_info = helper.get_cargo_extra_info(cargo)
        if extra_info:
            lines.append(extra_info)
            lines.append("")
        if helper.cargo_is_unused_in_any_economy(cargo) and cargo.id != "mail":
            lines.append("> %s" % t("DOC_CARGO_UNUSED"))
            lines.append("")

        rows = []
        for economy in firs.economy_manager:
            if helper.cargo_is_unused(cargo, economy):
                continue
            produced_by = ", ".join(
                page_link(helper, "industries", " / ".join(helper.get_industry_all_names(industry)), anchor=industry.id)
                for industry in helper.industries_producing_cargo_for_economy(cargo, economy)
            )
            accepted_by = ", ".join(
                page_link(helper, "industries", " / ".join(helper.get_industry_all_names(industry)), anchor=industry.id)
                for industry in helper.industries_accepting_cargo_for_economy(cargo, economy)
            )
            rows.append(
                "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                % (
                    page_link(helper, "economies", helper.get_economy_name(economy), anchor=economy_id(helper, economy)),
                    produced_by or t("DOC_NOTHING"),
                    accepted_by or t("DOC_NOTHING"),
                )
            )
        lines.append('<table class="cirs-table">')
        lines.append(
            "<thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead>"
            % (
                esc(t("DOC_CARGO_TABLE_ECONOMY")),
                esc(t("DOC_CARGO_TABLE_PRODUCED_BY")),
                esc(t("DOC_CARGO_TABLE_ACCEPTED_BY")),
            )
        )
        lines.append("<tbody>%s</tbody>" % "".join(rows))
        lines.append("</table>")
        lines.append("")
    return "\n".join(lines)


def render_industries(helper):
    """Render the industry reference: names, sprites and per-economy cargos."""
    t = helper.t
    lines = [
        "---",
        "title: %s" % yaml_str(t("DOC_IND_TITLE", count=len(firs.industry_manager))),
        "---",
        "",
        '<details class="cirs-jump"><summary>%s</summary><p>%s</p></details>'
        % (
            esc(t("DOC_IND_JUMP_LABEL")),
            " ".join(
                page_link(helper, "industries", " / ".join(helper.get_industry_all_names(industry)), anchor=industry.id)
                for _, industry in helper.get_industries_sorted_by_name()
            ),
        ),
        "",
    ]
    for _, industry in helper.get_industries_sorted_by_name():
        names = " / ".join(helper.get_industry_all_names(industry))
        image_name = industry.id + ".png"
        if not os.path.exists(os.path.join(docs_src, "static", "img", "industries", image_name)):
            image_name = "not_drawn.png"
        lines.append(anchor(industry.id))
        lines.append("## %s" % esc(names))
        if len(helper.get_industry_all_names(industry)) > 1:
            lines.append("*%s*" % t("DOC_IND_NAME_VARIES"))
            lines.append("")
        extra_info = helper.get_industry_extra_info(industry)
        if extra_info:
            lines.append(extra_info)
            lines.append("")
        lines.append(
            '<img class="cirs-industry-image" src="%s" alt="%s" />'
            % (esc(helper.asset("img/industries/" + image_name)), esc(names))
        )
        lines.append("")

        rows = []
        for economy in firs.economy_manager:
            if helper.industry_is_unused(industry, economy):
                continue
            accepts = ", ".join(
                page_link(helper, "cargos", helper.get_cargo_name(cargo), anchor=cargo.id)
                for cargo in helper.cargos_accepted_by_industry(industry, economy)
            )
            produces = ", ".join(
                page_link(helper, "cargos", helper.get_cargo_name(cargo), anchor=cargo.id)
                for cargo in helper.cargos_produced_by_industry(industry, economy)
            )
            rows.append(
                "<tr><td>%s</td><td>%s</td><td>%s</td></tr>"
                % (
                    page_link(helper, "economies", helper.get_economy_name(economy), anchor=economy_id(helper, economy)),
                    accepts or t("DOC_NOTHING"),
                    produces or t("DOC_NOTHING"),
                )
            )
        lines.append('<table class="cirs-table">')
        lines.append(
            "<thead><tr><th>%s</th><th>%s</th><th>%s</th></tr></thead>"
            % (
                esc(t("DOC_IND_TABLE_ECONOMY")),
                esc(t("DOC_IND_TABLE_ACCEPTS")),
                esc(t("DOC_IND_TABLE_PRODUCES")),
            )
        )
        lines.append("<tbody>%s</tbody>" % "".join(rows))
        lines.append("</table>")
        lines.append("")
    return "\n".join(lines)


def render_code_reference(helper):
    """Render the code reference: source, compiling, cargo and industry tables."""
    t = helper.t
    lines = [
        "---",
        "title: %s" % yaml_str(t("DOC_CR_TITLE")),
        "---",
        "",
        '<p class="cirs-jump">%s | <a href="#compiling">%s</a> | <a href="#cargos">%s</a> | '
        '<a href="#industries">%s</a> | <a href="#incompatible-grfs">%s</a></p>'
        % (
            '<a href="#source">%s</a>' % esc(t("DOC_CR_NAV_SOURCE")),
            esc(t("DOC_CR_NAV_COMPILING")),
            esc(t("DOC_CR_NAV_CARGOS", count=len(firs.cargo_manager))),
            esc(t("DOC_CR_NAV_INDUSTRIES", count=len(firs.industry_manager))),
            esc(t("DOC_CR_NAV_INCOMPATIBLE", count=len(incompatible_grfs))),
        ),
        "",
        anchor("source"),
        "## %s" % esc(t("DOC_CR_SOURCE_TITLE")),
        "%s<a href=\"%s\">%s</a>%s"
        % (
            t("DOC_CR_SOURCE_P1_PREFIX"),
            esc(global_constants.metadata["repo_url"]),
            esc(t("DOC_CR_SOURCE_P1_LINK")),
            t("DOC_CR_SOURCE_P1_SUFFIX"),
        ),
        "",
        '%s<a href="http://www.gnu.org/licenses/gpl-2.0.html">%s</a>%s'
        % (
            t("DOC_CR_SOURCE_P2_PREFIX"),
            esc(t("DOC_CR_SOURCE_P2_LINK")),
            t("DOC_CR_SOURCE_P2_SUFFIX"),
        ),
        "",
        anchor("compiling"),
        "## %s" % esc(t("DOC_CR_COMPILING_TITLE")),
        t("DOC_CR_COMPILING_P1"),
        "",
        t("DOC_CR_DEPENDENCIES"),
        "",
        "- [%s](https://www.python.org/)" % t("DOC_CR_DEP_PYTHON"),
        "- [%s](https://newgrf-specs.tt-wiki.net/wiki/NML:Getting_started)" % t("DOC_CR_DEP_NML"),
        "- [%s](http://chameleon.readthedocs.org/en/latest/)" % t("DOC_CR_DEP_CHAMELEON"),
        "- [%s](https://pypi.python.org/pypi/Markdown)" % t("DOC_CR_DEP_MARKDOWN"),
        "- [%s](http://www.graphviz.org)" % t("DOC_CR_DEP_GRAPHVIZ"),
        "- [Node.js 20+](https://nodejs.org/) (VitePress documentation site)",
        "",
        anchor("cargos"),
        "## %s" % esc(t("DOC_CR_CARGOS_TITLE", count=len(firs.cargo_manager))),
        t("DOC_CR_FRAX_P1"),
        "",
        '> <a href="https://grf.farm/polar_fox/frax_latest.html">%s</a>'
        % esc(t("DOC_CR_FRAX_LINK")),
        "",
        t("DOC_CR_FRAX_P2"),
        "",
        "<small>%s</small>" % t("DOC_CR_PRICE_NOTE"),
        "",
        "<small>%s</small>" % t("DOC_CR_TOWN_GROWTH_NOTE"),
        "",
        '<table class="cirs-table">',
        "<thead><tr>",
        "<th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th>"
        % (
            esc(t("DOC_CR_TH_NAME")),
            esc(t("DOC_CR_TH_LABEL")),
            esc(t("DOC_CR_TH_ICON")),
            esc(t("DOC_CR_TH_WEIGHT")),
            esc(t("DOC_CR_TH_PRICE_FACTOR")),
            esc(t("DOC_CR_TH_CARGO_CLASSES")),
            esc(t("DOC_CR_TH_TOWN_GROWTH")),
            esc(t("DOC_CR_TH_SPRITES_DONE")),
        ),
        "</tr></thead>",
        "<tbody>",
    ]
    for _, cargo in helper.get_registered_cargo_sorted_by_name():
        lines.append(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
            % (
                page_link(helper, "cargos", helper.get_cargo_name(cargo), anchor=cargo.id),
                esc(cargo.cargo_label),
                cargo_icon_span(helper, cargo),
                esc(cargo.weight),
                esc(cargo.price_factor),
                esc(helper.pretty_print_cargo_classes(cargo)),
                esc(cargo.town_growth_effect),
                esc(cargo.sprites_complete),
            )
        )
    lines.append("</tbody>")
    lines.append("</table>")
    lines.append("")

    lines.append(anchor("industries"))
    lines.append("## %s" % esc(t("DOC_CR_INDUSTRIES_TITLE", count=len(firs.industry_manager))))
    lines.append(
        '> <a href="http://newgrf-specs.tt-wiki.net/wiki/IndustryDefaultProps">%s</a>'
        % esc(t("DOC_CR_INDUSTRY_ID_LINK"))
    )
    lines.append("")
    lines.append('<table class="cirs-table">')
    lines.append(
        "<thead><tr><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead>"
        % (
            esc(t("DOC_CR_TH_NAME")),
            esc(t("DOC_CR_TH_ID")),
            esc(t("DOC_CR_TH_MAP_COLOUR")),
            esc(t("DOC_CR_TH_STATION_NAME")),
            esc(t("DOC_CR_TH_SPRITES_DONE")),
            esc(t("DOC_CR_TH_ANIMATED_TILES")),
        )
    )
    lines.append("<tbody>")
    for _, industry in helper.get_industries_sorted_by_name():
        colour = helper.get_industry_colour(industry)
        lines.append(
            '<tr><td>%s</td><td>%s</td><td><span class="cirs-colour" style="background-color:rgb(%s)"></span></td>'
            "<td>%s</td><td>%s</td><td>%s</td></tr>"
            % (
                page_link(
                    helper,
                    "industries",
                    " / ".join(helper.get_industry_all_names(industry)),
                    anchor=industry.id,
                ),
                esc(global_constants.industry_numeric_ids[industry.id]),
                esc(",".join(str(i) for i in colour)),
                esc(helper.get_nearby_station_name(industry)),
                esc(industry.sprites_complete),
                esc(industry.animated_tiles_fixed),
            )
        )
    lines.append("</tbody>")
    lines.append("</table>")
    lines.append("")

    lines.append(anchor("incompatible-grfs"))
    lines.append("## %s" % esc(t("DOC_CR_INCOMPATIBLE_TITLE", count=len(incompatible_grfs))))
    lines.append('<table class="cirs-table">')
    lines.append(
        "<thead><tr><th>%s</th><th>%s</th></tr></thead>"
        % (esc(t("DOC_CR_TH_NAME")), esc(t("DOC_CR_TH_GRFID")))
    )
    lines.append("<tbody>")
    for incompatible_grf in incompatible_grfs:
        lines.append(
            "<tr><td>%s</td><td>%s</td></tr>"
            % (esc(incompatible_grf.grfname), esc(incompatible_grf.grfid))
        )
    lines.append("</tbody>")
    lines.append("</table>")
    lines.append("")
    return "\n".join(lines)


def render_translations(helper):
    """Render the translation guide: supported languages and contribution steps."""
    t = helper.t
    lines = [
        "---",
        "title: %s" % yaml_str(t("DOC_TRANS_TITLE")),
        "---",
        "",
        t("DOC_TRANS_INTRO"),
        "",
        "## %s" % esc(t("DOC_TRANS_CURRENT")),
        "",
        " · ".join(
            '<a href="%s">%s</a>' % (esc(url), esc(label))
            for label, url in helper.get_language_links()
        ),
        "",
        "## %s" % esc(t("DOC_TRANS_HOW")),
        "",
        t("DOC_TRANS_HOW_P1"),
        "",
        t("DOC_TRANS_HOW_P2"),
        "",
        t("DOC_TRANS_HOW_P3"),
        "",
        "## %s" % esc(t("DOC_TRANS_HISTORY")),
        "",
        t("DOC_TRANS_HISTORY_P1"),
        "",
        t("DOC_TRANS_THANKS"),
        "",
    ]
    return "\n".join(lines)


def render_changelog(helper, changelog_source):
    """Render the changelog page (content is maintained in English only)."""
    t = helper.t
    lines = ["---", "title: %s" % yaml_str(t("DOC_NAV_CHANGELOG")), "---", ""]
    if helper.site_lang_code != "en":
        lines.append("> %s" % t("DOC_CHANGELOG_EN_ONLY"))
        lines.append("")
    lines.append(changelog_source)
    lines.append("")
    return "\n".join(lines)


def render_cirs_growth(helper):
    """Render the CIRS Growth companion Game Script page.

    Content is authored in src/docs/cirs_growth/{en,zh}.md. English is the
    reference text; Simplified Chinese has a full translation. Other site
    languages show the English text with a short pointer, like the changelog.
    """
    lang_code = helper.site_lang_code
    source_name = "zh.md" if lang_code == "zh" else "en.md"
    source_path = os.path.join(docs_src, "cirs_growth", source_name)
    with open(source_path, "r", encoding="utf-8") as fp:
        body = fp.read().strip()
    # source files carry an H1; generated pages take the title from frontmatter
    body_lines = body.split("\n")
    if body_lines and body_lines[0].startswith("# "):
        body_lines = body_lines[1:]
        if body_lines and not body_lines[0].strip():
            body_lines = body_lines[1:]
    body = "\n".join(body_lines).strip()
    lines = ["---", "title: %s" % yaml_str("CIRS Growth"), "---", ""]
    # relative Markdown links resolve against the generated .md tree; unlike
    # root-absolute links they are not affected by the /CIRS/ deployment base
    if lang_code == "zh":
        lines.append("> 本页提供简体中文与英文两个版本：[阅读英文版](../cirs-growth.html)。")
        lines.append("")
    elif lang_code != "en":
        lines.append("> This page is maintained in English and Simplified Chinese: [English](../cirs-growth.html) · [简体中文](../zh/cirs-growth.html).")
        lines.append("")
    lines.append(body)
    lines.append("")
    return "\n".join(lines)


def write_page(site_lang, page_name, content):
    """Write one generated Markdown page into the VitePress source tree."""
    if site_lang["dir"]:
        dst_dir = os.path.join(site_source, site_lang["dir"])
    else:
        dst_dir = site_source
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    with open(
        os.path.join(dst_dir, page_name + ".md"), "w", encoding="utf-8", newline=""
    ) as fp:
        fp.write(content)


def copy_static_assets():
    """Copy sprites used by the site into the VitePress public directory."""
    industries_src = os.path.join(docs_src, "static", "img", "industries")
    industries_dst = os.path.join(site_images, "industries")
    if os.path.exists(industries_dst):
        shutil.rmtree(industries_dst)
    shutil.copytree(industries_src, industries_dst)

    # upscale the cargo icon sheet so the icons are legible on the website
    cargo_icons_src = os.path.join(currentdir, "src", "graphics", "cargoicons.png")
    cargo_icons = Image.open(cargo_icons_src)
    cargo_icons = cargo_icons.resize(
        (2 * cargo_icons.size[0], 2 * cargo_icons.size[1]),
        resample=Image.Resampling.NEAREST,
    )
    cargo_icons.save(
        os.path.join(site_images, "cargoicons.png"), optimize=True, transparency=0
    )


def render_cargoflow(helper):
    """Render the cargo flow graphs as SVG (requires graphviz, skipped if missing)."""
    templates = PageTemplateLoader(os.path.join(docs_src, "templates"), format="text")
    # graphviz loads IMG files from disk and copies the path verbatim into the SVG,
    # so the template uses "../industries/<id>.png": it resolves both on disk and
    # in the browser, because the SVG is published next to the images in img/
    dotall = templates["cargoflow.pt"](firs=firs, doc_helper=helper)

    graph_dir = os.path.abspath(os.path.join(site_images, "cargoflow"))
    if not os.path.exists(graph_dir):
        os.makedirs(graph_dir)
    dotall_path = os.path.join(graph_dir, "cargoflow.dotall")
    with open(dotall_path, "w", encoding="utf-8", newline="") as fp:
        fp.write(dotall)

    gvpr = shutil.which("gvpr")
    dot = shutil.which("dot")
    if gvpr is None or dot is None:
        print("[RENDER SITE] graphviz not found, skipping cargo flow graphs")
        return

    graph_dir_slashes = graph_dir.replace("\\", "/")
    split_expression = (
        'BEG_G { fname = sprintf("%s/%%s.dot", $G.name); writeG($G, fname) }'
        % graph_dir_slashes
    )
    subprocess.run([gvpr, split_expression, dotall_path], check=True)

    for economy in firs.economy_manager:
        safe_id = economy_id(helper, economy)
        dot_path = os.path.join(graph_dir, safe_id + ".dot")
        if os.path.exists(dot_path):
            # run from the graph directory so "../industries/<id>.png" resolves on disk
            subprocess.run([dot, "-Tsvg", "-O", dot_path], check=True, cwd=graph_dir)


def main():
    start = time()
    print("[RENDER SITE]")

    firs.main()

    # start from a clean generated tree so removed pages do not linger
    if os.path.exists(site_source):
        shutil.rmtree(site_source)
    os.makedirs(site_images)

    doc_helpers = {}
    for site_lang in SITE_LANGS:
        doc_helpers[site_lang["id"]] = build_doc_helper(site_lang)
    # English is the reference language for shared artefacts (graphs, changelog)
    default_helper = doc_helpers[SITE_LANGS[0]["id"]]

    copy_static_assets()
    render_cargoflow(default_helper)

    with open(os.path.join(currentdir, "changelog.md"), "r", encoding="utf-8") as fp:
        changelog_source = fp.read().strip()

    for site_lang in SITE_LANGS:
        helper = doc_helpers[site_lang["id"]]
        write_page(site_lang, "index", render_home(helper))
        write_page(site_lang, "get-started", render_get_started(helper))
        write_page(site_lang, "economies", render_economies(helper))
        write_page(site_lang, "cargos", render_cargos(helper))
        write_page(site_lang, "industries", render_industries(helper))
        write_page(site_lang, "cirs-growth", render_cirs_growth(helper))
        write_page(site_lang, "code-reference", render_code_reference(helper))
        write_page(site_lang, "translations", render_translations(helper))
        write_page(site_lang, "changelog", render_changelog(helper, changelog_source))

    print(
        "[RENDER SITE]",
        "- complete",
        format((time() - start), ".2f") + "s",
    )


if __name__ == "__main__":
    main()
