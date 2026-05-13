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

(test-functions:genz-oscillatory)=
# Oscillatory Function from Genz (1984)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The Genz oscillatory function (or `GenzOscillatory` for short)
is an $M$-dimensional scalar-valued function featuring
an oscillating cosine shape across the input domain.

It is one of six functions introduced by Genz {cite}`Genz1984`;
see the note below.

The plots for one-dimensional and two-dimensional Genz oscillatory function
with the default parameters can be seen below.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data from Genz Oscillatory
my_fun_1d = uqtf.GenzOscillatory(input_dimension=1)
xx_1d = np.linspace(0, 1, 1000)[:, np.newaxis]
yy_1d = my_fun_1d(xx_1d)

# --- Create 2D data from Genz Oscillatory
my_fun_2d = uqtf.GenzOscillatory(input_dimension=2)
mesh_2d = np.meshgrid(xx_1d, xx_1d)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
yy_2d = my_fun_2d(xx_2d)

# --- Create two-dimensional plots
fig = plt.figure(figsize=(15, 5))

# 1D
axs_1 = plt.subplot(131)
axs_1.plot(xx_1d, yy_1d, color="#8da0cb")
axs_1.grid()
axs_1.set_xlabel(r"$x$", fontsize=14)
axs_1.set_ylabel(r"$\mathcal{M}(x)$", fontsize=14)
axs_1.set_title("1D Genz oscillatory")

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
axs_2.set_title("Surface plot of 2D Genz oscillatory", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma"
)
axs_3.set_xlabel(r"$x_1$", fontsize=14)
axs_3.set_ylabel(r"$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D Genz oscillatory", fontsize=14)
divider = make_axes_locatable(axs_3)
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs_3.axis('scaled')

fig.tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

```{note}
Genz {cite}`Genz1984` introduced six challenging
parameterized $M$-dimensional functions
designed to test the performance of numerical integration routines:

- {ref}`Oscillatory <test-functions:genz-oscillatory>` function features
  an oscillating shape in the multidimensional space. (_this function_)
- {ref}`Product peak <test-functions:genz-product-peak>` function features
  a prominent peak at the center of the multidimensional space.
- {ref}`Corner peak <test-functions:genz-corner-peak>` function features
  a prominent peak in one corner of the multidimensional space.
- {ref}`Gaussian <test-functions:genz-gaussian>` function features
  a bell-shaped peak at the center of the multidimensional space.
- {ref}`Continuous <test-functions:genz-continuous>` function features
  an exponential decay from the center of the multidimensional space.
  The function is continuous everywhere, but non-differentiable at the center.
- {ref}`Discontinuous <test-functions:genz-discontinuous>` function features
  an exponential rise from a corner of the multidimensional space up to the
  offset parameter value, after which the function value drops to zero
  everywhere, creating discontinuity.

The functions are further characterized by offset (shift) and shape parameters.
While the offset parameter has minimal impact on the integral's value,
the shape parameter significantly affects
the difficulty of the integration problem.
```

## Test function instance

To create an instance of the test function with, for example,
six input dimensions, type:

```{code-cell} ipython3
my_testfun = uqtf.GenzOscillatory(input_dimension=6)
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

In the later sections, 
the function will be illustrated using this six-dimensional instance.

## Description

The Genz oscillatory function is defined as:

$$
\mathcal{M}(\boldsymbol{x}; \boldsymbol{a}, b) = \cos{\left(2 \pi b + \sum_{i = 1}^M a_i x_i \right)},
$$

where $\boldsymbol{x} = \left( x_1, \ldots, x_M \right)$
is the $M$-dimensional vector of input variables;
$\boldsymbol{a} = \left( a_1, \ldots, a_M \right)$ 
is $M$-dimensional vector corresponding to the (fixed) shape and parameters;
and $b$ is the scalar offset parameter.
Further details about these parameters are provided below.

## Probabilistic input

Based on {cite}`Genz1984`, the probabilistic input model for the function
consists of $M$ independent uniform random variables over $[0,1]$:

$$
X_m \sim \mathcal{U}(0,1), \quad m = 1, \ldots, M
$$

which for the current instance is shown below:

```{code-cell} ipython3
:tags: [hide-input, output_scroll]

print(my_testfun.prob_input)
```

## Parameters

The parameters of the Genz Gaussian function consist
of the vector of shape (scale) parameters $\boldsymbol{a}$
and the scalar of offset parameter $b$. 

The shape parameters control the frequency of oscillation;
larger values produce more rapid oscillation
and make integration more challenging.
The offset parameter, on the other hand, does not significantly affect
the difficulty of the problem and can be chosen randomly.

The default parameter is shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.parameters)
```

## Reference results

This section provides several reference results of typical UQ analyses
involving the test function.

### Sample histogram

Shown below is the histogram of the output based on $100'000$ random points:

```{code-cell} ipython3
:tags: [hide-input]

yy_test = my_testfun.get_sample(100000)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel(r"$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

## References

```{bibliography}
:filter: docname in docnames
```
