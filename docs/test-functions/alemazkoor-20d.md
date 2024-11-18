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

(test-functions:alemazkoor-20d)=
# Twenty-dimensional Function from Alemazkoor and Meidani (2018)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The 20-dimensional test function from {cite}`Alemazkoor2018`
(or `Alemazkoor20D` for short) is a polynomial function that features 
low-degree of interactions (i.e., $2$) between the input variables
(i.e., high in dimension but of low-degree).
It was used as a test function for
a metamodeling exercise (i.e., sparse polynomial chaos expansion).

## Test function instance

To create a default instance of the `Alemazkoor20D` function[^location]:

```{code-cell} ipython3
my_testfun = uqtf.Alemazkoor20D()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The `Alemazkoor20D` function is defined as follows:

$$
\mathcal{M}(\boldsymbol{x}) = \sum_{i = 1}^{19} x_{i} x_{i+1}
$$
where $\boldsymbol{x} = \{ x_1, \ldots, x_{20} \}$
is the twenty-dimensional vector of input variables further defined below.

## Probabilistic input

Based on {cite}`Alemazkoor2018`, the probabilistic input model
for the function consists of twenty independent random variables
as shown in the table below.

|   No.    |   Name   | Distribution | Parameters  | Description |
|:--------:|:--------:|:------------:|:-----------:|:-----------:|
|    1     |  $x_1$   |   uniform    | [-1.0, 1.0] |     N/A     |
| $\vdots$ | $\vdots$ |   $\vdots$   |  $\vdots$   |  $\vdots$   |
|    20    | $x_{20}$ |   uniform    | [-1.0, 1.0] |     N/A     |

## Reference results

This section provides several reference results of typical UQ analyses
involving the test function.

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

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Section 4.1, Eq. (32) in {cite}`Alemazkoor2018`.