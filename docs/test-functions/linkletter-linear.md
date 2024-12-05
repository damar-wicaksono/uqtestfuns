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

(test-functions:linkletter-linear)=
# Linear Function from Linkletter et al. (2006)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The linear function is a ten-dimensional, scalar-valued function.
Only the first four input variables are active, while the rest is inert.
The function was used in {cite}`Linkletter2006` to demonstrate a variable
selection method (i.e., sensitivity analysis)
in the context of Gaussian process metamodeling:

```{note}
Linkletter et al. {cite}`Linkletter2006` introduced four ten-dimensional
analytical test functions with some of the input variables inert.
They are used to demonstrate a variable selection method (i.e., screening)
in the context of Gaussian process metamodeling:

- {ref}`Linear <test-functions:linkletter-linear>` function features
  a simple function with four active input variables (out of 10).
  (_this function_)
```


## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.LinkletterLinear()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is defined as[^location]:

$$
\mathcal{M}(\boldsymbol{x}) = 0.2 (x_1 + x_2 + x_3 + x_4),
$$

where $\boldsymbol{x} = \left( x_1, \ldots x_{10} \right)$
is the ten-dimensional vector of input variables further defined below.
Notice that only four out of ten input variables are active.

```{note}
In the original paper, the function was added with an independent identically
distributed (i.i.d) noise from $\mathcal{N}(0, \sigma)$
with a standard deviation $\sigma = 0.05$.
```

## Probabilistic input

The probabilistic input model for the test function is shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

## Reference results

This section provides several reference results of typical UQ analyses involving
the test function.

### Sample histogram

Shown below is the histogram of the output based on $100'000$ random points:

```{code-cell} ipython3
:tags: [hide-input]

my_testfun.prob_input.reset_rng(42)
xx_test = my_testfun.prob_input.get_sample(100000)
yy_test = my_testfun(xx_test)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(X)$");
plt.gcf().tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Eq. (5), Example 1, in {cite}`Linkletter2006`.
