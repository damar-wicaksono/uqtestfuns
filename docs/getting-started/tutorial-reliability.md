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

(getting-started:tutorial-reliability)=
# Tutorial: Test a Reliability Analysis Method

UQTestFuns includes several test functions from the literature used
in reliability analysis.
In this tutorial, you'll implement a method to estimate the failure probability
of a computational model and try it out on a test function from UQTestFuns.

By the end, you'll understand how a UQTestFuns function lets you
test a reliability analysis method.
A reliability problem asks what is the probability a system fails
under uncertain inputs,
so it is well-posed once those inputs' distribution is fixed;
each UQTestFuns function comes with one.
For the cantilever beam problem used here,
the literature also provides published estimates of the failure probability,
giving you reference values to check against.

```{code-cell}
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

## Reliability analysis

Consider a system whose performance is defined by a *performance function*[^lsf] $g$.
Its value depends on:

- $\boldsymbol{x}_p$: the (uncertain) input variables to an underlying 
  computational model $\mathcal{M}$;
- $\boldsymbol{x}_s$: additional (uncertain) input variables that affect
  the system's performance but are not arguments of $\mathcal{M}$;
- $\boldsymbol{p}$: a set of *deterministic* parameters of the system.

These combine into the performance function as

$$
g(\boldsymbol{x}; \boldsymbol{p}) = g(\mathcal{M}(\boldsymbol{x}_p), \boldsymbol{x}_s; \boldsymbol{p}),
$$

where $\boldsymbol{x} = \{ \boldsymbol{x}_p, \boldsymbol{x}_s \}$.

The system is in a *failure state* if and only if $g(\boldsymbol{x}; \boldsymbol{p}) \leq 0$;
the set of all values ${ \boldsymbol{x}, \boldsymbol{p} }$
such that $g(\boldsymbol{x}; \boldsymbol{p}) \leq 0$
is called the *failure domain*.

Conversely, the system is in a *safe state*
if and only if $g(\boldsymbol{x}; \boldsymbol{p}) > 0$;
the set of all values ${ \boldsymbol{x}, \boldsymbol{p} }$
such that $g(\boldsymbol{x}; \boldsymbol{p}) > 0$ is called the *safe domain*.

### Failure probability

*Reliability analysis*[^rare-event] is concerned with estimating
the failure probability of a system with a given performance function $g$.
For a given joint probability density function (PDF) $f_{\boldsymbol{X}}$
of the uncertain input variables $\boldsymbol{X} = \{ \boldsymbol{X}_p, \boldsymbol{X}_s \}$,
the failure probability $P_f$ is defined as {cite}`Sudret2012, Verma2015`:

$$
P_f \equiv \mathbb{P}[g(\boldsymbol{X}; \boldsymbol{p}) \leq 0] = \int_{\{ \boldsymbol{x} \, \mid \, g(\boldsymbol{x}; \boldsymbol{p}) \leq 0 \}} f_{\boldsymbol{X}} (\boldsymbol{x}) \, d\boldsymbol{x}.
$$

Evaluating this integral is generally non-trivial:
the integration domain is given only implicitly,
and the dimension may be high.

### Monte-Carlo estimation

```{warning}
The Monte-Carlo method implemented below is one of the most straightforward
and robust approaches for estimating a (small) failure probability.
It is rarely used in practice, however, because of its high computational cost,
and it appears here purely as an illustration.
Numerous methods have been developed to estimate a failure probability
more efficiently and accurately.
```

The failure probability of a computational model with probabilistic inputs
can be estimated directly by Monte-Carlo simulation.

The method is straightforward to implement but potentially expensive:
in a typical reliability problem,
the chance of observing a failure event is very small
and thus large sample size must be generated.

An alternative formulation of the failure probability,
following {cite}`Beck2015` and well suited to Monte-Carlo simulation,
is given below:

$$
P_f \equiv \mathbb{P}[g(\boldsymbol{X}; \boldsymbol{p}) \leq 0] = \int_{\mathcal{D}_{\boldsymbol{X}}} \mathbb{I}[g(\boldsymbol{x}; \boldsymbol{p}) \leq 0] \, f_{\boldsymbol{X}} (\boldsymbol{x}) , d\boldsymbol{x},
$$

where $\mathbb{I}[g(\boldsymbol{x}; \boldsymbol{p}) \leq 0]$
is the indicator function such that

$$
\mathbb{I}[g(\boldsymbol{x}; \boldsymbol{p}) \leq 0] = \begin{cases} 1, & g(\boldsymbol{x}; \boldsymbol{p}) \leq 0, \\ 0, & g(\boldsymbol{x}; \boldsymbol{p}) > 0. \end{cases}
$$

The Monte-Carlo estimate of the failure probability is

$$
P_f \approx \widehat{P}_f = \frac{1}{N} \sum_{i = 1}^{N} \mathbb{I}[g(\boldsymbol{x}^{(i)}; \boldsymbol{p}) \leq 0],
$$

where $N$ is the number of Monte-Carlo sample points.

To assess the accuracy of this estimate,
the coefficient of variation ($\mathrm{CoV}$) is often used:

$$
\mathrm{CoV}[\widehat{P}_f] \equiv \frac{\left( \mathbb{V}[\widehat{P}_f] \right)^{1/2}}{\mathbb{E}[\widehat{P}_f]} = \left( \frac{1 - \widehat{P}_f}{N \widehat{P}_f} \right)^{1/2}.
$$

The Monte-Carlo simulation for estimating the failure probability is summarized
in {prf:ref}`MC Simulation Pf`.


```{prf:algorithm}
:label: MC Simulation Pf

**Inputs** A performance function $g$, random input variables $\boldsymbol{X}$,
a set of deterministic parameters $\boldsymbol{p}$,
number of MC sample points $N$

**Output** $\widehat{P}_f$ and $\mathrm{CoV}[\widehat{P}_f]$

1. $N_f \leftarrow 0$
2. For $i = 1$ to $N$:

    1. Sample $\boldsymbol{x}^{(i)}$ from $\boldsymbol{X}$
    2. Evaluate $g(\boldsymbol{x}^{(i)}; \boldsymbol{p})$
    3. If $g(\boldsymbol{x}^{(i)}; \boldsymbol{p}) \leq 0$:

        - $N_f \leftarrow N_f + 1$

3. $\widehat{P}_f \leftarrow \frac{N_f}{N}$
4. $\mathrm{CoV}[\widehat{P}_f] \leftarrow \left( \frac{1 - \widehat{P}_f}{N \widehat{P}_f} \right)^{1/2}$
```

```{margin}
Indeed, every test function in UQTestFuns comes
with a probabilistic input model taken from the literature.
```

{prf:ref}`MC Simulation Pf` is implemented below as a Python function.
It assumes the performance function can be evaluated in a vectorized manner
and that a probabilistic input model has been defined
so that sample points can be drawn from it.

```{code-cell}
:tags: [hide-input]

def estimate_pf(performance_function, prob_input, sample_size, rng):
    """Estimate failure probability via MC simulation.

    Parameters
    ----------
    performance_function
      The function to be evaluated; accepts a vector of values as the input.
    prob_input
      The probabilistic input model of the performance function.
    sample_size
      The Monte-Carlo simulation sample size.
    rng
      An instance of a NumPy random number generator used to draw the sample.

    Returns
    -------
    Tuple
      The estimated failure probability and its coefficient of variation (CoV).
    """

    xx = prob_input.get_sample(sample_size, rng=rng)
    yy = performance_function(xx)

    pf = np.sum(yy <= 0) / sample_size
    cov = np.sqrt((1 - pf) / (sample_size * pf))

    return pf, cov
```

## Two-dimensional cantilever beam reliability problem

To test the algorithm above,
we use the {ref}`two-dimensional cantilever beam reliability problem <test-functions:cantilever-beam-2d>`
included in UQTestFuns, for which several published results are available.

The problem consists of a cantilever beam with a rectangular cross-section
under a uniformly distributed load.

The maximum deflection at the free end serves as the performance criterion,
so the performance function reads

$$
g(\boldsymbol{x}; \boldsymbol{p}) = \frac{l}{325} - \frac{12 \, l^4 w}{8 \, E h^3},
$$

where $\boldsymbol{x} = \{ w, h \}$ collects the input variables:
the load per unit area ($w$) and the depth of the cross-section ($h$).
The parameters $\boldsymbol{p} = \{ E, l \}$
are the modulus of elasticity ($E$) and the span of the beam ($l$).

Create an instance of the cantilever beam function:

```{code-cell}
cantilever = uqtf.CantileverBeam2D()
```

The input variables $w$ and $h$ are defined probabilistically as shown below:

```{code-cell}
print(cantilever.prob_input)
```

The default values of the parameters $E$ and $l$ are:

```{code-cell}
print(cantilever.parameters)
```

Finally, several published estimates of the failure probability are available for this problem:

- $\widehat{P}_f = 9.88 \times 10^{-3}$, using {term}`FORM`
  with $27$ performance function evaluations {cite}`Li2018`;
- $\widehat{P}_f = 9.6071 \times 10^{-3}$, using {term}`IS`
  with $10^3$ performance function evaluations {cite}`Rajashekhar1993`;
- $\widehat{P}_f = 9.499 \times 10^{-3}$,
  using a sequential surrogate reliability method
  with $18$ performance function evaluations {cite}`Li2018`.

## Failure probability estimation

To observe the convergence of the procedure,
we estimate the failure probability at several Monte-Carlo sample sizes.
For reproducibility, we create a random number generator with a fixed seed
and pass it to each call, so the successive estimates draw from a single,
advancing stream:

```{code-cell}
rng = np.random.default_rng(245634)

sample_sizes = 5 ** np.arange(3, 12)
pf_estimates = np.zeros(len(sample_sizes))
cov_estimates = np.zeros(len(sample_sizes))

for i, sample_size in enumerate(sample_sizes):
    pf_estimates[i], cov_estimates[i] = estimate_pf(
        cantilever, cantilever.prob_input, sample_size, rng
    )
```

The estimated failure probability is plotted below against the sample size,
with an uncertainty band of one standard deviation around each estimate.

```{code-cell}
:tags: [hide-input]

fig, ax = plt.subplots(1, 1)

ax.plot(sample_sizes, pf_estimates, color="k", linewidth=1.0)
ax.plot(
    sample_sizes, pf_estimates * (1 + cov_estimates), color="k", linestyle="--"
)
ax.plot(
    sample_sizes, pf_estimates * (1 - cov_estimates), color="k", linestyle="--"
)
ax.fill_between(
    sample_sizes,
    pf_estimates * (1 + cov_estimates),
    pf_estimates * (1 - cov_estimates),
    color="gray",
)
ax.axhline(y=9.88e-3, color="black", linestyle="--", label="FORM")
ax.axhline(y=9.6071e-3, label="IS", color="black", linestyle="-.")
ax.axhline(y=9.499e-3, color="black", linestyle=":", label="Surrogate")
ax.grid()
ax.legend(fontsize=14)
ax.set_ylim([0.004, 0.016])
ax.set_xscale("log")
ax.set_xlabel("MC sample size", fontsize=14)
ax.set_ylabel(r"$\widehat{P}_f$", fontsize=14);
```

The final estimate of the failure probability,
from more than $10^7$ function evaluations, is:

```{code-cell}
print(f"{pf_estimates[-1]:1.4e}")
```

This value is consistent with the published results above,
though it comes at a much higher computational cost.
Such a cost is acceptable here
only because the cantilever beam is an inexpensive analytic test function;
for a real computational model,
where a single evaluation may take minutes or hours (even days!),
obtaining more than $10^7$ evaluations would be unrealistic.

## Trying another problem

Because `estimate_pf()` takes the test function
and its probabilistic input as arguments,
nothing in it is specific to the cantilever beam problem.
To test your method on a different reliability problem,
change a single line: swap `uqtf.CantileverBeam2D()` for another function,
and the probabilistic input that comes along with it.
For example, the {ref}`four-branch <test-functions:four-branch>`
series-system problem {cite}`Katsuki1994`
is also a two-dimensional reliability function:

```{code-cell}
four_branch = uqtf.FourBranch()

rng = np.random.default_rng(245634)
pf, cov = estimate_pf(four_branch, four_branch.prob_input, 500000, rng)

print(f"{pf:1.4e}")
```

The same method now runs on an entirely different problem,
with the correct input model supplied by the library
rather than provided by hand.
In UQTestFuns, every built-in function shares the same interface,
so a method designed for one works for all of them.
See the full list of
{ref}`test functions for reliability analysis <fundamentals:reliability>`
for the other problems you can drop in.

---

## Summary

In this tutorial, you implemented a Monte-Carlo method
to estimate the failure probability of a computational model
and tried it out on the two-dimensional cantilever beam from UQTestFuns.
Two features of the test function made this validation straightforward:
its probabilistic input model came built in, ready to sample from,
and its published reference results gave you concrete numbers
to check your estimate against.
The estimate converged to a value consistent with the literature,
confirming the implementation works as intended.

This is the role a UQTestFuns test function plays: a known,
well-documented problem against which you can develop
and validate your own reliability analysis method
before applying it to a real computational model.
There, the challenge is to estimate the failure probability
both accurately and efficiently,
i.e., with as few performance function evaluations as possible.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```

[^lsf]: also called _limit-state function_

[^rare-event]: also called rare-events estimation