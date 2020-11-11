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
BUILDCOVERAGE = base/_build_coverage
#PDF
SOURCEPDF = pdf/
BUILDPDF = pdf/_build/
#no_inline_exercises
SOURCENOEX     = no_inline_exercises/
BUILDNOEX      = no_inline_exercises/_build

CORES 		  = 4

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile pdf rst-test

test: clean clean-pdf jupyter pdf
	python check_diffs.py

no-inline:
	@$(SPHINXBUILD) -M jupyter "$(SOURCENOEX)" "$(BUILDNOEX)" $(SPHINXOPTS) $(O)

clean-no-inline:
	rm -rf $(BUILDNOEX)

no-inline-test: clean-no-inline no-inline
	python check_diffs.py

preview:
ifneq (,$(filter $(parallel),website Website))
	cd _build/jupyter_html/ && python -m http.server
else
ifdef lecture
	cd _build/jupyter/ && jupyter notebook $(basename $(lecture)).ipynb
else
	cd _build/jupyter/ && jupyter notebook
endif
endif

clean-coverage:
	rm -rf $(BUILDCOVERAGE)

clean-website:
	rm -rf $(BUILDWEBSITE)

clean-pdf:
	rm -rf $(BUILDPDF)

pdf:
	@$(SPHINXBUILD) -M jupyterpdf "$(SOURCEPDF)" "$(BUILDPDF)" $(SPHINXOPTS) $(O) -D tojupyter_number_workers=$(CORES)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
