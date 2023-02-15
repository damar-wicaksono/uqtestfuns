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

(prob-input:univariate-distributions:logitnormal)=
# Logit-Normal Distribution

The logit-normal distribution is a two-parameter continuous probability distribution.
A logit-normal random variable is a variable whose _logit_ is
a {ref}`normally distributed <prob-input:univariate-distributions:normal>` 
random variable.

```{admonition} Logit and logistic function

The logit function is the inverse cumulative distribution function of
the standard logistic distribution. It is defined as

$$
\mathrm{logit}(x) = \ln \frac{x}{1 - x}, \; x \in (0, 1).	
$$

The inverse of the logit function is called the _logistic function_
(it's, the cumulative distribution function of the standard logistic
distribution):

$$
\mathrm{logistic}(x) = \frac{1}{1 + e^{-x}}, \; x \in \mathbb{R}
$$

The range of the logistic function is $(0, 1)$.
```

The table below summarizes some important aspects of the distribution.

|                      |                                                                                                                                                  |
|---------------------:|--------------------------------------------------------------------------------------------------------------------------------------------------|
|         **Notation** | $X \sim \mathcal{N}_{\mathrm{logit}}(\mu, \sigma)$                                                                                               |
|       **Parameters** | $\mu \in \mathbb{R}$                                                                                                                             |
|                      | $\sigma > 0$                                                                                                                                     |
|  **{term}`Support`** | $\mathcal{D}_X = (0, 1)$                                                                                                                         |
|      **{term}`PDF`** | $f_X (x; \mu, \sigma) = \frac{1}{\sigma \sqrt{2 \pi}} \exp{\left[ - \frac{1}{2} \left(\frac{\mathrm{logit}(x) - \mu}{\sigma} \right)^2 \right]}$ |
|      **{term}`CDF`** | $F_X (x; \mu, \sigma) = \frac{1}{2} \left[ 1 + \mathrm{erf}\left( \frac{\mathrm{logit}(x) - \mu}{\sigma \sqrt{2}}\right) \right]$                |
|     **{term}`ICDF`** | $F^{-1}_X (x; \mu, \sigma) = \mathrm{logistic} \left(\mu + \sqrt{2} \, \sigma \, \mathrm{erf}^{-1}(2 x - 1) \right)$                             |

```{note}
The parameters $\mu$ and $\sigma$ of a logit-normal distribution correspond
to the mean and standard deviation of the underlying normal distribution,
respectively.
```

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

parameters = [[0, 0.5], [0, 1.0], [0, 1.5], [1, 1.5]]
colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c"]

univariate_inputs = []
for parameter in parameters:
    univariate_inputs.append(
    uqtf.UnivariateInput(distribution="logitnormal", parameters=parameter)
    )

fig, axs = plt.subplots(2, 2, figsize=(10,10))

# --- PDF
xx = np.linspace(0, 1, 1000)
for i, univariate_input in enumerate(univariate_inputs):
    axs[0, 0].plot(
        xx,
        univariate_input.pdf(xx),
        color=colors[i],
        label=f"$\\mu = {univariate_input.parameters[0]}, s = {univariate_input.parameters[1]}$",
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
axs[0, 1].set_xlim([0, 1]);
axs[0, 1].set_title("Sample histogram");

# --- CDF
xx = np.linspace(0, 1, 1000)
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
axs[1, 1].set_ylim([0, 1]);
axs[1, 1].set_title("Inverse CDF");

plt.gcf().set_dpi(150)
```