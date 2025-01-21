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

(test-functions:dette-8d)=
# Eight-Dimensional Function from Dette and Pepelyshev (2010)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The function is a three-dimensional, scalar-valued function.
The function include the curved term from the {ref}`curved function <test-functions:dette-curved>`
and an additional logarithm term. It is highly curved with respect to some
input variables and less so with respect to the others.

The function appeared in {cite}`Dette2010` as a test function for comparing
different experimental designs in the construction of metamodels.

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.Dette8D()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is defined as[^location]:

$$
\mathcal{M}(\boldsymbol{x}) = 4 \left( x_1 - 2 + 8 x_2 - 8 x_2^2 \right) + \left( 3 - 4 x_2 \right)^2 + 16 \left( x_3 + 1\right)^{0.5} \left( 2 x_3 - 1\right)^2
+ \sum_{k = 4}^8 k \, \ln{\left( 1 + \sum_{i = 3}^k \right)},
$$

where $\boldsymbol{x} = \left( x_1, x_2, x_3 \right)$ is the three-dimensional
vector of input variables further defined below. Notice that the term before
the logarithm term is the terms from the {ref}`curved function <test-functions:dette-curved>`.

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

[^location]: see Eq. (6), Section 3.3, p. 424, in {cite}`Dette2010`.
