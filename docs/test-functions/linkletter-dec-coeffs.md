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

(test-functions:linkletter-dec-coeffs)=
# Linear Function with Decreasing Coefficients from Linkletter et al. (2006)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The `LinkletterDecCoeffs` function is a nominally ten-dimensional function
introduced in {cite}`Linkletter2006` to demonstrate variable selection
in the context of Gaussian process metamodeling.
Only the first eight input variables are active with decreasing coefficients;
the remaining two are inert.

```{note}
Linkletter et al. {cite}`Linkletter2006` introduced four _nominally_
ten-dimensional analytical test functions
with some of the input variables inert.
They are used to demonstrate a variable selection method (i.e., screening)
in the context of Gaussian process metamodeling:

- {ref}`Linear <test-functions:linkletter-linear>` function features
  a simple function with four active input variables (out of 10).
- {ref}`Linear with decreasing coefficients <test-functions:linkletter-dec-coeffs>`
  function features a slightly more complex linear function with eight active
  input variables (out of 10). (_this function_)
- {ref}`Sine <test-functions:linkletter-sine>` function features only two
  active input variables (out of 10); the effect of the two inputs on
  the output, however, is very different.
- {ref}`Inert <test-functions:linkletter-inert>` function does not have any
  active input variables; a constant zero is returned for any input values.
```


## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.LinkletterDecCoeffs()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is defined as[^location]:

$$
\mathcal{M}(\boldsymbol{x}) = 0.2 \sum_{i = 1}^8 \frac{x_i}{2^{(i - 1)}}
$$

where $\boldsymbol{x} = \left( x_1, \ldots x_{10} \right)$
is the ten-dimensional vector of input variables further defined below.
Notice that only eight out of ten input variables are active.

```{note}
In the original paper, the function was added with an independent identically
distributed (i.i.d) noise from $\mathcal{N}(0, \sigma)$
with a standard deviation $\sigma = 0.05$.

Furthermore, also in the original paper, a batch of data is generated from
the function and then standardized to have mean $0.0$ and standard deviation
$1.0$.

The implementation of UQTestFuns does not include any error addition
or standardization. However, these processes can be done manually
after the data is generated.
```

## Probabilistic input

The probabilistic input model for the test function is shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

## Reference results

This section provides several reference results of typical UQ analyses
involving the test function.

### Sample histogram

Shown below is the histogram of the output based on $100'000$ random points:

```{code-cell} ipython3
:tags: [hide-input]

yy_test = my_testfun.get_sample(100000, 42)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel(r"$\mathcal{M}(X)$");
plt.gcf().tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Eq. (6), Example 1, in {cite}`Linkletter2006`.
