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

(prob-input:marginal-distributions:triangular)=
# Triangular Distribution

The triangular distribution is a three-parameter continuous probability
distribution.
The table below summarizes some important aspects of the distribution.


|                      |                                                                                                                                                                                                      |
|---------------------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|         **Notation** | $X \sim \mathcal{T}_r (a, b, c)$                                                                                                                                                                     |
|       **Parameters** | $a \in (-\infty, b)$ (lower bound)                                                                                                                                                                   |
|                      | $b \in (a, \infty)$ (upper bound)                                                                                                                                                                    |
|                      | $c \in (a, b)$ (mid point)                                                                                                                                                                           |
|  **{term}`Support`** | $\mathcal{D}_X = [a, b] \subset \mathbb{R}$                                                                                                                                                          |
|      **{term}`PDF`** | $f_X (x; a, b, c) = \begin{cases} 0.0 & x < a \\ \frac{2}{(b-a) (c-a)} (x - a) & x \in [a, c) \\	\frac{2}{b-a} & x = c \\ \frac{2}{(b-a) (b - c)} (b - x) & x \in (c, b] \\ 0.0 & x > b \end{cases}$ |
|      **{term}`CDF`** | $F_X (x; a, b, c) = \begin{cases} 0.0 & x < a \\	\frac{(x - a)^2}{(b - a) (c - a)} & x \in [a, c] \\	1.0 - \frac{(b - x)^2}{(b-a) (b - c)} & x \in (c, b] \\	1.0 & x > b \end{cases}$                |
|     **{term}`ICDF`** | $F^{-1}_X (x; a, b, c) = \begin{cases} a + \sqrt{(b - a) (c - a) x} & x \in [0.0, \frac{c - a}{b - a}] \\ b - \sqrt{(b - a) (b - c) (1 - x)} & x \in (\frac{c - a}{b - a}, 1.0] \\ \end{cases}$      |

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

univ_dists = []
for parameter in parameters:
    univ_dists.append(uqtf.Marginal(distribution="triangular", parameters=parameter))

fig, axs = plt.subplots(2, 2, figsize=(10,10))

# --- PDF
xx = np.linspace(-4, 4, 1000)
for i, univ_dist in enumerate(univ_dists):
    axs[0, 0].plot(
        xx,
        univ_dist.pdf(xx),
        color=colors[i],
        label=f"$a = {univ_dist.parameters[0]}, b = {univ_dist.parameters[1]}, c = {univ_dist.parameters[2]}$",
        linewidth=2,
    )
axs[0, 0].legend();
axs[0, 0].grid();
axs[0, 0].set_title("PDF");

# --- Sample histogram
sample_size = 5000
np.random.seed(42)
for col, univ_dist in zip(reversed(colors), reversed(univ_dists)):
    axs[0, 1].hist(
        univ_dist.get_sample(sample_size),
        color=col,
        bins="auto",
        alpha=0.75
    )
axs[0, 1].grid();
axs[0, 1].set_xlim([-4, 4]);
axs[0, 1].set_title("Sample histogram");

# --- CDF
xx = np.linspace(-4, 4, 1000)
for i, univ_dist in enumerate(univ_dists):
    axs[1, 0].plot(
        xx,
        univ_dist.cdf(xx),
        color=colors[i],
        linewidth=2,
    )
axs[1, 0].grid();
axs[1, 0].set_title("CDF");

# --- Inverse CDF
xx = np.linspace(0, 1, 1000)
for i, univ_dist in enumerate(univ_dists):
    axs[1, 1].plot(
        xx,
        univ_dist.icdf(xx),
        color=colors[i],
        linewidth=2
    )
axs[1, 1].grid();
axs[1, 1].set_ylim([-4, 4]);
axs[1, 1].set_title("Inverse CDF");

plt.gcf().set_dpi(150)
```
