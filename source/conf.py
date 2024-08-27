# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cog_plot'
copyright = '2024, Alex Lepauvre'
author = 'Alex Lepauvre'
version = 'v0.1'
release = 'v0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autosummary',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]
autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = []
html_static_path = ['source/_static']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_logo = "./_static/cogitate_logo.png"

html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["navbar-icon-links"],
    "navbar_persistent": ["search-button"],
    "navbar_align": "content",  # Aligns the navbar content with the page content
    "show_nav_level": 2,    
    "secondary_sidebar_items": ["page-toc", "sourcelink"]
}
