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

(test-functions:gramacy-1d-sine)=
# Gramacy (2007) One-dimensional (1D) Sine Function

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The Gramacy (2007) one-dimensional (1D) sine function 
(or `Gramacy1DSine` function for short)
is a scalar-valued function that features two regimes: one part is a mixture
of sines and cosines, and another part is a linear function.
The function was introduced in {cite}`Gramacy2007` in the context of 
metamodeling with non-stationary Gaussian processes.

A plot of the function is shown below for $x \in [0, 20]$.

```{code-cell} ipython3
:tags: [remove-input]

my_testfun = uqtf.Gramacy1DSine()

xx = np.linspace(0, 20, 100)[:, np.newaxis]
yy = my_testfun(xx)

# --- Create the plot
plt.plot(xx, yy, color="#8da0cb")
plt.grid()
plt.xlabel("$x$")
plt.ylabel("$\mathcal{M}(x)$")
plt.gcf().tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

Note that the function is discontinuous at $x = 9.6%$ which also pinpoints
the change of regime.

```{note}
In the original paper, the response of the function is disturbed by an 
independent identically distributed (i.i.d) Gaussian noise 
$\varepsilon \sim \mathcal{N}(0, \sigma_n=0.1)$.
```

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.Gramacy1DSine()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is analytically defined as follows[^location]:

$$
\mathcal{M}(x) = \begin{cases}
\sin{(\frac{\pi x}{5})} + \frac{1}{5} \cos{(\frac{4 \pi x}{5})}, & x \leq 9.6 \\
\frac{1}{10} x - 1, & x > 9.6,
\end{cases}
$$
where $x$ is defined below.

## Probabilistic input

Based on {cite}`Gramacy2007`, the domain of the function is $[0, 20]$.
This input can be modeled with a single uniform random variable shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Section 4.2, p. 17, Eq. (16) in {cite}`Gramacy2007`;
also the actual implementation as an R code not far below that.
