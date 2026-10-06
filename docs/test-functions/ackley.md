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

(test-functions:ackley)=
# Ackley Function

The `Ackley` function is an $M$-dimensional scalar-valued function.
Introduced by Ackley {cite}`Ackley1987` as a benchmark function for
global optimization algorithms, the function was originally presented in
two dimensions.
Bäck and Schwefel {cite}`Baeck1993` later generalized the function to higher
dimensions.
More recently, it was used as a test function for a metamodeling method
in {cite}`Kaintura2017`.

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The plots for one-dimensional and two-dimensional Ackley function
are shown below. As can be seen, the function features many local optima
with a single global optimum.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data from Ackley
my_ackley_1d = uqtf.Ackley(input_dimension=1)
xx_1d = np.linspace(-32.768, 32.768, 1000)[:, np.newaxis]
yy_1d = my_ackley_1d(xx_1d)

# --- Create 2D data from Ackley
my_ackley_2d = uqtf.Ackley(input_dimension=2)
mesh_2d = np.meshgrid(xx_1d, xx_1d)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
yy_2d = my_ackley_2d(xx_2d)

# --- Create two-dimensional plots
fig = plt.figure(figsize=(15, 5))

# 1D
axs_1 = plt.subplot(131)
axs_1.plot(xx_1d, yy_1d, color="#8da0cb")
axs_1.grid()
axs_1.set_xlabel(r"$x$", fontsize=14)
axs_1.set_ylabel(r"$\mathcal{M}(x)$", fontsize=14)
axs_1.set_title("1D Ackley")

# Surface
axs_2 = plt.subplot(132, projection='3d')
axs_2.plot_surface(
    mesh_2d[0],
    mesh_2d[1],
    yy_2d.reshape(1000,1000).T,
    linewidth=0,
    cmap="plasma",
    antialiased=False,
    alpha=0.5
)
axs_2.set_xlabel(r"$x_1$", fontsize=14)
axs_2.set_ylabel(r"$x_2$", fontsize=14)
axs_2.set_zlabel(r"$\mathcal{M}(x_1, x_2)$", fontsize=14)
axs_2.set_title("Surface plot of 2D Ackley", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma"
)
axs_3.set_xlabel("$x_1$", fontsize=14)
axs_3.set_ylabel("$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D Ackley", fontsize=14)
divider = make_axes_locatable(axs_3)
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs_3.axis('scaled')

fig.tight_layout(pad=3.0)
plt.gcf().set_dpi(75);
```

## Test function instance  
  
To create an instance of the test function with, for example,
six input dimensions, type:

```{code-cell} ipython3
my_testfun = uqtf.Ackley(input_dimension=6)
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

In the later sections, 
the function will be illustrated using this six-dimensional instance.

## Description

The generalized Ackley function according to {cite}`Baeck1993` is defined
as follows:

$$
\mathcal{M}(\boldsymbol{x}) = -a_1 \exp \left[ -a_2 \sqrt{\frac{1}{M} \sum_{m=1}^M x_m^2} \right] - \exp \left[ \frac{1}{M} \sum_{m=1}^M \cos (a_3 x_m) \right] + a_1 + e
$$

where $\boldsymbol{x} = \{ x_1, \ldots, x_M \}$ is the $M$-dimensional vector of
input variables further defined below, and
$\boldsymbol{a} = \{ a_1, a_2, a_3 \}$ are parameters of the function.

## Input

Based on {cite}`Ackley1987`, the probabilistic input model for the function
consists of $M$ independent uniform random variables over $[0,1]$:

$$
X_m \sim \mathcal{U}(-32.768, 32.768), \quad m = 1, \ldots, M
$$

which for the current instance is shown below:

```{code-cell} ipython3
:tags: [hide-input, output_scroll]

print(my_testfun.prob_input)
```

## Parameters

The Ackley function requires three additional parameters
to complete the specification.
The default values are shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.parameters)
```

## Reference results

This section provides several reference results related to the test function.

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

### Optimum values

The global optimum value of the Ackley function is
$\mathcal{M}(\boldsymbol{x}^*) = 0$ at $x_m^* = 0,\, m = 1, \ldots, M$.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
