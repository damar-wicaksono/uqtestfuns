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

```{code-cell} ipython3
:tags: [remove-cell]

import uqtestfuns as uqtf
import matplotlib.pyplot as plt
import numpy as np
```

(prob-input:univariate-distributions:trunc-gumbel)=
# Truncated Gumbel (max.) Distribution

The truncated Gumbel (max.) distribution is a four-parameter continuous
probability distribution.
The table below summarizes some important aspects of the distribution.

|                      |                                                                                                                                                                                                                                                                   |
|---------------------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|         **Notation** | $X \sim \mathrm{Gumbel}_{\mathrm{Tr}} (\mu, \beta, a, b)$                                                                                                                                                                                                         |
|       **Parameters** | $\mu \in \mathbb{R}$ (location parameter)                                                                                                                                                                                                                         |
|                      | $\beta > 0$ (scale parameter)                                                                                                                                                                                                                                     |
|                      | $a \in (-\infty, b)$ (lower bound)                                                                                                                                                                                                                                |
|                      | $b \in (a, \infty)$ (upper bound)                                                                                                                                                                                                                                 |
|  **{term}`Support`** | $\mathcal{D}_X = [a, b]$                                                                                                                                                                                                                                          |
|      **{term}`PDF`** | $f_X (x; \mu, \sigma, a, b) = \begin{cases} \frac{1}{F_{\mathrm{Gumbel}}(b; \mu, \sigma) - F_{\mathrm{Gumbel}}(a; \mu, \sigma)} f_{\mathrm{Gumbel}}(x; \mu, \sigma) & x \in [a, b]\\ 0.0 & x \notin [a, b] \end{cases}$                                           |
|      **{term}`CDF`** | $F_X (x; \mu, \sigma, a, b) = \begin{cases} 0.0 & x < a \\ \frac{F_{\mathrm{Gumbel}}(x; \mu, \sigma) - F_{\mathrm{Gumbel}}(a; \mu, \sigma)}{F_{\mathrm{Gumbel}}(b; \mu, \sigma) - F_{\mathrm{Gumbel}}(a; \mu, \sigma)} & x \in [a, b] \\ 1.0 & x > b \end{cases}$ |
|     **{term}`ICDF`** | $F^{-1}_X (x; \mu, \beta, a, b) = \left(F_{\mathrm{Gumbel}}(b; \mu, \sigma) - F_{\mathrm{Gumbel}}(a; \mu, \sigma)\right) x + F_{\mathrm{Gumbel}}(a; \mu, \sigma)$                                                                                                 |

In the table above, $f_{\mathrm{Gumbel}}$, $F_{\mathrm{Gumbel}}$,
and $F^{-1}_{\mathrm{Gumbel}}$ are the probability density,
the cumulative, and the inverse cumulative distribution functions
of {ref}`the (untruncated) Gumbel (max.) distribution <prob-input:univariate-distributions:gumbel>`,
respectively.

The plots of probability density functions (PDFs),
sample histogram (of $5'000$ points),
cumulative distribution functions (CDFs),
and inverse cumulative distribution functions (ICDFs) for different parameter
values are shown below.

```{code-cell} ipython3
:tags: [remove-input]

import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf

parameters = [[-1, 2.0, 0, 20], [4.0, 2.0, 0, 20], [7.5, 3.0, 0, 20], [2.0, 3.0, 0, 20]]
colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c"]

univariate_inputs = []
for parameter in parameters:
    univariate_inputs.append(uqtf.UnivariateInput(distribution="trunc-gumbel", parameters=parameter))

fig, axs = plt.subplots(2, 2, figsize=(10,10))

# --- PDF
xx = np.linspace(0, 20, 1000)
for i, univariate_input in enumerate(univariate_inputs):
    axs[0, 0].plot(
        xx,
        univariate_input.pdf(xx),
        color=colors[i],
        label=f"$\\mu = {univariate_input.parameters[0]}, \\beta={univariate_input.parameters[1]}, a={univariate_input.parameters[2]}, b={univariate_input.parameters[3]}$",
        linewidth=2,
    )
axs[0, 0].legend();
axs[0, 0].grid();
axs[0, 0].set_title("PDF");

# --- Sample histogram
sample_size = 5000
np.random.seed(42)
for col, univariate_input in zip(reversed(colors), reversed(univariate_inputs)):
    axs[0, 1].hist(
        univariate_input.get_sample(sample_size),
        color=col,
        bins="auto",
        alpha=0.75
    )
axs[0, 1].grid();
axs[0, 1].set_xlim([0, 20]);
axs[0, 1].set_title("Sample histogram");

# --- CDF
xx = np.linspace(0, 20, 1000)
for i, univariate_input in enumerate(univariate_inputs):
    axs[1, 0].plot(
        xx,
        univariate_input.cdf(xx),
        color=colors[i],
        linewidth=2,
    )
axs[1, 0].grid();
axs[1, 0].set_title("CDF");

# --- Inverse CDF
xx = np.linspace(0, 1, 1000)
for i, univariate_input in enumerate(univariate_inputs):
    axs[1, 1].plot(
        xx,
        univariate_input.icdf(xx),
        color=colors[i],
        linewidth=2
    )
axs[1, 1].grid();
axs[1, 1].set_ylim([0, 20]);
axs[1, 1].set_title("Inverse CDF");

plt.gcf().set_dpi(150)
```