# Makefile for Sphinx Jupyter builder (urlpath tests)

SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help jupyter clean

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  jupyter    to make Jupyter notebooks"
	@echo "  clean      to remove generated files"

jupyter:
	@echo "Building Jupyter notebooks with urlpath config..."
	$(SPHINXBUILD) -b jupyter $(SOURCEDIR) $(BUILDDIR)/jupyter
	@echo
	@echo "Notebooks built in $(BUILDDIR)/jupyter/"
	@echo
	@echo "Verify the following:"
	@echo "  - Cross-document links should have: https://continuous-time-mcs.quantecon.org/"
	@echo "  - In-page anchors should start with: #"
	@echo "  - External links should not be modified"

clean:
	rm -rf $(BUILDDIR)
