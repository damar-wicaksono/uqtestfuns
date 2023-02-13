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

(prob-input:univariate-distributions:triangular)=
# Triangular Distribution

The triangular distribution is a three-parameter continuous probability
distribution.
The table below summarizes some important aspects of the uniform distributions.


|                     |                                                                                                                                                                                              |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Notation**        | $X \sim \mathcal{T}_r (a, b, c)$                                                                                                                                                             |
| **Parameters**      | $a \in \mathbb{R}$ (lower bound)                                                                                                                                                             |
|                     | $b \in \mathbb{R}$, $b > a$ (upper bound)                                                                                                                                                    |
|                     | $c \in \mathbb{R}$, $a < b < c$ (mid point)                                                                                                                                                  |
| **{term}`Support`** | $\mathcal{D}_X = [a, b] \subset \mathbb{R}$                                                                                                                                                  |
| **{term}`PDF`**     | $f_X (x) = \begin{cases} 0.0 & x < a \\ \frac{2}{(b-a) (c-a)} (x - a) & x \in [a, c) \\	\frac{2}{b-a} & x = c \\ \frac{2}{(b-a) (b - c)} (b - x) & x \in (c, b] \\ 0.0 & x > b \end{cases}$  |
| **{term}`CDF`**     | $F_X (x) = \begin{cases} 0.0 & x < a \\	\frac{(x - a)^2}{(b - a) (c - a)} & x \in [a, c] \\	1.0 - \frac{(b - x)^2}{(b-a) (b - c)} & x \in (c, b] \\	1.0 & x > b \end{cases}$                 |
| **{term}`ICDF`**    | $F^{-1}_X (x) = \begin{cases} a + \sqrt{(b - a) (c - a) x} & x \in [0.0, \frac{c - a}{b - a}] \\ b - \sqrt{(b - a) (b - c) (1 - x)} & x \in (\frac{c - a}{b - a}, 1.0] \\ \end{cases}$       |

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

parameters = [[0, 4, 3], [-4, -1, -2.5], [-1, 1, 0], [-4, 3, -3]]
colors = ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c"]

univariate_inputs = []
for parameter in parameters:
    univariate_inputs.append(uqtf.UnivariateInput(distribution="triangular", parameters=parameter))

fig, axs = plt.subplots(2, 2, figsize=(10,10))

# --- PDF
xx = np.linspace(-4, 4, 1000)
for i, univariate_input in enumerate(univariate_inputs):
    axs[0, 0].plot(
        xx,
        univariate_input.pdf(xx),
        color=colors[i],
        label=f"$a = {univariate_input.parameters[0]}, b = {univariate_input.parameters[1]}, c = {univariate_input.parameters[2]}$",
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
axs[0, 1].set_xlim([-4, 4]);
axs[0, 1].set_title("Sample histogram");

# --- CDF
xx = np.linspace(-4, 4, 1000)
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
axs[1, 1].set_ylim([-4, 4]);
axs[1, 1].set_title("Inverse CDF");

plt.gcf().set_dpi(150)
```