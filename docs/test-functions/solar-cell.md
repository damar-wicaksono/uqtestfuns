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

(test-functions:solar-cell)=
# Single-Diode Solar Cell Model

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The test function is a five-dimensional, scalar-valued function that models
the maximum power of a single-diode solar cell. The function was used in
{cite}`Constantine2015` to demonstrate the active subspace method for
input dimension reduction and sensitivity analysis.

For a given voltage, the corresponding current is defined implicitly.
The plot below (left) displays 15 current-voltage curves from 15 different
input variable values.
The dots on the curves indicate the current and voltage values that yield
the maximum cell power; the power curves are shown in the right plot.

```{code-cell} ipython3
:tags: [remove-input]

my_fun = uqtf.SolarCell()
my_fun.prob_input.reset_rng(237324)
num_sample = 15
xx = my_fun.prob_input.get_sample(num_sample)

n_s = my_fun.parameters["n_s"]
v_th = my_fun.parameters["v_th"]
def compute_ii(vv, xx, ns, v_th):
    ii = np.empty((len(vv), len(xx)))
    for idx_1 in range(len(xx)):
        x = xx[idx_1]
        for idx_2 in range(len(vv)):
            v = vv[idx_2]
            ii[idx_2, idx_1] = uqtf.test_functions.solar_cell.compute_current(
                v,
                x,
                n_s,
                v_th,
            ).squeeze()

    return ii

vv = np.linspace(0, 1.4, 1000)
ii = compute_ii(vv, xx, n_s, v_th)

pp_max, vv_max = uqtf.test_functions.solar_cell.compute_power_max(
    xx,
    n_s,
    v_th,
)
ii_max = np.array(
    [
        uqtf.test_functions.solar_cell.compute_current(
            vv_max[k],
            xx[k],
            n_s,
            v_th,
        ).squeeze()
        for k in range(num_sample)
    ]
)

# --- Create a series of plots
fig = plt.figure(figsize=(10, 5))

# Current-voltage curves
axs_1 = plt.subplot(121)
for i in range(len(xx)):
    axs_1.plot(vv, ii[:, i], color="#8da0cb")
axs_1.set_ylim([0.0, 0.3])
axs_1.set_xlim([0.0, 1.5])
axs_1.scatter(vv_max, ii_max, color="#8da0cb")
axs_1.grid()
axs_1.set_xlabel("Voltage (V)", fontsize=14)
axs_1.set_ylabel("Current (A)", fontsize=14)
axs_1.set_title("Current-voltage curves")

# Power-voltage curves
axs_2 = plt.subplot(122)
for i in range(len(xx)):
    axs_2.plot(vv, ii[:, i] * vv, color="#8da0cb")
axs_2.scatter(vv_max, pp_max, color="#8da0cb")
axs_2.set_ylim([0.0, 0.18])
axs_2.set_xlim([0.0, 1.5])
axs_2.grid()
axs_2.set_xlabel("Voltage (V)", fontsize=14)
axs_2.set_ylabel("Power (W)", fontsize=14)
axs_2.set_title("Power-voltage curves")

plt.gcf().tight_layout(pad=4.0)
plt.gcf().set_dpi(150);
```

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.SolarCell()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The model predicts the maximum power of a single-diode solar cell defined
in the following formula:

$$
\mathcal{M}(\boldsymbol{x}; \boldsymbol{p}) = \max_{I, V}  I(V; \boldsymbol{x}, \boldsymbol{p}) V,
$$

where the current ($I$) is defined implicitly as a function of the voltage ($V$),
input variables $\boldsymbol{x}$ and parameters $\boldsymbol{p}$.
The implicit relationshow is described by the following equation:

$$
I(V; \boldsymbol{x}, \boldsymbol{p}) = I_L - I_S \left( \exp{\left( \frac{V + I R_S}{n_S \, n \, V_{\text{th}}} \right) } - 1 \right) - \frac{V + I R_S}{R_P},
$$

where $I_L$, the photocurrent, is defined by the auxiliary equation:

$$
I(\boldsymbol{x}, \boldsymbol{p}) = I_{SC} + I_S \left( \exp{ \left( \frac{I_{SC} R_S}{n_S \, n \, V_{\text{th}}} \right) } - 1 \right) + \frac{I_{SC} R_S}{R_P}.
$$

Here, $\boldsymbol{x} = \left( I_{SC}, I_S, n, R_S, R_P \right)$ represents
the five-dimensional the vector of input variables probabilistically defined below.
The vector $\boldsymbol{p} = \left( n_s, V_{\text{th}} \right)$ contains fixed parameters,
which are also further detailed below.

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

## Reference results

This section provides several reference results of typical UQ analyses involving
the test function.

### Sample histogram

Shown below is the histogram of the output based on $1000$ random points:

```{code-cell} ipython3
:tags: [hide-input]

xx_test = my_testfun.prob_input.get_sample(1000)
yy_test = my_testfun(xx_test)

plt.hist(yy_test, bins="auto", color="#8da0cb");
plt.grid();
plt.ylabel("Counts [-]");
plt.xlabel("$\mathcal{M}(\mathbf{X})$");
plt.gcf().set_dpi(150);
```

## Notes on numerical algorithms

The maximum power of the solar cell model is computed numerically
using the following methods:

- [`root()`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.root.html)
  from SciPy, with its default method and parameter values,
  to solve the implicit current as a function of voltage.
- [`minimize()`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html)
  from SciPy, with its default method (i.e., `BFGS`) and parameter values,
  to find the maximum power by optimizing over the voltage (the current is
  is computed on-the-fly during the iteration).

The default parameter values for these methods can be overridden by providing
a dictionary with new parameter values. For example:

To override the tolerance value for `root()`:

```python
fun.parameters.add("root", {"tol": 1e-12})  # 'root' as the parameter keyword
```

To override the tolerance value for `minimize()`:

```python
fun.parameters.add("minimize", {"tol": 1e-12})  # 'minimize' as the parameter keyword
```

```{note}
In this example, `tol` is acceptable keyword-named argument for both `root()`
and `minimize()`; indeed, the key-value pairs specified for the parameters
`root` and `minimize` must be recognized by the respective methods.
```

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: See Eqs. (9-12), Section 3.1 in {cite}`Constantine2015`.
