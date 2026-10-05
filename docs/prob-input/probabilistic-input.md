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

(prob-input:probabilistic-input-model)=
# Creating a Probabilistic Input Model

The input of an uncertainty quantification (UQ) test function is modeled probabilistically.
In the case of a multi-dimensional input,
the whole input model is, in essence, a random vector.
Each of the input variables is represented as a (one-dimensional) marginal distribution.
A fully-specified probabilistic input model
then combines all the marginals under some prescribed dependency structures.

```{note}
Currently, UQTestFuns does not support specifying dependency between random variables.
Specifically, all input variables can only be modeled as independent random variables.
```

This page explains how a probabilistic input model can be specified in UQTestFuns.
It assumes some familiarity with {ref}`(one-dimensional) marginal distributions <prob-input:marginal-distribution>`

```{code-cell} ipython3
import matplotlib.pyplot as plt
import numpy as np
import uqtestfuns as uqtf
```

Suppose we want to define the probabilistic input model of a three-dimensional function.
The probabilistic input model is then a three-dimensional random vector
with a joint probability distribution.
The one-dimensional marginal distribution for each of the input variables is shown
in the table below. 

| No. | Name  | Distribution  |                   Parameters                   |
|:---:|:-----:|:-------------:|:----------------------------------------------:|
| 1.  | $X_1$ | Gumbel (max.) |            $\mu = 3.0, \beta = 4.0$            |
| 2.  | $X_2$ |    Normal     |              $\mu=1, \sigma=0.2$               |
| 3.  | $X_3$ |     Beta      | $\alpha = 5.0, \beta = 2.0, a = 0.25, b = 1.0$ |

Moreover, it is assumed that all the input variables are statistically independent.

## One-dimensional marginals

The first step of creating the probabilistic input model is to define
all one-dimensional marginals according to the specification above.
One-dimensional marginals are the distributions
of the component univariate random variables.
In UQTestFuns, the distribution of a univariate random variable is
represented by ``Marginal`` class
(please refer to {ref}`marginal distribution <prob-input:marginal-distribution>` for more detail).
Because three marginals belong to a single probabilistic input model,
we need to collect all the marginals inside a list (or a tuple) as follows:

```{code-cell} ipython3
my_marginals = [
  uqtf.Marginal(
      distribution="gumbel", parameters=[3, 4], name="X1", description="1st input"
  ),
  uqtf.Marginal(
      distribution="normal", parameters=[1, 0.2], name="X2", description="2nd input"
  ),
  uqtf.Marginal(
      distribution="beta", parameters=[5, 2, 0.25, 1.0], name="X3", description="3rd input"
  ),
]
```

Note that in the snippet above,
the parameters `name` and `description` of `Marginal()` are optional.

## A `ProbInput` instance

A probabilistic input model in UQTestFuns is represented
by the {ref}`ProbInput <api_reference_probabilistic_input>`.
To create an instance of the class, you need to pass the following arguments:

- `marginals`: a list or tuple of one-dimensional marginals,
  each represented by an instance of `Marginal`.
- `name`: the name of the probabilistic input model (optional)

Once we define all the marginals,
we create a probabilistic input model as follows:

```{code-cell} ipython3
my_probinput = uqtf.ProbInput(
  marginals=my_marginals,
  name="MyProbInput",
)
```

The variable `my_probinput` now stores
an instance of a probabilistic input model
consisting of three independent random variables.
You can print the instance to the terminal to verify it:

```{code-cell} ipython3
print(my_probinput)
```

An instance of ``Marginal`` exposes the following main properties:

|   Property   |                                                                Description                                                                |
|:------------:|:-----------------------------------------------------------------------------------------------------------------------------------------:|
|    `name`    |                                    the assigned name of the probabilistic input model (may be `None`)                                     |
| `marginals`  |                                   A tuple of one-dimensional marginal distributions of the input model                                    | 
| `dimension`  |                                                the number of dimensions of the input model                                                |
|  `copulas`   | specified copulas that model dependency structure between random variables (currently always the independence copula; see the note above) |

and methods:

|             Method             |                                        Description                                        |
|:------------------------------:|:-----------------------------------------------------------------------------------------:|
| `get_sample(sample_size, rng)` |        get a sample of size `sample_size` from the input with a NumPy PRNG[^prng]         |
|  `transform_from(xx, source)`  | transform a set of sample values `xx` (from a `source` distribution) to this distribution |
|   `transform_to(xx, target)`   |   transform a set of sample values `xx` (of this distribution) to `target` distribution   |

Below, we'll go quickly through each of the methods.

```{important}
In UQTestFuns, one-dimensional probabilistic input models are still represented
as instances of `ProbInput` even though they only have one marginal.
This is because a one-dimensional probabilistic input
and a univariate random variable are conceptually different.
```

## Getting a sample

A random sample of a given size can be generated
from the probabilistic input model using the `get_sample()` method.

For instance, to generate $5$ sample points, type:

```{code-cell} ipython3
xx_sample = my_probinput.get_sample(5)
xx_sample
```

Notice that the sample values are given as a $5$-by-$3$ array.
In general, a sample of size $N$ for an $M$-dimensional probabilistic input model
will be given as an $N$-by-$M$ array.

Shown below is the corner plot from $1'000$ sample points.
The plot shows the histograms for each one-dimensional marginal
as well as the scatter plots for each possible pair.

```{code-cell} ipython3
:tags: [hide-input]

xx_sample = my_probinput.get_sample(1000)

fig, axs = plt.subplots(3, 3, figsize=(6, 6))

axs[0, 1].axis('off')
axs[0, 2].axis('off')
axs[1, 2].axis('off')

axs[0, 0].hist(xx_sample[:, 0], bins="auto", color="#8da0cb")
axs[0, 0].grid()
axs[0, 0].tick_params("x", bottom=False, labelbottom=False)

axs[1, 0].scatter(xx_sample[:, 0], xx_sample[:, 1], marker="x", color="#8da0cb", alpha=0.5)
axs[1, 0].grid()
axs[1, 0].tick_params("x", bottom=False, labelbottom=False)
axs[1, 0].set_ylabel("$X_2$")

axs[1, 1].hist(xx_sample[:, 1], bins="auto", color="#8da0cb")
axs[1, 1].grid()
axs[1, 1].tick_params("y", left=False, labelleft=False)
axs[1, 1].tick_params("x", bottom=False, labelbottom=False)

axs[2, 0].scatter(xx_sample[:, 0], xx_sample[:, 2], marker="x", color="#8da0cb", alpha=0.5)
axs[2, 0].grid()
axs[2, 0].set_xlabel("$X_1$")
axs[2, 0].set_ylabel("$X_3$")

axs[2, 1].scatter(xx_sample[:, 1], xx_sample[:, 2], marker="x", color="#8da0cb", alpha=0.5)
axs[2, 1].grid()
axs[2, 1].tick_params("y", left=False, labelleft=False)
axs[2, 1].set_xlabel("$X_2$")

axs[2, 2].hist(xx_sample[:, 2], bins="auto", color="#8da0cb")
axs[2, 2].grid()
axs[2, 2].tick_params("y", left=False, labelleft=False)
axs[2, 2].set_xlabel("$X_3$")

#fig.tight_layout(pad=1)
plt.gcf().set_dpi(150)
```

## Transforming a sample

Using the `transform_from()` and `transform_to()` methods,
we can transform a sample generated from one probabilistic input model
to another.

Let's suppose we define a three-dimensional probabilistic input model
consisting of three independent standard uniform distributions.

```{code-cell} ipython3
my_marginals_2 = [
  uqtf.Marginal(distribution="uniform", parameters=[0, 1], name="X1", description="1st input"),
  uqtf.Marginal(distribution="uniform", parameters=[0, 1], name="X2", description="2nd input"),
  uqtf.Marginal(distribution="uniform", parameters=[0, 1], name="X3", description="3rd input"),
]
my_probinput_2 = uqtf.ProbInput(
  marginals=my_marginals_2,
  name="MyProbInput-2",
  )
print(my_probinput_2)
```

A sample from this probabilistic input model can be transformed into a sample from our initial input model as follows:

```{code-cell} ipython3
xx_sample_2 = my_probinput_2.get_sample(1000)
xx_sample_1 = my_probinput_2.transform_to(xx_sample_2, my_probinput)
```

The histogram of the transformed sample is shown below.
They look similar to the ones before;
that is, the sample is distributed as if it was generated directly
from the original probabilistic input model.

```{code-cell} ipython3
:tags: [hide-input]

fig, axs = plt.subplots(3, 3, figsize=(6, 6))

axs[0, 1].axis('off')
axs[0, 2].axis('off')
axs[1, 2].axis('off')

axs[0, 0].hist(xx_sample_1[:, 0], bins="auto", color="#8da0cb")
axs[0, 0].grid()
axs[0, 0].tick_params("x", bottom=False, labelbottom=False)

axs[1, 0].scatter(xx_sample_1[:, 0], xx_sample_1[:, 1], marker="x", color="#8da0cb", alpha=0.5)
axs[1, 0].grid()
axs[1, 0].tick_params("x", bottom=False, labelbottom=False)
axs[1, 0].set_ylabel("$X_2$")

axs[1, 1].hist(xx_sample_1[:, 1], bins="auto", color="#8da0cb")
axs[1, 1].grid()
axs[1, 1].tick_params("y", left=False, labelleft=False)
axs[1, 1].tick_params("x", bottom=False, labelbottom=False)

axs[2, 0].scatter(xx_sample_1[:, 0], xx_sample_1[:, 2], marker="x", color="#8da0cb", alpha=0.5)
axs[2, 0].grid()
axs[2, 0].set_xlabel("$X_1$")
axs[2, 0].set_ylabel("$X_3$")

axs[2, 1].scatter(xx_sample_1[:, 1], xx_sample_1[:, 2], marker="x", color="#8da0cb", alpha=0.5)
axs[2, 1].grid()
axs[2, 1].tick_params("y", left=False, labelleft=False)
axs[2, 1].set_xlabel("$X_2$")

axs[2, 2].hist(xx_sample_1[:, 2], bins="auto", color="#8da0cb")
axs[2, 2].grid()
axs[2, 2].tick_params("y", left=False, labelleft=False)
axs[2, 2].set_xlabel("$X_3$")

#fig.tight_layout(pad=1)
plt.gcf().set_dpi(150)
```

### Transforming to and from a canonical domain

Beyond transforming between two probabilistic input models, `transform_to()`
and `transform_from()` also accept a plain domain tuple as `target`/`source`,
defaulting to $(-1, 1)^M$ (i.e., the same bounds for all dimensions).
This is arguably the more common case in practice.

Many sampling schemes (Latin hypercube sampling, for instance) generate
points on a canonical domain like $[-1, 1]^M$ or $[0, 1]^M$, which then need
to be mapped into the model's actual input domain before the test function
can be evaluated.

Conversely, many metamodeling techniques are built on a
canonical domain, so samples in the physical input space need to be mapped
the other way before being used to fit or query the metamodel.

Suppose a set of points has been generated on the canonical $[-1, 1]^3$
domain by an external sampling scheme (a uniform random sample stands in
for one here):

```{code-cell} ipython3
rng = np.random.default_rng(42)
xx_canonical = rng.uniform(-1, 1, size=(5, 3))
xx_canonical
```

These can be mapped into `my_probinput`'s own domain with `transform_from()`,
ready to evaluate a test function on:

```{code-cell} ipython3
xx_original = my_probinput.transform_from(xx_canonical)  # source is (-1.0, 1.0)^M by default
xx_original
```

Going the other way, for example, to prepare physical-domain samples for a
metamodel built on $[-1, 1]$, use `transform_to()`:

```{code-cell} ipython3
xx_canonical_2 = my_probinput.transform_to(xx_original)  # target is (-1.0, 1.0)^M by default
xx_canonical_2
```

Notice that the transformation returns the same sample points as the original.

## Next steps

You now know how to build a probabilistic input model, sample from it, and
transform samples between two models. A `ProbInput` on its own, however,
only represents the *input* side of a UQ test function; combined with an
evaluation function (and, optionally, a set of parameters), it becomes a
full {ref}`UQTestFun <api_reference_uqtestfun>` instance. See
{ref}`Create a Custom Test Function <getting-started:tutorial-custom-functions>`
for how to put these pieces together.

[^prng]: The `rng` argument accepts either a NumPy `numpy.random.Generator`
instance directly or an integer used as a seed to construct one. If
omitted, a fresh, unseeded generator is used, so consecutive calls without
an explicit `rng` are not reproducible.
