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

(test-functions:friedman-10d)=
# Ten-dimensional (10D) Friedman Function

The 10D Friedman function (or `Friedman6D` function for short) is
a ten-dimensional (including five dummy variables) scalar-valued function.
The function features a combination of non-linearity and variable interaction.

It was originally used in {cite}`Friedman1991` as a test function for testing
a regression spline method.

```{note}
The function was an extension of the six-dimensional version introduced
in {cite}`Friedman1983` by adding four additional dummy variables
(for a total of five);
the function is also {ref}`available <test-functions:friedman-6d>`
in UQTestFuns.
```

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as pltx
import uqtestfuns as uqtf
```

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.Friedman10D()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is analytically defined as follows:

$$
\mathcal{M}(\boldsymbol{x}) = 10 \sin{(\pi x_1 x_2)} + 20 (x_3 - 0.5)^2 + 10 x_4 + 5 x_5 + 0 x_6 + 0 x_7 + 0 x_8 + 0 x_9 + 0 x_{10},
$$
where $x$ is defined below. Notice that the last five input variables are 
inert.

## Input

Based on {cite}`Friedman1991`, the probabilistic input model
for the function consists of two independent random variables as shown below.

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

xx_test = my_testfun.prob_input.get_sample(100000)
yy_test = my_testfun(xx_test)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

## References

```{bibliography}
:filter: docname in docnames
```