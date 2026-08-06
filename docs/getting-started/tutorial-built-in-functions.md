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

(getting-started:tutorial-built-in-functions)=
# Tutorial: Create Built-in Test Functions

UQTestFuns includes a wide range of test functions from the uncertainty
quantification community; these are the _built-in test functions_.

This tutorial gives you an overview of them. You'll learn what the built-in
test functions are, the common interface they share, and their important
properties and methods.

By the end, you'll be able to create any test function available in
UQTestFuns and use its basic but essential functionality.

UQTestFuns is designed to work with minimal dependencies within the numerical
Python ecosystem. It mainly requires NumPy and SciPy.

To follow along with this tutorial, import NumPy alongside UQTestFuns:

```{code-cell} ipython3
import numpy as np
import uqtestfuns as uqtf
```

## Listing available test functions

To list all the test functions currently available:

```{code-cell} ipython3
:tags: ["output_scroll"]

uqtf.list_functions()
```

The output lists each test function along with its constructor,
input dimension, typical applications, and a short description.

## A Callable instance

Take, for instance, the {ref}`borehole <test-functions:borehole>` function
{cite}`Harper1983`. It's an eight-dimensional test function widely used in
metamodeling and sensitivity analysis exercises.

To instantiate it, call the constructor:

```{code-cell} ipython3
my_testfun = uqtf.Borehole()
```

Print the instance to see some basic information about it:

```{code-cell} ipython3
print(my_testfun)
```

```{margin}
Think of a `Callable` as a regular function: it takes some inputs,
evaluates them, and produces some outputs. In other words, you _call_ it
with arguments.
```

The resulting object is a `Callable`. It can be evaluated on a set of input
values.

For example, the borehole function can be evaluated at a single point
(a 1-by-8 array):

```{code-cell} ipython3
xx = np.array([
  [
    1.04803586e-01, 2.54527756e+03, 9.44572869e+04, 9.94988176e+02,
    6.31793993e+01, 7.63308791e+02, 1.57530252e+03, 1.00591588e+04
  ]
])
my_testfun(xx)
```

```{note}
Calling the function on a set of input values automatically checks
that the input is correct (both its dimensionality and its bounds).

The test function also accepts vectorized input: an $N$-by-$M$ array,
where $N$ and $M$ are the number of points and dimensions.
```

## Probabilistic input

In general, the results of uncertainty quantification (UQ) analyses depend
on the specified probabilistic input.

When a test function appears in the literature, it usually comes
with a specification for its probabilistic input.
In UQTestFuns, this input model is an integral part of each test function.

For instance, the borehole function has probabilistic input model consisting
of eight independent random variables. The model is stored in the `prob_input`
property of the instance.
Print it to see the full specification:

```{code-cell} ipython3
print(my_testfun.prob_input)
```

```{note}
_Copulas_ models the statistical dependence structure between the component
(univariate) marginals.

Currently, UQTestFuns does not support probabilistic input models with
dependence structure.
```

From the input model, you can randomly generate a set of input values,
which is often useful for verification and validation. For instance,
to generate $10,000$ sample points:

```{code-cell} ipython3
xx_sample = my_testfun.prob_input.get_sample(10000)
yy_sample = my_testfun(xx_sample)
```

The histogram of the output values is shown below:

```{code-cell} ipython3
:tags: [hide-input]

import matplotlib.pyplot as plt

plt.hist(yy_sample, bins="auto", color="#8da0cb")
plt.grid()
plt.xlabel(r"$\mathcal{M}(\mathbf{X})$")
plt.ylabel("Counts [-]")
plt.gcf().set_dpi(150);
```

```{note}
By default, sampling uses a fresh RNG seeded from system entropy. To make
sampling reproducible, pass `rng` to `get_sample()`. It accepts a seed
(an integer), an existing NumPy generator, or `None` to fall back to the
[NumPy default random generator](https://numpy.org/doc/stable/reference/random/generator.html#numpy.random.default_rng).

See this [blog post](https://albertcthomas.github.io/good-practices-random-number-generators/)
on good practices for using NumPy's RNG.
```

Often you only need the output values, not the inputs that produced them.
For that case, the test function offers a shortcut: calling `get_sample()`
directly on the instance returns the output values in one step.

```{code-cell} ipython3
yy_sample = my_testfun.get_sample(10000)
```

This is exactly the two steps above composed into one. With the same `rng`,
the two approaches produce identical results:

```{code-cell} ipython3
assert np.array_equal(
    my_testfun.get_sample(10000, rng=42),
    my_testfun(my_testfun.prob_input.get_sample(10000, rng=42)),
)
```

## Transforming a sample into the function domain

Some UQ methods produce sample points in a hypercube domain
(for example, $[0, 1]^M$ or $[-1, 1]^M, where $M$ is the number of input
dimensions) at which the function should be evaluated.

This hypercube domain may differ from the test function's domain.
Before the function can be evaluated, those values must first be transformed
to the function domain.

```{margin}
The transformation is _isoprobabilistic_: each value is mapped so that its
position in the source distribution (i.e., its quantile) is preserved in the
target distribution. In other words, equal probability in,
equal probability out.
```

The probabilistic input instance provides `transform_from()` method for this:
it brings a sample from a source domain into the input model's own domain.
For instance, suppose we have a sample of size $5$ in $[-1, 1]^8$
for the borehole function:

```{code-cell} ipython3
rng_1 = np.random.default_rng(42)
xx_sample_dom_1 = rng_1.uniform(low=-1, high=1, size=(5, 8))
xx_sample_dom_1
```

Transform these values into the function's domain with `transform_from()`:

```{code-cell} ipython3
xx_sample_trans_1 = my_testfun.prob_input.transform_from(xx_sample_dom_1)
xx_sample_trans_1
```

By default, the method assumes the input values lie in $[-1, 1]^M$. You can
also transform values from another uniform domain by passing `source`.

For example, take sample values in $[0, 1]^8$, the unit hypercube:

```{code-cell} ipython3
rng_2 = np.random.default_rng(42)
xx_sample_dom_2 = rng_2.random((5, 8))
xx_sample_dom_2
```

These transform into the borehole function's domain as follows:

```{code-cell} ipython3
xx_sample_trans_2 = my_testfun.prob_input.transform_from(
    xx_sample_dom_2, source=(0.0, 1.0)
)
xx_sample_trans_2
```

For a given sample, the bounds of the hypercube domain must be the same in
all dimensions.

The two transformed samples should match, since we generated both
from the default RNG with the same seed:

```{code-cell} ipython3
assert np.allclose(xx_sample_trans_1, xx_sample_trans_2)
assert np.allclose(my_testfun(xx_sample_trans_1), my_testfun(xx_sample_trans_2))
```

## Test functions with parameters

```{margin}
Parameters of a test function can be anything: numerical values, flags,
strings, and so on.
```

Some test functions are _parameterized_. Alongside the probabilistic input,
they carry a set of fixed values called _parameters_.

It helps to be clear about how a parameter differs from an input. The
probabilistic input is the uncertain part of the problem: you put
distributions over it, sample from it, and propagate it through the function.

A parameter is not uncertain. It is part of the model's definition, a fixed
value that shapes how the function computes without ever being sampled.

Changing a parameter does not draw a new realization. It changes which
function you are studying.

Take the {ref}`Ishigami <test-functions:ishigami>` function
{cite}`Ishigami1991`, defined as:

$$
\mathcal{M}(\boldsymbol{x}) = \sin{(x_1)} + a \sin^2{(x_2)} + b x_3^4 \sin{(x_1)}
$$

The coefficients $a$ and $b$ are its parameters. The three $x_i$ are its
uncertain inputs. Before the function can be evaluated, $a$ and $b$ must be
assigned values.

When you instantiate a function from the library, its parameters come
pre-loaded with values from a published source. Print the parameters to see
them:

```{code-cell} ipython3
my_testfun = uqtf.Ishigami()

print(my_testfun.parameters)
```

These values are reference points. They make your results reproducible against
the literature, and they are what gives the name `Ishigami1991` its meaning.

For that reason, the library protects them. You cannot change the parameter
values on a function you obtained directly from the library:

```{code-cell} ipython3
:tags: [raises-exception]

my_testfun.parameters["a"] = 10.0
```

### Choosing a published parameter set

Some functions ship with more than one published set of parameters.
You can select one by name at construction with `parameters_id`:

```{code-cell} ipython3
my_testfun = uqtf.Ishigami(parameters_id="Sobol1999")
```

To see which sets are available for a function, use `list_parameters`,
which also lists the current values:

```{code-cell} ipython3
uqtf.list_parameters("Ishigami")
```

### Experimenting with your own values

When you want to experiment, sweep a value, try a variant, see what happens at
the edges, start from a copy. Copying a published set gives you a working
version that is yours to edit:

```{code-cell} ipython3
my_params = uqtf.Ishigami().parameters.copy()
```

A copy is no longer the published set, so the library does not protect it.
Pass it to the constructor to build a function that uses it:

```{code-cell} ipython3
my_testfun = uqtf.Ishigami(parameters=my_params)
```

The result is still an Ishigami function, the same mathematical model,
evaluated at parameter values you control. From here, change values directly
through the function:

```{code-cell} ipython3
my_testfun.parameters["a"] = 10.0
```

The function uses the updated value the next time you call it.

### How parameters change the function

Recall that changing a parameter changes which function you are studying. Two
parameter values give two different Ishigami functions, and they need not have
the same output variance, as the figure below illustrates.

We build one experimental instance from a copy, then sweep `b` through it:

```{code-cell} ipython3
my_testfun = uqtf.Ishigami(parameters=uqtf.Ishigami().parameters.copy())
xx_sample = my_testfun.prob_input.get_sample(10000)

my_testfun.parameters["b"] = 0.05
yy_param_1 = my_testfun(xx_sample)

my_testfun.parameters["b"] = 0.35
yy_param_2 = my_testfun(xx_sample)
```

```{code-cell} ipython3
:tags: [hide-input]

plt.hist(yy_param_2, bins="auto", color="#fc8d62", label="parameter 2")
plt.hist(yy_param_1, bins="auto", color="#66c2a5", label="parameter 1")
plt.grid()
plt.xlabel(r"$\mathcal{M}(\mathbf{X})$")
plt.ylabel("Counts [-]")
plt.legend(fontsize=14)
plt.gcf().set_dpi(150);
```

## Test functions with variable dimension

Some test functions support a _variable dimension_, meaning an instance can be
constructed for any number (positive integer, please) of input dimensions.

Consider the {ref}`Sobol'-G <test-functions:sobol-g>` function
{cite}`Saltelli1995`, a popular choice in sensitivity analysis whose dimension
you can vary. It is defined as:

$$
\mathcal{M}(\boldsymbol{x}) = \prod_{m = 1}^M \frac{\lvert 4 x_m - 2 \rvert + a_m}{1 + a_m}
$$

where $\boldsymbol{x} = \{ x_1, \ldots, x_M \}$ is the $M$-dimensional vector of
input variables, and $\boldsymbol{a} = \{ a_1, \ldots, a_M \}$ are parameters of
the function.

To create a six-dimensional Sobol'-G function with the default selection
of parameter values,
pass the desired dimensionality  through `input_dimension`:

```{code-cell} ipython3
my_testfun = uqtf.SobolG(input_dimension=6)
```

Verify that the function is indeed six-dimensional:

```{code-cell} ipython3
print(my_testfun)
```

and that its probabilistic input has six marginals:

```{code-cell} ipython3
print(my_testfun.prob_input)
```

## Where to go next

You now can list all the built-in test functions, create any of them,
inspect its probabilistic input, generate a sample, transform a sample into
the function's domain, and work with parameters and variable dimensions.
That covers the common interface every built-in function shares.

This tutorial stayed with the basics, the functions themselves, and how to
handle them. It did not touch the UQ analysis they are typically built for,
nor how to build a function that is not in the library.

From here:

- {ref}`Test a Sensitivity Analysis Method <getting-started:tutorial-sensitivity>`,
  to put these functions to work in sensitivity analysis.
- {ref}`Test a Reliability Analysis Method <getting-started:tutorial-reliability>`,
  to use them in reliability analysis.
- {ref}`Create a Custom Function <getting-started:tutorial-custom-functions>`,
  to define a test function of your own.

## References

```{bibliography}
:style: unsrtalpha
:filter: docname in docnames
```
