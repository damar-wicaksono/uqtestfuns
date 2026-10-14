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

(test-functions:saturated-point-heat-source)=
# Thermal Consolidation around a Point Heat Source in Saturated Porous Media from Chaudhry et al. (2021)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

Thermal consolidation around a point heat source (`SaturatedPointHeatSource`)
describes the coupled thermo-hydro-mechanical response of a water-saturated
porous rock to a steady point source of heat.
The model yields three output fields: temperature change $\Delta T$,
excess pore pressure $p$, and radial displacement $u_r$.
It appeared in {cite}`Chaudhry2021` as a test case for global sensitivity analysis.

The three output fields evaluated at the nominal parameter values
are shown in the figures below.

```{code-cell} ipython3
:tags: [remove-input]

my_fun = uqtf.SaturatedPointHeatSource()

# Mean for normal/trunc-normal (mu parameter); median for uniform; mode for triangular
def _marginal_central(m):
    if m.distribution == "uniform":
        return (m.parameters[0] + m.parameters[1]) / 2.0
    if m.distribution == "triangular":
        return float(m.parameters[2])
    return float(m.parameters[0])

xx = np.array([[_marginal_central(m) for m in my_fun.prob_input.marginals]])
yy = my_fun(xx)  # (1, 3, N_r, N_t)

rr = np.asarray(my_fun.parameters["rr"])
tt_days = np.asarray(my_fun.parameters["tt"]) / 86400.0
tt_years = tt_days / 365.0

titles = [r"$\Delta T$ [K]", r"$p$ [Pa]", r"$u_r$ [m]"]
fig, axes = plt.subplots(1, 3, figsize=(13, 4))

for i, (ax, title) in enumerate(zip(axes, titles)):
    for j in range(len(rr)):
        ax.plot(tt_years, yy[0, i, j, :], marker="o", ms=4)
    ax.set_xlabel("Time [years]", fontsize=12)
    ax.set_ylabel(title, fontsize=12)

fig.tight_layout()
fig.set_dpi(150)
```

The same output fields can also be viewed as a color map over the full
spatial-temporal grid:

```{code-cell} ipython3
:tags: [remove-input]

titles = [r"$\Delta T$ [K]", r"$p$ [Pa]", r"$u_r$ [m]"]
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for i, (ax, title) in enumerate(zip(axes, titles)):
    pc = ax.pcolormesh(rr, tt_days, yy[0, i].T, shading="auto", cmap="plasma")
    ax.set_xlim(rr[0], rr[-1])
    ax.set_xlabel("Radius [m]", fontsize=12)
    ax.set_ylabel("Time [days]", fontsize=12)
    ax.set_title(title, fontsize=12)
    fig.colorbar(pc, ax=ax)

fig.tight_layout()
fig.set_dpi(150)
```


## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.SaturatedPointHeatSource()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The analytical solution for thermal consolidation around a steady point heat
source $Q$ [W] in a water-saturated porous rock gives three coupled output
fields as functions of radial distance $r$ and time $t$
{cite}`Booker1985,Chaudhry2019`:

**Temperature change:**

$$
\Delta T(r, t) = \frac{Q}{4 \pi K r}\, f^\kappa(r, t),
$$

**Excess pore pressure:**

$$
p(r, t) = \frac{P_1 Q}{4 \pi K r}\, \left[ f^\kappa(r, t) - f^c(r, t) \right],
$$

**Radial displacement:**

$$
u_r(r, t) = \frac{Q}{4 \pi K M}\, \left[ (b' + P_1)\, g^\kappa(r, t) - P_1\, g^c(r, t) \right],
$$

where $A \in \{ \kappa, c \}$ denotes the diffusivity (thermal or hydraulic),
and the front function $f^A$ and displacement shape function $g^A$ are[^eqs]:

$$
f^A(r, t) = \mathrm{erfc}\!\left( \frac{r}{2\sqrt{A t}} \right),
$$

$$
g^A(r, t) = \frac{A t}{r^2} + \left( \frac{1}{2} - \frac{A t}{r^2} \right) f^A(r, t)
             - \sqrt{\frac{A t}{\pi r^2}}\, \exp\!\left( -\frac{r^2}{4 A t} \right).
$$

The derived quantities are computed from the uncertain inputs as:

$$
\kappa = \frac{K}{C \rho}, \quad
\lambda = \frac{E \nu}{(1 + \nu)(1 - 2\nu)}, \quad
G = \frac{E}{2(1 + \nu)}, \quad
M = \lambda + 2G,
$$

$$
c = \frac{k_s}{\mu_w}\, M, \quad
\alpha_u = \phi\, \alpha_w + (1 - \phi)\, \alpha_s, \quad
b' = \left( \lambda + \tfrac{2}{3} G \right) \alpha_s, \quad
P_1 = \frac{\alpha_u M - b'}{1 - c / \kappa}.
$$

The test function evaluates all three fields on a grid of $N_r$ radii
$\boldsymbol{r} = (r_1, \ldots, r_{N_r})$ and $N_t$ times
$\boldsymbol{t} = (t_1, \ldots, t_{N_t})$:

$$
\mathcal{M}(\boldsymbol{x}; \boldsymbol{p})
= \Bigl(\Delta T(r_i, t_j),\; p(r_i, t_j),\; u_r(r_i, t_j)\Bigr),
\quad i = 1, \ldots, N_r,\; j = 1, \ldots, N_t,
$$

where:

- $\boldsymbol{x} = (K, C, \rho, E, \alpha_s, k_s, \nu, \phi)$ is the
  eight-dimensional vector of uncertain input variables, defined further below.
- $\boldsymbol{p} = \{ Q, \alpha_w, \mu_w, \boldsymbol{r}, \boldsymbol{t} \}$
  are the model parameters defined further below.

The output has shape $(3, N_r, N_t)$ per sample.

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

## Reference Results

This section provides reference results of typical UQ analyses
involving the test function.

### Importance ranking

The table below shows the ranking of the eight uncertain input parameters
by their first-order Sobol' indices for each output field,
as read from Fig. 16 of {cite}`Chaudhry2021`.
Rankings are derived from the maximum first-order index over all grid
points $(r_i, t_j)$, with rank 1 being the most influential.

| Parameter  | $\Delta T$ | $p$ | $u_r$ |
|:----------:|:----------:|:---:|:-----:|
|    $K$     |     1      |  7  |   1   |
|    $C$     |     2      |  6  |   5   |
|   $\rho$   |     3      |  8  |   8   |
|    $E$     |    N/A     |  2  |   7   |
| $\alpha_s$ |    N/A     |  3  |   3   |
|   $k_s$    |    N/A     |  1  |   2   |
|   $\nu$    |    N/A     |  5  |   6   |
|   $\phi$   |    N/A     |  4  |   4   |

N/A indicates that the parameter does not enter the expression for that output
field[^na].
Although $\rho$ ranks last for $p$ and $u_r$, its index is not exactly zero:
it enters through the thermal diffusivity $\kappa = K / (C\rho)$,
which drives both fields; its narrow prior range keeps its contribution close
to, but strictly above, zero.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^eqs]: See Eqs. (18)-(19) for $f^A$ and $g^A$, and Eqs. (23)-(25) for the three output fields, all in {cite}`Chaudhry2019`.
[^na]: $E$, $\alpha_s$, $k_s$, $\nu$, and $\phi$ appear only in the mechanical
and hydraulic terms and do not enter the temperature expression;
$\Delta T$ depends solely on $K$, $C$, and $\rho$ through $\kappa = K/(C\rho)$.
