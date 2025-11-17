# Numbered Directives with Titles

This document tests numbered directives with titles.

## Named Theorem

```{prf:theorem} Pythagorean Theorem
:label: pythagoras

In a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides:

$$
a^2 + b^2 = c^2
$$
```

## Named Definition

```{prf:definition} Limit of a Function
:label: limit-definition

We say that $\lim_{x \to a} f(x) = L$ if for every $\epsilon > 0$, there exists $\delta > 0$ such that $0 < |x - a| < \delta$ implies $|f(x) - L| < \epsilon$.
```

## Named Lemma

```{prf:lemma} Fundamental Lemma
:label: fundamental-lemma

If $f$ is continuous on $[a,b]$ and differentiable on $(a,b)$, then there exists $c \in (a,b)$ such that:

$$
f'(c) = \frac{f(b) - f(a)}{b - a}
$$
```

## Unnumbered Example

Some directives can be unnumbered using the `:nonumber:` option:

```{prf:example}
:nonumber:

This example has no number assigned to it.

$$
\int_0^\infty e^{-x} dx = 1
$$
```

## Another Numbered Theorem

```{prf:theorem} Mean Value Theorem
:label: mvt

Let $f$ be continuous on $[a,b]$ and differentiable on $(a,b)$. Then there exists $c \in (a,b)$ such that:

$$
f'(c) = \frac{f(b) - f(a)}{b - a}
$$
```

## Cross-referencing

We can reference {prf:ref}`pythagoras` and {prf:ref}`limit-definition` in our text.

The {prf:ref}`fundamental-lemma` is used to prove {prf:ref}`mvt`.
