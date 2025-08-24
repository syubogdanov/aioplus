import os
import sys

# "Read the Docs" may not find the package
sys.path.insert(0, os.path.abspath(".."))

author = "Sergei Y. Bogdanov <syubogdanov@outlook.com>"
copyright = "2025, Sergei Y. Bogdanov"
project = "aioplus"

html_theme = "alabaster"
html_theme_options = {
    "description": "Because asyncio.gather() is not enough!",
    "github_user": "syubogdanov",
    "github_repo": "aioplus",
    "github_type": "star",
    "github_button": True,
    "github_banner": True,
}

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

autodoc_member_order = "bysource"
autodoc_typehints = "description"
