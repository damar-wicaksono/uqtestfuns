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

(test-functions:currin-sine)=
# Sine Function from Currin et al. (1988)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The function is a simple one-dimensional, scalar-valued test function.
It was featured in {cite}`Currin1988` as an example introducing Gaussian
process metamodeling method.

A plot of the function is shown below..

```{code-cell} ipython3
:tags: [remove-input]

my_testfun = uqtf.CurrinSine()

xx = np.linspace(0, 1, 100)[:, np.newaxis]
yy = my_testfun(xx)

xx_train = np.array([[0.0], [0.25], [0.5], [0.75], [1.0]])
yy_train = my_testfun(xx_train)

# --- Create the plot
plt.plot(xx, yy, color="#8da0cb")
plt.scatter(xx_train, yy_train, color="#8da0cb")
plt.grid()
plt.xlabel("$x$")
plt.ylabel("$\mathcal{M}(x)$")
plt.gcf().tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

```{note}
In the original paper, the function was evaluated at
$x = \{ 0.00, 0.25, 0.50, 0.75, 1.00 \}$ to serve as the training data;
these points are shown in the above plot.
```

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.CurrinSine()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is analytically defined as follows[^location]:

$$
\mathcal{M}(x) = \sin{\left( 2 \, \pi \, \left( x - 0.1 \right) \right)},
$$

where $x$ is further defined below.

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

[^location]: see Eq. (5.1), Section 5.1, p. 20, in {cite}`Currin1988`.
