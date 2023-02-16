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

(prob-input:univariate-distributions:trunc-normal)=
# Truncated Normal (Gaussian) Distribution

The normal (or Gaussian) distribution is a two-parameter continuous probability
distribution.
The table below summarizes some important aspects of the distribution.

|                      |                                                                                                                                                                                                                                    |
|---------------------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|         **Notation** | $X \sim \mathcal{N}_{\mathrm{Tr}} (\mu, \sigma, a, b)$                                                                                                                                                                             |
|       **Parameters** | $\mu \in \mathbb{R}$ (mean, or location parameter)                                                                                                                                                                                 |
|                      | $\sigma > 0$ (standard deviation, or scale parameter)                                                                                                                                                                              |
|                      | $a \in (-\infty, b)$ (lower bound)                                                                                                                                                                                                 |
|                      | $b \in (a, \infty)$ (upper bound)                                                                                                                                                                                                  |
|  **{term}`Support`** | $\mathcal{D}_X = [a, b]$                                                                                                                                                                                                           |
|      **{term}`PDF`** | $f_X (x; \mu, \sigma, a, b) = \begin{cases} \frac{1}{\Phi(\frac{b - \mu}{\sigma}) - \Phi(\frac{a - \mu}{\sigma})} \frac{1}{\sigma} \phi\left(\frac{x - \mu}{\sigma}\right) & x \in [a, b] \\ 0.0 & x \notin [a, b] \end{cases}$    |
|      **{term}`CDF`** | $F_X (x; \mu, \sigma, a, b) = \begin{cases} 0.0 & x < a \\ \frac{\Phi(\frac{x - \mu}{\sigma}) - \Phi(\frac{a - \mu}{\sigma})}{\Phi(\frac{b - \mu}{\sigma}) - \Phi(\frac{a - \mu}{\sigma})} & x \in [a, b] \\ 1.0 & x > b \end{cases}$ |
|     **{term}`ICDF`** | $F^{-1}_X (x; \mu, \sigma, a, b) = \mu + \sigma \Phi^{-1} \left[ \left(\Phi\left(\frac{b - \mu}{\sigma}\right) - \Phi\left(\frac{a - \mu}{\sigma}\right)\right) x + \Phi\left(\frac{x - a}{\sigma}\right) \right]$                 |

In the table above, $\phi$, $\Phi$, and $\Phi^{-1}$ are the probability density,
the cumulative and the inverse cumulative distribution functions 
of {ref}`the standard normal distribution <prob-input:univariate-distributions:normal:standard>`,
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

parameters = [[0, 2, -10, 10], [-5, 3, -10, 10], [0, 5.0, -10, 10], [7, 2.5, -10, 10]]
colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c"]

univariate_inputs = []
for parameter in parameters:
    univariate_inputs.append(uqtf.UnivariateInput(distribution="trunc-normal", parameters=parameter))

fig, axs = plt.subplots(2, 2, figsize=(10,10))

# --- PDF
xx = np.linspace(-10, 10, 1000)
for i, univariate_input in enumerate(univariate_inputs):
    axs[0, 0].plot(
        xx,
        univariate_input.pdf(xx),
        color=colors[i],
        label=f"$\\mu = {univariate_input.parameters[0]}, \\sigma={univariate_input.parameters[1]}$",
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
        label=f"mu = {univariate_input.parameters[0]}, beta={univariate_input.parameters[1]}",
        bins="auto",
        alpha=0.75
    )
axs[0, 1].grid();
axs[0, 1].set_xlim([-10, 10]);
axs[0, 1].set_title("Sample histogram");

# --- CDF
xx = np.linspace(-10, 10, 1000)
for i, univariate_input in enumerate(univariate_inputs):
    axs[1, 0].plot(
        xx,
        univariate_input.cdf(xx),
        color=colors[i],
        label=f"mu = {univariate_input.parameters[0]}, beta={univariate_input.parameters[1]}",
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
        label=f"mu = {univariate_input.parameters[0]}, beta={univariate_input.parameters[1]}",
        linewidth=2
    )
axs[1, 1].grid();
axs[1, 1].set_ylim([-10, 10]);
axs[1, 1].set_title("Inverse CDF");

plt.gcf().set_dpi(150)
```