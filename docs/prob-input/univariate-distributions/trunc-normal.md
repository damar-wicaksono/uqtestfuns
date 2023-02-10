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

Uniform distribution is a two-parameter continuous probability distribution.
The table below summarizes some important aspects of the uniform distributions:

|                | Values                                                                                            | Remarks     |
|----------------|---------------------------------------------------------------------------------------------------|-------------|
| **Notation**   | $X \sim \mathcal{U}(a, b)$                                                                        |             |
| **Parameters** | $a \in \mathbb{R}$                                                                                | lower bound |
|                | $b \in \mathbb{R}$, $b > a$                                                                       | upper bound |
| **Support**    | $\mathcal{D}_X = [a, b] \subset \mathbb{R}$                                                       |             |
| **PDF**        | $f_X(x) = \begin{cases} \frac{1}{b - a} & x \in [a, b] \\ 0 & x \notin [a, b] \end{cases}$        |             |
| **CDF**        | $F_X(x) = \begin{cases} 0 & x < a \\ \frac{x - a}{b - a} & x \in [a, b] \\ 1 & x > b \end{cases}$ |             |

The plots of probability density function (PDF),
cumulative distribution function (CDF),
as well as the histogram of a sample ($5000$ points) for different parameter
values are shown below.

```{code-cell} ipython3
:tags: [remove-input]

my_input_1 = uqtf.UnivariateInput(distribution="beta", parameters=[0.5, 0.5, 0, 1])
my_input_2 = uqtf.UnivariateInput(distribution="beta", parameters=[1, 1, -1, 1])
my_input_3 = uqtf.UnivariateInput(distribution="beta", parameters=[2, 5, -1, 1])
my_input_4 = uqtf.UnivariateInput(distribution="beta", parameters=[5, 2, 1, 2])

xx = np.linspace(-3, 3, 1000)
sample_size = 5000
pdf_1 = my_input_1.pdf(xx)
cdf_1 = my_input_1.cdf(xx)
xx_1 = my_input_1.get_sample(sample_size)

pdf_2 = my_input_2.pdf(xx)
cdf_2 = my_input_2.cdf(xx)
xx_2 = my_input_2.get_sample(sample_size)

cdf_3 = my_input_3.cdf(xx)
pdf_3 = my_input_3.pdf(xx)
xx_3 = my_input_3.get_sample(sample_size)

cdf_4 = my_input_4.cdf(xx)
pdf_4 = my_input_4.pdf(xx)
xx_4 = my_input_4.get_sample(sample_size)

fig, axs = plt.subplots(1, 3, figsize=(10,4))
axs[0].plot(xx, pdf_1, label="a = -5.0, b = 5.0")
axs[0].plot(xx, pdf_2, label="a = 0.0, b = 1.0")
axs[0].plot(xx, pdf_3, label="a = -3.0, b = -1.0")
axs[0].plot(xx, pdf_4, label="a = -3.0, b = -1.0")
axs[0].set_title("PDF")

axs[1].plot(xx, cdf_1, label="a = -5.0, b = 5.0")
axs[1].plot(xx, cdf_2, label="a = 0.0, b = 1.0")
axs[1].plot(xx, cdf_3, label="a = -3.0, b = -1.0")
axs[1].plot(xx, cdf_4, label="a = -3.0, b = -1.0")
axs[1].set_title("CDF")
axs[1].legend();

axs[2].hist(xx_1, label="a = -5.0, b = 5.0", bins="auto")
axs[2].hist(xx_2, label="a = 0.0, b = 1.0", bins="auto")
axs[2].hist(xx_3, label="a = -3.0, b = -1.0", bins="auto")
axs[2].hist(xx_4, label="a = -3.0, b = -1.0", bins="auto")
axs[2].set_title("Sample histogram")

plt.gcf().set_dpi(300)
```