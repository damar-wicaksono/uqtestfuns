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

(prob-input:univariate-distributions:gumbel)=
# Gumbel (max.) Distribution

The Gumbel (max.) distribution is a two-parameter continuous probability distribution.
The table below summarizes some important aspects of the distribution:

|                     |                                                                                                                          |
|---------------------|--------------------------------------------------------------------------------------------------------------------------|
| **Notation**        | $X \sim \mathrm{Gumbel}(\mu, \beta)$                                                                                     |
| **Parameters**      | $\mu \in \mathbb{R}$                                                                                                     |
|                     | $\beta > 0$                                                                                                              |
| **{term}`Support`** | $\mathcal{D}_X = (-\infty, \infty)$                                                                                      |
| **{term}`PDF`**     | $f_X (x) = \frac{1}{\beta} \exp{- \left[ \frac{x - \mu}{\beta} + \exp{-\left(\frac{x - \mu}{\beta} \right)} \right]}$    |
| **{term}`CDF`**     | $F_X (x) = \exp{-\left[ \exp{- \left(\frac{x - \mu}{\beta}) \right)} \right]}$                                           |
| **{term}`ICDF`**    | $F^{-1}_X (x) = \mu + \beta \ln{(\ln{x})}$                                                                               |

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

parameters = [[-1, 2.0], [1.0, 2.0], [1.5, 3.0], [3.0, 4.0]]
colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c"]

univariate_inputs = []
for parameter in parameters:
    univariate_inputs.append(uqtf.UnivariateInput(distribution="gumbel", parameters=parameter))
    
fig, axs = plt.subplots(2, 2, figsize=(10,10))

# --- PDF
xx = np.linspace(-10, 30, 1000)
for i, univariate_input in enumerate(univariate_inputs):
    axs[0, 0].plot(
        xx,
        univariate_input.pdf(xx),
        color=colors[i],
        label=f"$\\mu = {univariate_input.parameters[0]}, \\beta={univariate_input.parameters[1]}$",
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
axs[0, 1].set_xlim([-10, 30]);
axs[0, 1].set_title("Sample histogram");

# --- CDF
xx = np.linspace(-10, 30, 1000)
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
axs[1, 1].set_ylim([-10, 30]);
axs[1, 1].set_title("Inverse CDF");

plt.gcf().set_dpi(150)
```