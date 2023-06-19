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

(test-functions:forrester)=
# One-dimensional (1D) Forrester et al. (2008) Function

The 1D Forrester et al. (2008) function (or `Forrester2008` function for short)
is a one-dimensional scalar-valued function.
It was used in {cite}`Forrester2008` as a test function for illustrating
optimization using metamodels.

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

A plot of the function is shown below for $x \in [0, 1]$.

```{code-cell} ipython3
:tags: [remove-input]

my_testfun = uqtf.Forrester2008()
xx = np.linspace(0, 1, 1000)[:, np.newaxis]
yy = my_testfun(xx)

# --- Create the plot
plt.plot(xx, yy, color="#8da0cb")
plt.grid()
plt.xlabel("$x$")
plt.ylabel("$\mathcal{M}(x)$")
plt.ylim([-10, 15])
plt.scatter(
    np.array([0.14258919, 0.75724876, 0.5240772]),
    np.array([-0.98632541, -6.02074006, 0.98632541]),
    color="k",
    marker="x",
    s=50,
)
plt.gcf().tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

As can be seen in the plot above, the function features a multimodal shape
with one global minimum ($\approx -6.02074006$ at $x = 0.75724876$),
one global maximum ($\approx -0.98632541$ at $x = 014258919$),
and an inflection point with zero gradient ($\approx -6.02074006$ at $x = 0.5240772$).

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.Forrester2008()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is analytically defined as follows:

$$
\mathcal{M}(x) = (6 x - 2)^2 \sin{(12 x - 4)}
$$
where $x$ is defined below.

## Input

Based on {cite}`Forrester2008`, the search domain of the 
function is in $[0, 1]$.
In UQTestFuns, this search domain can be represented as probabilistic input
using the uniform distribution with a marginal shown in the table below.

```{code-cell} ipython3
my_testfun.prob_input
```

## Reference results

This section provides several reference results of typical UQ analyses involving
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
plt.xlabel("$\mathcal{M}(X)$");
plt.gcf().tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

### Optimum values

The optimum values of the function are:

- Global minimum: $\mathcal{M}(\boldsymbol{x}^*) \approx -6.02074006$ at $x^* = 0.75724876$.
- Local minimum: $\mathcal{M}(\boldsymbol{x}^*) \approx -0.98632541$ at $x^* = 014258919$.
- Inflection: $\mathcal{M}(\boldsymbol{x}^*) \approx -6.02074006$ at $x^* = 0.5240772$.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
