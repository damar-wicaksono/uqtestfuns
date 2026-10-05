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

(test-functions:coffee-cup)=
# Cooling Coffee Cup Model from Tennøe et al. (2018)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The cooling coffee cup model (`CoffeeCup`) simulates the temperature evolution
of a coffee cup as it cools to an ambient temperature by solving an initial
value problem. As a UQ test function, the model is expressed as a
two-dimensional, vector-valued function. It appeared in {cite}`Tennoee2018`
and {cite}`Richardson2020` as an introductory example for metamodeling.

Some realizations of the temperature evolutions are shown in the figure below.

```{code-cell} ipython3
:tags: [remove-input]

my_fun = uqtf.CoffeeCup()
num_sample = 20
xx = my_fun.prob_input.get_sample(num_sample, 237324)

yy = my_fun(xx)
t_e = 200.0
n_ts = 150
tt = np.linspace(0, t_e, n_ts)

for i in range(len(xx)):
    plt.plot(tt, yy[i, :], color="#8da0cb", alpha=0.5)
plt.grid()
plt.xlabel("Time [s]", fontsize=14)
plt.ylabel("Temperature [degC]", fontsize=14)

plt.gcf().tight_layout()
plt.gcf().set_dpi(150);
```

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.CoffeeCup()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The temperature evolution of a coffee cup, $T(t)$, as it cools down
to an ambient temperature, $T_{\text{amb}}$, is described by
the following initial value problem (IVP)[^location]:

$$
\frac{dT (t)}{dt} = - \kappa (T (t) - T_{\text{amb}}), T \in [ 0, t_e ],
$$

with an initial condition (IC):

$$
T (t = 0) = T_0,
$$

where $\kappa$ is the thermal conductivity of the cup.

The test function is the solution to the IVP evaluated at $n_{ts} = 150$
evenly spaced time points over $[0, t_e]$ with $t_e = 200$ s:

$$
\mathcal{M}(\boldsymbol{x}; \boldsymbol{p}) = \left( T(t_i; \boldsymbol{x}, \boldsymbol{p}) \right), \; i = 0, \ldots, n_{ts},
$$

where:

- $\boldsymbol{x} = \left( \kappa, T_{\text{amb}} \right)$ is a
  two-dimensional vector of uncertain input variables, defined further below.
- $\boldsymbol{p} = \{ T_0 \}$ is the initial temperature of the coffee cup,
  defined further below.

## Probabilistic input

The probabilistic input model for the test function is shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

## Parameters

The default values of the parameters are shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.parameters)
```

## Notes on numerical algorithms

The IVP described above is solved numerically using
[`solve_ivp()`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)
from SciPy with its default method and parameter values.

```{note}
The default solver settings can be overridden by defining a custom parameter
set with a non-null ``solve_ivp_kwargs`` value and passing it at instantiation.
```

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: See Eqs. (18-20), Section 4.1 in {cite}`Tennoee2018`.
