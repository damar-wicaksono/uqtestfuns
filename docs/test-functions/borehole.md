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

(test-functions:borehole)=
# Borehole Function

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The Borehole test function is an eight-dimensional scalar-valued function.
The function has been used in the context of sensitivity analysis
{cite}`Harper1983` and metamodeling {cite}`Morris1993`.

The function models the flow rate of water through a borehole drilled
from the ground surface through two aquifers.
The model assumes laminar-isothermal flow, and there is no groundwater gradient,
with steady-state flow between the upper aquifer and the borehole
and between the borehole and the lower aquifer.

## Test function instance

To create an instance of the Borehole test function:

```{code-cell} ipython3
my_testfun = uqtf.Borehole()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The Borehole function computes the water flow rate through a borehole drilled
through two aquifers:

$$
\mathcal{M}(\boldsymbol{x}) = \frac{2 \, \pi \, T_u \, (H_u - H_l)}{\ln{(r/rw)} \left[1 + \frac{2 \, L \, Tu}{\ln{(r/rw)} \, r_w^2 K_w} + \frac{T_u}{T_l} \right]} 
$$

where $\boldsymbol{x} = \{ r_w, r, T_u, H_u, T_l, H_l, L, K_w\}$
is the vector of input variables defined below.
The unit of the output is $\left[ \mathrm{m}^3 / \mathrm{year} \right]$

## Probabilistic input

There are two probabilistic input models available as shown in the table below.

|  No.   |        Keyword         |       Source       |  
|:------:|:----------------------:|:------------------:|  
|   1.   | `Harper1983` (default) | {cite}`Harper1983` |  
|   2.   |      `Morris1993`      | {cite}`Morris1993` |

In both specifications, the input variables are modeled as independent random
variables.
The marginals of the original specification (from {cite}`Harper1983`) are shown
below:

```{code-cell} ipython3
my_testfun.prob_input
```

```{note}
In {cite}`Morris1993`,
the non-uniform distributions ($r_w$ and $r$) are replaced
with uniform distributions.
```

For example, to create a Borehole test function using
the input specification by {cite}`Morris1993`:

```python
my_testfun = uqtf.Borehole(prob_input_selection="Morris1993")
```

## Reference Results

This section provides several reference results of typical UQ analyses involving
the test function.

### Sample histogram

Shown below is the histogram of the output based on $100'000$ random points:

```{code-cell} ipython3
:tags: [hide-input]

xx_test = my_testfun.prob_input.get_sample(100000)
yy_test = my_testfun(xx_test)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

### Moments estimation

Shown below is the convergence of a direct Monte-Carlo estimation of
the output mean and variance with increasing sample sizes.

```{code-cell} ipython3
:tags: [hide-input]

# --- Compute the mean and variance estimate
np.random.seed(42)
sample_sizes = np.array([1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7], dtype=int)
mean_estimates = np.empty(len(sample_sizes))
var_estimates = np.empty(len(sample_sizes))

for i, sample_size in enumerate(sample_sizes):
    xx_test = my_testfun.prob_input.get_sample(sample_size)
    yy_test = my_testfun(xx_test)
    mean_estimates[i] = np.mean(yy_test)
    var_estimates[i] = np.var(yy_test)

# --- Compute the error associated with the estimates
mean_estimates_errors = np.sqrt(var_estimates) / np.sqrt(np.array(sample_sizes))
var_estimates_errors = var_estimates * np.sqrt(2 / (np.array(sample_sizes) - 1))

# --- Do the plot
fig, ax_1 = plt.subplots(figsize=(6,4))

ax_1.errorbar(
    sample_sizes,
    mean_estimates,
    yerr=mean_estimates_errors,
    marker="o",
    color="#66c2a5",
    label="Mean",
)
ax_1.set_xlabel("Sample size")
ax_1.set_ylabel("Output mean estimate")
ax_1.set_xscale("log");
ax_2 = ax_1.twinx()
ax_2.errorbar(
    sample_sizes + 1,
    var_estimates,
    yerr=var_estimates_errors,
    marker="o",
    color="#fc8d62",
    markerfacecolor='none',
    label="Variance",
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
outputs = []
for (
    sample_size,
    mean_estimate,
    mean_estimate_error,
    var_estimate,
    var_estimate_error,
) in zip(
    sample_sizes,
    mean_estimates,
    mean_estimates_errors,
    var_estimates,
    var_estimates_errors,
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
    headers=header_names,
    floatfmt=(".1e", ".4e", ".4e", ".4e", ".4e", "s"),
    tablefmt="html",
    stralign="center",
    numalign="center",
)
```

## References

```{bibliography}
:style: unsrt
:filter: docname in docnames
```
