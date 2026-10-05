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

(test-functions:morris2006)=
# Sensitivity Test Function from Morris et al. (2006)

The `MorrisM` function is an $M$-dimensional scalar-valued function
used in the context of sensitivity analysis
{cite}`Morris2006, Horiguchi2021, Sun2022`.
It features a parameter that controls the number of active input variables;
any remaining variables are inert.
The Sobol' main-effect and total-effect indices are equal
for each active variable,
making the function well-suited for benchmarking sensitivity analysis methods.

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The plots for the one-dimensional and two-dimensional `MorrisM` function
can be seen below.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data
my_fun_1d = uqtf.MorrisM(input_dimension=1)
xx_1d = np.linspace(0, 1, 1000)[:, np.newaxis]
yy_1d = my_fun_1d(xx_1d)

# --- Create 2D data
my_fun_2d = uqtf.MorrisM(input_dimension=2)
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
axs_1.set_title("1D MorrisM")

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
axs_2.set_title("Surface plot of 2D MorrisM", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma"
)
axs_3.set_xlabel(r"$x_1$", fontsize=14)
axs_3.set_ylabel(r"$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D MorrisM", fontsize=14)
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
my_testfun = uqtf.MorrisM(input_dimension=6)
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

In the later sections, 
the function will be illustrated using this six-dimensional instance.

```{note}
The function originally appeared in {cite}`Morris2006` in 30 dimensions;
to reproduce that setting, pass `input_dimension=30`.
```

## Description

The `Morris2006` function is defined as follows[^location]:

$$
\mathcal{M}(\boldsymbol{x}; p) = \alpha(p) \sum_{i = 1}^p x_i + \beta(p) \sum_{i = 1}^{p - 1} x_i \left( \sum_{j = i + 1}^p x_j \right),
$$
where

$$
\alpha(p) = \sqrt{12} - 6 \sqrt{0.1 (p - 1)}
$$

and

$$
\beta(p) = \frac{12}{\sqrt{10 (p - 1)}}.
$$

where $\boldsymbol{x} = \{ x_1, \ldots, x_M \}$ is the $M$-dimensional vector
of input variables further defined below,
and $p$ is the parameter of the function.

```{important}
The original formula for $\beta$ in {cite}`Morris2006` contains an error.
The formula given, $12 \sqrt{0.1} \sqrt{p - 1}$, fails to meet the specified
condition for the function, where the products of the main-effect
and total-effect indices with the variance should yield values $1.0$ and $1.1$,
respectively.
```

## Probabilistic input

Based on {cite}`Morris2006`, the probabilistic input model for the function
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

The parameter $p$ of the test function controls the number of important input
variables; if this number is larger than the actual number of input dimensions,
then all input variables are deemed important.

The default parameter is shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.parameters)
```

```{note}
If $p \geq M$, all $M$ input variables are active and none are inert.
The parameter $p$ is most meaningful when $p < M$; choosing $p \geq M$
reduces the function to a sum with no inert variables, which defeats
its purpose as a variable-screening test function.
In the original paper {cite}`Morris2006`, $p$ was varied from $1$ to $10$
with $M = 30$, ensuring $p < M$ throughout.
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

### Sensitivity indices

The values of $p$, $\alpha$ ,and $\beta$ in the above equation are chosen
such that the following conditions are satisfied:

$$
\begin{aligned}
S_i \times \mathbb{V}[Y]  & = 1.0, & i & = 1, \ldots, p, \\
S_i                       & = 0.0, & i &  = p + 1, \ldots, M,
\end{aligned}
$$

and

$$
\begin{aligned}
ST_i \times \mathbb{V}[Y] & = 1.1 & i & = 1, \ldots, p, \\
ST_i & = 0.0, & i & = p + 1, \ldots, M,
\end{aligned}
$$

where $S_i$ and $ST_i$ are the main-effect and total-effect indices for $i$-th
input variable; and $\mathbb{V}[Y]$ is the output variance.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Section 4, p. 3213 in {cite}`Morris2006`.
