#!/usr/bin/env python
# coding: utf-8

# (config_extension_pdf)=
# # Converting Notebooks to PDF
# 
# ```{contents} Options
# ---
# depth: 1
# local: 
# ---
# ```
# 
# ## jupyter_latex_template
# 
# Provide path to latex nbconvert template file
# 
# `conf.py` usage:

# In[1]:


jupyter_latex_template = "theme/templates/latex.tpl"


# ## jupyter_pdf_logo
# 
# Add project logo to pdf document
# 
# `conf.py` usage:

# In[2]:


jupyter_pdf_logo = "theme/img/logo.png"


# ## jupyter_bib_file
# 
# Provide path to bibtex file for reference support
# 
# `conf.py` usage:

# In[3]:


jupyter_bib_file = "_static/references.bib"


# ## jupyter_pdf_author
# 
# Specify Author Field for PDF document
# 
# `conf.py` usage:

# In[4]:


jupyter_pdf_author = "QuantEcon Developers"


# ## jupyter_pdf_showcontentdepth
# 
# Specify which depth of the local contents directives to add to generated pdf files
# 
# 
# 
# 
# 
# |Values|
# |:--------------------------------------------------------------------------------------------------:|
# |2  (|**|Default|**|)|
# 
# ```{note}
# this shows second level contents by default as the pdf document adds the page
# or document title to the top of the article format.
# ```
# 
# ## jupyter_pdf_urlpath
# 
# Enable local links within the project to link a hosted located via a urlprefix and
# link modification.
# 
# `conf.py` usage:

# In[5]:


jupyter_pdf_urlpath  = "https://lectures.quantecon.org/"


# ## jupyter_pdf_excludepatterns
# 
# Exclude certainly documents from getting compiled as pdf files.
# 
# `conf.py` usage:

# In[6]:


jupyter_pdf_excludepatterns = ["index", "404", "search"]


# This can be useful for make site when pdf construction is part of
# a broader project that supports html targets.
