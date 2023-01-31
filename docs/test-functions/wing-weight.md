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

(test-functions:wing-weight)=
# Wing Weight Function

The Wing Weight test function is a 10-dimensional scalar-valued function {cite}`forresterEngineeringDesignSurrogate2008`.

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns
```

Create an instance of the wing weight test function using
the built-in default arguments:

```{code-cell} ipython3
my_testfun = uqtestfuns.create_from_default("wing-weight")
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```


## Description

The weight of a light aircraft wing is computed using the following analytical expression:

$$
\mathcal{M}(\boldsymbol{x}) = 0.036 \, S_w^{0.758} \, W_{fw}^{0.0035} \, \left( \frac{A}{\cos^2{(\Lambda)}} \right)^{0.6} q^{0.006} \lambda^{0.04} \left(\frac{100 t_c}{\cos{(\Lambda)}}\right)^{-0.3} \left( N_z W_{dg} \right)^{0.49} + S_w W_p 
$$

where $\boldsymbol{x} = \{ S_w, W_{fw}, A, \Lambda, q, \lambda, t_c, N_z, W_{dg}, W_p\}$ is the vector of input variables defined below.

+++

## Probabilistic input

The ten input variables of the wing weight function are modeled as independent uniform random variables with specified ranges shown in the table below.

```{code-cell} ipython3
my_testfun.prob_input
```

## Reference Results

+++

Generate a random sample of input/output pairs:

```{code-cell} ipython3
xx_test = my_testfun.prob_input.get_sample(10000)
yy_test = my_testfun(xx_test)
```

Create a histogram of the raw output (i.e., the weight of the wing):

```{code-cell} ipython3
plt.hist(yy_test, bins="auto");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
```

## References

```{bibliography}
:style: plain
:filter: docname in docnames
```