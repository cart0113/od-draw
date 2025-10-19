"""
Sphinx configuration for od-draw documentation.
"""

project = 'od-draw'
copyright = '2025, AJ Carter'
author = 'AJ Carter'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'furo'
html_static_path = ['_static']

html_theme_options = {
    "sidebar_hide_name": False,
}
