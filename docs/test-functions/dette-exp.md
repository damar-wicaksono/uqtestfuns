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

(test-functions:dette-exp)=
# Exponential Function from Dette and Pepelyshev (2010)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The function is a three-dimensional, scalar-valued function that exhibits
asymptotic behavior where the function value approaches zero near the origin
and increases toward a value as the input moves farther away from the origin
in any direction.

The function appeared in {cite}`Dette2010` as a test function for comparing
different experimental designs in the construction of metamodels.

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.DetteExp()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is defined as[^location]:

$$
\mathcal{M}(\boldsymbol{x}) = 100 \left[ \exp{\left( -\frac{2}{x_1^{1.75}} \right)} + \exp{\left( -\frac{2}{x_2^{1.5}} \right)} + \exp{\left( -\frac{2}{x_3^{1.25}} \right)} \right],
$$

where $\boldsymbol{x} = \left( x_1, x_2, x_3 \right)$ is the three-dimensional
vector of input variables further defined below.

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

[^location]: see Eq. (4), Section 3.1, p. 424, in {cite}`Dette2010`.
