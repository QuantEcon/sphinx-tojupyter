#!/usr/bin/env python
# coding: utf-8

# (sphinx_setup)=
# # Sphinx Setup
# 
# To initially setup a Sphinx project, please refer [here](https://www.sphinx-doc.org/en/master/usage/quickstart.html).
# 
# ```{note}
# QuantEcon has developed a `jupinx-quickstart` that can assist with setting up a repository
# to get you up and running quickly. Please refer to the [Jupinx Project](https://jupinx.quantecon.org/)
# for more details.
# ```
# 
# You can use the sphinx quickstart and update the project `conf.py` file to
# include the jupyter extension and add the desired configuration settings
# (see {doc}`Extension Configuration <config-extension>` section for details):

# In[1]:


extensions = ["sphinx_tojupyter"]


# once the extension is installed you can then run:
# 
# ```{code-block} bash
# make jupyter
# ```
# 
# The {doc}`Extension Configuration <config-extension>` section includes details
# on how to configure the extension in your `conf.py`.
