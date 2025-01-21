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

(test-functions:genz-product-peak)=
# Genz Product Peak Function

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The Genz product peak function is an $M$-dimensional scalar-valued
function commonly used to assess the accuracy of numerical
integration routines.
It is one of six functions introduced by Genz {cite}`Genz1984`;
see the box below.

The function features a peak at the center of the multidimensional space.
The plots for one-dimensional and two-dimensional Genz product peak function
with the default parameters can be seen below.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data from Genz Product Peak
my_fun_1d = uqtf.GenzProductPeak(input_dimension=1)
xx_1d = np.linspace(0, 1, 1000)[:, np.newaxis]
yy_1d = my_fun_1d(xx_1d)

# --- Create 2D data from Genz Product Peak
my_fun_2d = uqtf.GenzProductPeak(input_dimension=2)
mesh_2d = np.meshgrid(xx_1d, xx_1d)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
yy_2d = my_fun_2d(xx_2d)

# --- Create two-dimensional plots
fig = plt.figure(figsize=(15, 5))

# 1D
axs_1 = plt.subplot(131)
axs_1.plot(xx_1d, yy_1d, color="#8da0cb")
axs_1.grid()
axs_1.set_xlabel("$x$", fontsize=14)
axs_1.set_ylabel("$\mathcal{M}(x)$", fontsize=14)
axs_1.set_title("1D Genz product peak")

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
axs_2.set_title("Surface plot of 2D Genz product peak", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma"
)
axs_3.set_xlabel("$x_1$", fontsize=14)
axs_3.set_ylabel("$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D Genz product peak", fontsize=14)
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
  an oscillating shape in the multidimensional space.
- {ref}`Product peak <test-functions:genz-product-peak>` function features
  a prominent peak at the center of the multidimensional space.
  (_this function_)
- {ref}`Corner peak <test-functions:genz-corner-peak>` function features
  a prominent peak in one corner of the multidimensional space.
- {ref}`Gaussian <test-functions:genz-gaussian>` function features
  a bell-shaped peak at the center of the multidimensional space.
- {ref}`Continuous <test-functions:genz-continuous>` function features
  an exponential decay from the center of the multidimensional space.
  The function is continuous everywhere, but non-differentiable at the center.
- {ref}`Discontinuous <test-functions:genz-discontinuous>` function features
  an exponential rise from corner of the multidimensional space up to the
  offset parameter value, after which the function value drops to zero
  everywhere, creating discontinuity.
The functions are further characterized by offset (shift) and shape parameters.
While the offset parameter has minimal impact on the integral's value,
the shape parameter significantly affects
the difficulty of the integration problem.
```

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.GenzProductPeak()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

By default, the input dimension is set to $2$[^default_dimension].
To create an instance with another value of input dimension,
pass an integer to the parameter `input_dimension` (the first parameter).
For example, to create an instance of the test function in six dimensions,
type:

```python
my_testfun = uqtf.GenzProductPeak(input_dimension=6)
```

## Description

The Genz product peak function is defined as:

$$
\mathcal{M}(\boldsymbol{x}; \boldsymbol{a}, \boldsymbol{b}) = \prod_{i = 1}^M \frac{1}{\left( a_i^{-2} + (x_i - b_i)^2 \right)}
$$

where $\boldsymbol{x} = \left( x_1, \ldots, x_M \right)$
is the $M$-dimensional vector of input variables;
and $\boldsymbol{a} = \left( a_1, \ldots, a_M \right)$ 
$\boldsymbol{b} = \left( b_1, \ldots, b_M \right)$ are $M$-dimensional
vectors corresponding to the (fixed) shape and offset parameters, respectively.
Further details about these parameters are provided below.

## Probabilistic input

The input specification for the Genz product peak function is shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

## Parameters

The parameters of the Genz corner peak function consists
of the vector of shape parameters $\boldsymbol{a}$
and the vector of offset parameters $\boldsymbol{b}$. 

The shape parameters determines the extent of the product peaking;
Larger values of $\boldsymbol{a}$
increase the prominence of the peak,
making the integration problem more challenging.
The offset parameters, on the other hand, do not affect significantly
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

my_testfun.prob_input.reset_rng(42)
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

[^default_dimension]: This default dimension applies to all variable dimension
test functions. It will be used if the `input_dimension` argument is not given.