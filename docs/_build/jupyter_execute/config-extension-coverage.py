#!/usr/bin/env python
# coding: utf-8

# (coverage_extension_coverage)=
# # Computing Coverage Statistics
# 
# ```{warning}
# `make coverage` will currently produce a `json` report
# that can be used to support an execution status page. But adding
# badges and a status page needs to be made into an option and
# specified via the default theme.
# See [#237](https://github.com/QuantEcon/sphinx-tojupyter/issues/237)
# ```
# 
# ## jupyter_make_coverage
# 
# Enable coverage statistics to be computed
# 
# 
# 
# 
# 
# 
# 
# |Values|
# |:--------------------------------------------------------------------------------------------------:|
# |False (|**|default|**|)|
# |True|
# 
# ## jupyter_template_coverage_file_path
# 
# Provide path to template coverage file
# 
# ```{todo}
# ## Todo
# 
# Document format for template
# 
# ```
# 
# `conf.py` usage:

# In[1]:


jupyter_template_coverage_file_path = "theme/templates/<file>.json"

