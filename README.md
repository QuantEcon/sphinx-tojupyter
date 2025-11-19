# sphinx-tojupyter

A [Sphinx](http://www.sphinx-doc.org/en/stable/) Extension for
Generating [Jupyter Notebooks](https://jupyter.org/)

**Version 2.0** - Focused on converting RST and MyST source files to Jupyter notebooks. For notebook execution, PDF generation, and website building, use [Jupyter Book](https://jupyterbook.org/).

## Installation

To install you can clone the repository and install using:

```bash
python setup.py install
```

## Usage

Update project `conf.py` file to include the jupyter extension and the
desired **configuration** settings (see [configuration](#configuration)
section below):

``` {.python}
extensions = ["sphinx_tojupyter"]
```

then run

```bash
make jupyter
```

## Features

### MyST-NB Glue Support

This extension supports [MyST-NB](https://myst-nb.readthedocs.io/) glue functionality, allowing you to store and reference notebook variables in your documentation:

**Basic Usage:**

```markdown
\```python
from myst_nb import glue
glue("my_variable", "Hello World")
glue("my_number", 3.14159)
\```

The value is {glue:text}`my_variable` and pi is approximately {glue:text}`my_number:.2f`.
```

**Figure Glue:**

```markdown
\```python
import matplotlib.pyplot as plt
from myst_nb import glue

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
glue("my_plot", fig, display=False)
\```

\```{glue:figure} my_plot
:name: fig-example

Caption for the figure.
\```
```

**Requirements:**
- Add `myst_nb` to your extensions in `conf.py`
- Set `nb_execution_mode = "cache"` (or "auto"/"force")

See the [test suite](tests/glue/) for more examples.

### sphinx-proof Support

Full support for [sphinx-proof](https://sphinx-proof.readthedocs.io/) directives, allowing you to include mathematical theorems, proofs, and related content in your notebooks:

**Supported Directives (15 types):**
- `theorem`, `axiom`, `lemma`, `definition`, `remark`
- `conjecture`, `corollary`, `algorithm`, `criterion`
- `example`, `property`, `observation`, `proposition`
- `assumption`, `notation`, `proof`

**Example:**

```markdown
\```{prf:theorem} Pythagorean Theorem
:label: pythagoras

In a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides:

$$
a^2 + b^2 = c^2
$$
\```

\```{prf:proof}
The proof follows from...
\```
```

**Features:**
- ✅ Automatic numbering from Sphinx's numfig system
- ✅ Support for titled and untitled directives
- ✅ Cross-reference handling
- ✅ Clean markdown formatting for notebooks

**Requirements:**
- Add `sphinx_proof` to your extensions in `conf.py`
- Enable `numfig = True` for numbered directives

See the [test suite](tests/sphinx_proof/) for comprehensive examples.

### LaTeX Macros Support

Define custom LaTeX commands once, use everywhere (HTML and notebooks):

```python
# conf.py
mathjax3_config = {
    'tex': {
        'macros': {
            'ZZ': r'\mathbb{Z}',
            'RR': r'\mathbb{R}',
            'NN': r'\mathbb{N}',
        }
    }
}
```

Then use them in your documentation:

```markdown
The set of integers is $\ZZ$ and the reals are $\RR$.
```

**Benefits:**
- ✅ Single configuration for HTML and notebooks
- ✅ Standard Sphinx/Jupyter Book approach  
- ✅ Macros automatically added to generated notebooks
- ✅ Works with existing `mathjax3_config` setups

See the [LaTeX macros documentation](docs/latex-macros.md) and [test suite](tests/latex_macros/) for more details.

Credits
-------

This project is supported by [QuantEcon](https://www.quantecon.org). The
writers and translators have been migrated and improved from the
[sphinxcontrib-jupyter](https://github.com/quantecon/sphinxcontrib-jupyter) project.

Many thanks to the contributors of this project.

-   [\@AakashGfude](https://github.com/AakashGfude)
-   [\@mmcky](https://github.com/mmcky)
-   [\@myuuuuun](https://github.com/myuuuuun)
-   [\@NickSifniotis](https://github.com/NickSifniotis)

LICENSE
-------

Copyright © 2020 QuantEcon Development Team: BSD-3 All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1.  Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
2.  Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.
3.  Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived from
    this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS
IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
