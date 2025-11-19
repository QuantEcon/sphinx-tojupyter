# Makefile for Sphinx Jupyter builder (raw HTML tests)

SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help jupyter clean

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  jupyter    to make Jupyter notebooks"
	@echo "  clean      to remove generated files"

jupyter:
	@echo "Building Jupyter notebooks with raw HTML drop enabled..."
	$(SPHINXBUILD) -b jupyter $(SOURCEDIR) $(BUILDDIR)/jupyter
	@echo
	@echo "Notebooks built in $(BUILDDIR)/jupyter/"
	@echo
	@echo "Verify that raw HTML blocks are NOT present in the notebooks."

clean:
	rm -rf $(BUILDDIR)
