# Basic Directives Test

This document tests all basic sphinx-proof directive types.

## Theorem

```{prf:theorem}
:label: basic-theorem

Let $f$ be a function defined on $[a,b]$. If $f$ is continuous on $[a,b]$, then $f$ is integrable on $[a,b]$.
```

## Axiom

```{prf:axiom}
:label: basic-axiom

For any sets $A$ and $B$, we have $A \cup B = B \cup A$.
```

## Lemma

```{prf:lemma}
:label: basic-lemma

If $n$ is even, then $n^2$ is even.
```

## Definition

```{prf:definition}
:label: basic-definition

A **prime number** is a natural number greater than 1 that has no positive divisors other than 1 and itself.
```

## Remark

```{prf:remark}
:label: basic-remark

This result can be extended to more general cases.
```

## Conjecture

```{prf:conjecture}
:label: basic-conjecture

Every even integer greater than 2 can be expressed as the sum of two primes.
```

## Corollary

```{prf:corollary}
:label: basic-corollary

If $f$ is differentiable at $x_0$, then $f$ is continuous at $x_0$.
```

## Algorithm

```{prf:algorithm}
:label: basic-algorithm

**Inputs:** A list of numbers $L = [a_1, a_2, \ldots, a_n]$

**Output:** The maximum value in $L$

1. Set $max = a_1$
2. For $i = 2$ to $n$:
   - If $a_i > max$, set $max = a_i$
3. Return $max$
```

## Criterion

```{prf:criterion}
:label: basic-criterion

A function $f$ is continuous at $x_0$ if and only if for every $\epsilon > 0$, there exists $\delta > 0$ such that $|x - x_0| < \delta$ implies $|f(x) - f(x_0)| < \epsilon$.
```

## Example

```{prf:example}
:label: basic-example

Consider the function $f(x) = x^2$. We have:

$$
f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h} = \lim_{h \to 0} \frac{(x+h)^2 - x^2}{h} = 2x
$$
```

## Property

```{prf:property}
:label: basic-property

The set of real numbers $\mathbb{R}$ is uncountable.
```

## Observation

```{prf:observation}
:label: basic-observation

As the sample size increases, the sample mean tends to approach the population mean.
```

## Proposition

```{prf:proposition}
:label: basic-proposition

For any positive integer $n$, the sum of the first $n$ positive integers is $\frac{n(n+1)}{2}$.
```

## Assumption

```{prf:assumption}
:label: basic-assumption

We assume that all agents in the economy are rational and have perfect information.
```

## Notation

```{prf:notation}
:label: basic-notation

We denote the set of natural numbers by $\mathbb{N}$, the set of integers by $\mathbb{Z}$, and the set of real numbers by $\mathbb{R}$.
```
