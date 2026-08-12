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

(getting-started:tutorial-sensitivity)=
# Tutorial: Test a Sensitivity Analysis Method

UQTestFuns includes a wide range of test functions from the literature used
in sensitivity analysis.
In this tutorial, you'll implement a sensitivity analysis method
and try it out on a test function from UQTestFuns:
the popular Ishigami function.
You'll then compare the estimates against known analytical results.

By the end, you'll understand how a UQTestFuns function lets you verify
a global sensitivity analysis method. In global sensitivity analysis,
the probabilistic input is part of the problem: both the function
and its probabilistic input specification define what the sensitivity indices
even mean. Each UQTestFuns function bundles both in one object.
Furthermore, the sensitivity indices of the Ishigami function are analytically
 available, giving you exact values to check against.

```{code-cell}
import numpy as np
import matplotlib.pyplot as plt
import uqtestfuns as uqtf
```

## Global sensitivity analysis

Sensitivity analysis is a model inference technique whose overarching goal
is to understand the input/output relationship of a complex,
potentially black-box model. In short: *how the inputs affect the output*.

A *global* sensitivity analysis is usually distinguished from a *local* one.
A local analysis concerns the effect on the output of perturbations around
a particular instance of the inputs (e.g., their nominal values).
A global analysis, by contrast, concerns the effect of variations
across the inputs' entire uncertainty ranges.

The specific goals of global sensitivity analysis include:

- *identifying the inputs that drive output uncertainty*, which supports
  *factor prioritization*: ranking inputs by how much reducing
  their uncertainty would reduce the output uncertainty.
- *identifying non-influential inputs*, which supports *factor fixing*:
  determining which inputs can be fixed with minimal effects on
  the output uncertainty.

### Variance decomposition

Consider an $M$-dimensional function $\mathcal{M}:
\mathcal{D}_{\boldsymbol{X}} = [0, 1]^M \to \mathbb{R}$ representing
a computational model of interest.

Because the inputs are uncertain, represented by an $M$-dimensional random
vector $\boldsymbol{X}$, the model output becomes a random variable
$Y = \mathcal{M}(\boldsymbol{X})$.

We further assume that the components $X_m$ of $\boldsymbol{X}$ are mutually
independent,
so that the joint probability density function (PDF) $f_{\boldsymbol{X}}$
factorizes:

$$
f_{\boldsymbol{X}}(\boldsymbol{x}) = \prod_{m=1}^M f_{X_m}(x_m)
$$

where $f_{X_m}$ is the marginal PDF of $X_m$.

```{margin}
Variance is now used to measure the more general (perhaps rather vague)
notion of *uncertainty* in both the inputs and the output.
```

The Hoeffding-Sobol' decomposition expresses the variance of $Y$ as a sum
of contributions from every subset of the inputs.
Let $\boldsymbol{u} \subseteq \{ 1, \ldots, M \}$ index such a subset,
and let $\boldsymbol{X}_{\boldsymbol{u}}$ denote the corresponding group of
input variables. The decomposition then reads:

$$
\mathbb{V}[Y] = \sum_{\lvert \boldsymbol{u} \rvert > 0}^M V_{\boldsymbol{u}}
$$

where the sum runs over all non-empty subsets $\boldsymbol{u}$
and each $V_{\boldsymbol{u}}$ is the *partial variance* attributable
to the interaction of the variables in $\boldsymbol{X}_{\boldsymbol{u}}$.
For a single input ($\boldsymbol{u} = { m }$), the partial variance is

$$
V_m = \mathbb{V}_{X_m} \left[ \mathbb{E}_{\boldsymbol{X}_{\sim m}} \left[ Y \mid X_m \right] \right],
$$

where $\boldsymbol{X}_{\sim m}$ denotes all input variables *except* $X_m$. 

### Sobol' sensitivity indices

Dividing the variance decomposition by the total variance $\mathbb{V}[Y]$ gives

$$
1 = \sum_{\lvert \boldsymbol{u} \rvert > 0} S_{\boldsymbol{u}}, \quad \text{where} \quad S\_{\boldsymbol{u}} = \frac{V_{\boldsymbol{u}}}{\mathbb{V}[Y]}.
$$

Each $S_{\boldsymbol{u}}$ is a normalized partial variance,
called a Sobol' sensitivity index.
There are $2^M - 1$ of them, one per non-empty subset of the $M$ inputs.

Of particular importance is the *first-order* (or *main-effect*) index $S_m$,
the index of the singleton $\boldsymbol{u} = \{ m \}$ {cite}`Sobol1993`:

$$
S_m = \frac{\mathbb{V}_{X_m} \left[ \mathbb{E}_{\boldsymbol{X}_{\sim m}} \left[ Y \mid X_m \right] \right]}{\mathbb{V}[Y]}.
$$

It measures the contribution of $X_m$ acting alone to the output variance,
and thus in line with the *factor prioritization* goal above.

The other widely used index is the *total-effect* index $ST_m$,
which captures the contribution of $X_m$ through its main effect
and all its interactions {cite}`Homma1996`:

$$
ST_m = 1 - \frac{\mathbb{V}_{\boldsymbol{X}_{\sim m}} \left[ \mathbb{E}_{X_m} \left[ Y \mid \boldsymbol{X}_{\sim m} \right] \right]}{\mathbb{V}[Y]}.
$$

### Monte-Carlo estimation

```{warning}
The method implemented here estimates the main-effect and total-effect indices
by Monte-Carlo simulation,
following the most naive and straightforward approach.
It serves only as an illustration and is far from the state of the art
(see, for instance, {cite}`Saltelli2002, Saltelli2010`).

For a proper analysis, use a dedicated sensitivity analysis
and uncertainty quantification package.
```

The Sobol' indices defined above can be estimated directly
by Monte-Carlo simulation.
The most straightforward (though naive and computationally expensive) approach
uses a nested loop to compute the conditional variances
and expectations that appear in both indices.

Take the first-order index of an input variable $X_m$.
The outer loop samples values of $X_m$,
and for each one the inner loop samples values of $\boldsymbol{X}_{\sim m}$
to estimate the conditional expectation $\mathbb{E}_{\boldsymbol{X}_{\sim m}}\[Y \mid X_m]$.

Estimating the first-order index for a single input therefore
costs $N^2$ model evaluations, where $N$ is the Monte-Carlo sample size,
typically between $10^3$ and $10^6$.

{prf:ref}`Brute Force MC First-Order` below illustrates the procedure
to compute the main-effect Sobol' indices.

```{prf:algorithm}
:label: Brute Force MC First-Order

**Inputs** A computational model $\mathcal{M}$,
random input variables $\boldsymbol{X} = \{ X_1, \ldots, X_M \}$,
number of MC sample points $N$

**Output** First-order Sobol' sensitivity indices $S_m$ for $m = 1, \ldots, M$

For $m = 1$ to $M$:

1. $S \leftarrow 0$
2. $Q \leftarrow 0$
3. For $i = 1$ to $N$:

   1. Sample $x_m^{(i)}$ from $X_m$
   2. $T \leftarrow 0$
   3. For $j = 1$ to $N$:

      1. Sample $\boldsymbol{x}_{\sim m}^{(j)}$ from $\boldsymbol{X}_{\sim m}$
      2. $T \leftarrow T + \mathcal{M}(x_m^{(i)}, \boldsymbol{x}_{\sim m}^{(j)})$

   4. $\mathbb{E}_{\boldsymbol{X}_{\sim m}}\left[ Y \mid X_m \right]^{(i)} \leftarrow \frac{1}{N} T$
   5. $S \leftarrow S + \mathbb{E}_{\boldsymbol{X}_{\sim m}}\left[ Y \mid X_m \right]^{(i)}$
   6. $Q \leftarrow Q + \left( \mathbb{E}_{\boldsymbol{X}_{\sim m}}\left[ Y \mid X_m \right]^{(i)} \right)^2$
4. $\mathbb{V}_{X_m} \left[ \mathbb{E}_{\boldsymbol{X}_{\sim m}}\left[ Y \mid X_m \right]\right] \leftarrow \frac{1}{N} Q - \left( \frac{1}{N} S \right)^2$
5. $S_m \leftarrow \frac{\mathbb{V}_{X_m} \left[ \mathbb{E}_{\boldsymbol{X}_{\sim m}}\left[ Y \mid X_m \right]\right]}{\mathbb{V}[Y]}$
```

The output variance $\mathbb{V}[Y]$ used in the algorithm above can be computed
following {prf:ref}`Brute Force Output Variance`.

```{prf:algorithm}
:label: Brute Force Output Variance

**Inputs** A computational model $\mathcal{M}$,
random input variables $\boldsymbol{X}$, number of MC sample points $N$

**Output** Output variance $\mathbb{V}[Y]$

1. $S \leftarrow 0$
2. $Q \leftarrow 0$
3. For $i = 1$ to $N$:

   1. Sample $\boldsymbol{x}^{(i)}$ from $\boldsymbol{X}$
   2. $S \leftarrow S + \mathcal{M}(\boldsymbol{x}^{(i)})$
   3. $Q \leftarrow Q + \left( \mathcal{M}(\boldsymbol{x}^{(i)}) \right)^2$

4. $\mathbb{V}[Y] \leftarrow \frac{1}{N} Q - \left( \frac{1}{N} S \right)^2$
```

A similar Monte-Carlo algorithm computes the total-effect Sobol' indices,
as shown in {prf:ref}`Brute Force MC Total-Effect`.

```{prf:algorithm}
:label: Brute Force MC Total-Effect

**Inputs** A computational model $\mathcal{M}$,
random input variables $\boldsymbol{X} = \{ X_1, \ldots, X_M \}$,
number of MC sample points $N$

**Output** Total-effect Sobol' sensitivity indices $ST_m$
for $m = 1, \ldots, M$

For $m = 1$ to $M$:

1. $S \leftarrow 0$
2. $Q \leftarrow 0$
3. For $i = 1$ to $N$:

   1. Sample $\boldsymbol{x}_{\sim m}^{(i)}$ from $\boldsymbol{X}_{\sim m}$
   2. $T \leftarrow 0$
   3. For $j = 1$ to $N$:

      1. Sample $x_{m}^{(j)}$ from $X_m$
      2. $T \leftarrow T + \mathcal{M}(x_m^{(j)}, \boldsymbol{x}_{\sim m}^{(i)})$

   4. $\mathbb{E}_{X_m}\left[ Y \mid \boldsymbol{X}_{\sim m} \right]^{(i)} \leftarrow \frac{1}{N} T$
   5. $S \leftarrow S + \mathbb{E}_{X_m}\left[ Y \mid \boldsymbol{X}_{\sim m} \right]^{(i)}$
   6. $Q \leftarrow Q + \left( \mathbb{E}_{X_m}\left[ Y \mid \boldsymbol{X}_{\sim m} \right]^{(i)} \right)^2$
4. $\mathbb{V}_{\boldsymbol{X}_{\sim m}} \left[ \mathbb{E}_{X_m}\left[ Y \mid \boldsymbol{X}_{\sim m} \right]\right] \leftarrow \frac{1}{N} Q - \left( \frac{1}{N} S \right)^2$
5. $ST_m \leftarrow 1 - \frac{\mathbb{V}_{\boldsymbol{X}_{\sim m}} \left[ \mathbb{E}_{X_m}\left[ Y \mid \boldsymbol{X}_{\sim m} \right]\right]}{\mathbb{V}[Y]}$
```

These algorithms are implemented below in a Python function that returns
the main-effect and total-effect Sobol' indices
for every input of a computational model.
It assumes a probabilistic input model has been defined,
so that sample points can be drawn from it.

```{margin}
As you shall soon see, every test function in UQTestFuns comes
with a probabilistic input model taken from the literature.
```

```{code-cell}
:tags: [hide-input]

def estimate_sobol_indices(my_func, prob_input, num_sample, rng):
    """Estimate the first-order and total-effect Sobol' indices via MC.

    Parameters
    ----------
    my_func
        The function (or computational model) to analyze.
    prob_input
        The probabilistic input model of the function.
    num_sample
        The Monte-Carlo sample size.
    rng
        An instance of a NumPy random number generator used to draw the
        samples.

    Returns
    -------
    A tuple of two NumPy arrays: the first-order and total-effect Sobol'
    indices, each of length equal to the number of input variables.
    """

    # --- Compute output variance
    xx = prob_input.get_sample(num_sample, rng=rng)
    yy = my_func(xx)
    var_yy = np.var(yy)

    num_dim = prob_input.dimension

    # --- Compute first-order Sobol' indices
    first_order = np.zeros(num_dim)
    for m in range(num_dim):
        xx_m = prob_input.marginals[m].get_sample(num_sample, rng=rng)
        exp_nm = np.zeros(num_sample)
        for i in range(num_sample):
            xx = prob_input.get_sample(num_sample, rng=rng)
            # Replace the m-th column
            xx[:, m] = xx_m[i]
            yy = my_func(xx)
            exp_nm[i] = np.mean(yy)
        var_m = np.var(exp_nm)
        first_order[m] = var_m / var_yy

    # --- Compute total-effect Sobol' indices
    total_effect = np.zeros(num_dim)
    for m in range(num_dim):
        xx = prob_input.get_sample(num_sample, rng=rng)
        exp_m = np.zeros(num_sample)
        for i in range(num_sample):
            xx_m = np.repeat(xx[i:i + 1], num_sample, axis=0)
            xx_m[:, m] = prob_input.marginals[m].get_sample(num_sample, rng=rng)
            yy = my_func(xx_m)
            exp_m[i] = np.mean(yy)
        var_nm = np.var(exp_m)
        total_effect[m] = 1 - var_nm / var_yy

    return first_order, total_effect
```

## Ishigami function

To test the algorithm above,
we use the popular {ref}`Ishigami function <test-functions:ishigami>`
{cite}`Ishigami1991`,
whose sensitivity indices are known analytically.
The function is highly non-linear and non-monotonic, and reads

$$
\mathcal{M}(\boldsymbol{x}) = \sin(x_1) + a \sin^2(x_2) + b , x_3^4 \sin(x_1),
$$

where $\boldsymbol{x} = \{ x_1, x_2, x_3 \}$ collects
the three input variables, defined probabilistically below,
and $a$ and $b$ are the function's parameters.

Create an instance of the Ishigami function:

```{code-cell}
ishigami = uqtf.Ishigami()
```

The input variables are defined probabilistically as shown below:

```{code-cell}
print(ishigami.prob_input)
```

Finally, the default values of the parameters $a$ and $b$ are:

```{code-cell}
print(ishigami.parameters)
```

The variance of the Ishigami function can be derived analytically,
as a function of the parameters:

$$
\mathbb{V}[Y] = \frac{a^2}{8} + \frac{b \pi^4}{5} + \frac{b^2 \pi^8}{18} + \frac{1}{2}.
$$

The sensitivity indices are likewise available in closed form, again as functions of the parameters:

| Input variable |                                    $S_m$                                     |                                                        $ST_m$                                                         |
|:--------------:|:----------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------------------------------------:|
|     $X_1$      | $\frac{1}{\mathbb{V}[Y]} \frac{1}{2} \left( 1 + \frac{b \pi^4}{5} \right)^2$ | $\frac{1}{\mathbb{V}[Y]} \left( \frac{1}{2} \left( 1 + \frac{b \pi^4}{5} \right)^2 + \frac{8 b^2 \pi^8}{225} \right)$ |
|     $X_2$      |                   $\frac{1}{\mathbb{V}[Y]} \frac{a^2}{8}$                    |                                           $\frac{a^2}{8 \, \mathbb{V}[Y]}$                                            |
|     $X_3$      |                                     $0$                                      |                                      $\frac{8 b^2 \pi^8}{225 \, \mathbb{V}[Y]}$                                       |

Notice that although $X_3$ has no main effect of its own
(its main-effect index is zero), it still contributes to the output variance
through its interaction with $X_1$,
reflected in its nonzero total-effect index.
By contrast, $X_2$ has no interaction effect at all:
its main-effect and total-effect indices are equal.

For later comparison, we define a Python function
that returns the analytical Sobol' indices of the Ishigami function:

```{code-cell}
:tags: [hide-input]

def compute_sobol_indices(a, b):
    """Compute the analytical Sobol' indices for the Ishigami function."""

    # --- Compute the variance
    var_y = a**2 / 8 + b * np.pi**4 / 5 + b**2 * np.pi**8 / 18 + 1 / 2

    # --- Compute the first-order Sobol' indices
    first_order = np.zeros(3)
    first_order[0] = (1 + b * np.pi**4 / 5) ** 2 / 2
    first_order[1] = a**2 / 8
    first_order[2] = 0

    # --- Compute the total-effect Sobol' indices
    total_effect = np.zeros(3)
    total_effect[2] = 8 * b**2 * np.pi**8 / 225
    total_effect[1] = first_order[1]
    total_effect[0] = first_order[0] + total_effect[2]

    return first_order / var_y, total_effect / var_y
```

## Sobol' indices estimation

To observe the convergence of the estimation procedure,
we estimate the Sobol' indices at several Monte-Carlo sample sizes.
For reproducibility, we create a random number generator with a fixed seed
and pass it to each call, so the successive estimates draw from a single,
advancing stream:

```{code-cell}
rng = np.random.default_rng(452397)

sample_sizes = np.arange(1000, 5000, 1000)
first_order_indices = np.zeros((len(sample_sizes), ishigami.input_dimension))
total_effect_indices = np.zeros((len(sample_sizes), ishigami.input_dimension))

for i, sample_size in enumerate(sample_sizes):
    first_order_indices[i, :], total_effect_indices[i, :] = estimate_sobol_indices(
        ishigami, ishigami.prob_input, sample_size, rng
    )
```

Compute the analytical values for the given parameters:

```{code-cell}
first_order_ref, total_effect_ref = compute_sobol_indices(
    **ishigami.parameters
)
```

The estimated indices are plotted below against the sample size:
solid lines for the estimates, dashed lines for the analytical values.

```{code-cell}
:tags: [hide-input]

fig, axs = plt.subplots(1, 2, figsize=(10, 5))

axs[0].plot(sample_sizes, first_order_indices[:, 0], color="#e41a1c")
axs[0].plot(sample_sizes, first_order_indices[:, 1], color="#377eb8")
axs[0].plot(sample_sizes, first_order_indices[:, 2], color="#4daf4a")

axs[0].axhline(first_order_ref[0], linestyle="--", color="#e41a1c")
axs[0].axhline(first_order_ref[1], linestyle="--", color="#377eb8")
axs[0].axhline(first_order_ref[2], linestyle="--", color="#4daf4a")

axs[0].set_xscale("log")
axs[0].set_ylim([-0.1, 1])
axs[0].set_title("First-order Sobol' indices")
axs[0].set_xlabel("MC sample size", fontsize=14)
axs[0].set_ylabel("Sensitivity index", fontsize=14)

axs[1].plot(sample_sizes, total_effect_indices[:, 0], color="#e41a1c", label=r"$X_1$")
axs[1].plot(sample_sizes, total_effect_indices[:, 1], color="#377eb8", label=r"$X_2$")
axs[1].plot(sample_sizes, total_effect_indices[:, 2], color="#4daf4a", label=r"$X_3$")

axs[1].axhline(total_effect_ref[0], linestyle="--", color="#e41a1c")
axs[1].axhline(total_effect_ref[1], linestyle="--", color="#377eb8")
axs[1].axhline(total_effect_ref[2], linestyle="--", color="#4daf4a")

axs[1].set_xscale("log")
axs[1].set_ylim([-0.1, 1])
axs[1].set_title("Total-effect Sobol' indices")
axs[1].set_xlabel("MC sample size", fontsize=14)
axs[1].legend()

fig.tight_layout(pad=3.0)
plt.gcf().set_dpi(150);
```

The method estimates the indices reasonably well,
and the estimates converge toward the analytical values
as the sample size grows.
As the nested loop makes clear, though,
that accuracy comes at a steep computational cost:
each additional level of precision multiplies the number of model evaluations.

## Trying another problem

Because `estimate_sobol_indices()` takes the test function
and its probabilistic input as arguments,
nothing in it is specific to the Ishigami function.
To test the method on a different problem, you change a single line.
The {ref}`Sobol'-G <test-functions:sobol-g>` function {cite}`Saltelli1995`
is a good example: it is variable-dimension,
so the same method now also runs at a dimension of your choosing,
with its probabilistic input supplied by the library.

```{code-cell}
sobol_g = uqtf.SobolG(input_dimension=6)

rng = np.random.default_rng(452397)
first_order, total_effect = estimate_sobol_indices(
    sobol_g, sobol_g.prob_input, 1000, rng
)

print(first_order)
print(total_effect)
```

The method code did not change at all; only the function name did.
Every built-in function in UQTestFuns shares the same interface,
so a method designed for one should work for all of them.
See the full list of {ref}`built-in functions <test-functions:available>`

---

## Summary

In this tutorial, you implemented a Monte-Carlo method to estimate
the first-order and total-effect Sobol' indices and tried it out
on the Ishigami function from UQTestFuns.
Because the Ishigami function's indices are known in closed form,
you could verify the implementation directly:
the estimates converged to the exact analytical values as the sample size grew.

This is the role a UQTestFuns test function plays:
a known, well-documented problem against which
you can develop and verify your own sensitivity analysis method
before applying it to a real (possibly much more expensive) computational model.
There, the challenge is to figure out the importance (or non-importance)
of the input variables, qualitatively or quantitatively,
with as few model evaluations as possible.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
