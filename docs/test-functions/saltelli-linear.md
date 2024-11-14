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

(test-functions:saltelli-linear)=
# Saltelli Linear Function

The Saltelli Linear function is an $M$-dimensional scalar-valued function.
It was introduced in {cite}`Saltelli2008` for illustrating sensitivity
analysis methods.
It is later used in {cite}`Sun2022` for benchmarking various sensitivity
analysis methods.

Due to its simple form, the moments and Sobol' sensitivity indices may be
computed analytically.

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The plots for one-dimensional and two-dimensional Sobol'-G function can be seen
below.

```{code-cell} ipython3
:tags: [remove-input]

from mpl_toolkits.axes_grid1 import make_axes_locatable

# --- Create 1D data from SaltelliLinear
my_fun_1d = uqtf.SaltelliLinear(input_dimension=1)
lb = my_fun_1d.prob_input.marginals[0].lower
ub = my_fun_1d.prob_input.marginals[0].upper
xx_1d = np.linspace(lb, ub, 1000)[:, np.newaxis]
yy_1d = my_fun_1d(xx_1d)

# --- Create 2D data from SaltelliLinear
my_fun_2d = uqtf.SaltelliLinear(input_dimension=2)
lb_1 = my_fun_2d.prob_input.marginals[0].lower
ub_1 = my_fun_2d.prob_input.marginals[0].upper
lb_2 = my_fun_2d.prob_input.marginals[1].lower
ub_2 = my_fun_2d.prob_input.marginals[1].upper
xx_1 = np.linspace(lb_1, ub_1, 1000)[:, np.newaxis]
xx_2 = np.linspace(lb_2, ub_2, 1000)[:, np.newaxis]
mesh_2d = np.meshgrid(xx_1, xx_2)
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
axs_1.set_title("1D Saltelli Linear")

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
axs_2.set_title("Surface plot of 2D Saltelli Linear", fontsize=14)

# Contour
axs_3 = plt.subplot(133)
cf = axs_3.contourf(
    mesh_2d[0], mesh_2d[1], yy_2d.reshape(1000, 1000).T, cmap="plasma"
)
axs_3.set_xlabel("$x_1$", fontsize=14)
axs_3.set_ylabel("$x_2$", fontsize=14)
axs_3.set_title("Contour plot of 2D Saltelli Linear", fontsize=14)
divider = make_axes_locatable(axs_3)
cax = divider.append_axes('right', size='5%', pad=0.05)
fig.colorbar(cf, cax=cax, orientation='vertical')

fig.tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

## Test function instance

To create a default instance of the test function, type:

```{code-cell} ipython3
my_testfun = uqtf.SaltelliLinear()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

By default, the input dimension is set to $2$[^default_dimension].
To create an instance with another value of input dimension,
pass an integer to the parameter `input_dimension` (the first parameter).
For example, to create an instance of the Saltelli Linear function
in six dimensions, type:

```{code-cell} ipython3
my_testfun = uqtf.SaltelliLinear(input_dimension=6)
```

In the subsequent section, the function will be illustrated
using six dimensions.

## Description

The Saltelli Linear function is defined as follows:

$$
\mathcal{M}(\boldsymbol{x}) = \sum_{i = 1}^M x_i
$$
where $\boldsymbol{x} = \{ x_1, \ldots, x_M \}$ is the $M$-dimensional vector
of input variables further defined below.

## Probabilistic input

Based on {cite}`Saltelli2008` the probabilistic input model for the function
consists of $M$ independent uniform random variables with the following ranges:

$$
X_i \sim \mathcal{U}[x_{o, i} - \sigma_{o, i}, x_{o, i} + \sigma_{o, i}], \; i = 1, \ldots, M,
$$
where $x_{o, i} = 3^{i - 1}$ and $\sigma_{o, i} = 0.5 * x_{o, i}$.
Notice that the higher the variable index, the larger its uncertainty both
in absolute sense (i.e., the standard deviation is larger)
and in relative sense (i.e., the coefficient of variation is larger).

For the six-variable model, the ranges are shown below.

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
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

### Moments estimation

The mean and variance of the Sobol'-G function can be computed analytically.

The mean is given as follows:

$$
\mathbb{E}[Y] = \sum_{i = 1}^M \mathbb{E}[X_i] = \sum_{i = 1}^M x_{o, i},
$$
where $x_{o, i} = 3^{i - 1}, i = 1, \ldots, M$.

The variance is given as follows:

$$
\mathbb{V}[Y] = \sum_{i = 1}^M \mathbb{V}[X_i] = \frac{1}{12} \sum_{i = 1}^M x_{o, i}^2,
$$

The means and variances for the linear function up to dimension $10$ are shown
in the table below.

```{code-cell} ipython3
:tags: [hide-input]

from tabulate import tabulate

input_dims = 10

# --- Compile data row-wise

outputs = []
for input_dim in range(1, input_dims + 1):
    xx_o = 3**(np.arange(1, input_dim + 1) - 1)
    outputs.append(
        [input_dim, np.sum(xx_o), np.sum(xx_o**2) / 12]
    )

header_names = [
    "Input dimensions",
    "Mean",
    "Variance",
]

tabulate(
    outputs,
    numalign="center",
    stralign="center",
    tablefmt="html",
    floatfmt=("d", ".4e", ".4e"),
    headers=header_names
)
```

Shown below is the convergence of a direct Monte-Carlo estimation of
the output mean and variance with increasing sample sizes compared with the
analytical values.
The error bars correspond to twice the standard deviation
of the estimates obtained from $50$ replications.

```{code-cell} ipython3
:tags: [hide-input]

# --- Compute the mean and variance estimate
my_testfun.prob_input.reset_rng(42)
sample_sizes = np.array([1e1, 1e2, 1e3, 1e4, 1e5, 1e6], dtype=int)
mean_estimates = np.empty((len(sample_sizes), 50))
var_estimates = np.empty((len(sample_sizes), 50))

for i, sample_size in enumerate(sample_sizes):
    for j in range(50):
        xx_test = my_testfun.prob_input.get_sample(sample_size)
        yy_test = my_testfun(xx_test)
        mean_estimates[i, j] = np.mean(yy_test)
        var_estimates[i, j] = np.var(yy_test)

mean_estimates_errors = np.std(mean_estimates, axis=1)
var_estimates_errors = np.std(var_estimates, axis=1)

# --- Compute analytical mean and variance
xx_o = 3**(np.arange(1, my_testfun.input_dimension + 1) - 1)
mean_analytical = np.sum(xx_o)
var_analytical = np.sum(xx_o**2) / 12.0

# --- Plot the mean and variance estimates
fig, ax_1 = plt.subplots(figsize=(6,4))

ext_sample_sizes = np.insert(sample_sizes, 0, 1)
ext_sample_sizes = np.insert(ext_sample_sizes, -1, 5e6)

# --- Mean plot
ax_1.errorbar(
    sample_sizes,
    mean_estimates[:,0],
    yerr=2.0*mean_estimates_errors,
    marker="o",
    color="#66c2a5",
    label="Mean"
)
# Plot the analytical mean
ax_1.plot(
    ext_sample_sizes,
    np.repeat(mean_analytical, len(ext_sample_sizes)),
    linestyle="--",
    color="#66c2a5",
    label="Analytical mean",
)
ax_1.set_xlim([5, 5e6])
ax_1.set_xlabel("Sample size")
ax_1.set_ylabel("Output mean estimate")
ax_1.set_xscale("log");
ax_2 = ax_1.twinx()

# --- Variance plot
ax_2.errorbar(
    sample_sizes+1,
    var_estimates[:,0],
    yerr=2.0*var_estimates_errors,
    marker="o",
    color="#fc8d62",
    label="Variance",
)
# Plot the analytical variance
ax_2.plot(
    ext_sample_sizes,
    np.repeat(var_analytical, len(ext_sample_sizes)),
    linestyle="--",
    color="#fc8d62",
    label="Analytical variance",
)
ax_2.set_ylabel("Output variance estimate")

# Add the two plots together to have a common legend
ln_1, labels_1 = ax_1.get_legend_handles_labels()
ln_2, labels_2 = ax_2.get_legend_handles_labels()
ax_2.legend(ln_1 + ln_2, labels_1 + labels_2, loc=0)

plt.grid()
fig.set_dpi(150)
```

The tabulated results for each sample size is shown below.

```{code-cell} ipython3
:tags: [hide-input]

from tabulate import tabulate

# --- Compile data row-wise
outputs = [
    [
        np.nan,
        mean_analytical,
        0.0,
        var_analytical,
        0.0,
        "Analytical",
    ]
]

for (
    sample_size,
    mean_estimate,
    mean_estimate_error,
    var_estimate,
    var_estimate_error,
) in zip(
    sample_sizes,
    mean_estimates[:,0],
    2.0*mean_estimates_errors,
    var_estimates[:,0],
    2.0*var_estimates_errors,
):
    outputs += [
        [
            sample_size,
            mean_estimate,
            mean_estimate_error,
            var_estimate,
            var_estimate_error,
            "Monte-Carlo",
        ],
    ]

header_names = [
    "Sample size",
    "Mean",
    "Mean error",
    "Variance",
    "Variance error",
    "Remark",
]

tabulate(
    outputs,
    numalign="center",
    stralign="center",
    tablefmt="html",
    floatfmt=(".1e", ".4e", ".4e", ".4e", ".4e", "s"),
    headers=header_names
)
```

### Sensitivity indices

The main-effect Sobol' sensitivity indices of the linear function are given
by the following formula:

$$
S_i \equiv \frac{V_i}{\mathbb{V}[Y]} = \frac{\mathbb{V}[X_i]}{\mathbb{V}[Y]} = \frac{x_{o, i}^2}{\sum_{i = 1}^M x_{o, i}^2},\; i = 1, \ldots, M. 
$$

Since there is no interaction effect present in the model, the total-effect
indices are equal to the main-effect indices.

Some example values of the main-effect indices for the linear function 
up to dimension $6$ is shown in the table below.

```{code-cell} ipython3
:tags: [hide-input]

from tabulate import tabulate

input_dims = 6

# --- Compile data row-wise

outputs = []
for input_dim in range(input_dims):
    output = [f"X{input_dim + 1}"]
    for _ in range(input_dim):
        output.append(0.0)
    for i in range(input_dim, input_dims):
        xx_o = 3**(np.arange(1, i + 2) - 1)
        
        output.append(
            xx_o[input_dim]**2 / np.sum(xx_o**2)
        )

    outputs.append(output)

header_names = [
    "Si",
    "m = 1",
    "m = 2",
    "m = 3",
    "m = 4",
    "m = 5",
    "m = 6",
]

tabulate(
    outputs,
    numalign="center",
    stralign="center",
    tablefmt="html",
    floatfmt=("s", ".4e", ".4e", ".4e", ".4e", ".4e", ".4e"),
    headers=header_names
)
```

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^integral]: The expected value is the same as the integral over the domain
because the input is uniform in a unit hypercube.

[^default_dimension]: This default dimension applies to all variable dimension
test functions. It will be used if the `input_dimension` argument is not given.
