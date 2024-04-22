import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath("../pure_utils"))

autodoc_mock_imports = ["pure_utils"]

DOCS_ROOT_DIR = Path(__file__).resolve(strict=True).parent

project = html_title = "pure-utils"
copyright = "Peter Bro <p3t3rbr0@gmail.com || peter@peterbro.su>"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
]

templates_path = [str(DOCS_ROOT_DIR / "templates")]

html_theme = "furo"

pygments_dark_style = "monokai"

master_doc = "index"

html_search_language = "en"
pygments_style = "sphinx"

html_show_sourcelink = False

html_theme_options = {
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
}

autodoc_member_order = "bysource"
autodoc_typehints = "both"
autodoc_typehints_description_target = "documented"
autodoc_default_options = {
    "exclude-members": ",".join(
        [
            "__weakref__",
            "__module__",
            "__abstractmethods__",
            "__dict__",
            "__parameters__",
            "__subclasshook__",
            "__init__",
            "__annotations__",
            "__dataclass_fields__",
            "__dataclass_params__ ",
            "__orig_bases__",
        ],
    ),
}

autosummary_generate = True
autosectionlabel_maxdepth = 4
autosectionlabel_prefix_document = True
