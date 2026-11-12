"""Render the plain text documents shipped with the NewGRF and GameScript.

The HTML documentation has moved to the VitePress site (see src/render_site.py);
this module only produces the readme, license and changelog text files that are
bundled in release archives and installed alongside the grf.
"""

import os
import shutil
import sys

currentdir = os.curdir
from time import time

import firs
import utils
from polar_fox import git_info
from chameleon import PageTemplateLoader

docs_src = os.path.join(currentdir, "src", "docs")
docs_output_path = os.path.join(currentdir, "docs")

docs_templates = PageTemplateLoader(os.path.join(docs_src, "templates"), format="text")
root_templates = PageTemplateLoader(currentdir, format="text")


def write_doc(doc_name, content):
    """Write one text document into the docs output directory."""
    with open(
        os.path.join(docs_output_path, doc_name + ".txt"),
        "w",
        encoding="utf-8",
        newline="",
    ) as fp:
        fp.write(content)


def main():
    start = time()
    print("[RENDER DOCS]")

    firs.main()

    if os.path.exists(docs_output_path):
        shutil.rmtree(docs_output_path)
    os.mkdir(docs_output_path)

    # readme is shared by the grf and the game script, and is translated as part of the site
    write_doc("readme", docs_templates["readme.pt"](git_info=git_info, utils=utils))
    write_doc("license", root_templates["license.pt"](git_info=git_info))

    with open(
        os.path.join(currentdir, "changelog.md"), "r", encoding="utf-8"
    ) as fp:
        changelog_source = fp.read()
    write_doc("changelog", changelog_source)

    print("[RENDER DOCS]", "- complete", format((time() - start), ".2f") + "s")


if __name__ == "__main__":
    main()
