# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# I've simplified this a little to use append instead of insert.
# sys.path.append(os.path.abspath('../'))
sys.path.append(os.path.abspath('../mysite'))

# Specify settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# # Setup Django
import django
django.setup()

project = 'Portal for Courses'
copyright = '2022, Veeresh, Pratham, Faiz'
author = 'Veeresh, Pratham, Faiz'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', "**/*.migrations.rst",]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
