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

(test-functions:bratley1992a)=
# Bratley et al. (1992) A function

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The Bratley et al. (1992) A function (or `Bratley1992a` function for short),
is an $M$-dimensional scalar-valued function.
The function was introduced in {cite}`Bratley1992` as a test function
for multi-dimensional numerical integration using low discrepancy sequences.

```{note}
There are four other test functions used in Bratley et al. {cite}`Bratley1992`:

- {ref}`Bratley et al. (1992) A <test-functions:bratley1992a>`:
  A product of an absolute function (_this function_)
- {ref}`Bratley et al. (1992) B <test-functions:bratley1992b>`:
  A product of a trigonometric function
- {ref}`Bratley et al. (1992) C <test-functions:bratley1992c>`:
  A product of the Chebyshev polynomial of the first kind
- {ref}`Bratley et al. (1992) D <test-functions:bratley1992d>`:
  A sum of product
  
The function was reintroduced in {cite}`Saltelli1995` with additional
parameters for global sensitivity analysis purposes.
The "generalized" function became known as the {ref}`Sobol'-G <test-functions:sobol-g>`. 
```

The plots for one-dimensional and two-dimensional `Bratley1992a` functions
are shown below.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data
my_bratley1992a_1d = uqtf.Bratley1992a(spatial_dimension=1)
xx_1d = np.linspace(0, 1, 1000)[:, np.newaxis]
yy_1d = my_bratley1992a_1d(xx_1d)

# --- Create 2D data
my_bratley1992a_2d = uqtf.Bratley1992a(spatial_dimension=2)
mesh_2d = np.meshgrid(xx_1d, xx_1d)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
yy_2d = my_bratley1992a_2d(xx_2d)

# --- Create a series of plots
fig = plt.figure(figsize=(15, 5))

# 1D
axs_1 = plt.subplot(131)
axs_1.plot(xx_1d, yy_1d, color="#8da0cb")
axs_1.grid()
axs_1.set_xlabel("$x$", fontsize=14)
axs_1.set_ylabel("$\mathcal{M}(x)$", fontsize=14)
axs_1.set_title("1D Bratley1992a")

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
axs_2.set_xlabel("$x_1$", fontsize=14)
axs_2.set_ylabel("$x_2$", fontsize=14)
axs_2.set_zlabel("$\mathcal{M}(x_1, x_2)$", fontsize=14)
axs_2.set_title("Surface plot of 2D Bratley1992a", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma"
)
axs_3.set_xlabel("$x_1$", fontsize=14)
axs_3.set_ylabel("$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D Bratley1992a", fontsize=14)
divider = make_axes_locatable(axs_3)
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs_3.axis('scaled')

fig.tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.Bratley1992a()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

By default, the spatial dimension is set to $2$[^default_dimension].
To create an instance with another value of spatial dimension,
pass an integer to the parameter `spatial_dimension` (keyword only).
For example, to create an instance of 10-dimensional `Bratley1992a` function,
type:

```{code-cell} ipython3
my_testfun = uqtf.Bratley1992a(spatial_dimension=10)
```

## Description

The `Bratley1992a` function is defined as follows[^location]:

$$
\mathcal{M}(\boldsymbol{x}) = \prod_{m = 1}^{M} \lvert 4 x_m - 2 \rvert,
$$

where $\boldsymbol{x} = \{ x_1, \ldots, x_M \}$
is the $M$-dimensional vector of input variables further defined below.

## Probabilistic input

Based on {cite}`Bratley1992`, the test function is integrated over the 
hypercube domain of $[0, 1]^M$.
Such an input specification can be modeled using an $M$ independent uniform
random variables as shown in the table below.

| No.       |  Name    |  Distribution | Parameters | Description |
|:---------:|:--------:|:-------------:|:----------:|:-----------:|
|  1        | $x_1$    | uniform       | [0.0 1.0]  |     N/A     |
|  $\vdots$ | $\vdots$ | $\vdots$      | $\vdots$   |  $\vdots$   |
|  M        | $x_M$    | uniform       | [0.0 1.0]  |     N/A     |

## Reference results

This section provides several reference results of typical UQ analyses involving
the test function.

### Definite integration

The integral value of the function over the domain of $[0.0, 1.0]^M$
is analytical:

$$
I[\mathcal{M}] (M) \equiv \int_{[0, 1]^M} \mathcal{M}(\boldsymbol{x}) \; d\boldsymbol{x} = 1.0.
$$

### Moments

The moments of the test function are analytically known
and the first two moments are given below.

#### Expected value

Due to the domain being a hypercube,
the above integral value over the domain is the same as the expected value:

$$
\mathbb{E}[\mathcal{M}](M) = 1.0.
$$

#### Variance

The analytical value for the variance is given as follows:

$$
\mathbb{V}[\mathcal{M}](M) = \left( \frac{4}{3} \right)^M - 1 
$$

The table below shows the numerical values of the variance
for several selected dimensions.

| Dimension |      $I[\mathcal{M}]$       |
|:---------:|:---------------------------:|
|     1     | $3.3333333 \times 10^{-1}$  | 
|     2     | $7.7777778 \times 10^{-1}$  |
|     3     |  $1.3703704 \times 10^{0}$  |
|     4     |  $2.1604938 \times 10^{0}$  |
|     5     |  $3.2139918 \times 10^{0}$  |
|     6     |  $4.6186557 \times 10^{0}$  |
|     7     |  $6.4915409 \times 10^{0}$  |
|     8     |  $8.9887212 \times 10^{0}$  |
|     9     |  $1.2318295 \times 10^{1}$  |
|    10     |  $1.6757727 \times 10^{1}$  |


The variance grows as the number of dimensions and becomes unbounded
for a very large dimension.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Section 5.1, p. 207 (test function no. 1)
in {cite}`Bratley1992`.

[^default_dimension]: This default dimension applies to all variable dimension
test functions. It will be used if the `spatial_dimension` argument is not given.
