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

(test-functions:rs-speed-reducer-shaft)=
# Speed Reducer Shaft Reliability Problem from Du and Sudjianto (2004)

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The speed reducer shaft test function (`RSSpeedReducerShaft`)
is a five-dimensional reliability problem analyzing
the performance of a shaft in a speed reducer under combined bending
and torsional loading.
The performance is defined as the strength of the shaft minus the stress;
the system fails when this quantity is negative.

The function was introduced by {cite}`Du2004`
and is used as a benchmark for reliability analysis algorithms
(see, for instance, {cite}`Li2018`).

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.RSSpeedReducerShaft()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The function models the performance of a shaft in a speed reducer {cite}`Du2004`.
The performance is defined as the strength of the shaft subtracted by the
stress as follows[^location]:

$$
g(\boldsymbol{x}) = S - \frac{32}{\pi D^3} \sqrt{\frac{F^2 L^2}{16} + T^2},
$$

where $\boldsymbol{x} = \{ D, L, F, T, S \}$
is the five-dimensional vector of input variables probabilistically defined
further below.

The failure event and the failure probability are defined as
$g(\boldsymbol{x}) \leq 0$ and $\mathbb{P}[g(\boldsymbol{X}) \leq 0]$,
respectively.

## Probabilistic input

Based on {cite}`Du2004`, the probabilistic input model
for the speed reducer shaft reliability problem consists of five independent
random variables with marginal distributions shown in the table below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

```{note}
The variables $S$, $D$, and $L$ must be first converted to SI base units
before being substituted into the formula above:

- $S$ from $[\mathrm{MPa}]$ to $[\mathrm{Pa}]$ (multiply by $10^6$)
- $D$ and $L$ from $[\mathrm{mm}]$ to $[\mathrm{m}]$ (multiply by $10^{-3}$)

The forces $F$ and torque $T$ are already in SI base units.
```

## Reference results

This section provides several reference results of typical UQ analyses involving
the test function.

### Sample histogram

Shown below is the histogram of the output based on $10^6$ random points:

```{code-cell} ipython3
:tags: [hide-input]

yy_test = my_testfun.get_sample(1000000)
idx_pos = yy_test > 0
idx_neg = yy_test <= 0

hist_pos = plt.hist(yy_test, bins="auto", color="#0571b0")
plt.hist(yy_test[idx_neg], bins=hist_pos[1], color="#ca0020")
plt.axvline(0, linewidth=1.0, color="#ca0020")

plt.grid()
plt.ylabel("Counts [-]")
plt.xlabel(r"$\mathcal{M}(\mathbf{X})$")
plt.gcf().set_dpi(150);
```

### Failure probability

Some reference values for the failure probability $P_f$ and from the literature
are summarized in the table below.

|    Method     |   $N$   |       $\hat{P}_f$       | $\mathrm{CoV}[\hat{P}_f]$ |          Source           |
|:-------------:|:-------:|:-----------------------:|:-------------------------:|:-------------------------:|
|  {term}`MCS`  | $10^6$  | $7.850 \times 10^{-4}$  |          &#8212;          | {cite}`Du2004` (Table 11) |
| {term}`FORM`  | $1'472$ | $7.007 \times 10^{-7}$  |          &#8212;          | {cite}`Du2004` (Table 11) |
| {term}`SORM`  | $1'514$ | $4.3581 \times 10^{-7}$ |          &#8212;          | {cite}`Du2004` (Table 11) |
| {term}`FOSPA` |  $102$  | $6.1754 \times 10^{-4}$ |          &#8212;          | {cite}`Du2004` (Table 11) |
| {term}`SSRM`  |  $44$   |  $7.52 \times 10^{-3}$  |          &#8212;          | {cite}`Li2018` (Table 9)  |

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: See Eq. (34), p. 1205 in {cite}`Du2004`.
