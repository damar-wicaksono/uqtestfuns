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

(test-functions:bratley-c)=
# Product-of-Chebyshev-Polynomials Function from Bratley et al. (1992)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The `BratleyC` function is an $M$-dimensional scalar-valued function
defined as the product of Chebyshev polynomials of the first kind
evaluated at its inputs.
It was introduced in {cite}`Bratley1992` as a test function
for multidimensional numerical integration using low-discrepancy sequences.

```{note}
There are three other test functions used in Bratley et al. {cite}`Bratley1992`:

- {ref}`Bratley et al. (1992) A <test-functions:bratley-a>`:
  A product of an absolute function
- {ref}`Bratley et al. (1992) B <test-functions:bratley-b>`:
  A product of cosines
- {ref}`Bratley et al. (1992) C <test-functions:bratley-c>`:
  A product of the Chebyshev polynomial of the first kind (_this function_)
- {ref}`Bratley et al. (1992) D <test-functions:bratley-d>`:
  A sum of product
```

The plots for one-dimensional and two-dimensional `BratleyC` functions
are shown below.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data
my_bratley_c_1d = uqtf.BratleyC(input_dimension=1)
xx_1d = np.linspace(0, 1, 1000)[:, np.newaxis]
yy_1d = my_bratley_c_1d(xx_1d)

# --- Create 2D data
my_bratley_c_2d = uqtf.BratleyC(input_dimension=2)
mesh_2d = np.meshgrid(xx_1d, xx_1d)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
yy_2d = my_bratley_c_2d(xx_2d)

# --- Create a series of plots
fig = plt.figure(figsize=(15, 5))

# 1D
axs_1 = plt.subplot(131)
axs_1.plot(xx_1d, yy_1d, color="#8da0cb")
axs_1.grid()
axs_1.set_xlabel(r"$x$", fontsize=14)
axs_1.set_ylabel(r"$\mathcal{M}(x)$", fontsize=14)
axs_1.set_title("1D BratleyC")

# Surface
axs_2 = plt.subplot(132, projection='3d')
axs_2.plot_surface(
    mesh_2d[0],
    mesh_2d[1],
    yy_2d.reshape(1000, 1000).T,
    cmap="plasma",
    linewidth=0,
    antialiased=False,
    alpha=0.5
)
axs_2.set_xlabel(r"$x_1$", fontsize=14)
axs_2.set_ylabel(r"$x_2$", fontsize=14)
axs_2.set_zlabel(r"$\mathcal{M}(x_1, x_2)$", fontsize=14)
axs_2.set_title("Surface plot of 2D BratleyC", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma"
)
axs_3.set_xlabel(r"$x_1$", fontsize=14)
axs_3.set_ylabel(r"$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D BratleyC", fontsize=14)
divider = make_axes_locatable(axs_3)
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs_3.axis('scaled')

fig.tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

## Test function instance

To create an instance of the test function with, for example,
six input dimensions, type:

```{code-cell} ipython3
my_testfun = uqtf.BratleyC(input_dimension=6)
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

In the later sections, 
the function will be illustrated using this six-dimensional instance.

## Description

The `BratleyC` function is defined as follows[^location]:

$$
\mathcal{M}(\boldsymbol{x}) = \prod_{m = 1}^M T_{n_m} (2 x_m - 1)
$$

where $T_{n_m}$ is the Chebyshev polynomial (of the first kind)
of degree $n_m$, $n_m = m \bmod 4 + 1$, and
$\boldsymbol{x} = \{ x_1, \ldots, x_M \}$
is the $M$-dimensional vector of input variables further defined below.

## Probabilistic input

Based on {cite}`Bratley1992`, the probabilistic input model for the function
consists of $M$ independent uniform random variables over $[0,1]$:

$$
X_m \sim \mathcal{U}(0,1), \quad m = 1, \ldots, M
$$

which for the current instance is shown below:

```{code-cell} ipython3
:tags: [hide-input, output_scroll]

print(my_testfun.prob_input)
```

## Reference results

This section provides several reference results of typical UQ analyses involving
the test function.

### Definite integration

The integral value of the function over the domain of $[0.0, 1.0]^M$
is analytical:

$$
I[\mathcal{M}] (M) \equiv \int_{[0, 1]^M} \mathcal{M}(\boldsymbol{x}) \; d\boldsymbol{x} = 
\begin{cases}
-\frac{1}{3}, & M = 1 \\
0,            & M \neq 1
\end{cases}.
$$

Due to the domain being a hypercube,
the above integral value over the domain is the same as the expected value.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Section 5.1, p. 207 (test function no. 3)
in {cite}`Bratley1992`.
