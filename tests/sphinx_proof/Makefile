# Makefile for sphinx-proof tests

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help jupyter clean

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  jupyter    to make Jupyter notebooks"
	@echo "  clean      to remove build artifacts"

jupyter:
	$(SPHINXBUILD) -b jupyter $(SOURCEDIR) $(BUILDDIR)/jupyter $(SPHINXOPTS)
	@echo
	@echo "Build finished. The Jupyter notebooks are in $(BUILDDIR)/jupyter."

clean:
	rm -rf $(BUILDDIR)
	@echo "Build artifacts removed."
