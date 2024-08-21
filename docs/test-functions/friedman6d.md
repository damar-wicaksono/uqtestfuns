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

(test-functions:friedman-6d)=
# Six-dimensional (6D) Friedman Function

The 6D Friedman function (or `Friedman6D` function for short) is
a six-dimensional (including one dummy variable) scalar-valued function.
The function features a combination of non-linearity and variable interaction.

It was originally used in {cite}`Friedman1983` as a test function for testing
a spline approximation method.
In {cite}`Sun2022` and {cite}`Horiguchi2021` (albeit in a modified form)
the function was employed as a test function in the context of
sensitivity analysis.

```{note}
The function was later extended to ten dimension by incorporating four
additional dummy variables (for a total of five) in {cite}`Friedman1991`;
the function is also {ref}`available <test-functions:friedman10d>`
in UQTestFuns.
```

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.Friedman6D()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is analytically defined as follows:

$$
\mathcal{M}(\boldsymbol{x}) = 10 \sin{(\pi x_1 x_2)} + 20 (x_3 - 0.5)^2 + 10 x_4 + 5 x_5 + 0 x_6,
$$
where $x$ is defined below. Notice that the sixth input variable is inert.

## Input

Based on {cite}`Friedman1983`, the probabilistic input model
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