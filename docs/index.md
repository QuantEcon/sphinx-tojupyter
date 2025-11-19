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

# `sphinx-tojupyter` Documentation

This sphinx extension converts RST and MyST source files to Jupyter notebooks.

**Version 2.0** focuses solely on notebook generation. For notebook execution, PDF generation, 
and website building, use [Jupyter Book](https://jupyterbook.org/).

```{note}
Version 2.0 is a major refactoring that removes PDF, HTML, and execution features.
See the [migration guide](https://github.com/QuantEcon/sphinx-tojupyter/blob/main/MIGRATION.md) 
if upgrading from v1.x.
```

**Requires:** Sphinx >= 7.0

One of the main benefits of writing Jupyter notebooks as `RST` files is to simplify
the task of version control for large projects.

```{toctree}
:caption: Contents
:maxdepth: 1

installation
config-sphinx
config-extension
myst-nb
latex-macros
examples
config-example
config-project
builders
```

## Credits

This project is supported by [QuantEcon](https://www.quantecon.org)

Many thanks to the lead developers of this project.

* [@AakashGfude](https://github.com/AakashGfude)
* [@mmcky](https://github.com/mmcky)

Contributors

* [FelipeMaldonado](https://github.com/FelipeMaldonado)
* [@myuuuuun](https://github.com/myuuuuun)
* [@NickSifniotis](https://github.com/NickSifniotis)

## Projects using Extension

1. [QuantEcon Lectures](https://lectures.quantecon.org)

If you find this extension useful please let us know at
[contact@quantecon.org](mailto:contact@quantecon.org)

# LICENSE

Copyright © 2019 QuantEcon Development Team: BSD-3 All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
1. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
1. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Indices and tables

* {ref}`genindex <genindex>`
* {ref}`modindex <modindex>`
* {ref}`search <search>`

