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

The Borehole test function is an 8-dimensional scalar-valued function
{cite}`Harper1983`.

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns
```

Create an instance of the Borehole test function using
the built-in default arguments:

```{code-cell} ipython3
my_testfun = uqtestfuns.create_from_default("borehole")
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The weight of a light aircraft wing is computed using the following analytical expression:

$$
\mathcal{M}(\boldsymbol{x}) = \frac{2 \, \pi \, T_u \, (H_u - H_l)}{\ln{(r/rw)} \left[1 + \frac{2 \, L \, Tu}{\ln{(r/rw)} \, r_w^2 K_w} + \frac{T_u}{T_l} \right]} 
$$

where $\boldsymbol{x} = \{ r_w, r, T_u, H_u, T_l, H_l, L, K_w\}$ is the vector of input variables defined below.

+++

## Inputs

The original eight input variables of the Borehole function
(from {cite}`Harper1983`) are modeled as independent random variables
whose marginals shown in the table below.

```{code-cell} ipython3
my_testfun.input
```

There is another input specification from the literature listed in the table below.

| No. | Source | Keyword |
|:--:|:-----:|:-------:|
| 1 | {cite:t}`Harper1983` |  `'harper'` (default) |
| 2 | {cite:t}`Morris1993` | `'morris'`           | 

```{note}
If available, alternative input specification can be selected when a default test function is created 
by additionally passing one of the available keywords (such as listed above)
to the `input_selection` parameter.
```

For example, to create a Borehole test function using the input specification by {cite:t}`Morris1993`:

```{code-cell} ipython3
my_testfun_alt = uqtestfuns.create_from_default("borehole", input_selection="morris")
my_testfun_alt.input
```

## Reference Results

+++

Generate a random sample of input/output pairs:

```{code-cell} ipython3
xx_test = my_testfun.input.get_sample(10000)
yy_test = my_testfun(xx_test)
```

Create a histogram of the raw output (i.e., the water flow rate):

```{code-cell} ipython3
plt.hist(yy_test, bins="auto");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
```

## References

```{bibliography}
:style: unsrt
:filter: docname in docnames
```