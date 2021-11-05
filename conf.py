# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# import sphinx_celery
import pydata_sphinx_theme
import ablog

# -- Project information -----------------------------------------------------

project = 'Paper Weekly'
copyright = '2021, Xinyi Li'
author = 'Xinyi Li'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["myst_parser",'sphinx_panels', 'sphinx.ext.viewcode', 'sphinx_copybutton', "sphinx.ext.autodoc",
              "sphinx.ext.autosummary", "ablog", "sphinxext.opengraph","sphinx_togglebutton"]
# Add any paths that contain templates here, relative to this directory.
templates_path = [ablog.get_html_templates_path()]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store','README.md']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "pydata_sphinx_theme"

html_theme_options = {
  "github_url": "https://github.com/li-xin-yi/",
  "search_bar_text": "Search this site...",
  "show_toc_level": 3,
}


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

myst_enable_extensions = ["dollarmath", "amsmath","linkify","deflist",
    "colon_fence",]

html_sidebars = {
    "posts/**": ['searchbox.html','postcard.html','tagcloud.html','archives.html'],
    "notes": ['searchbox.html','tagcloud.html', 'archives.html'],
    "index": ['searchbox.html','recentposts.html','tagcloud.html','archives.html',],
     
}

blog_title = "Paper Notes"

blog_path = "notes"
fontawesome_included = True

blog_post_pattern = "posts/*/*"
post_redirect_refresh = 1
post_auto_image = 1
post_auto_excerpt = 2

panels_add_bootstrap_css = False

def setup(app):
    app.add_css_file("custom.css")