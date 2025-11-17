# Makefile for MyST-NB glue tests

# Sphinx build commands
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
NOTEBOOKDIR   = ipynb

# Build targets
.PHONY: help clean jupyter html

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  jupyter         to build Jupyter notebooks (base64 images)"
	@echo "  jupyter-urlpath to build Jupyter notebooks (URL path images)"
	@echo "  html            to build HTML documentation"
	@echo "  clean           to remove build artifacts"

clean:
	rm -rf $(BUILDDIR)
	rm -rf $(NOTEBOOKDIR)
	rm -rf .jupyter_cache

jupyter:
	$(SPHINXBUILD) -b jupyter $(SOURCEDIR) $(NOTEBOOKDIR)

jupyter-urlpath:
	$(SPHINXBUILD) -D tojupyter_glue_urlpath="https://example.com" \
		-b jupyter $(SOURCEDIR) ipynb_urltest

html:
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)/html
