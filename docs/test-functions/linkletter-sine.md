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

(test-functions:linkletter-sine)=
# Sine Function from Linkletter et al. (2006)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The function is a ten-dimensional, scalar-valued function.
Only the first two input variables are active, while the rest is inert.
The function was used in {cite}`Linkletter2006` to demonstrate a variable
selection method (i.e., sensitivity analysis)
in the context of Gaussian process metamodeling.

```{note}
Linkletter et al. {cite}`Linkletter2006` introduced four ten-dimensional
analytical test functions with some of the input variables inert.
They are used to demonstrate a variable selection method (i.e., screening)
in the context of Gaussian process metamodeling:

- {ref}`Linear <test-functions:linkletter-linear>` function features
  a simple function with four active input variables (out of 10).
- {ref}`Linear with decreasing coefficients <test-functions:linkletter-dec-coeffs>`
  function features a slightly more complex linear function with eight active
  input variables (out of 10).
- {ref}`Sine <test-functions:linkletter-sine>` function features only two
  active input variables (out of 10); the effect of the two inputs on
  the output, however, is very different. (_this function_).
```

Because the function is effectively two dimensional, the surface and contour
plots are shown below.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

my_fun = uqtf.LinkletterSine()

# --- Create 2D data
xx_1d = np.linspace(0.0, 1.0, 1000)[:, np.newaxis]
mesh_2d = np.meshgrid(xx_1d, xx_1d)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
xx = my_fun.prob_input.get_sample(len(xx_2d))
xx[:,:2] = xx_2d
yy_2d = my_fun(xx)

# --- Create two-dimensional plots
fig = plt.figure(figsize=(10, 5))

# Surface
axs_1 = plt.subplot(121, projection='3d')
axs_1.plot_surface(
    mesh_2d[0],
    mesh_2d[1],
    yy_2d.reshape(1000,1000).T,
    linewidth=0,
    cmap="plasma",
    antialiased=False,
    alpha=0.5
)
axs_1.set_xlabel("$x_1$", fontsize=14)
axs_1.set_ylabel("$x_2$", fontsize=14)
axs_1.set_zlabel("$\mathcal{M}(x_1, x_2)$", fontsize=14)
axs_1.set_title("Surface plot of LinkletterSine", fontsize=14)

# Contour
axs_2 = plt.subplot(122)
cf = axs_2.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma", levels=10,
)
axs_2.set_xlabel("$x_1$", fontsize=14)
axs_2.set_ylabel("$x_2$", fontsize=14)
axs_2.set_title("Contour plot of LinkletterSine", fontsize=14)
divider = make_axes_locatable(axs_2)
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs_2.axis('scaled')

fig.tight_layout(pad=4.0)
plt.gcf().set_dpi(75);
```


## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.LinkletterSine()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The test function is defined as[^location]:

$$
\mathcal{M}(\boldsymbol{x}) = \sin{(x_1)} + \sin{(5 x_2)},
$$

where $\boldsymbol{x} = \left( x_1, \ldots x_{10} \right)$
is the ten-dimensional vector of input variables further defined below.
Notice that only two out of ten input variables are active.

```{note}
In the original paper, the function was added with an independent identically
distributed (i.i.d) noise from $\mathcal{N}(0, \sigma)$
with a standard deviation $\sigma = 0.05$.

Furthermore, also in the original paper, a batch of data is generated from
the function and then standardized to have mean $0.0$ and standard deviation
$1.0$.

The implementation of UQTestFuns does not include any error addition
or standardization. However, these processes can be done manually
after the data is generated.
```

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

[^location]: see Eq. (7), Example 3, in {cite}`Linkletter2006`.
