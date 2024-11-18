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

(test-functions:undamped-oscillator)=
# Undamped Oscillator

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

The undamped oscillator function (`UndampedOscillator`) is a six-dimensional,
scalar-valued test function that models a non-linear, undamped,
single-degree-of-freedom, forced oscillating mechanical system.

This function is frequently used as a test function for reliability analysis
methods (see  {cite}`Bucher1990, Rajashekhar1993, Gayton2003, Schueremans2005, Echard2011, Echard2013`).
Additionally, in {cite}`Luethen2021`, the function is employed
as a test function for metamodeling exercises.

## Test function instance

To create a default instance of the test function:

```{code-cell} ipython3
my_testfun = uqtf.UndampedOscillator()
```

Check if it has been correctly instantiated:

```{code-cell} ipython3
print(my_testfun)
```

## Description

The system under consideration is a single-degree-of-freedom mechanical system
that undergoes undamped forced oscillation.
The performance function is analytically defined as follows[^location]:

$$
g(\boldsymbol{x}) = 3 r - \lvert z_{\text{max}} \rvert,
$$

where $z_{\text{max}}$ is the maximum displacement response of the system
given by

$$
z_{\text{max}} (\boldsymbol{x}) = \frac{2 F_1}{m \omega_0^2} \sin{\left( \frac{\omega_0 t_1}{2} \right)}
$$

and

$$
\omega_0 = \sqrt{\frac{c_1 + c_2}{m}}.
$$


$\boldsymbol{x} = \{ m, c_1, c_2, r, F_1, t_1 \}$ is the six-dimensional vector
of input variables probabilistically defined further below.

The failure state and the failure probability are defined as
$g(\boldsymbol{x}; \boldsymbol{p}) \leq 0$
and $\mathbb{P}[g(\boldsymbol{X}; \boldsymbol{p}) \leq 0]$, respectively.

## Probabilistic input

The available probabilistic input models are shown in the table below.
The different specifications alter the failure probability of the system
(as expected).

```{table} Available probabilistic input of the undamped oscillator function
:name: undamped-oscillator-inputs
| No. |       Remark       |        Keyword         |            Source            |  
|:---:|:------------------:|:----------------------:|:----------------------------:|  
| 1.  | $\mu_{F_1} = 1.00$ | `Gayton2003` (default) | {cite}`Gayton2003` (Table 9) |  
| 2.  | $\mu_{F_1} = 0.60$ |     `Echard2013-1`     | {cite}`Echard2013` (Table 4) |
| 3.  | $\mu_{F_1} = 0.45$ |     `Echard2013-2`     | {cite}`Echard2013` (Table 4) |
```

The default input is shown below.

```{code-cell} ipython3
:tags: [hide-input]

print(my_testfun.prob_input)
```

## Reference results

This section provides several reference results of typical UQ analyses involving
the test function.

### Sample histogram

Shown below is the histogram of the output based on $10^6$ random points:

```{code-cell} ipython3
:tags: [hide-input]

xx_test = my_testfun.prob_input.get_sample(1000000)
yy_test = my_testfun(xx_test)
idx_pos = yy_test > 0
idx_neg = yy_test <= 0

hist_pos = plt.hist(yy_test, bins="auto", color="#0571b0")
plt.hist(yy_test[idx_neg], bins=hist_pos[1], color="#ca0020")
plt.axvline(0, linewidth=1.0, color="#ca0020")

plt.grid()
plt.ylabel("Counts [-]")
plt.xlabel("$g(\mathbf{X})$")
plt.gcf().set_dpi(150);
```

### Failure probability ($P_f$)

Some reference values for the failure probability $P_f$ from the literature
are summarized in the tables below according to the chosen input specification.

::::{tab-set}

:::{tab-item} Gayton2003
|                 Method                 |        $N$        |      $\hat{P}_f$       | $\mathrm{CoV}[\hat{P}_f]$ |              Source               |
|:--------------------------------------:|:-----------------:|:----------------------:|:-------------------------:|:---------------------------------:|
|               {term}`DS`               |      $1281$       |  $3.5 \times 10^{-2}$  |          &#8212;          | {cite}`Schueremans2005` (Table 5) |
|        {term}`DS` + Polynomial         |       $62$        |  $3.4 \times 10^{-2}$  |          &#8212;          | {cite}`Schueremans2005` (Table 5) |
|          {term}`DS` + Splines          |       $76$        |  $3.4 \times 10^{-2}$  |          &#8212;          | {cite}`Schueremans2005` (Table 5) |
|    {term}`DS` + Neural network (NN)    |       $86$        |  $2.8 \times 10^{-2}$  |          &#8212;          | {cite}`Schueremans2005` (Table 5) |
|        {term}`MCS` + {term}`IS`        |      $6144$       |  $2.7 \times 10^{-2}$  |          &#8212;          | {cite}`Schueremans2005` (Table 5) |
| {term}`MCS` + {term}`IS` + Polynomials |       $109$       |  $2.5 \times 10^{-2}$  |          &#8212;          | {cite}`Schueremans2005` (Table 5) |
|   {term}`MCS` + {term}`IS` + Splines   |       $67$        |  $2.7 \times 10^{-2}$  |          &#8212;          | {cite}`Schueremans2005` (Table 5) |
|     {term}`MCS` + {term}`IS` + NN      |       $68$        |  $3.1 \times 10^{-2}$  |          &#8212;          | {cite}`Schueremans2005` (Table 5) |
|              {term}`MCS`               | $7 \times 10^{4}$ | $2.834 \times 10^{-2}$ |          $2.2\%$          |   {cite}`Echard2011` (Table 6)    |
|  Adaptive Kriging + {term}`MCS` + EFF  |       $58$        | $2.834 \times 10^{-2}$ |          &#8212;          |   {cite}`Echard2011` (Table 6)    |
|   Adaptive Kriging + {term}`MCS` + U   |       $45$        | $2.851 \times 10^{-2}$ |          &#8212;          |   {cite}`Echard2011` (Table 6)    |
:::

:::{tab-item} Echard2013-1
|            Method             |         $N$          |      $\hat{P}_f$      | $\mathrm{CoV}[\hat{P}_f]$ |            Source            |
|:-----------------------------:|:--------------------:|:---------------------:|:-------------------------:|:----------------------------:|
|          {term}`MCS`          | $1.8 \times 10^{8}$  | $9.09 \times 10^{-6}$ |         $2.47\%$          | {cite}`Echard2013` (Table 5) |
|         {term}`FORM`          |         $29$         | $9.76 \times 10^{-6}$ |          &#8212;          | {cite}`Echard2013` (Table 5) |
|          {term}`IS`           | $20 + \times 10^{4}$ | $9.13 \times 10^{-6}$ |         $2.29\%$          | {cite}`Echard2013` (Table 5) |
| Adaptive Kriging + {term}`IS` |      $29 + 38$       | $9.13 \times 10^{-6}$ |         $2.29\%$          | {cite}`Echard2013` (Table 5) |
:::

:::{tab-item} Echard2013-2
|            Method             |         $N$          |      $\hat{P}_f$      | $\mathrm{CoV}[\hat{P}_f]$ |            Source            |
|:-----------------------------:|:--------------------:|:---------------------:|:-------------------------:|:----------------------------:|
|          {term}`MCS`          |  $9 \times 10^{8}$   | $1.55 \times 10^{-8}$ |         $2.68\%$          | {cite}`Echard2013` (Table 5) |
|         {term}`FORM`          |         $29$         | $1.56 \times 10^{-8}$ |          &#8212;          | {cite}`Echard2013` (Table 5) |
|          {term}`IS`           | $29 + \times 10^{4}$ | $1.53 \times 10^{-8}$ |         $2.70\%$          | {cite}`Echard2013` (Table 5) |
| Adaptive Kriging + {term}`IS` |      $29 + 38$       | $1.54 \times 10^{-8}$ |         $2.70\%$          | {cite}`Echard2013` (Table 5) |
:::

::::


## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^location]: see Section 6.4.1 in {cite}`Gayton2003`.