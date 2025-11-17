# Proofs

This document tests the proof directive.

## Theorem with Proof

```{prf:theorem} Fermat's Little Theorem
:label: fermat

If $p$ is a prime number, then for any integer $a$, the number $a^p - a$ is an integer multiple of $p$.
```

```{prf:proof}

We proceed by induction on $a$.

**Base case:** When $a = 0$, we have $0^p - 0 = 0$, which is clearly divisible by $p$.

**Inductive step:** Assume $a^p - a$ is divisible by $p$. We need to show that $(a+1)^p - (a+1)$ is divisible by $p$.

By the binomial theorem:

$$
(a+1)^p = \sum_{k=0}^{p} \binom{p}{k} a^k
$$

Since $p$ is prime, $\binom{p}{k}$ is divisible by $p$ for $0 < k < p$.

Therefore:

$$
(a+1)^p - (a+1) = a^p - a + p \cdot (\text{integer})
$$

By the inductive hypothesis, this is divisible by $p$.
```

## Simple Proof

```{prf:theorem}
:label: simple-theorem

The sum of two even numbers is even.
```

```{prf:proof}

Let $a = 2m$ and $b = 2n$ where $m, n$ are integers.

Then:

$$
a + b = 2m + 2n = 2(m + n)
$$

Since $m + n$ is an integer, $a + b$ is even.
```

## Proof with Class Name

```{prf:proof}
:class: dropdown

This proof is hidden by default (if sphinx-togglebutton is enabled).

The proof uses standard techniques and is left as an exercise.
```
