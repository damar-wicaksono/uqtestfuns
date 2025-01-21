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

(test-functions:higdon-sine)=
# Sine Function from Higdon (2002)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The function is a simple one-dimensional, scalar-valued test function.
It was featured in {cite}`Higdon2002` as an example for illustrating
a multi-resolution spatial modeling technique.

A plot of the function is shown below..

```{code-cell} ipython3
:tags: [remove-input]

rng = np.random.default_rng(93025)
my_testfun = uqtf.HigdonSine()

xx = np.linspace(1.0, 10.0, 100)[:, np.newaxis]
yy = my_testfun(xx)

xx_train = np.linspace(1, 10, 30)[:, np.newaxis]
yy_train = my_testfun(xx_train) + rng.normal(0, 0.1, size=(30, 1))

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
In the original paper, the function was evaluated at 30 equispaced points
in $[1.0, 10.0]$ with added i.i.d noise from $\mathcal{N} \sim (0, 0.1)$;
these points are shown in the above plot.
```

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.HigdonSine()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is analytically defined as follows[^location]:

$$
\mathcal{M}(x) = \sin{\left(2 \pi \frac{x}{10} \right)} + 0.2 \, \sin{\left(2 \pi \frac{x}{2.5} \right)},
$$

where $x$ is further defined below.

Notice that the second term of the equation gives variation 5 times smaller
but 4 times faster.

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

[^location]: see Section 4.1 in {cite}`Higdon2002`.
