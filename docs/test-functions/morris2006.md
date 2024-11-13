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
# Test Function from Morris et al. (2006)

The test function from Morris et al. (2006) {cite}`Morris2006`
(or  `Morris2006` for short) is an $M$-dimensional scalar-valued function used
in the context of sensitivity analysis
{cite}`Morris2006, Horiguchi2021, Sun2022`.

The function features a parameter that controls the number of important input
variables; the remaining variables, if any, are inert. Furthermore, the Sobol'
main-effect and total-effect sensitivity indices are the same for each input
variable.

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The plots for one-dimensional and two-dimensional `Morris2006` function
can be seen below.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data
my_fun_1d = uqtf.Morris2006(input_dimension=1)
xx_1d = np.linspace(0, 1, 1000)[:, np.newaxis]
yy_1d = my_fun_1d(xx_1d)

# --- Create 2D data
my_fun_2d = uqtf.Morris2006(input_dimension=2)
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
axs_1.set_title("1D Morris2006")

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
axs_2.set_title("Surface plot of 2D Morris2006", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma"
)
axs_3.set_xlabel("$x_1$", fontsize=14)
axs_3.set_ylabel("$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D Morris2006", fontsize=14)
divider = make_axes_locatable(axs_3)
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')
axs_3.axis('scaled')

fig.tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

## Test function instance

To create a default instance of the function, type:

```{code-cell} ipython3
my_testfun = uqtf.Morris2006()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

By default, the input dimension is set to $2$[^default_dimension].
To create an instance with another value of input dimension,
pass an integer to the parameter `input_dimension` (the first parameter).
For example, to create an instance of the function in 30 dimensions,
type:

```{code-cell} ipython3
my_testfun = uqtf.Morris2006(input_dimension=30)
```

In the subsequent section, the function will be illustrated
using 30 dimensions as it originally appeared in {cite}`Morris2006`.

## Description

The `Morris2006` function is defined as follows[^location]:

$$
\mathcal{M}(\boldsymbol{x}; p) = \alpha(p) \sum_{i = 1}^p x_p + \beta(p) \sum_{i = 1}^{p - 1} x_i \left( \sum_{j = i + 1}^p x_j \right),
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

The probabilistic input model for the `Morris2006` function consists of $M$
independent uniform random variables in $[0.0, 1.0]^M$. 

For the selected input dimension, the input model is shown below.

```{code-cell} ipython3
:tags: [hide-input, "output_scroll"]

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

````{note}
You can replace the default value of the parameter by assigning a new value
to it as follows:

```python
my_testfun.parameters["p"] = 5
```
````

## Reference results

This section provides several reference results of typical UQ analyses
involving the test function.

### Sample histogram

Shown below is the histogram of the output based on $100'000$ random points:

```{code-cell} ipython3
:tags: [hide-input]

np.random.seed(42)
xx_test = my_testfun.prob_input.get_sample(100000)
yy_test = my_testfun(xx_test)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

### Sensitivity indices

The values of $p$, $\alpha$ ,and $\beta$ in the above equation are chosen
such that the following conditions are satisfied:

$$
\begin{aligned}
S_i \times \mathbb{V}[Y]  & = 1.0, & i = 1, \ldots, p \\
S_i & = 0.0, & i = p + 1, \ldots, M,
\end{aligned}
$$

and

$$
\begin{aligned}
ST_i \times \mathbb{V}[Y] & = 1.1 & i = 1, \ldots, p \\
ST_i & = 0.0, & i = p + 1, \ldots, M,
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

[^default_dimension]: This default dimension applies to all variable dimension
test functions. It will be used if the `input_dimension` argument is not given.
