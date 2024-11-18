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

(test-functions:flood)=
# Flood Model

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The flood model is an eight-dimensional scalar valued function.
The model was used in the context of sensitivity analysis in {cite}`Iooss2015, Lamboni2013`
and has become a canonical example of the OpenTURNS package {cite}`Baudin2017`.

## Test function instance

To create a default instance of the flood model:

```{code-cell} ipython3
my_testfun = uqtf.Flood()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The flood model computes the maximum annual underflow of a river
using the following analytical formula:

$$
\begin{align}
	\mathcal{M}(\boldsymbol{x}) & = z_v + h - h_d - c_b\\
	h & = \left[ \frac{q}{b k_s \left(\frac{z_m - z_v}{l} \right)^{0.5}} \right]^{0.6}
\end{align}
$$
where $\boldsymbol{x} = \{ q, k_s, z_v, z_m, h_d, c_b, l, b \}$
is the eight-dimensional vector of input variables further defined below.
The output is given in $[\mathrm{m}]$.
A negative value indicates that an overflow (_flooding_) occurs.

```{note}
Compared to the original function,
this implementation inverted the sign of the output
such that underflowing has a positive sign.
```
The model is based on a simplification of the one-dimensional hydro-dynamical
equations of St. Venant under the assumption of uniform and constant flow rate 
and a large rectangular section. 

## Probabilistic input

Based on {cite}`Iooss2015` (Table 4), the probabilistic input model
for the flood model consists of eight independent random variables
with marginals shown in the table below.

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

np.random.seed(42)
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
:style: unsrtalpha
:filter: docname in docnames
```