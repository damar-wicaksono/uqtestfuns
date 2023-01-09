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

(test-functions:ishigami)=
# Ishigami Function

The Ishigami test function is a 3-dimensional scalar-valued function {cite}`Ishigami1991`.

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns
```

Create an instance of the wing weight test function using
the built-in default arguments:

```{code-cell} ipython3
my_testfun = uqtestfuns.create_from_default("ishigami")
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The Ishigami function is defined as the following expression:

$$
\mathcal{M}(\boldsymbol{x}) = \sin(x_1) + a \, \sin^2(x_2) + b \, x_3^4 \, \sin{(x_1)} 
$$

where $\boldsymbol{x} = \{ x_1, x_2, x_3 \}$ is the vector of input variables
and $(a, b)$ are the parameters of the function;
both are given below.

+++

## Inputs

The 3 input variables of the wing weight function are modeled
as independent uniform random variables
with specified ranges shown in the table below.

```{code-cell} ipython3
my_testfun.input
```

The parameters of the Ishigami function are two real-valued numbers.
The values of these parameters differ in the literature,
some of which shown in the table below.

| No. | Value | Source | Keyword |
|:--:|:-----:|:-------:|:-------:|
| 1 | $a = 7$, $b = 0.05$ | {cite:t}`Sobol1999`  | `sobol` (default) |
| 2 | $a = 7$, $b = 0.1$  | {cite:t}`Marrel2009` | `marrel` |

````{note}
To use another set of parameters, create a default test function
and pass one of the available keywords
(such as indicated in the table above) to the `param_selection` parameter.
For example:
```python
uqtestfuns.create_from_default("ishigami", param_selection="marrel")
```
````

## Reference Results

+++

Generate a random sample of input/output pairs:

```{code-cell} ipython3
xx_test = my_testfun.input.get_sample(1000000)
yy_test = my_testfun(xx_test)
```

Create a histogram of the raw output (i.e., the weight of the wing):

```{code-cell} ipython3
plt.hist(yy_test, bins="auto");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
```

### Moments

The mean and variance of the Ishigami function can be computed analytically,
and the results are:

- $\mathbb{E}[Y] = \frac{a}{2}$
- $\mathbb{V}[Y] = \frac{a^2}{8} + \frac{b \pi^4}{5} + \frac{b^2 \pi^8}{18} + \frac{1}{2}$

which depend on the choice of the parameter values.

### Sobol' indices

The main-effect and total-effect Sobol' indices of the Ishigami function can be 
derived analytically.

The main-effect (i.e., first-order) Sobol' indices are:

- $S_1 \equiv \frac{V_1}{\mathbb{V}[Y]}$
- $S_2 \equiv \frac{V_2}{\mathbb{V}[Y]}$
- $S_3 \equiv \frac{V_3}{\mathbb{V}[Y]}$

where the total variances $\mathbb{V}[Y]$ is given in the section above and
the partial variances are given by:

- $V_1 = \frac{1}{2} \, (1 + \frac{b \pi^4}{5})^2$
- $V_2 = \frac{a^2}{8}$
- $V_3 = 0$

The total-effect Sobol' indices, on the other hand:

- $ST_1 \equiv \frac{VT_1}{\mathbb{V}[Y]}$
- $ST_2 \equiv \frac{VT_2}{\mathbb{V}[Y]}$
- $ST_3 \equiv \frac{VT_3}{\mathbb{V}[Y]}$

where:

- $VT_1 = \frac{1}{2} \, (1 + \frac{b \pi^4}{5})^2 + \frac{8 b^2 \pi^8}{225}$
- $VT_2 = \frac{a^2}{8}$
- $VT_3 = \frac{8 b^2 \pi^8}{225}$

The values of the partial variances depend on the parameter values.

```{note}
The Ishigami function has a peculiar dependence on $X_3$;
the main-effect index of the input variable is $0$ but the total-effect index
is not due to an interaction with $X_1$!

Furthermore, as can be seen from the function definition, $X_2$
has no interaction effect; its main-effect and total-effect indices are exactly
the same.
```

## References

```{bibliography}
:style: plain
:filter: docname in docnames
```