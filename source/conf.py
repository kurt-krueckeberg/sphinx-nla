# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Lower Saxony Archive in Bückeburg Documents'
copyright = '2026, Kurt Krueckeberg'
author = 'Kurt Krueckeberg'
release = '0.8'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',        # Enables Markdown support
    'sphinx_inline_tabs',  # Enables tabbed content
    'linuxdoc.rstFlatTable',
    'sphinx_external_toc',
    'sphinx.ext.intersphinx',
    'sphinx_design',
]

external_toc_exclude_missing = True # exclude .md files not listing in the _toc.yml file.

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# Add this to enable colon-fences (useful for the :::figure::: syntax)
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

master_doc = "index"
nitpicky = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'

html_static_path = ['_static']

html_css_files = [
    'custom.css',
]

html_js_files = ['antora-self-link.js']

html_theme_options = {
    "show_navbar_depth": 2,
    "home_page_in_toc": True,
    "use_download_button": True,
}
