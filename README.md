# sphinx-tojupyter

A [Sphinx](http://www.sphinx-doc.org/en/stable/) Extension for
Generating [Jupyter Notebooks](https://jupyter.org/)

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
