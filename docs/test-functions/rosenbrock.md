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

(test-functions:rosenbrock)=
# Generalized Rosenbrock Function

The Rosenbrock function (`Rosenbrock`) was originally introduced
in {cite}`Rosenbrock1960` as a two-dimensional scalar-valued test function
for global optimization and later generalized to $M$ dimensions,
making it a widely used benchmark (e.g., {cite}`Dixon1978, Picheny2013`).
Also known as the valley or banana function,
it features a curved, non-convex valley that is easy to reach
but challenging to converge within.
In {cite}`Tan2015`, it was used in a metamodeling exercise.

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The one-dimensional plot as well as the surface and contour plots
for the two-dimensional Rosenbrock function are shown below
for the default parameter set and for $x \in [-2, 2] \times [-1, 3]$.

As shown, the function features a curved, non-convex valley.
While it is relatively easy to reach the valley, the convergence to the global
minimum is challenging.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data
my_fun_1d = uqtf.Rosenbrock(input_dimension=1)
lb = my_fun_1d.prob_input.marginals[0].lower
ub = my_fun_1d.prob_input.marginals[0].upper
xx_1d = np.linspace(lb, ub, 1000)[:, np.newaxis]
yy_1d = my_fun_1d(xx_1d)

# --- Create 2D data
x1_1d = np.arange(-2, 2, 0.05)
x2_1d = np.arange(-1, 3, 0.05)
my_fun = uqtf.Rosenbrock(input_dimension=2)
mesh_2d = np.meshgrid(x1_1d, x2_1d)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)
yy_2d = my_fun(xx_2d)

# --- Create two-dimensional plots
fig = plt.figure(figsize=(15, 5))

# 1D
axs_1 = plt.subplot(131)
axs_1.plot(xx_1d, yy_1d, color="#8da0cb")
axs_1.grid()
axs_1.set_xlabel(r"$x$", fontsize=14)
axs_1.set_ylabel(r"$\mathcal{M}(x)$", fontsize=14)
axs_1.set_title("1D Rosenbrock")

# Surface
axs_2 = plt.subplot(132, projection='3d')
axs_2.plot_surface(
    mesh_2d[0],
    mesh_2d[1],
    yy_2d.reshape(len(x1_1d), len(x2_1d)).T,
    linewidth=0,
    cmap="plasma",
    antialiased=False,
    alpha=0.5
)
axs_2.set_xlabel(r"$x_1$", fontsize=14)
axs_2.set_ylabel(r"$x_2$", fontsize=14)
axs_2.set_title("Surface plot of 2D Rosenbrock", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contour(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(len(x1_1d), len(x2_1d)).T,
    levels=1000, cmap="plasma",
)
axs_3.set_xlabel(r"$x_1$", fontsize=14)
axs_3.set_ylabel(r"$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D Rosenbrock", fontsize=14)
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
my_testfun = uqtf.Rosenbrock(input_dimension=6)
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

In the later sections, 
the function will be illustrated using this six-dimensional instance.

## Description

The Rosenbrock function is defined as follows:

$$
\mathcal{M}(\boldsymbol{x}; \boldsymbol{p}) = \frac{1}{d} \left[ 
\left( \sum_{i = 1}^{M - 1} (x_i - a)^2 + b \, (x_{i + 1} - x_i^2)^2 \right) 
- c \right]
$$

where $\boldsymbol{x} = \{ x_1, \ldots, x_M \}$ is the $M$-dimensional vector
of input variables further defined below,
and $\boldsymbol{p} = \{ a, b, c, d \}$ is the set of parameters
also defined further below.

```{note}
The canonical Rosenbrock function is defined for $M \geq 2$[^location].
For $M = 1$, the sum above is empty by convention;
the function instead reduces to $\frac{1}{d} \left( (x_1 - a)^2 - c \right)$.
This convention is adopted in this implementation for completeness.
```

## Input

The Rosenbrock function is defined on $\mathbb{R}^M$, but in the context
of the optimization test function, the search space is often limited as shown
in the table below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

## Parameters

The Rosenbrock function requires four additional parameters
to complete the specification. The default values are shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.parameters)
```

The parameter $a$ controls the location and value of the global optimum.
The parameter $b$ controls the steepness and width of the valley.
In particular, it determines the variation scale of the function;
large value of $b$ creates a steeper and tight valley.

The parameters $c$ and $d$ are used to shift and scale the function such that
its mean and standard deviation become $0.0$ and $1.0$, respectively.

Below are some contour plots of the function in two dimensions with different
values of $a$ and $b$ along with the location of the global optimum.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable
from uqtestfuns.core.parameters import Parameters

# --- Create 2D data
x1_1d = np.arange(-2, 2, 0.05)
x2_1d = np.arange(-1, 3, 0.05)
mesh_2d = np.meshgrid(x1_1d, x2_1d)
xx_2d = np.array(mesh_2d).T.reshape(-1, 2)

# --- Create contour plots
fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# a = 1.0, b = 100.0
my_fun = uqtf.Rosenbrock(input_dimension=2)
yy_2d = my_fun(xx_2d)
a = my_fun.parameters["a"]
b = my_fun.parameters["b"]

cf = axs[0, 0].contour(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(len(x1_1d), len(x2_1d)).T,
    levels=1000, cmap="plasma",
)
axs[0, 0].set_xlabel("$x_1$", fontsize=14)
axs[0, 0].set_ylabel("$x_2$", fontsize=14)
axs[0, 0].set_title(f"a = {a}, b = {b}", fontsize=14)
divider = make_axes_locatable(axs[0, 0])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs[0, 0].axis('scaled')

axs[0, 0].scatter(a, a**2, marker="x", s=150, color="k")

# a = 1.6, b = 100.0
my_fun = uqtf.Rosenbrock(input_dimension=2)
params_ = {**my_fun.parameters}
params_["a"] = 1.6
my_fun._parameters = Parameters(params_)
yy_2d = my_fun(xx_2d)
a = my_fun.parameters["a"]
b = my_fun.parameters["b"]

cf = axs[0, 1].contour(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(len(x1_1d), len(x2_1d)).T,
    levels=1000, cmap="plasma",
)
axs[0, 1].set_xlabel("$x_1$", fontsize=14)
axs[0, 1].set_ylabel("$x_2$", fontsize=14)
axs[0, 1].set_title(f"a = {a}, b = {b}", fontsize=14)
divider = make_axes_locatable(axs[0, 1])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs[0, 1].axis('scaled')

axs[0, 1].scatter(a, a**2, marker="x", s=150, color="k")

# a = 1.0, b = 500.0
my_fun = uqtf.Rosenbrock(input_dimension=2)
params_ = {**my_fun.parameters}
params_["b"] = 500.0
my_fun._parameters = Parameters(params_)
yy_2d = my_fun(xx_2d)
a = my_fun.parameters["a"]
b = my_fun.parameters["b"]

cf = axs[1, 0].contour(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(len(x1_1d), len(x2_1d)).T,
    levels=1000, cmap="plasma",
)
axs[1, 0].set_xlabel("$x_1$", fontsize=14)
axs[1, 0].set_ylabel("$x_2$", fontsize=14)
axs[1, 0].set_title(f"a = {a}, b = {b}", fontsize=14)
divider = make_axes_locatable(axs[1, 0])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs[1, 0].axis('scaled')

axs[1, 0].scatter(a, a**2, marker="x", s=150, color="k")

# a = 1.6, b = 500.0
my_fun = uqtf.Rosenbrock(input_dimension=2)
params_ = {**my_fun.parameters}
params_["a"] = 1.6
params_["b"] = 500.0
my_fun._parameters = Parameters(params_)
yy_2d = my_fun(xx_2d)
a = my_fun.parameters["a"]
b = my_fun.parameters["b"]

cf = axs[1, 1].contour(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(len(x1_1d), len(x2_1d)).T,
    levels=1000, cmap="plasma",
)
axs[1, 1].set_xlabel("$x_1$", fontsize=14)
axs[1, 1].set_ylabel("$x_2$", fontsize=14)
axs[1, 1].set_title(f"a = {a}, b = {b}", fontsize=14)
divider = make_axes_locatable(axs[1, 1])
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs[1, 1].axis('scaled')

axs[1, 1].scatter(a, a**2, marker="x", s=150, color="k")

fig.tight_layout()
plt.gcf().set_dpi(75);
```

Changing the value of $a$ shifts the location of the global optimum
(and in $M > 2$ also its value).
Changing $b$ modifies the scale of the function variation
and the steepness of the valley (see the color bars).

## Reference results

This section provides several reference results related to the test function.

### Optimum values

The global optimum of the Rosenbrock function is located at

$$
\begin{aligned}
\boldsymbol{x}^* & = \left( x^*_1, \ldots, x^*_M \right), \\
x_i^* & = a^{2^{i - 1}}.
\end{aligned}
$$

In dimension two, the function value at the optimum location is always $0.0$
(but not in higher dimension!).

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: The original two-dimensional expression can be found in Eq. (10),
Section 3.2, in {cite}`Rosenbrock1960`.
