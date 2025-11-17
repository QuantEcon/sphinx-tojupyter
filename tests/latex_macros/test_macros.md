# LaTeX Macros Test

This notebook tests LaTeX macro support in sphinx-tojupyter.

## Custom Math Commands

We define custom LaTeX commands like `\ZZ`, `\RR`, `\NN`, etc. These should render properly in the Jupyter notebook.

### Examples

The set of integers is denoted by $\ZZ$.

The set of real numbers is $\RR$.

The natural numbers are $\NN = \{0, 1, 2, 3, \ldots\}$.

### Inline Math

We can use these in inline math: $x \in \RR$ and $n \in \NN$.

### Display Math

$$
\begin{align}
\ZZ &\subset \QQ \subset \RR \subset \CC \\
\NN &\subset \ZZ
\end{align}
$$

## Summary

This test demonstrates:

- Custom LaTeX macros defined via `tojupyter_latex_macros`
- Macros working in inline math
- Macros working in display math
- Multiple custom commands (`\ZZ`, `\RR`, `\NN`, `\QQ`, `\CC`)
