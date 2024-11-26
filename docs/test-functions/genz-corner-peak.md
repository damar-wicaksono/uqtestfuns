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

(test-functions:genz-corner-peak)=
# Genz Corner Peak Function

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The Genz corner peak function is an $M$-dimensional, scalar-valued
function.
The function was introduced in {cite}`Genz1984` to assess the accuracy
of numerical integration routines.
The function was featured in {cite}`Zhang2014` as a test function
for a global sensitivity analysis method.

```{note}
Genz {cite}`Genz1984` introduced six challenging
parameterized $M$-dimensional functions
designed to test the performance of numerical integration routines:

- {ref}`Corner peak <test-functions:genz-corner-peak>` features a prominent
  peak in one corner of the multidimensional space. (_this function_)

The functions are further characterized by shift and scale parameters.
While the shift parameter has minimal impact on the integral's value,
the scale parameter significantly affects
the difficulty of the integration problem.
```

The plots for one-dimensional and two-dimensional Genz corner peak function
with the default parameters can be seen below.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data from Genz Corner Peak
my_fun_1d = uqtf.GenzCornerPeak(input_dimension=1)
xx_1d = np.linspace(0, 1, 1000)[:, np.newaxis]
yy_1d = my_fun_1d(xx_1d)

# --- Create 2D data from Genz Corner Peak
my_fun_2d = uqtf.GenzCornerPeak(input_dimension=2)
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
axs_1.set_title("1D Genz corner peak")

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
axs_2.set_title("Surface plot of 2D Genz corner peak", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma"
)
axs_3.set_xlabel("$x_1$", fontsize=14)
axs_3.set_ylabel("$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D Genz corner peak", fontsize=14)
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
my_testfun = uqtf.GenzCornerPeak()
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
my_testfun = uqtf.GenzCornerPeak(input_dimension=6)
```

## Description

The Genz corner peak function as follows:

$$
\mathcal{M}(\boldsymbol{x}; \boldsymbol{a}) = \left( 1 + \sum_{i = 1}^{M} a_i x_i \right)^{-(M + 1)}
$$
where $\boldsymbol{x} = \left( x_1, \ldots, x_M \right)$
is the $M$-dimensional vector of input variables
and $\boldsymbol{a} = \left( a_1, \ldots, a_M \right)$ is the $M$-dimensional
vector of (fixed) scale parameters.
Further details about these parameters are provided below.

## Probabilistic input

The input specification for the Genz corner peak function is shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

## Parameters

The parameters of the Genz corner peak function consists
of the vector of scale parameters $\boldsymbol{a}$,
which determine the extent of the corner peaking.
Larger values of $\boldsymbol{a}$
increase the prominence of the peak,
making the integration problem more challenging.

The available parameters for the Genz corner peak function
are shown in the table below.

```{table} Available parameters of the Genz corner peak function
:name: genz-corner-peak-parameters

```
| No. |                    $\boldsymbol{a}$                    |          Keyword          |             Source              |          Remark           |
|:---:|:------------------------------------------------------:|:-------------------------:|:-------------------------------:|:-------------------------:|
| 1.  |                $a_1 = \ldots = a_M = 5$                | `Genz1984` <br> (default) |        {cite}`Genz1984`         |            ---            |
| 2.  | $a_i = 0.02 + 0.03 \times (i - 1),\, i = 1, \ldots, M$ |       `Zhang2014-1`       | {cite}`Zhang2014` (Section 4.4) | Originally, 3 dimensions  |
| 3.  |       $a_i = 0.01 \times i,\, i = 1, \ldots, M$        |       `Zhang2014-2`       | {cite}`Zhang2014` (Section 4.4) | Originally, 10 dimensions |

The default parameter is shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.parameters)
```

````{note}
To create an instance of the Genz corner peak function with different built-in
parameter values, pass the corresponding keyword to the parameter `parameters_id`.
For example, to use the parameters from {cite}`Zhang2014`,
type:

```python
my_testfun = uqtf.GenzCornerPeak(parameters_id="Zhang2014-1")
```
````

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

plt.hist(yy_test, color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

Notice that the values are indeed mostly zeros.

## References

```{bibliography}
:filter: docname in docnames
```

[^default_dimension]: This default dimension applies to all variable dimension
test functions. It will be used if the `input_dimension` argument is not given.