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
# Twenty-dimensional Low-Degree Polynomial from Alemazkoor and Meidani (2018)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The test function from {cite}`Alemazkoor2018` (`Alemazkoor20D` for short)
is a twenty-dimensional polynomial of total degree 2.
It was used as a benchmark for sparse polynomial chaos expansion metamodeling,
as the counterpart to {ref}`Alemazkoor2D <test-functions:alemazkoor-2d>`:
where that function is low-dimensional with high polynomial degree,
this one is high-dimensional with low degree.

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

```{code-cell} ipython3
:tags: [hide-input, output_scroll]

print(my_testfun.prob_input)
```

## Reference results

This section provides several reference results of typical UQ analyses
involving the test function.

### Sample histogram

Shown below is the histogram of the output based on $100'000$ random points:

```{code-cell} ipython3
:tags: [hide-input]

yy_test = my_testfun.get_sample(100000)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel(r"$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Section 4.1, Eq. (32) in {cite}`Alemazkoor2018`.