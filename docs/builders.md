---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(builders)=
# Builders

```{note}
**Version 2.0** provides only the `jupyter` builder for notebook generation.
For PDF, HTML, and execution features, use [Jupyter Book](https://jupyterbook.org/).
```

## jupyter

The `jupyter` builder converts RST and MyST source files to Jupyter notebooks.

### Basic Usage

```bash
make jupyter
```

Or directly with sphinx-build:

```bash
sphinx-build -M jupyter "source" "build" $(SPHINXOPTS)
```

### Output

Notebooks are generated in `_build/jupyter/` with:
- All markdown cells from your documentation
- Code blocks as executable cells
- Proper kernel metadata
- Static assets (images, CSS, etc.)

### Configuration

See [notebook configuration](config_extension_notebooks) for available options.

### Example Makefile Target

```makefile
.PHONY: jupyter
jupyter:
	@$(SPHINXBUILD) -M jupyter "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

## Removed Builders (v2.0)

The following builders have been removed in v2.0:

- **jupyterpdf**: Use Jupyter Book for PDF generation
  ```bash
  jupyter-book build --builder pdflatex yourbook/
  ```

See the [migration guide](https://github.com/QuantEcon/sphinx-tojupyter/blob/main/MIGRATION.md) for details.

