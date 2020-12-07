SHELL := bash
#
# Makefile for Sphinx Extension Test Cases
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = python -msphinx
SPHINXPROJ    = sphinxcontrib-jupyter-testcases
#BASE
SOURCEDIR     = base/
BUILDDIR      = base/_build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile test

test: clean jupyter jupyter-project
	python check_diffs.py

jupyter-project:
	cd project/lecture-python-programming.myst && jb build lectures --path-output ../ --builder=custom --custom-builder=jupyter

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
