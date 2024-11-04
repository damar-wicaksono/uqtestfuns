---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

(test-functions:welch1992)=
# Welch et al. (1992) Function

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The Welch et al. (1992) test function (or the `Welch1992` function for short)
is a 20-dimensional scalar-valued function.
The function features some strong non-linearities as well as some
pair interaction effects. Furthermore, a couple of two input variables
are set to be inert.

The function was introduced in Welch et al. (1992) {cite}`Welch1992`
as a test function for metamodeling and sensitivity analysis purposes.
The function is also suitable for testing multi-dimensional integration
algorithms.

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.Welch1992()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The `Welch1992` function is defined as follows[^location]:

$$
\begin{aligned}
\mathcal{M}(\boldsymbol{x}) =
    & \frac{5 x_{12}}{1 + x_1} + 5 (x_4 - x_{20})^2 + x_5 + 40 x_{19}^3 - 5 x_{19} \\
    & + 0.05 x_2 + 0.08 x_3 - 0.03 x_6 + 0.03 x_7 \\
    & - 0.09 x_9 - 0.01 x_{10} - 0.07 x_{11} + 0.25 x_{13}^2 \\
    & - 0.04 x_{14} + 0.06 x_{15} - 0.01 x_{17} - 0.03 x_{18},
\end{aligned}
$$

where $\boldsymbol{x} = \{ x_1, \ldots, x_{20} \}$ is the 20-dimensional vector
of input variables further defined below.
Notice that the input variables $x_8$ and $x_{16}$ are inert
and therefore, missing from the expression.

## Probabilistic input

Based on {cite}`Welch1992`, the test function is defined on the 
20-dimensional input space $[-0.5, 0.5]^{20}$.
This input can be modeled using 20 independent uniform random variables
shown in the table below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

## Reference Results

This section provides several reference results of typical analyses involving
the test function.

### Sample histogram

Shown below is the histogram of the output based on $100'000$ random points:

```{code-cell} ipython3
:tags: [hide-input]

np.random.seed(42)
xx_test = my_testfun.prob_input.get_sample(100000)
yy_test = my_testfun(xx_test)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

### Definite integration

The integral value of the test function over the domain $[-0.5, 0.5]^{20}$
is analytical:

$$
I[\mathcal{M}] = \int_{[-0.5, 0.5]^{20}} \mathcal{M}(\boldsymbol{x}) \; d\boldsymbol{x} = \frac{41}{48}.
$$

### Moments estimation

The moments of the test function may be derived analytically; the first two
(i.e., the expected value and the variance) are given below.

#### Expected value

Due to the fact that the function domain is a hypercube
and the input variables are uniformly distributed,
the expected value of the function is the same as the integral value
over the domain:

$$
\mathbb{E}[\mathcal{M}] = \frac{41}{48}.
$$

#### Variance

The analytical value (albeit inexact) for the variance is given as follows:

$$
\mathbb{V}[\mathcal{M}] \approx 5.2220543.
$$

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Section 3.1, p. 20 in {cite}`Welch1992`.