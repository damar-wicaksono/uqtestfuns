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

(test-functions:bratley1992b)=
# Bratley et al. (1992) B function

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The Bratley et al. (1992) B function (or `Bratley1992b` function for short),
is an $M$-dimensional scalar-valued function.
The function was introduced in {cite}`Bratley1992` as a test function
for multi-dimensional numerical integration using low discrepancy sequences.

```{note}
There are four other test functions used in Bratley et al. {cite}`Bratley1992`:

- {ref}`Bratley et al. (1992) B <test-functions:bratley1992b>`:
  A product of trigonometric function (_this function_)
- {ref}`Bratley et al. (1992) D <test-functions:bratley1992d>`:
  A sum of product
```

The plots for one-dimensional and two-dimensional `Bratley1992b` functions
are shown below.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data
my_bratley1992b_1d = uqtf.Bratley1992b(spatial_dimension=1)
xx_1d = np.linspace(0, 1, 1000)[:, np.newaxis]
yy_1d = my_bratley1992b_1d(xx_1d)

# --- Create 2D data
my_bratley1992b_2d = uqtf.Bratley1992b(spatial_dimension=2)
mesh_2d = np.meshgrid(xx_1d, xx_1d)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
yy_2d = my_bratley1992b_2d(xx_2d)

# --- Create a series of plots
fig = plt.figure(figsize=(15, 5))

# 1D
axs_1 = plt.subplot(131)
axs_1.plot(xx_1d, yy_1d, color="#8da0cb")
axs_1.grid()
axs_1.set_xlabel("$x$", fontsize=14)
axs_1.set_ylabel("$\mathcal{M}(x)$", fontsize=14)
axs_1.set_title("1D Bratley1992b")

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
axs_2.set_title("Surface plot of 2D Bratley1992b", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma"
)
axs_3.set_xlabel("$x_1$", fontsize=14)
axs_3.set_ylabel("$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D Bratley1992b", fontsize=14)
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
my_testfun = uqtf.Bratley1992b()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

By default, the spatial dimension is set to $2$[^default_dimension].
To create an instance with another value of spatial dimension,
pass an integer to the parameter `spatial_dimension` (keyword only).
For example, to create an instance of 10-dimensional `Bratley1992b` function,
type:

```{code-cell} ipython3
my_testfun = uqtf.Bratley1992b(spatial_dimension=10)
```

## Description

The `Bratley1992b` function is defined as follows[^location]:

$$
\mathcal{M}(\boldsymbol{x}) = \prod_{m = 1}^{M} m \cos{(m x)},
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
I[\mathcal{M}] (M) \equiv \int_{[0, 1]^M} \mathcal{M}(\boldsymbol{x}) \; d\boldsymbol{x} = \prod_{m = 1}^M \sin{(m)}.
$$

The table below shows the numerical values of the integral
for several selected dimensions.

| Dimension |      $I[\mathcal{M}]$       |
|:---------:|:---------------------------:|
|     1     | $8.4147098 \times 10^{-1}$  |
|     2     | $7.6514740 \times 10^{-1}$  |
|     3     | $1.0797761 \times 10^{-1}$  |
|     4     | $-8.1717723 \times 10^{-2}$ |
|     5     | $7.8361108 \times 10^{-2}$  |
|     6     | $-2.1895308 \times 10^{-2}$ |
|     7     | $-1.4384924 \times 10^{-2}$ |
|     8     | $-1.4231843 \times 10^{-2}$ |
|     9     | $-5.8652056 \times 10^{-3}$ |
|    10     | $3.1907957 \times 10^{-3}$  |

The absolute value of the integral is monotonically decreasing function
of the number of dimensions. Asymptotically, it is zero.
In the original paper of Bratley {cite}`Bratley1992`, the integration was
carried out for the function in dimension eight.

### Moments

The moments of the test function are analytically known
and the first two moments are given below.

#### Expected value

Due to the domain being a hypercube,
the above integral value over the domain is the same as the expected value:

$$
\mathbb{E}[\mathcal{M}](M) = \prod_{m = 1}^M \sin{(m)}.
$$

#### Variance

The analytical value for the variance is given as follows:

$$
\mathbb{V}[\mathcal{M}](M) = \frac{1}{4} \prod_{m = 1}^M m (2 m + \sin{(2m)}) - \left( \prod_{m = 1}^M \sin{m} \right)^2.
$$

The table below shows the numerical values of the variance
for several selected dimensions.

| Dimension |      $I[\mathcal{M}]$      |
|:---------:|:--------------------------:|
|     1     | $1.9250938 \times 10^{-2}$ | 
|     2     | $5.9397772 \times 10^{-1}$ |
|     3     | $5.0486051 \times 10^{0}$  |
|     4     | $4.5481851 \times 10^{1}$  |
|     5     | $5.3766707 \times 10^{2}$  |
|     6     |  $9.245366 \times 10^{3}$  |
|     7     | $2.4253890 \times 10^{5}$  |
|     8     | $7.6215893 \times 10^{6}$  |
|     9     | $2.9579601 \times 10^{8}$  |
|    10     | $1.5464914 \times 10^{10}$ |

The variance grows as the number of dimensions and becomes unbounded
for a very large dimension.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Section 5.1, p. 207 (test function no. 2)
in {cite}`Bratley1992`.

[^default_dimension]: This default dimension applies to all variable dimension
test functions. It will be used if the `spatial_dimension` argument is not given.
